import pytest
import server.auth as auth
import server.user_profile as user
from server.error import ValueError, AccessError

# email addresses must have structure info@domain
# domain must contain domain_name and at least 1 extension (domain.ex1.ex2)
# extensions can only have a period followed by 2-3 alphanumeric characters
_INVALID_EMAILS = [".@gmail.com",  # emails with invalid info (before @)
                   "-@gmail.com",
                   "$@gmail.com",
                   "a!@gmail.com",
                   ".gh@gmail.com",
                   "-gnig@gmail.com",
                   "h-h-h-@gmail.com",
                   "a..t@gmail.com",
                   "1nv4l1d#@gmail.com",
                   ".a.t@outlook.com",
                   "(hello_word)@dfis.co",
                   "no spaces allowed@here.soz",
                   "where_is_the_at_symbol.com",  # emails without @ symbol
                   "39ts0tflk.com.au",
                   "8.8.8.8",
                   "something-missing.ru",
                   "@.com",  # emails with multiple @ symbols
                   "user@australia@sydney.com",
                   "f@110ver@gmail.com",
                   "valid_info@101-.val.id.ext.ens.ion",  # emails with an invalid domain
                   "nothing@wrong here.com",
                   "ndfiosn@dot..dot.au",
                   "a.t@gmail",  # emails with invalid/missing domain extensions
                   "a.t@gmail.",
                   "a.t@gmail.comm",
                   "user.name@yahoo.com.toolong",
                   "userdfsid@outlook.t.o.o.s.h.o.r.t",
                   "abc123@123..hi",
                   "email@111.222.333.44444"]

_VALID_EMAILS = ["b.gh@gmail.com",
                 "h-gnig@gmail.com",
                 "h-h-h-h@gmail.com.au",
                 "a.n.t@gmail.com",
                 "1nv4l1d@gmail.com",
                 "hello_word@dfis.edu.au",
                 "where_is_the_@_symbol.com",
                 "a@a.com",
                 "user@australia.sydney.com",
                 "valid_info@101.val.id.ext.ens.ion",
                 "nothing@wrong_here.com",
                 "ndfiosn@dot.dot.dot.au",
                 "a.t@gmail.comm.com",
                 "user.name@yahoo.com.toolong.hi",
                 "userdfsid@outlook.t.o.o.s.h.o.r.t.com",
                 "email@111.222.333.44444.55"]

_VALID_PASSWORDS = ["abc123",
                    "qwerty",
                    "asdfghjk",
                    "l33tc0d3",
                    "helloworld",
                    "trimesterbad",
                    "dfawevrw",
                    "fvwqvtest32",
                    "565v5634wv",
                    "ryt67w4b6",
                    "nyw56ywb5",
                    "t4wby543",
                    "tv4w3tv",
                    "fgbser",
                    "$W^$%^bthd",
                    "$$$$$$$$$$$$$$$"]

_RESET_CODE = ""

#####   TEST SUITES   #####

# test that emails are correctly marked as invalid
@pytest.mark.parametrize('email', _INVALID_EMAILS)
def test_register_invalid_email(email):
    with pytest.raises(ValueError) as error:
        auth.register(email, "password", "Bob", "Smith")
    assert str(
        error.value) == "400 Bad Request: Given email is not a valid email address"

# test when registered names are invalid
def test_register_invalid_names():
    with pytest.raises(ValueError) as error:
        # first name length 50, last name length 51
        auth.register(
            "fhioadhf@gmail.com",
            "password",
            "B4590v9nu9uq4u09q309809v40909908098tv093409t9043ob",
            "B4590qv9nu9uq4u09q309809v40909908098tv093409t9043ob")
    assert str(
        error.value) == "400 Bad Request: Last name must be between 1 and 50 characters long"
    with pytest.raises(ValueError) as error:
        # both names length 51, first name triggers error first
        auth.register(
            "101@gmail.com",
            "45b3dr",
            "B4590qv9nu9uq4u09q309809v40909908098tv093409t9043ob",
            "B4590qv9nu9uq4u09q309809v40909908098tv093409t9043ob")
    assert str(
        error.value) == "400 Bad Request: First name must be between 1 and 50 characters long"

# test when password is the only invalid registration field
def test_register_invalid_password():
    with pytest.raises(ValueError) as error:
        auth.register("random@mail.com.au", "p@$$", "dsacfwe", "dfaf")
    assert str(
        error.value) == "400 Bad Request: Password entered is invalid (must have at least 6 characters)"
    with pytest.raises(ValueError) as error:
        auth.register("jafioe@fndisaon.com", "!", "Bob", "George")
    assert str(
        error.value) == "400 Bad Request: Password entered is invalid (must have at least 6 characters)"
    with pytest.raises(ValueError) as error:
        auth.register("jefferson@yahoo.mail.com.jp", "l33t", "Hello", "World")
    assert str(
        error.value) == "400 Bad Request: Password entered is invalid (must have at least 6 characters)"

