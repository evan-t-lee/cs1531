import os
import urllib.request
import urllib.error
import shutil
import hashlib
from PIL import Image
from server.error import ValueError
import server.auth as auth
import server.data as data

#####   CONSTANTS   #####

_CURR_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_CURR_DIR)
_TEMP_IMG_DIR = _CURR_DIR + "/temp_img/"
_IMG_DIR = _PARENT_DIR + "/static/imgurl/"

#####   CORE FUNCTIONS   #####

# if you are authorised, you can enter anyone's u_id and get information about them
# returns email, name_first, name_last and handle_str if successful
def profile(token, u_id):
    auth.validate_token(token)
    if u_id not in data.users.keys():
        raise ValueError(description="Invalid user")

    email = data.users[u_id]['email']
    name_first = data.users[u_id]['name_first']
    name_last = data.users[u_id]['name_last']
    handle_str = data.users[u_id]['handle_str']
    profile_img_url = data.users[u_id]['profile_img_url']

    return {
        'email': email,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle_str,
        'profile_img_url': profile_img_url
    }

# update the user's first and last name
@data.save(['users'])
def profile_setname(token, name_first, name_last):
    u_id = auth.validate_token(token)
    if len(name_first) > 50:
        raise ValueError(description="First name is more than 50 characters")
    if len(name_last) > 50:
        raise ValueError(description="Last name is more than 50 characters")

    data.users[u_id]['name_first'] = name_first
    data.users[u_id]['name_last'] = name_last
    return {}

# update the user's email
@data.save(['users'])
def profile_setemail(token, email):
    u_id = auth.validate_token(token)
    if not auth.is_email_valid(email):
        raise ValueError(description="Email is not valid")
    if auth.is_email_registered(email):
        raise ValueError(description="Email is already used")

    data.users[u_id]['email'] = email
    return {}

# Changes the user's handle name
@data.save(['users'])
def profile_sethandle(token, handle_str):
    u_id = auth.validate_token(token)
    if len(handle_str) > 20:
        raise ValueError(description="Handle name exceeded 20 characters")

    data.users[u_id]['handle_str'] = handle_str
    return {}

@data.save(['users'])
def profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, port):
    u_id = auth.validate_token(token)
    if not is_photo_jpg(img_url):
        raise ValueError(description="Image is not a JPG")

    file_dir = _TEMP_IMG_DIR + str(u_id) + '.jpg'
    mode = 'ab' if not os.path.exists(file_dir) else 'wb'

    # download the image and save to a temporary folder
    try:
        with urllib.request.urlopen(img_url) as response, open(file_dir, mode) as file:
            shutil.copyfileobj(response, file)
    except urllib.error.HTTPError:
        raise ValueError(description="Image upload failed. Provided url didn't return 200 OK status code")

    img = Image.open(file_dir)
    width, height = img.size

    if not is_crop_dimensions_valid(width, height, x_start, y_start, x_end, y_end):
        raise ValueError(description="The boundary of the image is not valid")

    # crop the image and save so it can be accessed via frontend
    cropped_img = img.crop((x_start, y_start, x_end, y_end))
    dimension_strings = [str(x) for x in [width, height, x_start, y_start, x_end, y_end]]
    cropped_img_name = "_".join([hashlib.sha256(img_url.encode()).hexdigest()] + dimension_strings) + '.jpg'
    cropped_img.save(_IMG_DIR + cropped_img_name, 'JPEG')

    img_url = f"http://localhost:{port}/imgurl/{cropped_img_name}"

    data.users[u_id]['profile_img_url'] = img_url
    return {}

def all(token):
    auth.validate_token(token)
    users = []
    for u_id in data.users:
        user = {
            'u_id': u_id,
            'email': data.users[u_id]['email'],
            'name_first': data.users[u_id]['name_first'],
            'name_last': data.users[u_id]['name_last'],
            'handle_str': data.users[u_id]['handle_str'],
            'profile_img_url': data.users[u_id]['profile_img_url']
        }
        users.append(user)

    return {'users': users}

#####   HELPER FUNCTIONS   #####

# checks the extension of the url
def is_photo_jpg(img_url):
    return img_url[-4:].lower() == ".jpg" or img_url[-5:].lower() == '.jpeg'

def is_crop_dimensions_valid(width, height, x_start, y_start, x_end, y_end):
    if x_start < 0 or y_start < 0:
        return False
    if x_end > width or y_end > height:
        return False
    if x_start >= x_end or y_start >= y_end:
        return False
    return True
