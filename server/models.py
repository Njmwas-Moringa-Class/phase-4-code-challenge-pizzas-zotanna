

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates


db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant', cascade='all, delete-orphan')

    def to_dict(self, fields=None, included=None):
        data = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
        }
        
        if included:
            if 'restaurant_pizzas' in included:
                data['restaurant_pizzas'] = [rp.to_simple_dict() for rp in self.restaurant_pizzas]
        
        return data

class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
        }

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')

    @validates('price')
    def validate_price(self, key, price):
        if not 1 <= price <= 30:
            raise AssertionError('Price must be between 1 and 30.')
        return price

    def to_dict(self, included=None):
        data = {
            'id': self.id,
            'price': self.price,
            'pizza_id': self.pizza_id,
            'restaurant_id': self.restaurant_id,
        }
        
        if included:
            if 'pizza' in included:
                data['pizza'] = self.pizza.to_dict()
            if 'restaurant' in included:
                data['restaurant'] = self.restaurant.to_dict(fields=('id', 'name'))
        
        return data
    
    def to_simple_dict(self):
        return {
            'id': self.id,
            'price': self.price,
        }