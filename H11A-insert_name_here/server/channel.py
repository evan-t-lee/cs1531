from server.error import AccessError, ValueError
import server.auth as auth
import server.data as data

#####   CORE FUNCTIONS   #####

# invites a user if the caller is an owner
@data.save(['channels'])
def invite(token, channel_id, u_id):
    validate_u_id(u_id)
    caller_id = auth.validate_token(token) # tell between user added and caller
    valid_channel_id(channel_id)
    is_channel_member(caller_id, channel_id)
    not_channel_member(u_id, channel_id)

    # add u_id to members list and to owners if an owner
    data.channels[channel_id]['members'].append(u_id)
    if is_slackr_admin(u_id):
        data.channels[channel_id]['owners'].append(u_id)

    return {}

# returns details of the channel
def details(token, channel_id):
    u_id = auth.validate_token(token)
    valid_channel_id(channel_id)
    is_channel_member(u_id, channel_id)

    owners = data.channels[channel_id]['owners']
    owners_list = [{
        'u_id': o,
        'name_first': data.users[o]['name_first'],
        'name_last': data.users[o]['name_last'],
        'profile_img_url': data.users[o]['profile_img_url']
    } for o in owners]

    members = data.channels[channel_id]['members']
    members_list = [{
        'u_id': m,
        'name_first': data.users[m]['name_first'],
        'name_last': data.users[m]['name_last'],
        'profile_img_url': data.users[m]['profile_img_url']
    } for m in members]

    return {
        'name': data.channels[channel_id]['name'],
        'owner_members': owners_list,
        'all_members': members_list
    }

# returns 50 messages from the channel
def messages(token, channel_id, start):
    valid_channel_id(channel_id)
    u_id = auth.validate_token(token)
    is_channel_member(u_id, channel_id)
    message_len = len(data.messages[channel_id])
    if message_len == 0 and start == 0:
        return {'messages': [], 'start': 0, 'end': -1}
    if start >= message_len:
        raise ValueError(description='Start is equal or greater than number of messages')
    message_return = []
    i = 0
    while i < 50 and start + i < message_len:
        reacts = []
        for react in data.messages[channel_id][start + i]['reacts']:
            reacts.append({
                'react_id': react['react_id'],
                'u_ids': react['u_ids'],
                'is_this_user_reacted': u_id in react['u_ids']
                })
        message_return.append({
            'message_id': data.messages[channel_id][start + i]['message_id'],
            'message': data.messages[channel_id][start + i]['message'],
            'u_id': data.messages[channel_id][start + i]['u_id'],
            'time_created': data.messages[channel_id][start + i]['time_created'],
            'reacts': reacts,
            'is_pinned': data.messages[channel_id][start + i]['is_pinned']
            })
        i += 1
    if start + i < message_len:
        end = start + i
    else:
        end = -1
    return {'messages': message_return, 'start': start, 'end': end}

# caller member gets removed from the channel
@data.save(['channels'])
def leave(token, channel_id):
    u_id = auth.validate_token(token)
    valid_channel_id(channel_id)
    is_channel_member(u_id, channel_id)

    data.channels[channel_id]['members'].remove(u_id)
    if u_id in data.channels[channel_id]['owners']:
        data.channels[channel_id]['owners'].remove(u_id)

    return {}

# caller immediately joins channel if permitted or not already a member
@data.save(['channels'])
def join(token, channel_id):
    # channel exists and is not private
    u_id = auth.validate_token(token)
    valid_channel_id(channel_id)
    if not data.channels[channel_id]['is_public']:
        if data.users[u_id]['permission_id'] == data._PERMISSION_MEMBER:
            raise AccessError(description="Channel is private")
    not_channel_member(u_id, channel_id)

    if is_slackr_admin(u_id):
        data.channels[channel_id]['owners'].append(u_id)

    data.channels[channel_id]['members'].append(u_id)

    return {}

