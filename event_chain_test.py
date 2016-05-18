from rabbit_client import RabbitCommandClient
from simple_event import Trigger


class EventChainTest():
    def __init__(self):
        self.rcc = RabbitCommandClient(exchange='dragon', routing_key='dragon.command')

    def __trigger(self, chain_id):
        self.rcc.send(json_string=Trigger(chain_id).to_json(), exchange='dragon', routing_key='dragon.command')

    def test_blah(self):
        self.__trigger(0)

    def test_hello_world(self):
        self.__trigger(1)

    def test_hello_user(self):
        self.__trigger(2)


if __name__ == '__main__':
    ect = EventChainTest()
    ect.test_blah()
    ect.test_hello_world()
    ect.test_hello_user()
