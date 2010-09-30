"""ppbot.py

A modular python bot that utilizes/will utilize postgresql as a data source.

TODO: Lots
"""
# database stuff
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import irclib
from handlers.modulehandler import ModuleHandler
from handlers.eventhandler import EventHandler
from models.configuration import Configuration
from db import Db

# traceback shit
import inspect
import traceback
import sys
import string

#irclib.DEBUG = True

class ppbot:
    
    def __init__ (self):
        """Create an IRC object and do some initializations.
        Need to set handlers for events that may occur so that modules will be able to
        use them.
        
        """
    
        self.irc = irclib.IRC()
        self.server = self.irc.server()
        
        
        # initialize the databse
        self.engine = Db.engine
        self.session = Db.session
        
        
        # load configuration
        self.config = Configuration()
        self.config.session_start()
        
        # initialize the module handler 
        self.module_handler = ModuleHandler(self.server)
        # initialize the event handler
        self.event_handler = EventHandler(self.server)
        self.event_handler.module_handler = self.module_handler
        
        # send all events to the event handler dispatcher
        self.irc.add_global_handler('all_events', self.event_handler.dispatcher)
        
        # load the default modules and auto-run modules
        self.load_modules()
      
        
    def connect(self):
        """ Create a server object, connect and join the channel. """

        # get configuration values
        network = self.config.val('network')
        port = int(self.config.val('port'))
        nickname = self.config.val('nickname')
        password = self.config.val('password')
        realname = self.config.val('realname')

        # connect to the server
        self.server.connect(network, port, nickname, password, ircname=realname)

        # jump into an infinite loop
        self.irc.process_forever()
		
    def load_modules(self):
        """ for now we will manually load modules, but this will eventually 
        call the database for what modules to auto-load
            
        """
        
        core = self.module_handler.load('Core')
        core.module_handler = self.module_handler
        
        self.module_handler.load('Irc')
        self.module_handler.load('Weather')
        #self.module_handler.load('Aion')
        self.module_handler.load('Urlparser')
   		

if __name__ == "__main__":
    bot = ppbot()
    bot.connect()
