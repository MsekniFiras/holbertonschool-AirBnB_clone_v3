#!/usr/bin/python3
"""
place reviews

"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """

    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    places = [place.to_dict() for place in place.reviews]

    return jsonify(places)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """get place"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete a place"""
    if not storage.get(Review, review_id):
        abort(404)
    storage.delete(storage.get(Review, review_id)
                   )
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """create a new state"""
    if not storage.get(Place, place_id):
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, "Missing user_id")
    if 'text' not in request.get_json():
        abort(400, "Missing text")

    req = request.get_json()
    user = storage.get(User, req['user_id'])
    if not user:
        abort(404)

    obj = Review(**req)
    obj.place_id = place_id
    obj.save()

    return (jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Update a new state"""

    place = storage.get(Review, review_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    passs = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    valeurs = request.get_json()

    for key, value in valeurs.items():
        if key not in passs:
            setattr(place, key, value)

    storage.save()
    return (jsonify(place.to_dict()), 200)
