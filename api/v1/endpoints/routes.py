#!/usr/bin/env python3
'''
Define a blueprint that handles all the api routes/endpoints
'''
from flask import Blueprint, jsonify, make_response, request, abort, url_for, redirect
from ..auth.session_auth import Auth
from ..ollama.inference import generate_insights


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
    result = make_response({'status': 'OK'})
    return result

@incoming.route('/user/login', strict_slashes=False, methods=['POST'])
def login():
    '''
    Log a user in and create a cached session for them
    '''
    check_login()
    
    user = auth.get_user(email=request.form.get('email'))
    session_id = auth.create_session(user.id)
    result = {'redirect': f"{request.host_url[:request.host_url.rfind(':')] + '/journal-area.html'}"}
    result['session'] = session_id

    return result
    
@incoming.route('/logout', strict_slashes=False, methods=['DELETE'])
def logout():
    '''
    Log a user out and delete their session from the cache
    '''
    session_id = request.args.get('id')

    if session_id:
        auth.destroy_session(session_id)

    result = {'redirect': f"{request.host_url[:request.host_url.rfind(':')] + '/login.html'}"}
    result['message'] = 'Success'
    return result

@incoming.route('/journal', strict_slashes=False, methods=['GET'])
def journal():
    '''
    Fetch all of a user's entries and insight for the current
    month and return them sorted chronologically, as JSON
    '''
    year = request.args.get('year')
    month = request.args.get('month')

    try:
        session_id = request.args.get('id')
        print('session_id from cookies: ', session_id)
        result = auth.get_journals(
        session_id=session_id,
            year=year, month=month)

        result = make_response(jsonify(result))
        return result
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
    session_id = request.args.get('id')

    if not session_id:
        print('session_id not found in request args')
        abort(401)
    data = request.get_json()
    
    if request.method == 'POST':
        entry = data.get('entry')
        try:
            user_id = auth.get_userId_from_sessionId(session_id)
            print('user found from session_id')
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
    'GET', 'POST'])
def generate_insight():
    '''
    Generate an insight by making inference to ollama
    with all of a user's journal entries for the current
    month
    '''
    session_id = request.args.get('id')

    if request.method == 'POST':
        try:
            user_id = auth.get_userId_from_sessionId(session_id=session_id)
        except ValueError:
            abort(401)

        insight = request.get_json().get('insight')
        auth.new_insight(insight=insight, user_id=user_id)
        return {'message': 'Success'}
    else:
        result = generate_insights(session_id=session_id)
        try:
            user_id = auth.get_userId_from_sessionId(session_id=session_id)
        except ValueError:
            abort(401)

        result = make_response({'generated_insight': result})
        result.content_type = 'text/plain'
        return result


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
            result = {'message': 'User created successfully'}
            return result
        except ValueError:
            return {'message': 'Form is missing required field(s)'}, 400
        except TypeError:
            return {'message': 'Email is already registered'}, 409
