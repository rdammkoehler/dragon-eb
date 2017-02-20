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

# Ping-Pong Example (RabbitMQ, MongoDB)

Start the server side

	python logger.py &
	python ponger.py &

Start the client side

	python pinger.py

Go look in the db! 

[http://localhost:28017/dragon/sys/](http://localhost:28017/dragon/sys/)

Ponger should have written a json message into a database named dragon and a collection named sys. The message should look a little like the contents of 'simple event message example.json'. Some real ones from my db look like this;

```json
{
	offset: 0,
	rows: [
			{
				_id: {
						$oid: "56df2637073dcb2252d7c9c1"
				},
				body: {
					start: "start"
				},
				header: {
					public_key: null,
					encoding: "utf-8",
					event_id: 0,
					host: {
						IPv4: "10.0.1.214",
						name: "thought.local"
					},
					time: "2016-03-08T13:21:27.234596",
					schema: null,
					process: {
						name: "MainProcess",
						cwd: "/Users/rich/projects/HISC/spikes/simpleevent",
						pid: 74472
					}
				}
			},
			{
				_id: {
						$oid: "56df2637073dcb2252d7c9c4"
				},
				body: "ping!",
				header: {
					public_key: null,
					encoding: "utf-8",
					event_id: 1,
					host: {
						IPv4: "10.0.1.214",
						name: "thought.local"
					},
					time: "2016-03-08T13:21:27.235895",
					schema: null,
					process: {
						name: "MainProcess",
						cwd: "/Users/rich/projects/HISC/spikes/simpleevent",
						pid: 74472
					}
				}
			},
			{
				_id: {
						$oid: "56df2637073dcb2252d7c9c6"
				},
				body: "pong!",
				header: {
					public_key: null,
					encoding: "utf-8",
					event_id: 2,
					host: {
						IPv4: "10.0.1.214",
						name: "thought.local"
					},
					time: "2016-03-08T13:21:27.237287",
					schema: null,
					process: {
						name: "MainProcess",
						cwd: "/Users/rich/projects/HISC/spikes/simpleevent",
						pid: 74472
					}
				}
			},
			{
				_id: {
						$oid: "56df2637073dcb2252d7c9c8"
				},
				body: {
					tick: "2016-03-08T13:21:27.239166"
				},
				header: {
					public_key: null,
					encoding: "utf-8",
					event_id: 3,
					host: {
						IPv4: "10.0.1.214",
						name: "thought.local"
					},
					time: "2016-03-08T13:21:27.239185",
					schema: null,
					process: {
						name: "MainProcess",
						cwd: "/Users/rich/projects/HISC/spikes/simpleevent",
						pid: 74472
					}
				}
			},
			{
				_id: {
						$oid: "56df59f6073dcb86327ff690"
				},
				body: "ping!",
				header: {
					encoding: "utf-8",
					public_key: null,
					host: {
						IPv4: "10.0.1.214",
						name: "thought.local"
					},
					time: "2016-03-08T17:02:14.349381",
					event_id: 1,
					process: {
						cwd: "/Users/rich/projects/HISC/spikes/simpleevent",
						pid: 99935,
						name: "MainProcess"
					},
					schema: null
				}
			},
			{
				_id: {
						$oid: "56df59f6073dcb86327ff691"
				},
				body: "pong!",
				header: {
					encoding: "utf-8",
					public_key: null,
					host: {
						IPv4: "10.0.1.214",
						name: "thought.local"
					},
					time: "2016-03-08T17:02:14.351607",
					event_id: 2,
					process: {
						cwd: "/Users/rich/projects/HISC/spikes/simpleevent",
						pid: 99922,
						name: "MainProcess"
					},
					schema: null
				}
			}
	],
	total_rows: 6,
	query: { },
	millis: 0
}
```

Lots of changes
