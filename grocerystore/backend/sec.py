from flask_security import SQLAlchemyUserDatastore
from model import db,User,Role

user_datastore = SQLAlchemyUserDatastore(db,User,Role)