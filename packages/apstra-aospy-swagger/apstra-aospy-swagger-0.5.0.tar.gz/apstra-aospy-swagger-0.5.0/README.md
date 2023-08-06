# AOS Python Client

This Python client uses the AOS server Swagger specification to provide complete API feature
functionality.  This library will always be "up to date" with the AOS server API as a result.  Yea!  

## QuickStart

This is a short example that creates a python client to an AOS server, gets an existing
Blueprint called *pod-alpha* and obtains rack information about the blueprint.

````python
from __future__ import print_function

from aospy.swagger import Client
from aospy.swagger.groups.blueprints import Blueprints

aos = Client("https://172.20.172.3")
blueprints = Blueprints(aos)

bp = blueprints['pod-alpha']

print(bp.id)

resp, ok = aos.request.blueprints.all_racks(blueprint_id=bp.id)
````

### Installation from cloned repo

```bash
python setup.py install
```

### Installation from PyPi (comming soon!)

```bash
pip install apstra-aospy-swagger
```

## Testing

The [ptests](ptests) directory contains the py.test scripts used to test against an actual AOS system.
For details on using these py.tests, refer to the [README.md](ptests/README.md) file in that directory.