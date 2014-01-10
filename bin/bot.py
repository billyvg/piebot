"""piebot.py

A modular python bot

TODO: Lots
"""

from optparse import OptionParser

from piebot.bot import Bot

import piebot.bot
if __name__ == "__main__":
    parser = OptionParser()
    #parser.add_option('-i', '--init-db', dest='initdb', action='store_true',
                        #help='Initialize the database.')
    # parser.add_option('-c', '--config', dest='config_file', action='store',
    #                     type='string', default='ppbot.cfg', help='Initialize the database.')

    (options, args) = parser.parse_args()

    bot = Bot()
    bot.start()
