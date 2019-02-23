from flask import jsonify, Blueprint
from flask_restful import Resource, Api, reqparse

import model


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
        messages = {}
        query = model.Message.select()

        for row in query:
            messages[row.id] = {'content': row.content, 'published_at': row.published_at}

        return jsonify({'messages': messages})

    def post(self):
        args = self.reqparse.parse_args()
        message = {}
        row = model.Message.create(**args)
        message[row.id] = {'content': row.content, 'published_at': row.published_at}

        return jsonify({'messages': message,'success': True })


class Message(Resource):
    def get(self, id):
        query = model.Message.get_by_id(id)
        return jsonify({'content': query.content, 'published_at': query.published_at})


messages_api = Blueprint('resources.message', __name__)
api = Api(messages_api)

api.add_resource(MessageList, '/messages', endpoint='messages')
api.add_resource(Message, '/message/<int:id>', endpoint='message')
