from dragon_esb import DragonBusClient
from simple_event import Pong

class Ponger(DragonBusClient):

    def __init__(self):
        DragonBusClient.__init__(self)
        self.callback(self.send_pong)
        self.ignores('event_id', 2)

    def send_pong(self, ch, method, properties, message):
        self.rmq_client.send(Pong().to_json())
        print("{{{Pong}}}")

if __name__ == "__main__":
    Ponger().start()
