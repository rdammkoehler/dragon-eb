# DRAGON EB

An Event Bus SPIKE related to Resource Ready Event

# Setup

You will need to install the following things;

- RabbitMQ   (mac: brew install rabbitmq)
- NGINX 

Use pip to install the dependencies in requirements.txt. At the time of this writing;

pika==0.10.0
requests==2.9.1

Run:

	pip install -r requirements.txt --upgrade

# Etc

Check RabbitMQ status at [http://localhost:15672/#/](http://localhost:15672/#/)


# How to Run

- You will need RabbitMQ running for all examples
- You will need NGINX running for all examples

# Resource Ready Nofifier (RabbitMQ, NGINX)

Start RabbitMQ Server

    sudo rabbitmq-server &

NGINX:

Place a files named 'agencies.jsonl', 'caregivers.jsonl', 'care_logs.jsonl', 
'clients.jsonl', 'locations.jsonl_', 'shifts.jsonl', 
'timezone_agencies.jsonl' in the HTML root folder of NGINX


Then start NGINX

	????

Run the Example Code:

    python dc_dr_simulation.py

Result:

You will see a bunch of logging out of this. What is happening is, 
a simulated Data Collector is sending Resource Ready Events and a 
simulated Data Retention is using HTTPS to pull those files over the 
wire.

What's missing?

Things