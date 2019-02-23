from flask import Flask
from flask_restful import Api
import  model
from resources.message import messages_api

app = Flask(__name__)

app.register_blueprint(messages_api, url_prefix = '/api/v1')

if __name__ == '__main__':
    model.initialize()
    app.run(debug=True)
    app.run(port=8080)

