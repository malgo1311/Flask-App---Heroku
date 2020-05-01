import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
            type=str,
            required=True,
            help='This field cannot be left blank'
    )
    parser.add_argument('password',
            type=str,
            required=True,
            help='This field cannot be left blank'
    )

    def post(self):

        # data = request.get_json()
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']): #is not None
            return {'message': 'A user with same username already exists'}, 401

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {'message': 'New user registered'}, 201
