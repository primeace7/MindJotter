#!/usr/bin/env python3
'''
Define and implement a session authentication scheme
for the application using Redis as session storage
'''
from . import storage
from typing import Mapping
from ..storage.cache import redis_cache
from redis.exceptions import DataError
from . import User, Entries, Insights
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import NoResultFound, IntegrityError
from uuid import uuid4
from datetime import datetime, timedelta, timezone


def get_uid() -> str:
    '''
    Create and return a uuid4 as a string
    '''
    return str(uuid4())

def hash_pwd(password: str) -> str:
    '''
    Generate and return a password hash
    '''
    return generate_password_hash(password)


class Auth:
    '''
    A session auth provider that uses Redis for session
    storage
    '''
    def __init__(self):
        self._db = storage
        self._redis = redis_cache

    def is_valid_login(self, email: str, password: str) -> bool:
        '''
        Determine if a user's login credentials are valid
        Return True if valid, or False otherwise
        '''
        try:
            user = self._db.find_user(email=email)
            if check_password_hash(user.hashed_password, password):
                return True
            return False
        except NoResultFound:
            return False

    def get_userId_from_sessionId(self, session_id: str) -> str | None:
        '''
        Get a user id corresponding to a session id from
        redis cache
        '''
        user_id = self._redis.get(session_id)
        if not user_id:
            raise ValueError
        return user_id.decode()

    def get_user(self, user_id: str = None, email: str = None) -> User:
        '''
        Get a user from the database using the given user_id or email
        '''
        try:
            if user_id:
                result = self._db.find_user(user_id=user_id)
            else:
                result = self._db.find_user(email=email)
            return result

        except NoResultFound:
            raise ValueError

    def all_user_entries(self, session_id: str) -> list[Entries]:
        '''
        Get all entries of a specific user from the database,
        given the user's session_id
        '''
        user_id = self._redis.get(session_id)

        if not user_id:
            raise ValueError
        
        user_id = user_id.decode()
        
        user = self.get_user(user_id=user_id)
        return user.entries

    def all_user_insights(self, session_id: str) -> list[Insights]:
        '''
        Get all insights generated for a specific user from
        the database, given the user's session_id
        '''
        user_id = self._redis.get(session_id)

        if not user_id:
            raise ValueError
        
        user_id = user_id.decode()
        
        user = self.get_user(user_id=user_id)
        return user.insights

    def new_entry(self, **kwargs) -> None:
        '''
        Create a new journal entry and save in database
        '''
        filters = {}
        for key, val in kwargs.items():
            if key in Entries.__table__.columns:
                filters[key] = val

        new_entry = Entries(**filters)
        self._db.add(new_entry)
        self._db.save()

    def new_insight(self, **kwargs) -> str:
        '''
        Generate a new insight and save in database
        '''
        filters = {}
        for key, val in kwargs.items():
            if key in Insights.__table__.columns:
                filters[key] = val

        new_insight = Insights(**filters)
        self._db.add(new_insight)
        self._db.save()
        return new_insight.id

    def new_user(self, data: Mapping) -> None:
        '''
        Create a new user in the database

        Args:
        data - a dict-like object containing the new user's
        info, e.g email, firstname. it's the same as request.form
        in Flask
        '''
        for key in ['firstname', 'email', 'password']:
            if data.get(key) is None:
                raise ValueError

            try:
                if self.get_user(email=data.get('email')):
                    raise TypeError
            except ValueError:
                continue

        new_user = User(firstname=data.get('firstname'),
                        email=data.get('email'),
                        hashed_password=hash_pwd(data.get('password')),
                        lastname=data.get('lastname'))
        self._db.add(new_user)
        self._db.save()
        
    def create_session(self, user_id: str) -> str:
        '''
        Create and return a new session id for a logged-in user
        '''
        session_id = get_uid()
        self._redis.setex(session_id, timedelta(hours=1), user_id)
        return session_id

    def destroy_session(self, session_id: str) -> None:
        '''
        Destroy a user's session id from the cache during logout
        '''
        self._redis.delete(session_id)

    def delete_entry(self, entry_id:str) -> None:
        '''
        Delete a user's journal entry from the database
        '''
        self._db.delete(Entries, entry_id)

    def update_entry(self, entry, entry_id):
        '''
        Update a user's journal entry in the database after an edit
        '''
        self._db.update(Entries, entry_id, {'entry': entry})

    def get_journals(self, session_id, year=None, month=None):
        '''
        Get all of a user's entries and insights sorted in
        chronological order, and return them as JSON
        '''
        try:
            all_entries = self.all_user_entries(session_id)
            all_insights = self.all_user_insights(session_id)
        except ValueError:
            raise
        
        current_date = datetime.now(tz=timezone.utc)
  
        if not year:
            year = current_date.year
        if not month:
            month = current_date.month
            
        start = datetime(year=year + (month // 12), month=month, day=1)

        stop = datetime(year=year + (month // 12),
                        month=(month % 12) + 1,
                        day=1)
        
        current_month_entries = [
            entry for entry in all_entries
            if entry.created_at >= start and entry.created_at < stop]
        current_month_insights = [
            insight for insight in all_insights
            if insight.created_at > start and insight.created_at < stop]

        journals = current_month_entries
        journals.extend(
            current_month_insights)

        journals.sort(key=lambda obj: obj.timestamp)

        journals_json = {}
        fmt = '%A %B %d'

        for obj in journals:
            pretty_date = obj.created_at.strftime(fmt)
            if pretty_date not in journals_json:
                journals_json[pretty_date] = [obj.to_json()]
            else:
                journals_json[pretty_date].append(obj.to_json())

        return journals_json
