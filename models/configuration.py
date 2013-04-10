"""configuration.py
@package ppbot

Connects to the database to retrieve and write configuration values.

"""
import traceback

from models import Model
from db import db

class Configuration(Model):
    collection = 'configuration'

    def __init__(self, name=None, value=None, description=None, **kwargs):
        pass

    def __repr__(self):
        """Pretty string formatting."""

        return '<Configuration(%s, %s)>' % (self.name, self.value)

