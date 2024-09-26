#!/usr/bin/python3
"""This module defines a class to manage DB storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
import os

class DBStorage:
    """This class manages storage of hbnb models in MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Create engine"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            os.getenv('HBNB_MYSQL_USER'),
            os.getenv('HBNB_MYSQL_PWD'),
            os.getenv('HBNB_MYSQL_HOST'),
            os.getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True)
        
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects depending on the class name"""
        if cls:
            objects = self.__session.query(cls).all()
        else:
            objects = []
            for class_name in [User, State, City, Amenity, Place, Review]:
                objects.extend(self.__session.query(class_name).all())
        
        return {"{}.{}".format(obj.__class__.__name__, obj.id): obj for obj in objects}

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in database and create a new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
