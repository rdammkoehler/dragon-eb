import pika
import threading
import time

class RabbitClient:

    def __init__(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.chan = self.conn.channel()

class RabbitCommandClient(RabbitClient):

    def __init__(self, exchange, routing_key):
        RabbitClient.__init__(self)
        self.chan.exchange_declare(exchange=exchange, type='fanout')

        result = self.chan.queue_declare(exclusive=True)
        self.queue_name = result.method.queue
        self.chan.queue_bind(exchange=exchange, queue=self.queue_name)

    def send(self, json_string, exchange, routing_key):
        try:
            self.chan.basic_publish(exchange=exchange, routing_key=routing_key, body=json_string)
        except pika.exceptions.ChannelClosed:
            print('ChannelClosed: dropped %s' % json_string)

    def recv(self, callback, no_ack=True):
        self.chan.basic_consume(callback, queue=self.queue_name, no_ack=no_ack)
        return self

    def start(self):
        reg_thread = threading.Thread(target=self.__start)
        reg_thread.setDaemon(True)
        reg_thread.start()
        return reg_thread

    def __start(self):
        try:
            self.chan.start_consuming()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.chan.stop_consuming()

    def __del__(self):
        self.stop()
        self.conn.close()

def callback(ch, method, properties, body):
    print(" [x] received %r" % body)

if __name__ == "__main__":
    RabbitCommandClient(exchange='test', routing_key='test.routing_key').recv(callback).start()
    RabbitCommandClient(exchange='test', routing_key='test.routing_key').send(json_string='{ "hello": "I am Groot!" }', exchange='test', routing_key='test.routing_key')
    
