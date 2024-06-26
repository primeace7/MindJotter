#!/usr/bin/env python3
'''
Definition of a user
'''
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text
from .base import basemodel, Base
from typing import List


class User(basemodel, Base):
    '''
    Define the mapping of a user object
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    __tablename__ = 'user'
    firstname = mapped_column(String(120), nullable=False)
    lastname = mapped_column(String(120), nullable=True)
    email = mapped_column(String(120),nullable=False, unique=True)
    hashed_password = mapped_column(Text, nullable=False)
    entries: Mapped[List["Entries"]] = relationship(back_populates='user', cascade="delete, delete-orphan")
    insights: Mapped[List["Insights"]] = relationship(back_populates='user', cascade="delete, delete-orphan")
    
    
    def __str__(self):
        return f'id: {self.id}, email: {self.email}, firstname:' +\
            f' {self.firstname}, Entries: {self.entries},' +\
            f'Insights: {self.insights}, ' + f'created_at: {self.created_at}'
