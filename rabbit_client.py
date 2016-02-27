import pika
import time

class RabbitClient:

    def __init__(self):
        #cred = pika.PlainCredentials('guest','guest')
        #time.sleep(0.01)
        self.conn = pika.BlockingConnection(pika.ConnectionParameters('10.0.1.233'))
        self.chan = self.conn.channel()

class RabbitCommandClient(RabbitClient):

    def __init__(self):
        RabbitClient.__init__(self)
        self.chan.queue_declare(queue='command')

    def send(self, json_string):
        self.chan.basic_publish(exchange='', routing_key='command',body=json_string)

    def recv(self, callback, queue='command', no_ack=True):
        self.chan.basic_consume(callback, queue=queue, no_ack=no_ack)
        return self

    def start(self):
        self.chan.start_consuming()

    def __del__(self):
        self.conn.close()

def callback(ch, method, properties, body):
    print(" [x] received %r" % body)

if __name__ == "__main__":
    RabbitCommandClient().send('{ "hello": "I am Groot!" }')
    RabbitCommandClient().recv(callback, 'command').start()
