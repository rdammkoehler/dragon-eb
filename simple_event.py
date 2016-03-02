import datetime
import json
import multiprocessing
import os
import socket

class SimpleEvent:

    def __init__(self, event_id, body=None):
        self.event_id = int(event_id)  # basically need this to be a required and an int
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

    def event_id(self):
        return self.event_id

    def to_json(self):
        return json.JSONEncoder().encode({ 'header': self.header, 'body': self.body })

class Start(SimpleEvent):

  def __init__(self):
    SimpleEvent.__init__(self, 0, { 'start' : 'start'})
    
class Ping(SimpleEvent):

    def __init__(self):
        SimpleEvent.__init__(self, 1, 'ping!')

class Pong(SimpleEvent):

    def __init__(self):
        SimpleEvent.__init__(self, 2, 'pong!')

#  represents a clock tick for centralized time coordination
class Tick(SimpleEvent):

    def __init__(self, date_time):
        SimpleEvent.__init__(self, 3, { 'tick': date_time.isoformat() })

class Notification(SimpleEvent):

  def __init__(self, notification):
    SimpleEvent.__init__(self, 1000, notification)

class Acknowledgement(SimpleEvent):

  def __init__(self, ack):
    SimpleEvent.__init__(self, 9999, ack)