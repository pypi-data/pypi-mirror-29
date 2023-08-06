A RabbitMQ consumer plugin for the helga chat bot
=================================================

About
-----

Helga is a Python chat bot. Full documentation can be found at
http://helga.readthedocs.org.

This plugin is meant to be a simple interface *for other plugins*, sending
message bus events via ``smokesignal`` so that they can be consumed.

There is currently no command, just enough to connect to a remote RabbitMQ
instance and setup channels to listen on specific routing keys.

Installation
------------
This plugin is `available from PyPI <https://pypi.python.org/pypi/helga-pika>`_,
so you can simply install it with ``pip``::

  pip install helga-pika

If you want to hack on the helga-pika source code, in your virtualenv where
you are running Helga, clone a copy of this repository from GitHub and run
``python setup.py develop``.

Configuration
-------------
In your ``settings.py`` file (or whatever you pass to ``helga --settings``),
you must the following required keys::

    RABBITMQ_USER = "user"
    RABBITMQ_PASSWORD= "secret"
    RABBITMQ_HOST = "localhost"
    RABBITMQ_EXCHANGE= "exchange"

The port is entirely optional, defaulting to ``5672``::

    RABBITMQ_PORT = 5672

Optionally, the *interesting* routing keys must be set, so that the queues can
be correctly setup for listening::

    RABBITMQ_ROUTING_KEYS = [
        "ceph-volume.prs",
        "ceph-volume.builds",
        "ceph-volume.repos",
        "ceph.prs",
        "ceph.builds",
        "ceph.repos",
    ]
