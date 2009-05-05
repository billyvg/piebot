"""module.py
@package ppbot

Module for our bot's modules.  Contains the base module class.

TODO: Need some methods for user management so that modules can use decorators.
"""

from user import *

# define some decorators here, to be used by modules for access control
def access(f, access):
    def new_f(*args, **kwargs):
        print 'calling %s' % f.__name__
        print args
        print kwargs
        return f(*args, **kwargs)
    return new_f
    
# shortcut decorators for some main access levels
def user(f):
    pass

def master(f):
    def new_f(*args, **kwargs):
        session = Session()
        try:
            # query the database to check to see if the user is a master or owner
            query = session.query(User).filter(User.name == args[1]['source']['nick'])
            user = query.first()
        except Exception, e:
            print e
        # check to see if we receive a result from the database and that
        # their access level is at least master status
        if user and user.access >= Access.master.index:
            return f(*args, **kwargs)
    return new_f
    
def owner(f):
    pass
    
class Module:
    """The base module class where all of our modules will be derived from."""

    def __init__(self, server):
        self.server = server
        self.triggers = {}
        self.num_args = 0
        self._register_triggers()
        
    def add_trigger(self, trigger, action=None):
        """Register a trigger.  
        
        If action is None, then the default action will be the trigger name.
        
        """
        
        if not action:
            action = trigger
        self.triggers[trigger] = action

    def handle(self, event):
        """Calls the function that a trigger was bound to."""

        # set the number of arguments
        self.num_args = len(event['args'])

        command = event['command']
        if command in self.triggers:
            if hasattr(self, self.triggers[command]):
                call_func = getattr(self, self.triggers[command])
                call_func(event)

    def syntax_message(self, target, syntax):
        """Sends the target the correct syntax of a trigger."""

        message = "syntax: %s" % syntax
        self.server.notice(target, message)
        
    def notice(self, target, message):
        """Gives modules the ability to send a notice to a user."""
        
        self.server.notice(target, message)
        
    def msg(self, target, message):
        """Gives modules the ability to send a message to a user/channel."""

        self.server.privmsg(target, message)
    
