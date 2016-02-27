from dragon_esb import DragonBusClient
from simple_event import Pong

class Ponger(DragonBusClient):

    def __init__(self):
        DragonBusClient.__init__(self)
        self.callback(self.send_pong)

    def send_pong(self, ch, method, properties, message):
        json_message = Pong().to_json()
        self.rmq_client.send(json_message)
        print("{{{Pong}}} %s" % json_message)

if __name__ == "__main__":
    Ponger().start()
