Data Models
===========

`PyUniProt` uses `SQLAlchemy <http://www.sqlalchemy.org/>`_ to store the data in the database.
Use instance of :class:`pyhgnc.manager.query.QueryManager` to query the content of the database.

Entity–relationship model:

.. image:: _static/models/all.png
    :target: _images/all.png


.. contents::


HGNC
----

.. autoclass:: pyhgnc.manager.models.HGNC
    :members:

AliasSymbol
-----------

.. autoclass:: pyhgnc.manager.models.AliasSymbol
    :members:

AliasName
---------

.. autoclass:: pyhgnc.manager.models.AliasName
    :members:

GeneFamily
----------

.. autoclass:: pyhgnc.manager.models.GeneFamily
    :members:

RefSeq
------

.. autoclass:: pyhgnc.manager.models.RefSeq
    :members:

RGD
---

.. autoclass:: pyhgnc.manager.models.RGD
    :members:

OMIM
----

.. autoclass:: pyhgnc.manager.models.OMIM
    :members:

MGD
---

.. autoclass:: pyhgnc.manager.models.MGD
    :members:

UniProt
-------

.. autoclass:: pyhgnc.manager.models.UniProt
    :members:

CCDS
----

.. autoclass:: pyhgnc.manager.models.CCDS
    :members:

PubMed
------

.. autoclass:: pyhgnc.manager.models.PubMed
    :members:

ENA
---

.. autoclass:: pyhgnc.manager.models.ENA
    :members:

Enzyme
------

.. autoclass:: pyhgnc.manager.models.Enzyme
    :members:

LSDB
----

.. autoclass:: pyhgnc.manager.models.LSDB
    :members:

OrthologyPrediction
-------------------

.. autoclass:: pyhgnc.manager.models.OrthologyPrediction
    :members:

Database functions
==================

set_connection
--------------

.. autofunction:: pyhgnc.manager.database.set_connection

update
------

.. autofunction:: pyhgnc.manager.database.update

set_mysql_connection
--------------------

.. autofunction:: pyhgnc.manager.database.set_mysql_connection