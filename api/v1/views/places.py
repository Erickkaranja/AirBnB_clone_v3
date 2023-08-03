#!/usr/bin/python3
'''implements http requests for place object'''
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def cities_places(city_id=None):
    '''city http request to handle place requests by city.'''
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_places = storage.all('Places')
        place_city = [obj.to_dict() for obj in all_places.values()
                      if obj.city_id == city_id]
        return jsonify(place_city)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')

        user_id = req_json.get('user_id')
        if user_id is None:
            abort(400, 'Missing user_id')

        if req_json.get('name') is None:
            abort(400, 'Missing name')

        users_id = storage.get('User', user_id)
        if users_id is None:
            abort(404, 'Not found')

        User = classes.get('User')
        req_json['user_id'] = user_id
        new_object = User(**req_json)
        new_object.save()
        return jsonify(new_object.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'])
def places_with_id(place_id=None):
    '''places route to handle https methods for all place.'''
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(place_obj.to_dict())

    if request.method == 'DELETE':
        place_obj.delete()
        del place_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.json()
        if req_json is None:
            abort(404, 'Not found')
        place_obj.bm_update(req_json)
        return jsonify(place_obj.to_dict()), 200
