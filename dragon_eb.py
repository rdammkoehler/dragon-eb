import json

from rabbit_client import RabbitCommandClient

class DragonBusClient:

    def __init__(self):
        self.rmq_client = RabbitCommandClient()
        self.rmq_client.recv(callback=self.on_message)
        self.callbacks = []
        self.listens_for = {}
        self.ignore = {}

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def listen_for(self, key, value):
        if self.listens_for and key in self.listens_for:
            self.listens_for[key].append(value)
        else:
            self.listens_for[key] = [value]

    def ignores(self, key, value):
        if self.ignore and key in self.ignore:
            self.ignore[key].append(value)
        else:
            self.ignore[key] = [value]

    def start(self):
        self.rmq_client.start()

    def send(self, json_string):
        self.rmq_client.send(json_string)

    def on_message(self, ch, method, properties, message):
        json_message = json.loads(message.decode('utf-8'))
        if not self.ignored(json_message) and self.accepted(json_message):
            for callback in self.callbacks:
                callback(ch, method, properties, json_message)

    def accepted(self, json_message):
        return self.__contains(self.listens_for, json_message)

    def ignored(self, json_message):
        return self.__contains(self.ignore, json_message)

    def __contains(self, kvp, json_message):
        rval = False
        if type(json_message) is dict:
            for key, values in kvp.items():
                if key in json_message:
                    for value in values:
                        if json_message[key] == value:
                            rval = True
                else:
                    for json_key in json_message:
                        rval = rval or self.__contains(kvp, json_message[json_key])
        return rval        
