"""Primecoin ticker module for ppbot.
@package ppbot

Displays the current primecoin pricing from btc-e.

@syntax xpm

"""
import requests

from piebot.modules import *


class Primecoin(Module):

    def __init__(self, *args, **kwargs):
        """Constructor"""

        Module.__init__(self, kwargs=kwargs)

        self.url = 'https://btc-e.com/api/2/xpm_btc/ticker'

    def _register_events(self):
        """Register module commands."""

        self.add_command('xpm')

    def xpm(self, event):
        """Action to react/respond to user calls."""

        data = {}

        try:
            data = self.lookup()
            ticker = data.get('ticker')
            output = "[btc-e]"
            output += " last: \x02%0.2f\x02 mBTC (%0.2f/%0.2f)" % (
                ticker.get('last')*1000,
                ticker.get('high')*1000,
                ticker.get('low')*1000)
            output += ", vol: %0.2f XPM (%0.2f BTC)" % (
                ticker.get('vol_cur'), ticker.get('vol'))
            self.reply(output)

        except:
            pass

    def lookup(self):
        """Connects to API and parses the receiving json for the stock info."""

        result = requests.get(self.url)
        return result.json()
