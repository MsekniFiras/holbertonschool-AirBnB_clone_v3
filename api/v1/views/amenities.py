#!/usr/bin/python3
"""
manipulate the amenitiess

"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """get amenities"""
    list_of_amenities = []
    for i in storage.all(Amenity).values():
        list_of_amenities.append(i.to_dict())

    return jsonify(list_of_amenities)


@app_views.route('/amenities/<amenity_id>/', strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id):
    """get amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """delete a amenities"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def post_amenity():
    """create a new amenities"""
    if not request.get_json():
        abort(400, "Not a JSON")

    if 'name' not in request.get_json():
        abort(400, "Missing name")

    req = request.get_json()
    obj = Amenity(**req)
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Update a new amenities"""

    amenity = storage.get(Amenity, amenity_id)
    valeurs = request.get_json()
    if not amenity:
        abort(404)

    if not valeurs:
        abort(400, "Not a JSON")

    passs = ['id', 'created_at', 'updated_at']

    for key, value in valeurs.items():
        if key not in passs:
            setattr(amenity, key, value)

    storage.save()
    return (jsonify(amenity.to_dict()), 200)
