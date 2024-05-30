#!/usr/bin/env python3
'''
Define custom error handlers for the api service
'''
from flask import error_handler
from .routes import incoming

@incoming.error_handler(404)
def error_404():
    '''
    Define custom 404 error for api service
    '''
    return {'message': 'Not found'}, 404

@incoming.error_handler(403)
def error_403():
    '''
    Define custom 403 error for api service
    '''
    return {'message': 'Unauthorized'}, 403

@incoming.error_handler(401)
def error_401():
    '''
    Define custom 401 error for api service
    '''
    return {'message': 'Forbidden'}, 401
