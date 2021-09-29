from datetime import datetime
import time
from threading import Timer
from server.error import ValueError, AccessError
import server.data as data
import server.auth as auth

#####   CONSTANTS   #####

_REACT_ID_LIST = [1]

#####   CORE FUNCTIONS   #####

def send(token, channel_id, message):
    if channel_id not in data.channels:
        raise ValueError(description="You are attempting to send a message to an invalid channel")

    u_id = auth.validate_token(token)

    if u_id not in data.channels[channel_id]['members']:
        raise AccessError(description=f"You need to have joined the channel {data.channels[channel_id]['name']} to send messages to it")

    if len(message) > 1000:
        raise ValueError(description="Your message is more than 1000 characters")

    # remove leading and trailing spaces (frontend guarantees text)
    message = message.strip()
    new_message = create_message(channel_id, u_id, message)
    send_messages(channel_id, new_message)

    return {'message_id': new_message['message_id']}

def sendlater(token, channel_id, message, time_sent_unix):
    if channel_id not in data.channels:
        raise ValueError(description="You are attempting to send a message to an invalid channel")

    u_id = auth.validate_token(token)

    if u_id not in data.channels[channel_id]['members']:
        raise AccessError(description=f"You need to have joined the channel {data.channels[channel_id]['name']} to send messages to it")

    if len(message) > 1000:
        raise ValueError(description="Your message is more than 1000 characters")

    time_difference = time_sent_unix - time.time()
    if time_difference < 0:
        time_sent = convert_time(time_sent_unix)
        raise ValueError(description=f"You are trying to send a message at {time_sent} which is in the past")

    # remove leading and trailing spaces (frontend guarantees text)
    message = message.strip()
    new_message = create_message(channel_id, u_id, message)

    # start timeout before message is sent
    message_send_timer = Timer(time_difference, send_messages, [channel_id, new_message])
    message_send_timer.start()

    return {'message_id': new_message['message_id']}

@data.save(['messages'])
def remove(token, message_id):
    u_id = auth.validate_token(token)
    found_message = find_message(message_id)

    if not found_message:
        raise ValueError(description="You are attempting to delete a message which no longer exists")

    channel_id, selected_message = found_message['channel_id'], found_message['message']

    if u_id != selected_message['u_id'] and data.users[u_id]['permission_id'] == data._PERMISSION_MEMBER:
        raise AccessError(description="You need to be the original poster, or be an admin/owner of the channel/slackr to remove the message")

    data.messages[channel_id].remove(selected_message)

    return {}

@data.save(['messages'])
def edit(token, message_id, message):
    u_id = auth.validate_token(token)
    found_message = find_message(message_id)
    selected_message = found_message['message']

    if u_id != selected_message['u_id'] and data.users[u_id]['permission_id'] == data._PERMISSION_MEMBER:
        raise AccessError(description="You need to be the original poster, or be an admin/owner of the channel/slackr to edit the message")

    # remove leading and trailing spaces
    message = message.strip()
    if message:
        selected_message['message'] = message
    else:
        remove(token, message_id)

    return {}

@data.save(['messages'])
def react(token, message_id, react_id):
    found_message = find_message(message_id)

    if not found_message:
        raise ValueError(description="You are attempting to react to a message that does not exist")

    selected_message = found_message['message']

    if react_id not in _REACT_ID_LIST:
        raise ValueError(description="You have used an invalid react")

    selected_react = next((react for react in selected_message['reacts'] if react['react_id'] == react_id), None)

    u_id = auth.validate_token(token)

    if selected_react and u_id in selected_react['u_ids']:
        raise ValueError(description="You are attempting to react to a message which you have already reacted to")

    if selected_react:
        selected_react['u_ids'].append(u_id)
    else:
        selected_message['reacts'].append(create_react(u_id, react_id))

    return {}

