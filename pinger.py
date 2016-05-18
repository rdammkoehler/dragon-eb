from dragon_eb import DragonBusClient
from simple_event import Ping


class Pinger(DragonBusClient):
    def __init__(self):
        DragonBusClient.__init__(self)

    def send_ping(self):
        self.send(Ping().to_json())


if __name__ == "__main__":
    Pinger().send_ping()
