import json

from pymongo import MongoClient
from rabbit_client import RabbitCommandClient

class DragonBusClient:

    def __init__(self):
        self.mongo_client = MongoClient()
        self.rmq_client = RabbitCommandClient()
        self.rmq_client.recv(callback=self.store_received_message)

    def callback(self, callback):
        self.callback = callback

    def start(self):
        self.rmq_client.start()

    def send(self, json_string):
        self.rmq_client.send(json_string)

    def store_received_message(self, ch, method, properties, message):
        json_message = json.loads(message.decode('utf-8'))
        self.mongo_client.dragon.events.insert_one(json_message).inserted_id
        print("stored %s" % json_message)
        self.callback(ch, method, properties, message)
