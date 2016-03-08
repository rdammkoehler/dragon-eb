import json

from dragon_eb import DragonBusClient
from event_id_filter import EventIdFilter

from pymongo import MongoClient

class Deadpool(DragonBusClient):

    DEAD_LEVELS = [ 'ERROR', 'CRITICAL' ]

    def __init__(self):
        DragonBusClient.__init__(self, EventIdFilter(1001))
        self.mongo_client = MongoClient()
        self.add_callback(self.__persist_message)

    def __persist_message(self, ch, method, properties, json_message):
        if self.__dead(json_message):
            self.mongo_client.dragon.deadpool.insert_one(json_message)

    def __dead(self, json_message):
        level = json_message['header']['level']
        return level in self.DEAD_LEVELS


if __name__ == "__main__":
    Deadpool().start().join()
