import json

from dragon_eb import DragonBusClient
from event_id_filter import EventIdRangeExclusionFilter

from pymongo import MongoClient

class Logger(DragonBusClient):

    def __init__(self):
        DragonBusClient.__init__(self, EventIdRangeExclusionFilter(0, 99))
        self.mongo_client = MongoClient()
        self.add_callback(self.__persist_message)

    def __persist_message(self, ch, method, properties, json_message):
        self.mongo_client.dragon.events.insert_one(json_message)

if __name__ == "__main__":
    Logger().start().join()
