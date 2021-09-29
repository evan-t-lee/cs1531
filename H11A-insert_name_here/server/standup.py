import time
from threading import Timer
from server.error import ValueError, AccessError
import server.data as data
import server.auth as auth
import server.message as message

#####   GLOBALS   #####

standup = {}

#####  CORE FUNCTIONS   #####

def start(token, channel_id, length):
    global standup

    auth.validate_token(token)

    if channel_id not in data.channels:
        raise ValueError(description="You are attempting to start a standup in an invalid channel")

    if channel_id in standup:
        raise ValueError(description="There is already an active standup in the channel you're currently in")

    time_finish = int(time.time()) + length

    standup[channel_id] = {
        'messages': [],
        'time_finish': time_finish
    }

    standup_message_timer = Timer(length, send_messages, [token, channel_id])
    standup_message_timer.start()

    return {'time_finish': time_finish}

def active(token, channel_id):
    auth.validate_token(token)

    channel_id = int(channel_id)

    if channel_id not in data.channels:
        raise ValueError(description="This channel is not valid")

    time_finish = standup[channel_id]['time_finish'] if channel_id in standup else None
    return {
        'is_active': channel_id in standup,
        'time_finish': time_finish
    }

def send(token, channel_id, message_text):
    global standup

    u_id = auth.validate_token(token)

    if channel_id not in data.channels:
        raise ValueError(description="You are attempting to send a standup message to an invalid channel")

    if u_id not in data.channels[channel_id]['members']:
        raise AccessError(description="You need to have joined the channel to send a standup message to it")

    if channel_id not in standup:
        raise ValueError(description="There is no active standup in the channel you're currently in")

    if message_text.startswith("/standup"):
        raise ValueError(description="There is already an active standup in the channel you're currently in")

    if len(message_text) > 1000:
        raise ValueError(description="Your message is more than 1000 characters")

    standup[channel_id]['messages'] += [f"{data.users[u_id]['handle_str']}: {message_text}"]

    return {}

#####   HELPER FUNCTIONS   #####

def send_messages(token, channel_id):
    global standup

    message_text = '\n'.join(standup[channel_id]['messages'])

    if message_text:
        message.send(token, channel_id, message_text)

    del standup[channel_id]
