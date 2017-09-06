# -*- coding: utf-8 -*-

import logging
import os
import shutil
import unittest
import datetime

import pyhgnc

from pandas.core.frame import DataFrame
from pyhgnc.constants import PYHGNC_TEST_DATA_DIR
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
        pass

    def test_query_alias_name(self):
        pass

    def test_query_gene_family(self):
        pass

    def test_query_ref_seq(self):
        pass

    def test_query_rgd(self):
        pass

    def test_query_omim(self):
        pass

    def test_query_mgd(self):
        pass

    def test_query_uniprot(self):
        pass

    def test_query_ccds(self):
        pass

    def test_query_pubmed(self):
        pass

    def test_query_ena(self):
        pass

    def test_query_enzyme(self):
        pass

    def test_query_lsdb(self):
        pass



    # def test_query_accession(self):
    #     accessions = self.query.accession(entry_name='5HT2A_PIG', limit=1, as_df=False)
    #
    #     accession = accessions[0]
    #     self.assertEqual(isinstance(accession, models.Accession), True)
    #     self.assertEqual(accession.accession, 'P50129')
    #
    #     df = self.query.accession(limit=1, as_df=True)
    #     self.assertEqual(isinstance(df, DataFrame), True)
    #
    # def test_query_alternative_full_name(self):
    #     alternative_full_names = self.query.alternative_full_name(
    #         name='Serotonin receptor 2A',
    #         entry_name='5HT2A_PIG',
    #         limit=1,
    #         as_df=False
    #     )
    #
    #     alternative_full_name = alternative_full_names[0]
    #     self.assertEqual(isinstance(alternative_full_name, models.AlternativeFullName), True)
    #     self.assertEqual(alternative_full_name.name, 'Serotonin receptor 2A')
    #
    #     df = self.query.alternative_full_name(limit=1, as_df=True)
    #     self.assertEqual(isinstance(df, DataFrame), True)
    #
    # def test_query_alternative_short_name(self):
    #     alternative_short_names = self.query.alternative_short_name(entry_name='AAH_ARATH', limit=1, as_df=False)
    #
    #     alternative_short_name = alternative_short_names[0]
    #     self.assertEqual(isinstance(alternative_short_name, models.AlternativeShortName), True)
    #     self.assertEqual(alternative_short_name.name, 'AtAAH')
    #
    #     df = self.query.alternative_short_name(limit=1, as_df=True)
    #     self.assertEqual(isinstance(df, DataFrame), True)
    #
    # def test_query_db_reference(self):
    #     db_references = self.query.db_reference(entry_name='5HT2A_PIG', limit=1, as_df=False)
    #
    #     db_reference = db_references[0]
    #     self.assertEqual(isinstance(db_reference, models.DbReference), True)
    #
    #     self.assertEqual((db_reference.identifier, db_reference.type_), ('S78208', 'EMBL'))
    #
    #     df = self.query.db_reference(limit=1, as_df=True)
    #     self.assertEqual(isinstance(df, DataFrame), True)
    #
    # def test_query_disease(self):
    #     diseases = self.query.disease(ref_id='177900', limit=1, as_df=False)
    #
    #     disease = diseases[0]
    #     self.assertEqual(isinstance(disease, models.Disease), True)
    #     self.assertEqual(disease.name, 'Psoriasis 1')
    #
    #     df = self.query.disease(limit=1, as_df=True)
    #     self.assertEqual(isinstance(df, DataFrame), True)
    #
    # def test_query_disease_comment(self):
    #     disease_comments = self.query.disease_comment(entry_name='1C06_HUMAN', limit=1, as_df=False)
    #
    #     disease_comment = disease_comments[0]
    #     self.assertEqual(isinstance(disease_comment, models.DiseaseComment), True)
    #
    #     expected_comment = "Disease susceptibility is associated with variations affecting the " \
    #                        "gene represented in this entry."
    #
    #     self.assertEqual(disease_comment.comment, expected_comment)
    #
    #     df = self.query.disease_comment(limit=1, as_df=True)
    #     self.assertEqual(isinstance(df, DataFrame), True)
    #
    # def test_query_ec_number(self):
    #     ec_numbers = self.query.ec_number(entry_name='AAH_ARATH', limit=1, as_df=False)
    #
    #     ec_number = ec_numbers[0]
    #     self.assertEqual(isinstance(ec_number, models.ECNumber), True)
    #     self.assertEqual(ec_number.ec_number, '3.5.3.9')
    #
    #     df = self.query.ec_number(limit=1, as_df=True)
    #     self.assertEqual(isinstance(df, DataFrame), True)
    #
    # def test_query_entry(self):
    #     entries = self.query.entry(name='5HT2A_PIG', limit=1, as_df=False)
    #
    #     entry = entries[0]
    #     self.assertEqual(isinstance(entry, models.Entry), True)
    #
    #     expected_entry = {
    #         'created': datetime.date(1996, 10, 1),
    #         'dataset': 'Swiss-Prot',
    #         'gene_name': 'HTR2A',
    #         'modified': datetime.date(2017, 5, 10),
    #         'name': '5HT2A_PIG',
    #         'recommended_full_name': '5-hydroxytryptamine receptor 2A',
    #         'recommended_short_name': '5-HT-2',
    #         'taxid': 9823,
    #         'version': 111}
    #
    #     for attribute, value in expected_entry.items():
    #         print(entry.__getattribute__(attribute))
    #         self.assertEqual(entry.__getattribute__(attribute), value)
    #
    #     df = self.query.entry(limit=1, as_df=True)
    #     self.assertEqual(isinstance(df, DataFrame), True)
    #
    # def test_query_feature(self):
    #     features = self.query.feature(entry_name='5HT2A_PIG', limit=1, as_df=False)
    #
    #     feature = features[0]
    #     self.assertEqual(isinstance(feature, models.Feature), True)
    #
    #     expected_feature = {
    #         'description': '5-hydroxytryptamine receptor 2A',
    #         'identifier': 'PRO_0000068949',
    #         'type_': 'chain'}
    #
    #     for attribute, value in expected_feature.items():
    #         print(feature.__getattribute__(attribute))
    #         self.assertEqual(feature.__getattribute__(attribute), value)
    #
    #     df = self.query.feature(limit=1, as_df=True)
    #     self.assertEqual(isinstance(df, DataFrame), True)
    #
    # def test_query_function(self):
    #     functions = self.query.function(entry_name='001R_FRG3G', limit=1, as_df=False)
    #     function_ = functions[0]
    #     self.assertEqual(isinstance(function_, models.Function), True)
    #     self.assertEqual(function_.text, 'Transcription activation.')
    #
    #     df = self.query.function(limit=1, as_df=True)
    #     self.assertEqual(isinstance(df, DataFrame), True)
    #
    # def test_query_keyword(self):
    #     keywords = self.query.keyword(identifier='KW-0085', limit=1, as_df=False)
    #
    #     keyword = keywords[0]
    #     self.assertEqual(isinstance(keyword, models.Keyword), True)
    #     self.assertEqual(keyword.name, 'Behavior')
    #
    #     df = self.query.keyword(limit=1, as_df=True)
    #     self.assertEqual(isinstance(df, DataFrame), True)
    #
    # def test_query_pmid(self):
    #     pmids = self.query.pmid( entry_name='5HT2A_PIG', limit=1, as_df=False)
    #
    #     pmid = pmids[0]
    #     self.assertEqual(isinstance(pmid, models.Pmid), True)
    #
    #     expected_pmid = {
    #         'date': 1995,
    #         'first': '201',
    #         'last': '206',
    #         'name': 'Biochim. Biophys. Acta',
    #         'pmid': 7794950,
    #         'title': 'Species differences in 5-HT2A receptors: cloned pig and rhesus monkey 5-HT2A receptors reveal '
    #                  'conserved transmembrane homology to the human rather than rat sequence.',
    #         'volume': 1236}
    #
    #     for attribute, value in expected_pmid.items():
    #         print(pmid.__getattribute__(attribute))
    #         self.assertEqual(pmid.__getattribute__(attribute), value)
    #
    #     df = self.query.pmid(limit=1, as_df=True)
    #     self.assertEqual(isinstance(df, DataFrame), True)
    #
    # def test_query_sequence(self):
    #     sequences = self.query.sequence(entry_name='5HT2A_PIG', limit=1, as_df=False)
    #
    #     sequence = sequences[0]
    #     self.assertEqual(isinstance(sequence, models.Sequence), True)
    #     self.assertEqual(sequence.sequence[-10:], 'NTVNEKVSCV')
    #
    #     df = self.query.sequence(limit=1, as_df=True)
    #     self.assertEqual(isinstance(df, DataFrame), True)
    #
    # def test_query_subcellular_location(self):
    #     subcellular_locations = self.query.subcellular_location(entry_name='AAH_ARATH', limit=1, as_df=False)
    #
    #     subcellular_location = subcellular_locations[0]
    #     self.assertEqual(isinstance(subcellular_location, models.SubcellularLocation), True)
    #     self.assertEqual(subcellular_location.location, 'Endoplasmic reticulum')
    #
    #     df = self.query.subcellular_location(limit=1, as_df=True)
    #     self.assertEqual(isinstance(df, DataFrame), True)
    #
    # def test_query_tissue_in_reference(self):
    #     tissue_in_references = self.query.tissue_in_reference(entry_name='5HT2A_PIG', limit=1, as_df=False)
    #
    #     tissue_in_reference = tissue_in_references[0]
    #     self.assertEqual(isinstance(tissue_in_reference, models.TissueInReference), True)
    #     self.assertEqual(tissue_in_reference.tissue, 'Pulmonary artery')
    #
    #     df = self.query.tissue_in_reference(limit=1, as_df=True)
    #     self.assertEqual(isinstance(df, DataFrame), True)
    #
    # def test_query_tissue_specificity(self):
    #     tissue_specificities = self.query.tissue_specificity(entry_name='AAH_ARATH', limit=1, as_df=False)
    #
    #     tissue_specificity = tissue_specificities[0]
    #     self.assertEqual(isinstance(tissue_specificity, models.TissueSpecificity), True)
    #     self.assertEqual(tissue_specificity.comment, 'Expressed in seedlings, roots, stems, leaves, '
    #                                                    'flowers, siliques and seeds.')
    #
    #     df = self.query.tissue_specificity(limit=1, as_df=True)
    #     self.assertEqual(isinstance(df, DataFrame), True)
    #
    # def test_prop_dbreference_types(self):
    #     self.assertEqual(len(self.query.dbreference_types), 60)
    #
    # def test_prop_taxids(self):
    #     self.assertEqual(set(self.query.taxids), set([9823, 3702, 9606, 654924]))
    #
    # def test_prop_datasets(self):
    #     self.assertEqual(self.query.datasets, ['Swiss-Prot'])
    #
    # def test_feature_types(self):
    #     self.assertEqual(len(self.query.feature_types), 15)
    #
    # def test_subcellular_locations(self):
    #     self.assertEqual(len(self.query.subcellular_locations), 8)
    #
    # def test_tissues_in_references(self):
    #     self.assertEqual(set(self.query.tissues_in_references), set(['Blood', 'Liver', 'Pulmonary artery']))
    #
    # def test_keywords(self):
    #     self.assertEqual(len(self.query.keywords), 29)
    #
    # def test_diseases(self):
    #     self.assertEqual(self.query.diseases, ['Psoriasis 1'])
    #
    # def test_version(self):
    #     expected_version = set(['Swiss-Prot:1968_12:1968-12-06', 'TrEMBL:2003_04:2003-04-25'])
    #     query_set = set([str(x) for x in self.query.version])
    #     self.assertEqual(expected_version, query_set)
