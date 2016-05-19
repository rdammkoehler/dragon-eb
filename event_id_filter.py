from filter import Filter


class EventIdFilter(Filter):
    def __init__(self, event_id):
        self.event_id = event_id

    def accept(self, json_message):
        return self.event_id == json_message['header']['event_id']

    def __str__(self):
        return "header.event_id == %s" % self.event_id

    def __repr__(self):
        return self.__str__()


class EventIdRangeFilter(Filter):
    def __init__(self, range_start, range_end):
        self.event_id_lower_bound = range_start
        self.event_id_upper_bound = range_end

    def accept(self, json_message):
        event_id = json_message['header']['event_id']
        return self.event_id_lower_bound <= event_id and self.event_id_upper_bound >= event_id

    def __str__(self):
        return "%s <= header.event_id <= %s" % (self.event_id_lower_bound, self.event_id_upper_bound)

    def __repr__(self):
        return self.__str__()

class EventIdExclusionFilter(Filter):
    def __init__(self, event_id):
        self.excluded_id = event_id

    def accept(self, json_message):
        return self.excluded_id != json_message['header']['event_id']

    def __str__(self):
        return "header.event_id != %s" % self.excluded_id

    def __repr__(self):
        return self.__str__()

class EventIdRangeExclusionFilter(Filter):
    def __init__(self, range_start, range_end):
        self.event_id_lower_bound = range_start
        self.event_id_upper_bound = range_end

    def accept(self, json_message):
        event_id = json_message['header']['event_id']
        return self.event_id_lower_bound > event_id or self.event_id_upper_bound < event_id

    def __str__(self):
        return "%s > header.event_id > %s" % (self.event_id_lower_bound, self.event_id_upper_bound)

    def __repr__(self):
        return self.__str__()