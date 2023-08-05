prequest
========

.. image:: https://travis-ci.org/Data-Mechanics/prequest.svg?branch=master
    :target: https://travis-ci.org/Data-Mechanics/prequest

Light wrapper around the ``requests`` library that facilitates data backup to a configurable data source.

Installation
============

``prequest`` can be installed using ``pip``::

    $ pip install prequest

Usage
=====

To make a GET request::

    import prequest
    resp = prequest.get('https://your_url.com')

