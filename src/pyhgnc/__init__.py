"""

PyHGNC is tested (NOT YET) on both Python3

.. warning:: PyHGNC is not thoroughly tested on Windows.

Installation
------------

.. code-block:: sh

   $ git clone https://gitlab.scai.fraunhofer.de/andrej.konotopez/pyhgnc.git
   $ cd pyhgnc
   $ pip3 install -e .
"""

# ToDo: Make all the imports!
from .manager.query import QueryManager
from .manager.database import update

query = QueryManager

__all__ = ['update', 'query']

__version__ = '0.1.0-dev'

__title__ = 'PyHGNC'
__description__ = 'Importing and querying HGNC data'
__url__ = 'https://gitlab.scai.fraunhofer.de/andrej.konotopez/pyhgnc.git'

__author__ = 'Andrej Konotopez'
__email__ = 'Andrej.Konotopez@scai.fraunhofer.de'

__license__ = 'Apache 2.0 License'
__copyright__ = 'Copyright (c) 2017 Andrej Konotopez, Fraunhofer Institute for Algorithms and Scientific ' \
                'Computing SCAI, Schloss Birlinghoven, 53754 Sankt Augustin, Germany'