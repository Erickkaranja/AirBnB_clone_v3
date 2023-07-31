#!/usr/bin/python3

from flask import abort, request, jsonify
from api.v1.views import app_views
from model import storage, classes


@app_views.route('/users', methods=['GET', 'POST'])
def user_no_id():
    '''implements get and post requst on users.'''
    if request.method == 'GET':
        all_users = storage.all('Users')
        all_users = list(obj.to_dict() for obj in all_users.values())
        return jsonify(all_users)

    if request.method == 'POST':
        req_json = request.get_json()
        if request is None:
            abort(400, 'Not a JSON')
        if req_json.get('email') is None:
            abort(400, 'Missing email')
        if req_json.get('password') is None:
            abort(400, 'Missing password')
        User = classes.get('User')
        new_obj = User(**req_json)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user_with_id(user_id=None):
    '''implement get/put/delete requests of object user with given id.'''
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404, 'Not found')

    if request.json == 'GET':
        return jsonify(user_obj.to_dict())

    if request.json == 'DELETE':
        user_obj.delete()
        del useer_obj
        return jsonify({}), 200

    if request.json == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        user_obj.bm_update(req_json)
        return jsonify(user_obj.to_dict()), 200
