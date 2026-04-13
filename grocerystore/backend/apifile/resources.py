from flask_restful import Resource, marshal_with,fields, reqparse
from model import User as user_model
from model import Category as category_model
from model import Item as item_model
from model import Cart as cart_model
from model import db,Role
from datetime import datetime
from sec import user_datastore
import string
import random
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify,request
import requests
import urllib.request
from tasks import download
from flask_security import auth_required,roles_required, current_user, roles_accepted
from model import Adminreq as adminreq_model
from instances import cache



user_resource = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "password": fields.String,
    "active": fields.Boolean,
    "fs_uniquifier": fields.String,
    "roles" : fields.String,
}
req_resource = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "user_id": fields.Integer,
    "is_approved": fields.Boolean,
}
item_resource = {
    "id": fields.Integer,
    "name": fields.String,
    "stock": fields.Integer,
    "sold": fields.Integer,
    "manufactured_date": fields.DateTime,
    "expiry_date": fields.DateTime,
    "rate": fields.Integer,
    "category_id": fields.Integer,
    "date_added" : fields.DateTime,
}
category_resource = {
    "id": fields.Integer,
    "name": fields.String,
    "is_approved": fields.Boolean,
    "items": fields.String,
}
cart_resource = {
    "id": fields.Integer,
    "name": fields.String,
    "rate": fields.Integer,
    "quantity": fields.Integer,
    "amount": fields.Integer,
    "item_id": fields.Integer,
    "user_id": fields.Integer,
}


user_put = reqparse.RequestParser()
user_put.add_argument("name", type=str)
user_put.add_argument("email", type=str , required=True)
user_put.add_argument("password", type=str , required=True)


item_put = reqparse.RequestParser()
item_put.add_argument('name',type=str)
item_put.add_argument('stock',type=int)
item_put.add_argument('manufactured_date',type=str)
item_put.add_argument('expiry_date',type=str)
item_put.add_argument('rate',type=int)
item_put.add_argument('category_id',type=int)

category_put = reqparse.RequestParser()
category_put.add_argument('name', type=str)

cart_put = reqparse.RequestParser()
cart_put.add_argument('name', type=str)
cart_put.add_argument('rate', type=int)
cart_put.add_argument('quantity', type=int)
cart_put.add_argument('item_id', type=int)

class User(Resource):
    @marshal_with(user_resource)
    def get(self):
        users = user_model.query.all()
        return users
    def post(self):
        x = user_put.parse_args()
        if not user_datastore.find_user(email=x['email']):
            user_datastore.create_user(email=x['email'], password=generate_password_hash(x['password']),roles=["User"])
            db.session.commit()
            #generate_password_hash(x['password'])
class UserTask(Resource):
    @marshal_with(user_resource)
    def get(self,id):
        user = user_model.query.get(id)
        return user
    def delete(self,id):
        user = user_model.query.get(id)
        db.session.delete(user)
        db.session.commit()

class Item(Resource):
    @marshal_with(item_resource)
    @auth_required('token')
    def get(self):
        items = item_model.query.order_by(item_model.date_added.desc()).all()
        return items
    @auth_required('token')
    @roles_accepted('Admin','StoreManager')
    def post(self):
        x = item_put.parse_args()
        item = item_model(name = x['name'],stock = x['stock'] ,manufactured_date=datetime.strptime(x['manufactured_date'],"%Y-%m-%d"),expiry_date =datetime.strptime(x['expiry_date'],"%Y-%m-%d"), rate =x['rate'],category_id =x['category_id'])
        db.session.add(item)
        db.session.commit()

class ItemTask(Resource):
    @marshal_with(item_resource)
    @auth_required('token')
    def get(self,id):
        items = item_model.query.get(id)
        return items
    @auth_required('token')
    def put(self,id):
        x = item_put.parse_args()
        item = item_model.query.get(id)
        item.name = x['name']
        item.stock= x['stock']
        try:
            item.manufactured_date=datetime.strptime(x['manufactured_date'],"%Y-%m-%d")
        except:
            item.manufactured_date= item.manufactured_date
        try:
            item.expiry_date=datetime.strptime(x['expiry_date'],"%Y-%m-%d")
        except:
            item.expiry_date=item.expiry_date
        item.rate =x['rate']
        db.session.commit()
    @auth_required('token')
    def delete(self,id):
        item = item_model.query.get(id)
        db.session.delete(item)
        db.session.commit()
    


