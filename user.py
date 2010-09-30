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

from db import Db
    
Base = declarative_base()
engine = Db.engine
session = Db.session

class User(Base):
    __tablename__ = 'users'

    # set the different fields in the user database
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String)
    access = Column(Integer, ForeignKey('access.id'))
    
    def __init__(self, name, password, access):
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
        
class Access(Base):
    """Table to hold all the different access levels."""
    __tablename__ = 'access'
    
    id = Column(Integer, primary_key=True)
    access = Column(String)
    
    def __init__(self, user_id, access):
        self.user_id = user_id
        self.access = access
        
    def __repr__(self):
        """Pretty string formatting."""
        
        return '<Access(%s)>' % (self.access)
        
        
# create the necessary tables in the database using the metadata
# from the classes
try:
    metadata = Base.metadata
    metadata.create_all(engine)
except:
    print "Error: Could not connect to database."
    print traceback.print_exc()
    sys.exit()
