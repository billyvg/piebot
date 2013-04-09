"""Weather module for ppbot.
@package ppbot

Given a zipcode, will lookup the associated weather for that zipcode.
Will be using wunderground.com's API.

@syntax w <zipcode>

"""
import urllib
import string
import re
import json

import requests

from config import BotConfig
from modules import *


class Weather(Module):
    API_URL = 'http://api.wunderground.com/api/%s/conditions/q/%s.json'

    def __init__(self, *args, **kwargs):
        """Constructor"""

        Module.__init__(self, kwargs=kwargs)

        # TODO throw exception if it doesn't exist
        self.api_key = BotConfig().get('wunderground', 'api_key')
        # url for wunderground's api, forecast url

    def _register_events(self):
        """Register module commands."""

        self.add_command('w')

    def w(self, event):
        """Action to react/respond to user calls."""

        if self.num_args >= 1:
            # need to fetch the weather and parse it
            zipcode = ' '.join(event['args'])

            m = re.search('\+\+|\-\-', zipcode)
            if m:
                self.msg(event['target'], 'Could not get weather data for "%s--"' % event['nick'])
            else:
                try:
                    weather = self.get_weather(zipcode)
                    # stylize the message output
                    try:
                        message1 = "%(city)s (%(zipcode)s) - %(condition)s @ %(temp_f)sF (%(temp_c)sC) - Humidity: %(humidity)s, Winds: %(wind)s" % (weather)
                    except:
                        message1 = "%(city)s - %(condition)s @ %(temp_f)sF (%(temp_c)sC) - Humidity: %(humidity)s, Winds: %(wind)s" % (weather)

                    #message2 = "Today (%(day)s) - High: %(high)sF, Low: %(low)sF - %(condition)s" % weather['forecast'][0]
                    #message3 = "Tomorrow (%(day)s) - High: %(high)sF, Low: %(low)sF - %(condition)s" % weather['forecast'][1]
                    # send the messages
                    self.msg(event['target'], message1)
                    #self.msg(event['target'], message2)
                    #self.msg(event['target'], message3)
                except:
                    import traceback
                    traceback.print_exc()
                    self.msg(event['target'], 'Could not get weather data for "%s"' % zipcode)
        else:
            self.syntax_message(event['nick'], '.w <zipcode>')

    def get_weather(self, zipcode):
        """Connects to weather API and parses for the weather."""

        # make the parser, and send the xml to be parsed
        data = {}
        r = requests.get(self.__class__.API_URL % (self.api_key, zipcode.replace(' ', '_')))
        resp = json.loads(r.text)
        try:
            obs = resp['current_observation']

            data['city'] = obs['display_location']['full']
            data['zipcode'] = obs['display_location']['zip']
            data['temp_f'] = obs['temp_f']
            data['temp_c'] = obs['temp_c']
            data['condition'] = obs['weather']
            data['humidity'] = obs['relative_humidity']
            data['wind'] = obs['wind_string']

            return data
        except KeyError:
            print 'no current_obs'
            print resp
