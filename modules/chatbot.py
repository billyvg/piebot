from modules import *

import mh_python
import re


class Chatbot(Module):

    def __init__(self, server):
	    """Constructor."""
	    
	    Module.__init__(self, server)
        self.hal = mh_python.initbrain()

    def _register_events(self):
        """Register module events and commands."""

        self.add_event('pubmsg', 'parse_message')


    def parse_message(self, event):
        """Parses any public messages to add it to the brain,
            as well as look for users who are talking to the bot
            by detecting users who type the bot's name in chat.

            TODO: Do we want to add text when people are talking to the bot?

        """

        self.hal.learn(' '.join(event.arguments()))
        self.hal.cleanup() 
        print event

