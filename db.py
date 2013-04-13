"""Handles database connection, and all that fun stuff.
Adds a wrapper to pymongo.

@package ppbot

"""
from pymongo import mongo_client
from pymongo import database
from pymongo import collection

from settings import *

class ModuleMongoClient(mongo_client.MongoClient):
    def __getattr__(self, name):
        attr = super(ModuleMongoClient, self).__getattr__(name)
        if isinstance(attr, database.Database):
            return Database(self, name)
        return attr

class ModuleDatabase(database.Database):
    def __getattr__(self, name):
        attr = super(ModuleDatabase, self).__getattr__(name)
        if isinstance(attr, collection.Collection):
            return ModuleCollection(self, name)
        return attr

class ModuleCollection(collection.Collection):
    def __init__(self, database, name, create=False, **kwargs):
        _name = 'module_%s_%s' % (self.__class__.__name__, name)
        super(ModuleCollection, self).__init__(database=database,
            name=_name,
            create=create)

client = mongo_client.MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]
module_client = ModuleMongoClient(MONGO_HOST, MONGO_PORT)
module_db = module_client[MONGO_DB]
