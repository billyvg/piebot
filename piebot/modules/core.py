from modules import *

import irc.client

class Core(Module):
    """Core Module to provide chat commands for core functionality of 
    ppbot.

    """

    def __init__(self, *args, **kwargs):
        """Constructor."""

        Module.__init__(self, kwargs=kwargs)
        self.module_handler = None

    def _register_events(self):
        """Register module commands."""

        # events
        self.add_event('welcome', 'welcome')
        self.add_event('disconnect', 'disconnected')

        # commands
        self.add_command('load')
        self.add_command('reload')
        self.add_command('raw')

    @master
    def load(self, event):
        """Loads a module specified from IRC.

        @param the irclib event object

        """

        if self.num_args == 1:
            if self.module_handler.load(event['args'][0].title()):
                self.notice(event['nick'], 
                    'Successfully loaded module: %s' % event['args'][0])
            else:
                self.notice(event['nick'], 
                    'Could not load module: %s' % event['args'][0])
        else:
            self.syntax_message(event['nick'], '.load <module>')

    @master
    def reload(self, event):
        """Reloads a module specified from IRC.

        @param the irclib event object

        """

        if self.num_args == 1:
            # if module was successfully reloaded
            if self.module_handler.reload(event['args'][0].title()):
                # alert the user that reload was successful
                self.notice(event['nick'], 
                    'Successfully reloaded module: %s' % event['args'][0])
                # re-register any commands
                self.module_handler.modules[event['args'][0].title()]._register_events()
            else:
                # alert user that reload failed
                self.notice(event['nick'], 
                    'Could not reload module: %s' % event['args'][0])
        else:

            self.syntax_message(event['nick'], '.reload <module>')

    @owner
    def raw(self, event):
        """Processes a raw python command from IRC.

        @param the python command to run

        """
        try:
            print ' '.join(event['args'])
            self.msg(event['target'], eval(' '.join(event['args'])))
        except Exception, e:
            print e

    def welcome(self, event):
        """Event handler for when the bot connects to a server."""

        try:
            print "Connected to network: %s." % event['source']
        except:
            import traceback
            traceback.print_exc()
            print self.server
            import pdb
            pdb.set_trace()

        for channel in db.channels.find({'network': self.server.server_config['name']}):
            self.server.join(channel['name'])

    def disconnected(self, event):
        """Event handler for when the bot connects to a server."""

        print "Disconnected from network %s." % event
        # TODO : reconnect
        self._reconnect(event['connection'])

    def _reconnect(self, connection):
        try:
	    self.server.connect(connection.server, connection.port, connection.username, connection.password)
        except irc.client.ServerConnectionError:
            self._reconnect(connection)
