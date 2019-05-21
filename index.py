""" index file for running the API"""
import os
import sys
from flask import jsonify, make_response

from app import app, mongo
from app.model.point import Point
from app.model.category import Category
from app.model.suggestions import Suggestion

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'app'))

""" Port variable to run the server on """
PORT = os.environ.get('PORT')


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    points = []
    categories = []
    suggestions = []

    point1 = Point({'lat': -34.6, 'lng': -58.5}, 'Rodicio', 'Comida rica', "Rodicio", "Restaurantes")
    point2 = Point({'lat': -34.52, 'lng': -58.55}, 'PF Changs', 'Comida asiática', "PF Changs", "Restaurantes")
    point3 = Point({'lat': -30.52, 'lng': -58.55}, 'Sakiko', 'Comida japonesa', "Sakiko", "Restaurantes")
    point4 = Point({'lat': -34.56, 'lng': -58.4432}, 'Club Amigos', 'Tenis, Football y más', "Club Amigos", "Deportes")
    point5 = Point({'lat': -34.573, 'lng': -58.4548}, 'Future Bar', 'Cerveza artesanal', "Future Bar", "Bares")

    cat1 = Category("Restaurantes", "Restaurantes")
    cat2 = Category("Bares", "Bares")
    cat3 = Category("Deportes", "Deportes")

    sug1 = Suggestion("Colegios", "Colegios")
    sug2 = Category("Entretenimiento", "Entretenimiento")

    points.append(point1)
    points.append(point2)
    points.append(point3)
    points.append(point4)
    points.append(point5)

    categories.append(cat1)
    categories.append(cat2)
    categories.append(cat3)

    suggestions.append(sug1)
    suggestions.append(sug2)

    print("Cargando datos de prueba", flush=True)

    with app.app_context():

        mongo.db.points.remove({})
        mongo.db.categories.remove({})
        mongo.db.suggestions.remove({})

        for point in points:
            mongo.db.points.insert_one(point.__dict__)

        for category in categories:
            mongo.db.categories.insert_one(category.__dict__)

        for sug in suggestions:
            mongo.db.suggestions.insert_one(sug.__dict__)


    app.debug = os.environ.get('ENV') == 'development'
    app.run(host='0.0.0.0', port=int(PORT))
