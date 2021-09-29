import pytest

from server.error import AccessError, ValueError
import server.data as data
import server.channel as channel
import server.auth as auth
import server.message as message

#####   SETUP   #####

# owner user
try:
    owner_data = auth.register("johnsmith101@gmail.com", "UsydUnsw101", "John", "Smith")
except ValueError:
    owner_data = auth.login("johnsmith101@gmail.com", "UsydUnsw101")
owner_u_id = owner_data['u_id']
owner_token = owner_data['token']

# user 1
try:
    user_1_dict = auth.register("user1@gmail.com", "user1pass", "User", "1")
except ValueError:
    user_1_dict = auth.login("user1@gmail.com", "user1pass")
user_1_id = user_1_dict['u_id']
user_1_token = user_1_dict['token']

# user 2
try:
    user_2_dict = auth.register("user2@gmail.com", "user2pass", "User", "2")
except ValueError:
    user_2_dict = auth.login("user2@gmail.com", "user2pass")
user_2_id = user_2_dict['u_id']
user_2_token = user_2_dict['token']

#####   TEST SUITES   #####

# test invalid details being used for channel invitations ##
# testing when user isn't in the channel
def test_invite_not_member():
    channel_id = channel.create(user_1_token, "Channel 1", True)['channel_id']

    with pytest.raises(AccessError) as error:
        channel.invite(user_2_token, channel_id, user_1_id)
    assert str(error.value) == "400 Bad Request: User is not a member of the channel"

# testing when the u_id is invalid
def test_invite_u_id_invalid():
    channel_id = channel.create(user_1_token, "Channel 1", True)['channel_id']
    with pytest.raises(ValueError) as error:
        channel.invite(user_1_token, channel_id, 5438752398759834)
    assert str(
        error.value) == "400 Bad Request: User ID does not refer to a valid user"

    with pytest.raises(ValueError) as error:
        channel.invite(user_1_token, channel_id, 3.14)
    assert str(
        error.value) == "400 Bad Request: User ID does not refer to a valid user"

    with pytest.raises(ValueError) as error:
        channel.invite(user_1_token, channel_id, -10)
    assert str(
        error.value) == "400 Bad Request: User ID does not refer to a valid user"

# testing when the channel_id is invalid
def test_invite_channel_invalid():
    channel.create(user_1_token, "Channel 1", True)
    with pytest.raises(ValueError) as error:
        channel.invite(user_1_token, -11, user_2_id)
    assert str(error.value) == "400 Bad Request: This channel ID does not match a valid channel"

    with pytest.raises(ValueError) as error:
        channel.invite(user_1_token, 10.96, user_2_id)
    assert str(error.value) == "400 Bad Request: This channel ID does not match a valid channel"

# testing if the invited u_id is already a member
def test_invite_already_member():
    channel_id = channel.create(user_1_token, "Channel 1", True)['channel_id']
    channel.invite(user_1_token, channel_id, user_2_id)
    with pytest.raises(ValueError) as error:
        channel.invite(user_1_token, channel_id, user_2_id)
    assert str(error.value) == "400 Bad Request: Already part of channel"

# slackr owner invite test
def test_invite_valid_owner():
    channel_id = channel.create(user_1_token, "Channel 1", True)['channel_id']
    assert channel.invite(user_1_token, channel_id, owner_u_id) == {}
    assert len(data.channels[channel_id]['owners']) == 2

## simultaneously test invite and details functions##
# test details of channel with only the owner user
def test_invite_details_one():
    # setup
    channel_id = channel.create(user_1_token, "Channel 2", True)['channel_id']
    # end setup

    details = channel.details(user_1_token, channel_id)
    assert details['name'] == "Channel 2"
    assert len(details['owner_members']) == 1
    assert details['all_members'][0] == {
        "u_id": user_1_id,
        "name_first": "User",
        "name_last": "1",
        "profile_img_url": ""
    }
    assert len(details['all_members']) == 1
    assert details['all_members'][0] == {
        "u_id": user_1_id,
        "name_first": "User",
        "name_last": "1",
        "profile_img_url": ""
    }

