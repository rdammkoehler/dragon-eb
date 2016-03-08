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
        self.send(LogMessage(record).to_json())

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(DeadHandler())
    logger.debug("Test Debugging")
    logger.info("And Test %s" % logging.INFO)
    logger.warn("Be Warned")
    logger.error("This is power")
    logger.critical("to slay processess")
