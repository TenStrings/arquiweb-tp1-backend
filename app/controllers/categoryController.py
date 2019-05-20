import flask
from bson import ObjectId
from flask import Blueprint, jsonify, request

from app.model.category import Category
from app.controllers.pointController import updatePointsOfCategory, deletePointsOfCategory

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

    data = request.get_json()

    title = data['title']
    icon = "TODO send fname from frontend"

    newCategory = Category(title, icon)

    mongo.db.points.insert_one(category.__dict__)
    response = flask.make_response(jsonify({'inserted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201

@category.route('/category/<id>', methods=['PUT'])
def updateCategory(id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.get_json()
    newTitle = data['title']
    icon = "TODO send fname from frontend"
    is_visible = data['visible']
    category= Category(newTitle, icon)
    category.visible = is_visible

    matching_categories = mongo.db.find({'_id': ObjectId(id)} )
    is_category = matching_categories.hasNext()
    if is_category:
        oldTitle = matching_categories.next()['title']
        updatePointsOfCategory(oldTitle, newTitle, is_visible)

    ack = mongo.db.categories.update({'_id' : ObjectId(id)}, category.__dict__)

    response = flask.make_response(jsonify({'updated': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


@category.route('/category/<id>', methods=['DELETE'])
def deleteCategory(id):
    matching_categories = mongo.db.find({'_id': ObjectId(id)} )
    is_category = matching_categories.hasNext()
    db_response = mongo.db.categories.delete_one({'_id': ObjectId(id)})
    if was_category:
        categoryName = matching_categories.next()['title']
        deletePointsOfCategory(categoryName)

    response = flask.make_response(jsonify({'deleted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200
