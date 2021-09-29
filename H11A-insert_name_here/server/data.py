import pickle
import os
import time

_PERMISSION_OWNER = 1
_PERMISSION_ADMIN = 2
_PERMISSION_MEMBER = 3

_CURR_DIR = os.path.dirname(os.path.abspath(__file__))
_USERS_DIR = _CURR_DIR + "/storage/users.p"
_CHANNELS_DIR = _CURR_DIR + "/storage/channels.p"
_MESSAGES_DIR = _CURR_DIR + "/storage/messages.p"
_CODES_DIR = _CURR_DIR + "/storage/codes.p"

_USERS = "users"
_CHANNELS = "channels"
_MESSAGES = "messages"
_CODES = "codes"

users = {
    # 1: {
    #   'email':'abc@gmail.com',
    #   'password':'5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
    #   'name_first':'a',
    #   'name_last': 'b',
    #   'handle_str': 'ab',
    #   'permission_id': 1,
    #   'tokens': []
    # }
}

channels = {
    # 1: {
    #   'name': "dfksaghdios",
    #   'is_public': True,
    #   'members': [1,2,6],
    #   'owners': []
    # }
}

messages = {
    # channel_id: [{
    #       message_id,
    #       u_id,
    #       message,
    #       time_created,
    #       reacts,
    #       is_pinned
    # }]
}

reset_codes = {
    # code: {
    #     email,
    #     time
    # }
}

def init_users():
    global users
    try:
        with open(_USERS_DIR, 'rb') as file:
            users = pickle.load(file)
    except FileNotFoundError:
        users = {}

def save_users():
    mode = 'ab' if not os.path.exists(_USERS_DIR) else 'wb'
    with open(_USERS_DIR, mode) as file:
        pickle.dump(users, file)

def init_channels():
    global channels
    try:
        with open(_CHANNELS_DIR, 'rb') as file:
            channels = pickle.load(file)
    except FileNotFoundError:
        channels = {}

def save_channels():
    mode = 'ab' if not os.path.exists(_CHANNELS_DIR) else 'wb'
    with open(_CHANNELS_DIR, mode) as file:
        pickle.dump(channels, file)

def init_messages():
    global messages
    try:
        with open(_MESSAGES_DIR, 'rb') as file:
            messages = pickle.load(file)
    except FileNotFoundError:
        messages = {}

def save_messages():
    mode = 'ab' if not os.path.exists(_MESSAGES_DIR) else 'wb'
    with open(_MESSAGES_DIR, mode) as file:
        pickle.dump(messages, file)

def init_codes():
    global reset_codes
    try:
        with open(_CODES_DIR, 'rb') as file:
            reset_codes = pickle.load(file)
    except FileNotFoundError:
        reset_codes = {}

def save_codes():
    global reset_codes

    # clear expired reset codes
    for code in reset_codes.copy():
        if time.time() > reset_codes[code]['time']:
            del reset_codes[code]

    mode = 'ab' if not os.path.exists(_CODES_DIR) else 'wb'
    with open(_CODES_DIR, mode) as file:
        pickle.dump(reset_codes, file)

def save(to_save):
    def save_decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            for data in to_save:
                if data == _USERS:
                    save_users()
                elif data == _CHANNELS:
                    save_channels()
                elif data == _MESSAGES:
                    save_messages()
                elif data == _CODES:
                    save_codes()
            return result
        return wrapper
    return save_decorator
