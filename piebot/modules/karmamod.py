"""Keeps track of karma counts.
@package ppbot

@syntax .karma <item>
"""
import re

from piebot.modules import *

class Karmamod(Module):

    def __init__(self, *args, **kwargs):
        """Constructor"""

        Module.__init__(self, kwargs=kwargs)

    def _register_events(self):
        self.add_command('karma', 'get_karma')
        self.add_event('pubmsg', 'parsekarma')

    @op
    def get_karma(self, event):
        karma = self.db.karma.find_one({'name': event['args'][0].lower(),
            'source': event['target']})
        try:
            result = karma['count']
            self.reply('%s has %d karma.' % (event['args'][0], result))
        except KeyError, TypeError:
            result = 0

    def parsekarma(self, event):
        inc_pattern = re.compile('([^ ]{2,})\+\+')
        m = inc_pattern.findall(event['message'])
        for term in m:
            self.change(event, term, 1)
        dec_pattern = re.compile('([^ ]{2,})--')
        m = dec_pattern.findall(event['message'])
        for term in m:
            self.change(event, term, -1)

    def change(self, event, name, value):
        """Change karma count."""

        self.db.karma.update({
            'name': name.lower(),
            'source': event['target']
        }, {
            '$inc': {
                'count': 1
            }
        }, True)
