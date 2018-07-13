from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)

users = [
    {
        'id': 1,
        'name': u'proba',
        'email': u'proba@proba.proba'
    },
    {
        'id': 2,
        'name': u'nikola',
        'email': u'nikolailic02@gmail.com'
    }
]


@app.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    return jsonify({'users': [make_public_user(user) for user in users]})


@app.route('/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': make_public_user(user[0])})


@app.route('/users', methods=['POST'])
@auth.login_required
def create_user():
    if not request.json or not 'name' in request.json:
        abort(400)
    user = {
        'id': users[-1]['id'] + 1,
        'name': request.json['name'],
        'email': request.json.get('email', "")
    }
    users.append(user)
    return jsonify({'user': make_public_user(user)}), 201


@app.route('/users/<int:user_id>', methods=['PUT'])
@auth.login_required
def update_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)
    if 'email' in request.json and type(request.json['email']) is not unicode:
        abort(400)
    user[0]['name'] = request.json.get('name', user[0]['name'])
    user[0]['email'] = request.json.get('email', user[0]['email'])
    return jsonify({'user': make_public_user(user[0])})


@app.route('/users/<int:user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    users.remove(user[0])
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def make_public_user(user):
    new_user = {}
    for field in user:
        if field == 'id':
            new_user['uri'] = url_for('get_user', user_id=user['id'], _external=True)
        else:
            new_user[field] = user[field]
    return new_user


@auth.get_password
def get_password(username):
    if username == 'pi':
        return 'raspberry'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


if __name__ == '__main__':
    app.run(debug=True)
