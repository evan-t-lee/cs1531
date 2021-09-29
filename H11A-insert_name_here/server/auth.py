import time
import random
import string
import hashlib
import re
import jwt
from server.error import ValueError, AccessError
import server.data as data

#####   CONSTANTS   #####

_EMAIL_REGEX = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
_MIN_PASSWORD_LENGTH = 6
_SECRET = "t8nc9vyw8t9peynv"
_ALGORITHM = 'HS256'
_CODE_VALID_TIME = 10 * 60 # 10 minutes

#####   CORE FUNCTIONS   #####

# lets the user login provided correct credentials are given
@data.save(['users'])
def login(email, password):
    if not is_email_valid(email):
        raise ValueError(
            description="Given email is not a valid email address")
    if not is_email_registered(email):
        raise ValueError(description="Email doesn't belong to a user")

    u_id = get_id_from_email(email)

    if data.users[u_id]['password'] != hash(password):
        raise ValueError(description="Password is incorrect")

    token = generate_token(u_id)
    data.users[u_id]['tokens'].append(token)

    return {"u_id": u_id, "token": token}

# lets the user logout safely by having their token invalidated
@data.save(['users'])
def logout(token):
    try:
        u_id = validate_token(token)
        data.users[u_id]['tokens'].remove(token)
        return {'is_success': True}
    except AccessError:
        return {'is_success': False}

# lets a user register with their credentials
@data.save(['users'])
def register(email, password, name_first, name_last):
    # error checking
    if not is_email_valid(email):
        raise ValueError(
            description="Given email is not a valid email address")
    if is_email_registered(email):
        raise ValueError(
            description="Email address is being used by another user")
    if not is_password_valid(password):
        raise ValueError(
            description="Password entered is invalid (must have at least 6 characters)")
    if not 0 < len(name_first) < 51:
        raise ValueError(
            description="First name must be between 1 and 50 characters long")
    if not 0 < len(name_last) < 51:
        raise ValueError(
            description="Last name must be between 1 and 50 characters long")

    # guarantees unique u_ids since users can't leave slackr at present
    u_id = len(data.users.keys()) + 1

    base_handle = handle_str = name_first.lower() + name_last.lower()
    handle_extension = 0

    # verify that the generated handle hasn't been used by another user
    while not is_handle_unique(handle_str):
        # try make the handle unique by appending the user's id
        if handle_extension == 0:
            handle_extension = u_id
        else:
            # then just keep adding 1 until it's unique
            handle_extension += 1
        handle_str = base_handle + str(handle_extension)

    data.users[u_id] = {}
    data.users[u_id]['email'] = email
    data.users[u_id]['password'] = hash(password)
    data.users[u_id]['name_first'] = name_first
    data.users[u_id]['name_last'] = name_last
    data.users[u_id]['handle_str'] = handle_str
    data.users[u_id]['profile_img_url'] = ""

    # first user to sign up is slackr owner, the rest are members
    if u_id == 1:
        data.users[u_id]['permission_id'] = data._PERMISSION_OWNER
    else:
        data.users[u_id]['permission_id'] = data._PERMISSION_MEMBER

    token = generate_token(u_id)
    data.users[u_id]['tokens'] = [token]

    return {"u_id": u_id, "token": token}

# lets the user request a password change if the supplied email address
# matches that of a registered user
@data.save(['codes'])
def passwordreset_request(email):
    if not is_email_registered(email):
        raise ValueError(description="Email doesn't belong to a user")

    code = generate_code()
    while code in data.reset_codes.keys():
        code = generate_code()

    # time data is used for expiration check later
    data.reset_codes[code] = {
        'email': email,
        'time': time.time() + _CODE_VALID_TIME
    }

    text = f"Dear user,\nPlease use this reset code (valid for 10 minutes) to set a new password for your slackr account:\n{code}"

    # this return type is for use in server.py
    return {
        'title': "Your slackr account password reset code",
        'body': text}

# changes a users password if the given reset code is valid
@data.save(['users', 'codes'])
def passwordreset_reset(reset_code, new_password):
    if not is_reset_code_valid(reset_code):
        raise ValueError(description="Reset code is invalid")
    if not is_password_valid(new_password):
        raise ValueError(
            description="Password entered is invalid (must have at least 5 characters)")

    email = data.reset_codes[reset_code]['email']
    u_id = get_id_from_email(email)
    data.users[u_id]['password'] = hash(new_password)
    del data.reset_codes[reset_code]

    return {}

@data.save(['users'])
def admin_userpermission_change(token, u_id, permission_id):
    if u_id not in data.users:
        raise ValueError(description='This user does not exist')
    if permission_id > data._PERMISSION_MEMBER or permission_id < data._PERMISSION_OWNER:
        raise ValueError(description='Specified permission is invalid')

    auth_u_id = validate_token(token)
    auth_perm = data.users[auth_u_id]['permission_id']
    user_perm = data.users[u_id]['permission_id']

    if not can_change_permission(auth_perm, user_perm):
        raise AccessError(
            description="User is not permitted to make permission changes")

    data.users[u_id]['permission_id'] = permission_id
    data.save_users()

    return {}

#####   HELPER FUNCTIONS   #####

# performs criteria check on email address structure validity
def is_email_valid(email):
    return re.search(_EMAIL_REGEX, email)

# checks if an email belongs to a registered user
def is_email_registered(email):
    for u_id in data.users.keys():
        if data.users[u_id]['email'] == email:
            return True
    return False

# performs criteria check on minimum password length
def is_password_valid(password):
    return len(password) >= _MIN_PASSWORD_LENGTH

# verifies if a reset code is one that was validly generated
def is_reset_code_valid(code):
    if code not in data.reset_codes.keys():
        return False
    if time.time() > data.reset_codes[code]['time']:
        return False
    return True

# hashes a password for safer non-plaintext storage
def hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

# generate a token for a given u_id
def generate_token(u_id):
    payload = {
        'u_id': u_id,
        'time': time.time()
    }

    return jwt.encode(payload, _SECRET, algorithm=_ALGORITHM).decode('UTF-8')

# verifies that a token is valid then returns the u_id of the payload
def validate_token(token):
    u_id = None
    try:
        decoded = jwt.decode(token.encode(), _SECRET, algorithms=_ALGORITHM)
        u_id = decoded['u_id']
        if token not in data.users[u_id]['tokens']:
            raise AccessError(description="Token is invalid")
    except Exception:
        raise AccessError(description="Token is invalid")
    return u_id

# retrieves to u_id mapped to an email
def get_id_from_email(email):
    for u_id in data.users.keys():
        if data.users[u_id]['email'] == email:
            return u_id
    return None

# generates a random reset code
def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# checks if a handle is being used by any user
def is_handle_unique(handle_str):
    for user in data.users.values():
        if user['handle_str'] == handle_str:
            return False
    return True

# verify the current user can make a permission change
def can_change_permission(auth_perm, user_perm):
    if auth_perm == data._PERMISSION_MEMBER:
        return False
    if auth_perm == data._PERMISSION_ADMIN and user_perm == data._PERMISSION_OWNER:
        return False
    return True
