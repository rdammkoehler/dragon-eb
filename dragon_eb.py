import json
import os

from filter import Filter
from rabbit_client import RabbitCommandClient


class DragonBusClient:
    EXCHANGE = 'dragon'
    ROUTING_KEY = 'dragon.command'

    def __init__(self, message_filter=Filter()):
        self.message_filter = message_filter
        self.rmq_client = RabbitCommandClient(exchange=self.EXCHANGE,
                                              routing_key=self.ROUTING_KEY)  # TODO, insulate us from Rabbit
        self.rmq_client.recv(callback=self.on_message)
        self.callbacks = []
        self.thread = None

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def start(self):
        self.thread = self.rmq_client.start()
        return self

    def stop(self):
        self.rmq_client.stop()

    def join(self):  # probably need to handle None thread
        try:
            self.thread.join()
        except KeyboardInterrupt:
            pass

    def send(self, json_string):
        self.rmq_client.send(json_string=json_string, exchange=self.EXCHANGE, routing_key=self.ROUTING_KEY)

    def on_message(self, ch, method, properties, message):
        json_message = self.__json_of(message)
        if json_message:
            if self.message_filter.accept(json_message):
                for callback in self.callbacks:
                    callback(ch, method, properties, json_message)

    def __json_of(self, message):
        try:
            return json.loads(message.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            print("(%d) discarding non-json message" % os.getpid())
