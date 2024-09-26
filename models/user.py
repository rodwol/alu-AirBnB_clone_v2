#!/usr/bin/python3
"""User class"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This represents the user class
    Attributes:
        email: represnt tje email address
        password: represent the password for user login
        first_name: represent user's first name
        last_name: represent user's last name
    """
    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    places = relationship(
        'Place',
        backref='user',
        cascade='all, delete-orphan')
    reviews = relationship(
        'Review',
        backref='user',
        cascade='all, delete-orphan')