import os
import re


from flask import Flask         # request, jsonify
from flask_restful import Api   #Resource, reqparse
from flask_jwt import JWT       #jwt_required

from resources.user import UserRegister
from resources.item import Item, Itemlist
from resources.store import Store, StoreList
from security import authenticate, identity

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri or "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "Adarsh_raj"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth endpoint

# @app.before_first_request
# def create_tables():
#     db.create_all()      #create table which it sees, unless they exists.

api.add_resource(Itemlist, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(UserRegister,'/register')


if __name__ == "__main__":
    from db import db
    db.create_all()
    db.init_app(app)
    app.run(port=5000, debug=True)
