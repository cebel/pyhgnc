Installation
============

System requirements
-------------------

After complete installation of HGNC (gene symbols and names) and HCOP (orthology) data by `PyHGNC`
~1,441,250 rows in 22 tables need only ~380 MB of disk storage (depending on the used RDMS).

Tests were performed on *Ubuntu 16.04, 4 x Intel Core i7-6560U CPU @ 2.20Ghz* with
*16 GiB of RAM*. In general PyHGNC should work also on other systems like Windows,
other Linux distributions or Mac OS. Installation were complete after ~4 min. For system
with lower memory we have added the option `--low_memory` in the update method.

.. _rdbms:

Supported databases
-------------------

`PyHGNC` uses `SQLAlchemy <http://sqlalchemy.readthedocs.io>`_ to cover a wide spectrum of RDMSs
(Relational database management system). For best performance MySQL or MariaDB is recommended. But if you have no
possibility to install software on your system, SQLite - which needs no further
installation - also works. Following RDMSs are supported (by SQLAlchemy):

1. Firebird
2. Microsoft SQL Server
3. MySQL / `MariaDB <https://mariadb.org/>`_
4. Oracle
5. PostgreSQL
6. SQLite
7. Sybase

Install software
----------------

The following instructions are written for Linux/MacOS. The way you install python software on Windows could be a
little bit different.

Often is make sense to avoid conflicts with other python installations by using different virtual environments. More
information about an easy way to manage different virtual environments you find
`here <http://virtualenvwrapper.readthedocs.io/en/latest/install.html>`_.

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

In general you don't have to setup any database, because by default `pyhgnc` uses file based SQLite. But we strongly
recommend to use MySQL/MariaDB.

Log in MySQL/MariaDB as root user and create a new database, create a user, assign the rights and flush privileges.

.. code-block:: mysql

    CREATE DATABASE pyhgnc CHARACTER SET utf8 COLLATE utf8_general_ci;
    GRANT ALL PRIVILEGES ON pyhgnc.* TO 'pyhgnc_user'@'%' IDENTIFIED BY 'pyhgnc_passwd';
    FLUSH PRIVILEGES;

The simplest way to set eth configurations for MySQL/MariaDB is use use the command ...

.. code-block:: sh

    pyhgnc mysql

... and except all default values.

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

Download files will take no space on your disk after the update process.

To update execute the following command in the shell

.. code-block:: sh

    pyhgnc update

More options are available with `pyhgnc update --help`

Second option in your Python shell is ...

.. code-block:: python

    import pyhgnc
    pyhgnc.update()

To make sure that the latest HGNC/HCOP version is used, use the parameter `force_download`

.. code-block:: python

    import pyhgnc
    pyhgnc.update(force_download=True)

Changing database configuration
-------------------------------

Following functions allow to change the connection to you RDBMS (relational database management system). Next
time you will use :code:`pyhgnc` by default this connection will be used.

To set a new MySQL/MariaDB connection use the interactive command line interface (bash, terminal, cmd) ...

.. code-block:: sh

    pyhgnc mysql

... or in Python shell ...

.. code-block:: python

    import pyhgnc
    pyhgnc.set_mysql_connection(host='localhost', user='pyhgnc_user', passwd='pyhgnc_passwd', db='pyhgnc')

To set connection to other database systems use the :func:`.database.set_connection` function.

For more information about connection strings go to
the `SQLAlchemy documentation <http://docs.sqlalchemy.org/en/latest/core/engines.html>`_.

Examples for valid connection strings are:

- mysql+pymysql://user:passwd@localhost/database?charset=utf8
- postgresql://scott:tiger@localhost/mydatabase
- mssql+pyodbc://user:passwd@database
- oracle://user:passwd@127.0.0.1:1521/database
- Linux: sqlite:////absolute/path/to/database.db
- Windows: sqlite:///C:\\path\\to\\database.db

.. code-block:: python

    import pyhgnc
    pyhgnc.set_connection('oracle://user:passwd@127.0.0.1:1521/database')