# test details of channel with 2 members
def test_invite_details_two():
    # setup
    channel_id = channel.create(user_1_token, "Channel 2", True)['channel_id']
    channel.invite(user_1_token, channel_id, user_2_id)
    # setup End

    details = channel.details(user_1_token, channel_id)
    assert details['name'] == "Channel 2"
    assert len(details['owner_members']) == 1
    assert details['owner_members'][0] == {
        "u_id": user_1_id,
        "name_first": "User",
        "name_last": "1",
        "profile_img_url": ""
    }
    assert len(details['all_members']) == 2
    assert details['all_members'][0] == {
        "u_id": user_1_id,
        "name_first": "User",
        "name_last": "1",
        "profile_img_url": ""
    }
    assert details['all_members'][1] == {
        "u_id": user_2_id,
        "name_first": "User",
        "name_last": "2",
        "profile_img_url": ""
    }

# test details of channel with 3 members
def test_invite_details_three():
    # setup
    channel_id = channel.create(user_1_token, "Channel 2", True)['channel_id']
    channel.invite(user_1_token, channel_id, user_2_id)
    try:
        user_3_dict = auth.register("user3@gmail.com", "user3pass", "User", "3")
    except ValueError:
        user_3_dict = auth.login("user3@gmail.com", "user3pass")
    user_3_id = user_3_dict['u_id']
    channel.invite(user_1_token, channel_id, user_3_id)
    # setup end

    details = channel.details(user_1_token, channel_id)
    assert len(details['owner_members']) == 1
    assert details['owner_members'][0] == {
        "u_id": user_1_id,
        "name_first": "User",
        "name_last": "1",
        "profile_img_url": ""
    }
    assert len(details['all_members']) == 3
    assert details['all_members'][0] == {
        "u_id": user_1_id,
        "name_first": "User",
        "name_last": "1",
        "profile_img_url": ""
    }
    assert details['all_members'][1] == {
        "u_id": user_2_id,
        "name_first": "User",
        "name_last": "2",
        "profile_img_url": ""
    }
    assert details['all_members'][2] == {
        "u_id": user_3_id,
        "name_first": "User",
        "name_last": "3",
        "profile_img_url": ""
    }

# testing value and access errors in details
def test_details_access_errors():
    # setup
    channel.create(user_1_token, "Channel 2", True)
    # end setup

    with pytest.raises(ValueError) as error:
        channel.details(user_1_token, -1)
    assert str(error.value) == "400 Bad Request: This channel ID does not match a valid channel"

    with pytest.raises(ValueError) as error:
        channel.details(user_1_token, 10.96)
    assert str(error.value) == "400 Bad Request: This channel ID does not match a valid channel"

# Errors - Invalid token
def test_details_invalid_token():
    # setup
    channel_id = channel.create(user_1_token, "Channel 2", True)['channel_id']
    # end setup

    with pytest.raises(AccessError) as error:
        channel.details(-1, channel_id)
    assert str(error.value) == "400 Bad Request: Token is invalid"

## test the retrieval of channel messages##
# test when the user isn't a member of the channel
def test_messages_not_member():
    # setup
    channel_id = channel.create(user_1_token, "Channel 3", True)['channel_id']
    # end setup

    with pytest.raises(AccessError) as error:
        channel.messages(user_2_token, channel_id, 0)
    assert str(error.value) == "400 Bad Request: User is not a member of the channel"

# test when token is not valid
def test_messages_invalid_token():
    # setup
    channel_id = channel.create(user_1_token, "Channel 3", True)['channel_id']
    # end setup

    with pytest.raises(AccessError) as error:
        channel.messages("invalidToken", channel_id, 0)
    assert str(error.value) == "400 Bad Request: Token is invalid"

# test when the user is not a member
def test_messages_user_not_member():
    # setup
    channel_id = channel.create(user_1_token, "Channel 3", True)['channel_id']
    # end setup

    with pytest.raises(AccessError) as error:
        channel.messages(user_2_token, channel_id, 0)
    assert str(error.value) == "400 Bad Request: User is not a member of the channel"

# test when the channel doesn't exist
def test_messages_invalid_channel():
    # setup
    channel.create(user_1_token, "Channel 3", True)
    # end setup

    with pytest.raises(ValueError) as error:
        # assume this channel id is invalid
        channel.messages(user_1_token, 429042905790435709, 0)
    assert str(error.value) == "400 Bad Request: This channel ID does not match a valid channel"

