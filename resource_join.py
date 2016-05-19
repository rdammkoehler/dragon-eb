from mask import Condition, Mask
from resource_retriever import ResourceRetriever


class ResourceJoin:
    def __init__(self, matched_callback, mask, intermediate_callback=lambda event: event):
        self._callback = matched_callback
        self.intermediate_callback = intermediate_callback
        self._mask = mask
        self._retriever = ResourceRetriever(self.accept).start()

    def mask(self):
        return self._mask

    def accept(self, ch, method, properties, simple_event):
        self._mask.add(simple_event)
        self.intermediate_callback(simple_event)
        if self._mask.matched():
            self._callback(self)

    def stop(self):
        self._retriever.stop()

    def join(self):
        self._retriever.join()

    def __str__(self):
        return str(self._mask)

    def __repr__(self):
        return self.__str__()


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
