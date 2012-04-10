"""Handles a quote database
@package ppbot

@syntax quote <add/del/search> <nick/quote>
"""
from sqlalchemy import Column, Integer, String, Text, func, DateTime
from sqlalchemy.ext.declarative import declarative_base

from modules import *
from models import Model


Base = declarative_base()


class Quote(Base, Model):
    __tablename__ = 'quote_quotes'

    id = Column(Integer, primary_key=True)
    quote = Column(Text, nullable=False)
    added_by = Column(String(250), nullable=False)
    source = Column(String(250), nullable=False)
    time = Column(DateTime, default=func.now())
    nickname = Column(String(250), nullable=True)

    def __init__(self, **kwargs):
        Model.__init__(self)
        Base.__init__(self)
        self.metadata = Base.metadata

        for name, val in kwargs.iteritems():
            self.__setattr__(name, val)

    def __repr__(self):
        return "<Quote: %s, %s, %s> added by: %s" % (self.quote, self.nickname, self.source, self.added_by)

    def get(self, **kwargs):
        """Return a quote by primary id."""

        return self.session.query(Quote).get(self.id)

    def find(self, term, **kwargs):
        """Looks for a quote."""

        return self.session.query(Quote).filter(
                Quote.quote.like("%%%s%%" % term)
                ).order_by(Quote.time)


class Quotemod(Module):

    def __init__(self, *args, **kwargs):
        """Constructor"""

        Module.__init__(self, kwargs=kwargs)

    def _register_events(self):
        self.add_command('quote', 'subcommand')

    def subcommand(self, event):
        """ temporary, will refactor into Module later on. """

        try:
            getattr(self, event['args'][0])(event)
        except:
            import traceback
            traceback.print_exc()

    def add(self, event):
        """Adds a new quote."""

        quote = Quote(quote=' '.join(event['args'][1:]),
                added_by=event['source'],
                source=event['target']
                )

        quote.save()

        self.msg(event['target'], 'Quote added.')

    def delete(self, event):
        """Deletes a quote by id."""

        quote = Quote(id=event['args'][0])
        quote.delete()

        self.msg(event['target'], 'Quote deleted.')

    def search(self, event):
        quotes = Quote().find(' '.join(event['args'][1:-1]))
        print quotes
        print quotes.count()