# test when start index exceeds number of messages
def test_messages_start_exceed_message():
    # setup
    channel_id = channel.create(user_1_token, "Channel 3", True)['channel_id']
    # end setup

    with pytest.raises(ValueError) as error:
        channel.messages(user_1_token, channel_id, 1)
    assert str(
        error.value) == "400 Bad Request: Start is equal or greater than number of messages"

# test channel with no messages
def test_messages_0_message():
    # setup
    channel_id = channel.create(user_1_token, "Channel 3", True)['channel_id']
    # end setup
    messages = channel.messages(user_1_token, channel_id, 0)
    messages_list = messages['messages']
    assert messages['start'] == 0
    assert messages['end'] == -1
    assert len(messages_list) == 0


# test channel with 1 message
def test_messages_1_message():
    # setup
    channel_id = channel.create(user_1_token, "Channel 3", True)['channel_id']
    message.send(user_1_token, channel_id, "Welcome to our new channel!!!")
    # end setup

    messages = channel.messages(user_1_token, channel_id, 0)
    messages_list = messages['messages']
    assert messages['start'] == 0
    assert messages['end'] == -1
    assert len(messages_list) == 1
    assert messages_list[0]['message'] == "Welcome to our new channel!!!"
    assert messages_list[0]['u_id'] == user_1_id

# test channel with 2 messages, showing both
def test_messages_2_message():
    # setup
    channel_id = channel.create(user_1_token, "Channel 3", True)['channel_id']
    channel.invite(user_1_token, channel_id, user_2_id)
    message.send(user_1_token, channel_id, "Welcome to our new channel!!!")
    message.send(user_2_token, channel_id, "Thank you for the welcome")
    # end setup

    messages = channel.messages(user_2_token, channel_id, 0)
    messages_list = messages['messages']
    assert messages['start'] == 0
    assert messages['end'] == -1
    assert len(messages_list) == 2
    assert messages_list[0]['message'] == "Thank you for the welcome"
    assert messages_list[0]['u_id'] == user_2_id
    assert messages_list[1]['message'] == "Welcome to our new channel!!!"
    assert messages_list[1]['u_id'] == user_1_id

# test channel with 2 messages, skipping most recent
def test_messages_3_message():
    # setup
    channel_id = channel.create(user_1_token, "Channel 3", True)['channel_id']
    channel.invite(user_1_token, channel_id, user_2_id)
    message.send(user_1_token, channel_id, "Welcome to our new channel!!!")
    message.send(user_2_token, channel_id, "Thank you for the welcome")
    # end setup

    messages = channel.messages(user_1_token, channel_id, 1)
    messages_list = messages['messages']
    assert messages['start'] == 1
    assert messages['end'] == -1
    assert len(messages_list) == 1
    assert messages_list[0]['message'] == "Welcome to our new channel!!!"
    assert messages_list[0]['u_id'] == user_1_id

# test channel with over 50 messages and reactions
def test_messages_many():
    # create a channel for testing
    channel_id = channel.create(user_1_token, "Channel 4", True)['channel_id']
    for i in range(52):
        message_id = message.send(user_1_token, channel_id, str(i))['message_id']
        # react even numbered messages
        if i%2 == 0:
            message.react(user_1_token, message_id, 1)

    messages = channel.messages(user_1_token, channel_id, 1)
    messages_list = messages['messages']
    assert messages['start'] == 1
    assert messages['end'] == 51
    assert len(messages_list) == 50
    assert messages_list[0]['message'] == "50" # 2nd most recent message
    assert messages_list[0]['u_id'] == user_1_id
    assert messages_list[0]['reacts'][0]['react_id'] == 1

# test channel_leave function
# test not member of channel
def test_leave_not_member():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    # end setup

    with pytest.raises(AccessError) as error:
        channel.leave(user_2_token, channel_id)
    assert str(error.value) == "400 Bad Request: User is not a member of the channel"
    assert len(channel.details(user_1_token, channel_id)["all_members"]) == 1

# test general case
def test_leave_one():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    # end setup
    channel.join(user_2_token, channel_id)
    assert len(channel.details(user_1_token, channel_id)["all_members"]) == 2
    channel.leave(user_2_token, channel_id)
    assert len(channel.details(user_1_token, channel_id)["all_members"]) == 1

