import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from app.utils.jsonEncoder import JSONEncoder


app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = os.environ.get('DB')
app.json_encoder = JSONEncoder
mongo = PyMongo(app)

from app.controllers.pointController import point
from app.controllers.categoryController import category

app.register_blueprint(point)
app.register_blueprint(category)
