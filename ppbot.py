import time

import irclib
import modulehandler
import eventhandler

#irclib.DEBUG = True

# connection information, for now just have it here
# until I think of a better place to put it
network = 'localhost'
port = 6667
channel = '#test'
nick = 'billybot'
alt_nick = 'billybot2'
name = 'Powered by billy'
me = 'billy'
trigger = "."

class ppbot:
    
    def __init__ (self):
        """ Create an IRC object and do some initializations. """
		
        self.irc = irclib.IRC()
        self.server = self.irc.server()

        # initialize the module handler 
        self.module_handler = modulehandler.ModuleHandler(self.server)
        #self.event_handler = eventhandler.EventHandler(self.server)
        
        # load the default modules and auto-run modules
        self.load_modules()
      
		# register handlers for irclib
		# for now we will only be concerned with private messages and
		# messages in the channel
		# TODO: find a more elegant way to separate these two events, if necessary
        self.irc.add_global_handler('privmsg', self.handle_messages)
        self.irc.add_global_handler('pubmsg', self.handle_messages)
		
    def connect(self):
        """ Create a server object, connect and join the channel. """
		
		# connect to the server
        self.server.connect(network, port, nick, ircname=name)
        
        # loop to keep trying to connect if we aren't connected
        # might be a good idea to remove this completely, or 
        # add a timer to it
        while not self.server.is_connected():
            continue
        print "Connected to server -> %s." % network
		
		#for now just manually join a channel
        self.server.join(channel)

		# Jump into an infinite loop
        self.irc.process_forever()
		
    def load_modules(self):
        """ for now we will manually load modules, but this will eventually 
        call the database for what modules to auto-load
            
        """
	    
        self.module_handler.load('Irc')
        self.module_handler.load('Weather')
        core = self.module_handler.load('Core')
        core.module_handler = self.module_handler
		
	# Event Handlers
	# Private messages and channel messages
    def handle_messages(self, connection, event):
        if event.arguments()[0].split(' ')[0][0] == trigger:
            self.module_handler.message_handler(connection, event)
				
if __name__ == "__main__":
    bot = ppbot()
    bot.connect()