# -*- coding: utf-8 -*-
"""This file contains default URL settings for PyHGNC."""

import os
from ..constants import PYHGNC_DIR, PYHGNC_DATA_DIR

DEFAULT_SQLITE_DATABASE_NAME = 'pyhgnc.db'
DEFAULT_SQLITE_TEST_DATABASE_NAME = 'pyhgnc_test.db'
DEFAULT_DATABASE_LOCATION = os.path.join(PYHGNC_DATA_DIR, DEFAULT_SQLITE_DATABASE_NAME)
DEFAULT_TEST_DATABASE_LOCATION = os.path.join(PYHGNC_DATA_DIR, DEFAULT_SQLITE_TEST_DATABASE_NAME)

sqlalchemy_connection_string_default = 'sqlite:///' + DEFAULT_DATABASE_LOCATION
sqlalchemy_connection_string_4_tests = 'sqlite:///' + DEFAULT_TEST_DATABASE_LOCATION

sqlalchemy_connection_string_4_mysql = 'mysql+pymysql://pyhgnc:pyhgnc@localhost/pyhgnc?charset=utf8'
sqlalchemy_connection_string_4_mysql_tests = 'mysql+pymysql://pyhgnc:pyhgnc@localhost/pyhgnc_test?charset=utf8'

TABLE_PREFIX = 'pyhgnc_'

config_file_path = os.path.join(PYHGNC_DIR, 'config.ini')
