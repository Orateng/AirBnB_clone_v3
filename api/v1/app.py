#!/usr/bin/python3
"""
This script creates a Flask app and registers the blueprint
app_views with the Flask instance 'app'.
"""

from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})

app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_engine(exception):
    """
    Removes the currwnt SQLAlchemy Session object after each request.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Return JSON request with "Not found" error message.
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == '__main__':
    """Get the app in threaded mode"""
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
