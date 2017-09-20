Query
=====

.. contents::

Query interface
---------------

PyHGNC provides a powerfull query interface for the stored data. It can be accessed from python shell:

.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

You can use the query interface instance to issue a query to any model defined in :class:`pyhgnc.manager.models`:

.. code-block:: python

    # Issue query on hgnc table:
    query.hgnc()

    # Issue query on pubmed table:
    query.pubmed()

.. hint::
    See :doc:`query_functions` for more examples and check out :class:`pyhgnc.manager.query.QueryManager` (below) for
    all possible parameters for the different models.

Query Manager Reference
-----------------------

.. autoclass:: pyhgnc.manager.query.QueryManager
    :members:

