"""Looks up a location via yelp
@package ppbot

@syntax yelp <search term>

"""
import json

import requests
import oauth2 as oauth


from config import BotConfig
from modules import *

class Yelp(Module):
    API_URL = 'http://api.yelp.com/v2/search'

    def __init__(self, *args, **kwargs):
        """Constructor"""
        Module.__init__(self, kwargs=kwargs)

    def _register_events(self):
        """Register module commands."""

        self.add_command('yelp')

    def yelp(self, event):
        """Action to react/respond to user calls."""

        term = ' '.join(event['args'])
        try:
            resp = self.query(term)
            resp = resp['businesses'][0]

            result = {
                    'name': resp['name'],
                    'rating': resp['rating'],
                    'review_count': resp['review_count'],
                    'area_code': resp['phone'][0:3],
                    'phone': '%s-%s' % (resp['phone'][3:6], resp['phone'][6:]),
                    'url': resp['url'],
                    'address': resp['location']['display_address'][0],
                    'city': resp['location']['city'],
                    }

            message = '%(name)s (%(rating).2f w/ %(review_count)d reviews) @ %(address)s, %(city)s - (%(area_code)s) %(phone)s. %(url)s' % result
            self.msg(event['target'], message.encode('utf-8'))
        except KeyError:
            print resp
            self.msg(event['target'], 'Could not find "%s" on Yelp.' % term)
        except IndexError:
            print resp
            pass

    def query(self, term, location='San Francisco', **kwargs):
        url = self.get_signed_url(Yelp.API_URL, {'term': term, 'location': location, 'limit': 1})

        req = requests.get(url)
        resp = json.loads(req.text)
        return resp

    def get_signed_url(self, url, params):
        try:
            config = BotConfig()
            consumer_key = config.get('yelp', 'consumer_key')
            consumer_secret = config.get('yelp', 'consumer_secret')
            token = config.get('yelp', 'token')
            token_secret = config.get('yelp', 'token_secret')
        except NoOptionError:
            print "Error: You need to set your yelp API keys!"

        consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
        oauth_request = oauth.Request('GET', url, params)
        oauth_request.update({'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': oauth.generate_timestamp(),
            'oauth_token': token,
            'oauth_consumer_key': consumer_key})
        token = oauth.Token(token, token_secret)
        oauth_request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, token)
        signed_url = oauth_request.to_url()
        return signed_url

