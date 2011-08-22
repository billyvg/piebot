"""Handles reading the bot's configuration file.
@package ppbot


"""

from ConfigParser import RawConfigParser

CONFIG_FILE = 'ppbot.cfg'

class BotConfig(RawConfigParser):
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Singleton"""
        if not cls._instance:
            cls._instance = super(BotConfig, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, filename=None, **kwargs):
        RawConfigParser.__init__(self)

        if filename:
            self.readfp(open(filename))
        else:
            self.readfp(open(CONFIG_FILE))

