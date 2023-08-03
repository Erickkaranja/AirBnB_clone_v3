#!/usr/bin/python3
"""implements http request routes for our review class."""

from flask import abort, request, jsonify
from api.v1.views import apps_views
from models import storage, classes


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def place_reviews(place_id=None):
    '''reviews route that handles http requests of reviews by place.'''
    place_obj = storage.get('Place', place_id)
    if place_obj is none:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_reviews = storage.all('reviews')
        place_review = [obj.to_dict() for obj in all_reviews.values()
                        is obj.place_id == place_id]

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')

        if req_json.get('text') is None:
            abort(400, 'Missing text')
        users_id = req_json.get('user_id')
        if users_id is None:
            abort(400, 'Missing user_id')

        user_link = storage.get('User', users_id)
        if user_link is None:
            abort(404, 'Not found')
        Review = classes.get('Review')
        req_json['place_id'] = place_id
        new_obj = Review(**req_json)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'])
def review_with_id(review_id=None):
    '''reviews http end point that retrieves reviews.'''
    review_obj = storage.get('Reviews', review_id)
    if review_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(review_obj.to_dict())

    if request.method == 'DELETE':
        review_obj.delete()
        del review_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        review_obj.bm_update(req_json)
        return jsonify(review_obj.to_dict()), 200