# test many
def test_leave_many():
    # setup
    try:
        user_3_dict = auth.register("user3@gmail.com", "user3pass", "User", "3")
    except ValueError:
        user_3_dict = auth.login("user3@gmail.com", "user3pass")
    user_3_token = user_3_dict['token']
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    channel.join(user_2_token, channel_id)
    channel.join(user_3_token, channel_id)
    # end setup

    assert len(channel.details(user_1_token, channel_id)["all_members"]) == 3
    channel.leave(user_2_token, channel_id)
    channel.leave(user_3_token, channel_id)
    assert len(channel.details(user_1_token, channel_id)["all_members"]) == 1

# test invalid channel_id
def test_leave_invalid_channel():
    # setup
    channel.create(user_1_token, "weeb cave", True)
    # end setup
    with pytest.raises(ValueError) as error:
        channel.leave(user_1_token, -1)
    assert str(error.value) == "400 Bad Request: This channel ID does not match a valid channel"

    with pytest.raises(ValueError) as error:
        channel.leave(user_1_token, 10.96)
    assert str(error.value) == "400 Bad Request: This channel ID does not match a valid channel"

# test invalid token
def test_leave_invalid_token():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    # end setup

    with pytest.raises(AccessError) as error:
        channel.leave(-1, channel_id)
    assert str(error.value) == "400 Bad Request: Token is invalid"

# test zero case
def test_join_zero():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    # end setup

    assert len(channel.details(user_1_token, channel_id)["all_members"]) == 1

# test one case
def test_join_one():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    # end setup

    channel.join(user_2_token, channel_id)
    assert len(channel.details(user_1_token, channel_id)["all_members"]) == 2

# test many case
def test_join_many():
    # setup
    try:
        user_3_dict = auth.register("user3@gmail.com", "user3pass", "User", "3")
    except ValueError:
        user_3_dict = auth.login("user3@gmail.com", "user3pass")
    user_3_token = user_3_dict['token']
    # end setup

    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    assert len(channel.details(user_1_token, channel_id)["all_members"]) == 1
    channel.join(user_2_token, channel_id)
    assert len(channel.details(user_1_token, channel_id)["all_members"]) == 2
    channel.join(user_3_token, channel_id)
    assert len(channel.details(user_1_token, channel_id)["all_members"]) == 3

# test already a member of the channel
def test_join_already_member():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    # end setup

    with pytest.raises(ValueError) as error:
        channel.join(user_1_token, channel_id)
    assert str(error.value) == "400 Bad Request: Already part of channel"
    assert len(channel.details(user_1_token, channel_id)["all_members"]) == 1

# test channel is private (channel 2 - separate channel)
def test_join_private():
    # setup
    channel_id2 = channel.create(user_1_token, 'name', False)['channel_id']
    # end setup

    with pytest.raises(AccessError) as error:
        channel.join(user_2_token, channel_id2)
    assert str(error.value) == "400 Bad Request: Channel is private"
    assert len(channel.details(user_1_token, channel_id2)["all_members"]) == 1

    channel.join(owner_token, channel_id2)
    assert len(channel.details(user_1_token, channel_id2)["all_members"]) == 2

# test invalid channel_id
def test_join_invalid_channel():
    # setup
    channel.create(user_1_token, "weeb cave", True)
    # end setup

    with pytest.raises(ValueError) as error:
        channel.join(user_1_token, -1)
    assert str(error.value) == '400 Bad Request: This channel ID does not match a valid channel'

    with pytest.raises(ValueError) as error:
        channel.join(user_1_token, 10.96)
    assert str(error.value) == '400 Bad Request: This channel ID does not match a valid channel'

# slackr owner can join private channel
def test_join_slackr_owner():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    # end setup

    channel.join(owner_token, channel_id)
    assert len(channel.details(user_1_token, channel_id)["all_members"]) == 2
    assert len(channel.details(user_1_token, channel_id)["owner_members"]) == 2

# test zero case
def test_addowner_zero():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    # end setup

    assert len(channel.details(user_1_token, channel_id)['owner_members']) == 1

# test one case
def test_addowner_one():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    # end setup

    channel.join(user_2_token, channel_id)
    channel.addowner(user_1_token, channel_id, user_2_id)
    assert len(channel.details(user_1_token, channel_id)['owner_members']) == 2

