from modules import *

import re, htmlentitydefs
import urllib2
import string
try:
    import simplejson as json
except ImportError:
    import json

class Urlparser(Module):
    """Checks incoming messages for possible urls.  If a url is found then
    visit the site and get the <title>.

    """

    def __init__(self, *args, **kwargs):
        """Constructor."""

        Module.__init__(self, kwargs=kwargs)
        self.url_pattern = re.compile("http://(.*?$(?<!jpg|png|gif))")
        self.youtube_pattern = re.compile("http(s|)://(www\.|)youtube.com/(#!/|)watch")
        

    def _register_events(self):
        self.add_event('pubmsg', 'parse_message')

    def parse_message(self, event):
        nick = event['nick']
        try:
            m = self.url_pattern.search(event['message'])
            if m:
                matched_url = m.group(0)
                try:
                    d = self.youtube_pattern.search(matched_url)
                    if d:
                        matched_url = matched_url + "&hd=1"
                    short_url = self.get_short_url(matched_url)
                    self.server.privmsg(event['target'], "%s .:. %s" % (short_url, self.get_url_title(m.group(0))))
                except:
                    # need some proper logging =[
                    pass
        except:
            pass

    def get_url_title(self, url):
        """Connects to a URL and grabs the site title"""

        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        page = response.read()

        regex = '<title[^>]*>(.*?)</title>'
        m = re.search(regex, page, re.S)
        if m:
            return ' '.join(self.unescape(m.group(1)).split()).encode('ascii', 'ignore')
        else:
            return "<No Title>"

    def get_short_url(self, url):
        """Uses bit.ly's API to shorten a URL"""

        # first setup some options for bitly
        api_key = 'R_c8b8a9be4763f9c4a8ebcf6cdaef1004'
        api_login = 'rdmty'
        api_version = '2.0.1'
        api_url = 'http://api.bit.ly/shorten?version=%s&longUrl=%s&login=%s&apiKey=%s' % (api_version, string.replace(url, '&', '%26'), api_login, api_key)

        req = urllib2.Request(api_url)
        response = urllib2.urlopen(req)
        page = response.read()

        decoded = json.loads(page)
        if decoded['results']:
            return decoded['results'][url]['shortUrl']

    def unescape(self, text):
        """Try to unescape the different weird characters in titles."""

        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except:
                    pass
            return text # leave as is
        return re.sub("&#?\w+;", fixup, text)
