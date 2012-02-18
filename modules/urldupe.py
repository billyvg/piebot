"""Checks if someone has posted a link already and yells at them.
@package ppbot

"""
import re
from datetime import datetime

from dateutil.relativedelta import relativedelta

from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.ext.declarative import declarative_base

from modules import *
from models import Model

Base = declarative_base()


class Url(Base, Model):
    __tablename__ = 'urldupe_urls'

    id = Column(Integer, primary_key=True)
    url = Column(Text, nullable=False)
    time = Column(DateTime, default=func.now())
    username = Column(String(50), nullable=False)
    channel = Column(String(50), nullable=False)

    def __init__(self, **kwargs):
        Model.__init__(self)
        Base.__init__(self)
        self.metadata = Base.metadata

        for name, val in kwargs.iteritems():
            self.__setattr__(name, val)

    def __repr__(self):
        return "<Url: %s, %s, %s>" % (self.url, self.username, self.channel)

    def get_dupes(self, **kwargs):
        """Checks if URL is in the database."""

        return self.session.query(Url).filter_by(
                    url=self.url, channel=self.channel
                ).order_by(Url.time).all()


class Urldupe(Module):

    def __init__(self, *args, **kwargs):
        """Constructor"""

        Module.__init__(self, kwargs=kwargs)

        self.url_pattern = re.compile('http://[^ ]+')

    def _register_events(self):
        self.add_event('pubmsg', 'urldupe')

    def urldupe(self, event):
        """Action to react/respond to chat messages."""

        m = self.url_pattern.search(event['message'])

        if m:
            # check if this url has been posted before
            url = Url(
                url=m.group(0),
                username=event['nick'],
                channel=event['target']
            )
            dupes = url.get_dupes()

            num_dupes = len(dupes)
            if num_dupes == 1:
                rd = relativedelta(datetime.now(), dupes[0].time)
                message = "%s: That url was already linked by %s %s ago." % (
                        event['nick'],
                        dupes[0].username,
                        self.pretty_time_duration(rd)
                        )
                self.msg(event['target'], message)
            elif num_dupes > 1:
                rd = relativedelta(datetime.now(), dupes[0].time)
                message = ("%s: That url has been linked %d times already"
                            " (first linked by \x02%s\x02 %s ago).") % (
                        event['nick'],
                        num_dupes,
                        dupes[0].username,
                        self.pretty_time_duration(rd)
                        )
                self.msg(event['target'], message)

            # add to database
            url.save()

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
