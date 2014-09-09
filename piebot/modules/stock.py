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

from piebot.modules import *

class Stock(Module):

    def __init__(self, *args, **kwargs):
        """Constructor"""

        Module.__init__(self, kwargs=kwargs)

        self.url = "http://www.google.com/finance/info?infotype=infoquoteall&q=%s"

    def _register_events(self):
        """Register module commands."""

        self.add_command('stock')
        self.add_event('pubmsg', 'parse_message')

    def stock(self, event):
        """Action to react/respond to user calls."""

        if self.num_args == 1:
            # need to fetch the weather and parse it
            symbol = event['args'][0]

            try:
                self.reply(self.lookup_symbol(symbol))
            except:
                self.reply('Could not find symbol "%s"' % symbol)
                import traceback
                traceback.print_exc()
        else:
            self.syntax_message(event['nick'], '.stock <symbol>')

    def parse_message(self, event):
        match = re.search('\$([a-zA-Z]{2,10})', event['message'])

        if match:
            try:
                self.reply(self.lookup_symbol(match.group(1)))
            except:
                pass


    def lookup_symbol(self, symbol):
        """Given a stock symbol, returns a formatted string to be displayed"""

        stock_info = self.request_symbol(symbol)
        # stylize the message output
        change = float(stock_info['cp'])
        color = "\x033" if change > 0 else "\x034" if change < 0 else ""
        stock_info['color'] = color

        try:
            ah_change = float(stock_info['ecp'])
            color = "\x033" if ah_change > 0 else "\x034" if ah_change < 0 else ""
            stock_info['ah_color'] = color
            stock_info['afterhours'] = "%(el)s (%(ah_color)s%(ec)s\x0f,%(ah_color)s %(ecp)s%%\x0f)" % stock_info
        except KeyError:
            pass

        try:
            message1 = "%(name)s (%(e)s:%(t)s) - Now: %(afterhours)s - Today: %(l)s (%(color)s%(c)s\x0f,%(color)s %(cp)s%%\x0f) - 52week high/low: (%(hi52)s/%(lo52)s) - MktCap: %(mc)s - P/E: %(pe)s" % (stock_info)
        except:
            message1 = "%(name)s (%(e)s:%(t)s) - %(l)s (%(color)s%(c)s\x0f,%(color)s %(cp)s%%\x0f) - 52week high/low: (%(hi52)s/%(lo52)s) - MktCap: %(mc)s - P/E: %(pe)s" % (stock_info)

        return message1

    def request_symbol(self, symbol):
        """Connects to google's secret finance API and parses the receiving json for the stock info."""

        # make the parser, and send the xml to be parsed
        result = urllib2.urlopen(self.url % symbol).read()
        result = result.replace('\\x', '\\u00')
        stock = json.loads(result[4:])
        return stock[0]
