#!/usr/bin/python3
'''implements http requests for class city includes POST, GET, PUT AND DELETE
   request.
 '''
from models import storage, classes
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def states_cities(state_id=None):
    ''' cities route to handle http method for requested cities by state.'''
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_cities = storage.all('City')
        state_cities = [obj.to_dict() for obj in all_cities.values()
                        if obj.state_id == state_id]
        return jsonify(state_cities)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get("name") is None:
            abort(400, 'Missing name')
        City = classes.get("City")
        req_json['state_id'] = state_id
        new_object = City(**req_json)
        new_object.save()
        return jsonify(new_object.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def cities_with_id(city_id=None):
    '''cities route to handle http methods for given cities'''
    cities_obj = storage.get('City', city_id)
    is cities_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(cities_obj.to_dict())

    if request.method == 'DELETE':
        cities_obj.delete()
        del cities_obj
        return ({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        cities_obj.bm_update(req_json)
        return jsonify(cities_obj.to_dict()), 200
