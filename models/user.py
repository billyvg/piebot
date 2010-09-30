"""User.py
@package ppbot

Model for users.

"""
import traceback

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from models import Model

Base = declarative_base()

class User(Base, Model):
    """Model for users"""
    __tablename__ = 'users'

    # set the different fields in the user database
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String)
    access = Column(Integer, ForeignKey('access.id'))
    
    def __init__(self, name, password, access):
    	super(User, self).__init__()        
    	self.name = name
    	self.password = password
    	self.access = access
	
    def __repr__(self):
        """Pretty string formatting."""
    
        return '<User(%s, %s)>' % (self.name, self.access)
	
    def _getUsers():
    	"Get a list of users from the database"
    	pass