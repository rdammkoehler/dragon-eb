# to eventually move to its own world
import re

from jsonpath_rw import parse


class Condition:
    def __init__(self, expr_str, value):
        self.expr = parse(expr_str)
        self.match_value = value

    def matches(self, simple_event):
        match = self.expr.find(simple_event)
        return match and re.match(self.match_value, str(match[0].value))

    def __str__(self):
        return "%s ?? %s" % (self.expr, self.match_value)

    def __repr__(self):
        return self.__str__()


class Mask:
    def __init__(self, conditions):
        self.conditions = list(conditions)
        self._events = []
        self._matched = False


    def events(self):
        return self._events

    def add(self, simple_event):
        self._events.append(simple_event)
        self.check()

    def check(self):
        matches = 0
        for condition in self.conditions:
            for event in self._events:
                if condition.matches(event):
                    matches += 1
                    break
        self._matched = matches == len(self.conditions)

    def matched(self):
        return self._matched

    def __str__(self):
        str = []
        for condition in self.conditions:
            matching = None
            for event in self._events:
                if condition.matches(event):
                    matching = event
                    break
            if matching:
                str.append("%s == %s" % (condition, matching))
            else:
                str.append("%s unmatched" % condition)
        return '\n'.join(str)

    def __repr__(self):
        return self.__str__()


# e.g.
if __name__ == "__main__":
    from simple_event import ResourceReady

    c1 = Condition('header.event_id', '2000')  # this is silly b/c event filters did it already
    c2 = Condition('body.resource_url', 'http://inde.*')
    m = Mask([c1, c2])
    rr = ResourceReady('http://index.html')
    m.add(rr)
    print("%s" % m.matched)  # should be True
    print("-----------------")

    c1 = Condition('body.resource_url', re.compile('.*agencies.jsonl'))
    c2 = Condition('body.resource_url', re.compile('.*caregivers.*'))
    m = Mask([c1, c2])
    print("%s" % m.matched)
    rr = ResourceReady("http://localhost/agencies.jsonl")
    m.add(rr)
    print("%s" % m.matched)
    rr = ResourceReady("http://localhost/caregivers.jsonl")
    m.add(rr)
    print("%s" % m.matched)
    print("-----------------")

    c1 = Condition('body.resource_url', re.compile('.*agencies.jsonl'))
    c2 = Condition('body.resource_url', re.compile('.*caregivers.*'))
    m = Mask([c1, c2])
    print("%s" % m.matched)
    rr = ResourceReady("http://localhost/agencies.jsonl")
    m.add(rr)
    print("%s" % m.matched)
    rr = ResourceReady("http://localhost/locations.jsonl")
    m.add(rr)
    print("%s" % m.matched)
    rr = ResourceReady("http://localhost/caregivers.jsonl")
    m.add(rr)
    print("%s" % m.matched)
    print("-----------------")

    c1 = Condition('body.resource_url', re.compile('.*agencies.jsonl'))
    c2 = Condition('body.resource_url', re.compile('https://.*'))
    m = Mask([c1, c2])
    print("%s" % m.matched)
    rr = ResourceReady("https://localhost/agencies.jsonl")
    m.add(rr)
    print("%s" % m.matched)
    print("-----------------")
