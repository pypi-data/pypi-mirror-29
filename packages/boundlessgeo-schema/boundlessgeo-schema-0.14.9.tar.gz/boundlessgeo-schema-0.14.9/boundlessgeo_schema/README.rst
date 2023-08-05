boundlessgeo-schema
-------------------

This package will convert the packaged actions.json to a dictionary.
By convention, Actions can be Queries or Commands in a
`CQRS <https://martinfowler.com/bliki/CQRS.html>`_ architecture.

Installation

.. code::

    pip install boundlessgeo-schema

Usage

.. code::

    >>> import boundlessgeo_schema as bs
    >>> schema = bs.get_schema()
    >>> import_command = schema['SPATIALIO_IMPORT']
    >>> print(import_command)
    'v1/SPATIALIO_IMPORT'
    >>> events = bs.get_events()
    >>> event = events['NO_LAYERS_FOUND']
    >>> print(event)
    'v1/NO_LAYERS_FOUND'
