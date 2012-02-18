"""Looks up a movie from rottentomatoes.com
@package ppbot

@syntax rt <movie>

"""
import urllib

import requests
import json

from config import BotConfig
from modules import *

class Rottentomatoes(Module):
    API_URL = 'http://api.rottentomatoes.com/api/public/v1.0/movies.json?%s'

    def __init__(self, *args, **kwargs):
        """Constructor"""
        Module.__init__(self, kwargs=kwargs)
        self.api_key = BotConfig().get('rt', 'api_key')

    def _register_events(self):
        """Register module commands."""

        self.add_command('rt')

    def rt(self, event):
        """Action to react/respond to user calls."""

        term = ' '.join(event['args'])
        params = urllib.urlencode({'q': term, 'apikey': self.api_key})
        r = requests.get(self.__class__.API_URL % (params))
        resp = json.loads(r.text)

        print resp
        try:
            result = resp['movies'][0]
            result.setdefault('critics_consensus', result['synopsis'])
            cast = ', '.join([x['name'] for x in result['abridged_cast'][0:2]])
            message = '%s (%d) - rating: %d%%, %d%% - length: %dmins - theater: %s - starring: %s - http://www.rottentomatoes.com/m/%s' % (
                    result['title'],
                    result['year'],
                    result['ratings']['critics_score'],
                    result['ratings']['audience_score'],
                    result['runtime'],
                    result['release_dates']['theater'],
                    cast,
                    result['id']
                    )
            self.msg(event['target'], message)
            self.msg(event['target'], '[synopsis] %s' % (result['critics_consensus']))
        except KeyError:
            self.msg(event['target'], 'Could not find "%s" on rottentomatoes.com' % term)
