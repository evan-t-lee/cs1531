import time
import pytest
from server.error import ValueError, AccessError
import server.data as data
import server.message as message
import server.auth as auth
import server.channel as channel

#####   CONSTANTS   #####

_INVALID_VALUE = -1
_MINUTE = 60
_DELAY_TIME = 5 # delay time for sendlater, keep < 10

_EMPTY_MESSAGE = ""
_STANDUP_MESSAGE = "/standup"
_TEST_MESSAGE1 = "lorem ipsum"
_TEST_MESSAGE2 = "dolor sit"
_LONG_MESSAGE = "*" * 1001

_PAST_TIME_UNIX = 1546300800 # 2019-01-01 00:00
_VALID_REACT_ID = 1

#####   SETUP   #####

# create owner user (all perms)
try:
    auth_data = auth.register("johnsmith101@gmail.com", "UsydUnsw101", "John", "Smith")
except ValueError:
    auth_data = auth.login("johnsmith101@gmail.com", "UsydUnsw101")
u_id_owner, token_owner = auth_data['u_id'], auth_data['token']

_CHANNEL1 = channel.create(token_owner, 'test_channel1', True)['channel_id']
_CHANNEL2 = channel.create(token_owner, 'test_channel2', True)['channel_id']

# create member user (limited perms)
try:
    auth_data = auth.register("rakazaa@outlook.com", "SbhsSghs2020", "Karen", "Green")
except ValueError:
    auth_data = auth.login("rakazza@outlook.com", "SbhsSghs2020")
u_id_member, token_member = auth_data['u_id'], auth_data['token']

try:
    channel.join(token_member, _CHANNEL1)
except ValueError:
    pass

# create dummy user (no perms)
try:
    auth_data = auth.register("puppy1909@hotmail.com", "HSC99.95atar", "David", "Wang")
except ValueError:
    auth_data = auth.login("puppy1909@hotmail.com", "HSC99.95atar")
u_id_dummy, token_dummy = auth_data['u_id'], auth_data['token']

#####   TEST SUITES   #####

def test_send_success():
    # sending message as owner
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']

    newest_message = data.messages[_CHANNEL1][0]
    assert message_id == newest_message['message_id']
    assert newest_message['message'] == _TEST_MESSAGE1
    assert newest_message['u_id'] == u_id_owner

    # sending message as member
    message_id = message.send(token_member, _CHANNEL1, _TEST_MESSAGE2)['message_id']

    newest_message = data.messages[_CHANNEL1][0]
    assert message_id == newest_message['message_id']
    assert newest_message['message'] == _TEST_MESSAGE2
    assert newest_message['u_id'] == u_id_member

def test_send_invalid_channel():
    # sending message to a non-existent channel
    with pytest.raises(ValueError) as error:
        message.send(token_member, _INVALID_VALUE, _TEST_MESSAGE1)
    assert str(error.value) == "400 Bad Request: You are attempting to send a message to an invalid channel"

    # sending message to a channel you haven't joined
    with pytest.raises(AccessError) as error:
        message.send(token_dummy, _CHANNEL1, _TEST_MESSAGE1)
    assert str(error.value) == f"400 Bad Request: You need to have joined the channel {data.channels[_CHANNEL1]['name']} to send messages to it"

    with pytest.raises(AccessError) as error:
        message.send(token_member, _CHANNEL2, _TEST_MESSAGE2)
    assert str(error.value) == f"400 Bad Request: You need to have joined the channel {data.channels[_CHANNEL2]['name']} to send messages to it"

def test_send_invalid_message():
    # sending a message over 1000 characters
    with pytest.raises(ValueError) as error:
        message.send(token_owner, _CHANNEL1, _LONG_MESSAGE)
    assert str(error.value) == "400 Bad Request: Your message is more than 1000 characters"

    with pytest.raises(ValueError) as error:
        message.send(token_member, _CHANNEL1, _LONG_MESSAGE)
    assert str(error.value) == "400 Bad Request: Your message is more than 1000 characters"

# sendlater is being test with a set delay time
def test_sendlater():
    valid_time = int(time.time()) + _DELAY_TIME
    # sendlater as owner
    message_id = message.sendlater(token_owner, _CHANNEL1, _TEST_MESSAGE1, valid_time)['message_id']
    time.sleep(_DELAY_TIME + 0.5) # 0.5 buffer time

    newest_message = data.messages[_CHANNEL1][0]
    assert message_id == newest_message['message_id']
    assert newest_message['time_created'] == valid_time
    assert newest_message['message'] == _TEST_MESSAGE1
    assert newest_message['u_id'] == u_id_owner

