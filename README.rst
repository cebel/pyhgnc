|project_logo_large| |stable_build|
===================================

|stable_documentation| |pypi_license|

`PyHGNC <http://pyHGNC.readthedocs.io>`_ is a Python package
to access and query data provided by HGNC-approved gene nomenclature, gene families and associated resources 
including links to genomic, proteomic and phenotypic information.

Data are installed in a (local or remote) RDBMS enabling bioinformatic algorithms very fast response times
to sophisticated queries and high flexibility by using SOLAlchemy database layer.

PyHGNC is developed by the
`Department of Bioinformatics <https://www.scai.fraunhofer.de/en/business-research-areas/bioinformatics.html>`_
at the Fraunhofer Institute for Algorithms and Scientific Computing
`SCAI <https://www.scai.fraunhofer.de/en.html>`_
For more in for information about PyHGNC go to
`the documentation <http://pyhgnc.readthedocs.io/en/latest/index.html>`_.

|er_model|

This development is supported by following `IMI <https://www.imi.europa.eu/>`_ projects:

- `AETIONOMY <http://www.aetionomy.eu/>`_ and
- `PHAGO <http://www.phago.eu/>`_.

|imi_logo| |aetionomy_logo| |phago_logo| |scai_logo|

Supported databases
-------------------

`PyHGNC` uses `SQLAlchemy <http://sqlalchemy.readthedocs.io>`_ to cover a wide spectrum of RDMSs
(Relational database management system). For best performance MySQL or MariaDB is recommended. But if you have no
possibility to install software on your system SQLite - which needs no further
installation - also works. Following RDMSs are supported (by SQLAlchemy):

1. `Firebird <https://www.firebirdsql.org/en/start/>`_
2. `Microsoft SQL Server <https://www.microsoft.com/en-us/sql-server/>`_
3. `MySQL <https://www.mysql.com/>`_ / `MariaDB <https://mariadb.org/>`_
4. `Oracle <https://www.oracle.com/database/index.html>`_
5. `PostgreSQL <https://www.postgresql.org/>`_
6. `SQLite <https://www.sqlite.org/>`_
7. Sybase

Getting Started
---------------
This is a quick start tutorial for impatient.

Installation
~~~~~~~~~~~~
|pypi_version| |python_versions|

PyHGNC can be installed with `pip <https://pip.pypa.io/en/stable/>`_.

.. code-block:: bash

    pip install pyhgnc

If you fail because you have no rights to install use superuser (sudo on Linux before the commend) or ...

.. code-block:: bash

    pip install --user pyhgnc

If you want to make sure you are installing this under python3 use ...

.. code-block:: bash

    python3 -m pip install pyhgnc

SQLite
~~~~~~
.. note:: If you want to use SQLite as your database system, because you ...

    - have no possibility to use RDMSs like MySQL/MariaDB
    - just test PyHGNC, but don't want to spend time in setting up a database

    skip the next *MySQL/MariaDB setup* section. But in general we strongly recommend MySQL or MariaDB as your
    relational database management system.

If you don't know what all that means skip the section *MySQL/MariaDB setup*.

Don't worry! You can always later change the configuration. For more information about
changing database system later go to the subtitle *Changing database configuration*
`Changing database configuration <http://pyuniport.readthedocs.io/en/latest/installation.html>`_
in the documentation on readthedocs.

MySQL/MariaDB setup
~~~~~~~~~~~~~~~~~~~
Log in MySQL as root user and create a new database, create a user, assign the rights and flush privileges.

.. code-block:: mysql

    CREATE DATABASE pyhgnc CHARACTER SET utf8 COLLATE utf8_general_ci;
    GRANT ALL PRIVILEGES ON pyhgnc.* TO 'pyhgnc_user'@'%' IDENTIFIED BY 'pyhgnc_passwd';
    FLUSH PRIVILEGES;

There are two options to set the MySQL/MariaDB.

1. The simplest is to start the command line tool

.. code-block:: sh

    pyhgnc mysql

You will be guided with input prompts. Accept the default value in squared brackets with RETURN. You will see
something like this

.. code-block:: sh

    server name/ IP address database is hosted [localhost]:
    MySQL/MariaDB user [pyhgnc_user]:
    MySQL/MariaDB password [pyhgnc_passwd]:
    database name [pyhgnc]:
    character set [utf8]:

Connection will be tested and in case of success return `Connection was successful`.
Otherwise you will see following hint

