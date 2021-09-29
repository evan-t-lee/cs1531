"""Flask server"""
import sys
from flask_cors import CORS
from json import dumps
from flask import Flask, request, redirect, url_for, send_from_directory
from flask_cors import CORS
from flask_mail import Mail, Message
from werkzeug.exceptions import HTTPException

import server.auth as auth
import server.channel as channel
import server.message as message
import server.standup as standup
import server.user_profile as user
import server.data as data
from server.error import ValueError, AccessError

# HTTPExceptions attach p tags to error messages so we filter them out
def strip_p_tags(message):
    if message[0:3] == '<p>' and message[-4:] == '</p>':
        return message[3:-4]
    return message

def defaultValueErrorHandler(err):
    response = err.get_response()
    description = strip_p_tags(err.get_description())
    response.data = dumps({
        "code": err.code,
        "name": "Value Error",
        "message": description,
    })
    response.content_type = 'application/json'
    return response

def defaultAccessErrorHandler(err):
    response = err.get_response()
    description = strip_p_tags(err.get_description())
    response.data = dumps({
        "code": err.code,
        "name": "Value Error",
        "message": description,
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
APP.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'slackrteam@gmail.com',
    MAIL_PASSWORD = "insertnamehere123"
)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(ValueError, defaultValueErrorHandler)
APP.register_error_handler(AccessError, defaultAccessErrorHandler)
CORS(APP)

@APP.route('/imgurl/<fname>')
def send_photo(fname):
    return redirect(url_for('static', filename='imgurl/' + fname), code=301)

######## ECHO ROUTES ########

@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })

@APP.route('/echo/post', methods=['POST'])
def echo2():
    """ Description of function """
    return dumps({
        'echo' : request.form.get('echo'),
    })

######## AUTH ROUTES ########

@APP.route('/auth/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    return dumps(auth.register(email, password, name_first, name_last))

@APP.route('/auth/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    return dumps(auth.login(email, password))

@APP.route('/auth/logout', methods=['POST'])
def logout():
    return dumps(auth.logout(request.form.get('token')))

@APP.route('/auth/passwordreset/request', methods=['POST'])
def passwordrequest():
    email = request.form.get('email')
    email_data = auth.passwordreset_request(email)
    if email_data == {}:
        return "Email could not be sent"

    mail = Mail(APP)
    try:
        msg = Message(email_data['title'],
            sender="slackrteam@gmail.com",
            recipients=[email])
        msg.body = email_data['body']
        mail.send(msg)
        return 'Mail sent!'
    except Exception as e:
        return (str(e))

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def passwordreset():
    reset_code = request.form.get('reset_code')
    new_password = request.form.get('new_password')
    return dumps(auth.passwordreset_reset(reset_code, new_password))

######## CHANNEL ROUTES ########

@APP.route('/channel/invite', methods=['POST'])
def invite():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    return dumps(channel.invite(token, channel_id, u_id))

@APP.route('/channel/details', methods=['GET'])
def details():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return dumps(channel.details(token, channel_id))

@APP.route('/channel/messages', methods=['GET'])
def messages():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    return dumps(channel.messages(token, channel_id, start), default=str)

@APP.route('/channel/leave', methods=['POST'])
def leave():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    return dumps(channel.leave(token, channel_id))

@APP.route('/channel/join', methods=['POST'])
def join():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    return dumps(channel.join(token, channel_id))

@APP.route('/channel/addowner', methods=['POST'])
def addowner():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    return dumps(channel.addowner(token, channel_id, u_id))

@APP.route('/channel/removeowner', methods=['POST'])
def removeowner():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    u_id = int(request.form.get('u_id'))
    return dumps(channel.removeowner(token, channel_id, u_id))

@APP.route('/channels/list', methods=['GET'])
def list():
    token = request.args.get('token')
    return dumps(channel.list(token))

@APP.route('/channels/listall', methods=['GET'])
def listall():
    token = request.args.get('token')
    return dumps(channel.listall(token))

@APP.route('/channels/create', methods=['POST'])
def create():
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public') == "True"
    return dumps(channel.create(token, name, is_public))

######## MESSAGE ROUTES ########

@APP.route('/message/sendlater', methods=['POST'])
def sendlater():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message_text = request.form.get('message')
    time_sent = int(float(request.form.get('time_sent')))
    return dumps(message.sendlater(token, channel_id, message_text, time_sent))

@APP.route('/message/send', methods=['POST'])
def message_send_route():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message_text = request.form.get('message')
    return dumps(message.send(token, channel_id, message_text))

@APP.route('/message/remove', methods=['DELETE'])
def remove():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    return dumps(message.remove(token, message_id))

@APP.route('/message/edit', methods=['PUT'])
def edit():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    message_text = request.form.get('message')
    return dumps(message.edit(token, message_id, message_text))

@APP.route('/message/react', methods=['POST'])
def react():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    return dumps(message.react(token, message_id, react_id))

@APP.route('/message/unreact', methods=['POST'])
def unreact():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))
    return dumps(message.unreact(token, message_id, react_id))

@APP.route('/message/pin', methods=['POST'])
def pin():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    return dumps(message.pin(token, message_id))

@APP.route('/message/unpin', methods=['POST'])
def unpin():
    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    return dumps(message.unpin(token, message_id))

@APP.route('/search', methods=['GET'])
def search_route():
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    return dumps(message.search(token, query_str))
    
######## STANDUP ROUTES ########

@APP.route('/standup/start', methods=['POST'])
def start():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    length = int(request.form.get('length'))
    return dumps(standup.start(token, channel_id, length))

@APP.route('/standup/active', methods=['GET'])
def active():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return dumps(standup.active(token, channel_id))

@APP.route('/standup/send', methods=['POST'])
def standup_send_route():
    token = request.form.get('token')
    channel_id = int(request.form.get('channel_id'))
    message_text = request.form.get('message')
    return dumps(standup.send(token, channel_id, message_text))

######## USER PROFILE ROUTES ########
@APP.route('/user/profile', methods=['GET'])
def profile():
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    return dumps(user.profile(token, u_id))

@APP.route('/user/profile/setname', methods=['PUT'])
def setname():
    token = request.form.get('token')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    return dumps(user.profile_setname(token, name_first, name_last))

@APP.route('/user/profile/setemail', methods=['PUT'])
def setemail():
    token = request.form.get('token')
    email = request.form.get('email')
    return dumps(user.profile_setemail(token, email))

@APP.route('/user/profile/sethandle', methods=['PUT'])
def sethandle():
    token = request.form.get('token')
    handle_str = request.form.get('handle_str')
    return dumps(user.profile_sethandle(token, handle_str))

@APP.route('/user/profiles/uploadphoto', methods=['POST'])
def uploadphoto():
    token = request.form.get('token')
    img_url = request.form.get('img_url')
    x_start = int(request.form.get('x_start'))
    y_start = int(request.form.get('y_start'))
    x_end = int(request.form.get('x_end'))
    y_end = int(request.form.get('y_end'))
    port = request.host.split(':')[1]
    return dumps(user.profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end, port))

@APP.route('/users/all', methods=['GET'])
def all():
    token = request.args.get('token')
    return dumps(user.all(token))


@APP.route('/admin/userpermission/change', methods=['POST'])
def change():
    token = request.form.get('token')
    u_id = int(request.form.get('u_id'))
    permission_id = int(request.form.get('permission_id'))
    return dumps(auth.admin_userpermission_change(token, u_id, permission_id))

if __name__ == '__main__':
    data.init_users()
    data.init_channels()
    data.init_messages()
    data.init_codes()
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
