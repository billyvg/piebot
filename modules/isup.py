"""Checks isup.me to see if a website is up
@package ppbot

@syntax isup <word>

"""
import requests
import re

from modules import *

class Isup(Module):


    def __init__(self, *args, **kwargs):
        """Constructor"""
        Module.__init__(self, kwargs=kwargs)
        self.url = "http://www.isup.me/%s"

    def _register_events(self):
        """Register module commands."""

        self.add_command('isup')

    def isup(self, event):
        """Action to react/respond to user calls."""

        if self.num_args == 1:
            domain = event['args'][0]

            try:
                r = requests.get(self.url % (domain))
                if re.search('Is Down ->', r.text):
                    message = "%s is DOWN" % domain
                else:
                    message = "%s is UP" % domain

                self.msg(event['target'], message)
            except:
                import traceback
                traceback.print_exc()
                self.msg(event['target'], 'Problem looking up "%s"' % domain)
        else:
            pass