.. code-block:: sh

    Test was NOT successful

    Please use one of the following connection schemas
    MySQL/MariaDB (strongly recommended):
            mysql+pymysql://user:passwd@localhost/database?charset=utf8

    PostgreSQL:
            postgresql://user:passwd@localhost/database

    MsSQL (pyodbc needed):
            mssql+pyodbc://user:passwd@database

    SQLite (always works):

    - Linux:
            sqlite:////absolute/path/to/database.db

    - Windows:
            sqlite:///C:\absolute\path\to\database.db

    Oracle:
            oracle://user:passwd@localhost:1521/database

2. The second option is to start a python shell and set the MySQL configuration.
If you have not changed anything in the SQL statements above ...

.. code-block:: python

    import pyhgnc
    pyhgnc.set_mysql_connection()

If you have used you own settings, please adapt the following command to you requirements.

.. code-block:: python

    import pyhgnc
    pyhgnc.set_mysql_connection(host='localhost', user='pyhgnc_user', passwd='pyhgnc_passwd', db='pyhgnc')

Updating
~~~~~~~~
The updating process will download the complete HGNC json file and the HCOP file.

.. code-block:: python

    import pyhgnc
    pyhgnc.manager.database.update()

This will use either the default connection settings of PyHGNC or the settings defined by the user.
It is also possible to run the update process from shell.

.. code-block:: sh

    pyhgnc update

Quick start with query functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Initialize the query object

.. code-block:: python

    query = pyhgnc.query()

Get all HGNC entries:

.. code-block:: python

    all_entries = query.hgnc()

.. hint::
    Check out the documentation: Query functions section for more examples and check out the Query section for
    all possible parameters for the different models.

More information
----------------
See the `installation documentation <http://pyhgnc.readthedocs.io/en/latest/installation.html>`_ for more advanced
instructions. Also, check the change log at :code:`CHANGELOG.rst`.

HGNC tools
----------
HGNC provides also `online tools <http://www.genenames.org/tools/all>`_ .

Links
-----
HUGO Gene Nomenclature Committee (HGNC)

- `HGNC website <http://www.genenames.org/>`_

PyHGNC

- Documented on `Read the Docs <http://pyhgnc.readthedocs.io/>`_
- Versioned on `GitHub <https://github.com/LeKono/pyhgnc>`_
- Tested on `Travis CI <https://travis-ci.org/LeKono/pyhgnc>`_
- Distributed by `PyPI <https://pypi.python.org/pypi/pyhgnc>`_
- Chat on `Gitter <https://gitter.im/pyhgnc/Lobby>`_

.. |stable_build| image:: https://travis-ci.org/LeKono/pyhgnc.svg?branch=master
    :target: https://travis-ci.org/LeKono/pyhgnc
    :alt: Stable Build Status

.. |stable_documentation| image:: https://readthedocs.org/projects/pyhgnc/badge/?version=latest
    :target: http://pyhgnc.readthedocs.io/en/latest/
    :alt: Development Documentation Status

.. |pypi_license| image:: https://img.shields.io/pypi/l/PyHGNC.svg
    :alt: Apache 2.0 License

.. |python_versions| image:: https://img.shields.io/pypi/pyversions/PyHGNC.svg
    :alt: Stable Supported Python Versions

.. |pypi_version| image:: https://img.shields.io/pypi/v/PyHGNC.svg
    :alt: Current version on PyPI

.. |phago_logo| image:: https://raw.githubusercontent.com/LeKono/pyhgnc/master/docs/source/_static/logos/phago_logo.png
    :target: https://www.imi.europa.eu/content/phago
    :alt: PHAGO project logo

.. |aetionomy_logo| image:: https://raw.githubusercontent.com/LeKono/pyhgnc/master/docs/source/_static/logos/aetionomy_logo.png
    :target: http://www.aetionomy.eu/en/vision.html
    :alt: AETIONOMY project logo

.. |imi_logo| image:: https://raw.githubusercontent.com/LeKono/pyhgnc/master/docs/source/_static/logos/imi_logo.png
    :target: https://www.imi.europa.eu/
    :alt: IMI project logo

.. |scai_logo| image:: https://raw.githubusercontent.com/LeKono/pyhgnc/master/docs/source/_static/logos/scai_logo.png
    :target: https://www.scai.fraunhofer.de/en/business-research-areas/bioinformatics.html
    :alt: SCAI project logo

.. |er_model| image:: https://raw.githubusercontent.com/LeKono/pyhgnc/master/docs/source/_static/models/all.png
    :target: http://pyhgnc.readthedocs.io/en/latest/
    :alt: Entity relationship model

.. |project_logo_large| image:: https://raw.githubusercontent.com/LeKono/pyhgnc/master/docs/source/_static/logos/project_logo_large.png
    :alt: Project logo