import flask
from bson import ObjectId
from flask import Blueprint, jsonify, request

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
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    pointData = request.get_json()

    position = pointData['position']
    name = pointData['name']
    description = pointData['description']
    image = "TODO send fname from Frontend"
    categoryName = pointData['categoryName']

    newPoint = Point(position, name, description, image, category)

    mongo.db.points.insert_one(newPoint.__dict__)

    response = flask.make_response(jsonify({'inserted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


@point.route('/point/<id>', methods=['PUT'])
def updatePoint(id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    pointData = request.get_json()

    name = pointData['name']
    position = pointData['position']
    description = pointData['description']
    categoryName = pointData['categoryName']
    image = "TODO send fname from Frontend"
    visible = pointData['visible']

    point = Point(position, name, description, image, categoryName)
    point.visible = visible

    ack = mongo.db.points.update({'_id': ObjectId(id)}, point.__dict__)

    response = flask.make_response(jsonify({'updated': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


def updatePointsOfCategory(categoryName, newCategoryName, is_visible):
    ack = mongo.db.points.update_many({'categoryName': categoryName},
                                      {'$set': {'categoryName': newCategoryName, 'visible': is_visible}})


def updatePointsOfCategoryWithTitle(categoryName, newCategoryName):
    ack = mongo.db.points.update_many({'categoryName': categoryName}, {'$set': {'categoryName': newCategoryName}})


@point.route('/point/<id>', methods=['DELETE'])
def deletePoint(id):
    db_response = mongo.db.points.delete_one({'_id': ObjectId(id)})

    response = flask.make_response(jsonify({'deleted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200


def deletePointsOfCategory(categoryName):
    db_response = mongo.db.points.remove({'categoryName': categoryName})
