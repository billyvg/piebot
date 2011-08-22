"""Handles database connection, and all that fun stuff.
@package ppbot

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

from config import BotConfig

config = BotConfig()
db_connect = 'postgresql://%s:%s@%s:%d/%s' % (
                config.get('db', 'user'),
                config.get('db', 'password'),
                config.get('db', 'host'),
                config.getint('db', 'port'),
                config.get('db', 'dbname')
            )

class Db(object):
    """
    Initializes the database

    """

    engine = create_engine(db_connect)
    sess = sessionmaker(bind=engine)
    session = sess()

    def __init__(self):
        self.engine = Db.engine
        self.session = Db.session

    def connect_db(self):
        """
        Connect to the database.  This really doesn't even need to be called

        """
        data = {}
        data['engine'] = self.engine
        data['session'] = self.session
        return data

    def init_db(self):
        """
        Create all the initial database tables.

        """

        from models.configuration import Configuration
        from models.user import Access
        from models.network import Network
        from models.server import Server
        from models.channel import Channel


        # should probably check if the db needs initializing
        init_list = [Configuration(), Access(), Network(), Server(), Channel()]

        for x in init_list:
            x.initialize_table()