def test_sendlater_invalid_channel():
    valid_time = time.time() + _MINUTE

    # sendlater to a non-existent channel
    with pytest.raises(ValueError) as error:
        message.sendlater(token_owner, _INVALID_VALUE, _TEST_MESSAGE1, valid_time)
    assert str(error.value) == "400 Bad Request: You are attempting to send a message to an invalid channel"

    # sendlater to a channel you haven't joined
    with pytest.raises(AccessError) as error:
        message.sendlater(token_dummy, _CHANNEL1, _TEST_MESSAGE1, valid_time)
    assert str(error.value) == f"400 Bad Request: You need to have joined the channel {data.channels[_CHANNEL1]['name']} to send messages to it"

    with pytest.raises(AccessError) as error:
        message.sendlater(token_member, _CHANNEL2, _TEST_MESSAGE1, valid_time)
    assert str(error.value) == f"400 Bad Request: You need to have joined the channel {data.channels[_CHANNEL2]['name']} to send messages to it"

def test_sendlater_invalid_message():
    valid_time = time.time() + _MINUTE

    # sendlater a message over 1000 characters
    with pytest.raises(ValueError) as error:
        message.sendlater(token_owner, _CHANNEL1, _LONG_MESSAGE, valid_time)
    assert str(error.value) == "400 Bad Request: Your message is more than 1000 characters"

    with pytest.raises(ValueError) as error:
        message.sendlater(token_member, _CHANNEL1, _LONG_MESSAGE, valid_time)
    assert str(error.value) == "400 Bad Request: Your message is more than 1000 characters"

def test_sendlater_invalid_time():
    past_time = message.convert_time(_PAST_TIME_UNIX) # convert to sec

    # sendlater for a past date
    with pytest.raises(ValueError) as error:
        message.sendlater(token_owner, _CHANNEL1, _TEST_MESSAGE1, _PAST_TIME_UNIX)
    assert str(error.value) == f"400 Bad Request: You are trying to send a message at {past_time} which is in the past"

    with pytest.raises(ValueError) as error:
        message.sendlater(token_member, _CHANNEL1, _TEST_MESSAGE1, _PAST_TIME_UNIX)
    assert str(error.value) == f"400 Bad Request: You are trying to send a message at {past_time} which is in the past"

def test_remove_success():
    # send messsage as owner
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']
    # remove message as owner
    message.remove(token_owner, message_id)

    assert not next((message for message in data.messages[_CHANNEL1] if message['message_id'] == message_id), None)

    # send messsage as member
    message_id = message.send(token_member, _CHANNEL1, _TEST_MESSAGE1)['message_id']
    # remove message as member
    message.remove(token_member, message_id)

    assert not next((message for message in data.messages[_CHANNEL1] if message['message_id'] == message_id), None)

def test_remove_invalid_message():
    # removing non-existent message
    with pytest.raises(ValueError) as error:
        message.remove(token_owner, _INVALID_VALUE)
    assert str(error.value) == "400 Bad Request: You are attempting to delete a message which no longer exists"

def test_remove_insufficient_perms():
    # send message as owner
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']

    # removing message you don't have perms to
    with pytest.raises(AccessError) as error:
        message.remove(token_dummy, message_id)
    assert str(error.value) == "400 Bad Request: You need to be the original poster, or be an admin/owner of the channel/slackr to remove the message"

    with pytest.raises(AccessError) as error:
        message.remove(token_member, message_id)
    assert str(error.value) == "400 Bad Request: You need to be the original poster, or be an admin/owner of the channel/slackr to remove the message"

def test_edit_success():
    # send message as owner
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']
    # edit message as owner
    message.edit(token_owner, message_id, _TEST_MESSAGE2)

    edited_message = next(message for message in data.messages[_CHANNEL1] if message['message_id'] == message_id)
    assert edited_message['message'] == _TEST_MESSAGE2

def test_edit_remove():
    # send message as owner
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']
    # edit message to empty as owner
    message.edit(token_owner, message_id, _EMPTY_MESSAGE)

    assert not next((message for message in data.messages[_CHANNEL1] if message['message_id'] == message_id), None)

