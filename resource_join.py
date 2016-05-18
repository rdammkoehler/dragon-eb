from mask import Condition, Mask
from resource_retriever import ResourceRetriever


class ResourceJoin:
    def __init__(self, callback, mask):
        self._callback = callback
        self._mask = mask
        self._retriever = ResourceRetriever(self.accept).start()

    def mask(self):
        return self._mask

    def accept(self, ch, method, properties, simple_event):
        self._mask.add(simple_event)
        if self._mask.matched():
            self._callback(self)

    def stop(self):
        self._retriever.stop()

    def join(self):
        self._retriever.join()


def blah(joiner):
    print("blah received the following events:")
    for event in joiner.mask().events():
        print(event)
    print("stopping the joiner!")
    joiner.stop()

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
    ResourceJoin(blah, mask).join()
