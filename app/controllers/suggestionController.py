import flask
import random
from bson import ObjectId
from flask import Blueprint, jsonify, request
import os

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
    title = request.form['title']
    icon = ""
    alreadySuggested = mongo.db.suggestions.find_one({'title' : title}) is not None
    alreadyCategory = mongo.db.categories.find_one({'title' : title}) is not None
    if not (alreadyCategory or alreadySuggested):
        if request.form['has_file']  == "true":
            files = request.files
            img = files['file']
            if os.environ.get('ENV') == 'development':
                fake_id = str(random.randint(0,10000))
                img.save('/usr/src/web/app/static/icons/' + fake_id)
                icon = "http://localhost:" + os.environ.get('PORT') + "/static/icons/" + fake_id
            else:
                upload_result = upload(img)
                icon = cloudinary.utils.cloudinary_url(upload_result['public_id'])[0]

        mongo.db.suggestions.insert_one( dict( title = title, icon = icon) )
        response = flask.make_response(jsonify({'inserted': True}))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 201
    else:
        response = flask.make_response(jsonify({
            'inserted': False,
            'error_msg': 'There is already a suggestion or category with that name'
        }))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 409


@suggestion.route('/suggested_category/<id>', methods=['DELETE'])
def deleteSuggestion(id):
    db_response = mongo.db.suggestions.delete_one({'_id': ObjectId(id)})

    response = flask.make_response(jsonify({'deleted': True}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response, 200
