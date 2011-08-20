"""User.py
@package ppbot

Handles users and access privileges for the bot

"""
import sys
import traceback

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models import Model
from db import Db

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    # set the different fields in the user database
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String)
    access = Column(Integer, ForeignKey('access.id'))

    def __init__(self, name=None, password=None, access=None, **kwargs):
    	#self.users = self._getUsers()
    	self.name = name
    	self.password = password
    	self.access = access
	
    def __repr__(self):
        """Pretty string formatting."""

        return '<User(%s, %s)>' % (self.name, self.access)
	
    def _getUsers():
    	"Get a list of users from the database"
    	pass


class Hostmasks(Base):
    """Hostmasks for users."""
    __tablename__ = 'hostmasks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    hostmask = Column(String)

    def __init__(self, user_id, hostmask):
        self.user_id = user_id
        self.hostmask = hostmask

    def __repr__(self):
        """Pretty string formatting."""

        return '<Hostmask(%d, %s)>' % (self.user_id, self.hostmask)

class Access(Base, Model):
    """Table to hold all the different access levels."""
    __tablename__ = 'access'

    id = Column(Integer, primary_key=True)
    access = Column(String)

    def __init__(self, access=None, **kwargs):
        Model.__init__(self)
        Base.__init__(self)
        self.access = access

    def __repr__(self):
        """Pretty string formatting."""

        return '<Access(%s)>' % (self.access)

    def initialize_table(self):
        try:
            metadata = Base.metadata
            metadata.create_all(self.engine)
        except:
            print "Error: Could not connect to database."
            print traceback.print_exc()

        self.session.add_all([
            Access('master'),
            Access('owner'),
            Access('op'),
            Access('user'),
            Access('guest'),
            Access('all')
        ])

        self.session.commit()
        self.session.close()
