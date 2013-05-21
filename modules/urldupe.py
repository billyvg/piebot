"""Checks if someone has posted a link already and yells at them.
@package ppbot

"""
import re
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from modules import *
from db import db

class Urldupe(Module):

    def __init__(self, *args, **kwargs):
        """Constructor"""

        Module.__init__(self, kwargs=kwargs)

        self.url_pattern = re.compile('http://[^ #]+')

    def _register_events(self):
        self.add_event('pubmsg', 'urldupe')

    def get_dupes(self, url, username, channel):
        """Checks if there is a dupe url already"""

        return self.db.urls.find({
            'url': url,
            'channel': channel,
            'username': {
                '$neq': username
            }
        })

    def save_url(self, url, username, channel):
        data = {'url': url,
                'username': username,
                'channel': channel,
                'time': datetime.now()}
        self.db.urls.insert(data)

    def urldupe(self, event):
        """Action to react/respond to chat messages."""

        m = self.url_pattern.search(event['message'])

        if m:
            match = m.group(0).rstrip('/')
            # check if this url has been posted before
            dupes = self.get_dupes(match, event['nick'], event['target'])

            if dupes.count() == 1:
                rd = relativedelta(datetime.now(), dupes[0].time)
                message = "%s: That url was already linked by %s %s ago." % (
                        event['nick'],
                        dupes[0].username,
                        self.pretty_time_duration(rd)
                        )
                self.msg(event['target'], message)
            elif dupes.count() > 1:
                rd = relativedelta(datetime.now(), dupes[0].time)
                message = ("%s: That url has been linked %d times already"
                            " (first linked by \x02%s\x02 %s ago).") % (
                        event['nick'],
                        dupes.count(),
                        dupes[0].username,
                        self.pretty_time_duration(rd)
                        )
                self.msg(event['target'], message)

            # add to database
            self.save_url(match, event['nick'], event['target'])

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