@data.save(['messages'])
def unreact(token, message_id, react_id):
    found_message = find_message(message_id)

    if not found_message:
        raise ValueError(description="You are attempting to react to a message that does not exist")

    selected_message = found_message['message']

    if react_id not in _REACT_ID_LIST:
        raise ValueError(description="You have used an invalid react")

    selected_react = next((react for react in selected_message['reacts'] if react['react_id'] == react_id), None)

    u_id = auth.validate_token(token)

    if not selected_react or u_id not in selected_react['u_ids']:
        raise ValueError(description="You are attempting to unreact to a message which you have not reacted to")

    selected_react['u_ids'].remove(u_id)

    # no users have used this react
    if not selected_react['u_ids']:
        selected_message['reacts'].remove(selected_react)

    return {}

@data.save(['messages'])
def pin(token, message_id):
    u_id = auth.validate_token(token)
    found_message = find_message(message_id)

    if not found_message:
        raise ValueError(description="You are attempting to pin a message that does not exist")

    channel_id, selected_message = found_message['channel_id'], found_message['message']

    if u_id not in data.channels[channel_id]['members']:
        raise AccessError(description="You need to have joined the channel to pin messages to it")

    if data.users[u_id]['permission_id'] == data._PERMISSION_MEMBER:
        raise ValueError(description="You need to be an admin/owner of the slackr to pin messages to channels")

    if selected_message['is_pinned']:
        raise ValueError(description="You are attempting to pin a message which has already been pinned")

    selected_message['is_pinned'] = True

    return {}

@data.save(['messages'])
def unpin(token, message_id):
    u_id = auth.validate_token(token)
    found_message = find_message(message_id)

    if not found_message:
        raise ValueError(description="You are attempting to unpin a message that does not exist")

    channel_id, selected_message = found_message['channel_id'], found_message['message']

    if u_id not in data.channels[channel_id]['members']:
        raise AccessError(description="You need to have joined the channel to unpin messages from it")

    if data.users[u_id]['permission_id'] == data._PERMISSION_MEMBER:
        raise ValueError(description="You need to be an admin/owner of the slackr to unpin messages from channels")

    if not selected_message['is_pinned']:
        raise ValueError(description="You are attempting to unpin a message which has not been pinned")

    selected_message['is_pinned'] = False

    return {}

# given a query_str, return all messages with that string
def search(token, query_str):
    u_id = auth.validate_token(token)

    messages = []
    for channel_id in data.messages:
        if u_id in data.channels[channel_id]['members']:
            messages += [message for message in data.messages[channel_id] if query_str in message['message']]

    return {'messages': messages}

#####   HELPER FUNCTIONS   #####

@data.save(['messages'])
def send_messages(channel_id, message):
    message['time_created'] = int(time.time())
    data.messages[channel_id].insert(0, message)

def find_message(message_id):
    for channel_id in data.messages:
        message = next((message for message in data.messages[channel_id] if message['message_id'] == message_id), None)
        if message:
            return {
                'channel_id': channel_id,
                'message': message
            }
    return None

def generate_message_id(channel_id):
    channel_pos = len(data.messages[channel_id]) + 1
    curr_time = int(time.time())
    message_id = int(f"{channel_id}{channel_pos}{curr_time}")
    return message_id

def convert_time(time_unix):
    time_date = datetime.fromtimestamp(time_unix)
    time_24h = time.strptime(time_date.strftime("%H:%M"), "%H:%M")
    time_12h = time.strftime("%I:%M %p", time_24h)
    return time_12h

def create_message(channel_id, u_id, message):
    new_message = {
        'message_id': generate_message_id(channel_id),
        'u_id': u_id,
        'message': message,
        'time_created': 0,
        'reacts': [],
        'is_pinned': False
    }
    return new_message

def create_react(u_id, react_id):
    new_react = {
        'react_id': react_id,
        'u_ids': [u_id],
        'is_this_user_reacted': True
    }
    return new_react
