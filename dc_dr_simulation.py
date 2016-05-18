# This represents the interaction(s) between DC and DR tiers in Dragon
import logging


FORMAT = '%(asctime)-15s -- %(processName)-15s -- %(threadName)-10s -- %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


from mask import Condition, Mask
from resource_join import ResourceJoin
import requests


class DataRetention:
    '''receives ResourceReadyEvents and acts upon them'''

    def __init__(self):
        logging.basicConfig(format=FORMAT, level=logging.INFO)

    def __str__(self):
        return "DataRetention completed"

    def run(self):
        logging.info("starting data retention")
        file_regex = ['.*agencies.jsonl',
                      '.*caregivers.jsonl',
                      '.*care_logs.jsonl',
                      '.*clients.jsonl',
                      '.*locations.jsonl',
                      '.*shifts.jsonl',
                      '.*timezone_agencies.jsonl']
        mask = Mask([Condition("body.resource_url", file_mask) for file_mask in file_regex])
        ResourceJoin(matched_callback=self.retain_data, intermediate_callback=self.acknowledge, mask=mask).join()

    def acknowledge(self, event):
        from dragon_eb import DragonBusClient
        from simple_event import Acknowledgement

        DragonBusClient().send(Acknowledgement({'acknowledge': event}).to_json())

    def retain_data(self, joiner):
        '''we get called only if all the resources ready notifications have been received'''
        logging.info("Starting to Retain Data")
        from dragon_eb import DragonBusClient
        from simple_event import ResourceConsumed

        class ConsumptionNotifier(DragonBusClient):
            def __init__(self):
                DragonBusClient.__init__(self)

            def send_notice(self, url):
                self.send(ResourceConsumed(url).to_json())

        notifier = ConsumptionNotifier()
        try:
            failures = []
            for event in joiner.mask().events():
                url = event['body']['resource_url']
                #  the following lines simulates the consumption of the resource
                response = requests.get(url, verify='ca-chain.cert.pem')
                if response.status_code in range(200, 299):  #  TODO IRL we need to handle redirects
                    print("%s -- %s" % (url, response.text))
                    time.sleep(5)
                    notifier.send_notice(url)
                else:
                    failures.append(url)
            # TODO if one or more resources could not be fetched, we'd have to do something about it
            #      if failures is not empty we have a problem. Send a 'Retry' to the source and wait some more?
            #      \ this is a serious issue that you must resolve. We've left the Joiner, so now we need another joiner
            #      \ for resources we did not create and therefore don't know the names of.
            #      Rich: I think you made a mess.
            #      Can the server detect what was not received? I think it can because we didn't
            #      \ send a consumption notification. So how does this client recover from not
            #      \ having actually received its file?
            #      Clearly Consumption Notifier shoul be sending ACKs! But we'd still have the
            #      \ issue of consumption notifications -- not out of the woods yet.
            joiner.stop()
            logging.info("ResourceJoiner stopped -- %s" % failures)
        except:
            logging.exception("failed to retrieve resources")


from resource_ready_notifier import ResourceReadyNotifier


class DataCollection:
    '''sends resource ready events'''

    def __init__(self):
        self.receivers = []
        self.acknowledgments = []
        logging.basicConfig(format=FORMAT, level=logging.INFO)

    def __str__(self):
        return "DataCollection.receivers: %s\nDataCollection.acknowledgments: %s" % (self.receivers, self.acknowledgments)

    def run(self):
        logging.info("starting data collection")
        file_names = ['agencies.jsonl', 'caregivers.jsonl', 'care_logs.jsonl', 'clients.jsonl', 'locations.jsonl',
                  'shifts.jsonl', 'timezone_agencies.jsonl']
        notifier = ResourceReadyNotifier()
        for resource in file_names:
            url = "https://ender.noradltd.com/%s" % resource
            logging.info("Sending Resource Ready Event for %s" % url)
            self.receivers.append(self.start_listener_for(url))
            msg = notifier.notify(url)
            self.acknowledgments.append(self.start_ack_listener_for(msg))  # probable timing issue here
        #self.wait_for_all(self.acknowledgments)
        self.wait_for_all(self.receivers)
        logging.info("all ConsumptionNotifications received")

    def wait_for_all(self, receivers):
        logging.info("waiting for all %s" % receivers)
        for receiver in receivers:
            receiver.join()

    def start_listener_for(self, url):
        from dragon_eb import DragonBusClient
        from event_id_filter import EventIdFilter

        class ConsumptionReceiver(DragonBusClient):
            def __init__(self, url):
                DragonBusClient.__init__(self, EventIdFilter(2001))
                self.url = url
                self.add_callback(self.receipt)

            def receipt(self, ch, method, properties, json_message):
                logging.info("received receipt %s" % json_message)
                if self.url == json_message['body']['resource_url']:
                    self.stop()

        cr = ConsumptionReceiver(url)
        cr.start()
        return cr

    def start_ack_listener_for(self, msg):
        from dragon_eb import DragonBusClient
        from event_id_filter import EventIdFilter

        class AckListener(DragonBusClient):
            def __init__(self, msg):
                DragonBusClient.__init__(self, EventIdFilter(9999))
                self.msg = msg
                self.add_callback(self.acknowledged)

            def acknowledged(self, ch, method, properties, json_message):
                logging.info("received acknowledgement %s" % json_message)
                # if message == ack['body']['acknowledge']['body']:
                if self.msg == json_message['body']['acknowledge']['body']:
                    # TODO something important should happen here
                    print("ACK: %s" % msg)

        al = AckListener(msg)
        al.start()
        return al


from multiprocessing import Process
import time

dr = DataRetention()
dr_process = Process(target=dr.run, name='DataRetention')
dr_process.start()

time.sleep(1)  # Timing problem caused by the GIL. With the current setup the DataRetention process will miss all the DataCollection messages unless we take a nap

dc = DataCollection()
dc_process = Process(target=dc.run, name='DataCollection')
dc_process.start()

dc_process.join(10)
logging.info("DataCollection finished")
dr_process.join(10)
logging.info("DataRetention completed")
logging.info("Done")
logging.info(dr)
logging.info(dc)
