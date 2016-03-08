import json
import time
import urllib.request

from dragon_eb import DragonBusClient
from event_id_filter import EventIdFilter
from simple_event import ResourceReady

class ResourceRetriever(DragonBusClient):

    def __init__(self, resource_receiver):
        DragonBusClient.__init__(self, EventIdFilter(2000))
        self.add_callback(resource_receiver)

class ResourceCat:

    def cat(self, ch, method, properties, json_message):
        print(urllib.request.urlopen(json_message['body']['resource_url']))
        with urllib.request.urlopen(json_message['body']['resource_url']) as resource:
            print('cat')
            print(resource.read())

if __name__ == "__main__":
    ResourceRetriever(ResourceCat().cat).start().join()
