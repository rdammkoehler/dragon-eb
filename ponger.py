from dragon_esb import DragonBusClient

class Ponger(DragonBusClient):

    def __init__(self):
        DragonBusClient.__init__(self)

    # def send_pong(self):
    #    self.rmq_client.send(Pong().to_json())

if __name__ == "__main__":
    Ponger().start()
