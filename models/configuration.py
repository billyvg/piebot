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
        #super(Model, self).__init__()
        #super(Base, self).__init__()
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

        # should do this elsewhere
        self.session.add_all([
            Configuration('network', 'localhost', 'The name of the network to connect to. (temp. )'),
            Configuration('port', '6667', 'The port of the IRC server.'),
            Configuration('nickname', 'ppbot', 'The nickname that the bot should use.'),
            Configuration('password', '', 'The password for a server if necessary'),
            Configuration('alt_nickname', 'ppbot_', 'An alternate nickname the bot should use if the primary is in use.'),
            Configuration('realname', 'Powered by billy', 'The "real name" field displayed on /whois.'),
            Configuration('me', 'billy', 'lol...'),
            Configuration('trigger', '.', 'The trigger that the bot should respond to.'),
        ])

        self.session.close()