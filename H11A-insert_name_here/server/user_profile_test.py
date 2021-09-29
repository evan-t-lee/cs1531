import pytest
import server.auth as auth
import server.user_profile as user
from server.error import ValueError, AccessError

#####   CONSTANTS   #####
_INVALID_VALUE = -1
_USER_ID = 22

# this image is 776 x 500 px
_IMAGE_URL = 'https://jixta.files.wordpress.com/2015/11/featured-mandelbrot.jpeg'
_START_X = 150
_START_Y = 25
_END_X = 610
_END_Y = 485
_PORT = 5001

_INVALID_IMG = [
    "www.google.com",
    "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    "www.image.google.com",
    "www.randomimage.com/file.tiff"
]

_INVALID_URL = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.jpg"

_IMG_RANGES = [
    (-1, 10, 10, 10),
    (10, -1, 10, 10),
    (0, 0, 777, 100),
    (0, 0, 400, 501),
    (100, 100, 100, 200),
    (100, 100, 200, 100),
    (101, 50, 100, 100),
    (50, 101, 100, 100)
]

#####   SETUP   #####

try:
    AUTH_DATA = auth.register(
        'johnsmith10111@gmail.com',
        'UsydUnsw101',
        'John',
        'Smith')
except ValueError:
    AUTH_DATA = auth.login(
        'johnsmith10111@gmail.com',
        'UsydUnsw101')
TOKEN = AUTH_DATA['token']

#####   TEST SUITES   #####

def test_profile():
    with pytest.raises(ValueError) as error:
        user.profile(TOKEN, _INVALID_VALUE)
    assert str(error.value) == '400 Bad Request: Invalid user'

    with pytest.raises(AccessError) as error:
        user.profile(_INVALID_VALUE, _USER_ID)
    assert str(error.value) == '400 Bad Request: Token is invalid'

    assert user.profile(TOKEN, AUTH_DATA['u_id']) == {
        'email': 'johnsmith10111@gmail.com',
        'name_first': 'John',
        'name_last': 'Smith',
        'handle_str': 'johnsmith' + str(AUTH_DATA['u_id']),
        'profile_img_url': ''
    }

def test_profile_setname():
    with pytest.raises(AccessError) as error:
        user.profile_setname(_INVALID_VALUE, 'john', 'smith')
    assert str(error.value) == '400 Bad Request: Token is invalid'

    with pytest.raises(ValueError) as error:
        user.profile_setname(TOKEN, 'john' * 51, 'smith')
    assert str(error.value) == '400 Bad Request: First name is more than 50 characters'

    with pytest.raises(ValueError) as error:
        user.profile_setname(TOKEN, 'john', 'smith' * 51)
    assert str(error.value) == '400 Bad Request: Last name is more than 50 characters'

    assert user.profile_setname(TOKEN, 'john', 'smith') == {}

    assert user.profile(TOKEN, AUTH_DATA['u_id']) == {
        'email': 'johnsmith10111@gmail.com',
        'name_first': 'john',
        'name_last': 'smith',
        'handle_str': 'johnsmith' + str(AUTH_DATA['u_id']),
        'profile_img_url': ''
    }

def test_profile_setemail():
    with pytest.raises(AccessError) as error:
        user.profile_setemail(_INVALID_VALUE, 'johnsmith10111@gmail.com')
    assert str(error.value) == '400 Bad Request: Token is invalid'

    with pytest.raises(ValueError) as error:
        user.profile_setemail(TOKEN, 'johnsmith10111')
    assert str(error.value) == '400 Bad Request: Email is not valid'

    with pytest.raises(ValueError) as error:
        user.profile_setemail(TOKEN, 'johnsmith10111@gmail.com')
    assert str(error.value) == '400 Bad Request: Email is already used'

    assert user.profile_setemail(TOKEN, 'johnsmith10111@hotmail.com') == {}

    assert user.profile(TOKEN, AUTH_DATA['u_id']) == {
        'email': 'johnsmith10111@hotmail.com',
        'name_first': 'john',
        'name_last': 'smith',
        'handle_str': 'johnsmith' + str(AUTH_DATA['u_id']),
        'profile_img_url': ''
    }

def test_profile_sethandle():
    with pytest.raises(AccessError) as error:
        user.profile_sethandle(_INVALID_VALUE, 'Jsmith')
    assert str(error.value) == '400 Bad Request: Token is invalid'

    with pytest.raises(ValueError) as error:
        user.profile_sethandle(TOKEN, 'J' * 21)
    assert str(error.value) == '400 Bad Request: Handle name exceeded 20 characters'

    assert user.profile_sethandle(TOKEN, 'jonnosmith') == {}

    assert user.profile(TOKEN, AUTH_DATA['u_id']) == {
        'email': 'johnsmith10111@hotmail.com',
        'name_first': 'john',
        'name_last': 'smith',
        'handle_str': 'jonnosmith',
        'profile_img_url': ''
    }

# testing urls (valid/invalid) with incorrect image extension
@pytest.mark.parametrize('img_url', _INVALID_IMG)
def test_profiles_uploadphoto_invalid_image(img_url):
    with pytest.raises(ValueError) as error:
        user.profiles_uploadphoto(TOKEN, img_url, 0, 0, 10, 10, _PORT)
    assert str(error.value) == "400 Bad Request: Image is not a JPG"

# testing crop ranges that are invalid
@pytest.mark.parametrize('start_x,start_y,end_x,end_y', _IMG_RANGES)
def test_profiles_uploadphoto_invalid_range(start_x, start_y, end_x, end_y):
    with pytest.raises(ValueError) as error:
        user.profiles_uploadphoto(TOKEN, _IMAGE_URL, start_x, start_y, end_x, end_y, _PORT)
    assert str(error.value) == "400 Bad Request: The boundary of the image is not valid"

# testing other cases
def test_profiles_uploadphoto():
    # unauthorise user test
    with pytest.raises(AccessError) as error:
        user.profiles_uploadphoto(_INVALID_VALUE, _IMAGE_URL, 0, 0, 100, 100, _PORT)
    assert str(error.value) == '400 Bad Request: Token is invalid'

    # invalid url without a downloadable image
    with pytest.raises(ValueError) as error:
        user.profiles_uploadphoto(TOKEN, _INVALID_URL, 0, 0, 100, 100, _PORT)
    assert str(error.value) == "400 Bad Request: Image upload failed. Provided url didn't return 200 OK status code"

    assert user.profiles_uploadphoto(TOKEN, _IMAGE_URL, _START_X, _START_Y, _END_X, _END_Y, _PORT) == {}

# this can't really be tested elegantly due to persistence of data
# so we're just testing the number of users in all our tests
def test_all():
    assert len(user.all(TOKEN)['users']) == 30
