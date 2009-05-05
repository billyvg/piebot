"""eventhandler.py
@package piebot

"""

class EventHandler:
    """Class to handle events.  So far just message handling."""

    def __init__(self, server):
        self.server = server

    def message_handler(self, connection, event):
        """Handles incoming messages, parses them before sending to a 
        module.

        """

        module_args = {}
        source = {}
        # parse the event
        # target is who (private message) or what (channel) the event is directed towards
        target = event.target()
        # source is where the event came from
        the_source = event.source()
        # the nickname of the person who sent the message
        source['nick'] = the_source.split('!')[0]
        source['ident'] = the_source.split('!')[1].split('@')[0]
        source['hostname'] = the_source.split('!')[1].split('@')[1]

        # get the entire message and split it by spaces
        args = event.arguments()[0].split(' ')
        # this is the first part of the message, which will be the command
        command = args.pop(0)[1:]
        # the number of arguments -- the rest of the message string after the command
        num_args = len(args)

        # make a dictionary for all the arguments we send to the module's handle method
        module_args['command'] = command
        module_args['args'] = args
        module_args['target'] = target
        module_args['source'] = source
        module_args['connection'] = connection

        # check to see if a trigger was called
        called_module = self.trigger(command)
        if called_module:
            self.modules[called_module].handle(module_args)