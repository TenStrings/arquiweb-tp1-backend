import flask
import random
from bson import ObjectId
from flask import Blueprint, jsonify, request
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import os

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
    image = pointData['name']
    categoryName = pointData['categoryName']
    print("debug", flush=True)
    categoryId = mongo.db.categories.find_one( {'title':categoryName}, projection={'_id':True} )['_id']
    print(categoryId, flush=True)
    newPoint = Point(position, name, description, image, categoryId, categoryName)
    mongo.db.points.insert_one(newPoint.__dict__)

    response = flask.make_response(jsonify({'inserted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


@point.route('/point/<id>/visibility', methods=['PUT'])
def updatePointVisibility(id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    pointData = request.get_json()

    name = pointData['name']
    position = pointData['position']
    description = pointData['description']
    categoryName = pointData['categoryName']
    image = pointData['image']
    visible = pointData['visible']

    point = Point(position, name, description, image, categoryName)
    point.visible = visible

    ack = mongo.db.points.update({'_id': ObjectId(id)}, point.__dict__)

    response = flask.make_response(jsonify({'updated': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


@point.route('/point/<id>', methods=['PUT'])
def updatePoint(id):
    data = request.files
    pointData = request.form

    values = {}

    name = pointData['name']
    description = pointData['description']
    categoryName = pointData['categoryName']
    img = data['file']

    values['name'] = name
    values['description'] = description
    values['categoryName'] = categoryName

    try:
        if os.environ.get('ENV') == 'development':
            img.save('/usr/src/web/app/static/pointImages/' + id)
            values['image'] =  "http://localhost:" + os.environ.get('PORT') + "/static/pointImages/" + id
        else:
            upload_result = upload(img, public_id = id)
            values['image'] = cloudinary.utils.cloudinary_url(upload_result['public_id'])[0]

    except Exception as e:
        print(e.message, flush=True)

    ack = mongo.db.points.update({'_id': ObjectId(id)}, {'$set': values})

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
