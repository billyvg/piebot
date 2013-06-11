"""Google search
@package ppbot

Returns the first google search result

@syntax g <search terms>

"""
import requests
import json

from modules import *

class Search(Module):


    def __init__(self, *args, **kwargs):
        """Constructor"""

        Module.__init__(self, kwargs=kwargs)

        self.url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&safe=off&q=%s"

    def _register_events(self):
        """Register module commands."""

        self.add_command('g', 'search')

    def search(self, event):
        """Action to react/respond to user calls."""

        # need to fetch the weather and parse it
        search_term = "%20".join(event['args'])
        try:
            results = self.ajax_search(search_term)
            # stylize the message output
            message = "%(titleNoFormatting)s - %(content)s - %(url)s" % (results)
            # send the messages
            self.msg(event['target'], message.encode('ascii', 'ignore'))
        except:
            import traceback
            print "Failed to search for %s - %s" % (search_term, results)
            traceback.print_exc()


    def ajax_search(self, term):
        """Connects to google's ajax search api to perform a search."""

        # make the parser, and send the xml to be parsed
        result = requests.get(self.url % term)
        search = json.loads(result.text)
        return search['responseData']['results'][0]
