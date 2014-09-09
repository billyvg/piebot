#!/usr/bin/python

from argparse import ArgumentParser

from piebot.bot import Bot
import irc.logging

#import piebot.bot
if __name__ == "__main__":
    parser = ArgumentParser(
        description="Start piebot"
    )
    irc.logging.add_arguments(parser)
    irc.logging.setup(parser.parse_args())

    bot = Bot(parser.parse_args())
    bot.start()
