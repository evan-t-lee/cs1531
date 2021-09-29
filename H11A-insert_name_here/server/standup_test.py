import time
import pytest
import server.standup as standup
import server.auth as auth
import server.channel as channel
from server.error import ValueError, AccessError

#####   CONSTANTS   #####

_INVALID_VALUE = -1
_TIME = 'time'
_STANDUP_LENGTH = 5
_STANDUP_SHORT = 1
_MARGIN = 0.5

#####   SETUP   #####

try:
    USER = auth.register(
        'yespleasework@gmail.com',
        'this1passw0rd',
        'yes',
        'please')
except ValueError:
    USER = auth.login('yespleasework@gmail.com', 'this1passw0rd')

TOKEN = USER['token']
CHANNEL = channel.create(TOKEN, 'name', True)
CHANNEL_ID = CHANNEL['channel_id']

#####   TEST SUITES   #####

def test_standup_start_errors():
    with pytest.raises(ValueError) as error:
        standup.start(TOKEN, _INVALID_VALUE, _STANDUP_LENGTH)
    assert str(error.value) == '400 Bad Request: You are attempting to start a standup in an invalid channel'

    with pytest.raises(AccessError) as error:
        standup.start(_INVALID_VALUE, CHANNEL_ID, _STANDUP_LENGTH)
    assert str(error.value) == '400 Bad Request: Token is invalid'

def test_standup_send_errors():
    with pytest.raises(AccessError) as error:
        standup.send(_INVALID_VALUE, CHANNEL_ID, "test")
    assert str(error.value) == '400 Bad Request: Token is invalid'

    with pytest.raises(ValueError) as error:
        standup.send(TOKEN, CHANNEL_ID, "message")
    assert str(error.value) == "400 Bad Request: There is no active standup in the channel you're currently in"

    with pytest.raises(ValueError) as error:
        standup.send(TOKEN, _INVALID_VALUE, "message")
    assert str(error.value) == '400 Bad Request: You are attempting to send a standup message to an invalid channel'

    user1 = auth.login("user1@gmail.com", "user1pass")
    with pytest.raises(AccessError) as error:
        standup.send(user1['token'], CHANNEL_ID, "hello")
    assert str(error.value) == '400 Bad Request: You need to have joined the channel to send a standup message to it'

def test_active_errors():
    with pytest.raises(AccessError) as error:
        standup.active(_INVALID_VALUE, CHANNEL_ID)
    assert str(error.value) == '400 Bad Request: Token is invalid'

    with pytest.raises(ValueError) as error:
        standup.active(TOKEN, _INVALID_VALUE)
    assert str(error.value) == "400 Bad Request: This channel is not valid"

def test_standup_no_messages():
    time_finish = standup.start(TOKEN, CHANNEL_ID, _STANDUP_SHORT)['time_finish']
    assert standup.active(TOKEN, CHANNEL_ID) == {
        'is_active': True,
        "time_finish": time_finish
    }

    time.sleep(_STANDUP_SHORT + _MARGIN)

    assert len(channel.messages(TOKEN, CHANNEL_ID, 0)['messages']) == 0
    assert standup.active(TOKEN, CHANNEL_ID) == {
        'is_active': False,
        "time_finish": None
    }

def test_mid_standup_errors():
    time_finish = standup.start(TOKEN, CHANNEL_ID, _STANDUP_LENGTH)['time_finish']

    with pytest.raises(ValueError) as error:
        standup.send(TOKEN, CHANNEL_ID, "/standup 10")
    assert str(error.value) == "400 Bad Request: There is already an active standup in the channel you're currently in"

    with pytest.raises(ValueError) as error:
        standup.send(TOKEN, CHANNEL_ID, "yo"*501)
    assert str(error.value) == "400 Bad Request: Your message is more than 1000 characters"

    assert standup.active(TOKEN, CHANNEL_ID) == {
        'is_active': True,
        "time_finish": time_finish
    }

    with pytest.raises(ValueError) as error:
        standup.start(TOKEN, CHANNEL_ID, _STANDUP_LENGTH)
    assert str(error.value) == "400 Bad Request: There is already an active standup in the channel you're currently in"

# note this function continues from the standup started
# in the previous test
def test_standup_success():
    user1 = auth.login("user1@gmail.com", "user1pass")
    channel.join(user1['token'], CHANNEL_ID)

    assert standup.send(TOKEN, CHANNEL_ID, "lorem") == {}
    assert standup.send(user1['token'], CHANNEL_ID, "ipsum") == {}

    time.sleep(_STANDUP_LENGTH + _MARGIN)

    assert standup.active(TOKEN, CHANNEL_ID) == {
        'is_active': False,
        "time_finish": None
    }

    curr_messages = channel.messages(TOKEN, CHANNEL_ID, 0)['messages']
    assert len(curr_messages) == 1
    assert curr_messages[0]['message'] == "yesplease: lorem\nuser1: ipsum"
