import json

from dragon_eb import DragonBusClient
from simple_event import Pong

class Ponger(DragonBusClient):

    def __init__(self):
        DragonBusClient.__init__(self, True)
        # self.ignores('event_id', 2)
        self.listen_for('event_id', 1)
        self.add_callback(self.send_pong)

    def send_pong(self, ch, method, properties, json_message):
        self.rmq_client.send(Pong().to_json())
        print("{{{Pong}}}")

if __name__ == "__main__":
    Ponger().start()
