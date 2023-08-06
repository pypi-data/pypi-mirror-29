from django.conf import settings
from django.utils import timezone

import requests

class NeoAction(object):
    WELCOME = 'Welcome to Neo\n\n'
    RELEASE = {'Type': 'Release'}
    INVALID_INPUT = 'Invalid input.'
    INVALID_OPTION = 'Invalid option.'

    def __init__(self, session, message):
        self.session = session
        self.message = message

    @staticmethod
    def error(message):
        r = NeoAction.RELEASE
        r.update({'Message': 'Error - ' + message})
        return r

    @staticmethod
    def response(message):
        r = {'Type': 'Response'}
        r.update({'Message': message})
        return r
    
    @staticmethod
    def release(message):
        r = NeoAction.RELEASE
        r.update({'Message': message})
        return r

    @staticmethod
    def paginate(session, title, string, nav):
        lst = string.split('\n')
        page_stop = session.get_page_stop()
        suffix = 'm. More\nb. Back'

        if page_stop == None:
            # This is the beginning of the string. No previous page.
            page_stop = -1

        page_elements_length = len(title + '\n' + suffix)
        page_length = settings.MSG_LENGTH - page_elements_length
        if len(string) > page_length:
            new_string = ''
            sub_lst = lst[page_stop+1:]

            if nav in ['b', 'B']:
                s = 0
                sub_lst = []
                for i, v in reversed(list(enumerate(lst[0:page_stop+1]))):
                    s += len(v + '\n')
                    sub_lst.insert(0, v)
                    if s > page_length:
                        s -= len(v + '\n')
                        session.set_page_stop(i)
                        sub_lst = sub_lst[1:]
                        break

            # print page_stop, sub_lst

            for index, value in enumerate(sub_lst):
                new_string += value + '\n'
                if len(new_string) > page_length:
                    new_string = new_string[:-len(value + '\n')]
                    if page_stop > 0:
                        if nav in ['b', 'B']:
                            page_stop = page_stop - index
                        else:
                            page_stop = page_stop + index
                    else:
                        page_stop = index - 1
                    session.set_page_stop(page_stop)
                    break
            return '{}{}{}{}'.format(title, '\n', new_string, suffix)

        return '{}{}{}'.format(title, '\n', string)

    @staticmethod
    def set_selector_and_nav(session, message):
        nav = None
        # Save selector in session
        try:
            selector = int(message)
        except ValueError:
            if message in ['M', 'm', 'B', 'b']:
                nav = message
            else:
                return NeoAction.release(NeoAction.INVALID_OPTION)
        else:
            session.set_selector(selector)

        return nav

    @staticmethod
    def get_time(timestamp):
        return int(timestamp.strftime('%-H%M%S'))

    @staticmethod
    def msg_invalid(message):
        return not message or message.startswith('*') or message == 'User timeout'

    @staticmethod
    def singular_or_plural(quantity, word):
        if quantity == 1:
            return '1 ' + word
        return str(quantity) + ' ' + word + 's'

    @staticmethod
    def send_sms(phone_number, message):
        params = settings.SMS_PARAMS
        params.update({'Content': message, 'To': '+233' + phone_number[1:]})
        requests.get(settings.SMS_URL, params)

def build_session_args(data, other_initiator):
    is_agent = data.get('is_agent', None)
    phone_number = '0' + data['Mobile'][3:]

    if not is_agent:
        return other_initiator, False, {
            'phone_number': phone_number,
            'service_code': data['ServiceCode'],
            'operator': data['Operator'],
        }

    return 'agent', True, {
        'phone_number': phone_number,
        'service_code': data['ServiceCode'],
        'operator': data['Operator'],
        'actor_first_name': data['first_name'],
        'actor_last_name': data['last_name']
    }

def create_activate_deactivate_object(model_class, action, **kwargs):
    if action == 'create':
        model_class.objects.create(**kwargs)
    else:
        obj = model_class.objects.get(**kwargs)
        if action == 'deac':
            if obj.is_active:
                obj.is_active = False
        elif action == 'act':
            if not obj.is_active:
                obj.is_active = True
        obj.save()

    return {'message': 'Success!'}

def get_step(session, curr_seq):
    seq_at_menu = session.get_sequence_at_menu()
    parts = session.get_init_message().split('*')

    # if initiation message is a shortcut, add 1 to step
    if len(parts) == 4:
        return (curr_seq - seq_at_menu) + 1

    return curr_seq - seq_at_menu

def get_init_menu(first_name, is_agent, menu_dict):
    if first_name:
        s = '{} {}.'.format('Hi', first_name)
    else:
        s = 'Hi.'

    if is_agent:
        return '{} {}'.format(s, menu_dict['agent'])
    keys = menu_dict.keys()
    keys.remove('agent')
    return '{} {}'.format(s, menu_dict[keys[0]])

def perform_action(actions, steps, step, session, message, initiator, has_menu=True):
    if not has_menu:
        option = 1
    else:
        # Set option if not already set
        option = session.get_menu_option()

    if len(message) == 1 and option == None:
        try:
            option = int(message)
        except ValueError:
            # Message is not an integer, return error
            return NeoAction.error(NeoAction.INVALID_INPUT)
        else:
            # Message is an integer, set message as option
            session.set_menu_option(message)

    step_at_paged = session.get_step_at_paged()

    # Check whether user selected valid option
    try:
        instance = actions[initiator][option](session, message)
    except KeyError:
        return NeoAction.error(NeoAction.INVALID_OPTION)

    if message in ['m', 'M', 'b', 'B']:
        # Set step_at_paged
        if not step_at_paged:
            session.set_step_at_paged(step-1)
        return getattr(instance, session.get_or_create()[0].method)() 

    # Set (new) step
    if step_at_paged:
        step = step_at_paged + 1

    # Set step_at_paged and page_stop to None
    session.set_page_stop(None)
    session.set_step_at_paged(None)

    return steps[str(step)](instance, initiator, option)

def perform_init_action(actions, steps, session, sequence, message, initiator, actor_first_name, is_agent, menu=None):
    if not menu:
        session.set_sequence_at_menu(0)
        step = get_step(session, int(sequence))
        has_menu = False
    else:
        session.set_sequence_at_menu(sequence)

    selection = message.split('*')[-1:]
    if len(selection[0]) == 2:
        # If agent dialled shortcut e.g. *711*78*2#
        message = selection[0][0]
        step = 1
        # return Response(perform_action(step, session, message, initiator))
        return perform_action(actions, steps, step, session, message, initiator)

    # Agent dialled normal code e.g. *711*78#
    if menu:
        return NeoAction.response(get_init_menu(actor_first_name, is_agent, menu))
    return perform_action(actions, steps, step, session, message, initiator, has_menu=has_menu)