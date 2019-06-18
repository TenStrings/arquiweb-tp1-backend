import flask
import random
import os
from bson import ObjectId
from flask import Blueprint, jsonify, request
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from app.model.category import Category
from app.controllers.pointController import (
    update_points_of_category,
    update_visibility_of_category,
    delete_points_of_category,
    delete_points
)
from app.controllers.externProviderController import get_extern_categories

category = Blueprint("category", __name__)

# no cambiar el lugar del import por las dependencias circulares
from app import mongo

@category.route('/category', methods=['GET'])
def get_categories():
    intern_categories = [cat for cat in mongo.db.categories.find({})]
    extern_categories = get_extern_categories()

    #TODO unify categories with the same title
    categories = intern_categories + extern_categories

    response = flask.make_response(jsonify(categories))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@category.route('/category', methods=['POST'])
def add_category():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    new_category = Category( data['title'], data['icon'])
    mongo.db.categories.insert_one(new_category.__dict__)
    response = flask.make_response(jsonify({'inserted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


@category.route('/category/<id>', methods=['PUT'])
def update_category(id):
    category_id = ObjectId(id)
    new_title = request.form['title']
    new_icon = request.form['icon']
    #new_icon = new_title + str(random.randint(0,1000)) #para que cambie el icono y refrezque
    if request.form['has_file'] == "true":
        files = request.files
        img = files['file']
        if os.environ.get('ENV') == 'development':
            fake_id = str(random.randint(0,10000))
            img.save('/usr/src/web/app/static/icons/' + fake_id)
            new_icon =  "http://localhost:" + os.environ.get('PORT') + "/static/icons/" + fake_id

        else:
            upload_result = upload(img, public_id = id)
            new_icon = cloudinary.utils.cloudinary_url(upload_result['public_id'])[0]

    old_category = mongo.db.categories.find_one_and_update({'_id': category_id},
                                                           {'$set':{'title': new_title,
                                                                    'icon':new_icon}} )
    if old_category is not None:
        update_points_of_category(category_id, new_title)
        response = flask.make_response(jsonify({'updated': True}))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 201
    else:
        response = flask.make_response(jsonify({'updated': False,
                                                'message' : 'Category not found'}))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 404


@category.route('/category/<id>/visibility', methods=['PUT'])
def update_category_visibility(id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    category_id = ObjectId(id)
    is_visible = request.get_json()['visible']
    old_category = mongo.db.categories.find_one_and_update({'_id': category_id},
                                                           {'$set': {'visible':is_visible}})
    if old_category is not None:
        update_visibility_of_category(category_id, is_visible)
    else:
        pass

    response = flask.make_response(jsonify({'updated': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


@category.route('/category/<id>', methods=['DELETE'])
def delete_category(id):
    category_id = ObjectId(id)
    category = mongo.db.categories.find_one_and_delete({'_id': category_id})
    if category is not None:
        delete_points_of_category(category_id)
    else:
        pass

    response = flask.make_response(jsonify({'deleted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200

@category.route('/category', methods=['DELETE'])
def delete_categories():
    category = mongo.db.categories.delete({})
    delete_points()
    response = flask.make_response(jsonify({'deleted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200

@category.route('/category/extern/<abs_id>', methods=['POST'])
def hide_extern_category(abs_id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    mongo.db.hidden_extern_categories.insert_one({'abs_id': abs_id,
                                                  'title':request.get_json()['title']})
    response = flask.make_response(jsonify({'hidden': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


@category.route('/category/extern/<abs_id>', methods=['DELETE'])
def whiten_extern_category(abs_id):
    mongo.db.hidden_extern_categories.find_one_and_delete({'abs_id': abs_id})
    response = flask.make_response(jsonify({'deleted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201

@category.route('/category/extern/hidden', methods=['GET'])
def get_hidden_extern_categories():
    hidden_categories = [cat for cat in mongo.db.hidden_extern_categories.find({})]

    response = flask.make_response(jsonify(hidden_categories))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
