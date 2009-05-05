"""Weather module for ppbot.
@package ppbot

Given a zipcode, will lookup the associated weather for that zipcode.
Will be using wunderground.com's API.

@syntax w <zipcode>

"""
import urllib2
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

from modules import *

class Weather(Module):
    
    def __init__(self, server):
        """Constructor"""
        
        Module.__init__(self, server)
        
        # url for wunderground's api, location url
        self.lurl = 'http://api.wunderground.com/auto/wui/geo/GeoLookupXML/index.xml?query=%s'
        # url for wunderground's api, forecast url
        self.furl = 'http://api.wunderground.com/auto/wui/geo/ForecastXML/index.xml?query=%s'
        
    def _register_triggers(self):
        """Register module triggers."""
        
        self.add_trigger('w')
    
    def w(self, event):
        """Action to react/respond to user calls."""
        
        if self.num_args == 1:
            # need to fetch the weather and parse it
            zipcode = event['args'][0]
            self.get_weather(zipcode)
            
            # create a nice output for the results
            fc = self.handler.forecast
            txt = self.handler.txt
            print fc
            print txt
            
            # stylize the message output
            message1 = "%s - High: %sF (%sC) Low: %sF (%sC) - %s" % (zipcode, fc['1']['high']['fahrenheit'],
                fc['1']['high']['celsius'], fc['1']['low']['fahrenheit'], fc['1']['low']['celsius'],
                fc['1']['conditions'] )
            try:
                message2 = "%s: %s" % (txt['1']['title'], txt['1']['fcttext'])
                message3 = "%s: %s" % (txt['2']['title'], txt['2']['fcttext'])
            except:
                pass
                
            # send the messages
            self.msg(event['target'], message1)
            try:
                self.msg(event['target'], message2)
                self.msg(event['target'], message3)
            except:
                pass
        else:
            self.syntax_message(event['source']['nick'], '.w <zipcode>')
        
        
    def get_weather(self, zipcode):
        """Connects to wunderground's API and parses the receiving XML for the weather."""
        
        try:
            # make the parser, and send the xml to be parsed
            parser = make_parser()
            self.handler = WeatherHandler()
            parser.setContentHandler(self.handler)
            parser.parse(self.furl % zipcode)
        except urllib2.URLError, e:
            print "something fucked up in weather"
            print e
        

class WeatherHandler(ContentHandler):
    """ContentHandler for wunderground's XML API."""
    
    def __init__(self):
        # current element
        self.element = None
        self.elementData = None
        
        # txt_forecast, to get the description of the weather
        self.txt_forecast = False
        # simpleforecast flag, to get the forecast numbers
        self.simpleforecast = False
        self.high = False
        self.low = False
        self.isPeriod = False
        self.period = None
        
        self.data = {}
        self.txt = {}
        self.forecast = {}
        
    def startElement(self, name, attrs):
        
        # if statements for the different flags we need to track
        if name == 'txt_forecast':
            self.txt_forecast = True
        
        if name == 'simpleforecast':
            self.simpleforecast = True
        
        if name == 'high':
            self.high = True
        if name == 'low':
            self.low = True
                
        if name == 'period':
            self.isPeriod = True
            
        self.element = name
        
    def characters(self, ch):
        ch = ch.strip()
        self.elementData = ch
        self.data[self.element] = ch

        # get the period number
        if self.isPeriod:
            self.period = ch
            
        # parse for the title and forecast txt
        if self.txt_forecast:
            if self.period:
                try:
                    self.txt[self.period][self.element] = ch
                except:
                    self.txt[self.period] = {}
                    
        # parse for the forecasts
        if self.simpleforecast and ch:
            # make sure a period is set
            if self.period:
                # see if we're looking for the high temps
                if self.high:
                    try:
                        self.forecast[self.period]['high'][self.element] = ch
                    except:
                        self.forecast[self.period]['high'] = {}
                        self.forecast[self.period]['high'][self.element] = ch
                # the low temps
                if self.low:
                    try:
                        self.forecast[self.period]['low'][self.element] = ch
                    except:
                        self.forecast[self.period]['low'] = {}
                        self.forecast[self.period]['low'][self.element] = ch
                # every other element in the simpleforecast tree
                else:
                    try:
                        self.forecast[self.period][self.element] = ch
                    except:
                        self.forecast[self.period] = {}
                        self.forecast[self.period][self.element] = ch
        
    def endElement(self, name):
        
        # reverse the flags at the end of an element
        if name == 'txt_forecast':
            self.txt_forecast = False
        
        if name == 'simpleforecast':
            self.simpleforecast = False
            
        if name == 'high':
            self.high = False
        if name == 'low':
            self.low = False
            
        if name == 'period':
            self.isPeriod = False
            
        self.element = None