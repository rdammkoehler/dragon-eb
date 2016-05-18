import time

from dragon_eb import DragonBusClient
from event_id_filter import EventIdFilter
from simple_event import Notification, Acknowledgement


class Notifier(DragonBusClient):
    def __init__(self, check_acknowledgement=False):
        self.acked = []
        if check_acknowledgement:
            DragonBusClient.__init__(self, EventIdFilter(9999))
            self.add_callback(self.__recv_ack)
            self.start()
        else:
            DragonBusClient.__init__(self)

    def notify(self, notification_dict):
        message = Notification(notification_dict).to_json()
        self.send(message)

    def __recv_ack(self, ch, method, properties, json_message):
        self.acked.append(json_message)

    def acknowledged(self, message):
        rval = False
        kill = None
        for ack in self.acked:
            if message == ack['body']['acknowledge']['body']:
                kill = ack
                rval = True
        if rval:
            self.acked.remove(kill)
        return rval


class Acknowledger(DragonBusClient):
    def ack():
        return Acknowledger().start()

    def __init__(self):
        DragonBusClient.__init__(self, EventIdFilter(1000))
        self.add_callback(self.__ack)

    def __ack(self, ch, method, properties, json_message):
        self.send(Acknowledgement({'acknowledge': json_message}).to_json())


if __name__ == "__main__":
    acker = Acknowledger.ack()
    notifier = Notifier(check_acknowledgement=True)
    for pid in range(5):
        message = {'proc': pid}
        notifier.notify(message)
        time.sleep(1)  # thanks to the GIL we need to take a nap or this contrivance won't work
        if not notifier.acknowledged(message):
            print("no ack for %s" % message)
    time.sleep(1)
