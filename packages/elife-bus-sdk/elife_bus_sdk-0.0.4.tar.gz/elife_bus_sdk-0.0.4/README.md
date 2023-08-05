# bus-sdk-python

[![Build Status](https://alfred.elifesciences.org/buildStatus/icon?job=library-bus-sdk-python)](https://alfred.elifesciences.org/job/library-bus-sdk-python/) [![Coverage Status](https://coveralls.io/repos/github/elifesciences/bus-sdk-python/badge.svg?branch=HEAD)](https://coveralls.io/github/elifesciences/bus-sdk-python?branch=HEAD)

This library provides a Python SDK for the [eLife Sciences Bus](https://github.com/elifesciences/bus).
    

Dependencies
------------

* Python >=3.5

Installation
------------

`pip install elife_bus_sdk`

AWS Credentials
---------------
To use any of the AWS provided services through this library, you will need to provide credentials in a way that is supported [here.](http://boto3.readthedocs.io/en/latest/guide/configuration.html) 


Publisher
---------

Current supported:
- [SNS](https://aws.amazon.com/sns/)

Configuration:

```python
from elife_bus_sdk import get_publisher

config = {
    'region': 'us-east-2',
    'subscriber': '00000000000',       
    'name': 'profile',
    'env': 'dev'
}

publisher = get_publisher(config=config, pub_type='sns')
print(publisher.arn)
>>> 'arn:aws:sns:us-east-2:00000000000:profile--dev'
```

Publish:

```python
from elife_bus_sdk.events import Event

publisher.publish(Event(foo='bar', some='fields'))

```

Queue
---------

Current supported:
- [SQS](https://aws.amazon.com/sqs/)


Configuration:

```python
from elife_bus_sdk import get_queue

config = {   
    'queue_name': 'some_queue',
}

message_queue = get_queue(config=config, pub_type='sqs')
```

Poll for messages:
```python
for msg in message_queue.poll():
    print(msg)
```

Check if a queue is polling:
```python
message_queue.is_polling()
```

Stop a queue from polling (normally running in another thread):
```python
message_queue.stop_polling()
```

Receive message(s):
```python
msg = message_queue.dequeue()
```

Send message:
```python
message_queue.enqueue('test message')
```

Local Testing
-------------
To test the `aws` services locally you can setup [goaws](https://github.com/p4tin/goaws) and pass the local `endpoint_url` value to your configuration.

Example:

```python
from elife_bus_sdk import get_queue

dev_config = {
    'endpoint_url': 'http://localhost:4100',
    'queue_name': 'test1',
}

message_queue = get_queue(config=dev_config, q_type='sqs')
```

Tests
-----

You can run the full automated test suite from the base folder with:

`$ ./project_tests.sh`