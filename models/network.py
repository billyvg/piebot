"""network.py
@package ppbot

Model for the different irc networks the bot can connect to.

"""
import traceback

from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from models import Model
from db import Db

Base = declarative_base()

class Network(Base, Model):
    __tablename__ = 'networks'

    # set the different fields in the user database
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    autoconnect = Column(Boolean, default=True)

    def __init__(self, name=None, autoconnect=None, **kwargs):
        Model.__init__(self)
        Base.__init__(self)
        self.metadata = Base.metadata

    	self.name = name
        self.autoconnect = autoconnect

    def __repr__(self):
        """Pretty string formatting."""

        return '<Network(%s, autoconnect:  %s): %s, %s>' % (self.name, self.autoconnect, self.servers, self.channels)
	
	def active_servers(self):
	    """Retrieves a configuration row by its key."""
	
        return self.session.query(Network).filter_by(autoconnect=True).all()

    def val(self):
        """Retrieves a configuration value by its key."""

        return self.session.query(Network).filter_by(autoconnect=True).all()
        return self.session.query(Network).filter_by(name=key).first().value

    def initialize_table(self):
        self.session.add_all([
            Network('gamesurge')
        ])

        Model.initialize_table(self)
