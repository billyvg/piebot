"""module.py
@package ppbot

Module for our bot's modules.  Contains the base module class.
"""
import traceback
from db import db

# define some decorators here, to be used by modules for access control
def access(*a, **kw):
    def check_access(f, *args, **kwargs):
        def new_f(*args, **kwargs):
            try:
                # query the database to check to see if the user is a master or owner
                #query = session.query(User).filter(User.name == args[1]['nick'])
                #user = query.first()
                pass
            except Exception, e:
                print "query error: ", e
            # check to see if we receive a result from the database and that
            # their access level meets the minimum access level
            else:
                pass
                #if user and user.access >= a[0]:
                    #return f(*args, **kwargs)
        new_f.func_name = f.func_name
        return new_f
    return check_access

# shortcut decorators for some main access levels
levels = db.access_levels.find().sort('level', 1)

# here's a hack to dynamically generate decorators from access levels
# that are defined in the database.
level_lambdas = {}
def decorator_generator():
    def hack(i): level_lambdas[i['name']] = lambda f: access(i['level'])(f)
    return [hack(i) for i in levels]

decorator_generator()
for f in level_lambdas:
    vars()[f] = level_lambdas[f]


def command(f):
    """Decorator to add the method as a command."""
    def new(*args, **kwargs):
        module = getattr(sys.modules[f.__module__], 'Module')
        return f(*args, **kwargs)
    return new


class ModuleCollection:
    def __init__(self, className):
        self.className = className

    def __getattr__(self, name):
        _name = u"module_%s_%s" % (self.className, name)
        return db[_name]


class Module:
    """The base module class where all of our modules will be derived from."""
    #commands = {}

    def __init__(self, *args, **kwargs):
        #self.server = server
        # server object from irclib
        # events dict that is created via irclib on each irc event
        self.events = {}
        # dict of commands that the module has registered
        self.commands = {}
        self.http_routes = {}
        self.num_args = 0
        self._register_events()
        self.irc = kwargs['kwargs']['irc']
        self.db = ModuleCollection(self.__class__.__name__)

    def _register_events(self):
        """Registers an event so that the eventhandler can pass the module
        the required data.

        """
        pass

    def add_event(self, event_type, action):
        """Registers an event with the event handler."""

        self.events[event_type] = action

    def add_command(self, command, action=None, event_type='allmsg'):
        """Register a command.

        If action is None, then the default action will be the command name.
        @param command      A string that will be used as the command
        @param action       The corresponding function that will be called in the module when
                            a command is received from IRC.
        @param event_type   In this helper, the event_type will be the different message mediums
                            that the bot will respond to a command.  Default: 'allmsg'
                            Available: 'allmsg', 'privmsg', 'pubmsg', 'privnotice', 'pubnotice'
        """

        if not action:
            action = command

        self.commands[command] = action

    def add_http_route(self, handler, **kwargs):
        """Adds an http route for module"""

        try:
            route_name = kwargs['name']
        except KeyError:
            route_name = self.__class__.__name__.lower()
        try:
            methods = kwargs['methods']
        except KeyError:
            methods = ['GET', 'POST']

        self.http_routes[route_name] = {'handler': handler, 'methods': methods}

    def handle(self, action, event):
        """Calls the function that a command was bound to."""

        self.server = event['connection']
        # set the number of arguments
        self.num_args = event['num_args']

        try:
            call_func = getattr(self, action)
            call_func(event)
        except:
            # print out traceback if something wrong happens in the module
            print traceback.print_exc()

    def handle_command(self, event):
        """Calls the function that a command was bound to."""

        self.server = event['connection']
        # set the number of arguments
        self.num_args = event['num_args']
        command = event['command']

        try:
            call_func = getattr(self, self.commands[command])
            call_func(event)
        except:
            # print out traceback if something wrong happens in the module
            print traceback.print_exc()

    def syntax_message(self, target, syntax):
        """Sends the target the correct syntax of a command."""

        message = "syntax: %s" % syntax
        self.server.notice(target, message)

    def notice(self, target, message):
        """Gives modules the ability to send a notice to a user."""

        self.server.notice(target, message)

    def msg(self, target, message):
        """Gives modules the ability to send a message to a user/channel."""

        self.server.privmsg(target, message)

    def bold(self, message):
        """Helper function to bold a message."""

        return "\x02%s\x02" % message
