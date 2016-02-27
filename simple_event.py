import datetime
import json
import multiprocessing
import os
import socket

class SimpleEvent:

    def __init__(self):
        self.header = {
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
              'public_key': "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxncE8JXF28pxUigzurxkmtjAw1DjNYbZR7BbJ7xdS9WU5DGBNJa4Mu0rNNp+MWPEiHlisSLPU1M/z6HF7sq3nx5mbd6oR0/Y/55s4mus7wMUOyax3hFzBHEF/bXIgeQOFOg1/1ITEAwwg2/W7xBBAMZUTgKrmC70Ai2Qf+DRXVUSZ5508STa5qK0ujm2jRaWd53E1jA6QgTolQ8AcHGrX/ICjxpKtpya06VpXOhkLG202RJSuqYos1+kLiJCPBWkf4xlM6kNBzix8CWXXtEba80CUa99ogGC8vgJpCR/Jt1mb5lgnU0NjPVzlx8SWl4h0Ld5t5rFGEETOehc/D8mNQ== rpd@noradltd.com"
        }
        self.body = None

    def to_json(self):
        return json.JSONEncoder().encode({ 'header': self.header, 'body': self.body })

class Ping(SimpleEvent):

    def __init__(self):
        SimpleEvent.__init__(self)
        self.header['event_id'] = 1
        self.body = 'ping!'

class Pong(SimpleEvent):

    def __init__(self):
        SimpleEvent.__init__(self)
        self.header['event_id'] = 2
        self.body = 'pong!'
