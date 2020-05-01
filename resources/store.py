from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel

class Store(Resource):

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
        store = StoreModel.find(name)
        if store is None:
            return {'message': 'Store not found'}, 404

        return store.json(), 200

    def post(self, name):
        store = StoreModel.find(name)
        if store:
            return {'message': "An store with name {} exists".format(name)}, 400

        store = StoreModel(name)
        store.save_to_db()

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find(name)
        if store is None:
            return {'message': "No store found"}, 400

        store.delete_from_db()
        return {'message': 'Store <{}> deleted'.format(name)}


class StoreList(Resource):
    def get(self):
        return {'Stores': [store.json() for store in StoreModel.query.all()]}
        # list(map(lambda x: x.json(), ItemModel.query.all()))