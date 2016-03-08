import json
# import threading
import time
import urllib.request

from dragon_eb import DragonBusClient
from event_id_filter import EventIdFilter
from simple_event import ResourceReady

class ResourceRetriever(DragonBusClient):

    def __init__(self, resource_receiver):
        self.resource_receiver = resource_receiver
        DragonBusClient.__init__(self, EventIdFilter(2000))
        self.add_callback(self.__retrieve_resource)
        # tt = threading.Thread(target=self.start())
        # tt.setDaemon(True)
        # tt.start()

    def __retrieve_resource(self, ch, method, properties, json_message):
        print(urllib.request.urlopen(json_message['body']['resource_url']))
        with urllib.request.urlopen(json_message['body']['resource_url']) as resource:
            self.resource_receiver(resource)

class ResourceCat:

    def cat(self, resource):
        print('cat')
        print(resource.read())


if __name__ == "__main__":
    ResourceRetriever(ResourceCat().cat).start()
