from mask import Condition, Mask
from resource_retriever import ResourceRetriever


class ResourceJoin:
    def __init__(self, mask):
        self.mask = mask
        self.retriever = ResourceRetriever(self.accept).start()

    def accept(self, ch, method, properties, simple_event):
        self.mask.add(simple_event)
        if self.mask.matched():
            self.retriever.stop()

    def join(self):
        self.retriever.join()


# e.g.
if __name__ == "__main__":
    file_regex = ['.*agencies.jsonl',
                  '.*caregivers.jsonl',
                  '.*care_logs.jsonl',
                  '.*clients.jsonl',
                  '.*locations.jsonl',
                  '.*shifts.jsonl',
                  '.*timezone_agencies.jsonl']
    mask = Mask([Condition("body.resource_url", file_mask) for file_mask in file_regex])
    ResourceJoin(mask).join()
    print('all conditions match')
    print(mask)
