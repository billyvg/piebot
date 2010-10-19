from modules import *

import re

try:
    import mh_python
except:
    raise("You need the megaHAL for python installed.")


class Chatbot(Module):
    def __init__(self, server):
        """Constructor."""

        Module.__init__(self, server)
        mh_python.initbrain()
        
    def _register_events(self):
        """Register module events and commands."""

        self.add_event('pubmsg', 'parse_message')

    def parse_message(self, event):
        """Parses any public messages to add it to the brain,
        as well as look for users who are talking to the bot
        by detecting users who type the bot's name in chat.

        TODO: Do we want to add text when people are talking to the bot?

        """
        
        bot_nick = self.server.get_nickname()
        message = ' '.join(event['args'])
        
        # check if the bot's name was used
        m = re.search(bot_nick, message)
        if m:
            # we don't want the bot to learn its own nick
            message = re.sub(bot_nick, '', message)
            
            # get the megaHAL reply
            reply = mh_python.doreply(message)
            self.msg(event['target'], reply)
            
        self.learn_message(message)
    
    def learn_message(self, message):
        """Passes the message to megahal brain to learn."""
        
        mh_python.learn(message)
        mh_python.cleanup() 

