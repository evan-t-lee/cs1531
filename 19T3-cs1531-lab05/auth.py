from flask import Flask, request
import jwt

app = Flask(__name__)

password_data = {}
secret_data = {}

@app.route('/user/create', methods=['POST'])
def user_create():
    global user_data

    data = request.form
    password, secret = data['password'], data['secret']
    token = jwt.encode({'password': password}, secret, algorithm='HS256').decode('utf-8')
    password_data[password] = token
    secret_data[token] = secret

    return {'token': token}

@app.route('/user/connect', methods=['PUT'])
def user_connect():
    global user_data

    password = request.form.get('password')

    return {'token': password_data[password]}

@app.route('/user/secret', methods=['GET'])
def user_secret():
    global user_data

    token = request.form.get('token')

    return {'secret': secret_data[token]}

if __name__ == '__main__':
    app.run()