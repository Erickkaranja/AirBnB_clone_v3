#!/usr/bin/python3
'''implements the restFul API blue prints with required error handlers.'''

from model import storage
from os import getenv
from dotenv import load_dotenv
from flask import Flask
from flask import make_response
from api.v1.views import api_views

app = Flask(__name__)
app.register_blueprint(app_views)

load_dotenv()

@app.teardown_appcontext
def teardown(self):
    '''call the close function from storage.'''
    storage.close()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_POST", 5000))
    app.run(host=host, port=port, threaded=True)
