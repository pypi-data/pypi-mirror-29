# bus-sdk-python

[![Build Status](https://alfred.elifesciences.org/buildStatus/icon?job=library-bus-sdk-python)](https://alfred.elifesciences.org/job/library-bus-sdk-python/) [![Coverage Status](https://coveralls.io/repos/github/elifesciences/bus-sdk-python/badge.svg?branch=HEAD)](https://coveralls.io/github/elifesciences/bus-sdk-python?branch=HEAD)

This library provides a Python SDK for the [eLife Sciences Bus](https://github.com/elifesciences/bus).
    

Dependencies
------------

* Python >=3.5

Installation
------------

`pip install elife_bus_sdk`

Publisher
---------

Configuration:

```python
from elife_bus_sdk import get_publisher

config = {
    'region': 'us-east-2',
    'subscriber': '00000000000',       
    'name': 'profile',
    'env': 'prod'
}

publisher = get_publisher(pub_name='test', pub_type='sns', config=config)
```
