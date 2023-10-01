#!/usr/bin/python3
"""

"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route('/stats',  methods=['GET'], strict_slashes=False)
def number_of_object():
    '''
    retrieves the number of each objects by type
    '''
    classes = [Amenity, City, Place, Review, State, User]
    classes_names = ["amenities", "cities",
                     "places", "reviews", "states", "users"]

    dic = {}
    for i in range(len(classes)):
        dic[classes_names[i]] = storage.count(classes[i])

    return jsonify(dic)
