from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime

db = SQLAlchemy()

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))) 

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement = True,primary_key = True)
    username = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(100), unique = False)
    password = db.Column(db.String(100), nullable = False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique = True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),nullable = False)
    is_approved = db.Column(db.Boolean(), default = False)
    items = db.relationship('Item', backref = 'items',cascade = "delete, merge, save-update")

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),nullable = False)
    stock = db.Column(db.Integer,nullable = False)
    sold = db.Column(db.Integer,default = 0)
    manufactured_date = date_added = db.Column(db.DateTime)
    expiry_date = date_added = db.Column(db.DateTime)
    rate = db.Column(db.Integer,nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable = False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),nullable = False)
    rate = db.Column(db.Integer,nullable = False)
    quantity = db.Column(db.Integer,nullable = False)
    amount = db.Column(db.Integer,nullable = False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'),nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
    is_sent = db.Column(db.Boolean(), default = False)


class Adminreq(db.Model):
    __tablename__ = 'adminreq'
    id = db.Column(db.Integer, autoincrement = True,primary_key = True)
    username = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(100), unique = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
    is_approved = db.Column(db.Boolean(), default = False)



