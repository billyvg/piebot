"""Stock ticker module for ppbot.
@package ppbot

Given a stock symbol, will lookup the current trading price.
Uses Google's Finance API

@syntax stock <symbol>

"""
import urllib2
import string
import json
from xml.dom.minidom import parseString

from modules import *

class Stock(Module):

    def __init__(self, *args, **kwargs):
        """Constructor"""

        Module.__init__(self, kwargs=kwargs)

        self.url = "http://www.google.com/finance/info?infotype=infoquoteall&q=%s"

    def _register_events(self):
        """Register module commands."""

        self.add_command('stock')

    def stock(self, event):
        """Action to react/respond to user calls."""

        if self.num_args == 1:
            # need to fetch the weather and parse it
            symbol = event['args'][0]
            try:
                stock_info = self.lookup_symbol(symbol)
                # stylize the message output
                try:
                    change = float(stock_info['ecp'])
                except:
                    change = float(stock_info['cp'])
                if change > 0:
                    color = "\x033"
                elif change < 0:
                    color = "\x034"
                else:
                    color = ""
                stock_info['color'] = color
		try:
                    message1 = "%(name)s (%(e)s:%(t)s) - %(el)s (%(color)s%(ec)s\x0f,%(color)s %(ecp)s%%\x0f) - 52week high/low: (%(hi52)s/%(lo52)s) - MktCap: %(mc)s - P/E: %(pe)s" % (stock_info)
                except:
                    message1 = "%(name)s (%(e)s:%(t)s) - %(l)s (%(color)s%(c)s\x0f,%(color)s %(cp)s%%\x0f) - 52week high/low: (%(hi52)s/%(lo52)s) - MktCap: %(mc)s - P/E: %(pe)s" % (stock_info)
                # send the messages
                self.reply(message1)
            except:
                self.reply('Could not find symbol "%s"' % symbol)
                import traceback
                traceback.print_exc()
        else:
            self.syntax_message(event['nick'], '.stock <symbol>')


    def lookup_symbol(self, symbol):
        """Connects to google's secret finance API and parses the receiving json for the stock info."""

        # make the parser, and send the xml to be parsed
        result = urllib2.urlopen(self.url % symbol).read()
        stock = json.loads(result[4:])
        return stock[0]
