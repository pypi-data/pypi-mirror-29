python-linode-api
=================

The official python library for the `Linode API v4`_ in python.

.. image:: https://travis-ci.org/linode/python-linode-api.svg?branch=master
    :target: https://travis-ci.org/linode/python-linode-api

.. image:: https://badge.fury.io/py/linode-api.svg
    :target: https://badge.fury.io/py/linode-api

Installation
------------
::

    pip install linode-api

Building from Source
--------------------

To build and install this package:

- Clone this repository
- ``./setup.py install``

This package uses the ``linode`` namespace.  This could conflict with libraries
intended for previous versions of the Linode API.  Please be cautious when
installing packages for both version of the API on the same machine.

Usage
-----

Check out the `Getting started with Linode Python`_ guide to start using the official Python library. Read our `Python Reference`_ for extensive documentation on this library.

Examples
--------

See the `Install on a Linode`_ example project for a simple use case demonstrating
many of the features of this library.

.. _Linode API v4: https://developers.linode.com/v4/introduction
.. _Install on a Linode: https://github.com/linode/python-api/tree/master/examples/install-on-linode
.. _Getting started with Linode Python: https://developers.linode.com/v4/guides/python/getting-started
.. _Python Reference: https://developers.linode.com/v4/libraries/python
