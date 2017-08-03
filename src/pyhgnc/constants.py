# -*- coding: utf-8 -*-

import os

# Path to PyWikiPathways folder
PYHGNC_DIR = os.path.expanduser('~/.pyhgnc')
if not os.path.exists(PYHGNC_DIR):
    os.mkdir(PYHGNC_DIR)

# Path to PyWikiPathways data folder
PYHGNC_DATA_DIR = os.path.join(PYHGNC_DIR, 'data')
if not os.path.exists(PYHGNC_DATA_DIR):
    os.mkdir(PYHGNC_DATA_DIR)

# Path to PyWikiPathways logs folder
PYHGNC_LOG_DIR = os.path.join(PYHGNC_DIR, 'logs')
if not os.path.exists(PYHGNC_LOG_DIR):
    os.mkdir(PYHGNC_LOG_DIR)

# Default database name and location
DEFAULT_DB_NAME = 'pyhgnc.db'
DEFAULT_DB_LOCATION = os.path.join(PYHGNC_DATA_DIR, DEFAULT_DB_NAME)

HGNC_JSON = "ftp://ftp.ebi.ac.uk/pub/databases/genenames/new/json/hgnc_complete_set.json"

# Colorcodes for terminal interaction
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
