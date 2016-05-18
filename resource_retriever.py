import requests

from dragon_eb import DragonBusClient
from event_id_filter import EventIdFilter


class ResourceRetriever(DragonBusClient):
    def __init__(self, resource_receiver):
        DragonBusClient.__init__(self, EventIdFilter(2000))
        self.add_callback(resource_receiver)


class ResourceCat:
    def cat(self, ch, method, properties, json_message):
        print(requests.get(json_message['body']['resource_url'], verify='ca-chain.cert.pem').text)
        # print(requests.get(json_message['body']['resource_url'], verify='intermediate.cert.pem').text)


if __name__ == "__main__":
    ResourceRetriever(ResourceCat().cat).start().join()
