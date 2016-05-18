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


### Event Coordination
class Start(SimpleEvent):
    def __init__(self):
        SimpleEvent.__init__(self, event_id=0, body={'start': 'start'})


class Ping(SimpleEvent):
    def __init__(self):
        SimpleEvent.__init__(self, event_id=1, body='ping!')


class Pong(SimpleEvent):
    def __init__(self):
        SimpleEvent.__init__(self, event_id=2, body='pong!')


# represents a clock tick for centralized time coordination
class Tick(SimpleEvent):
    def __init__(self, date_time):
        SimpleEvent.__init__(self, event_id=3, body={'tick': date_time.isoformat()})


### Events
class Notification(SimpleEvent):
    def __init__(self, notification):
        SimpleEvent.__init__(self, event_id=1000, body=notification)


class Acknowledgement(SimpleEvent):
    def __init__(self, ack):
        SimpleEvent.__init__(self, event_id=9999, body=ack)


class LogMessage(SimpleEvent):
    def __init__(self, record):
        SimpleEvent.__init__(self, event_id=1001,
                             body={'message': record.msg % record.args},
                             headers={"level": record.levelname,
                                      "pathname": record.pathname,
                                      "lineno": record.lineno,
                                      "exception": record.exc_info
                                      }
                             )


class ResourceReady(SimpleEvent):
    def __init__(self, resource_url):
        SimpleEvent.__init__(self, event_id=2000,
                             body={'resource_url': resource_url}
                             )


class ResourceConsumed(SimpleEvent):
    def __init__(self, resource_url):
        SimpleEvent.__init__(self, event_id=2001, body={'resource_url': resource_url})


class Issue(SimpleEvent):
    def __init__(self, name, body={}):
        SimpleEvent.__init__(self, event_id=90, body={**{'name': name}, **body})


class Approve(SimpleEvent):
    def __init__(self, issue):
        SimpleEvent.__init__(self, event_id=91, body={'issue': issue.as_dict()})


class Deny(SimpleEvent):
    def __init__(self, issue):
        SimpleEvent.__init__(self, event_id=92, body={'issue': issue.as_dict()})


class ResourceDisposalNotification(Issue):
    def __init__(self, resource_url, disposal_time):
        Issue.__init__(self, 'resource_disposal_event', body={'resource_url': resource_url,
                                                              'disposal_time': disposal_time.isoformat()})


class ResourceDisposalApprove(Approve):
    def __init__(self, notification):
        Approve.__init__(self, notification)


class ResourceDisposalDeny(Deny):
    def __init__(self, notification):
        Deny.__init__(self, notification)


class Trigger(SimpleEvent):
    def __init__(self, event_chain_id):  # a whole other realm of ids to maintain
        SimpleEvent.__init__(self, event_id=5000, body={'event_chain_id': event_chain_id})


#### Bus Administration
class NewEvent(SimpleEvent):
    def __init__(self, event_id):
        SimpleEvent.__init__(self, event_id=10000, body={'event_id': event_id})
