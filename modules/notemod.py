"""Handles user notes
@package ppbot

@syntax tell <user> <note>
@syntax showtells
"""
from datetime import datetime

from modules import *
from models import Model

class Notemod(Module):

    def __init__(self, *args, **kwargs):
        """Constructor"""

        Module.__init__(self, kwargs=kwargs)

    def _register_events(self):
        self.add_command('tell')
        self.add_event('pubmsg', 'parse_message')

    def tell(self, event):
        """Adds a new tell."""

        if event['nick'] != event['args'][0]:
            data = {'note': ' '.join(event['args'][1:]),
                    'added_by': event['source'],
                    'time': datetime.now(),
                    'active': True,
                    'target': event['args'][0].lower()}
            self.db.notes.insert(data)
            self.notice(event['nick'], 'Note added for %s.' % (event['args'][0]))

    def parse_message(self, event):
        """ Checks to see if user has notes waiting for them """

        notes = self.db.notes.find({'target': event['nick'].lower(), 'active': True}).sort('time', 0)
        if notes.count() > 0:
            for note in notes:
                self.notice(event['nick'], '%s told you some time ago: %s' % (note['added_by'].split('!')[0], note['note'].encode('ascii', 'ignore')))
                self.db.notes.update({'_id': note['_id']}, {'$set': {'active': False}})


