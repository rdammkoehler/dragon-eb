import json
import os

from filter import Filter
from rabbit_client import RabbitCommandClient


class DragonBusClient:

    def __init__(self, message_filter=Filter()):
        self.message_filter = message_filter
        self.rmq_client = RabbitCommandClient()
        self.rmq_client.recv(callback=self.on_message)
        self.callbacks = []

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def start(self):
        self.rmq_client.start()

    def send(self, json_string):
        self.rmq_client.send(json_string)

    def on_message(self, ch, method, properties, message):
        json_message = json.loads(message.decode('utf-8'))
        if self.message_filter.accept(json_message):
            for callback in self.callbacks:
                callback(ch, method, properties, json_message)
        else:
            print("(%d) not accepted %s" % (os.getpid(), json_message))
