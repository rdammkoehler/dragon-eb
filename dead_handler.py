import logging

from dragon_eb import DragonBusClient
from simple_event import LogMessage

class DeadHandler(DragonBusClient, logging.Handler):

    def __init__(self):
        DragonBusClient.__init__(self)
        self.level = 0
        self.filters = []
        self.lock = 0

    def emit(self, record):
        message = LogMessage(record).to_json()
        self.send(message)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    dh = DeadHandler()
    logger.addHandler(dh)
    logger.debug("Test Debugging")
    logger.info("And Test %s" % logging.INFO)
    logger.warn("Be Warned")
    logger.error("This is power")
    logger.critical("to slay processess")
    dh = None
