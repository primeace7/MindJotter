#!/usr/bin/env python3
'''
Create the Flask app instance
'''
from .api.v1.endpoints.routes import incoming
from flask import Flask, request
from flask_cors import CORS


app = Flask(__name__)
CORS(incoming, supports_credentials=True, origins=['http://127.0.0.1', 'http://localhost'])    

app.register_blueprint(incoming)


