import pika
import time

class RabbitClient:

    def __init__(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.chan = self.conn.channel()

class RabbitCommandClient(RabbitClient):

    def __init__(self, exchange='dragon', queue='command', routing_key='dragon.command'):
        RabbitClient.__init__(self)
        self.chan.exchange_declare(exchange=exchange, type='fanout')
        self.chan.queue_declare(queue=queue)
        self.chan.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)

    def send(self, json_string, exchange='dragon', routing_key='dragon.command'):
        self.chan.basic_publish(exchange=exchange, routing_key=routing_key,body=json_string)

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

#  I don't remember what this was for, I think its all about the routing_key
class RabbitCronClient(RabbitCommandClient):

    def __init__(self, exchange='dragon', queue='cron', routing_key='dragon.cron'):
        RabbitCommandClient.__init__(self, exchange, queue, routing_key)

    def send(self, json_string, exchange='dragon', routing_key='dragon.cron'):
        RabbitCommandClient.send(self, json_string, exchange, routing_key)

    def recv(self, callback, queue='cron', no_ack=True):
        RabbitCommandClient.recv(self, callback, queue, no_ack)

def callback(ch, method, properties, body):
    print(" [x] received %r" % body)

if __name__ == "__main__":
    RabbitCommandClient().send('{ "hello": "I am Groot!" }')
    RabbitCommandClient().recv(callback, 'command').start()
