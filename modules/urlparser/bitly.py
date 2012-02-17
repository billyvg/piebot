import re, htmlentitydefs
import urllib2
import string
import traceback

try:
    import simplejson as json
except ImportError:
    import json
from unidecode import unidecode

from config import BotConfig

class Bitly(object):
    """Checks incoming messages for possible urls.  If a url is found then
    visit the site and get the <title>.

    """

    pattern = re.compile("http://([^ ]+)")

    def __init__(self, *args, **kwargs):
        """Constructor."""

        self.youtube_pattern = re.compile("http(s|)://(www\.|)youtube.com/(#!/|)watch")

    def handle(self, match, **kwargs):
        matched_url = match.group(0)
        title = ''

        try:
            title = self.get_url_title(matched_url)
        
            try:
                d = self.youtube_pattern.search(matched_url)
                if d:
                    matched_url = matched_url + "&hd=1"
                short_url = self.get_short_url(matched_url)
                return "%s .:. %s" % (short_url, title)
            except:
                pass
                # need some proper logging =[
        except:
            pass


    def get_url_title(self, url):
        """Connects to a URL and grabs the site title.

        TODO: Un-clusterfuck this.
        """

        USER_AGENT = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Ubuntu/11.04 Chromium/14.0.825.0 Chrome/14.0.825.0 Safari/535.1'

        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        page = response.read()
        
        # check if page type is text/html
        if response.info().type == 'text/html' or response.info().type == 'application/xhtml+xml':
            regex = '<title[^>]*>(.*?)</title>'
            m = re.search(regex, page, re.S)
            if m:
                title = m.group(1)
                title = title.strip()
                title = title.replace('\t', ' ')
                title = title.replace('\n', ' ')
                title = title.replace('\r', ' ')
                try:
                    title.decode('utf-8')
                except:
                    try: title = title.decode('iso-8859-1').encode('utf-8')
                    except: title = title.decode('cp1252').encode('utf-8')

                r_entity = re.compile(r'&[A-Za-z0-9#]+;')
                def e(m): 
                    entity = m.group(0)
                    if entity.startswith('&#x'): 
                        cp = int(entity[3:-1], 16)
                        return unichr(cp).encode('utf-8')
                    elif entity.startswith('&#'): 
                        cp = int(entity[2:-1])
                        return unichr(cp).encode('utf-8')
                    else: 
                        char = htmlentitydefs.name2codepoint[entity[1:-1]]
                        return unichr(char).encode('utf-8')
                title = r_entity.sub(e, title)

                title = unidecode(title)
                return title
            else:
                return "<No Title>"

        else:
            raise Exception('Error retrieving page')

    def get_short_url(self, url):
        """Uses bit.ly's API to shorten a URL"""

        # first setup some options for bitly
        config = BotConfig()
        api_key = config.get('bitly', 'api_key')
        api_login = config.get('bitly', 'api_login')
        api_url = 'http://api.bit.ly/v3/shorten?&login=%s&apiKey=%s&longUrl=%s' % (
                        api_login, api_key,
                        string.replace(url, '&', '%26')
                    )

        req = urllib2.Request(api_url)
        response = urllib2.urlopen(req)
        page = response.read()

        decoded = json.loads(page)
        if decoded['status_code'] == 200:
            return decoded['data']['url']


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
