#!/usr/bin/python3
'''implements http requests for class city includes POST, GET, PUT AND DELETE
   request.
 '''
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import request, jsonify, abort, make_response


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    '''http request route that returns all cities in a state.'''
    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)
    return jsonify([city.to_dict() for city in obj_state.cities])


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_cities(state_id):
    '''http route that handles a post request.'''
    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)

    req_json = request.get_json()
    if not req_json:
        abort(400, 'Not a JSON')
    if req_json.get('name') is None:
        abort(400, 'Missing name')

    new_city = City(**req_json)
    setattr(obj, 'state_id', state_id)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    '''http route method that gets a city by id.'''
    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)
    return jsonify(obj_city.to_dict())


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    '''http route that handle a put request for cities.'''
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    new_city = request.get_json()
    if new_city is None:
        abort(400, 'Not a JSON')
    for k, v in new_city.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    '''http route that deletes a city object by id.'''
    obj_city = storage.get(City, city_id)
    obj_city.delete()
    storage.save()
    return make_response(jsonify({}), 200)
