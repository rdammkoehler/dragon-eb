import datetime
import json
import multiprocessing
import os
import socket


class SimpleEvent:
    def __init__(self, event_id, body=None, headers={}):
        self.event_id = int(event_id)
        self.header = {
            **{
                'event_id': event_id,
                'time': datetime.datetime.now().isoformat(),
                'host': {
                    'name': socket.gethostname(),
                    'IPv4': socket.gethostbyname(socket.gethostname())
                },
                'process': {
                    'name': multiprocessing.current_process().name,
                    'pid': os.getpid(),
                    'cwd': os.getcwd()
                },
                'schema': None,
                'encoding': 'utf-8',
                'public_key': None,
            },
            **headers
        }
        self.body = body

    def event_id(self):
        return self.event_id

    def as_dict(self):
        return {'header': self.header, 'body': self.body}

    def to_json(self):
        return json.JSONEncoder().encode(self.as_dict())

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return self.__str__()

class ResourceReady(SimpleEvent):
    def __init__(self, resource_url):
        SimpleEvent.__init__(self, event_id=2000,
                             body={'resource_url': resource_url}
                             )
