from flask import Flask

import model
from resources.message import messages_api
from resources.users import users_api

app = Flask(__name__)

app.register_blueprint(messages_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/api/v1')
if __name__ == '__main__':
    model.initialize()
    app.run(debug=True)
    app.run(port=8080)
