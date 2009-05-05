"""eventhandler.py
@package ppbot

"""

import inspect
import sys

class ModuleHandler:
    """Class to handle modules: loading, reloading, unloading, autoloading"""

    def __init__(self, server):
        """Constructor
        
        @param the irclib server object
        
        """

        self.server = server
        self.modules = {}
        self.triggers = {}
        
    def message_handler(self, connection, event):
        """Handles incoming messages, parses them before sending to a 
        module.
        
        @param an irclib connection object
        @param an irclib event
        
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
            
    def trigger(self, trigger):
        """Adds a trigger mapping to our trigger dictionary.
        
        @param the trigger string
        
        """
        
        if trigger in self.triggers:
            return self.triggers[trigger]
        else:
            return None

    def load(self, name, class_name=None):
        """Loads a module.
        
        @param name of the module
        @param <optional> name of the class
        
        """
        
        if not class_name:
            class_name = name
        structured_name = 'modules.' + name.lower() + '.' + class_name
        component_names = structured_name.split('.')
        #try:
        mod = __import__('.'.join(component_names[:-1]))
        #except:
        #    print "Error importing module: %s" % name
            
        #try:
        for component_name in component_names[1:]:
            mod = getattr(mod, component_name)
        module = mod(self.server)
        self.modules[name] = module
        print "Added module: %s" % name
        for trigger, action in module.triggers.iteritems():
            self.triggers[trigger] = name
            print "Adding trigger: %s" % trigger
        return module
        #except:
         #   print "Error instanciating class/module"
        #    return None

    def reload(self, module):
        """Reloads a module.
        
        @param module name
        
        """
        
        # we can't reload the core module because we set the module_handler
        # when we first load it, and I can't think of a way to reset it
        # maybe find a way to save the instance of the module_handler and 
        # then reload it.
        if module is not 'Core':
            try:
                reload(sys.modules[self.modules[module].__module__])
                print "Reloaded module: %s" % module
                mod = getattr(sys.modules[self.modules[module].__module__], module)
                m = mod(self.server)
                self.modules[module] = m
                return True
            except:
                print "Could not reload module: %s" % module
                return False
        