# AOS Python Swagger Client

This package contains the python client to automate the AOS Server REST API
using the servers Swagger spec.


## Install apstra-aospy-swagger

```bash
$ pip install apstra-aospy-swagger
```

## Install Jupyter Notebook (optional)

To install ipython and jupyter notebook for Python 2 systems, use the following:

```bash
$ pip install ipython==5 jupyter
```

For Python 3 systems:

```bash
$ pip install ipython jupyter
```

Once you have jupyter installed, you can start the jupyter server
on your laptop.  To you start jupyter as a background process:

```bash
$ jupyter notebook &
```

When you run the following command, you should see a web-brower open
a page to the jupyter "home" page.  From there click on "new" and then
"Python 2" to start working on your notebook:

![jupyter-notebook](docs/media/jupyter-1.jpg "Jupyter Notebook")


## QuickStart

Use `ipython` the same as you use python.  Simply enter the command get to
the ipython shell.  From there, enter the following:

```python
from aospy.swagger.client import Client

aos = Client(server_url='https://172.20.181.3')

resp, ok = aos.request.hcl.get_hcls()

for hcl_item in resp['items']:
    print hcl_item['id']
```

You can also export the `AOS_SERVER` enviornment varaible so that
you do not need to provide the `server_url` value.  For example:

```bash
$ export AOS_SERVER=172.20.181.3
$ ipython
```

And then the python code is:

```python
from aospy.swagger.client import Client

aos = Client()

resp, ok = aos.request.hcl.get_hcls()

for hcl_item in resp['items']:
    print hcl_item['id']
```


## Detailed Documentation on using Swagger Client

The AOS swagger client is built on an open-source library that 
is designed to work for any Swagger 2.0 based system.  For additional details 
refer to the project documentation
[here](https://github.com/jeremyschulman/halutz/blob/master/docs/README.md).