# test that valid login credentials result in an appropriate return value
@pytest.mark.parametrize('email,password', list(
    zip(_VALID_EMAILS, _VALID_PASSWORDS)))
def test_register_valid(email, password):
    # checking that a proper dictionary with required fields is returned
    assert list(
        auth.register(
            email,
            password,
            "bob",
            "brown").keys()) == [
                "u_id",
                "token"]

# testing registering a user, then logging in as the user
# by verifying output is a dictionary with 2 fields
def test_register_then_login():
    try:
        auth.register("user1@gmail.com", "user1pass", "User", "1")
    except ValueError:
        pass
    assert list(
        auth.login(
            "user1@gmail.com",
            "user1pass").keys()) == [
                "u_id",
                "token"]
    try:
        auth.register("user2@gmail.com", "user2pass", "User", "2")
    except ValueError:
        pass
    assert list(
        auth.login(
            "user2@gmail.com",
            "user2pass").keys()) == [
                "u_id",
                "token"]

    try:
        auth.register("user3@gmail.com", "user3pass", "User", "3")
    except ValueError:
        pass
    assert list(
        auth.login(
            "user3@gmail.com",
            "user3pass").keys()) == [
                "u_id",
                "token"]

    try:
        auth.register("user4@gmail.com", "user4pass", "User", "4")
    except ValueError:
        pass
    assert list(
        auth.login(
            "user4@gmail.com",
            "user4pass").keys()) == [
                "u_id",
                "token"]

# for as long as email is different, users can have the same name
def test_register_duplicate_handles():
    assert list(auth.register("abcdefg@gmail.com", "password", "abcd", "efg").keys()) == ["u_id", "token"]
    second_user = auth.register("abcdefg1@gmail.com", "password", "abcd", "efg")
    assert list(second_user.keys()) == ["u_id", "token"]

    # send the handle of this user to default handle + u_id of next registered member
    user.profile_sethandle(second_user['token'], "abcdefg" + str(second_user['u_id'] + 1))

    third_user = auth.register("abcdefg2@gmail.com", "password", "abcd", "efg")
    assert list(third_user.keys()) == ["u_id", "token"]
    # we expect the handle's extension to be 1 more than this user's id, since
    # the previous user took what would be allocated as this third user's handle
    assert user.profile(third_user['token'], third_user['u_id'])['handle_str'] == "abcdefg" + str(third_user['u_id'] + 1)

# test that a list of invalid emails are detected as invalid
@pytest.mark.parametrize('email', _INVALID_EMAILS)
def test_login_invalid_email(email):
    with pytest.raises(ValueError) as error:
        auth.login(email, "password")
    assert str(
        error.value) == "400 Bad Request: Given email is not a valid email address"

# test that valid login credentials result in an appropriate return value
@pytest.mark.parametrize('email,password', list(
    zip(_VALID_EMAILS, _VALID_PASSWORDS)))
def test_login_valid(email, password):
    # checking that a proper dictionary with required fields is returned
    assert list(auth.login(email, password).keys()) == ["u_id", "token"]

def test_login_unregistered_user():
    with pytest.raises(ValueError) as error:
        auth.login("nonexistent@gmail.com", "password")
    assert str(error.value) == "400 Bad Request: Email doesn't belong to a user"

    with pytest.raises(ValueError) as error:
        auth.login("jfhaouihdgu@hotmail.gmail.random.co.nz", "password")
    assert str(error.value) == "400 Bad Request: Email doesn't belong to a user"

    with pytest.raises(ValueError) as error:
        auth.login("a-b-c@c.b.au", "password")
    assert str(error.value) == "400 Bad Request: Email doesn't belong to a user"

# test that login will fail with an incorrect password
def test_login_wrong_password():
    # setup 2 users
    try:
        auth.register("user1@gmail.com", "user1pass", "User", "1")
    except ValueError:
        pass
    try:
        auth.register("user2@gmail.com", "user2pass", "User", "2")
    except ValueError:
        pass

    # testing random wrong passwords
    with pytest.raises(ValueError) as error:
        auth.login("user1@gmail.com", "not_the_right_password")
    assert str(error.value) == "400 Bad Request: Password is incorrect"

    with pytest.raises(ValueError) as error:
        auth.login("user2@gmail.com", "gnoasfgnfodg")
    assert str(error.value) == "400 Bad Request: Password is incorrect"

    # testing using a password of another user
    with pytest.raises(ValueError) as error:
        auth.login("user1@gmail.com", "user2pass")
    assert str(error.value) == "400 Bad Request: Password is incorrect"

    with pytest.raises(ValueError) as error:
        auth.login("user2@gmail.com", "user1pass")
    assert str(error.value) == "400 Bad Request: Password is incorrect"

