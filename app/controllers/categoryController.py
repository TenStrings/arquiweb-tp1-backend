import flask
import random
from bson import ObjectId
from flask import Blueprint, jsonify, request
from app.model.category import Category
from app.controllers.pointController import updatePointsOfCategory, deletePointsOfCategory
from app.controllers.pointController import updatePointsOfCategoryWithTitle


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
    icon = data['icon']

    newCategory = Category(title, icon)
    mongo.db.categories.insert_one(newCategory.__dict__)
    response = flask.make_response(jsonify({'inserted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


@category.route('/category/<id>', methods=['PUT'])
def updateCategory(id):

    data = request.files

    img = data['file']
    newTitle = request.form['title']
    newIcon = newTitle + str(random.randint(0,1000)) #para que cambie el icono y refrezque

    updatedCategory= Category(newTitle, newTitle)

    oldCategory = mongo.db.categories.find_one_and_update({'_id': ObjectId(id)},
                                                          {'$set':{'title': newTitle, 'icon':newIcon}} )

    if oldCategory is not None:
        oldTitle = oldCategory['title']
        updatePointsOfCategoryWithTitle(oldTitle, newTitle)

        try:
            img.save('/usr/src/web/app/static/icons/' + newIcon)
        except Exception as e:
            print(e, flush=True)

        response = flask.make_response(jsonify({'updated': True}))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 201
    else:
        response = flask.make_response(jsonify({'updated': False, 'message' : 'category not found'}))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 404


@category.route('/category/<id>/visibility', methods=['PUT'])
def updateCategoryVisibility(id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.get_json()
    newTitle = data['title']
    icon = data['icon']
    is_visible = data['visible']
    updatedCategory = Category(newTitle, icon)
    updatedCategory.visible = is_visible
    oldCategory = mongo.db.categories.find_one_and_update({'_id': ObjectId(id)},
                                                          {'$set': updatedCategory.__dict__})
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
    category = mongo.db.categories.find_one_and_delete({'_id': ObjectId(id)})
    if category is not None:
        categoryName = category['title']
        deletePointsOfCategory(categoryName)
    else:  # doesn't have a hasNext()
        pass

    response = flask.make_response(jsonify({'deleted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200
