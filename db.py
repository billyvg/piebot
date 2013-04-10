"""Handles database connection, and all that fun stuff.
@package ppbot

"""
from pymongo import MongoClient

from settings import *

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]
