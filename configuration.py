"""configuration.py
@package ppbot

Connects to the database to retrieve and write configuration values.

"""

import sys
import traceback

#from ppbot import self.session
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# for now we will have the db setup here
#engine = create_engine('postgres://ppbot:ppb0t@localhost:5433/ppbot', echo=True)
#session = sessionmaker(bind=engine)
#session = session()
    
Base = declarative_base()

class Configuration(Base):
    __tablename__ = 'configuration'

    # set the different fields in the user database
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String)
    value = Column(String, nullable=False)
    
    def __init__(self, name=None, value=None, description=None, engine=None, session=None, **kwargs):
    	self.name = name
    	self.value = value
    	self.description = description
    	try:
    	    self.session = session
    	    self.engine = engine
    	except:
    	    pass
            	
    def __repr__(self):
        """Pretty string formatting."""
    
        return '<Configuration(%s, %s)>' % (self.name, self.value)
	
	def get(self, key):
	    """Retrieves a configuration row by its key."""
	
        return self.session.query(Configuration).filter_by(name=key).all()
        
    def val(self, key):
        """Retrieves a configuration value by its key."""
        
        return self.session.query(Configuration).filter_by(name=key).first().value

    def session_start(self, engine, session):
        # create the necessary tables in the database using the metadata
        # from the classes
        try:
            metadata = Base.metadata
            metadata.create_all(engine)
        except:
            print "Error: Could not connect to database."
            print traceback.print_exc()
            sys.exit()

        session.add_all([
            Configuration('network', 'localhost', 'The name of the network to connect to. (temp. )'),
            Configuration('port', '6667', 'The port of the IRC server.'),
            Configuration('nickname', 'ppbot', 'The nickname that the bot should use.'),
            Configuration('password', '', 'The password for a server if necessary'),
            Configuration('alt_nickname', 'ppbot_', 'An alternate nickname the bot should use if the primary is in use.'),
            Configuration('realname', 'Powered by billy', 'The "real name" field displayed on /whois.'),
            Configuration('me', 'billy', 'lol...'),
            Configuration('trigger', '.', 'The trigger that the bot should respond to.'),
        ])

        session.close()