# testing that logging out invalidates tokens
def test_logout():
    # setup 2 users
    try:
        user_1_dict = auth.register("abc@gmail.com", "fasdf1", "test", "one")
    except ValueError:
        user_1_dict = auth.login("abc@gmail.com", "fasdf1")
    user_1_token = user_1_dict['token']
    try:
        user_2_dict = auth.register("qwe@gmail.com", "dasfsd", "test", "two")
    except ValueError:
        user_2_dict = auth.login("qwe@gmail.com", "dasfsd")
    user_2_token = user_2_dict['token']

    # trying to logout with a valid token that doesn't belong to user
    # can be tested by generating new token with new time
    false_token = auth.generate_token(user_1_dict['u_id'])
    assert not auth.logout(false_token)['is_success']

    # tokens are valid before logout
    assert isinstance(auth.validate_token(user_1_token), int)
    assert isinstance(auth.validate_token(user_2_token), int)

    assert auth.logout(user_1_token)['is_success']
    assert auth.logout(user_2_token)['is_success']

    # tokens are invalid after logout
    with pytest.raises(AccessError) as error:
        auth.validate_token(user_1_token)
    assert str(error.value) == "400 Bad Request: Token is invalid"
    with pytest.raises(AccessError) as error:
        auth.validate_token(user_2_token)
    assert str(error.value) == "400 Bad Request: Token is invalid"


def test_passwordreset_request():
    global _RESET_CODE

    with pytest.raises(ValueError) as error:
        auth.passwordreset_request("nonexistentemail@gmail.com")
    assert str(error.value) == "400 Bad Request: Email doesn't belong to a user"

    try:
        auth.register("user1@gmail.com", "user1pass", "User", "1")
    except ValueError:
        pass

    email_data = auth.passwordreset_request("user1@gmail.com")
    assert list(email_data.keys()) == ['title', 'body']
    _RESET_CODE = email_data['body'][-6:]


# test invalid reset codes
@pytest.mark.parametrize('code', [12345543, 1, 10.5, -32])
def test_passwordreset_reset_invalid_code(code):
    with pytest.raises(ValueError) as error:
        auth.passwordreset_reset(code, "new_password!!")
    assert str(error.value) == "400 Bad Request: Reset code is invalid"

def test_passwordreset_reset():
    global _RESET_CODE
    with pytest.raises(ValueError) as error:
        auth.passwordreset_reset(_RESET_CODE, "short")
    assert str(error.value) == "400 Bad Request: Password entered is invalid (must have at least 5 characters)"

    # test correct password reset
    assert auth.passwordreset_reset(_RESET_CODE, "user1pass") == {}

def test_admin_userpermission_change():
    ADMIN_USER = auth.login("johnsmith101@gmail.com", "UsydUnsw101")
    USER = auth.login("user2@gmail.com", "user2pass")

    # Invalid u_id
    with pytest.raises(ValueError) as error:
        auth.admin_userpermission_change(USER['token'], 8947847389, 2)
    assert str(error.value) == "400 Bad Request: This user does not exist"

    # Invalid permission
    with pytest.raises(ValueError) as error:
        # permission_id 5 does not exist
        auth.admin_userpermission_change(USER['token'], ADMIN_USER['u_id'], 5)
    assert str(error.value) == "400 Bad Request: Specified permission is invalid"

    # Token does not refer to an admin or owner
    with pytest.raises(AccessError) as error:
        auth.admin_userpermission_change(USER['token'], ADMIN_USER['u_id'], 3)
    assert str(
        error.value) == "400 Bad Request: User is not permitted to make permission changes"

    # Valid operation
    assert auth.admin_userpermission_change(ADMIN_USER['token'], USER['u_id'], 1) == {}
    # user now has permission to change their permissions
    assert auth.admin_userpermission_change(USER['token'], USER['u_id'], 2) == {}

    # Admin trying to change owner's permission
    with pytest.raises(AccessError) as error:
        auth.admin_userpermission_change(USER['token'], ADMIN_USER['u_id'], 3)
    assert str(
        error.value) == "400 Bad Request: User is not permitted to make permission changes"

    # Change own permission to member
    assert auth.admin_userpermission_change(USER['token'], USER['u_id'], 3) == {}

def test_get_id_from_email():
    assert auth.get_id_from_email("fakeemail@email.com") is None
    assert auth.get_id_from_email("johnsmith101@gmail.com") == 1
