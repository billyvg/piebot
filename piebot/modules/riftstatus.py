import sys, threading, Queue, signal, os, string, random, time
import urllib2, StringIO, re
from xml.dom.minidom import parseString

from modules import *


class Riftstatus(Module):
    """Rift module that will check for server status."""
    
    def __init__(self, server):
        """Constructor"""
        Module.__init__(self, server)
        
    def _register_events(self):
        """Register module commands."""

        self.add_command("status")
        self.add_command("butt", "status")
        
    def status(self, event):
        """ Checks the status of a rift server. """ 

        url = "http://www.riftgame.com/en/status/na-status.xml"

        try:
            target_shard = event["args"][0]
        except:
            target_shard = "Briarcliff"

        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        code = response.read()

        try:
            dom = parseString(code)
            shards = dom.getElementsByTagName("shard")
            status = {}

            # look for briarcliff shard
            for shard in shards:
                if shard.getAttribute("name").lower() == target_shard.lower():
                    status["name"] = shard.getAttribute("name")
                    status["online"] = shard.getAttribute("online")
                    status["locked"] = shard.getAttribute("locked")
                    status["population"] = shard.getAttribute("population")
                    status["queued"] = shard.getAttribute("queued")
                    break

            status_message = self.status_messages(status)
            message = "\x02%s\x0f is currently %s with %s" % (status_message["name"], status_message["online"], status_message["queue"])
            self.reply(message)
        except:
            print traceback.print_exc()
            self.reply("Server status not available.")

    def status_messages(self, status):
        message = {}

        message["name"] = status["name"]

        if status["online"] == "True" and status["locked"] == "False":
            message["online"] = "\x033ONLINE\x0f"
        else:
            message["online"] = "\x035OFFLINE\x0f"

        if status["queued"] != "0":
            message["queue"] = "a queue of \x02%s\x0f" % status["queued"]
        else:
            message["queue"] = "\x02NO queue\x0f"

        return message

