from dragon_eb import DragonBusClient
from event_chain import *
from event_id_filter import EventIdFilter


class EventChainTrigger(DragonBusClient):
    def __init__(self):
        DragonBusClient.__init__(self, EventIdFilter(5000))
        self.add_callback(self.__execute_chain)
        self.chains = {
            0: blah.delay,
            1: hello_world.delay,
            2: hello_user.delay
        }

    def __execute_chain(self, ch, method, properties, json_message):
        event_chain_id = json_message['body']['event_chain_id']
        print("starting event_chain_id %s" % event_chain_id)
        print(self.chains[event_chain_id]().get(timeout=1))


if __name__ == "__main__":
    EventChainTrigger().start().join()
