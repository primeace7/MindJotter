#!/usr/bin/env python3
'''
Create the Flask app instance
'''
from .api.v1.endpoints.routes import incoming
from flask import Flask


app = Flask(__name__)

app.register_blueprint(incoming)


