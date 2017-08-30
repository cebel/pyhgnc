# -*- coding: utf-8 -*-
"""PyHGNC loads HGNC contant into a relational database and provides a RESTFull API."""

import os
import time
import logging
import json
import pandas
import numpy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, load_only

from tqdm import tqdm
from urllib import request
from datetime import datetime

from configparser import RawConfigParser, ConfigParser

from pyhgnc import constants
from . import models
from . import defaults
from ..constants import PYHGNC_LOG_DIR, HGNC_JSON


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
            log.warning('No valid database connection. Execute `pyhgnc connection` on command line')

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
    enzymes = {}
    gene_families = {}
    refseqs = {}
    mgds = {}
    uniprots = {}
    pubmeds = {}
    enas = {}
    rgds = {}

    def __init__(self, connection=None):
        """The DbManager implements all function to upload HGNC data into the database. Prefered SQL Alchemy
        database is MySQL with pymysql.

        :param connection: custom database connection SQL Alchemy string
        :type connection: str
        """

        super(DbManager, self).__init__(connection=connection)

    def db_import(self, silent=False, from_path=None, low_memory=False):
        self._drop_tables()
        self._create_tables()
        json_data = DbManager.load_hgnc_json(from_path)
        self.insert_hgnc(hgnc_dict=json_data, silent=silent, low_memory=low_memory)
        self.insert_hcop(silent=silent)

    @classmethod
    def get_date(cls, hgnc, key):
        date_value = hgnc.get(key)
        if date_value:
            return datetime.strptime(date_value, "%Y-%m-%d",).date()

    @classmethod
    def get_alias_symbols(cls, hgnc):
        alias_symbols = []

        if 'alias_symbol' in hgnc:
            for alias in hgnc['alias_symbol']:
                alias_symbols.append(models.AliasSymbol(alias_symbol=alias))
        if 'prev_symbol' in hgnc:
            for prev in hgnc['prev_symbol']:
                alias_symbols.append(models.AliasSymbol(alias_symbol=prev, is_previous_symbol=True))
        return alias_symbols

    @classmethod
    def get_alias_names(cls, hgnc):
        alias_names = []

        if 'alias_name' in hgnc:
            for alias in hgnc['alias_name']:
                alias_names.append(models.AliasName(alias_name=alias))

        if 'prev_name' in hgnc:
            for prev in hgnc['prev_name']:
                alias_names.append(models.AliasName(alias_name=prev, is_previous_name=True))

        return alias_names

    def get_gene_families(self, hgnc):
        gene_families = []

        if 'gene_family' in hgnc:

            for i, family in enumerate(hgnc['gene_family']):

                family_identifier = hgnc['gene_family_id'][i]

                if family_identifier not in self.gene_families:

                    gene_family = models.GeneFamily(family_identifier=family_identifier, family_name=family)
                    self.gene_families[family_identifier] = gene_family

                gene_families.append(self.gene_families[family_identifier])

        return gene_families

    def get_refseq(self, hgnc):
        refseqs = []

        if 'refseq_accession' in hgnc:
            for accession in hgnc['refseq_accession']:

                if accession not in self.refseqs:
                    self.refseqs[accession] = models.RefSeq(accession=accession)

                refseqs.append(self.refseqs[accession])

        return refseqs

    def get_mgds(self, hgnc):
        mgds = []

        if 'mgd_id' in hgnc:

            for mgd in hgnc['mgd_id']:

                if mgd not in self.mgds:
                    mgdid = int(mgd.split(':')[-1])
                    self.mgds[mgd] = models.MGD(mgdid=mgdid)

                mgds.append(self.mgds[mgd])

        return mgds

    def get_rgds(self, hgnc):
        rgds = []

        if 'rgd_id' in hgnc:

            for rgd in hgnc['rgd_id']:

                if rgd not in self.rgds:
                    rgdid = int(rgd.split(':')[-1])
                    self.rgds[rgd] = models.RGD(rgdid=rgdid)

                rgds.append(self.rgds[rgd])

        return rgds

    def get_omims(self, hgnc):
        omims = []

        if 'omim_id' in hgnc:

            for omim in hgnc['omim_id']:
                omims.append(models.OMIM(omimid=omim))

        return omims

    def get_uniprots(self, hgnc):
        uniprots = []

        if 'uniprot_ids' in hgnc:
            for uniprot in hgnc['uniprot_ids']:

                if uniprot not in self.uniprots:
                    self.uniprots[uniprot] = models.UniProt(uniprotid=uniprot)

                uniprots.append(self.uniprots[uniprot])

        return uniprots

    def get_ccds(self, hgnc):
        ccds = []

        if 'ccds_id' in hgnc:
            for ccdsid in hgnc['ccds_id']:
                ccds.append(models.CCDS(ccdsid=ccdsid))

        return ccds

    def get_pubmeds(self, hgnc):
        pubmeds = []

        if 'pubmed_id' in hgnc:
            for pubmed in hgnc['pubmed_id']:

                if pubmed not in self.pubmeds:
                    self.pubmeds[pubmed] = models.PubMed(pubmedid=int(pubmed))

                pubmeds.append(self.pubmeds[pubmed])

        return pubmeds

    def get_enas(self, hgnc):
        enas = []

        if 'ena' in hgnc:
            for ena in hgnc['ena']:
                if ena not in self.enas:
                    self.enas[ena] = models.ENA(enaid=ena)

                enas.append(self.enas[ena])

        return enas

    def get_lsdbs(self, hgnc):
        lsdbs = []

        if 'lsdb' in hgnc:

            for lsdb_url in hgnc['lsdb']:
                lsdb, url = lsdb_url.split('|')
                lsdbs.append(models.LSDB(lsdb=lsdb, url=url))

        return lsdbs

    def get_enzymes(self, hgnc):
        enzymes = []

        if 'enzyme_id' in hgnc:

            for ec_number in hgnc['enzyme_id']:

                if ec_number not in self.enzymes:
                    self.enzymes[ec_number] = models.Enzyme(ec_number=ec_number)

                enzymes.append(self.enzymes[ec_number])

        return enzymes

    def insert_hgnc(self, hgnc_dict, silent=False, low_memory=False):

        log.info('low_memory set to {}'.format(low_memory))

        for hgnc_data in tqdm(hgnc_dict['docs'], disable=silent):
            hgnc_table = {
                'symbol': hgnc_data['symbol'],
                'identifier': int(hgnc_data['hgnc_id'].split(':')[-1]),
                'name': hgnc_data['name'],
                'status': hgnc_data['status'],
                'orphanet': hgnc_data.get('orphanet'),
                'uuid': hgnc_data['uuid'],
                'locus_group': hgnc_data['locus_group'],
                'locus_type': hgnc_data['locus_type'],
                'ensembl_gene': hgnc_data.get('ensembl_gene_id'),
                'horde': hgnc_data.get('horde_id'),
                'vega': hgnc_data.get('vega_id'),
                'lncrnadb': hgnc_data.get('lncrnadb'),
                'entrez': hgnc_data.get('entrez_id'),
                'mirbase': hgnc_data.get('mirbase'),
                'iuphar': hgnc_data.get('iuphar'),
                'ucsc': hgnc_data.get('ucsc_id'),
                'snornabase': hgnc_data.get('snornabase'),
                'pseudogeneorg': hgnc_data.get('pseudogene.org'),
                'bioparadigmsslc': hgnc_data.get('bioparadigms_slc'),
                'locationsortable': hgnc_data.get('location_sortable'),
                'merops': hgnc_data.get('merops'),
                'location': hgnc_data.get('location'),
                'cosmic': hgnc_data.get('cosmic'),
                'imgt': hgnc_data.get('imgt'),
                'date_name_changed': self.get_date(hgnc_data, 'date_name_changed'),
                'date_modified': self.get_date(hgnc_data, 'date_modified'),
                'date_symbol_changed': self.get_date(hgnc_data, 'date_symbol_changed'),
                'date_approved_reserved': self.get_date(hgnc_data, 'date_approved_reserved'),
                'alias_symbols': self.get_alias_symbols(hgnc_data),
                'alias_names': self.get_alias_names(hgnc_data),
                'gene_families': self.get_gene_families(hgnc_data),
                'refseqs': self.get_refseq(hgnc_data),
                'mgds': self.get_mgds(hgnc_data),
                'rgds': self.get_rgds(hgnc_data),
                'omims': self.get_omims(hgnc_data),
                'uniprots': self.get_uniprots(hgnc_data),
                'ccdss': self.get_ccds(hgnc_data),
                'pubmeds': self.get_pubmeds(hgnc_data),
                'enas': self.get_enas(hgnc_data),
                'lsdbs': self.get_lsdbs(hgnc_data),
                'enzymes': self.get_enzymes(hgnc_data)
            }

            self.session.add(models.HGNC(**hgnc_table))
            if low_memory:
                self.session.flush()

        if not silent:
            print('Insert HGNC data into database')

        self.session.commit()

    def insert_hcop(self, silent=False):

        log_text = 'Load OrthologyPrediction data from {}'.format(constants.HCOP_GZIP)
        log.info(log_text)
        if not silent:
            print(log_text)

        df_hcop = pandas.read_table(constants.HCOP_GZIP, low_memory=False)
        df_hcop.replace('-', numpy.NaN, inplace=True)
        df_hcop.replace(to_replace={'hgnc_id': 'HGNC:'}, value='', regex=True, inplace=True)
        df_hcop.hgnc_id = df_hcop.hgnc_id.fillna(-1).astype(int)
        df_hcop.rename(columns={'hgnc_id': 'identifier'}, inplace=True)
        df_hcop.set_index('identifier', inplace=True)

        log_text = 'Join HGNC with HGNC'
        log.info(log_text)
        if not silent:
            print(log_text)

        data = self.session.query(models.HGNC).options(load_only(models.HGNC.id, models.HGNC.identifier))
        data = [{'hgnc_id': x.id, 'identifier': x.identifier} for x in data]
        df_hgnc = pandas.DataFrame(data)
        df_hgnc.set_index('identifier', inplace=True)

        df_hcnp4db = df_hcop.join(df_hgnc)
        df_hcnp4db.reset_index(inplace=True)
        df_hcnp4db.index += 1
        df_hcnp4db.drop('identifier', axis=1, inplace=True)
        df_hcnp4db.index.rename('id', inplace=True)

        log_text = 'Load OrthologyPrediction data in database'
        log.info(log_text)
        if not silent:
            print(log_text)

        df_hcnp4db.to_sql(name=models.OrthologyPrediction.__tablename__, con=self.connection, if_exists='append')

    @staticmethod
    def load_hgnc_json(from_path=None):

        if from_path:
            with open(from_path) as response:
                log.info('loading json data from {}'.format(from_path))
                hgnc_dict = json.loads(response.read())
        else:
            response = request.urlopen(HGNC_JSON)
            hgnc_dict = json.loads(response.read().decode())

        return hgnc_dict['response']


