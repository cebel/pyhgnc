# -*- coding: utf-8 -*-
"""This file contains default URL settings for PyWikiPathways."""

import os
from ..constants import PYWPW_DIR, PYWPW_DATA_DIR


DEFAULT_SQLITE_DATABASE_NAME = 'pywpw.db'
DEFAULT_SQLITE_TEST_DATABASE_NAME = 'pywpw_test.db'
DEFAULT_DATABASE_LOCATION = os.path.join(PYWPW_DATA_DIR, DEFAULT_SQLITE_DATABASE_NAME)
DEFAULT_TEST_DATABASE_LOCATION = os.path.join(PYWPW_DATA_DIR, DEFAULT_SQLITE_TEST_DATABASE_NAME)

sqlalchemy_connection_string_default = 'sqlite:///' + DEFAULT_DATABASE_LOCATION
sqlalchemy_connection_string_4_tests = 'sqlite:///' + DEFAULT_SQLITE_TEST_DATABASE_NAME

sqlalchemy_connection_string_4_mysql = 'mysql+pymysql://pywpw:pywpw@localhost/pywpw?charset=utf8'
sqlalchemy_connection_string_4_mysql_tests = 'mysql+pymysql://pywpw:pywpw@localhost/pywpw_test?charset=utf8'

config_file_path = os.path.join(PYWPW_DIR, 'config.ini')
