"""
Inspired from https://github.com/coleifer/irc/blob/master/bots/redisbot.py

"""
import re
import random

from modules import *

class Chatbot(Module):
    chain_length = 2
    chattiness = 0.01
    max_words = 20
    messages_to_generate = 5
    separator = '\x01'
    stop_word = '\x02'

    def __init__(self, *args, **kwargs):
        """Constructor"""

        Module.__init__(self, kwargs=kwargs)

    def _register_events(self):
        """Register module events and commands."""

        self.add_event('pubmsg', 'parse_message')

    def make_key(self, k):
        return k

    def sanitize_message(self, message):
        return re.sub('[\"\']', '', message.lower())

    def split_message(self, message):
        # split the incoming message into words, i.e. ['what', 'up', 'bro']
        words = message.split()

        # if the message is any shorter, it won't lead anywhere
        if len(words) > self.chain_length:

            # add some stop words onto the message
            # ['what', 'up', 'bro', '\x02']
            words.append(self.stop_word)

            # len(words) == 4, so range(4-2) == range(2) == 0, 1, meaning
            # we return the following slices: [0:3], [1:4]
            # or ['what', 'up', 'bro'], ['up', 'bro', '\x02']
            for i in range(len(words) - self.chain_length):
                yield words[i:i + self.chain_length + 1]

    def generate_message(self, seed):
        key = seed

        # keep a list of words we've seen
        gen_words = []

        # only follow the chain so far, up to <max words>
        for i in xrange(self.max_words):

            # split the key on the separator to extract the words -- the key
            # might look like "this\x01is" and split out into ['this', 'is']
            words = key.split(self.separator)

            # add the word to the list of words in our generated message
            gen_words.append(words[0])

            # get a new word that lives at this key -- if none are present we've
            # reached the end of the chain and can bail
            next_word = self.db.markov.find_one({
                'key': key
            })

            if not next_word or len(next_word['sequences']) < 1:
                break

            # create a new key combining the end of the old one and the next_word
            key = self.separator.join(words[1:] + [random.choice(next_word['sequences'])])

        return ' '.join(gen_words)

    def parse_message(self, event):
        """Parses any public messages to add it to the brain,
        as well as look for users who are talking to the bot
        by detecting users who type the bot's name in chat.

        TODO: Do we want to add text when people are talking to the bot?

        """

        say_something = False
        message = event['message']
        messages = []

        if message.startswith('.'):
            return

        if self.pinged():
            say_something = True
            message = self.fix_ping()

        # split up the incoming message into chunks that are 1 word longer than
        # the size of the chain, e.g. ['what', 'up', 'bro'], ['up', 'bro', '\x02']
        for words in self.split_message(self.sanitize_message(message)):
            # grab everything but the last word
            key = self.separator.join(words[:-1])

            # add the last word to the set
            self.db.markov.update({
                'key': key,
                'channel': event['target']
            }, {
                '$addToSet': {
                    'sequences': words[-1]
                }
            }, True)

                # if we should say something, generate some messages based on what
            # was just said and select the longest, then add it to the list
            if say_something:
                best_message = ''
                for i in range(self.messages_to_generate):
                    generated = self.generate_message(seed=key)
                    if len(generated) > len(best_message) and len(generated) > 2:
                        best_message = generated

                if best_message:
                    messages.append(best_message)

        if len(messages):
            self.reply(random.choice(messages))
