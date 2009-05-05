"""User.py
@package ppbot

Handles users and access privileges for the bot

"""
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from enum import Enum

# Access enumeration
Access = Enum('all', 'user', 'op', 'master', 'owner')

# for now we will have the db setup here
engine = create_engine('postgres://ppbot@localhost/ppbot')
Session = sessionmaker(bind=engine)
session = Session()
    
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    # set the different fields in the user database
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String)
    access = Column(Integer)
    
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
    	

class Hostmasks(Base):
    """Hostmasks for users."""
    __tablename__ = 'hostmasks'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, Foreignkey('users.id'))
    hostmask = Column(String)
# create the necessary tables in the database using the metadata
# from the classes
metadata = Base.metadata
metadata.create_all(engine)
