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

class Server(Base, Model):
    __tablename__ = 'servers'

    # set the different fields in the user database
    id = Column(Integer, primary_key=True)
    network_id = Column(Integer, ForeignKey(Network.id))
    address = Column(String(50), nullable=False)
    port = Column(Integer, default=6667, nullable=False)
    nickname = Column(String(50), nullable=False)
    alt_nickname = Column(String(50), nullable=False)
    password = Column(String(50), nullable=True)
    realname = Column(String(50), nullable=False)

    network = relationship(Network, backref="servers")

    def __init__(self, **kwargs):
        Model.__init__(self)
        Base.__init__(self)
        self.metadata = Base.metadata

        for name, val in kwargs.iteritems():
            self.__setattr__(name, val)

    def __repr__(self):
        """Pretty string formatting."""

        return '<Server(%s)>' % (self.address)
	
	def val2(self, key):
	    """Retrieves a configuration row by its key."""
	
        return self.session.query(Server).filter_by(name=key).all()

    def val(self, key):
        """Retrieves a configuration value by its key."""

        return self.session.query(Server).filter_by(name=key).first().value

    def initialize_table(self):
        self.session.add_all([
            Server(network_id=1, address="irc.gamesurge.net", port=6667,
                   nickname="ppbot", alt_nickname="ppbot",
                   realname="Powered by Dong Energy"),
        ])

        Model.initialize_table(self)
