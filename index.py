""" index file for running the API"""
import os
import sys
from flask import jsonify, make_response

from app import app, mongo
from app.model.point import Point
from app.model.category import Category
from app.model.suggestion import Suggestion

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'app'))

""" Port variable to run the server on """
PORT = os.environ.get('PORT')

@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)

def init_database(app):
    icons_dir = "http://localhost:" + os.environ.get('PORT') + "/static/icons"
    images_dir = "http://localhost:" + os.environ.get('PORT') + "/static/pointImages"
    cat_id = dict()
    with app.app_context():
        mongo.db.points.remove({})
        mongo.db.categories.remove({})
        mongo.db.suggestions.remove({})

    categories = []
    categories.append(Category("Restaurantes", icons_dir + "/Restaurantes"))
    categories.append(Category("Bares", icons_dir + "/Bares"))
    categories.append(Category("Deportes", icons_dir +"/Deportes"))
    with app.app_context():
        for category in categories:
            mongo.db.categories.insert_one(category.__dict__)
            cat_id[category.title] = mongo.db.categories.find_one({'title':category.title})['_id']

    points = []
    points.append(Point({'lat': -34.6, 'lng': -58.5}, 'Rodicio', 'Comida rica', images_dir + "/9170", cat_id['Restaurantes'],"Restaurantes"))
    points.append(Point({'lat': -34.52, 'lng': -58.55}, 'PF Changs', 'Comida asiática', images_dir + "/9170", cat_id['Restaurantes'], "Restaurantes"))
    points.append(Point({'lat':-34.55, 'lng': -58.52}, 'Sakiko', 'Comida japonesa', images_dir + "/9170", cat_id['Restaurantes'],"Restaurantes"))
    points.append(Point({'lat': -34.56, 'lng': -58.4432}, 'Club Amigos', 'Tenis, Football y más', images_dir + "/8888", cat_id['Deportes'], "Deportes"))
    points.append(Point({'lat': -34.573, 'lng': -58.4548}, 'Future Bar', 'Cerveza artesanal', images_dir + "/5888", cat_id['Bares'], "Bares"))

    suggestions = []
    suggestions.append(Suggestion("Colegios", "SinImagen"))
    suggestions.append(Suggestion("Entretenimiento", "SinImagen"))

    print("Cargando datos de prueba", flush=True)
    with app.app_context():
        for point in points:
            mongo.db.points.insert_one(point.__dict__)
        for sug in suggestions:
            mongo.db.suggestions.insert_one(sug.__dict__)

if __name__ == '__main__':

    app.debug = os.environ.get('ENV') == 'development'
    if app.debug:
        init_database(app)
    app.run(host='0.0.0.0', port=int(PORT))
