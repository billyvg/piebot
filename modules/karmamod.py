"""Keeps track of karma counts.
@package ppbot

@syntax .karma <item>
"""
import re

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

from modules import *
from models import Model

Base = declarative_base()


class Karma(Base, Model):
    __tablename__ = 'karma_karmas'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    source = Column(String(50), nullable=False)
    count = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        Model.__init__(self)
        Base.__init__(self)
        self.metadata = Base.metadata

        for name, val in kwargs.iteritems():
            self.__setattr__(name, val)

    def __repr__(self):
        return "<Karma: %s=%s>" % (self.name, self.count)

    def get(self, **kwargs):
        return Model.session.query(Karma).filter_by(
                name=self.name, source=self.source
                )

    def change_karma(self, val, **kwargs):
        try:
            if self.get().count() > 0:
                self.get().update({Karma.count: Karma.count + self.count})
                Model.session.commit()
            else:
                self.save()
        except:
            pass


class Karmamod(Module):

    def __init__(self, *args, **kwargs):
        """Constructor"""

        Module.__init__(self, kwargs=kwargs)

    def _register_events(self):
        self.add_command('karma', 'get_karma')
        self.add_event('pubmsg', 'parsekarma')

    def get_karma(self, event):
        karma = Karma(name=event['args'][0], source=event['target'])
        try:
            result = karma.get().one().count
        except NoResultFound:
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

        karma = Karma(name=name, source=event['target'], count=value)
        karma.change_karma(value)
