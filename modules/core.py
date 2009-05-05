from modules import *

class Core(Module):
    """Core Module to provide chat commands for core functionality of 
    piebot.

    """

    def __init__(self, server):
        """Constructor."""

        Module.__init__(self, server)
        self.module_handler = None

    def _register_triggers(self):
        """Register module triggers."""

        self.add_trigger('load', 'load')
        self.add_trigger('reload', 'reload')

    def load(self, event):
        """Loads a module specified from IRC.

        @param the irclib event object

        """

        if self.num_args == 1:
            if self.module_handler.load(event['args'][0].title()):
                self.notice(event['source']['nick'], 
                    'Successfully loaded module: %s' % event['args'][0])
            else:
                self.notice(event['source']['nick'], 
                    'Could not load module: %s' % event['args'][0])
        else:
            self.syntax_message(event['source']['nick'], '.load <module>')

    def reload(self, event):
        """Reloads a module specified from IRC.

        @param the irclib event object

        """

        if self.num_args == 1:
            # if module was successfully reloaded
            if self.module_handler.reload(event['args'][0].title()):
                # alert the user that reload was successful
                self.notice(event['source']['nick'], 
                    'Successfully reloaded module: %s' % event['args'][0])
                # re-register any triggers
                self.module_handler.modules[event['args'][0].title()]._register_triggers()
            else:
                # alert user that reload failed
                self.notice(event['source']['nick'], 
                    'Could not reload module: %s' % event['args'][0])
        else:
            
            self.syntax_message(event['source']['nick'], '.reload <module>')