#!/usr/bin/python3
""" Create a new view for State that handles all default RestFul API """

from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from flask import Flask, jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def Places_Get(city_id):
    """Retrieves the list of all Place objects of a City """

    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    data = storage.all('Place')
    places_list = []

    for key, value in data.items():
        if value.city_id == city_id:
            places_list.append(value.to_dict())

    return jsonify(places_list), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def Place_Get(place_id):
    """ Retrieves a Place object """
    place = storage.get('Place', place_id)

    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def Places_Delete(place_id):
    """ Delete a Place object """
    data = storage.all('Place')
    del_place = storage.get('Place', place_id)
    if del_place is None:
        abort(404)
    storage.delete(del_place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def Places_Post(city_id):
    """ Create a Place """
    data_req = request.get_json()
    data_city = storage.get('City', city_id)

    if data_city is None:
        abort(404)
    if not data_req:
        return jsonify({"message": "Not a JSON"}), 400
    if "user_id" not in data_req:
        return jsonify({"message": "Missing user_id"}), 400
    else:
        data_user = storage.get('User', data_req["user_id"])
        if data_user is None:
            print("entro", data_req["user_id"])
            abort(404)
    if "name" not in data_req:
        return jsonify({"message": "Missing name"}), 400

    data_req["city_id"] = city_id
    print(data_req)
    new_place = Place(**data_req)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def Places_Put(place_id):
    """ Updates a Place object """
    data = storage.get('Place', place_id)
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
