#!/usr/bin/python3
"""
manipulate the states

"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """ger states"""
    states = []
    for i in storage.all(State).values():
        states.append(i.to_dict())

    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_state(state_id):
    """get state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """delete a state"""
    if not storage.get(State, state_id):
        abort(404)
    storage.delete(storage.get(State, state_id))
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_state():
    """create a new state"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    req = request.get_json()
    obj = State(**req)
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=["PUT"])
def put_state(state_id):
    """Update a new state"""

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    passs = ['id', 'created_at', 'updated_at']

    valeurs = request.get_json()

    for key, value in valeurs.items():
        if key not in passs:
            setattr(state, key, value)

    storage.save()
    return (jsonify(state.to_dict()), 200)
