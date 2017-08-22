# -*- coding: utf-8 -*-
"""PyHGNC loads HGNC contant into a relational database and provides a RESTFull API."""

import os
import time
import logging
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from tqdm import tqdm
from urllib import request
from datetime import datetime

from configparser import RawConfigParser, ConfigParser

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
            log.warning('No valid database connection. Execute `pyuniprot connection` on command line')

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

    def db_import(self, silent=False, from_path=None):
        self._drop_tables()
        self._create_tables()
        json_data = DbManager.load_hgnc_json(from_path)
        self.insert_data(hgnc_dict=json_data, silent=silent)

    @classmethod
    def get_date(cls, hgnc, key):
        date_value = hgnc.get(key)
        if date_value:
            return datetime.strptime(date_value, "%Y-%m-%d",).date()

    def insert_data(self, hgnc_dict, silent=False):

        for hgnc_data in tqdm(hgnc_dict['docs'], disable=silent):
            hgnc_table = {
                'symbol': hgnc_data['symbol'],
                'identifier': int(hgnc_data['hgnc_id'].split(':')[-1]),
                'name': hgnc_data['name'],
                'status': hgnc_data['status'],
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
                'intermediatefilamentdb': hgnc_data.get('intermediate_filament_db'),
                'pseudogeneorg': hgnc_data.get('pseudogene.org'),
                'bioparadigmsslc': hgnc_data.get('bioparadigms_slc'),
                'locationsortable': hgnc_data.get('location_sortable'),
                'merop': hgnc_data.get('merops'),
                'location': hgnc_data.get('location'),
                'cosmic': hgnc_data.get('cosmic'),
                'imgt': hgnc_data.get('imgt'),
                'date_name_changed': self.get_date(hgnc_data, 'date_name_changed'),
                'date_modified': self.get_date(hgnc_data, 'date_modified'),
                'date_symbol_changed': self.get_date(hgnc_data, 'date_symbol_changed'),
                'date_approved_reserved': self.get_date(hgnc_data, 'date_approved_reserved')
            }

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
        if not silent:
            print('load data into database')

        self.session.commit()

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


def update(connection=None, silent=False, from_path=None):
    database = DbManager(connection)
    database.db_import(silent=silent, from_path=from_path)
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


def set_mysql_connection(host='localhost', user='pyuniprot_user', passwd='pyuniprot_passwd', db='pyuniprot',
                         charset='utf8'):
    """Method to set a MySQL connection

    :param host: MySQL database host
    :param user: MySQL database user
    :param passwd: MySQL database password
    :param db: MySQL database name
    :param charset: MySQL database charater set
    :return: None
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
