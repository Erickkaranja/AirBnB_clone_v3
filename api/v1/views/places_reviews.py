#!/usr/bin/python3
"""implements http request routes for our review class."""

from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    '''http route that handles get reguest for reviews by place id'''
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)

    return jsonify([reviews.to_dict() for review in obj_place.reviews])


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    '''http route request that handles a post request of review.'''
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    new_review = request.get_json()
    if new_review is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in new_review:
        abort(400, 'Missing user_id')

    user_id = new_review['user_id']
    obj_user = storage.get(User, user_id)
    if obj_user is None:
        abort(404)

    if 'text' not in new_review:
        abort(400, 'Missing text')
    new_obj = Review(**new_review)

    storage.new(new_obj)
    storage.save()
    return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    '''http route that handles a get request of a review by id.'''
    obj_review = storage.get(Review, review_id)
    if obj_review is None:
        abort(404)
    return jsonify(obj_review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    '''http route that handles a put request on reviews.'''
    obj_review = storage.get(Review, review_id)
    if obj_review is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    for k, v in req_json.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(obj_review, k, v)
    storage.save()
    return make_response(jsonify(obj_review.to_dict()), 200)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    '''http route that handles a delete request on reviews.'''
    obj_delete = storage.get(Review, review_id)
    if obj_delete is None:
        abort(404)
    obj_delete.delete()
    storage.save()
    return make_response(jsonify({}), 200)
