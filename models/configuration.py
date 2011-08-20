"""configuration.py
@package ppbot

Connects to the database to retrieve and write configuration values.

"""
import traceback

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from models import Model
from db import Db

Base = declarative_base()

class Configuration(Base, Model):
    __tablename__ = 'configuration'

    # set the different fields in the user database
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String)
    value = Column(String, nullable=False)
    
    def __init__(self, name=None, value=None, description=None, **kwargs):
        Model.__init__(self)
        Base.__init__(self)
    	self.name = name
    	self.value = value
    	self.description = description
        
    def __repr__(self):
        """Pretty string formatting."""
    
        return '<Configuration(%s, %s)>' % (self.name, self.value)
	
	def get(self, key):
	    """Retrieves a configuration row by its key."""
	
        return self.session.query(Configuration).filter_by(name=key).all()
        
    def val(self, key):
        """Retrieves a configuration value by its key."""
        
        return self.session.query(Configuration).filter_by(name=key).first().value

    def session_start(self):
        # create the necessary tables in the database using the metadata
        # from the classes
        try:
            metadata = Base.metadata
            metadata.create_all(self.engine)
        except:
            print "Error: Could not connect to database."
            print traceback.print_exc()

        self.session.commit()
        self.session.close()
