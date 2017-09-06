# -*- coding: utf-8 -*-

import logging
import os
import shutil
import unittest
import datetime

import pyhgnc

from pandas.core.frame import DataFrame
from pyhgnc.manager.defaults import sqlalchemy_connection_string_4_tests, DEFAULT_TEST_DATABASE_LOCATION
from pyhgnc.manager import models

from pyhgnc.manager.query import QueryManager

log = logging.getLogger(__name__)


class TestQuery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        test_data = os.path.join(dir_path, 'data')
        hgnc_test_file = os.path.join(test_data, 'hgnc_test.json')
        hcop_test_file = os.path.join(test_data, 'hcop_test.txt')

        test_connection = sqlalchemy_connection_string_4_tests

        pyhgnc.update(connection=test_connection, hgnc_file_path=hgnc_test_file, hcop_file_path=hcop_test_file)
        cls.query = QueryManager(connection=test_connection)

    @classmethod
    def tearDownClass(cls):
        cls.query.session.close()
        if os.path.isfile(DEFAULT_TEST_DATABASE_LOCATION):
            os.remove(DEFAULT_TEST_DATABASE_LOCATION)

    def test_number_of_inserts(self):
        models_list = [
            (models.HGNC, 3),
            (models.AliasSymbol, 7),    # Alias symbol and previous symbol
            (models.AliasName, 1),      # Alias name and previous name
            (models.GeneFamily, 3),
            (models.RefSeq, 3),
            (models.RGD, 3),
            (models.OMIM, 1),
            (models.MGD, 3),
            (models.UniProt, 3),
            (models.CCDS, 6),
            (models.PubMed, 4),
            (models.ENA, 2),
            (models.Enzyme, 0),
            (models.LSDB, 0),
            (models.OrthologyPrediction, 70),
        ]
        for model, num_of_results in models_list:
            self.assertEqual(num_of_results, self.query.session.query(model).count())

    def test_query_hgnc(self):
        A1BG_dict = {
            'bioparadigmsslc': None,
            'cosmic': 'A1BG',
            'date_approved_reserved': '1989-06-30',
            'date_modified': '2015-07-13',
            'date_name_changed': None,
            'date_symbol_changed': None,
            'ensembl_gene': 'ENSG00000121410',
            'entrez': '1',
            'horde': None,
            'identifier': 5,
            'imgt': None,
            'iuphar': None,
            'lncrnadb': None,
            'location': '19q13.43',
            'locationsortable': '19q13.43',
            'locus_group': 'protein-coding gene',
            'locus_type': 'gene with protein product',
            'merops': 'I43.950',
            'mirbase': None,
            'name': 'alpha-1-B glycoprotein',
            'orphanet': None,
            'pseudogeneorg': None,
            'snornabase': None,
            'status': 'Approved',
            'symbol': 'A1BG',
            'ucsc': 'uc002qsd.5',
            'uuid': 'fe3e34f6-c539-4337-82c1-1b4e8c115992',
            'vega': 'OTTHUMG00000183507'
        }

        hgnc = self.query.hgnc(symbol="A1BG")[0]
        self.assertIsInstance(hgnc, models.HGNC)
        self.assertEqual(hgnc.symbol, "A1BG")
        self.assertEqual(hgnc.to_dict(), A1BG_dict)

        hgnc_df = self.query.hgnc(symbol="A1BG", as_df=True)
        self.assertIsInstance(hgnc_df, DataFrame)

    def test_query_orthology_prediction(self):
        orthology_predictions = self.query.orthology_prediction(hgnc_identifier=5)
        self.assertEqual(len(orthology_predictions), 24)

        for prediction in orthology_predictions:
            self.assertIsInstance(prediction, models.OrthologyPrediction)

        orthology_predictions_df = self.query.orthology_prediction(as_df=True)
        self.assertIsInstance(orthology_predictions_df, DataFrame)

    def test_query_alias_symbol(self):
        ZSWIM1_aliases = [
            {
                'hgnc_symbol': 'ZSWIM1',
                'hgnc_identifier': 16155,
                'alias_symbol': "dJ337O18.5",
                'is_previous_symbol': False
            },
            {
                'hgnc_symbol': 'ZSWIM1',
                'hgnc_identifier': 16155,
                'alias_symbol': "C20orf162",
                'is_previous_symbol': True
            }
        ]

        aliases = self.query.alias_symbol(hgnc_symbol="ZSWIM1")
        for alias in aliases:
            self.assertIsInstance(alias, models.AliasSymbol)
            self.assertIn(alias.to_dict(), ZSWIM1_aliases)

    def test_query_alias_name(self):
        ZSWIM1_aliases = [{
            'hgnc_symbol': 'ZSWIM1',
            'hgnc_identifier': 16155,
            'alias_name': "chromosome 20 open reading frame 162",
            'is_previous_name': True
        }]

        alias = self.query.alias_name(hgnc_symbol="ZSWIM1")[0]
        self.assertIsInstance(alias, models.AliasName)
        self.assertIn(alias.to_dict(), ZSWIM1_aliases)

    def test_query_gene_family(self):
        families = [
            {
                'family_identifier': 594,
                'family_name': 'Immunoglobulin like domain containing',
                'hgnc_symbols': [
                    'A1BG'
                ]
            },
            {
                'family_identifier': 90,
                'family_name': 'Zinc fingers SWIM-type',
                'hgnc_symbols': [
                    'ZSWIM1'
                ]
            },
            {
                'family_identifier': 725,
                'family_name': 'RNA binding motif containing',
                'hgnc_symbols': [
                    'A1CF'
                ]
            }
        ]

        gene_families = self.query.gene_family()
        for family in gene_families:
            self.assertIsInstance(family, models.GeneFamily)
            self.assertIn(family.to_dict(), families)

        A1BG_family = self.query.gene_family(hgnc_identifier=5)[0]
        self.assertEqual(A1BG_family.to_dict(), families[0])

        ZSWIM1_family = self.query.gene_family(hgnc_symbol="ZSWIM1")[0]
        self.assertEqual(ZSWIM1_family.to_dict(), families[1])

        A1CF_family = self.query.gene_family(family_identifier=725)[0]
        self.assertEqual(A1CF_family.to_dict(), families[2])

    def test_query_ref_seq(self):
        A1CF_ref_seq = {
            'hgnc_symbol': "A1CF",
            'hgnc_identifier': 24086,
            'accession': "NM_014576"
        }
        ref_seq = self.query.ref_seq(hgnc_symbol="A1CF")[0]

        self.assertIsInstance(ref_seq, models.RefSeq)
        self.assertEqual(ref_seq.to_dict(), A1CF_ref_seq)

    def test_query_rgd(self):
        ZSQIM1_rgd = {
            'rgdid': 1305715,
            'hgnc_symbols': [
                'ZSWIM1'
            ]
        }
        rgd = self.query.rgd(rgdid=1305715)[0]
        self.assertIsInstance(rgd, models.RGD)
        self.assertEqual(rgd.to_dict(), ZSQIM1_rgd)

    def test_query_omim(self):
        A1BG_omim = {
            'hgnc_symbol': "A1BG",
            'hgnc_identifier': 5,
            'omimid': 138670
        }

        omim = self.query.omim(hgnc_identifier=5)[0]
        self.assertIsInstance(omim, models.OMIM)
        self.assertEqual(omim.to_dict(), A1BG_omim)

    def test_query_mgd(self):
        A1CF_mgd = {
            'hgnc_symbols': [
                "A1CF"
            ],
            'mgdid': 1917115
        }

        mgd = self.query.mgd(hgnc_symbol="A1CF")[0]
        self.assertIsInstance(mgd, models.MGD)
        self.assertEqual(mgd.to_dict(), A1CF_mgd)

    def test_query_uniprot(self):
        A1CF_uniprot = {
            'hgnc_symbols': [
                "A1CF"
            ],
            'uniprotid': "Q9NQ94"
        }

        uniprot = self.query.uniprot(hgnc_identifier=24086)[0]
        self.assertIsInstance(uniprot, models.UniProt)
        self.assertEqual(uniprot.to_dict(), A1CF_uniprot)

    def test_query_ccds(self):
        A1CF_ccds = [
            {
                'hgnc_symbol': "A1CF",
                'hgnc_identifier': 24086,
                'ccdsid': "CCDS7241"
            },
            {
                'hgnc_symbol': "A1CF",
                'hgnc_identifier': 24086,
                'ccdsid': "CCDS7242"
            },
            {
                'hgnc_symbol': "A1CF",
                'hgnc_identifier': 24086,
                'ccdsid': "CCDS7243"
            },
            {
                'hgnc_symbol': "A1CF",
                'hgnc_identifier': 24086,
                'ccdsid': "CCDS73133"
            },
        ]

        ccds = self.query.ccds(hgnc_identifier=24086)

        for ccd in ccds:
            self.assertIsInstance(ccd, models.CCDS)
            self.assertIn(ccd.to_dict(), A1CF_ccds)

    def test_query_pubmed(self):
        A1CF_pubmeds = [
            {
                'hgnc_symbols': [
                    "A1CF"
                ],
                'pubmedid': 11815617
            },
            {
                'hgnc_symbols': [
                    "A1CF"
                ],
                'pubmedid': 11072063
            }
        ]

        pubmeds = self.query.pubmed(hgnc_symbol="A1CF")
        for pubmed in pubmeds:
            self.assertIsInstance(pubmed, models.PubMed)
            self.assertIn(pubmed.to_dict(), A1CF_pubmeds)

    def test_query_ena(self):
        A1CF_ena = {
            'hgnc_symbols': [
                "A1CF"
            ],
            'enaid': "AF271790"
        }

        ena = self.query.ena(hgnc_symbol="A1CF")[0]
        self.assertIsInstance(ena, models.ENA)
        self.assertEqual(ena.to_dict(), A1CF_ena)
