# DRAGON ESB

Not really an ESB so much as an event client/server pair example for a spike

# How to Run


Start the server side

	python ponger.py &

Start the client side

	python pinger.py

Go look in the db!

# Setup Bits

You need RabbitMQ and MongoDB with default configs.

In my case I had to put RabbitMQ on my linux box (trainmaker) who is at 10.0.1.233, so you will need to change rabbit_client.py to point to your RabbitMQ Server. This isn't parameterized because this is a spike.