# test many case
def test_addowner_many():
    # setup
    try:
        user_3_dict = auth.register("user3@gmail.com", "user3pass", "User", "3")
    except ValueError:
        user_3_dict = auth.login("user3@gmail.com", "user3pass")
    user_3_id = user_3_dict['u_id']
    user_3_token = user_3_dict['token']

    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    # end setup

    channel.join(user_2_token, channel_id)
    channel.addowner(user_1_token, channel_id, user_2_id)
    assert len(channel.details(user_1_token, channel_id)['owner_members']) == 2

    channel.join(user_3_token, channel_id)
    channel.addowner(user_1_token, channel_id, user_3_id)
    assert len(channel.details(user_1_token, channel_id)['owner_members']) == 3

# test user not in channel
def test_addowner_access_not_permitted():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    # end setup

    with pytest.raises(AccessError) as error:
        channel.addowner(user_1_token, channel_id, user_2_id)
    assert str(
        error.value) == '400 Bad Request: User is not a member of the channel'

# test invalid token
def test_addowner_invalid_token():
    # setup
    try:
        user_3_dict = auth.register("user3@gmail.com", "user3pass", "User", "3")
    except ValueError:
        user_3_dict = auth.login("user3@gmail.com", "user3pass")
    user_3_id = user_3_dict['u_id']
    user_3_token = user_3_dict['token']
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    channel.join(user_3_token, channel_id)
    # end setup

    with pytest.raises(AccessError) as error:
        channel.addowner(-1, channel_id, user_3_id)
    assert str(error.value) == "400 Bad Request: Token is invalid"

    with pytest.raises(AccessError) as error:
        channel.addowner(10.96, channel_id, user_3_id)
    assert str(error.value) == "400 Bad Request: Token is invalid"

# test invalid channel
def test_addowner_invalid_channel():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    channel.join(user_2_token, channel_id)
    # end setup

    with pytest.raises(ValueError) as error:
        channel.addowner(user_1_token, -1, user_2_id)
    assert str(error.value) == "400 Bad Request: This channel ID does not match a valid channel"

    with pytest.raises(ValueError) as error:
        channel.addowner(user_1_token, 10.96, user_2_id)
    assert str(error.value) == "400 Bad Request: This channel ID does not match a valid channel"

#test invalid u_id
def test_addowner_invalid_u_id():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    # end setup

    with pytest.raises(ValueError) as error:
        channel.addowner(user_1_token, channel_id, -1)
    assert str(error.value) == "400 Bad Request: User ID does not refer to a valid user"

# test caller is not in owners
def test_addowner_caller_not_owner():
    # setup
    try:
        user_3_dict = auth.register("user3@gmail.com", "user3pass", "User", "3")
    except ValueError:
        user_3_dict = auth.login("user3@gmail.com", "user3pass")
    user_3_id = user_3_dict['u_id']
    user_3_token = user_3_dict['token']
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    # end setup

    channel.join(user_2_token, channel_id)
    channel.join(user_3_token, channel_id)
    with pytest.raises(AccessError) as error:
        channel.addowner(user_2_token, channel_id, user_3_id)
    assert str(error.value) == "400 Bad Request: The authorised user is not an owner of this channel"

# test u_id is already an owner
def test_addowner_already_owner():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    channel.join(user_2_token, channel_id)
    # end setup

    channel.addowner(user_1_token, channel_id, user_2_id)
    with pytest.raises(ValueError) as error:
        channel.addowner(user_1_token, channel_id, user_2_id)
    assert str(error.value) == "400 Bad Request: The user is already an owner of this channel"

# test 0 case
def test_removeowner_zero():
    # setup
    try:
        user_3_dict = auth.register("user3@gmail.com", "user3pass", "User", "3")
    except ValueError:
        user_3_dict = auth.login("user3@gmail.com", "user3pass")
    user_3_id = user_3_dict['u_id']
    user_3_token = user_3_dict['token']

    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    channel.join(user_2_token, channel_id)
    channel.join(user_3_token, channel_id)
    channel.addowner(user_1_token, channel_id, user_2_id)
    channel.addowner(user_1_token, channel_id, user_3_id)
    # end setup

    assert len(channel.details(user_1_token, channel_id)['owner_members']) == 3

