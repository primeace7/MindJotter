#!/usr/bin/env python3
'''
Definition of a user's journal entry
'''
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import basemodel, Base
from sqlalchemy import Text, ForeignKey, String
from . import User
import time


class Entries(basemodel, Base):
    '''
    Define the mapping of a user's journal entry
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    __tablename__ = 'entries'
    entry: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(String(120), ForeignKey('user.id'))
    user: Mapped[User] = relationship(back_populates='entries')

    def __str__(self):
        return f'Entry from user_id {self.user.id}: {self.entry}'
        
