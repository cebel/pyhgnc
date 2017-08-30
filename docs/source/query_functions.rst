Query functions
===============

.. contents::

Before you query
----------------

1. You can use % as a wildcard.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    # exact search
    query.hgnc(name='amyloid beta precursor protein')

    # starts with 'amyloid beta'
    query.hgnc(name='amyloid beta %')

    # ends with 'precursor protein'
    query.hgnc(name='% precursor protein')

    # contains 'precursor'
    query.hgnc(name='%precursor%')

2. `limit` to restrict number of results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    query.hgnc(limit=10)

Use an offset by paring a tuple `(page_number, number_of_results_per_page)` to the parameter `limit`.

`page_number` starts with 0!

.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    # first page with 3 results (every page have 3 results)
    query.hgnc(limit=(0,3))
    # fourth page with 10 results (every page have 10 results)
    query.hgnc(limit=(4,10))


3. Return :class:`pandas.DataFrame` as result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is very useful if you want to profit from amazing pandas functions.

.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    query.hgnc(as_df=True)


4. show all columns as dict
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    first_entry = query.hgnc(limit=1)[0]
    first_entry.to_dict()

5. Return single values with key name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    query.hgnc(name='%kinase')[0].name

6. Access to the linked data models (1-n, n-m)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From results of `pyhgnc.query().hgnc()` you can access

- alias_symbols
- alias_names
- rgds
- omims
- ccdss
- lsdbs
- orthology_predictions
- enzymes
- gene_families
- refseq_accessions
- mgds
- uniprots
- pubmeds
- enas

.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    r = query.hgnc(limit=1)[0]

    r.alias_symbols
    r.alias_names
    r.rgds
    r.omims
    r.ccdss
    r.lsdbs
    r.orthology_predictions
    r.enzymes
    r.gene_families
    r.refseq_accessions
    r.mgds
    r.uniprots
    r.pubmeds
    r.enas

But for example from `pyhgnc.query().uniprot()` you can go back to hgnc

.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    uniprot = query.uniprot(uniprotid='Q9BTE6')[0]
    uniprot.hgncs
    # [AARSD1, PTGES3L-AARSD1]
    # following is crazy but possible, again go back to ec_number
    uniprot.hgncs[0].uniprots
    # [Q9BTE6]

7. HGNC identifier and symbol is available in all methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. hint::
    In all query functions (except `hgnc`) you have the parameters
    - hgnc_identifier
    - hgnc_symbol
    even it is not part of the model.

.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    query.alias_symbol(hgnc_identifier=620)
    # [AD1]
    query.alias_symbol(hgnc_symbol='APP')
    # [AD1]

hgnc
----
.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    query.hgnc(entrez=503538)

Check documentation of :func:`pyhgnc.manager.query.QueryManager.hgnc` for all available parameters.

orthology_prediction
--------------------
.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    query.orthology_prediction(ortholog_species=10090, hgnc_symbol='APP')
    # [10090: amyloid beta (A4) precursor protein: App]

Check documentation of :func:`pyhgnc.manager.query.QueryManager.orthology_prediction` for all available parameters.

alias_symbol
------------
.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    result = query.alias_symbol(alias_symbol='AD1')[0]
    result.hgnc
    # APP

Check documentation of :func:`pyhgnc.manager.query.QueryManager.alias_symbol` for all available parameters.

alias_name
----------
.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    result = query.alias_name(alias_name='peptidase nexin-II')[0]
    result.hgnc.name
    # 'amyloid beta precursor protein'

Check documentation of :func:`pyhgnc.manager.query.QueryManager.alias_name` for all available parameters.

gene_family
-----------
.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

        result = query.gene_family(family_name='Parkinson%')[0]
    result
    # 'Parkinson disease associated genes'
    result.hgncs
    # [ATP13A2, EIF4G1, FBXO7, HTRA2, LRRK2, PARK3, PARK7, PARK10, PARK11, PARK12, PARK16, PINK1,\
    # PLA2G6, PRKN, SNCA, UCHL1, VPS35]


Check documentation of :func:`pyhgnc.manager.query.QueryManager.gene_family` for
all available parameters.

ref_seq
-------
.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    query.ref_seq(hgnc_symbol='APP')
    # [NM_000484]

Check documentation of :func:`pyhgnc.manager.query.QueryManager.ref_seq` for all
available parameters.

rgd
---
.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    query.rgd(rgdid=2139)[0].hgncs
    # [APP]

Check documentation of :func:`pyhgnc.manager.query.QueryManager.rgd` for all available parameters.

omim
----
.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    query.omim(omimid=104760)[0].hgnc.name
    # 'amyloid beta precursor protein'

Check documentation of :func:`pyhgnc.manager.query.QueryManager.omim` for all available parameters.

mgd
---
.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    query.mgd(mgdid=88059)[0].hgncs
    # [APP]

Check documentation of :func:`pyhgnc.manager.query.QueryManager.mgd` for all available parameters.

uniprot
-------
.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    query.uniprot(uniprotid='P05067')[0].hgncs
    # [APP]

Check documentation of :func:`pyhgnc.manager.query.QueryManager.uniprot` for all available parameters.

ccds
----
.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    query.ccds(ccdsid='CCDS13576')[0].hgnc
    # APP

Check documentation of :func:`pyhgnc.manager.query.QueryManager.ccds` for all available parameters.

pubmed
------
.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    query.pubmed(hgnc_symbol='A1CF')
    # [11815617, 11072063]

Check documentation of :func:`pyhgnc.manager.query.QueryManager.pubmed` for all available parameters.

ena
---
.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    query.ena(hgnc_identifier=620)
    # [AD1]

Check documentation of :func:`pyhgnc.manager.query.QueryManager.ena` for all available parameters.

enzyme
------
.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    query.enzyme(hgnc_symbol='PRKCA')
    # [2.7.11.1]

Check documentation of :func:`pyhgnc.manager.query.QueryManager.enzyme` for all available parameters.

lsdb
----
.. code-block:: python

    import pyhgnc
    query = pyhgnc.query()

    query.lsdb(hgnc_symbol='APP')
    # [Alzheimer Disease & Frontotemporal Dementia Mutation Database]

Check documentation of :func:`pyhgnc.manager.query.QueryManager.lsdb` for all available parameters.