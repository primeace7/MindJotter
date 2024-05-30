#!/usr/bin/env python3
'''
Define a blueprint that handles all the api routes/endpoints
'''
from flask import Blueprint, jsonify, make_response, request, abort
from ..auth.session_auth import Auth



incoming = Blueprint('incoming', __name__, url_prefix='/api/v1')
auth = Auth()

def check_login():
    '''
    Validate a user's login credentials before logging
    them in
    '''
    email = request.form.get('email')
    password = request.form.get('password')

    if not auth.is_valid_login(email=email, password=password):
        abort(401)

@incoming.route('/status', strict_slashes=False, methods=['GET'])
def status():
    '''
    Return the working status of the api service
    '''
    return {'status': 'OK'}

@incoming.route('/user/login', strict_slashes=False, methods=['POST'])
def login():
    '''
    Log a user in and create a cached session for them
    '''
    check_login()
    
    user = auth.get_user(email=request.form.get('email'))
    session_id = auth.create_session(user.id)
    response = make_response({'message': 'Logged in'})
    response.set_cookie('session_id', value=session_id)

    return response
    
@incoming.route('/logout', strict_slashes=False, methods=['DELETE'])
def logout():
    '''
    Log a user out and delete their session from the cache
    '''
    session_id = request.cookies.get('session_id')

    if session_id:
        auth.destroy_session(session_id)

    return {'message': 'Logged out'}

@incoming.route('/journal', strict_slashes=False, methods=['GET'])
def journal():
    '''
    Fetch all of a user's entries and insight for the current
    month and return them sorted chronologically, as JSON
    '''
    year = request.args.get('year')
    month = request.args.get('month')

    try:
        result = auth.get_journals(
            session_id=request.cookies.get('session_id'),
            year=year, month=month)

        return jsonify(result)
    except ValueError:
        abort(401)

@incoming.route('/entries', strict_slashes=False, methods=[
    'POST', 'DELETE', 'PATCH'])
def entries():
    '''
    Create, delete or edit a user entry and store in database
    depending on the request method.

    POST: create a new entry
    DELETE: delete a previously-created entry
    PATCH: edit/modify a previously-created entry
    '''
    session_id = request.cookies.get('session_id')
    if not session_id:
        print('session_id:', session_id)
        abort(401)
    data = request.form
    
    if request.method == 'POST':
        entry = data.get('entry')
        try:
            user_id = auth.get_userId_from_sessionId(session_id)
        except ValueError:
            abort(401)

        auth.new_entry(user_id=user_id, entry=entry)
    elif request.method == 'DELETE':
        entry_id = data.get('entry_id')
        auth.delete_entry(entry_id)
    else:
        entry = data.get('entry')
        entry_id = data.get('entry_id')
        auth.update_entry(entry, entry_id)

    return {'message': 'Success'}

@incoming.route('/insights', strict_slashes=False, methods=[
    'GET'])
def generate_insight():
    '''
    Generate an insight by making inference to an llm
    with all of a user's journal entries for the current
    month
    '''


@incoming.route('/user', strict_slashes=False, methods=[
    'GET', 'PATCH', 'POST', 'DELETE'])
def user():
    '''
    Create or delete a new user, or edit a user's information
    depending on the request method

    GET: return the user's information. e.g name, email, etc.
    PATCH: edit a user's information e.g firstname
    POST: create a new user account using provided form details
    DELETE: delete a user from the database, along with their
        entries and generated insights
    '''
    if request.method == 'POST':
        try:
            auth.new_user(request.form)
            return {'message': 'Success'}
        except ValueError:
            return {'message': 'Email already registered'}