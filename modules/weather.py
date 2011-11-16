"""Weather module for ppbot.
@package ppbot

Given a zipcode, will lookup the associated weather for that zipcode.
Will be using wunderground.com's API.

@syntax w <zipcode>

"""
import urllib, urllib2
import string
from xml.dom.minidom import parseString

from modules import *

class Weather(Module):
    
    def __init__(self, *args, **kwargs):
        """Constructor"""
        
        Module.__init__(self, kwargs=kwargs)
        
        # url for wunderground's api, forecast url
        self.wurl = 'http://www.google.com/ig/api?weather=%s'
        
    def _register_events(self):
        """Register module commands."""
        
        self.add_command('w')
    
    def w(self, event):
        """Action to react/respond to user calls."""
        
        if self.num_args >= 1:
            # need to fetch the weather and parse it
            zipcode = ' '.join(event['args'])
            try:
                weather = self.get_weather(zipcode)
                # stylize the message output
                message1 = "%(city)s (%(zipcode)s) - Currently: %(temp_f)sF (%(temp_c)sC) - Conditions: %(condition)s, %(humidity)s, %(wind)s" % (weather)
                message2 = "Today (%(day)s) - High: %(high)sF, Low: %(low)sF - %(condition)s" % weather['forecast'][0]
                message3 = "Tomorrow (%(day)s) - High: %(high)sF, Low: %(low)sF - %(condition)s" % weather['forecast'][1]
                # send the messages
                self.msg(event['target'], message1)
                self.msg(event['target'], message2)
                self.msg(event['target'], message3)
            except:
                self.msg(event['target'], 'Could not get weather data for "%s"' % zipcode)
        else:
            self.syntax_message(event['target'], '.w <zipcode>')
        
        
    def get_weather(self, zipcode):
        """Connects to google's secret weather API and parses the receiving XML for the weather."""
        
        # make the parser, and send the xml to be parsed
        xml = urllib2.urlopen(self.wurl % urllib.quote_plus(zipcode)).read()
        xml = string.replace(xml, '<?xml version="1.0"?>', '')
        dom = parseString(xml)
        weather = {}
        forecast = []

        forecast_information = dom.getElementsByTagName('forecast_information')[0]
        current_conditions = dom.getElementsByTagName('current_conditions')[0]
        forecast_conditions = dom.getElementsByTagName('forecast_conditions')

        weather['city'] = forecast_information.getElementsByTagName('city')[0].getAttribute('data')
        weather['zipcode'] = forecast_information.getElementsByTagName('postal_code')[0].getAttribute('data')
        weather['condition'] = current_conditions.getElementsByTagName('condition')[0].getAttribute('data')
        weather['wind'] = current_conditions.getElementsByTagName('wind_condition')[0].getAttribute('data')
        weather['humidity'] = current_conditions.getElementsByTagName('humidity')[0].getAttribute('data')
        weather['temp_f'] = current_conditions.getElementsByTagName('temp_f')[0].getAttribute('data')
        weather['temp_c'] = current_conditions.getElementsByTagName('temp_c')[0].getAttribute('data')

        for x in forecast_conditions:
            fc_temp = {}
            fc_temp['day'] = x.getElementsByTagName('day_of_week')[0].getAttribute('data') 
            fc_temp['low'] = x.getElementsByTagName('low')[0].getAttribute('data') 
            fc_temp['high'] = x.getElementsByTagName('high')[0].getAttribute('data') 
            fc_temp['condition'] = x.getElementsByTagName('condition')[0].getAttribute('data') 
            forecast.append(fc_temp)

        weather['forecast'] = forecast
        return weather
