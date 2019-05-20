import flask
from bson import ObjectId
from flask import Blueprint, jsonify, request
from pymongo import ReturnDocument
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

    mongo.db.categories.insert_one(category.__dict__)
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
    updatedCategory= Category(newTitle, icon)
    updatedCategory.visible = is_visible
    oldCategory = mongo.db.categories.find_one_and_update({'_id': ObjectId(id)},
                                                          {'$set':updatedCategory.__dict__} )
    for c in mongo.db.categories.find({'_id': ObjectId(id)}):
        print(c, flush=True)

    if oldCategory is not None:
        oldTitle = oldCategory['title']
        updatePointsOfCategory(oldTitle, newTitle, is_visible)
    else:
        pass

    response = flask.make_response(jsonify({'updated': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


@category.route('/category/<id>', methods=['DELETE'])
def deleteCategory(id):
    category = mongo.db.categories.find_one_and_delete( {'_id': ObjectId(id)} )
    if category is not None:
        categoryName = category['title']
        deletePointsOfCategory(categoryName)
    else: #doesn't have a hasNext()
        pass

    response = flask.make_response(jsonify({'deleted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200
