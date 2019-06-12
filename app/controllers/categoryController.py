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
    updateVisibilityOfCategory, deletePointsOfCategory, updatePointsOfCategory, deletePoints
)


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
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    pointData = request.get_json()
    newCategory = Category( pointData['title'], pointData['icon'])
    mongo.db.categories.insert_one(newCategory.__dict__)
    response = flask.make_response(jsonify({'inserted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


@category.route('/category/<id>', methods=['PUT'])
def updateCategory(id):

    newTitle = request.form['title']
    newIcon = request.form['icon']
    #newIcon = newTitle + str(random.randint(0,1000)) #para que cambie el icono y refrezque
    if request.form['has_file'] == "true":
        files = request.files
        img = files['file']
        if os.environ.get('ENV') == 'development':
            img.save('/usr/src/web/app/static/icons/' + id)
            newIcon =  "http://localhost:" + os.environ.get('PORT') + "/static/icons/" + id

        else:
            upload_result = upload(img, public_id = id)
            newIcon = cloudinary.utils.cloudinary_url(upload_result['public_id'])[0]

    oldCategory = mongo.db.categories.find_one_and_update({'_id': ObjectId(id)},
                                                          {'$set':{'title': newTitle, 'icon':newIcon}} )

    if oldCategory is not None:
        updatePointsOfCategory(id, newTitle)
        response = flask.make_response(jsonify({'updated': True}))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 201
    else:
        response = flask.make_response(jsonify({'updated': False, 'message' : 'Category not found'}))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 404


@category.route('/category/<id>/visibility', methods=['PUT'])
def updateCategoryVisibility(id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    is_visible = request.get_json()['visible']
    oldCategory = mongo.db.categories.find_one_and_update({'_id': ObjectId(id)},
                                                          {'$set': {'visible':is_visible}})
    if oldCategory is not None:
        updateVisibilityOfCategory( oldCategory['_id'], is_visible)
    else:
        pass

    response = flask.make_response(jsonify({'updated': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


@category.route('/category/<id>', methods=['DELETE'])
def deleteCategory(id):
    category = mongo.db.categories.find_one_and_delete({'_id': ObjectId(id)})
    if category is not None:
        deletePointsOfCategory(category['_id'])
    else:
        pass

    response = flask.make_response(jsonify({'deleted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200

@category.route('/category', methods=['DELETE'])
def deleteCategories():
    category = mongo.db.categories.delete({})
    deletePoints()
    response = flask.make_response(jsonify({'deleted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200
