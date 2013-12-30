from modules import *

import re
import urllib2
import traceback
try:
    import simplejson as json
except ImportError:
    import json

from unidecode import unidecode

from twitter import Twitter
from bitly import Bitly
from youtube import Youtube

class Urlparser(Module):
    """Checks incoming messages for possible urls.  If a url is found then
    route the url to a corresponding module to handle.

    """

    def __init__(self, *args, **kwargs):
        """Constructor."""

        Module.__init__(self, kwargs=kwargs)
        self.url_patterns = [
                Twitter,
                Youtube,
                Bitly,
                ]

        self.url_pattern = re.compile("http://(.*?)")

    def _register_events(self):
        self.add_event('pubmsg', 'parse_message')

    def parse_message(self, event):
        nick = event['nick']

        # make sure the message contains a url before checking
        # the other handlers patterns

        try:
            for handler in self.url_patterns:
                m = handler.pattern.search(event['message'])
                if m:
                    handler_instance = handler()
                    msg = handler_instance.handle(event=event, match=m)
                    if msg:
                        self.server.privmsg(event['target'], msg.encode('ascii', 'ignore'))
                        break
        except:
            print "<<Error>> in Urlparser (%s)" % (event['message'])
            print traceback.print_exc()

