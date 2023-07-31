#!/usr/bin/python3
'''
Flask route that returns json status response.
'''

from models import storage, classes
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/state', methods=['GET', 'POST'])
def states_no_id():
    '''retrives a list of all states.'''
    if request.method == 'GET':
        all_states = storage.all('State')
        all_states = list(obj.to_dict() for obj in all_states.values())
        return jsonify(all_states)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get("name") is None:
            abort(400, 'Missing name')
        State = classes.get("State")
        new_object = State(**req_json)
        new_object.save()
        return jsonify(new_object.to_dict()), 201


@app_views.route('states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def states_with_id(state_id=None):
    '''state route to handle http method for requested state by id.'''
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404, 'Not found')
    if request.method == 'GET':
        return jsonify(state_obj.to_dict())

    if request.method == 'DELETE':
        state_obj.delete()
        del state_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(404, 'Not a JSON')
        state_obj.bm_update(req_json)
        return jsonify(state_obj.to_dict()), 200
