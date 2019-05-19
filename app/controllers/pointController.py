import flask
from bson import ObjectId
from flask import Blueprint, jsonify, request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity, get_jwt_claims
)

from app.model.point import Point

point = Blueprint("point", __name__)

# no cambiar el lugar del import por las dependencias circulares
from app import mongo


@point.route('/point', methods=['GET'])
def getAllPoints():
    allPoints = mongo.db.points.find({})
    result = [point for point in allPoints]
    response = flask.make_response(jsonify(result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@point.route('/point', methods=['POST'])
def addPoint():
    pointData = request.get_json()

    name = pointData['name']
    position = pointData['position']
    description = pointData['description']
    category = pointData['category']
    visible = True

    point = Point(position, name, description, category, visible)

    mongo.db.points.insert_one(point.__dict__)
    response = flask.make_response(jsonify({'point inserted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response, 201

@point.route('/point/<id>', methods=['PUT'])
@jwt_required
def putPoint(id):
    admin = claims = get_jwt_claims()['admin']

    if not admin:
        return jsonify({"msg": "Invalid credentials"}), 401
    
    pointData = request.get_json()

    name = pointData['name']
    position = pointData['position']
    description = pointData['description']
    category = pointData['categoryName']
    visible = pointData['visible']

    point = Point(position, name, description, category, visible)
    print("point", point, flush=True)
    ack = mongo.db.points.update({'_id' : ObjectId(id)}, point.__dict__)
    print("ack", ack)

    response = flask.make_response(jsonify({'point inserted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response, 201

@point.route('/point/<id>', methods=['DELETE'])
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


@point.route('/point', methods=['DELETE'])
def deleteAllPoints():
    mongo.db.points.remove({})

    response = flask.make_response(jsonify({'message': 'records deleted'}))
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response, 200
