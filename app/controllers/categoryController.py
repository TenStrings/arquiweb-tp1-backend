import flask
from bson import ObjectId
from flask import Blueprint, jsonify, request

from app.model.point import Point

category = Blueprint("category", __name__)

# no cambiar el lugar del import por las dependencias circulares
from app import mongo


@category.route('/category', methods=['GET'])
def getAllCategories():
    allCategories = mongo.db.categories.find({})
    result = [cat for cat in allCategories]
    response = flask.make_response(jsonify(result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response



@category.route('/category', methods=['POST'])
def addCategory():
    pointData = request.get_json()

    name = pointData['name']
    position = pointData['position']
    description = pointData['description']
    category = pointData['category']

    point = Point(position, name, description, category)

    mongo.db.points.insert_one(point.__dict__)
    response = flask.make_response(jsonify({'point inserted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response, 201


@category.route('/category/<id>', methods=['DELETE'])
def deletePoint(id):
    db_response = mongo.db.points.delete_one({'_id': ObjectId(id)})
    if db_response.deleted_count == 1:
        response = flask.make_response(jsonify({'deleted': True, 'message': 'record deleted'}))
        response.headers['Access-Control-Allow-Origin'] = '*'

        return response, 200
    else:
        response = flask.make_response(jsonify({'deleted': True, 'message': 'no record found'}))
        response.headers['Access-Control-Allow-Origin'] = '*'

        return response, 404


@category.route('/category', methods=['DELETE'])
def deleteAllPoints():
    mongo.db.points.remove({})

    response = flask.make_response(jsonify({'message': 'records deleted'}))
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response, 200
