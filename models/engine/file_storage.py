#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import os
from importlib import import_module


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def __init__(self):
        """Initializes a FileStorage instance"""
        self.model_classes = {
            'BaseModel': import_module('models.base_model').BaseModel,
            'User': import_module('models.user').User,
            'State': import_module('models.state').State,
            'City': import_module('models.city').City,
            'Amenity': import_module('models.amenity').Amenity,
            'Place': import_module('models.place').Place,
            'Review': import_module('models.review').Review
        }

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects
        else:
            return {k: v for k, v in self.__objects.items(
            ) if isinstance(v, cls)}

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.__objects[f"{obj.to_dict()['__class__']}.{obj.id}"] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w') as file:
            json.dump({k: v.to_dict(
            ) for k, v in self.__objects.items()}, file)

    def reload(self):
        """Loads storage dictionary from file"""
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
                for key, val in data.items():
                    self.__objects[key] =
                    self.model_classes[val['__class__']](**val)

    def delete(self, obj=None):
        """Removes an object from the storage dictionary"""
        if obj is not None:
            obj_key = f"{obj.to_dict()['__class__']}.{obj.id}"
            self.__objects.pop(obj_key, None)

    def close(self):
        """Closes the storage engine by reloading data from file."""
        self.reload()
