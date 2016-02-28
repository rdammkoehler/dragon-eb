import pika
import time

class RabbitClient:

    def __init__(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters('trainmaker.local'))
        self.chan = self.conn.channel()

class RabbitCommandClient(RabbitClient):

    def __init__(self):
        RabbitClient.__init__(self)
        self.chan.exchange_declare(exchange='dragon', exchange_type='topic')
        self.chan.queue_declare(queue='command')
        self.chan.queue_bind(queue='command', exchange='dragon', routing_key='dragon.command')

    def send(self, json_string):
        self.chan.basic_publish(exchange='dragon', routing_key='dragon.command',body=json_string)

    def recv(self, callback, queue='command', no_ack=True):
        self.chan.basic_consume(callback, queue=queue, no_ack=no_ack)
        return self

    def start(self):
        try:
            self.chan.start_consuming()
        except KeyboardInterrupt:
            self.chan.stop_consuming()

    def __del__(self):
        self.conn.close()

def callback(ch, method, properties, body):
    print(" [x] received %r" % body)

if __name__ == "__main__":
    RabbitCommandClient().send('{ "hello": "I am Groot!" }')
    RabbitCommandClient().recv(callback, 'command').start()
