#!/usr/bin/python3
""" Create a new view for State that handles all default RestFul API """

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from flask import Flask, jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def Review_Get(place_id):
    """Retrieves the list of all Review objects of the Place """

    data = storage.all('Place')
    place = storage.get("Place", place_id)
    review_list = []

    if place is None:
        abort(404)
    for key, value in data.items():
        if value.place_id == place_id:
            review_list.append(value.to_dict())
    return jsonify(review_list), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def Review_Get(review_id):
    """ Retrieves a Review object """
    review = storage.get('Review', place_id)

    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def Review_Delete(review_id):
    """ Delete a Review object """
    data = storage.all('Review')
    del_review = storage.get('Review', review_id)
    if del_review is None:
        abort(404)
    storage.delete(del_review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def Review_Post(place_id):
    """ Create a Review """
    data_req = request.get_json()
    data_place = storage.get('Place', place_id)

    if data_place is None:
        abort(404)
    if not data_req:
        return jsonify({"message": "Not a JSON"}), 400
    if "user_id" not in data_req:
        return jsonify({"message": "Missing user_id"}), 400
    else:
        data_user = storage.get('User', data_req["user_id"])
        if data_user is None:
            abort(404)
    if "text" not in data_req:
        return jsonify({"message": "Missing text"}), 400

    data_req["place_id"] = place_id
    new_review = Review(**data_req)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def Review_Put(review_id):
    """ Updates a Review object """
    data = storage.get('Review', place_id)
    data_req = request.get_json()

    if data is None:
        abort(404)
    if not data_req:
        return jsonify({"message": "Not a JSON"}), 400

    for key, value in data_req.items():
        if key in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            continue
        setattr(data, key, value)
    data.save()
    return jsonify(data.to_dict()), 200
