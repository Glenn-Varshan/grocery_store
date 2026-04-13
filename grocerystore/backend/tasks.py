from celery import shared_task
import flask_excel as excel
from model import Item as item_model
from model import User as user_model
from model import Cart as cart_model
from mail_service import send_message
from jinja2 import Template
from model import db

@shared_task(ignore_result=False)
def download():
    products_res = item_model.query.all()
    csv_output = excel.make_response_from_query_sets(products_res,["name","stock","rate","sold","date_added"],"csv")
    filename="product.csv"
    with open(filename, 'wb') as f:
        f.write(csv_output.data)
    return filename

@shared_task(ignore_result=True)
def monthly_reminder(subject):
    users = user_model.query.all()
    for user in users:
        cart = cart_model.query.filter_by(user_id=user.id, is_sent=False).all()
        for c in cart:
            c.is_sent = True
            db.session.commit()
        with open('MonthlyReport.html', 'r') as f:
            template = Template(f.read())
            send_message(user.email,subject,template.render(user = user, cart = cart))
    return "OK"

@shared_task(ignore_result=True)
def daily_reminder(subject):
    users = user_model.query.all()
    for user in users:
        cart = cart_model.query.filter_by(user_id=user.id).all()
        with open('DailyReport.html', 'r') as f:
            template = Template(f.read())
            send_message(user.email,subject,template.render(user = user, cart = cart))
    return "OK"


