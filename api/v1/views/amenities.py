#!/usr/bin/python3
'''review module which implements http request for amenities.'''

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    '''http method that handles a get request on amenities.'''
    all_amenities = storage.all(Amenity)
    return jsonify(amenities.to_dict() for amenity in all_amenities.values())


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
    '''http method that handles a post request on amenities.'''
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if 'name' not in req_json:
        abort(400, 'Missing name')
    obj_amenities = Amenity(**req_json)
    storage.new(obj_amenities)
    storage.save()
    return make_response(jsonify(obj_amenities.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    '''http method that handles a get request on amenities by id.'''
    obj_amenities = storage.get(Amenity, amenity_id)
    if obj_amenities is None:
        abort(404)
    return jsonify(obj_amenities.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenities(amenity_id):
    '''http method that handles a put request on amenities by id.'''
    obj_amenities = storage.get(Amenity, amenity_id)
    if obj_amenities is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')

    for k, v in req_json.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj_amenities, k, v)

    return make_response(jsonify(obj_amenities.to_dict()), 200)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenity_id):
    '''http request that handle a delete request on amenities.'''
    obj_amenity = storage.get(Amenities, amenity_id)
    if obj_amenity is None:
        abort(404)
    obj_amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)
