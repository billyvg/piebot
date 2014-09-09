"""piebot.py

A modular python bot

TODO: Lots
"""

import traceback
import logging

import irc.client
import irc.buffer
import irc.logging

import gevent
from gevent import monkey; monkey.patch_all()
from gevent import wsgi

from handlers.modulehandler import ModuleHandler
from handlers.eventhandler import EventHandler

from http.core import app as httpcore

from piebot.db import db
from piebot import settings


class Bot(object):

    def __init__ (self, cli_args):
        """Create an IRC object and do some initializations.
        Need to set handlers for events that may occur so that modules will be able to
        use them.

        """
        self.ircloop_timeout = 0.5

        irc.logging.setup(cli_args)
        self.irc = irc.client.IRC()
        irc.client.ServerConnection.buffer_class = irc.buffer.LenientDecodingLineBuffer

        self.servers = []

        # initialize the module handler
        self.module_handler = ModuleHandler(self.servers, self.irc, httpcore=httpcore)

        # initialize the event handler
        self.event_handler = EventHandler(self.servers)
        self.event_handler.module_handler = self.module_handler

        # send all events to the event handler dispatcher
        self.irc.add_global_handler('all_events', self.event_handler.dispatcher)

        # load the default modules and auto-run modules
        self.load_modules()

    def start(self):
        """ Starts the bot, httpd, and connects to IRC. """

        server = wsgi.WSGIServer(('', settings.HTTP_PORT), httpcore)

        gevent.joinall([gevent.spawn(self.connect), gevent.spawn(server.serve_forever)])

    def connect(self):
        """ Create a server object, connect and join the channel. """

        networks = db.networks.find()

        for network in networks:
            # connect to the server
            server = self.irc.server()
            server.buffer_class.errors = 'replace'
            self.servers.append(server)
            server.server_config = network

            # TODO: should be using a queue for the servers to go through, 
            # since it could be possible to have more than one server to 
            # try to connect to.
            server_config = db.servers.find_one({'network': network['name']})
            try:
                server_config.setdefault('port', 6667)
                server_config.setdefault('password', '')
                server.connect(server_config['address'], int(server_config['port']), server_config['nickname'], server_config['password'])
            except:
                import traceback
                traceback.print_exc()
                print "<<Error>> Couldn't connect to %s:%s" % (server_config['address'], server_config['port'])

        # jump into an infinite loop
        jobs = [gevent.spawn(self.irc.process_forever)]
        gevent.joinall(jobs)

    def _run(self):
        self.irc.process_once(self.ircloop_timeout)
        gevent.sleep(self.ircloop_timeout)

    def load_modules(self):
        """ for now we will manually load modules, but this will eventually 
        call the database for what modules to auto-load

        """

        core = self.module_handler.load('Core')
        core.module_handler = self.module_handler

        self.module_handler.load('Coreirc')
        self.module_handler.load('Weather')
        self.module_handler.load('Stock')
        self.module_handler.load('Urldupe')
        self.module_handler.load('Urbandictionary')
        self.module_handler.load('Rottentomatoes')
        self.module_handler.load('Karmamod')
        self.module_handler.load('Yelp')
        self.module_handler.load('Quotemod')
        self.module_handler.load('Search')
        self.module_handler.load('Isup')
        self.module_handler.load('Notemod')
        self.module_handler.load('Urlparser')
        self.module_handler.load('Github')
        self.module_handler.load('Wikipediamod')
        self.module_handler.load('Choose')
        self.module_handler.load('Bitcoin')
