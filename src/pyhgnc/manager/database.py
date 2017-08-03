# -*- coding: utf-8 -*-
"""PyHGNC loads HGNC contant into a relational database and provides a RESTFull API."""

import os
import time
import logging
import zipfile
import json

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session

from urllib import request

from configparser import RawConfigParser, ConfigParser

from . import models
from . import defaults
from ..constants import PYHGNC_DATA_DIR, PYHGNC_DIR, PYHGNC_LOG_DIR, HGNC_JSON, bcolors


log = logging.getLogger('pyhgnc')

fh_path = os.path.join(PYHGNC_LOG_DIR, time.strftime('pyhgnc_database_%Y_%m_%d_%H_%M_%S.txt'))
fh = logging.FileHandler(fh_path)
fh.setLevel(logging.DEBUG)
log.addHandler(fh)


class BaseDbManager(object):
    """Creates a connection to database and a persistient session using SQLAlchemy"""

    def __init__(self, connection=None, echo=False):
        """
        :param str connection: SQLAlchemy
        :param bool echo: True or False for SQL output of SQLAlchemy engine
        """
        try:
            self.connection = self.get_connection_string(connection)
            self.engine = create_engine(self.connection, echo=echo)
            self.sessionmaker = sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)
            self.session = scoped_session(self.sessionmaker)
        except:
            self.set_connection_string_by_user_input()
            self.__init__()

    def set_connection_string_by_user_input(self):
        """Asks the user to setup a valid SQLAlchemy connection string if the first connection
        attempt did not work."""
        # ToDo: Should this maybe happen in cli?

        user_connection = input(
            bcolors.WARNING + "\nFor any reason connection to " + bcolors.ENDC +
            bcolors.FAIL + "{}".format(self.connection) + bcolors.ENDC +
            bcolors.WARNING + " is not possible.\n\n" + bcolors.ENDC +
            "For more information about SQLAlchemy connection strings go to:\n" +
            "http://docs.sqlalchemy.org/en/latest/core/engines.html\n\n"
            "Please insert a valid connection string:\n" +
            bcolors.UNDERLINE + "Examples:\n\n" + bcolors.ENDC +
            "MySQL (recommended):\n" +
            bcolors.OKGREEN + "\tmysql+pymysql://user:passwd@localhost/database?charset=utf8\n" + bcolors.ENDC +
            "PostgreSQL:\n" +
            bcolors.OKGREEN + "\tpostgresql://scott:tiger@localhost/mydatabase\n" + bcolors.ENDC +
            "MsSQL (pyodbc have to be installed):\n" +
            bcolors.OKGREEN + "\tmssql+pyodbc://user:passwd@database\n" + bcolors.ENDC +
            "SQLite (always works):\n" +
            " - Linux:\n" +
            bcolors.OKGREEN + "\tsqlite:////absolute/path/to/database.db\n" + bcolors.ENDC +
            " - Windows:\n" +
            bcolors.OKGREEN + "\tsqlite:///C:\\path\\to\\database.db\n" + bcolors.ENDC +
            "Oracle:\n" +
            bcolors.OKGREEN + "\toracle://user:passwd@127.0.0.1:1521/database\n\n" + bcolors.ENDC +
            "[RETURN] for standard connection {}:\n".format(defaults.sqlalchemy_connection_string_default)
        )
        if not (user_connection or user_connection.strip()):
            user_connection = defaults.sqlalchemy_connection_string_default
        set_connection(user_connection.strip())

    def _create_tables(self, checkfirst=True):
        """creates all tables from models in your database

        :param checkfirst: True or False check if tables already exists
        :type checkfirst: bool
        :return:
        """
        log.info('create tables in {}'.format(self.engine.url))
        models.Base.metadata.create_all(self.engine, checkfirst=checkfirst)

    def _drop_tables(self):
        """drops all tables in the database

        :return:
        """
        log.info('drop tables in {}'.format(self.engine.url))
        models.Base.metadata.drop_all(self.engine)

    @staticmethod
    def get_connection_string(connection=None):
        """return sqlalchemy connection string if it is set

        :param connection: get the SQLAlchemy connection string #TODO
        :return:
        """
        if not connection:
            config = ConfigParser()
            cfp = defaults.config_file_path
            if os.path.exists(cfp):
                log.info('fetch database configuration from {}'.format(cfp))
                config.read(cfp)
                connection = config['database']['sqlalchemy_connection_string']
                log.info('load connection string from {}: {}'.format(cfp, connection))
            else:
                with open(cfp, 'w') as config_file:
                    connection = defaults.sqlalchemy_connection_string_default
                    config['database'] = {'sqlalchemy_connection_string': connection}
                    config.write(config_file)
                    log.info('create configuration file {}'.format(cfp))
        return connection


