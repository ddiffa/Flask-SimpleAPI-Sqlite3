from flask import jsonify, Blueprint, abort
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with

import model

message_fileds = {
    'id': fields.Integer,
    'content': fields.String,
    'published_at': fields.String
}


def get_or_abort(id):
    try:
        msg = model.Message.get_by_id(id)
    except model.Message.DoesNotExist:
        raise abort(404)
    else:
        return msg


class MessageList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'content',
            required=True,
            help='Content is required',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'published_at',
            required=True,
            help='Published_at is required',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        messages = [marshal(message, message_fileds) for message in model.Message.select()]
        return jsonify({'messages': messages})

    def post(self):
        args = self.reqparse.parse_args()
        message = model.Message.create(**args)
        return marshal(message,message_fileds)


class Message(Resource):
    @marshal_with(message_fileds)
    def get(self, id):
        return get_or_abort(id)


messages_api = Blueprint('resources.message', __name__)
api = Api(messages_api)

api.add_resource(MessageList, '/messages', endpoint='messages')
api.add_resource(Message, '/message/<int:id>', endpoint='message')
