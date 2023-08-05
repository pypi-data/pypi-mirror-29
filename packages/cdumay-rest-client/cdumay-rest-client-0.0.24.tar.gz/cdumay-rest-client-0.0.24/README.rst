.. image:: https://travis-ci.org/cdumay/cdumay-rest-client.svg?branch=master
    :target: https://travis-ci.org/cdumay/cdumay-rest-client

cdumay-rest-client
==================

This library is a basic REST client with exception formatting.

Quickstart
----------

First, install cdumay-rest-client using 
`pip <https://pip.pypa.io/en/stable/>`_:

    $ pip install flask-zookeeper

Next, add a `RESTClient` instance to your code:

.. code-block:: python

    import json, sys
    from cdumay_rest_client.client import RESTClient

    client = RESTClient(server="http://jsonplaceholder.typicode.com")
    json.dump(
        client.do_request(method="GET", path="/posts/1"),
        sys.stdout,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )

Result:

.. code-block:: python

    {
        "body": "quia et suscipit\nsuscipit recusandae [...]",
        "id": 1,
        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
        "userId": 1
    }

Exception
---------

You can use `marshmallow <https://marshmallow.readthedocs.io/en/latest>`_
to serialize exceptions:

.. code-block:: python

    import json, sys
    from cdumay_rest_client.client import RESTClient
    from cdumay_rest_client.exceptions import HTTPException, HTTPExceptionValidator

    try:
        client = RESTClient(server="http://jsonplaceholder.typicode.com")
        data = client.do_request(method="GET", path="/me")
    except HTTPException as exc:
        data = HTTPExceptionValidator().dump(exc).data

    json.dump(data, sys.stdout, sort_keys=True, indent=4, separators=(',', ': '))

Result:

.. code-block:: python

    {
        "code": 404,
        "extra": {},
        "message": "Not Found"
    }

License
-------

Apache License 2.0