class DbManager(BaseDbManager):

    def __init__(self, connection=None):
        """The DbManager implements all function to upload HGNC data into the database. Prefered SQL Alchemy
        database is MySQL with pymysql.

        :param connection: custom database connection SQL Alchemy string
        :type connection: str
        """

        super(DbManager, self).__init__(connection=connection)

    def db_import(self):
        self._create_tables()
        self.insert_data(hgnc_dict=DbManager.download_hgnc_json())

    def insert_data(self, hgnc_dict):

        for hgnc_data in hgnc_dict['docs']:
            hgnc_table = {
                'symbol': hgnc_data['symbol'],
                'hgncID': hgnc_data['hgnc_id'],
                'status': hgnc_data['status'],
                'uuid': hgnc_data['uuid'],
                'locusGroup': hgnc_data['locus_group'],
                'locusType': hgnc_data['locus_type'],
                'ensemblgene_id': hgnc_data['ensembl_gene_id'] if 'ensembl_gene_id' in hgnc_data else None,
                'horde_id': hgnc_data['horde_id'] if 'horde_id' in hgnc_data else None,
                'vega_id': hgnc_data['vega_id'] if 'vega_id' in hgnc_data else None,
                'lncrnadb_id': hgnc_data['lncrnadb'] if 'lncrnadb' in hgnc_data else None,
                'entrez_id': hgnc_data['entrez_id'] if 'entrez_id' in hgnc_data else None,
                'mirbase_id': hgnc_data['mirbase'] if 'mirbare' in hgnc_data else None,
                'iuphar_id': hgnc_data['iuphar'] if 'uiphar' in hgnc_data else None,
                'ucsc_id': hgnc_data['ucsc_id'] if 'ucsc_id' in hgnc_data else None,
                'snornabase_id': hgnc_data['snornabase'] if 'snornabase' in hgnc_data else None,
                'intermediatefilamentdb_id': hgnc_data['intermediate_filament_db'] if 'intermediate_filament_db' in hgnc_data else None,
                'pseudogeneorg': hgnc_data['pseudogene.org'] if 'pseudogene.org' in hgnc_data else None,
                'bioparadigmsslc': hgnc_data['bioparadigms_slc'] if 'bioparadigms_slc' in hgnc_data else None,
                'locationsortable': hgnc_data['location_sortable'] if 'location_sortable' in hgnc_data else None,
                'merop': hgnc_data['merops'] if 'merops' in hgnc_data else None,
                'location': hgnc_data['location'] if 'location' in hgnc_data else None,
                'cosmic': hgnc_data['cosmic'] if 'cosmic' in hgnc_data else None,
                'imgt': hgnc_data['imgt'] if 'imgt' in hgnc_data else None
            }

            # 'datenamechanged': hgnc_data['date_name_changed'] if 'date_name_changed' in hgnc_data else None,
            # 'datemodified': hgnc_data['date_modified'] if 'date_modified' in hgnc_data else None,
            # 'datesymbolchanged': hgnc_data['date_symbol_changed'] if 'date_symbol_changed' in hgnc_data else None,
            # 'dateapprovedreserved': hgnc_data[
            # 'date_approved_reserved'] if 'date_approved_reserved' in hgnc_data else None,

            hgnc = models.HGNC(**hgnc_table)
            self.session.add(hgnc)

            if 'alias_symbol' in hgnc_data or 'prev_symbol' in hgnc_data:
                if 'alias_symbol' in hgnc_data:
                    for alias in hgnc_data['alias_symbol']:
                        self.session.add(models.AliasSymbol(symbol=alias,
                                                            hgnc=hgnc))
                else:
                    for prev in hgnc_data['prev_symbol']:
                        self.session.add(models.AliasSymbol(symbol=prev,
                                                            hgnc=hgnc,
                                                            isprev=True))

            if 'alias_name' in hgnc_data or 'prev_name' in hgnc_data:
                if 'alias_name' in hgnc_data:
                    for alias in hgnc_data['alias_name']:
                        self.session.add(models.AliasName(name=alias,
                                                          hgnc=hgnc))
                else:
                    for prev in hgnc_data['prev_name']:
                        self.session.add(models.AliasName(name=prev,
                                                          hgnc=hgnc,
                                                          isprev=True))

            if 'gene_family' in hgnc_data:
                for i, family in enumerate(hgnc_data['gene_family']):
                    self.session.add(models.GeneFamily(familyid=hgnc_data['gene_family_id'][i],
                                                       familyname=family,
                                                       hgnc=hgnc))

            if 'refseq_accession' in hgnc_data:
                for accession in hgnc_data['refseq_accession']:
                    self.session.add(models.RefSeq(accession=accession,
                                                       hgnc=hgnc))

            if 'rgd_id' in hgnc_data:
                for rgd in hgnc_data['rgd_id']:
                    self.session.add(models.RGD(rgdid=rgd,
                                                hgnc=hgnc))

            if 'mgd_id' in hgnc_data:
                for mgd in hgnc_data['mgd_id']:
                    self.session.add(models.MGD(mgdid=mgd,
                                                hgnc=hgnc))

            if 'omim_id' in hgnc_data:
                for omim in hgnc_data['omim_id']:
                    self.session.add(models.OMIM(omimid=omim,
                                                 hgnc=hgnc))

            if 'uniprot_ids' in hgnc_data:
                for uniprot in hgnc_data['uniprot_ids']:
                    self.session.add(models.Uniprot(uniprotid=uniprot,
                                                    hgnc=hgnc))

            if 'ccds_id' in hgnc_data:
                for ccds in hgnc_data['ccds_id']:
                    self.session.add(models.CCDS(ccdsid=ccds,
                                                 hgnc=hgnc))

            if 'pubmed_id' in hgnc_data:
                for pubmed in hgnc_data['pubmed_id']:
                    self.session.add(models.PubMed(pubmedid=pubmed,
                                                   hgnc=hgnc))

            if 'enzyme_id' in hgnc_data:
                for enzyme in hgnc_data['enzyme_id']:
                    self.session.add(models.Enzyme(enzymeid=enzyme,
                                                   hgnc=hgnc))

            if 'ena' in hgnc_data:
                for ena in hgnc_data['ena']:
                    self.session.add(models.ENA(enaid=ena,
                                                hgnc=hgnc))

            if 'lsdb' in hgnc_data:
                for lsdb in hgnc_data['lsdb']:
                    self.session.add(models.LSDB(lsdb=lsdb,
                                                 hgnc=hgnc))

        self.session.commit()

    @staticmethod
    def download_hgnc_json():

        response = request.urlopen(HGNC_JSON)
        hgnc_dict = json.loads(response.read().decode())

        return hgnc_dict['response']


def update(connection=None, urls=None, force_download=None):
    database = DbManager(connection)
    database.db_import()
    database.session.close()


def set_connection(connection=defaults.sqlalchemy_connection_string_default):
    """
    Set the connection string for sqlalchemy and write it to the config file.
    :param str connection: sqlalchemy connection string
    """
    config_path = defaults.config_file_path
    config = RawConfigParser()

    if not os.path.exists(config_path):
        with open(config_path, 'w') as config_file:
            config['database'] = {'sqlalchemy_connection_string': connection}
            config.write(config_file)
            log.info('create configuration file {}'.format(config_path))
    else:
        config.read(config_path)
        config.set('database', 'sqlalchemy_connection_string', connection)
        with open(config_path, 'w') as configfile:
            config.write(configfile)
