# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 14:52:32 2020
@author: prudh
"""
from flask import Flask,request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT,jwt_required

from security import authentication, identity

app = Flask(__name__)
app.secret_key = 'jim'
api = Api(app)

jwt = JWT(app,authentication,identity)

items =[]

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This Field cannot be left blank'
                        )
    @jwt_required
    def get(self ,name):
        item = next(filter(lambda x:x['name']==name,items),None)
        return {"Item":item},200 if item else 404

    def post(self,name):
        if next(filter(lambda x:x['name']==name,items),None):
            return {"message":"An item with '{}' already exists".format(name)},400
        data = Item.parser.parse_args()
        item ={"name":name,"price":data["price"]}
        items.append(item)
        return item,201

    def delete(self,name):
        global items
        items = list(filter(lambda x:x['name']!=name,items))
        return {'message':'Item Deleted'}


    def put(self,name):

        data = Item.parser.parse_args()
        item = next(filter(lambda x:x['name']==name,items),None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item

class itemslist(Resource):
    def get(self):
        return{"items":items}

api.add_resource(Item,'/item/<string:name>')
api.add_resource(itemslist,"/items")

app.run(port=5001,debug=True)