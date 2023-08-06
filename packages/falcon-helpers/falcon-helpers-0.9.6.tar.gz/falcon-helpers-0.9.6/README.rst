.. default-role:: code
.. role:: python(code)
  :language: python

==============
Falcon Helpers
==============

A number of helpful utilities to make working with Falcon Framework a breeze.


Quickstart
----------

.. code:: sh

  $ pip install falcon-helpers


.. code::

  import falcon
  import falcon_helpers

  api = falcon.API(
    middlewares=[
      falcon_helpers.middlewares.StaticsMiddleware()
    ]
  )
