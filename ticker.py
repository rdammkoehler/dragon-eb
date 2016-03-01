import datetime

from dragon_eb import DragonBusClient
from simple_event import Tick

class Ticker(DragonBusClient):

    def __init__(self):
        DragonBusClient.__init__(self)

    def send_tick(self):
        self.send(Tick(datetime.datetime.now()).to_json())

if __name__ == "__main__":
    Ticker().send_tick()
