import datetime
import threading
import time

from dragon_eb import DragonBusClient
from event_id_filter import EventIdExclusionFilter
from rabbit_client import RabbitCommandClient
from simple_event import *

class Registrar(DragonBusClient):

    def __init__(self):
        DragonBusClient.__init__(self, EventIdExclusionFilter(10000))
        self.registered_events = {}  # replace with a database
        self.add_callback(self.__check_registration)

    def __check_registration(self, ch, method, properties, json_message):
        event_id = json_message['header']['event_id']
        if not event_id in self.registered_events:
            self.registered_events[event_id] = 1
            self.__notify(event_id)
        else:
            self.registered_events[event_id] += 1

    def __notify(self, event_id):
        self.send(NewEvent(event_id).to_json())

    def dump(self):
        return self.registered_events

if __name__ == "__main__":
    reg = Registrar()
    reg_thread = threading.Thread(target=reg.start)
    reg_thread.setDaemon(True)
    reg_thread.start()

    rcc = RabbitCommandClient()
    rcc.send(Start().to_json())
    rcc.send(Ping().to_json())
    rcc.send(Pong().to_json())
    rcc.send(Tick(datetime.datetime.now()).to_json())
    rcc.send(Notification({ 'message': 'hi mom'}).to_json())
    rcc.send(Acknowledgement({ 'ack': 'hi rich'}).to_json())
    rcc.send(ResourceReady('http://google.com').to_json())

    time.sleep(1)
    print(reg.dump())
