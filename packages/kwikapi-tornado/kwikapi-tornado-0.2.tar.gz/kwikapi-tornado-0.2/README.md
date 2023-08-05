# kwikapi.tornado
Quickly build API services to expose functionality in Python. `kwikapi.tornado` was built by using the functionality of KwikAPI and Tornado web server.

## Installation

```bash
$ pip install kwikapi[tornado]
```

## Usage

### Basic example to use kwikapi.tornado

sample.py
```python
import tornado.ioloop
import tornado.web

from kwikapi.tornado import RequestHandler
from kwikapi import API

class BaseCalc(object):
    def add(self, a: int, b: int) -> int:
        return a + b

    def subtract(self, a: int, b: int) -> int:
        return a - b

api = API(default_version='v1')
api.register(BaseCalc(), 'v1')

def make_app():
    return tornado.web.Application([
        (r'^/api/.*', RequestHandler, dict(api=api)),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
```

### Run script

```bash
$ python sample.py
```

### Make API request

```bash
$ curl "http://localhost:8888/api/v1/add?a=10&b=10"
```

> To know how to use all features, please refer KwikAPI documentation https://github.com/deep-compute/kwikapi/blob/master/README.md
