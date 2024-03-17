#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# api = Api(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# @app.route('/restaurants')
# def restaurants():
#     restaurants = []
#     for restaurant in Restaurant.query.all():
#         restaurant_dict = restaurant.to_dict()
#         restaurants.append(restaurant_dict)

#     response = make_response(
#         restaurants,
#         200
#     )

#     return response




@app.route('/restaurants')
def restaurants():
    restaurants_list = []

    for restaurant in Restaurant.query.all():
        restaurant_dict = {
            "address": restaurant.address,
            "id": restaurant.id,
            "name": restaurant.name,
        }

        restaurants_list.append(restaurant_dict)
    response = make_response(
        jsonify(restaurants_list), 200
    )

    response.headers["Context-Type"] = "application/json"

    return response


# code without using to_dict()
# @app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
# def restaurant_by_id(id):

#     if request.method =='GET':
#         restaurant = Restaurant.query.filter(Restaurant.id == id).first()

#         if restaurant is None :

#             return make_response(
#             jsonify({'error': 'Restaurant not found'}),
#             404  )
        
#         restaurant_pizza = RestaurantPizza.query.filter(RestaurantPizza.pizza_id == restaurant.id).first()

#         pizza = Pizza.query.filter(Pizza.id == id).first()

#         restaurant_dict = {
#             "address": restaurant.address,
#             "id": restaurant.id,
#             "name": restaurant.name,
#             "restaurant_pizzas":[{
#                 "id": restaurant_pizza.id,  
#                 "pizza": { "id": pizza.id, "name": pizza.name, "ingredients": pizza.ingredients},
#                 "pizza_id": restaurant_pizza.pizza_id, 
#                 "price": restaurant_pizza.price,
#                 "restaurant_id": restaurant_pizza.restaurant_id
#             }],
                
#         }

#         response = make_response(
#             jsonify(restaurant_dict),
#             200
#         )

#         response.headers["Context-Type"] = "application/json"

        
#         return response
    
#     elif request.method =='DELETE':
        
#         restaurant_pizza = RestaurantPizza.query.filter_by(id=id).first()
#         restaurant = Restaurant.query.filter_by(id=id).first()
        
#         if restaurant is None :

#             return make_response(
#             jsonify({'error': 'Restaurant not found'}),
#             404  )
        
#         db.session.delete(restaurant_pizza)
#         db.session.commit()


#         db.session.delete(restaurant)
#         db.session.commit()

#         response_body={
#             "delete_successful": True,
#             "message": "Restaurant deleted",
#         }

#         response = make_response(
#             jsonify(response_body),
#             200
#         )

#         return response

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()

    if restaurant is None :

            return make_response(
            jsonify({'error': 'Restaurant not found'}),
            404  )

    if request.method =='GET':
        restaurant_dict=restaurant.to_dict()

        response = make_response(
            jsonify(restaurant_dict),
            200
        )

        return response
    
    elif request.method == 'DELETE':
        # restaurant_pizza = RestaurantPizza.query.filter_by(id=id).first()
        restaurant = Restaurant.query.filter_by(id=id).first()
        
        if restaurant is None :

            return make_response(
            jsonify({'error': 'Restaurant not found'}),
            404  )
        
        # db.session.delete(restaurant_pizza)
        # db.session.commit()


        db.session.delete(restaurant)
        db.session.commit()

        response_body={
            "delete_successful": True,
            "message": "Restaurant deleted",
        }

        response = make_response(
            jsonify(response_body),
            204
        )

        return response
    

@app.route('/pizzas')
def pizzas():
    pizzas_list = []

    for pizza in Pizza.query.all():
        pizza_dict = {
            "id": pizza.id,
            "ingredients": pizza.ingredients,
            "name": pizza.name,
        }

        pizzas_list.append(pizza_dict)
    response = make_response(
        jsonify(pizzas_list), 200
    )

    response.headers["Context-Type"] = "application/json"

    return response


@app.route('/restaurant_pizzas', methods=['POST'])
def restaurant_pizza():
    if request.method == 'POST':
        try:
            new_restaurantpizza = RestaurantPizza(
                price = request.get_json().get("price"),
                pizza_id = request.get_json().get("pizza_id"),
                restaurant_id = request.get_json().get("restaurant_id"),
            )

            db.session.add(new_restaurantpizza)
            db.session.commit()

            restaurantpizza_dict = new_restaurantpizza.to_dict()

            response = make_response(
                jsonify(restaurantpizza_dict),
                201
            )

            return response

        except ValueError as exception_message:
            return jsonify(errors=[str(exception_message)]), 400  
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
