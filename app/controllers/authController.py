import flask
from bson import ObjectId
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)

# from app.model.user import User

auth = Blueprint("auth", __name__, url_prefix='/auth')

# no cambiar el lugar del import por las dependencias circulares
from app import mongo


@auth.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    return jsonify(succeded=True), 200  #ALTO hack

# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@auth.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'admin' or password != 'admin':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@auth.route('/protected', methods=['GET'])
@jwt_required
def protected():
    claims = get_jwt_claims()
    return jsonify({
        'username': claims['username'],
        'admin': claims['admin']
    }), 200
