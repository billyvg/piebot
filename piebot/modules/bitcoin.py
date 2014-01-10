"""Bitccoin ticker module for ppbot.
@package ppbot

Displays the current bitcoin pricing from several exchanges via bitcoincharts

@syntax btc

"""
import requests

from piebot.modules import *

class Bitcoin(Module):

    def __init__(self, *args, **kwargs):
        """Constructor"""

        Module.__init__(self, kwargs=kwargs)

        self.tracked = ['mtgoxUSD', 'btceUSD', 'bitstampUSD']
        self.url = 'http://api.bitcoincharts.com/v1/markets.json'

    def _register_events(self):
        """Register module commands."""

        self.add_command('btc')

    def btc(self, event):
        """Action to react/respond to user calls."""

        data = {}

        try:
            data = self.lookup()
            relevant = [d for d in data if d.get('symbol') in self.tracked]
            output = ""
            for exchange in relevant:
                output += "%s last: %d, vol: %0.2f, high: %d, low: %d | " % (
                        exchange.get('symbol'),
                        exchange.get('bid'),
                        exchange.get('volume'),
                        exchange.get('high'),
                        exchange.get('low'))

                self.reply(output[:-3])

        except:
            pass

    def lookup(self):
        """Connects to API and parses the receiving json for the stock info."""

        result = requests.get(self.url)
        return result.json()
