""" index file for running the API"""
import os
import sys
from flask import jsonify, make_response

from app import app, mongo
from app.model.point import Point
from app.model.category import Category

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

    point1 = Point({'lat': -34.6, 'lng': -58.5}, 'macDonald', 'muchas gordas', "Food", True)
    point2 = Point({'lat': -34.52, 'lng': -58.55}, 'burgerKing', 'muchas gordas', "Food", False)
    point3 = Point({'lat': -34.58319, 'lng': -58.4432}, 'Estadio de football', 'fui de pepa', "Sports", True)
    point4 = Point({'lat': -34.573, 'lng': -58.4548}, 'FutureBar', 'rica, amaaaaargaa', "Night Life", True)

    cat1 = Category("Food", "idk1")
    cat2 = Category("Night Life", "idk2")
    cat3 = Category("Sports", "idk3")

    points.append(point1)
    points.append(point2)
    points.append(point3)
    points.append(point4)

    categories.append(cat1)
    categories.append(cat2)
    categories.append(cat3)

    print("cargando datos de prueba", flush=True)

    with app.app_context():

        mongo.db.points.remove({})
        mongo.db.categories.remove({})

        for point in points:
            mongo.db.points.insert_one(point.__dict__)

        for category in categories:
            mongo.db.categories.insert_one(category.__dict__)

    app.config['DEBUG'] = os.environ.get('ENV') == 'development'
    app.run(host='0.0.0.0', port=int(PORT))