def test_edit_chain():
    # send message as member
    message_id = message.send(token_member, _CHANNEL1, _TEST_MESSAGE1)['message_id']
    # edit message as owner
    message.edit(token_owner, message_id, _TEST_MESSAGE2)

    edited_message = next(message for message in data.messages[_CHANNEL1] if message['message_id'] == message_id)
    assert edited_message['message'] == _TEST_MESSAGE2

    # edit message as member
    message.edit(token_member, message_id, _TEST_MESSAGE1)

    assert edited_message['message'] == _TEST_MESSAGE1

    # edit message to empty as member
    message.edit(token_member, message_id, _EMPTY_MESSAGE)

    assert not next((message for message in data.messages[_CHANNEL1] if message['message_id'] == message_id), None)


def test_edit_insufficient_perms():
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']

    # editing message you don't have perms to
    with pytest.raises(AccessError) as error:
        message.edit(token_member, message_id, _TEST_MESSAGE2)
    assert str(error.value) == "400 Bad Request: You need to be the original poster, or be an admin/owner of the channel/slackr to edit the message"

    with pytest.raises(AccessError) as error:
        message.edit(token_dummy, message_id, _TEST_MESSAGE2)
    assert str(error.value) == "400 Bad Request: You need to be the original poster, or be an admin/owner of the channel/slackr to edit the message"

def test_react_success():
    # send message as owner
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']
    # react to message as owner
    message.react(token_owner, message_id, _VALID_REACT_ID)

    reacts = next(message for message in data.messages[_CHANNEL1] if message['message_id'] == message_id)['reacts']
    react = next(react for react in reacts if react['react_id'] == _VALID_REACT_ID)
    react_ids = [react['react_id'] for react in reacts]
    assert _VALID_REACT_ID in react_ids
    assert u_id_owner in react['u_ids']
    assert react['is_this_user_reacted']

    # react to message as member
    message.react(token_member, message_id, _VALID_REACT_ID)

    assert _VALID_REACT_ID in react_ids
    assert u_id_member in react['u_ids']
    assert react['is_this_user_reacted']

def test_react_invalid_message():
    with pytest.raises(ValueError) as error:
        message.react(token_owner, _INVALID_VALUE, _VALID_REACT_ID)
    assert str(error.value) == "400 Bad Request: You are attempting to react to a message that does not exist"

def test_react_invalid_react():
    # send message
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']

    # reacting with invalid react
    with pytest.raises(ValueError) as error:
        message.react(token_owner, message_id, _INVALID_VALUE)
    assert str(error.value) == "400 Bad Request: You have used an invalid react"

    message.react(token_owner, message_id, _VALID_REACT_ID)
    # reacting redundantly
    with pytest.raises(ValueError) as error:
        message.react(token_owner, message_id, _VALID_REACT_ID)
    assert str(error.value) == "400 Bad Request: You are attempting to react to a message which you have already reacted to"

def test_unreact_success():
    # send message as owner
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']
    # react to message as owner
    message.react(token_owner, message_id, _VALID_REACT_ID)

    # unreact to message as owner
    message.unreact(token_owner, message_id, _VALID_REACT_ID)

    reacts = next(message for message in data.messages[_CHANNEL1] if message['message_id'] == message_id)['reacts']
    react_ids = [react['react_id'] for react in reacts]
    assert _VALID_REACT_ID not in react_ids

def test_unreact_chain():
    # send message as owner
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']
    # react to message as owner
    message.react(token_owner, message_id, _VALID_REACT_ID)
    # react to message as member
    message.react(token_member, message_id, _VALID_REACT_ID)

    # unreact to message as owner
    message.unreact(token_owner, message_id, _VALID_REACT_ID)

    reacts = next(message for message in data.messages[_CHANNEL1] if message['message_id'] == message_id)['reacts']
    react = next(react for react in reacts if react['react_id'] == _VALID_REACT_ID)
    react_ids = [react['react_id'] for react in reacts]
    assert _VALID_REACT_ID in react_ids
    assert u_id_owner not in react['u_ids']
    assert u_id_member in react['u_ids']

    # unreact to message as member
    message.unreact(token_member, message_id, _VALID_REACT_ID)

    assert not reacts


def test_unreact_invalid_message():
    with pytest.raises(ValueError) as error:
        message.unreact(token_owner, _INVALID_VALUE, _VALID_REACT_ID)
    assert str(error.value) == "400 Bad Request: You are attempting to react to a message that does not exist"

def test_unreact_invalid_react():
    # send message as owner
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']
    # react to message as owner
    message.react(token_owner, message_id, _VALID_REACT_ID)

    # unreacting with invalid react
    with pytest.raises(ValueError) as error:
        message.unreact(token_owner, message_id, _INVALID_VALUE)
    assert str(error.value) == "400 Bad Request: You have used an invalid react"

    message.unreact(token_owner, message_id, _VALID_REACT_ID)
    # unreacting redundantly
    with pytest.raises(ValueError) as error:
        message.unreact(token_owner, message_id, _VALID_REACT_ID)
    assert str(error.value) == "400 Bad Request: You are attempting to unreact to a message which you have not reacted to"

