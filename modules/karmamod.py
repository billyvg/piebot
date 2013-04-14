"""Keeps track of karma counts.
@package ppbot

@syntax .karma <item>
"""
import re

from modules import *
from models import Model

class Karmamod(Module):

    def __init__(self, *args, **kwargs):
        """Constructor"""

        Module.__init__(self, kwargs=kwargs)

    def _register_events(self):
        self.add_command('karma', 'get_karma')
        self.add_event('pubmsg', 'parsekarma')

    @op
    def get_karma(self, event):
        karma = self.db.karma.find_one({'name': event['args'][0],
            'source': event['target']})
        try:
            result = karma['count']
        except KeyError:
            result = 0

        self.msg(event['target'], '%s has %d karma.' % (event['args'][0], result))

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

        karma = self.db.karma.find_one({'name': name,
            'source': event['target']})
        # TODO: find way to insert if doesn't exist or else update?
        try:
            count = karma['count'] + value
            self.db.karma.update({'name': name,
                'source': event['target']},
                {'count': count})
        except TypeError, KeyError:
            count = value
            self.db.karma.insert({'name': name,
                'source': event['target'],
                'count': count})
