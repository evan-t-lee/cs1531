from flask import Flask, request

app = Flask(__name__)

name_list = []

@app.route('/name/add', methods=['POST'])
def name_add():
    global name_list

    name = request.form.get('name')
    name_list += [name]

    return {}

@app.route('/names', methods=['GET'])
def names():
    global name_list
    return { 'names': name_list }

@app.route('/name/remove', methods=['DELETE'])
def name_remove():
    global name_list

    name = request.form.get('name')
    name_list.remove(name)

    return {}

if __name__ == '__main__':
    app.run()