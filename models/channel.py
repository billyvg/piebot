"""server.py
@package ppbot

Model for different IRC servers

"""
import traceback

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from models import Model
from models.network import Network

from db import Db

Base = declarative_base()

class Channel(Base, Model):
    __tablename__ = 'channels'

    # set the different fields in the user database
    id = Column(Integer, primary_key=True)
    network_id = Column(Integer, ForeignKey(Network.id))
    name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=True)

    network = relationship(Network, backref="channels")

    def __init__(self, **kwargs):
        Model.__init__(self)
        Base.__init__(self)
        self.metadata = Base.metadata

        for name, val in kwargs.iteritems():
            self.__setattr__(name, val)

    def __repr__(self):
        """Pretty string formatting."""

        return '<Channel:%s on network %s>' % (self.name, self.network.name)
	
	def val2(self, key):
	    """Retrieves a configuration row by its key."""
	
        return self.session.query(Server).filter_by(name=key).all()

    def val(self, key):
        """Retrieves a configuration value by its key."""

        return self.session.query(Server).filter_by(name=key).first().value

    def initialize_table(self):
        self.session.add_all([
            Channel(network_id=1, name="#dong"),
        ])

        Model.initialize_table(self)
