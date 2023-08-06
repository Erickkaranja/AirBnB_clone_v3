#!/usr/bin/python3
'''implements http requests for place object'''
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place(city_id):
    '''http route that handles a get request for places based on id'''
    all_cities = storage.get(City, city_id)
    if all_cties is None:
        abort(404)
    return jsonify([place.to_dict() for place in all_cities.cities])


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    '''http route that handles a post request for a place.'''
    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)
    req_json = request.get_json()
    if not req_json:
        abort(400, 'Not a JSON')
    if user_id not in req_json:
        abort(400, 'Missing user_id')
    user_id = storage.get(User, user_id)
    if user_id is None:
        abort(404)
    if 'name' not in req_json:
        abort(400, 'Missing name')

    new_place = Place(**req_json)
    setattr(new_place, 'city_id', city_id)
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    '''http route that handles a get request of a place by id.'''
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    return jsonify(obj_place.to_dict(), 200)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    '''http method that handles a put request.'''
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    for k, v in req_json.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(obj_place, k, v)
    storage.save()
    return make_response(jsonify(obj_place.to_dict()), 200)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''http method that handles a delete request on a place by id.'''
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    obj_place.delete()
    storage.save()
    return make_response(jsonify({}), 200)
