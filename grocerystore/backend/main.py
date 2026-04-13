from flask import Flask,jsonify,request,send_file
from os import path
from model import db,User,Role
from config import DevelopmentConfig
from flask_security import Security
from sec import user_datastore
from apifile import api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from worker import celery_init_app
import flask_excel as excel
from model import Item as item_model
from model import Category as category_model
from model import User as user_model
from model import Adminreq as adminreq_model
from celery.result import AsyncResult
from celery.schedules import crontab
from tasks import monthly_reminder,daily_reminder
from flask_security import auth_required,roles_required, current_user, roles_accepted

from instances import cache


app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app) 
app.config.from_object(DevelopmentConfig)
db.init_app(app)
api.init_app(app)
app.security = Security(app, user_datastore)
excel.init_excel(app)
cache.init_app(app)

celery_app=celery_init_app(app)

@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=17, minute=30,day_of_month=1),
        monthly_reminder.s('MONTHLY PURCHASE REPORT'),
    )
    sender.add_periodic_task(
        crontab(hour=17, minute=30),
        daily_reminder.s('DAILY REMINDER'),
    )


@app.route('/user-login',methods = ['POST'])
def user_login():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"message": "email not provided"}),400
    user = user_datastore.find_user(email=email)
    if not user:
        return jsonify({"message": "user not found"}),400
    if check_password_hash(user.password, data.get('password')):
        #userroles =user.roles[0].name'
        userroles=[]
        for role in user.roles:
            userroles.append(role.name)
        #role_names={'roles': userroles}

        return jsonify({"token" : user.get_auth_token(),"email": user.email,"role": userroles})
    else:
        return jsonify({"message": "wrong password"}),400
    
@app.route('/product-csv', methods =['GET'])
@auth_required('token')
def download_csv():
    products_res = item_model.query.all()
    csv_output = excel.make_response_from_query_sets(products_res,["name","stock","rate","date_added"],"csv", file_name="product.csv")
    return csv_output

@app.route('/category/<int:id>/approve', methods =['GET'])
@auth_required('token')
def approve(id):
    category = category_model.query.filter_by(id=id).first()
    if not category:
        return jsonify({"message":"resource not found"}),404
    category.is_approved = True
    db.session.commit()
    return jsonify({"message": "Category Approved"})

@app.route('/apply', methods=['GET'])
@auth_required('token')
def apply():
    user = current_user
    if not adminreq_model.query.filter_by(email = user.email).first():
        u = adminreq_model(email = user.email,user_id = user.id)
        db.session.add(u)
        db.session.commit()
        return jsonify({"message": "Applied for store manager"})
    else:
        return jsonify({"message": "already applied"})

@app.route('/user/<int:id>/approve', methods =['GET'])
@auth_required('token')
@roles_required('Admin')
def approvesm(id):
    sm = adminreq_model.query.filter_by(user_id=id).first()
    if not sm:
        return jsonify({"message":"request not found"}),404
    user = user_model.query.filter_by(email = sm.email).first()
    user_datastore.add_role_to_user(user, 'StoreManager')
    sm.is_approved = True
    db.session.commit()
    return jsonify({"message": "Store manager Approved"})

@app.route('/get-csv/<task_id>', methods=["GET"])
def get_csv(task_id):
    res = AsyncResult(task_id)
    if res.ready():
        filename = res.result
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"message":"download not complete"}),404






def create_database(app):
    if not path.exists('../instance/store.db'):
        with app.app_context():
            db.create_all()
            if not user_datastore.find_role('Admin'):
                user_datastore.create_role(name = 'Admin', description= 'Admin role')
                db.session.commit()
            if not user_datastore.find_role('User'):
                user_datastore.create_role(name = 'User', description= 'User role')
                db.session.commit()
            if not user_datastore.find_role('StoreManager'):
                user_datastore.create_role(name = 'StoreManager', description= 'Store Manager role')
                db.session.commit()
            if not user_datastore.find_user(email = "Admin@gmail.com"):
                user_datastore.create_user(email='Admin@gmail.com', password=generate_password_hash("Admin123"),roles=["Admin"])
                db.session.commit()
                #admin= User.query.filter_by(email='Admin@gmail.com').first()
                #role = Role.query.filter_by(name='Admin').first()
                #user_datastore.add_role_to_user(admin, role)
                #db.session.commit()
                

create_database(app)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')