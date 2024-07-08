#!/usr/bin/env python3
'''
Defines a connection to the Mysql database and
all data DDL and DML methods
'''
from sqlalchemy import create_engine, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from ..models.user import User
from ..models.insights import Insights
from ..models.entries import Entries
from ..models.base import Base
from typing import Mapping
import os


# define type alias for all data objects for future use
type data_objs = User | Entries | Insights

class DB():
    '''
    Model of the storage object that enables
    all interactions between data models and the MySQL
    database through SQLAlchemy
    '''
    def __init__(self):
        self.db_username = os.getenv('DB_USERNAME', 'mindjotter')
        self.db_password = os.getenv('DB_PASSWORD', 'mindjotter')
        self.db_name = os.getenv('DB_NAME', 'mindjotter')
        self.db_host = os.getenv('DB_HOST', 'localhost')

        uri = f'mysql://{self.db_username}:{self.db_password}@{self.db_host}/{self.db_name}'

        self.engine = create_engine(uri)
        Session = sessionmaker(self.engine)
        self._session = Session()

    def add(self, obj: data_objs) -> None:
        '''
        Add a new object of type obj to current db session
        '''
        self._session.add(obj)

    def save(self) -> None:
        '''
        Save the current session objects in the Base metadata to the db
        '''
        self._session.commit()

    def find_user(self, user_id=None, email=None) -> User:
        '''
        Search for a User object in the database based on id or email
        '''
        if email:
            result = self._session.execute(
                select(User).filter(User.email==email)).scalar()
        else:
            result = self._session.execute(
                select(User).filter(User.id==user_id)).scalar()
        if not result:
            raise NoResultFound

        return result

    def find_entry(self, entry_id) -> Entries:
        '''
        Search for an Entries object in the database based on id
        '''
        result = self._session.execute(select(Entries).filter(
            Entries.id==entry_id)).scalar()

        return result

    def find_insight(self, insight_id) -> Insights:
        '''
        Search for an Insights object in the database based on id
        '''
        result = self._session.execute(select(Insights).filter(
            Insights.id==insight_id)).scalar()

        return result
    
    def update(self, obj_type: data_objs, obj_id: str,
               changes: Mapping) -> None:
        '''
        Update an object in the database, whose id is obj_id and
        make the changes specified in the changes argument

        Args:
        obj_type - the object type to update: User, Entries, or Insights
        obj_id - the unique id of the object to update
        changes - a dictionary whose key, value pairs represent the fields
            to update and the new value of the fields, respectively
        '''
        if obj_type is User:
            to_update = self.find_user(user_id=obj_id)
        elif obj_type is Entries:
            to_update = self.find_entry(entry_id=obj_id)
        else:
            to_update = self.find_insight(insight_id=obj_id)

        for key, val in changes.items():
            to_update.key = val
        self.add(to_update)
        self.save()

    def delete(self, obj_type: data_objs, obj_id: str) -> None:
        '''
        Delete an object of type obj_type with id obj_id
        from the database

        Args:
        obj_type - the object type to delete: User, Entries, or Insights
        obj_id - the unique id of the object to delete
        '''
        try:
            if obj_type is User:
                to_delete = self.find_user(user_id=obj_id)
            elif obj_type is Entries:
                to_delete = self.find_entry(entry_id=obj_id)
            else:
                to_delete = self.find_insight(insight_id=obj_id)
        except NoResultFound:
            return

        self._session.delete(to_delete)
        self.save()

    def reload(self):
        '''
        reload the db storage by creating all tables
        in the metadata object if they don't already
        exist
        '''
        Base.metadata.create_all(self.engine)
