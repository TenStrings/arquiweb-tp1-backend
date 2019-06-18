import flask
import random
from bson import ObjectId
from flask import Blueprint, jsonify, request
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import os

from app.model.point import Point
from app.controllers.externProviderController import get_extern_points
point = Blueprint("point", __name__)

# no cambiar el lugar del import por las dependencias circulares
from app import mongo


@point.route('/point', methods=['GET'])
def get_points():
    intern_points = [point for point in mongo.db.points.find({})]
    response = flask.make_response(jsonify(intern_points))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@point.route('/point/extern', methods=['GET'])
def extern_points():
    extern_points = get_extern_points()
    response = flask.make_response(jsonify(extern_points))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@point.route('/point', methods=['POST'])
def add_point():

    data = request.form
    image = ""
    if data['has_file']  == "true":
        files = request.files
        img = files['file']
        if os.environ.get('ENV') == 'development':
            fake_id = str(random.randint(0,10000))
            img.save('/usr/src/web/app/static/pointImages/' + fake_id)
            image =  "http://localhost:" + os.environ.get('PORT') + "/static/pointImages/" + fake_id
        else:
            upload_result = upload(img)
            image = cloudinary.utils.cloudinary_url(upload_result['public_id'])[0]

    new_point = Point({'lat':data['positionLat'], 'lng':data['positionLng'] },
                     data['name'],
                     data['description'],
                     image,
                     data['categoryId'],
                     data['categoryName'])

    mongo.db.points.insert_one(new_point.__dict__)

    response = flask.make_response(jsonify({'inserted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201

@point.route('/point/<id>', methods=['PUT'])
def update_point(id):

    data = request.form
    values = {}
    values['name'] = data['name']
    values['description'] = data['description']
    values['image'] = data['image']
    values['categoryId'] = ObjectId(data['categoryId'])
    values['categoryName'] = data['categoryName']
    if data['has_file'] == "true":
        files = request.files
        img = files['file']

        if os.environ.get('ENV') == 'development':
            fake_id = str(random.randint(0,10000))
            img.save('/usr/src/web/app/static/pointImages/' + fake_id)
            values['image'] =  "http://localhost:" + os.environ.get('PORT') + "/static/pointImages/" + fake_id
        else:
            upload_result = upload(img, public_id = id)
            values['image'] = cloudinary.utils.cloudinary_url(upload_result['public_id'])[0]

    mongo.db.points.find_one_and_update({'_id': ObjectId(id)},
                                        {'$set': values })

    response = flask.make_response(jsonify({'updated': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


@point.route('/point/<id>/visibility', methods=['PUT'])
def update_point_visibility(id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    is_visible = request.get_json()['visible']
    mongo.db.points.find_one_and_update({'_id': ObjectId(id)},
                                        {'$set': {'visible':is_visible}})

    response = flask.make_response(jsonify({'updated': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


def update_points_of_category(id, new_title):
    ack = mongo.db.points.update_many({'categoryId': id},
                                      {'$set': {'categoryName': new_title}})


def update_visibility_of_category(id, is_visible):
    ack = mongo.db.points.update_many({'categoryId': id},
                                {'$set': {'visible': is_visible}})


@point.route('/point/<id>', methods=['DELETE'])
def delete_point(id):
    db_response = mongo.db.points.delete_one({'_id': ObjectId(id)})

    response = flask.make_response(jsonify({'deleted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200

@point.route('/point', methods=['DELETE'])
def delete_points():
    db_response = mongo.db.points.delete_many({})
    response = flask.make_response(jsonify({'deleted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200

def delete_points_of_category(id):
    db_response = mongo.db.points.delete_many({'categoryId': id})
