from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel
# from models.item.ItemModel import insert, update

# HTTP codes
# 200 - ok
# 201 - created
# 202 - accepted

# 400 - bad request
# 404 - not found

# 500 - Internal Server Error

# api works with Resouces. And every resource needs to be a class
# No need to use jasonify because flask_restful does it all...... yaaay!!
class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help='This field cannot be left blank'
    )
    parser.add_argument('store_id',
            type=int,
            required=True,
            help='This field cannot be left blank'
    )

    @jwt_required()
    def get(self, name):
        # next gives the first result found
        item = ItemModel.find(name)
        if item is None:
            return {'message': 'Item not found'}, 404

        return item.json(), 200

    def post(self, name):
        item = ItemModel.find(name)
        if item:
            return {'message': "An item with name {} exists".format(name)}, 400

        # force=True
        # You do not need content-type header
        # silent=True
        # Doesn't give an error, just returns None
        # data = request.get_json()
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        item.insert_or_update()

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find(name)
        if item is None:
            return {'message': "No item found"}, 400

        item.delete_in_db()
        return {'message': 'Item <{}> deleted'.format(name)}

    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()
        # updated_item = ItemModel(name, data['price'])
        # updated_item.insert_or_update()

        item = ItemModel.find(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.insert_or_update()

        return item.json(), 200 


class ItemList(Resource):
    def get(self):
        return {'itmes': [item.json() for item in ItemModel.query.all()]}
        # list(map(lambda x: x.json(), ItemModel.query.all()))