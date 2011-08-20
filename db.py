"""Handles database connection, and all that fun stuff.
@package ppbot

"""

import ConfigParser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

config = ConfigParser.RawConfigParser()
config.readfp(open('ppbot.cfg'))
db_connect = 'postgresql://%s:%s@%s:%s/%s' % (
                config.get('db', 'user'),
                config.get('db', 'password'),
                config.get('db', 'host'),
                config.get('db', 'port'),
                config.get('db', 'dbname')
            )

class Db:
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
        #self.engine = create_engine('postgres://ppbot:ppb0t@localhost:5433/ppbot', echo=True)
        #session = sessionmaker(bind=self.engine)
        #self.session = session()
        data = {}
        data['engine'] = self.engine
        data['session'] = self.session
        return data
        
    def init_db(self):
        """
        Create all the initial database tables.
        
        """
        
        metadata = MetaData()
        
        users_table = Table('users', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(50)),
            Column('password', String),
            Column('access', Integer)
        )
        configuration_table = Table('configuration', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(50)),
            Column('value', String),
            Column('description', String)
        )
        modules_table = Table('modules', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(50)),
            Column('description', String),
            Column('version', String),
            Column('autoload', Integer)
        )
        metadata.create_all(self.engine)

#        self.session.add_all([
#            Configuration('network', 'localhost', 'The name of the network to connect to. (temp. )'),
#            Configuration('port', '6667', 'The port of the IRC server.'),
#            Configuration('nickname', 'ppbot', 'The nickname that the bot should use.'),
#            Configuration('password', '', 'The password for a server if necessary'),
#            Configuration('alt_nickname', 'ppbot_', 'An alternate nickname the bot should use if the primary is in use.'),
#            Configuration('realname', 'Powered by billy', 'The "real name" field displayed on /whois.'),
#            Configuration('me', 'billy', 'lol...'),
#            Configuration('trigger', '.', 'The trigger that the bot should respond to.'),
#        ])
#
        self.session.close()
