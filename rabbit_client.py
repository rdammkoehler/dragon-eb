import pika
import time

class RabbitClient:

    def __init__(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.chan = self.conn.channel()

class RabbitCommandClient(RabbitClient):

    EXCHANGE='dragon'
    ROUTING_KEY = 'dragon.command'

    def __init__(self, exchange=EXCHANGE, routing_key=ROUTING_KEY):
        RabbitClient.__init__(self)
        self.chan.exchange_declare(exchange=exchange, type='fanout')

        result = self.chan.queue_declare(exclusive=True)
        self.queue_name = result.method.queue
        self.chan.queue_bind(exchange=exchange, queue=self.queue_name)

    def send(self, json_string, exchange=EXCHANGE, routing_key=ROUTING_KEY):
        self.chan.basic_publish(exchange=exchange, routing_key=routing_key, body=json_string)

    def recv(self, callback, no_ack=True):
        self.chan.basic_consume(callback, queue=self.queue_name, no_ack=no_ack)
        return self

    def start(self):
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
    RabbitCommandClient().send('{ "hello": "I am Groot!" }')
    RabbitCommandClient().recv(callback).start()
