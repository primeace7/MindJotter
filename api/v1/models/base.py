#!/usr/bin/env python3
'''
The base model definition for all other models
'''
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
from datetime import datetime, timezone
from uuid import uuid4


class Base(DeclarativeBase):
    pass

class basemodel():
    '''
    The foundation model defining common utilities for all
    other models
    '''

    created_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)
    id: Mapped[str] = mapped_column(String(120), primary_key=True)
    
    def __init__(self, *args, **kwargs):
        self.id = str(uuid4())
        for key, val in kwargs.items():
            setattr(self, key, val)

        if kwargs.get('created_at') is None:
            self.created_at = datetime.now(tz=timezone.utc).isoformat()
            self.updated_at = self.created_at
        else:
            self.created_at = datetime.fromisoformat(kwargs.get('created_at'))
            self.updated_at = datetime.fromisoformat(kwargs.get('created_at'))

    def to_json(self):
        '''
        Convert a class instance to json(dictionary) format.
        All keys and values are strings
        '''
        json = {}

        for key, val in self.__dict__.items():
            if key[0] != '_':
                if isinstance(val, datetime):
                    json[key] = val.isoformat()
                else:
                    json[key] = val
        return json

    
