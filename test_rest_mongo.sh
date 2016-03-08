#!/bin/bash

curl --silent --output notifications.json http://127.0.0.1:28017/dragon/events/?filter_header.event_id=1000
curl --silent --output acknowledgements.json http://127.0.0.1:28017/dragon/events/?filter_header.event_id=9999