def update(connection=None, silent=False, from_path=None, low_memory=False):
    """Update the database with current version of HGNC

    :param str connection: conncetion string
    :param bool silent: silent while import
    :param str from_path: import from path
    :param bool low_memory: set to `True` if you have low memory
    :return:
    """
    database = DbManager(connection)
    database.db_import(silent=silent, from_path=from_path, low_memory=low_memory)
    database.session.close()


def set_connection(connection=defaults.sqlalchemy_connection_string_default):
    """Set the connection string for sqlalchemy and write it to the config file.

    .. code-block:: python

        import pyhgnc
        pyhgnc.set_connection('mysql+pymysql://{user}:{passwd}@{host}/{db}?charset={charset}')


    .. hint::

        valid connection strings

        - mysql+pymysql://user:passwd@localhost/database?charset=utf8

        - postgresql://scott:tiger@localhost/mydatabase

        - mssql+pyodbc://user:passwd@database

        - oracle://user:passwd@127.0.0.1:1521/database

        - Linux: sqlite:////absolute/path/to/database.db

        - Windows: sqlite:///C:\path\to\database.db



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


def set_mysql_connection(host='localhost', user='pyhgnc_user', passwd='pyhgnc_passwd', db='pyhgnc',
                         charset='utf8'):
    """Method to set a MySQL connection

    :param str host: MySQL database host
    :param str user: MySQL database user
    :param str passwd: MySQL database password
    :param str db: MySQL database name
    :param str charset: MySQL database charater set

    :return: connection string
    :rtype: str
    """
    connection_string = 'mysql+pymysql://{user}:{passwd}@{host}/{db}?charset={charset}'.format(
        host=host,
        user=user,
        passwd=passwd,
        db=db,
        charset=charset
    )
    set_connection(connection_string)

    return connection_string
