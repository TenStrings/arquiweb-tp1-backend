import flask
from bson import ObjectId
from flask import Blueprint, jsonify, request

from app.model.category import Category

suggestion = Blueprint("suggestion", __name__)

# no cambiar el lugar del import por las dependencias circulares
from app import mongo

@suggestion.route('/suggested_category', methods=['GET'])
def getAllSuggestions():
    allSuggestions = mongo.db.suggestions.find({})
    result = [title for title in allSuggestions]

    response = flask.make_response(jsonify(result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@suggestion.route('/suggested_category', methods=['POST'])
def addSuggestion():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()

    title = data['title']
    icon = "todo send from front end"

    alreadySuggested = mongo.db.suggestions.find_one({'title' : title}) is not None
    alreadyCategory = mongo.db.categories.find_one({'title' : title}) is not None

    if not (alreadyCategory or alreadySuggested):
        mongo.db.suggestions.insert_one( dict( title = title, icon = icon) )

    response = flask.make_response(jsonify({'inserted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 201


@suggestion.route('/suggested_category/<id>', methods=['DELETE'])
def deleteSuggestion(id):
    db_response = mongo.db.suggestions.delete_one({'_id': ObjectId(id)})

    response = flask.make_response(jsonify({'deleted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200
