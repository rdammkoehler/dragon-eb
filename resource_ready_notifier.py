from dragon_eb import DragonBusClient
from simple_event import ResourceReady


class ResourceReadyNotifier(DragonBusClient):
    def __init__(self):
        DragonBusClient.__init__(self)

    def notify(self, resource_url):
        self.send(ResourceReady(resource_url).to_json())


if __name__ == "__main__":
    # ResourceReadyNotifier().notify('https://ender.noradltd.com/README.md')
    for resource in ['agencies.jsonl', 'caregivers.jsonl', 'care_logs.jsonl', 'clients.jsonl',
                     'locations.jsonl', 'shifts.jsonl', 'timezone_agencies.jsonl']:
        url = "https://ender.noradltd.com/%s" % resource
        print("sending %s" % url)
        ResourceReadyNotifier().notify(url)
