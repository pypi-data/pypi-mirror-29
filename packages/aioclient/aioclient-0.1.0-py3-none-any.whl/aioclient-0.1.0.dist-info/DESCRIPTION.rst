aioclient
=========

*An async web client for humans*

Installation
------------

.. code:: sh

    pip install aioserver

Usage
-----

.. code:: python

    import aioclient

    async def get_example():
        status, headers, body = await aioclient.get('https://www.example.com/')
        print(body)

Changelog
---------

v0.1.0
~~~~~~

-  GET requests return ``status, headers, body`` tuples


