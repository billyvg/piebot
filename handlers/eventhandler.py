"""eventhandler.py
@package ppbot

Events that can occur:
protocol_events = [
    # IRC protocol events
    "error",
    "join",
    "kick",
    "mode",
    "part",
    "ping",
    "privmsg",
    "privnotice",
    "pubmsg",
    "pubnotice",
    "quit",
    "invite",
    "pong",
]
"""

import inspect
import traceback
import sys

from handlers import Handler

class EventHandler(Handler):
    """Class to handle irc events."""

    def __init__(self, server):
        """Constructor
        
        @param the irclib server object
        
        """

        self.server = server
        self.modules = {}
        self.commands = {}
        self.events = {}
        self.module_handler = None
        
    def dispatcher(self, connection, event):
        """Dispatches an event to an event handler function.
        Taken from the irclib source.
        
        """
        
        # make sure all events of these types get sent to the message handler
        allmsgs = [
            'privmsg',
            'privnotice',
            'pubmsg',
            'pubnotice'
        ]
        
        if event.eventtype() in allmsgs:
            self.message_handler(connection, event)

        try:
            # look through the events dict in the modulehandler class 
            for action, module in self.module_handler.events[event.eventtype()].iteritems():
                self.module_handler.modules[module].handle(action, connection, event)
        except:
            pass
        
    def message_handler(self, connection, event):
        """Handles incoming messages, parses them before sending to a 
        module.
        
        @param an irclib connection object
        @param an irclib event
        
        """
        module_args = {}
        #source = {}
        # parse the event
        # target is who (private message) or what (channel) the event is directed towards
        target = event.target()
        # source is where the event came from
        source = event.source()
        # the nickname of the person who sent the message
        #source['nick'] = the_source.split('!')[0]
        #source['ident'] = the_source.split('!')[1].split('@')[0]
        #source['hostname'] = the_source.split('!')[1].split('@')[1]

        # get the entire message and split it by spaces
        args = event.arguments()[0].strip().split(' ')
        # this is the first part of the message, which will be the command
        cmd = args.pop(0)[1:]
        # the number of arguments -- the rest of the message string after the command
        num_args = len(args)

        # make a dictionary for all the arguments we send to the module's handle method
        module_args['command'] = cmd
        module_args['args'] = args
        module_args['target'] = target
        module_args['source'] = source
        module_args['nick'] = source.split('!')[0]
        module_args['connection'] = connection
                
        # check to see if a command was called
        called_module = self.command(cmd)
        try: 
            if self.module_handler.commands[cmd]:
                self.module_handler.modules[self.module_handler.commands[cmd]].handle_command(connection, module_args)
        except:
            pass
            
    def command(self, command):
        """Checks if a command is mapped in the command dictionary.
        
        @param the command string
        
        """
        
        if command in self.module_handler.commands:
            return self.module_handler.commands[command]
        else:
            return None