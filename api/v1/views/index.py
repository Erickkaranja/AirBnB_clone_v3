#!/usr/bin/python3
"""contains the route to the status of our api."""
from api.v1.views import app_views
from flask import request
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    '''function that returns the status of our route'''
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count():
    '''returns the total counts of objects in our storage.'''
    return jsonify(amenities=storage.count('Amenity'),
                   cities=storage.count('City'),
                   places=storage.count('Place'),
                   reviews=storage.count('Review'),
                   states=storage.count('State'),
                   users=storage.count('User'))
