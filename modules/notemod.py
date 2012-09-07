"""Handles user notes
@package ppbot

@syntax tell <user> <note>
@syntax showtells
"""
from sqlalchemy import Column, Integer, String, Text, func, DateTime, Boolean
from sqlalchemy.sql import and_
from sqlalchemy.ext.declarative import declarative_base

from modules import *
from models import Model


Base = declarative_base()


class Note(Base, Model):
    __tablename__ = 'note_notes'

    id = Column(Integer, primary_key=True)
    note = Column(Text, nullable=False)
    added_by = Column(String(250), nullable=False)
    target = Column(String(250), nullable=False)
    time = Column(DateTime, default=func.now())
    active = Column(Boolean, default=True)

    def __init__(self, **kwargs):
        Model.__init__(self)
        Base.__init__(self)
        self.metadata = Base.metadata

        for name, val in kwargs.iteritems():
            self.__setattr__(name, val)

    def __repr__(self):
        return "<Note: %s To: %s> from: %s" % (self.note, self.target, self.added_by)

    def get(self, **kwargs):
        """Return a note by primary id."""

        return Model.session.query(Note).get(self.id)

    def inactive(self, **kwargs):
        self.active = False
        self.save()

    def find(self, nick, **kwargs):
        """Looks for notes for a person."""
        notes = Model.session.query(Note)
        notes = notes.filter(and_(Note.target.like("%s" % nick), Note.active == True))
        notes = notes.order_by(Note.time)

        return notes

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
            note = Note(note=' '.join(event['args'][1:]),
                    added_by=event['source'],
                    target=event['args'][0]
                    )

            note.save()

            self.notice(event['source'], '%s: Note added.' % (event['nick']))

    def parse_message(self, event):
        """ Checks to see if user has notes waiting for them """

        notes = Note().find(event['nick']).all()
        if len(notes) > 0:
            for note in notes:
                n = Note(id=note.id)
                self.notice(event['nick'], '%s told you some time ago: %s' % (note.added_by.split('!')[0], note.note))
                note.inactive()

