import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from app.utils.jsonEncoder import JSONEncoder
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = os.environ.get('DB')
app.json_encoder = JSONEncoder
mongo = PyMongo(app)

from app.controllers.pointController import point
from app.controllers.categoryController import category
from app.controllers.suggestionController import suggestion
from app.controllers.authController import auth

app.register_blueprint(point)
app.register_blueprint(category)
app.register_blueprint(suggestion)
app.register_blueprint(auth)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
#Porque me da paja handlear este caso
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)

# Using the user_claims_loader, we can specify a method that will be
# called when creating access tokens, and add these claims to the said
# token. This method is passed the identity of who the token is being
# created for, and must return data that is json serializable
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'username': identity,
        'admin': True
    }
