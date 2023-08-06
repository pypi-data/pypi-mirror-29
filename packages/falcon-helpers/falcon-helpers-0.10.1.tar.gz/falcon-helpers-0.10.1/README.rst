.. default-role:: code
.. role:: python(code)
  :language: python


.. image:: https://codecov.io/gl/skosh/falcon-helpers/branch/master/graph/badge.svg
  :target: https://codecov.io/gl/skosh/falcon-helpers

.. image:: https://gitlab.com/skosh/falcon-helpers/badges/master/pipeline.svg
  :target: https://gitlab.com/skosh/falcon-helpers/commits/master


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
