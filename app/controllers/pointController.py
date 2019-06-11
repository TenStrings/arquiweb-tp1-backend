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

    pointData = request.form
    image = ""
    if pointData['has_file']  == "true":
        files = request.files
        img = files['file']
        if os.environ.get('ENV') == 'development':
            fake_id = str(random.randint(0,10000))
            img.save('/usr/src/web/app/static/pointImages/' + fake_id)
            image =  "http://localhost:" + os.environ.get('PORT') + "/static/pointImages/" + fake_id
        else:
            upload_result = upload(img)
            image = cloudinary.utils.cloudinary_url(upload_result['public_id'])[0]

    newPoint = Point({'lat':pointData['positionLat'], 'lng':pointData['positionLng'] },
                     pointData['name'],
                     pointData['description'],
                     image,
                     pointData['categoryId'],
                     pointData['categoryName'])

    mongo.db.points.insert_one(newPoint.__dict__)

    response = flask.make_response(jsonify({'inserted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201

@point.route('/point/<id>', methods=['PUT'])
def updatePoint(id):

    pointData = request.form
    values = {}
    values['name'] = pointData['name']
    values['description'] = pointData['description']
    values['image'] = pointData['image']
    values['categoryId'] = pointData['categoryId']
    values['categoryName'] = pointData['categoryName']

    if pointData['has_file'] == "true":
        files = request.files
        img = files['file']

        if os.environ.get('ENV') == 'development':
            img.save('/usr/src/web/app/static/pointImages/' + id)
            values['image'] =  "http://localhost:" + os.environ.get('PORT') + "/static/pointImages/" + id
        else:
            upload_result = upload(img, public_id = id)
            values['image'] = cloudinary.utils.cloudinary_url(upload_result['public_id'])[0]

    mongo.db.points.find_one_and_update({'_id': ObjectId(id)},
                                        {'$set': values })

    response = flask.make_response(jsonify({'updated': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


@point.route('/point/<id>/visibility', methods=['PUT'])
def updatePointVisibility(id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    is_visible = request.get_json()['visible']
    mongo.db.points.find_one_and_update({'_id': ObjectId(id)},
                                        {'$set': {'visible':is_visible}})

    response = flask.make_response(jsonify({'updated': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


def updatePointsOfCategory(categoryId, newCategoryName):
    ack = mongo.db.points.update_many({'categoryId': categoryId},
                                      {'$set': {'categoryName': newCategoryName}})


def updateVisibilityOfCategory(categoryId, is_visible):
    ack = mongo.db.points.update_many({'categoryId': str(categoryId)},
                                {'$set': {'visible': is_visible}})


@point.route('/point/<id>', methods=['DELETE'])
def deletePoint(id):
    db_response = mongo.db.points.delete_one({'_id': ObjectId(id)})

    response = flask.make_response(jsonify({'deleted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200


def deletePointsOfCategory(categoryId):
    db_response = mongo.db.points.remove({'categoryId': str(categoryId)})