# test one case
def test_removeowner_one():
    # setup
    try:
        user_3_dict = auth.register("user3@gmail.com", "user3pass", "User", "3")
    except ValueError:
        user_3_dict = auth.login("user3@gmail.com", "user3pass")
    user_3_id = user_3_dict['u_id']
    user_3_token = user_3_dict['token']

    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    channel.join(user_2_token, channel_id)
    channel.join(user_3_token, channel_id)
    channel.addowner(user_1_token, channel_id, user_2_id)
    channel.addowner(user_1_token, channel_id, user_3_id)
    # end setup

    channel.removeowner(user_1_token, channel_id, user_2_id)
    assert len(channel.details(user_1_token, channel_id)['owner_members']) == 2

# test many case
def test_removeowner_many():
    # setup
    try:
        user_3_dict = auth.register("user3@gmail.com", "user3pass", "User", "3")
    except ValueError:
        user_3_dict = auth.login("user3@gmail.com", "user3pass")
    user_3_id = user_3_dict['u_id']
    user_3_token = user_3_dict['token']

    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    channel.join(user_2_token, channel_id)
    channel.join(user_3_token, channel_id)
    channel.addowner(user_1_token, channel_id, user_2_id)
    channel.addowner(user_1_token, channel_id, user_3_id)
    # end setup

    channel.removeowner(user_1_token, channel_id, user_2_id)
    assert len(channel.details(user_1_token, channel_id)['owner_members']) == 2

    channel.removeowner(user_1_token, channel_id, user_3_id)
    assert len(channel.details(user_1_token, channel_id)['owner_members']) == 1

# test u_id does not refer to owner
def test_removeowner_u_id_not_owner():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    channel.join(user_2_token, channel_id)
    # end setup

    with pytest.raises(ValueError) as error:
        channel.removeowner(user_1_token, channel_id, user_2_id)
    assert str(error.value) == "400 Bad Request: The user is not an owner of this channel"

# test authorised u_id does not refer to an owner
def test_removeowner_caller_not_owner():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    channel.join(user_2_token, channel_id)
    # end setup

    with pytest.raises(AccessError) as error:
        channel.removeowner(user_2_token, channel_id, user_1_id)
    assert str(error.value) == "400 Bad Request: The authorised user is not an owner of this channel"

# test invalid token
def test_removeowner_invalid_token():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    channel.join(user_2_token, channel_id)
    channel.addowner(user_1_token, channel_id, user_2_id)
    # end setup

    with pytest.raises(AccessError) as error:
        channel.removeowner(-1, channel_id, user_2_id)
    assert str(error.value) == "400 Bad Request: Token is invalid"
    with pytest.raises(AccessError) as error:
        channel.removeowner(10.66, channel_id, user_2_id)
    assert str(error.value) == "400 Bad Request: Token is invalid"

# test invalid channel
def test_removeowner_invalid_channel():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    channel.join(user_2_token, channel_id)
    channel.addowner(user_1_token, channel_id, user_2_id)
    # end setup

    with pytest.raises(ValueError) as error:
        channel.removeowner(user_1_token, -1, user_2_id)
    assert str(error.value) == "400 Bad Request: This channel ID does not match a valid channel"

# test invalid u_id
def test_removeowner_user_not_owner():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    channel.join(user_2_token, channel_id)
    channel.addowner(user_1_token, channel_id, user_2_id)
    # end setup

    with pytest.raises(ValueError) as error:
        channel.removeowner(user_1_token, channel_id, -1)
    assert str(error.value) == "400 Bad Request: The user is not an owner of this channel"

# test attempt to remove Slackr owner from owners list
def test_removeowner_slackr_owner():
    # setup
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    channel.join(user_2_token, channel_id)
    channel.addowner(user_1_token, channel_id, user_2_id)
    # end setup

    channel.join(owner_token, channel_id)
    with pytest.raises(ValueError) as error:
        channel.removeowner(user_1_token, channel_id, owner_u_id)
    assert str(error.value) == "400 Bad Request: Owners and admins of the Slackr must be an owner of this channel"

    # test 3: returns empty dictionary
    assert channel.removeowner(user_1_token, channel_id, user_2_id) == {}

# test one case
def test_list_one():
    # setup
    size = len(channel.list(user_1_token)['channels'])
    # end setup

    channel.create(user_1_token, "random", True)
    assert len(channel.list(user_1_token)['channels']) == size + 1

# test many case
def test_list_many():
    # setup
    size = len(channel.list(user_1_token)['channels'])
    # end setup

    channel.create(user_1_token, "random", True)
    channel.create(user_1_token, "many", True)
    assert len(channel.list(user_1_token)['channels']) == size + 2

