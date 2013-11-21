"""Bitccoin ticker module for ppbot.
@package ppbot

Displays the current bitcoin pricing from mtgox

@syntax btc

"""
import requests
import string
import json
from xml.dom.minidom import parseString

from modules import *

class Bitcoin(Module):

    def __init__(self, *args, **kwargs):
        """Constructor"""

        Module.__init__(self, kwargs=kwargs)

        self.url = "http://data.mtgox.com/api/1/BTCUSD/ticker"

    def _register_events(self):
        """Register module commands."""

        self.add_command('btc')

    def btc(self, event):
        """Action to react/respond to user calls."""

        data = {}

        try:
            result = self.lookup()['return']
            data['high'] = result['high']['display_short']
            data['last'] = result['last_local']['display_short']
            data['low'] = result['low']['display_short']
            data['volume'] = result['vol']['display_short']
            
            message = "Last: %(last)s - High/Low: (%(high)s/%(low)s) - Volume: %(volume)s" % (data)
            self.msg(event['target'], message)

        except:
            pass
        
    def lookup(self):
        """Connects to google's secret finance API and parses the receiving json for the stock info."""

        # make the parser, and send the xml to be parsed
        result = requests.get(self.url)
        return result.json()
