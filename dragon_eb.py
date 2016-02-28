import json

from pymongo import MongoClient
from rabbit_client import RabbitCommandClient

class DragonBusClient:

    def __init__(self):
        self.mongo_client = MongoClient()
        self.rmq_client = RabbitCommandClient()
        self.rmq_client.recv(callback=self.store_received_message)
        self.ignore = {}

    def callback(self, callback):
        self.callback = callback

    def ignores(self, key, value):
        if self.ignore and key in self.ignore:
            self.ignore[key].append(value)
        else:
            self.ignore[key] = [value]

    def start(self):
        self.rmq_client.start()

    def send(self, json_string):
        self.rmq_client.send(json_string)

    def store_received_message(self, ch, method, properties, message):
        json_message = json.loads(message.decode('utf-8'))
        if not self.ignored(json_message):
            self.mongo_client.dragon.events.insert_one(json_message).inserted_id
        self.callback(ch, method, properties, json_message)

    def ignored(self, json_message):
        for header, values in self.ignore.items():
            if header in json_message['header']:
                for value in values:
                    if json_message['header'][header] == value:
                        return True
        return False
