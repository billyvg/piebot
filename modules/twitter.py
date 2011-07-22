from modules import *

import re, htmlentitydefs
import urllib2
import string
try:
    import simplejson as json
except ImportError:
    import json

class Twitter(Module):
    """Checks incoming messages for Twitter urls and calls the Twitter API to
    retrieve the tweet.

    TODO: 
        Implement commands for Twitter functionality

    """

    def __init__(self, *args, **kwargs):
        """Constructor."""

        Module.__init__(self, kwargs=kwargs)
        self.url_pattern = re.compile("http(s|)://(www\.|)twitter.com/#!/[^/]+/status/([0-9]+)")

    def _register_events(self):
        self.add_event('pubmsg', 'parse_tweet')

    def parse_tweet(self, event):
        nick = event['nick']
        try:
            m = self.url_pattern.search(event['message'])
            if m:
                tweet = self.fetch_tweet(m.group(3))
                self.server.privmsg(event['target'], '\x02%s\x02 tweets "%s"' % (tweet['user']['name'], tweet['text']))
        except:
            print "Problem fetching tweet"
            print traceback.print_exc()


    def fetch_tweet(self, status_id):
        """Use Twitter's REST API to fetch a status."""

        api_url = 'http://api.twitter.com/1/statuses/show.json?id=%s&include_entities=true' % (status_id)

        req = urllib2.Request(api_url)
        response = urllib2.urlopen(req)
        page = response.read()

        decoded = json.loads(page)
        return decoded