# change member in channel to an owner
@data.save(['channels'])
def addowner(token, channel_id, u_id):
    owner = auth.validate_token(token)
    valid_channel_id(channel_id)
    validate_u_id(u_id)
    is_channel_member(u_id, channel_id)

    if u_id in data.channels[channel_id]['owners']:
        raise ValueError(description="The user is already an owner of this channel")
    is_channel_member(u_id, channel_id)

    # check that the token belongs to an owner of the channel
    if owner not in data.channels[channel_id]['owners']:
        raise AccessError(description="The authorised user is not an owner of this channel")

    data.channels[channel_id]['owners'].append(u_id)

    return {}

# removes owner from the owners list
@data.save(['channels'])
def removeowner(token, channel_id, u_id):
    owner = auth.validate_token(token)
    valid_channel_id(channel_id)
    if u_id not in data.channels[channel_id]['owners']:
        raise ValueError(description="The user is not an owner of this channel")

    if owner not in data.channels[channel_id]['owners']:
        raise AccessError(description="The authorised user is not an owner of this channel")

    #slackr owners and admins cannot be removed from the owners list
    if data.users[u_id]['permission_id'] != data._PERMISSION_MEMBER:
        raise ValueError(description="Owners and admins of the Slackr must be an owner of this channel")

    data.channels[channel_id]['owners'].remove(u_id)

    return {}

# return channels that the user is part of
def list(token):
    u_id = auth.validate_token(token)
    user_list = []
    for k in data.channels.keys():
        if u_id in data.channels[k]['members']:
            user_list.append(channel_list_dict(k))

    return {'channels': user_list}

# return all channels that the user is part of and channels that are public
def listall(token):
    channel_l = []
    auth.validate_token(token)

    for k in data.channels.keys():
        channel_l.append(channel_list_dict(k))
    return {'channels': channel_l}

# create a channel and add the calling user as the owner
@data.save(['channels', 'messages'])
def create(token, name, is_public):
    u_id = auth.validate_token(token)
    # check that the name is shorter than 20 characters
    if len(name) > 20:
        raise ValueError(description="Name is longer than 20 characters")
    keys = data.channels.keys()
    if len(keys) == 0:
        channel_id = 1
    else:
        channel_id = max(keys) + 1

    # update channel and set messages to empty list
    update_created_channels(name, is_public, channel_id, u_id)
    data.messages[channel_id] = []

    return {'channel_id': channel_id}

#####   HELPER FUNCTIONS   #####

# creates a dictionary for the create function is appended to the global
def update_created_channels(name, is_public, channel_id, u_id):
    channel_dict = {
        'name': name,
        'is_public': is_public,
        'channel_id': channel_id,
        'members': [u_id],
        'owners': [u_id]
    }
    data.channels[channel_id] = channel_dict

#Checks the id is part of the data
def valid_channel_id(channel_id):
    if channel_id not in data.channels.keys():
        raise ValueError(description="This channel ID does not match a valid channel")

#Abstraction of repeated lengthy check for slackr admin or owner
def is_slackr_admin(u_id):
    return data.users[u_id]['permission_id'] == data._PERMISSION_OWNER or data.users[u_id]['permission_id'] == data._PERMISSION_ADMIN

#Validates u_id in keys
def validate_u_id(u_id):
    if u_id not in data.users.keys():
        raise ValueError(description='User ID does not refer to a valid user')

#Check if the u_id is already in the channel
def not_channel_member(u_id, channel_id):
    if u_id in data.channels[channel_id]['members']:
        raise ValueError(description='Already part of channel')

#Assure that the u_id is not in the channel
def is_channel_member(u_id, channel_id):
    if u_id not in data.channels[channel_id]['members']:
        raise AccessError(description='User is not a member of the channel')

def channel_list_dict(channel_id):
    return {
        'channel_id': channel_id,
        'name': data.channels[channel_id]['name']
    }
