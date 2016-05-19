class Filter:
    def __init__(self, response=True):
        self.response = response

    def accept(self, any):
        return self.response

    def __str__(self):
        return 'True'

    def __repr__(self):
        return self.__str__()


class FilterChain(Filter):
    def __init__(self, *args):
        self.filters = list(args)

    def accept(self, json_message):
        return all([function.accept(json_message) for function in self.filters])
