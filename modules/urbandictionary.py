"""Looks up a term from urban dictionary
@package ppbot

@syntax ud <word>

"""
import requests
import json

from modules import *

class Urbandictionary(Module):

    def __init__(self, *args, **kwargs):
        """Constructor"""
        Module.__init__(self, kwargs=kwargs)
        self.url = "http://www.urbandictionary.com/iphone/search/define?term=%s"

    def _register_events(self):
        """Register module commands."""

        self.add_command('ud')

    def ud(self, event):
        """Action to react/respond to user calls."""

        if self.num_args >= 1:
            word = '%20'.join(event['args'])
            r = requests.get(self.url % (word))
            ur = json.loads(r.text)

            try:
                definition = ur['list'][0]
                definition['definition'] = definition['definition'].replace("\r", " ").replace("\n", " ")
                definition['example'] = definition['example'].replace("\r", " ").replace("\n", " ")
                message = "%(word)s (%(thumbs_up)d/%(thumbs_down)d): %(definition)s (ex: %(example)s)" % (definition)
                self.reply(message[:450])
            except (IndexError, KeyError) as e:
                self.reply('Could not find word "%s"' % ' '.join(event['args']))
        else:
            self.syntax_message(event['nick'], '.ud <word>')
