# DRAGON EB

An Event Bus SPIKE. Note, this is not the final product, its just a collection of experiements. IRL I would TDD the hell out of this.

# Setup

You will need to install the following things;

- RabbitMQ   (mac: brew install rabbitmq)
- Redis		 (mac: brew install redis)
- MongoDB	 (mac: port install mongodb)
- Apache	 (mac: already installed)

Use pip to install the dependencies in requirements.txt. At the time of this writing;

celery==3.1.22

pika==0.10.0

pymongo==3.2.1

redis==2.10.5


Run:

	pip install -r requirements.txt

# Etc

Check MongoDB status at [http://localhost:28017/](http://localhost:28017/)

Check RabbitMQ status at [http://localhost:15672/#/](http://localhost:15672/#/)


# How to Run

- You will need RabbitMQ running for all examples
- You will need MongoDB running for most examples
- You will need Redis running to execute the Celery Example(s)

# Event Chain (RabbitMQ, Redis, Celery)
Celery:

	celery -A event_chain worker --loglevel=info
	
Server Side:

	python event_chain_trigger.py

Client Side:

	python event_chain_test.py

Result:

You should see output like this;

	starting event chain 0
	blah
	starting event chain 1
	hello world
	starting event chain 2
	hello %user%

Where %user% is your user name

What's Missing?

Almost everything, this was just an attempt to connect DragonEB to Celery and see what happens.


# Deadpool (RabbitMQ, MongoDB)
MongoDB:

	mongod --rest

Server Side:

	python deadpool.py

Client Side:

	python dead_handler.py

Result:

Two messages logged into the dragon.deadpool collection of Mongo DB for the error and the critial message.

You can view the content of the deadpool at;

	[http://localhost:28017/dragon/deadpool/](http://localhost:28017/dragon/deadpool/)

Note: The trailing slash is required.

You can filter to a log level (ERROR/CRITICAL) at;

	[http://localhost:28017/dragon/deadpool/?filter_header.level=ERROR](http://localhost:28017/dragon/deadpool/?filter_header.level=ERROR)

or;

	[http://localhost:28017/dragon/deadpool/?filter_header.level=CRITICAL](http://localhost:28017/dragon/deadpool/?filter_header.level=CRITICAL)

Additional examples are in the file test_rest_mongo.sh

What's missing?

Need better handling of exceptions (not json serializable) and string value substitutions

# Logger (RabbitMQ, MongoDB)
Server Side:

	python logger.py

Client Side:
Run anything that uses a logger, dead_handler.py is a good choice. 

Result:

Messages should be logged to the dragon.log collection in Mongo DB.

What's missing?

Logger only logs event ID > 99. SysLogger logs 0-99, no example client for SysLogger.

# Notification (RabbitMQ, MongoDB)
Server Side:

	python notification.py

Client Side:
Included in the server.

Result:

You should not see any output. What's happening is the notifier is sending notifications, acknowledger is acknowledgeing them, notifier is checking to see that its messages were acknowledged.

What's missing?
Nothing really

# Registrar (RabbitMQ, MongoDB)
Server Side:

	python registrar.py

Clien Side:
Included in the server.

Result:

Registrar will complain via the command channel that various event messages were not registered. These messages are not captured by registrar so you have to setup a listener for them

What's Missing?

There is no database behind the registrar, it just keeps track in memory. IRL we want this to keep track via a database and complain about 'new events' but remember forever the old ones. 

# Resource Ready Nofifier (RabbitMQ, MongoDB, Apache)

Apache (Mac):

Place a file named README.md in /Library/WebServer/Documents

	sudo cp README.md /Library/WebServer/Documents/README.md

Then start Apache

	sudo apachectrl start

Server Side:

	python resource_retriever.py

Client Side:

	python resource_ready_nofifier.py

Result:

The content of README.md will be displayed on the screen by the server.

What's missing?

Pretty close to complete

# Ticker (RabbitMQ)

Server Side:

None.

Client Side:

	python ticker.py

Result:

A tick message will be placed on the command channel (dragon.event)

What's Missing?

A server/receiver. At some point there was such a beast but has been lost. Not sure how practical this is IRL anyway.

# Rabbit Client (RabbitMQ)

Server Side:

	python rabbit_client.py

Client Side:

Included in Server Side.

Result:

On STDOUT you should see the following;

	 [x] received b'{ "hello": "I am Groot!" }'

What's Missing?

Nothing.

# Ping-Pong Example (RabbitMQ) [out of date]

Start the server side

	python ponger.py &

Start the client side

	python pinger.py

Go look in the db! Ponger should have written a json message into a database named dragon and a collection named events. The message should look a little like the contents of 'simple event message example.json'. Some real ones from my db look like this;

```json
{ "_id" : ObjectId("56d10716073dcb6e71806d8b"), "header" : { "event_id" : 1, "host" : { "name" : "thought.local", "IPv4" : "10.0.1.214" }, "process" : { "pid" : 28277, "name" : "MainProcess", "cwd" : "/Users/rich/projects/HISC/spikes/simpleevent" }, "schema" : null, "encoding" : "utf-8", "time" : "2016-02-26T20:16:53.994478", "public_key" : "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxncE8JXF28pxUigzurxkmtjAw1DjNYbZR7BbJ7xdS9WU5DGBNJa4Mu0rNNp+MWPEiHlisSLPU1M/z6HF7sq3nx5mbd6oR0/Y/55s4mus7wMUOyax3hFzBHEF/bXIgeQOFOg1/1ITEAwwg2/W7xBBAMZUTgKrmC70Ai2Qf+DRXVUSZ5508STa5qK0ujm2jRaWd53E1jA6QgTolQ8AcHGrX/ICjxpKtpya06VpXOhkLG202RJSuqYos1+kLiJCPBWkf4xlM6kNBzix8CWXXtEba80CUa99ogGC8vgJpCR/Jt1mb5lgnU0NjPVzlx8SWl4h0Ld5t5rFGEETOehc/D8mNQ== rpd@noradltd.com" }, "body" : "ping!" }
{ "_id" : ObjectId("56d1078f073dcb6eda67c802"), "header" : { "schema" : null, "encoding" : "utf-8", "event_id" : 1, "public_key" : "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxncE8JXF28pxUigzurxkmtjAw1DjNYbZR7BbJ7xdS9WU5DGBNJa4Mu0rNNp+MWPEiHlisSLPU1M/z6HF7sq3nx5mbd6oR0/Y/55s4mus7wMUOyax3hFzBHEF/bXIgeQOFOg1/1ITEAwwg2/W7xBBAMZUTgKrmC70Ai2Qf+DRXVUSZ5508STa5qK0ujm2jRaWd53E1jA6QgTolQ8AcHGrX/ICjxpKtpya06VpXOhkLG202RJSuqYos1+kLiJCPBWkf4xlM6kNBzix8CWXXtEba80CUa99ogGC8vgJpCR/Jt1mb5lgnU0NjPVzlx8SWl4h0Ld5t5rFGEETOehc/D8mNQ== rpd@noradltd.com", "time" : "2016-02-26T20:18:55.388776", "process" : { "name" : "MainProcess", "pid" : 28382, "cwd" : "/Users/rich/projects/HISC/spikes/simpleevent" }, "host" : { "name" : "thought.local", "IPv4" : "10.0.1.214" } }, "body" : "ping!" }
{ "_id" : ObjectId("56d10791073dcb6eda67c803"), "header" : { "schema" : null, "encoding" : "utf-8", "event_id" : 1, "public_key" : "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxncE8JXF28pxUigzurxkmtjAw1DjNYbZR7BbJ7xdS9WU5DGBNJa4Mu0rNNp+MWPEiHlisSLPU1M/z6HF7sq3nx5mbd6oR0/Y/55s4mus7wMUOyax3hFzBHEF/bXIgeQOFOg1/1ITEAwwg2/W7xBBAMZUTgKrmC70Ai2Qf+DRXVUSZ5508STa5qK0ujm2jRaWd53E1jA6QgTolQ8AcHGrX/ICjxpKtpya06VpXOhkLG202RJSuqYos1+kLiJCPBWkf4xlM6kNBzix8CWXXtEba80CUa99ogGC8vgJpCR/Jt1mb5lgnU0NjPVzlx8SWl4h0Ld5t5rFGEETOehc/D8mNQ== rpd@noradltd.com", "time" : "2016-02-26T20:18:57.415026", "process" : { "name" : "MainProcess", "pid" : 28386, "cwd" : "/Users/rich/projects/HISC/spikes/simpleevent" }, "host" : { "name" : "thought.local", "IPv4" : "10.0.1.214" } }, "body" : "ping!" }
{ "_id" : ObjectId("56d10792073dcb6eda67c804"), "header" : { "schema" : null, "encoding" : "utf-8", "process" : { "name" : "MainProcess", "pid" : 28390, "cwd" : "/Users/rich/projects/HISC/spikes/simpleevent" }, "public_key" : "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxncE8JXF28pxUigzurxkmtjAw1DjNYbZR7BbJ7xdS9WU5DGBNJa4Mu0rNNp+MWPEiHlisSLPU1M/z6HF7sq3nx5mbd6oR0/Y/55s4mus7wMUOyax3hFzBHEF/bXIgeQOFOg1/1ITEAwwg2/W7xBBAMZUTgKrmC70Ai2Qf+DRXVUSZ5508STa5qK0ujm2jRaWd53E1jA6QgTolQ8AcHGrX/ICjxpKtpya06VpXOhkLG202RJSuqYos1+kLiJCPBWkf4xlM6kNBzix8CWXXtEba80CUa99ogGC8vgJpCR/Jt1mb5lgnU0NjPVzlx8SWl4h0Ld5t5rFGEETOehc/D8mNQ== rpd@noradltd.com", "time" : "2016-02-26T20:18:58.425016", "event_id" : 1, "host" : { "name" : "thought.local", "IPv4" : "10.0.1.214" } }, "body" : "ping!" }
{ "_id" : ObjectId("56d10793073dcb6eda67c805"), "header" : { "schema" : null, "encoding" : "utf-8", "process" : { "name" : "MainProcess", "pid" : 28394, "cwd" : "/Users/rich/projects/HISC/spikes/simpleevent" }, "host" : { "name" : "thought.local", "IPv4" : "10.0.1.214" }, "time" : "2016-02-26T20:18:59.401086", "event_id" : 1, "public_key" : "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxncE8JXF28pxUigzurxkmtjAw1DjNYbZR7BbJ7xdS9WU5DGBNJa4Mu0rNNp+MWPEiHlisSLPU1M/z6HF7sq3nx5mbd6oR0/Y/55s4mus7wMUOyax3hFzBHEF/bXIgeQOFOg1/1ITEAwwg2/W7xBBAMZUTgKrmC70Ai2Qf+DRXVUSZ5508STa5qK0ujm2jRaWd53E1jA6QgTolQ8AcHGrX/ICjxpKtpya06VpXOhkLG202RJSuqYos1+kLiJCPBWkf4xlM6kNBzix8CWXXtEba80CUa99ogGC8vgJpCR/Jt1mb5lgnU0NjPVzlx8SWl4h0Ld5t5rFGEETOehc/D8mNQ== rpd@noradltd.com" }, "body" : "ping!" }
{ "_id" : ObjectId("56d10799073dcb6eda67c806"), "header" : { "schema" : null, "encoding" : "utf-8", "process" : { "name" : "MainProcess", "pid" : 28406, "cwd" : "/Users/rich/projects/HISC/spikes/simpleevent" }, "public_key" : "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxncE8JXF28pxUigzurxkmtjAw1DjNYbZR7BbJ7xdS9WU5DGBNJa4Mu0rNNp+MWPEiHlisSLPU1M/z6HF7sq3nx5mbd6oR0/Y/55s4mus7wMUOyax3hFzBHEF/bXIgeQOFOg1/1ITEAwwg2/W7xBBAMZUTgKrmC70Ai2Qf+DRXVUSZ5508STa5qK0ujm2jRaWd53E1jA6QgTolQ8AcHGrX/ICjxpKtpya06VpXOhkLG202RJSuqYos1+kLiJCPBWkf4xlM6kNBzix8CWXXtEba80CUa99ogGC8vgJpCR/Jt1mb5lgnU0NjPVzlx8SWl4h0Ld5t5rFGEETOehc/D8mNQ== rpd@noradltd.com", "time" : "2016-02-26T20:19:05.446384", "event_id" : 1, "host" : { "name" : "thought.local", "IPv4" : "10.0.1.214" } }, "body" : "ping!" }
{ "_id" : ObjectId("56d1079c073dcb6eda67c807"), "header" : { "schema" : null, "encoding" : "utf-8", "event_id" : 1, "public_key" : "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxncE8JXF28pxUigzurxkmtjAw1DjNYbZR7BbJ7xdS9WU5DGBNJa4Mu0rNNp+MWPEiHlisSLPU1M/z6HF7sq3nx5mbd6oR0/Y/55s4mus7wMUOyax3hFzBHEF/bXIgeQOFOg1/1ITEAwwg2/W7xBBAMZUTgKrmC70Ai2Qf+DRXVUSZ5508STa5qK0ujm2jRaWd53E1jA6QgTolQ8AcHGrX/ICjxpKtpya06VpXOhkLG202RJSuqYos1+kLiJCPBWkf4xlM6kNBzix8CWXXtEba80CUa99ogGC8vgJpCR/Jt1mb5lgnU0NjPVzlx8SWl4h0Ld5t5rFGEETOehc/D8mNQ== rpd@noradltd.com", "time" : "2016-02-26T20:19:08.352281", "process" : { "name" : "MainProcess", "pid" : 28410, "cwd" : "/Users/rich/projects/HISC/spikes/simpleevent" }, "host" : { "name" : "thought.local", "IPv4" : "10.0.1.214" } }, "body" : "ping!" }
{ "_id" : ObjectId("56d109f7073dcb72468780a4"), "header" : { "process" : { "cwd" : "/Users/rich/projects/HISC/spikes/simpleevent", "pid" : 29271, "name" : "MainProcess" }, "schema" : null, "public_key" : "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxncE8JXF28pxUigzurxkmtjAw1DjNYbZR7BbJ7xdS9WU5DGBNJa4Mu0rNNp+MWPEiHlisSLPU1M/z6HF7sq3nx5mbd6oR0/Y/55s4mus7wMUOyax3hFzBHEF/bXIgeQOFOg1/1ITEAwwg2/W7xBBAMZUTgKrmC70Ai2Qf+DRXVUSZ5508STa5qK0ujm2jRaWd53E1jA6QgTolQ8AcHGrX/ICjxpKtpya06VpXOhkLG202RJSuqYos1+kLiJCPBWkf4xlM6kNBzix8CWXXtEba80CUa99ogGC8vgJpCR/Jt1mb5lgnU0NjPVzlx8SWl4h0Ld5t5rFGEETOehc/D8mNQ== rpd@noradltd.com", "event_id" : 1, "host" : { "IPv4" : "10.0.1.214", "name" : "thought.local" }, "encoding" : "utf-8", "time" : "2016-02-26T20:29:11.158313" }, "body" : "ping!" }
{ "_id" : ObjectId("56d109fa073dcb72468780a5"), "header" : { "process" : { "cwd" : "/Users/rich/projects/HISC/spikes/simpleevent", "pid" : 29280, "name" : "MainProcess" }, "schema" : null, "public_key" : "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxncE8JXF28pxUigzurxkmtjAw1DjNYbZR7BbJ7xdS9WU5DGBNJa4Mu0rNNp+MWPEiHlisSLPU1M/z6HF7sq3nx5mbd6oR0/Y/55s4mus7wMUOyax3hFzBHEF/bXIgeQOFOg1/1ITEAwwg2/W7xBBAMZUTgKrmC70Ai2Qf+DRXVUSZ5508STa5qK0ujm2jRaWd53E1jA6QgTolQ8AcHGrX/ICjxpKtpya06VpXOhkLG202RJSuqYos1+kLiJCPBWkf4xlM6kNBzix8CWXXtEba80CUa99ogGC8vgJpCR/Jt1mb5lgnU0NjPVzlx8SWl4h0Ld5t5rFGEETOehc/D8mNQ== rpd@noradltd.com", "event_id" : 1, "host" : { "IPv4" : "10.0.1.214", "name" : "thought.local" }, "encoding" : "utf-8", "time" : "2016-02-26T20:29:14.123708" }, "body" : "ping!" }
```

