"""modulehandler.py
@package ppbot

"""

import inspect
import traceback
import sys

from modules import Module
from handlers import Handler

class ModuleHandler(Handler):
    """Class to handle modules: loading, reloading, unloading, autoloading"""

    def __init__(self, server):
        """Constructor
        
        @param the irclib server object
        
        """

        self.server = server
        self.modules = {}
        self.commands = {}
        self.events = {}

    def load(self, name, class_name=None):
        """Loads a module.
        
        @param name of the module
        @param <optional> name of the class
        
        """
        
        if not class_name:
            class_name = name
        # create a string in the form of "modules.<module name>.<class name>"
        structured_name = 'modules.' + name.lower() + '.' + class_name
        # split the structured name into different components
        component_names = structured_name.split('.')
        try:
            # try to import the module "modules.<module name>"
            mod = __import__('.'.join(component_names[:-1]))
        except:
            print "Error importing module: %s" % name
            print traceback.print_exc()
            
        try:
            for component_name in component_names[1:]:
                mod = getattr(mod, component_name)
            module = mod(self.server)
            # keep a dictionary of modules, with the module name as the key
            self.modules[name] = module
            
            print "Added module: %s" % name
            
            # go through the module's commands list and keep a list of the commands
            # so that the message handler knows how to route the commnands
            for command, action in module.commands.iteritems():
                # define a commands dict that has a key of the command name and 
                # value of the name of the x that holds the command
                self.commands[command] = name
                
            # also do something similar for events
            for event_type, action in module.events.iteritems():
                try: 
                    self.events[event_type][action] = name
                except:
                    self.events[event_type] = {action: name}
                
            return module
        except:
            print "Error instanciating class/module"
            print traceback.print_exc()
            return None

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
                print traceback.print_exc()
                return False
