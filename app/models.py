from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

orders_meals = db.Table('orders_meals',
                        db.Column("order_id", db.Integer, db.ForeignKey("order.id")),
                        db.Column("meal_id", db.Integer, db.ForeignKey("meal.id")))

class Category(db.Model):
    #__tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    meals = db.relationship('Meal', back_populates='category')

class Meal(db.Model):
    #__tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    price = db.Column(db.Integer)
    description = db.Column(db.String)
    picture = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='meals')
    orders = db.relationship('Order', secondary=orders_meals, back_populates='meals')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
    is_admin = db.Column(db.Boolean)
    orders = db.relationship('Order', back_populates='user')

    @property
    def password(self):
        raise Exception('no')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Integer)
    status = db.Column(db.String)
    mail = db.Column(db.String)
    phone = db.Column(db.Integer)
    address = db.Column(db.String)
    user = db.relationship('User', back_populates='orders')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    meals = db.relationship('Meal', secondary=orders_meals, back_populates='orders')

