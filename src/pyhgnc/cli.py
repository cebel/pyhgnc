"""CLI for PyHGNC"""
# -*- coding: utf-8 -*-
import logging
import os
import sys
import time
import click
from . import constants

from .webserver.web import get_app
from .constants import PYHGNC_DIR
from .manager import database

from sqlalchemy import create_engine

"""
Module that contains the command line app

Why does this file exist, and why not put this in __main__?
You might be tempted to import things from __main__ later, but that will cause
problems--the code will get executed twice:
 - When you run `python -m pyhgnc` python will execute
   ``__main__.py`` as a script. That means there won't be any
   ``pyhgnc.__main__`` in ``sys.modules``.
 - When you import __main__ it will get executed again (as a module) because
   there's no ``pyhgnc.__main__`` in ``sys.modules``.
Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""


log = logging.getLogger('pyhgnc')

logging.basicConfig(format='%(name)s:%(levelname)s - %(message)s')

fh_path = os.path.join(PYHGNC_DIR, time.strftime('pyhgnc_%Y_%m_%d_%H_%M_%S.txt'))
fh = logging.FileHandler(fh_path)
fh.setLevel(logging.DEBUG)

log.addHandler(fh)

hint_connection_string = [
    "MySQL/MariaDB (strongly recommended):\n\tmysql+pymysql://user:passwd@localhost/database?charset=utf8",
    "PostgreSQL:\n\tpostgresql://user:passwd@localhost/database",
    "MsSQL (pyodbc needed):\n\tmssql+pyodbc://user:passwd@database",
    "SQLite (always works):",
    "- Linux:\n\tsqlite:////absolute/path/to/database.db",
    "- Windows:\n\tsqlite:///C:\\absolute\\path\\to\\database.db",
    "Oracle:\n\toracle://user:passwd@localhost:1521/database\n"
]


def test_connection(conn_str):
    try:
        conn = create_engine(conn_str)
        conn.connect()
        del conn
        click.secho('Connection test was successful', fg='green')
    except:
        click.secho('Connection test was NOT successful', fg='black', bg='red')
        click.echo("\n")
        click.secho('Please use one of the following connection schemas', fg='black', bg='green')
        click.secho('\n\n'.join(hint_connection_string))


@click.group(help="PyHGNC Command Line Utilities on {}".format(sys.executable))
@click.version_option()
def main():
    pass


@main.command()
@click.option('-c', '--connection', help='SQL Alchemy connection string')
@click.option('-s', '--silent', help="True if want no output (e.g. cron job)", is_flag=True)
@click.option('--hgnc_file_path', help="Load data from path HGNC")
@click.option('--hcop_file_path', help="Load data from path HCOP")
@click.option('-l', '--low_memory', help="set this if you have very low memory available", is_flag=True)
def update(connection, silent, hgnc_file_path, hcop_file_path, low_memory):
    """Update the database"""
    database.update(connection=connection,
                    silent=silent,
                    hgnc_file_path=hgnc_file_path,
                    hcop_file_path=hcop_file_path,
                    low_memory=low_memory)


@main.command(help="Set SQL Alchemy connection string, change default " +
                   "configuration. Without any option, sqlite will be set as default.")
@click.option('-c', '--connection',
              prompt="set connection",
              default="sqlite:///"+constants.DEFAULT_DB_LOCATION,
              help="path to location")
def setcon(connection):
    """Set the connection string"""
    database.set_connection(connection)
    test_connection(connection)


@main.command(help="Set MySQL Alchemy connection string, change default " +
                   "configuration.")
@click.option('-h', '--host', prompt="server name/ IP address database is hosted",
              default='localhost', help="host / servername")
@click.option('-u', '--user', prompt="MySQL/MariaDB user", default='pyhgnc_user', help="MySQL/MariaDB user")
@click.option('-p', '--passwd', prompt="MySQL/MariaDB password", hide_input=True, default='pyhgnc_passwd',
              help="MySQL/MariaDB password to access database")
@click.option('-d', '--db', prompt="database name", default='pyhgnc', help="database name")
@click.option('-c', '--charset', prompt="character set", default='utf8',
              help="character set for mysql connection")
def mysql(host, user, passwd, db, charset):
    """Set MySQL/MariaDB connection"""
    connection_string = database.set_mysql_connection(host=host, user=user, passwd=passwd, db=db, charset=charset)
    test_connection(connection_string)


@main.command()
@click.option('-h', '--host', default='0.0.0.0', help='Flask host. Defaults to localhost')
@click.option('-p', '--port', type=int, help='Flask port. Defaults to 5000')
def web(host, port):
    """Start web application"""
    click.echo("Trying to start server on {host}:{port}".format(host=host, port=port if port else 5000))
    get_app().run(host=host, port=port)


@main.command()
def getcon():
    """Get the connection string"""
    click.echo(database.BaseDbManager.get_connection_string())


@main.group(help="PyHGNC Data Manager Utilities")
def manage():
    pass


if __name__ == '__main__':
    main()