# test invalid token
def test_list_invalid_token():
    with pytest.raises(AccessError) as error:
        channel.list(-1)
    assert str(error.value) == "400 Bad Request: Token is invalid"

    with pytest.raises(AccessError) as error:
        channel.list(10.96)
    assert str(error.value) == "400 Bad Request: Token is invalid"

# test user leaves a channel
def test_list_leave_channel():
    # setup
    channel_id = channel.create(user_1_token, "random", True)['channel_id']
    size = len(channel.list(user_1_token)['channels'])
    # end setup

    channel.leave(user_1_token, channel_id)
    assert len(channel.list(user_1_token)['channels']) == size - 1

# test type return
def test_list_correct_return_type():
    assert not isinstance(channel.list(user_1_token), list)

    channel.l = channel.list(user_1_token)
    for k in channel.l['channels']:
        assert isinstance(k, dict)

# test zero case
def test_listall_zero():
    size = len(channel.listall(user_1_token)['channels'])
    assert size == len(data.channels.keys())

# test one case
def test_listall_one():
    size = len(channel.listall(user_1_token)['channels'])
    assert size == len(data.channels.keys())

    channel.create(user_1_token, "random", True)
    assert len(channel.listall(user_1_token)['channels']) == size + 1

# test many case
def test_listall_many():
    size = len(channel.listall(user_1_token)['channels'])
    assert size == len(data.channels.keys())

    channel.create(user_1_token, "random", True)
    assert len(channel.listall(user_1_token)['channels']) == size + 1

    channel.create(user_1_token, "funny", True)
    assert len(channel.listall(user_1_token)['channels']) == size + 2

# test user joining or leaving channel has no effect
def test_listall_join_or_leave():
    channel_id = channel.create(user_2_token, "random", True)['channel_id']
    size = len(channel.listall(user_1_token)['channels'])

    channel.join(user_1_token, channel_id)
    assert len(channel.listall(user_1_token)['channels']) == size

    channel.leave(user_1_token, channel_id)
    assert len(channel.listall(user_1_token)['channels']) == size

# test same for any user
def test_listall_same_for_all():
    assert len(channel.listall(user_1_token)['channels']) == len(channel.listall(user_2_token)['channels'])

 # test correct type returned
def test_listall_correct_return():
    assert not isinstance(channel.list(user_1_token), list)

    channel_list = channel.listall(user_1_token)
    for k in channel_list['channels']:
        assert isinstance(k, dict)

# test invalid token
def test_listall_invalid_token():
    with pytest.raises(AccessError) as error:
        channel.list(-1)
    assert str(error.value) == "400 Bad Request: Token is invalid"

    with pytest.raises(AccessError) as error:
        channel.list(10.96)
    assert str(error.value) == "400 Bad Request: Token is invalid"

# test one case
def test_create_one():
    size = len(channel.listall(user_1_token)['channels'])
    assert len(channel.listall(user_1_token)['channels']) == size

    channel.create(user_1_token, "weeb cave", True)
    assert len(channel.listall(user_1_token)['channels']) == size + 1

# test data created is of the correct types and data
def test_create_correct_data_types():
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']

    assert isinstance(channel_id, int)
    assert data.channels[channel_id]['name'] == "weeb cave"
    assert data.channels[channel_id]['is_public']
    assert isinstance(data.channels[channel_id]['owners'], list)
    assert isinstance(data.channels[channel_id]['members'], list)

    assert len(data.channels[channel_id]['owners']) == 1
    assert len(data.channels[channel_id]['members']) == 1

# test channel_id is the largest of that created
def test_create_largest_id():
    channel_id = channel.create(user_1_token, "weeb cave", True)['channel_id']
    assert channel_id == max(data.channels.keys())

# test name too long
def test_create_name_too_long():
    with pytest.raises(ValueError) as error:
        channel.create(user_1_token, "This name is wayyyyyyy too long", True)
    assert str(error.value) == '400 Bad Request: Name is longer than 20 characters'

# test invalid token
def test_create_invalid_token():
    with pytest.raises(AccessError) as error:
        channel.create(-1, "hello", True)
    assert str(error.value) == "400 Bad Request: Token is invalid"

    with pytest.raises(AccessError) as error:
        channel.create(10.96, "bye", True)
    assert str(error.value) == "400 Bad Request: Token is invalid"
