"""Handles database connection, and all that fun stuff.
Adds a wrapper to pymongo.

@package ppbot

"""
from pymongo import mongo_client

from settings import *

client = mongo_client.MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]
