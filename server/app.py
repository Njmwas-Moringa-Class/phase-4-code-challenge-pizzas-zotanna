#!/usr/bin/env python3


from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    return 'Welcome to the Pizza App!'

@app.route('/restaurants')
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict(fields=('id', 'name', 'address')) for restaurant in restaurants]), 200


@app.route('/restaurants/<int:id>')
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return jsonify(restaurant.to_dict(included=['restaurant_pizzas'])), 200
    else:
        return jsonify({'error': 'Restaurant not found'}), 404


@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        return jsonify({'error': 'Restaurant not found'}), 404


@app.route('/pizzas')
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict() for pizza in pizzas]), 200

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    try:
        new_restaurant_pizza = RestaurantPizza(price=data['price'], pizza_id=data['pizza_id'], restaurant_id=data['restaurant_id'])
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        return jsonify(new_restaurant_pizza.to_dict(included=['pizza', 'restaurant'])), 201
    except AssertionError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except KeyError as e:
        db.session.rollback()
        return jsonify({'error': 'Missing key in request data: {}'.format(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while processing your request: {}'.format(e)}), 500


if __name__ == '__main__':
    app.run(port=5555, debug=True)