#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place, place_amenity
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """This class manages storage of hbnb models in a SQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the SQL database storage"""
        user = os.getenv('HBNB_MYSQL_USER')
        pword = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db_name = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        DATABASE_URL = f"mysql+mysqldb://{user}:{pword}@{host}:3306/{db_name}"
        self.__engine = create_engine(DATABASE_URL, pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        objects = {}
        all_classes = [User, State, City, Amenity, Place, Review]

        if cls:
            query = self.__session.query(cls)
            for obj in query.all():
                objects[f"{obj.__class__.__name__}.{obj.id}"] = obj
        else:
            for class_type in all_classes:
                query = self.__session.query(class_type)
                for obj in query.all():
                    objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

        return objects

    def new(self, obj):
        """Adds new object to storage database"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commits the session changes to database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Removes an object from the storage database"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Loads storage database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Closes the storage engine by removing the session."""
        self.__session.remove()
