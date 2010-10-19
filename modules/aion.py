import sys, threading, Queue, signal, os, string, random, time
import urllib2, StringIO, re
#import pycurl
#import sgmllib

from modules import *


# define some CURL options
ua = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"

class Aion(Module):
    """Aion module that will search aiononline for stats."""
    
    def __init__(self, server):
        """Constructor"""
        self.code = None
        Module.__init__(self, server)
        
    def _register_events(self):
        """Register module commands."""

        self.add_command('char')
        #self.add_command('guild')
        
    def char(self, event):
        """Searches aiononline's armory site for information about a character."""
        
        name = event['args'][0]
        url = "http://na.aiononline.com/livestatus/character-legion/search?serverName=Zikel&charName=%s" % name
        
        content = StringIO.StringIO()
        parser = CharacterParserRegex()

        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        code = response.read()
        #setup cURL
        #curl = pycurl.Curl()
       # curl.setopt(pycurl.URL, url)
       # curl.setopt(pycurl.USERAGENT, ua)
       # curl.setopt(pycurl.VERBOSE, 0)
       # curl.setopt(pycurl.HTTPGET, 1)
       # curl.setopt(pycurl.WRITEFUNCTION, content.write)
       # curl.perform()
       # curl.close()
        self.code = code
        try:
            #code = content.getvalue()
            parser.parse(code)
            character = parser.character

            short_url = "http://zikel.org/c/%s" % name
            message = '"%s" %s <%s>, a level %d %s %s (%s / %d AP / %d kills). %s' % (character['title'], character['name'], character['legion'], character['level'], character['race'], character['class'], character['pvprank'], character['ap'], character['kills'], short_url)
            self.msg(event['target'], message)
        #print message
        except:
            self.msg(event['target'], "Character not found: %s" % name)


class CharacterParserRegex:
    def parse(self, str):
        self.character = {'id': 0,
                  'title': "", 
                  'name': "", 
                  'legion': "", 
                  'level': 0,
                  'race': "",
                  'class': "", 
                  'pvprank': "", 
                  'ap': 0,
                  'kills': 0}

        #try: 
        # find the title               
        result = re.search('<strong class="title"><a [^>]+>([^<]+)', str)
	try:	
        	self.character['title'] = result.group(1).strip()
	except:
		self.character['title'] = '[No Title]'

        # find the level + name of character
        result = re.search('<span class="name"><span>Lv\.</span> <em>(?P<level>[0-9]+)</em>(?P<name>[^<]+)</span>', str)
        self.character['name'] = result.group('name').strip()
        self.character['level'] = int(result.group('level').strip())

        # find the server, race, and class
        result = re.search('<p class="info">.*?<span>(?P<server>[^<]+)</span>.*?<span>(?P<race>[^<]+)</span>.*?<span>(?P<class>[^<]+)</span>', str, re.I | re.S)
        self.character['race'] = result.group('race').strip()
        self.character['class'] = result.group('class').strip()

        # find the legion, if any
	result = re.search('There is no joined Legion.', str, re.I | re.S)
	if result:
		self.character['legion'] = '[No Legion]'
	else:
        	result = re.search('<p class="legion">.*?<a [^>]+>(?P<legion>[^<]+)</a>', str, re.I | re.S)
        	self.character['legion'] = result.group('legion').strip()

        # find the ap
        result = re.search('<dd><span>.*?<span class="point">([0-9]+)</span>', str)
        self.character['ap'] = int(result.group(1).strip())

        # find the top rank and total kills
        result = re.search('<dd class="total"><span>Top Rank: <strong>(?P<toprank>[^<]+)</strong></span><span>Total Kills: <strong>(?P<kills>[0-9]+)</strong></span></dd>', str)
        self.character['pvprank'] = result.group('toprank').strip()
        self.character['kills'] = int(result.group('kills').strip())

        return self.character
        #except:
        #    return None
