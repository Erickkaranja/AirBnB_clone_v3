#!/usr/bin/python3
'''implements http requests for place object'''
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.state import State
from models.city import City
from models.user import User


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
    if req_json.get('user_id') is None:
        abort(400, 'Missing user_id')

    user_id = req_json.get('user_id')
    user_id = storage.get(User, user_id)
    if user_id is None:
        abort(404)
    if 'name' not in req_json:
        abort(400, 'Missing name')
    req_json['city_id'] = city_id
    new_place = Place()

    for k, v in req_json.items():
        if k in ["city_id", "user_id", "name", "description", "number_rooms",
                 "number_bathrooms", "max_guest", "price_by_night",
                 "latitude"]:
            setattr(new_place, k, v)
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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    ''' '''
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    data = request.get_json()

    if data and len(data):
        states = data.get("states", None)
        cities = data.get("cities", None)
        amenities = data.get("amenities", None)

    if not data or len(data) or (
           not states and
           not cities and
           not amenities):
        all_places = storage.all(Place)
        for places in all_places.values():
            return jsonify(places.to_dict())

    list_places = []
    if states:
        states_obj = [storage.get(State, state_id) for state_id in states]
        for state in states_obj:
            if state:
                for city in state.city:
                    if city:
                        for place in city.place:
                            list_places.append(place)

    if cities:
        cities_obj = [storage.get(City, city_id) for city_id in cities]
        for city in cities_obj:
            if city:
                for place in city.place:
                    list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenities, amenity_id) for amenity_id in
                         amenities_obj]
        list_place = [place for place in list_place if
                      all([am in place.amenities for am in amenities_obj])]
    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