def test_pin_success():
    # send message as owner
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']
    # pin message as owner
    message.pin(token_owner, message_id)

    pinned_message = next(message for message in data.messages[_CHANNEL1] if message['message_id'] == message_id)
    assert pinned_message['is_pinned']

    # send message as member
    message_id = message.send(token_member, _CHANNEL1, _TEST_MESSAGE1)['message_id']
    # pin message as owner
    message.pin(token_owner, message_id)

    pinned_message = next(message for message in data.messages[_CHANNEL1] if message['message_id'] == message_id)
    assert pinned_message['is_pinned']


def test_pin_invalid_message():
    with pytest.raises(ValueError) as error:
        message.pin(token_owner, _INVALID_VALUE)
    assert str(error.value) == "400 Bad Request: You are attempting to pin a message that does not exist"

def test_pin_insufficient_perms():
    # send message as owner
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']

    # pinning message without being in channel
    with pytest.raises(AccessError) as error:
        message.pin(token_dummy, message_id)
    assert str(error.value) == "400 Bad Request: You need to have joined the channel to pin messages to it"

    # pinning message without perms
    with pytest.raises(ValueError) as error:
        message.pin(token_member, message_id)
    assert str(error.value) == "400 Bad Request: You need to be an admin/owner of the slackr to pin messages to channels"

def test_pin_redundant():
    # send message as owner
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']
    # pin message as owner
    message.pin(token_owner, message_id)

    # pinning redundantly
    with pytest.raises(ValueError) as error:
        message.pin(token_owner, message_id)
    assert str(error.value) == "400 Bad Request: You are attempting to pin a message which has already been pinned"

def test_unpin_success():
    # send message as owner
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']
    # pin message as owner
    message.pin(token_owner, message_id)

    # unpin message as owner
    message.unpin(token_owner, message_id)

    pinned_message = next(message for message in data.messages[_CHANNEL1] if message['message_id'] == message_id)
    assert not pinned_message['is_pinned']

    # send message as member
    message_id = message.send(token_member, _CHANNEL1, _TEST_MESSAGE1)['message_id']
    # pin message as owner
    message.pin(token_owner, message_id)

    # unpin message as owner
    message.unpin(token_owner, message_id)

    pinned_message = next(message for message in data.messages[_CHANNEL1] if message['message_id'] == message_id)
    assert not pinned_message['is_pinned']

def test_unpin_invalid_message():
    with pytest.raises(ValueError) as error:
        message.unpin(token_owner, _INVALID_VALUE)
    assert str(error.value) == "400 Bad Request: You are attempting to unpin a message that does not exist"

def test_unpin_insufficient_perms():
    # send message as owner
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']
    # pin message as owner
    message.pin(token_owner, message_id)

    # unpinning message without perms
    with pytest.raises(AccessError) as error:
        message.unpin(token_dummy, message_id)
    assert str(error.value) == "400 Bad Request: You need to have joined the channel to unpin messages from it"

    # unpinning message without perms
    with pytest.raises(ValueError) as error:
        message.unpin(token_member, message_id)
    assert str(error.value) == "400 Bad Request: You need to be an admin/owner of the slackr to unpin messages from channels"

def test_unpin_redudant():
    # send message as owner
    message_id = message.send(token_owner, _CHANNEL1, _TEST_MESSAGE1)['message_id']
    # pin message as owner
    message.pin(token_owner, message_id)
    # unpin message as owner
    message.unpin(token_owner, message_id)

    # unpinning redundantly
    with pytest.raises(ValueError) as error:
        message.unpin(token_owner, message_id)
    assert str(error.value) == "400 Bad Request: You are attempting to unpin a message which has not been pinned"

def test_search():
    messages = message.search(token_owner, 'lorem')['messages']
    assert len(messages) == 17
    messages = message.search(token_owner, 'ipsum')['messages']
    assert len(messages) == 17
    messages = message.search(token_owner, 'lorem ipsum')['messages']
    assert len(messages) == 17

    message.send(token_member, _CHANNEL1, 'lorem')

    messages = message.search(token_member, 'lorem')['messages']
    assert len(messages) == 18
    messages = message.search(token_member, 'ipsum')['messages']
    assert len(messages) == 17
    messages = message.search(token_member, 'lorem ipsum')['messages']
    assert len(messages) == 17
