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
        
        parsed_event = self.parse_event(event, connection)
        
        if event.eventtype() in allmsgs:
            self.message_handler(parsed_event)
            
        try:
            # look through the events dict in the modulehandler class 
            for action, module in self.module_handler.events[event.eventtype()].iteritems():
                self.module_handler.modules[module].handle(action, parsed_event)
        except:
            pass
            
    def message_handler(self, event):
        """Handles incoming messages, parses them before sending to a 
        module.
        
        @param an irclib connection object
        @param an irclib event
        
        """
                        
        # check to see if a command was called
        called_module = self.command(event['command'])
        try:
            self.module_handler.modules[self.module_handler.commands[event['command']]].handle_command(event)
        except:
            pass
            
    def command(self, command):
        """Checks if a command is mapped in the command dictionary.
        
        @param the command string
        
        """

        try:
            return self.module_handler.commands[command]
        except:
            return None
            
    def parse_event(self, event, connection):
        """Parses irclib's event object into something more usable."""
        
        module_args = {}
        # target is who (private message) or what (channel) the event is directed towards
        target = event.target()
        
        # source is where the event came from
        source = event.source()
        
        # get the entire message and split it by spaces
        try:
            message = ' '.join(event.arguments())
            args = event.arguments()[0].strip().split(' ')
            cmd = args.pop(0)[1:]
            num_args = len(args)
        except:
            message = ''
            args = ''
            cmd = ''
            num_args = 0
            #print traceback.print_exc()

        
        # this is the first part of the message, which will be the command
        
        # the number of arguments -- the rest of the message string after the command

        # make a dictionary for all the arguments we send to the module's handle method
        module_args['command'] = cmd
        module_args['args'] = args
        module_args['message'] = message 
        module_args['target'] = target
        module_args['source'] = source

        try:
            module_args['nick'] = source.split('!')[0]
        except:
            pass
        module_args['connection'] = connection
        module_args['eventtype'] = event.eventtype()
        module_args['num_args'] = num_args
        
        return module_args
