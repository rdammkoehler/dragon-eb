from celery import Celery

app = Celery('tasks', backend='redis://localhost', broker='amqp://guest@localhost//')

@app.task
def blah():
    return 'blah'

@app.task
def hello_world():
    return 'hello world'

@app.task
def hello_user():
    import getpass
    return "hello %s" % getpass.getuser()
