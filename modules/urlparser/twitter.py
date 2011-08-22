import re
import urllib2
import traceback

try:
    import simplejson as json
except ImportError:
    import json

class Twitter(object):
    """Checks incoming messages for Twitter urls and calls the Twitter API to
    retrieve the tweet.

    TODO: 
        Implement commands for Twitter functionality

    """
    pattern = re.compile("http(s|)://(www\.|)twitter.com/#!/[^/]+/status/([0-9]+)")

    def __init__(self, *args, **kwargs):
        """Constructor."""
        pass

    def handle(self, match, **kwargs):
        try:
            data = self.fetch (match.group(3))
            return '\x02%s\x02 tweets "%s"' % (tweet['user']['name'], tweet['text'])
        except:
            print "Problem fetching tweet"
            print traceback.print_exc()


    def fetch(self, status_id):
        """Use Twitter's REST API to fetch a status."""

        api_url = 'http://api.twitter.com/1/statuses/show.json?id=%s&include_entities=true' % (status_id)

        req = urllib2.Request(api_url)
        response = urllib2.urlopen(req)
        page = response.read()

        decoded = json.loads(page)
        return decoded

