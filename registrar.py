import datetime
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
    reg = Registrar().start()

    rcc = RabbitCommandClient(exchange='dragon', routing_key='dragon.command')
    rcc.send(json_string=Start().to_json(), exchange='dragon', routing_key='dragon.command')
    rcc.send(json_string=Ping().to_json(), exchange='dragon', routing_key='dragon.command')
    rcc.send(json_string=Pong().to_json(), exchange='dragon', routing_key='dragon.command')
    rcc.send(json_string=Tick(datetime.datetime.now()).to_json(), exchange='dragon', routing_key='dragon.command')
    rcc.send(json_string=Notification({ 'message': 'hi mom'}).to_json(), exchange='dragon', routing_key='dragon.command')
    rcc.send(json_string=Acknowledgement({ 'ack': 'hi rich'}).to_json(), exchange='dragon', routing_key='dragon.command')
    rcc.send(json_string=ResourceReady('http://google.com').to_json(), exchange='dragon', routing_key='dragon.command')

    time.sleep(1)
    print(reg.dump())
