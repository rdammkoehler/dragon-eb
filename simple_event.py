import datetime
import json
import multiprocessing
import os
import socket

class SimpleEvent:

    def __init__(self, event_id, body=None):
        self.header = {
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
              'public_key': None
        }
        self.body = body

    def to_json(self):
        return json.JSONEncoder().encode({ 'header': self.header, 'body': self.body })

class Ping(SimpleEvent):

    def __init__(self):
        SimpleEvent.__init__(self, 1, 'ping!')

class Pong(SimpleEvent):

    def __init__(self):
        SimpleEvent.__init__(self, 2, 'pong!')
