Benchmarks
==========

All benchmarks created on a standard notebook:

- OS: Linux Ubuntu 16.04.2 LTS (xenial)
- Python: 3.5.2
- Hardware: x86_64, Intel(R) Core(TM) i7-6560U CPU @ 2.20GHz, 4 CPUs, Mem 16Gb
- MariaDB: Server version: 10.0.29-MariaDB-0ubuntu0.16.04.1 Ubuntu 16.04

MySQL/MariaDB
-------------

Database created with following command in MySQL/MariaDB as root:

.. code:: sql

    CREATE DATABASE pyhgnc CHARACTER SET utf8 COLLATE utf8_general_ci;

User created with following command in MySQL/MariaDB:

.. code:: sql

    GRANT ALL PRIVILEGES ON pyhgnc.* TO 'pyhgnc_user'@'%' IDENTIFIED BY 'pyhgnc_passwd';
    FLUSH PRIVILEGES;

Update
------

To import HGNC data executed following commands in python console:

.. code:: python

    import pyhgnc
    pyhgnc.set_mysql_connection()
    pyhgnc.update()

The other possibility is to use the command line interface

.. code:: sh

    pyhgnc mysql # accept all default values
    pyhgnc update
    
- CPU times:
    - real 3m52.311s
    - user 3m4.964s
    - sys 0m6.340s

Low memory option
-----------------

If you have low memory available please use the --low_memory option in command line

.. code:: sh

    pyhgnc mysql # accept all default values
    pyhgnc update --low_memory
    # or short
    pyhgnc update -l

- CPU times:
    - real 6m40.913s
    - user 5m22.724s
    - sys 0m9.016s


