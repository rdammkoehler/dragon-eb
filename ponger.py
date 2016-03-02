import json

from dragon_eb import DragonBusClient
from event_id_filter import EventIdFilter
from simple_event import Pong

class Ponger(DragonBusClient):

    def __init__(self):
        DragonBusClient.__init__(self, EventIdFilter(1))
        self.add_callback(self.send_pong)

    def send_pong(self, ch, method, properties, json_message):
        self.send(Pong().to_json())

if __name__ == "__main__":
    Ponger().start()
