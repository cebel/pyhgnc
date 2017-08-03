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

from .manager.database import update

__all__ = ['update']

__version__ = '0.0.1'

__title__ = 'PyHGNC'
__description__ = 'Importing and querying HGNC data'
__url__ = '' # ToDo: Add URL!

__author__ = 'Andrej Konotopez'
__email__ = 'Andrej.Konotopez@scai.fraunhofer.de'

__license__ = 'Apache 2.0 License'
__copyright__ = 'Copyright (c) 2017 Andrej Konotopez, Fraunhofer Institute for Algorithms and Scientific Computing SCAI, Schloss Birlinghoven, 53754 Sankt Augustin, Germany'