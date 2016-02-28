import json

from pymongo import MongoClient
from rabbit_client import RabbitCommandClient

class DragonBusClient:

    def __init__(self, persist_messages=False):
        self.mongo_client = MongoClient()
        self.rmq_client = RabbitCommandClient()
        self.rmq_client.recv(callback=self.on_message)
        self.callbacks = []
        self.ignore = {}
        if persist_messages:
            self.persist_messages()

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def ignores(self, key, value):
        if self.ignore and key in self.ignore:
            self.ignore[key].append(value)
        else:
            self.ignore[key] = [value]

    def start(self):
        self.rmq_client.start()

    def send(self, json_string):
        self.rmq_client.send(json_string)

    def on_message(self, ch, method, properties, message):
        if not self.ignored(message):
            for callback in self.callbacks:
                callback(ch, method, properties, message)

    def ignored(self, message):
        json_message = json.loads(message.decode('utf-8'))
        for header, values in self.ignore.items():
            if header in json_message['header']:
                for value in values:
                    if json_message['header'][header] == value:
                        return True
        return False

    def persist_messages(self):
        self.callback(persist_message)

    def persist_message(self, ch, method, properties, message):
        json_message = json.loads(message.decode('utf-8'))
        if not self.ignored(json_message):
            self.mongo_client.dragon.events.insert_one(json_message).inserted_id