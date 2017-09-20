Installation
============

System requirements
-------------------

After complete installation of HGNC (gene symbols and names) and HCOP (orthology) data by `PyHGNC`
~1,441,250 rows in 22 tables need only ~380 MB of disk storage (depending on the used RDMS).

Tests were performed on *Ubuntu 16.04, 4 x Intel Core i7-6560U CPU @ 2.20Ghz* with
*16 GiB of RAM*. In general PyHGNC should work also on other systems like Windows,
other Linux distributions or Mac OS. Installation were complete after ~4 min. For systems
with low memory the option `--low_memory` was added in the update method.

.. _rdbms:

Supported databases
-------------------

`PyHGNC` uses `SQLAlchemy <http://sqlalchemy.readthedocs.io>`_ to cover a wide spectrum of RDMSs
(Relational database management systems). For best performance MySQL or MariaDB is recommended. But if you have no
possibility to install software on your system, SQLite - which needs no further
installation - also works. The following RDMSs are supported (by SQLAlchemy):

1. `Firebird <https://www.firebirdsql.org/en/start/>`_
2. `Microsoft SQL Server <https://www.microsoft.com/en-us/sql-server/>`_
3. `MySQL <https://www.mysql.com/>`_ / `MariaDB <https://mariadb.org/>`_
4. `Oracle <https://www.oracle.com/database/index.html>`_
5. `PostgreSQL <https://www.postgresql.org/>`_
6. `SQLite <https://www.sqlite.org/>`_
7. Sybase

Install software
----------------

The following instructions are written for Linux/MacOS. The way you install python software on Windows could be different.

Often it makes sense to avoid conflicts with other python installations by using different virtual environments.
Read `here <http://virtualenvwrapper.readthedocs.io/en/latest/install.html>`_ about easy setup and management of
different virtual environments.

* If you want to install `pyhgnc` system wide use superuser (sudo for Ubuntu):

.. code-block:: bash

    sudo pip install pyhgnc

* If you have no sudo rights install as user

.. code-block:: bash

    pip install --user pyhgnc

* If you want to make sure you install `pyhgnc` in python3 environment:

.. code-block:: bash

    sudo python3 -m pip install pyhgnc


MySQL/MariaDB setup
~~~~~~~~~~~~~~~~~~~

In general you don't have to setup any database, because `pyhgnc` uses file based SQLite by default. But we strongly
recommend to use MySQL/MariaDB.

Log in MySQL/MariaDB as root user and create a new database, create a user, assign the rights and flush privileges.

.. code-block:: mysql

    CREATE DATABASE pyhgnc CHARACTER SET utf8 COLLATE utf8_general_ci;
    GRANT ALL PRIVILEGES ON pyhgnc.* TO 'pyhgnc_user'@'%' IDENTIFIED BY 'pyhgnc_passwd';
    FLUSH PRIVILEGES;

The simplest way to set the configurations of `pyhgnc` for MySQL/MariaDB is to use the command ...

.. code-block:: sh

    pyhgnc mysql

... and accept all default values.

Another way is to open a python shell and set the MySQL configuration. If you have not changed
anything in the SQL statements ...

.. code-block:: python

    import pyhgnc
    pyhgnc.set_mysql_connection()

If you have used you own settings, please adapt the following command to you requirements.

.. code-block:: python

    import pyhgnc
    pyhgnc.set_mysql_connection(host='localhost', user='pyhgnc_user', passwd='pyhgnc_passwd', db='pyhgnc')

Updating
~~~~~~~~

During the updating process PyHGNC will download HGNC and HCOP files from the
`EBI ftp server <ftp://ftp.ebi.ac.uk/pub/databases/genenames>`_.

Downloaded files will take no space on your disk after the update process.

To update from command line or terminal:

.. code-block:: sh

    pyhgnc update

Update options are available aswell, type `pyhgnc update --help` to get a full list with descriptions.

To update from Python shell:

.. code-block:: python

    import pyhgnc
    pyhgnc.update()

Changing database configuration
-------------------------------

Following functions allow to change the connection to your RDBMS (relational database management system). The connection
settings will be used by default on the next time :code:`pyhgnc` is executed.

To set a new MySQL/MariaDB connection use the interactive command line interface (bash, terminal, cmd) ...

.. code-block:: sh

    pyhgnc mysql

... or in Python shell ...

.. code-block:: python

    import pyhgnc
    pyhgnc.set_mysql_connection(host='localhost', user='pyhgnc_user', passwd='pyhgnc_passwd', db='pyhgnc')

To set connection to other database systems use the :func:`.database.set_connection`.

For more information about connection strings go to
the `SQLAlchemy documentation <http://docs.sqlalchemy.org/en/latest/core/engines.html>`_.

Examples for valid connection strings are:

- mysql+pymysql://user:passwd@localhost/database?charset=utf8
- postgresql://scott:tiger@localhost/mydatabase
- mssql+pyodbc://user:passwd@database
- oracle://user:passwd@127.0.0.1:1521/database
- Linux: sqlite:////absolute/path/to/database.db
- Windows: sqlite:///C:\\path\\to\\database.db

You could use the following code to connect `pyhgnc` to an oracle database:

.. code-block:: python

    import pyhgnc
    pyhgnc.set_connection('oracle://user:passwd@127.0.0.1:1521/database')
