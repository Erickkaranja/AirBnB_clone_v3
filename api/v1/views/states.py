#!/usr/bin/python3
'''
Flask route that returns json status response for our state object.
'''

from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    '''http route that return all states in our application.'''
    all_states = storage.all(State)
    return jsonify([state.to_dict() for state in all_states.values()])


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """http route that adds a creates a new state object."""
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if req_json.get('name') is None:
        abort(400, 'Missing name')

    new_state = State(**req_json)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    '''http method that returns a given state by id.'''
    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)
    return jsonify(obj_state.to_dict())


@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    '''http route that delete a state object by id.'''
    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)
    obj_state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''http route that updates a state object by id.'''
    req_json = request.get_json()
    if req_json is None:
        abort(404)
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(400, 'Not a JSON')

    for k, v in req_json.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
