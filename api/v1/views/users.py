#!/usr/bin/python3
"""
manipulate the users

"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """ger users"""
    states = []
    for i in storage.all(User).values():
        states.append(i.to_dict())

    return jsonify(states)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """get user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """delete a user"""
    if not storage.get(User, user_id):
        abort(404)
    storage.delete(storage.get(User, user_id))
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def post_user():
    """create a new user"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'password' not in request.get_json():
        abort(400, "Missing password")

    if "email" not in request.get_json():
        abort(400, 'Missing email')
    req = request.get_json()
    obj = User(**req)
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=["PUT"])
def put_user(user_id):
    """Update a new user"""

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    passs = ['id', 'created_at', 'updated_at']

    valeurs = request.get_json()

    for key, value in valeurs.items():
        if key not in passs:
            setattr(user, key, value)

    storage.save()
    return (jsonify(user.to_dict()), 200)
