from modules import *

import time
import threading

import pika
import json

from config import BotConfig

class Git(Module):
    """Module that starts up a thread to check our message queue
    for any new github commits.

    """

    def __init__(self, *args, **kwargs):
        """ Constructor. """

        Module.__init__(self, kwargs=kwargs)
        
        self.callback = self.message_callback
        self.connection = None
        self.channel = None
        self.queue_name = "github"
        self.irc.execute_interval(10, self.connect)

    def message_callback(self, message, **kwargs):
        print message

    def connect(self):
        config = BotConfig()
        host = config.get('amqp', 'host')
        user = config.get('amqp', 'user')
        password = config.get('amqp', 'pass')

        print 'connecting'
        parameters = pika.ConnectionParameters(
            host=host,
            credentials=pika.PlainCredentials(user, password)
        )
        self.connection = pika.SelectConnection(parameters, self.on_connected)

    def on_connected(self, connection):
        connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        self.channel = channel
        self.channel.exchange_declare(exchange='gitExchange', type='topic',
                durable=True, callback=self.on_exchange_declared)

    def on_queue_declared(self, frame):
        self.channel.queue_bind(exchange='gitExchange', queue=self.queue_name, routing_key="#",
                callback=self.on_queue_binded)
        
    def on_exchange_declared(self, frame):
        self.channel.queue_declare(queue=self.queue_name, exclusive=False,
                callback=self.on_queue_declared)

    def on_queue_binded(self, frame):
        self.channel.basic_consume(self.handle_delivery, queue=self.queue_name)

    def handle_delivery(self, channel, method_frame, header_frame, body):
        self.callback(body)
        self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