class Category(Resource):
    @marshal_with(category_resource)
    @auth_required('token')
    #@cache.cached(timeout=30)
    def get(self):
        category= category_model.query.all()
        return category
    @auth_required('token')
    @roles_accepted('Admin', 'StoreManager')
    def post(self):
        x = category_put.parse_args()
        if current_user.email == 'Admin@gmail.com':
            category = category_model(name = x['name'], is_approved=True)
        else:
            category = category_model(name = x['name'])
        db.session.add(category)
        db.session.commit()
class CategoryTask(Resource):
    @marshal_with(category_resource)
    def get(self,id):
        category = category_model.query.get(id)
        return category
    def put(self,id):
        x = category_put.parse_args()
        category = category_model.query.get(id)
        category.name = x['name']
        db.session.commit()
    @auth_required('token')
    def delete(self,id):
        category = category_model.query.get(id)
        db.session.delete(category)
        db.session.commit()

class Cart(Resource):
    @marshal_with(cart_resource)
    def get(self):
        cart= cart_model.query.all()
        return cart
    @auth_required('token')
    def post(self):
        x = cart_put.parse_args()
        item = item_model.query.filter_by(id=x["item_id"]).first()
        if((item.sold+x["quantity"]) > item.stock):
            data = { "Message" : "NO STOCK",}
            return jsonify(data)
        else:
            item.sold = item.sold+x["quantity"]
            cart = cart_model(name = x['name'], rate = x["rate"], quantity=x['quantity'],amount=(x['rate']*x["quantity"]), item_id = x["item_id"], user_id = current_user.id)
            db.session.add(cart)
            db.session.commit()
            data = { "Message" : "ERROR",}
            return jsonify(data)
class CartTask(Resource):
    @auth_required('token')
    @marshal_with(cart_resource)
    def get(self):
        cart= cart_model.query.filter_by(user_id = current_user.id).all()
        return cart



class Adminreq(Resource):
    @auth_required('token')
    @marshal_with(req_resource)
    def get(self):
        adminreq = adminreq_model.query.all()
        return adminreq

class Infodownload(Resource):
    @auth_required('token')
    def get(self):
        res = download.delay()
        data = { "Message" : "Download has started",
                "task_id": res.id}
        return jsonify(data)
    
search_cat = reqparse.RequestParser()
search_cat.add_argument("category", type=str,required=False)

search_item = reqparse.RequestParser()
search_item.add_argument("item", type=str , required=False)
search_item.add_argument("price", type=int , required=False)
search_item.add_argument("manufactured_date", type=str , required=False)

searchcat_resource = {
    'category':{
        "id": fields.Integer,
        "name": fields.String,
        "is_approved": fields.Boolean,
        "items": fields.String,
    },
    'item':{
        "id": fields.Integer,
        "name": fields.String,
        "stock": fields.Integer,
        "sold": fields.Integer,
        "manufactured_date": fields.DateTime,
        "expiry_date": fields.DateTime,
        "rate": fields.Integer,
        "category_id": fields.Integer,
        "date_added" : fields.DateTime,
    }

    
}
class SearchCat(Resource):
    @marshal_with(category_resource)
    def post(self):
        s = search_cat.parse_args()
        category_name = s['category']
        if category_name:
            cat = category_model.query.filter(category_model.name.like('%'+category_name+'%')).all()
            return cat
        else:
            all= category_model.query.all()
            return all
class SearchItem(Resource):
    @marshal_with(item_resource)
    def post(self):
        s = search_item.parse_args()
        a = item_model.query.all()
        item_name =  s['item']
        item_price = s['price']
        manudate = s['manufactured_date']
        allitems = item_model.query.order_by(item_model.date_added.desc())
        if item_name:
            allitems = allitems.filter(item_model.name.like('%'+ item_name+"%"))
        if item_price:
            allitems = allitems.filter_by(rate=item_price)   
        if manudate:
            allitems = allitems.filter_by(manufactured_date=datetime.strptime(manudate,"%Y-%m-%d"))               
        return allitems.all()

