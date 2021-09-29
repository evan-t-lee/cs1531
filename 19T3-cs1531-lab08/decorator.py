import sys

MESSAGE_LIST = []

def authorised(auth_token):
    return auth_token == "CrocodileLikesStrawberries"
            

def authorise(func):
    def wrapper(auth_token, *args, **kwargs):
        if not authorised(auth_token):
            raise ValueError("Invalid authentication")
        return func(*args, **kwargs)
    return wrapper

@authorise
def get_messages():   
    return MESSAGE_LIST

@authorise
def add_messages(msg):
    global MESSAGE_LIST
    MESSAGE_LIST.append(msg)


if __name__ == '__main__':
    auth_token = ""
    if len(sys.argv) == 2:
        auth_token = sys.argv[1]

    add_messages(auth_token, "Hello")
    add_messages(auth_token, "How")
    add_messages(auth_token, "Are")
    add_messages(auth_token, "You?")
    print(get_messages(auth_token))
