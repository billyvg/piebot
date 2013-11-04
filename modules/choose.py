"""

If you're just lost in life and need something to make a choice for you.
Ask our beloved dongbot!

By Lucas/Mezmor

@syntax .c <comma delimited list>

"""

from modules import Module
from random import choice

class Choose(Module):

    def __init__(self, *args, **kwargs):
        """Constructor"""
        Module.__init__(self, kwargs=kwargs)
        
    def _register_events(self):
        """Register module commands."""

        self.add_command('c', 'choose')
    
    def choose(self, event):
        # Make that bitch a one-liner
        # Bitches love one-liners
        # - Sentinel, Oct 28 2013
        self.msg(event['target'], event['nick'] + ": " + choice([item.strip() for item in event['args'].split(",") if item.strip()]))
