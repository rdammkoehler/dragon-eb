class Filter:

    def __init__(self, response=True):
        self.response = response

    def accept(self, any):
        return self.response

class FilterChain(Filter):

    def __init__(self, *args):
        self.filters = list(args)

    def accept(self, json_message):
        return all([function.accept(json_message) for function in self.filters])