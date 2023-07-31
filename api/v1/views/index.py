#!/usr/bin/python3

from api.v1.views import app_views
from flask import request
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    '''function that returns the status of our route'''
    if request.method == 'GET':
        response = {"status": "OK"}
        return jsonify(response)


@app_view.route('/stats', methods=['GET'])
def count():
    '''returns the total counts of objects in our storage.'''
    if request.method == 'GET':
        response = {}
        obj = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for k, v in obj.items():
            response[v] = storage.count(key)
        return jsonify(response)
