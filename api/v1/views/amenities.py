#!/usr/bin/python3
'''review module which implements http request for amenities.'''

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities_no_id():
    '''retrieves all amenities'''
    if request.method == 'GET':
        all_amenities = storage.all('Amenities')
        all_amenities = list(obj.to_dict() for obj in all_amenities.values())
        return jsonify(all_amenities)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('name') is None:
            abort(400, 'Missing name')
        Amenity = classes.get('Amenity')
        new_obj = Amenity(**req_json)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'])
def amenities_with_id(amenity_id=None):
    '''gets/put/delete requests for amenity_id.'''
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(amenity_obj.to_dict())

    if request.method == 'DELETE':
        amenity_obj.delete()
        del amenity_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(404, 'Not a JSON')
        amenity_obj(**req_json)
        return jsonify(amenity_obj.to_dict()), 200
