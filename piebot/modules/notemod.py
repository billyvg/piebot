"""Handles user notes
@package ppbot

@syntax tell <user> <note>
@syntax showtells
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta

from modules import *

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
            self.reply_notice('Note added for %s.' % (event['args'][0]))

    def parse_message(self, event):
        """ Checks to see if user has notes waiting for them """

        notes = self.db.notes.find({'target': event['nick'].lower(), 'active': True}).sort('time', 0)
        if notes.count() > 0:
            for note in notes:
                rd = relativedelta(datetime.now(), note['time'])
                self.reply_notice('%s said to you %s ago: "%s"' % (note['added_by'].split('!')[0], self.pretty_time_duration(rd), note['note'].encode('ascii', 'ignore')))
                self.db.notes.update({'_id': note['_id']}, {'$set': {'active': False}})

    def pretty_time_duration(self, rd):
        """Formats the time difference in a pretty string"""
        output = ''
        delta = {'years': rd.years,
                 'months': rd.months,
                 'days': rd.days,
                 'hours': rd.hours,
                 'minutes': rd.minutes,
                 'seconds': rd.seconds}

        if rd.years > 1:
            output += '%(years)d years '
        elif rd.years > 0:
            output += '%(years)d year '
        elif rd.months > 1:
            output += '%(months)d months '
        elif rd.months > 0:
            output += '%(months)d month '
        elif rd.days > 1:
            output += '%(days)d days '
        elif rd.days > 0:
            output += '%(days)d day '
        elif rd.hours > 1:
            output += '%(hours)d hours '
        elif rd.hours > 0:
            output += '%(hours)d hour '
        elif rd.minutes > 1:
            output += '%(minutes)d minutes '
        elif rd.minutes > 0:
            output += '%(minutes)d minute '
        elif rd.seconds > 1:
            output += '%(seconds)d seconds '
        elif rd.seconds > 0:
            output += '%(seconds)d second '

        return output.strip() % delta
