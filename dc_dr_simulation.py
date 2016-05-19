# This represents the interaction(s) between DC and DR tiers in Dragon
import logging
import time
from multiprocessing import Process

import requests

from dragon_eb import DragonBusClient
from event_id_filter import EventIdRangeFilter, EventIdFilter
from mask import Condition, Mask
from resource_join import ResourceJoin
from simple_event import ResourceConsumed, ResourceIrretrievable
from simple_event import ResourceReady

# TODO this example leaks sockets on rabbit at a rate of about 8 per run (not always 8), fix!
# TODO investigate how to use a context manager in this beast (Up At Rabbit Client?) to avoid leaking

FORMAT = '%(asctime)-15s -- %(processName)-15s -- %(threadName)-10s -- %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


class DataRetention(DragonBusClient):
    '''receives ResourceReadyEvents and acts upon them'''

    def __init__(self):
        DragonBusClient.__init__(self, EventIdFilter(2000))
        logging.basicConfig(format=FORMAT, level=logging.INFO)
        self.start()

    def __str__(self):
        return "DataRetention completed"

    def run(self):
        logging.info("starting data retention")
        file_regex = ['.*agencies.jsonl', '.*caregivers.jsonl', '.*care_logs.jsonl', '.*clients.jsonl',
                      '.*locations.jsonl', '.*shifts.jsonl', '.*timezone_agencies.jsonl']
        mask = Mask([Condition("body.resource_url", file_mask) for file_mask in file_regex])
        ResourceJoin(matched_callback=self.retain_data, mask=mask).join()

    def retain_data(self, joiner):
        '''we get called only if all the resources ready notifications have been received'''
        logging.info("retain_data(%s)" % joiner)
        failures = []
        for event in joiner.mask().events():
            url = event['body']['resource_url']
            #  the following lines simulates the consumption of the resource
            response = requests.get(url, verify='ca-chain.cert.pem')
            if response.status_code in range(200, 299):  # TODO IRL we need to handle redirects
                self.send(ResourceConsumed(url).to_json())
                print("%s -- %s" % (url, response.text))
            else:
                logging.warn("failed to retrieve %s" % url)
                failures.append(url)
                self.send(ResourceIrretrievable(url).to_json())

        # TODO if one or more resources could not be fetched, we'd have to do something about it
        time.sleep(10)
        joiner.stop()


class DataCollection(DragonBusClient):
    '''sends resource ready events'''

    def __init__(self):
        DragonBusClient.__init__(self, EventIdRangeFilter(2001, 2002))
        logging.basicConfig(format=FORMAT, level=logging.INFO)
        self.receipts = []
        self.add_callback(self.receipt)
        self.start()

    def receipt(self, ch, method, properties, json_message):
        logging.info("receipt(%s) %s" % (json_message, self))
        # TODO replace with sexy dictionary of functions
        if json_message['header']['event_id'] == 2001:
            logging.info("looking for %s in %s" % (json_message['body']['resource_url'], self.receipts))
            if json_message['body']['resource_url'] in self.receipts:
                logging.info("removing %s from %s" % (json_message['body']['resource_url'], self.receipts))
                self.receipts.remove(json_message['body']['resource_url'])
        if json_message['header']['event_id'] == 2002:
            logging.info("handling fowled resource %s" % (json_message['body']['resource_url']))
            self.retransmit(json_message['body']['resource_url'])

    def __str__(self):
        return "DataCollection.receipts: %s" % self.receipts

    def run(self):
        file_names = ['agencies.jsonl', 'caregivers.jsonl', 'care_logs.jsonl', 'clients.jsonl', 'locations.jsonl_',
                      'shifts.jsonl', 'timezone_agencies.jsonl']
        for resource in file_names:
            url = "https://ender.noradltd.com/%s" % resource
            self.await(url)
            logging.info("receipts %s" % self.receipts)
            self.transmit(url)
        wait_count = 0
        while self.receipts and wait_count < 10:
            logging.info("waiting on receipts %s" % self.receipts)
            time.sleep(1)
            wait_count += 1
        logging.info("failed to complete receipts %s" % self.receipts)

    def await(self, url):
        self.receipts.append(url)

    def discard(self, url):
        self.receipts.remove(url)

    def transmit(self, url):
        self.send(ResourceReady(url).to_json())

    def retransmit(self, url):
        # Note: This is a hack for demo purposes
        new_url =url.replace("_", "")
        self.await(new_url)
        self.discard(url)
        self.transmit(new_url)


def dr_run():
    dr = DataRetention()
    dr.run()

dr_process = Process(target=dr_run, name='DataRetention')
dr_process.start()

# Timing problem caused by the GIL and/or Rabbit Client being slow to start.
# With the current setup the DataRetention process will miss
# all the DataCollection messages unless we take a nap
time.sleep(1)

def dc_run():
    dc = DataCollection()
    dc.run()

dc_process = Process(target=dc_run, name='DataCollection')
dc_process.start()

dc_process.join(10)
logging.info("DataCollection finished")
dr_process.join(10)
logging.info("DataRetention completed")
logging.info("Done")

