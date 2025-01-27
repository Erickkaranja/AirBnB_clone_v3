#!/usr/bin/python3
'''implements the restFul API blue prints with required error handlers.'''

from models import storage
import os
from flask import Flask
from flask import make_response, jsonify
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": os.getenv("HBNB_API_HOST",
            "0.0.0.0")}})
'''flask web application instance.'''
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    '''call the close function from storage.'''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_POST", 5000))
    app.run(host=host, port=port, threaded=True)
