#!/usr/bin/env python3
'''
Definition for insights generated from running
inference on a local LLM on a user's journal entries
'''
from . import User
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, relationship, mapped_column
from .base import basemodel, Base


class Insights(basemodel, Base):
    '''
    Define the mapping of an llm generated insight on
    a user's journal entires
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    __tablename__ = 'insights'
    insight: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(String(120), ForeignKey('user.id'))
    user: Mapped[User] = relationship(back_populates='insights')

    def __str__(self):
        return f'Insight for user id {user.id}: {insight}'
