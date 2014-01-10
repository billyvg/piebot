"""Looks up a term from wikipedia
@package ppbot

@syntax wiki <word>

"""
import requests
import json

from modules import *

import wikipedia

class Wikipediamod(Module):

    def __init__(self, *args, **kwargs):
        """Constructor"""
        Module.__init__(self, kwargs=kwargs)

    def _register_events(self):
        """Register module commands."""

        self.add_command('wiki')

    def wiki(self, event):
        """Action to react/respond to user calls."""

        if self.num_args >= 1:
            word = ' '.join(event['args'])

            try:
				page = wikipedia.page(word)
				self.reply("%s... (%s)" % (page.summary[:390], page.url))
            except:
				import traceback
				traceback.print_exc()
				self.reply_notice('Could not find entry for "%s"' % ' '.join(event['args']))
        else:
			self.syntax_message(event['nick'], '.wiki <word>')
