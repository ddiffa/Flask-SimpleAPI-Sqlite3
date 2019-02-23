from hashlib import md5

from flask import Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal

import model

user_fields = {
    'username': fields.String
}


class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='Username is required',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'password',
            required=True,
            help='Password is required',
            location=['form', 'json']
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        username = args.get('username')
        password = args.get('password')
        try:
            model.User.select().where(model.User.username == username).get()
        except model.User.DoesNotExist:

            user = model.User.create(
                username=username,
                password=md5(password.encode('utf-8')).hexdigest()
            )
            return marshal(user, user_fields)
        else:
            raise Exception('username sudah terdaftar')


class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='Username is required',
            location=['form', 'json']
        )

        self.reqparse.add_argument(
            'password',
            required=True,
            help='Password is required',
            location=['form', 'json']
        )
        super().__init__()

    def pos(self):
        args = self.reqparse.parse_args()
        username = args.get('username')
        password = args.get('password')
        try:
            hashpass = md5(password.encode('utf-8')).hexdigest()
            model.User.get((model.User.username == username) & (model.User.password == hashpass))
        except model.User.DoesNotExist:
            return {'messages': 'username or password is wrong !'}
        else:
            return {'messages': 'Registered'}


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(User, '/user/signin', endpoint='user/signin')
api.add_resource(UserList, '/user/register', endpoint='user/register')

