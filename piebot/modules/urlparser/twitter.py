import re
import json

import requests
import oauth2 as oauth
from HTMLParser import HTMLParser

import settings

class Twitter(object):
    """Checks incoming messages for Twitter urls and calls the Twitter API to
    retrieve the tweet.

    TODO: 
        Implement commands for Twitter functionality

    """
    pattern = re.compile("http(?:s|)://(?:mobile\.|)(?:www\.|)twitter.com/(?:#!/|)[^/]+/status(?:es|)/([0-9]+)")
    API_URL = 'https://api.twitter.com/1.1'

    def __init__(self, *args, **kwargs):
        """Constructor."""
        pass

    def handle(self, match, **kwargs):
        h = HTMLParser()
        try:
            data = self.fetch (match.group(1))
            return '\x02%s\x02 tweets "%s"' % (data['user']['name'], h.unescape(''.join(data['text'].splitlines())))
        except:
            import traceback
            print "Problem fetching tweet"
            print traceback.print_exc()


    def fetch(self, status_id):
        """Use Twitter's REST API to fetch a status."""

        api_url = 'http://api.twitter.com/1.1/statuses/show.json?id=%s&include_entities=true' % (status_id)
        url = self.get_signed_url('%s/statuses/show.json' % Twitter.API_URL, {'id': status_id})

        req = requests.get(url)
        decoded = json.loads(req.text)

        return decoded

    def get_signed_url(self, url, params):
        try:
            consumer_key = settings.TWITTER_CONSUMER_KEY
            consumer_secret = settings.TWITTER_CONSUMER_SECRET
            token = settings.TWITTER_TOKEN
            token_secret = settings.TWITTER_TOKEN_SECRET
        except:
            import traceback
            traceback.print_exc()
            print "Error: You need to set your Twitter API keys!"

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


