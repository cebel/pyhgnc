from .database import BaseDbManager
from collections import Iterable
from pandas import read_sql
from . import models
import sqlalchemy


class QueryManager(BaseDbManager):
    """Query interface to database."""

    def _limit_and_df(self, query, limit, as_df=False):
        """adds a limit (limit==None := no limit) to any query and allow a return as pandas.DataFrame

        :param bool as_df: if is set to True results return as pandas.DataFrame
        :param `sqlalchemy.orm.query.Query` query: SQL Alchemy query
        :param int,tuple limit: maximum number of results
        :return: query result of pyhgnc.manager.models.XY objects
        """
        if limit:

            if isinstance(limit, int):
                query = query.limit(limit)

            if isinstance(limit, Iterable) and len(limit) == 2 and [int, int] == [type(x) for x in limit]:
                page, page_size = limit
                query = query.limit(page_size)
                query = query.offset(page * page_size)

        if as_df:
            results = read_sql(query.statement, self.engine)

        else:
            try:
                results = query.all()
            except sqlalchemy.exec.Statement.Error:
                query.session.rollback()
                results = query.all()

        return results

    def get_model_queries(self, query_obj, model_queries_config):
        """use this if your are searching for a field in the same model"""
        for search4, model_attrib in model_queries_config:

            if search4 is not None:
                query_obj = self._model_query(query_obj, search4, model_attrib)
        return query_obj

    def get_many_to_many_queries(self, query_obj, many_to_many_queries_config):
        for search4, model_attrib, many2many_attrib in many_to_many_queries_config:
            if search4 is not None:
                query_obj = self._many_to_many_query(query_obj, search4, model_attrib, many2many_attrib)
        return query_obj

    def get_one_to_many_queries(self, query_obj, one_to_many_queries):
        for search4, model_attrib in one_to_many_queries:
            if search4 is not None:
                query_obj = self._one_to_many_query(query_obj, search4, model_attrib)
        return query_obj

    @classmethod
    def _one_to_many_query(cls, query_obj, search4, model_attrib):
        """extends and returns a SQLAlchemy query object to allow one-to-many queries

        :param query_obj: SQL Alchemy query object
        :param str search4: search string
        :param model_attrib: attribute in model
        """
        model = model_attrib.parent.class_

        already_joined_tables = [mapper.class_ for mapper in query_obj._join_entities]

        if isinstance(search4, (str, int, Iterable)) and model not in already_joined_tables:
            query_obj = query_obj.join(model)

        if isinstance(search4, str):
            query_obj = query_obj.filter(model_attrib.like(search4))

        elif isinstance(search4, int):
            query_obj = query_obj.filter(model_attrib == search4)

        elif isinstance(search4, Iterable):
            query_obj = query_obj.filter(model_attrib.in_(search4))

        return query_obj

    @classmethod
    def _many_to_many_query(cls, query_obj, search4, join_attrib, many2many_attrib):

        model = join_attrib.property.mapper.class_

        already_joined_tables = [mapper.class_ for mapper in query_obj._join_entities]

        if isinstance(search4, (str, int, Iterable)) and model not in already_joined_tables:
            query_obj = query_obj.join(join_attrib)

        if isinstance(search4, str):
            query_obj = query_obj.filter(many2many_attrib.like(search4))

        elif isinstance(search4, int):
            query_obj = query_obj.filter(many2many_attrib == search4)

        elif isinstance(search4, Iterable):
            query_obj = query_obj.filter(many2many_attrib.in_(search4))

        return query_obj

    @classmethod
    def _model_query(cls, query_obj, search4, model_attrib):

        if isinstance(search4, str):
            query_obj = query_obj.filter(model_attrib.like(search4))
        elif isinstance(search4, int):
            query_obj = query_obj.filter(model_attrib == search4)
        elif isinstance(search4, Iterable):
            query_obj = query_obj.filter(model_attrib.in_(search4))
        return query_obj

    def hgnc(self, name=None, symbol=None, identifier=None, status=None, uuid=None, locus_group=None, orphanet=None,
             locus_type=None, date_name_changed=None, date_modified=None, date_symbol_changed=None, pubmedid=None,
             date_approved_reserved=None, ensembl_gene=None, horde=None, vega=None, lncrnadb=None, uniprotid=None,
             entrez=None, mirbase=None, iuphar=None, ucsc=None, snornabase=None, gene_family_name=None, mgdid=None,
             pseudogeneorg=None, bioparadigmsslc=None, locationsortable=None, ec_number=None, refseq_accession=None,
             merops=None, location=None, cosmic=None, imgt=None, enaid=None, alias_symbol=None, alias_name=None,
             rgdid=None, omimid=None, ccdsid=None, lsdbs=None, ortholog_species=None, gene_family_identifier=None,
             limit=None, as_df=False):
        """Method to query :class:`pyhgnc.manager.models.Pmid`


        :param name: HGNC approved name for the gene
        :type name: str or tuple(str) or None

        :param symbol: HGNC approved gene symbol
        :type symbol: str or tuple(str) or None

        :param identifier: HGNC ID. A unique ID created by the HGNC for every approved symbol
        :type identifier: int or tuple(int) or None

        :param status: Status of the symbol report, which can be either "Approved" or "Entry Withdrawn"
        :type status: str or tuple(str) or None

        :param uuid: universally unique identifier
        :type uuid: str or tuple(str) or None

        :param locus_group: group name for a set of related locus types as defined by the HGNC
        :type locus_group: str or tuple(str) or None

        :param orphanet: Orphanet database identifier (related to rare diseases and orphan drugs)
        :type orphanet: int ot tuple(int) or None

        :param locus_type: locus type as defined by the HGNC (e.g. RNA, transfer)
        :type locus_type: str or tuple(str) or None

        :param date_name_changed: date the gene name was last changed (format: YYYY-mm-dd, e.g. 2017-09-29)
        :type date_name_changed: str or tuple(str) or None

        :param date_modified: date the entry was last modified (format: YYYY-mm-dd, e.g. 2017-09-29)
        :type date_modified: str or tuple(str) or None

        :param date_symbol_changed: date the gene symbol was last changed (format: YYYY-mm-dd, e.g. 2017-09-29)
        :type date_symbol_changed: str or tuple(str) or None

        :param date_approved_reserved: date the entry was first approved (format: YYYY-mm-dd, e.g. 2017-09-29)
        :type date_approved_reserved: str or tuple(str) or None

        :param pubmedid: PubMed identifier
        :type pubmedid: int ot tuple(int) or None

        :param ensembl_gene: Ensembl gene ID. Found within the "GENE RESOURCES" section of the gene symbol report
        :type ensembl_gene: str or tuple(str) or None

        :param horde: symbol used within HORDE for the gene (not available in JSON)
        :type horde: str or tuple(str) or None

        :param vega: Vega gene ID. Found within the "GENE RESOURCES" section of the gene symbol report
        :type vega: str or tuple(str) or None

        :param lncrnadb: Noncoding RNA Database identifier
        :type lncrnadb: str or tuple(str) or None

        :param uniprotid: UniProt identifier
        :type uniprotid: str or tuple(str) or None

        :param entrez: Entrez gene ID. Found within the "GENE RESOURCES" section of the gene symbol report
        :type entrez: str or tuple(str) or None

        :param mirbase: miRBase ID
        :type mirbase: str or tuple(str) or None

        :param iuphar: The objectId used to link to the IUPHAR/BPS Guide to PHARMACOLOGY database
        :type iuphar: str or tuple(str) or None

        :param ucsc: UCSC gene ID. Found within the "GENE RESOURCES" section of the gene symbol report
        :type ucsc: str or tuple(str) or None

        :param snornabase: snoRNABase ID
        :type snornabase: str or tuple(str) or None

        :param gene_family_name: Gene family name
        :type gene_family_name: str or tuple(str) or None

        :param gene_family_identifier: Gene family identifier
        :type gene_family_name: int or tuple(int) or None

        :param mgdid: Mouse Genome Database identifier
        :type mgdid: int ot tuple(int) or None

        :param imgt: Symbol used within international ImMunoGeneTics information system
        :type imgt: str or tuple(str) or None

        :param enaid: European Nucleotide Archive (ENA) identifier
        :type enaid: str or tuple(str) or None

        :param alias_symbol: Other symbols used to refer to a gene
        :type alias_symbol: str or tuple(str) or None

        :param alias_name: Other names used to refer to a gene
        :type alias_name: str or tuple(str) or None

        :param pseudogeneorg: Pseudogene.org ID
        :type pseudogeneorg: str or tuple(str) or None

        :param bioparadigmsslc: Symbol used to link to the SLC tables database at bioparadigms.org for the gene
        :type bioparadigmsslc: str or tuple(str) or None

        :param locationsortable: locations sortable
        :type locationsortable: str or tuple(str) or None

        :param ec_number: Enzyme Commission number (EC number)
        :type ec_number: str or tuple(str) or None

        :param refseq_accession: RefSeq nucleotide accession(s)
        :type refseq_accession: str or tuple(str) or None

        :param merops: ID used to link to the MEROPS peptidase database
        :type merops: str or tuple(str) or None

        :param location: Cytogenetic location of the gene (e.g. 2q34).
        :type location: str or tuple(str) or None

        :param cosmic: Symbol used within the Catalogue of somatic mutations in cancer for the gene
        :type cosmic: str or tuple(str) or None

        :param rgdid: Rat genome database gene ID
        :type rgdid: int or tuple(int) or None

        :param omimid: Online Mendelian Inheritance in Man (OMIM) ID
        :type omimid: int or tuple(int) or None

        :param ccdsid: Consensus CDS ID
        :type ccdsid: str or tuple(str) or None

        :param lsdbs: Locus Specific Mutation Database Name
        :type lsdbs: str or tuple(str) or None

        :param ortholog_species: Ortholog species NCBI taxonomy identifier
        :type ortholog_species: int or tuple(int) or None

        :param limit:
            - if `isinstance(limit,int)==True` -> limit
            - if `isinstance(limit,tuple)==True` -> format:= tuple(page_number, results_per_page)
            - if limit == None -> all results
        :type limit: int or tuple(int) or None

        :param bool as_df: if `True` results are returned as :class:`pandas.DataFrame`

        :return:
            - if `as_df == False` -> list(:class:`.models.Keyword`)
            - if `as_df == True`  -> :class:`pandas.DataFrame`
        :rtype: list(:class:`.models.Keyword`) or :class:`pandas.DataFrame`
        """
        q = self.session.query(models.HGNC)

        model_queries_config = (
            (orphanet, models.HGNC.orphanet),
            (name, models.HGNC.name),
            (symbol, models.HGNC.symbol),
            (identifier, models.HGNC.identifier),
            (status, models.HGNC.status),
            (uuid, models.HGNC.uuid),
            (locus_group, models.HGNC.locus_group),
            (locus_type, models.HGNC.locus_type),
            (date_name_changed, models.HGNC.date_name_changed),
            (date_modified, models.HGNC.date_modified),
            (date_symbol_changed, models.HGNC.date_symbol_changed),
            (date_approved_reserved, models.HGNC.date_approved_reserved),
            (ensembl_gene, models.HGNC.ensembl_gene),
            (horde, models.HGNC.horde),
            (vega, models.HGNC.vega),
            (lncrnadb, models.HGNC.lncrnadb),
            (entrez, models.HGNC.entrez),
            (mirbase, models.HGNC.mirbase),
            (iuphar, models.HGNC.iuphar),
            (ucsc, models.HGNC.ucsc),
            (snornabase, models.HGNC.snornabase),
            (pseudogeneorg, models.HGNC.pseudogeneorg),
            (bioparadigmsslc, models.HGNC.bioparadigmsslc),
            (locationsortable, models.HGNC.locationsortable),
            (merops, models.HGNC.merops),
            (location, models.HGNC.location),
            (cosmic, models.HGNC.cosmic),
            (imgt, models.HGNC.imgt),
        )
        q = self.get_model_queries(q, model_queries_config)

        many_to_many_queries_config = (
            (ec_number, models.HGNC.enzymes, models.Enzyme.ec_number),
            (gene_family_name, models.HGNC.gene_families, models.GeneFamily.family_name),
            (gene_family_identifier, models.HGNC.gene_families, models.GeneFamily.family_identifier),
            (refseq_accession, models.HGNC.refseqs, models.RefSeq.accession),
            (mgdid, models.HGNC.mgds, models.MGD.mgdid),
            (uniprotid, models.HGNC.uniprots, models.UniProt.uniprotid),
            (pubmedid, models.HGNC.pubmeds, models.PubMed.pubmedid),
            (enaid, models.HGNC.enas, models.ENA.enaid),
        )
        q = self.get_many_to_many_queries(q, many_to_many_queries_config)

        one_to_many_queries_config = (
            (alias_symbol, models.AliasSymbol.alias_symbol),
            (alias_name, models.AliasName.alias_name),
            (rgdid, models.RGD.rgdid),
            (omimid, models.OMIM.omimid),
            (ccdsid, models.CCDS.ccdsid),
            (lsdbs, models.LSDB.lsdb),
            (ortholog_species, models.OrthologyPrediction.ortholog_species),
        )
        q = self.get_one_to_many_queries(q, one_to_many_queries_config)

        return self._limit_and_df(q, limit, as_df)

    def orthology_prediction(self,
                             ortholog_species=None,
                             human_entrez_gene=None,
                             human_ensembl_gene=None,
                             human_name=None,
                             human_symbol=None,
                             human_chr=None,
                             human_assert_ids=None,
                             ortholog_species_entrez_gene=None,
                             ortholog_species_ensembl_gene=None,
                             ortholog_species_db_id=None,
                             ortholog_species_name=None,
                             ortholog_species_symbol=None,
                             ortholog_species_chr=None,
                             ortholog_species_assert_ids=None,
                             support=None,
                             hgnc_identifier=None,
                             hgnc_symbol=None,
                             limit=None,
                             as_df=False):
        """Method to query :class:`pyhgnc.manager.models.Pmid`

        :param int ortholog_species: NCBI taxonomy identifier
        :param str human_entrez_gene: Entrez gene identifier
        :param str human_ensembl_gene: Ensembl identifier
        :param str human_name: human gene name
        :param str human_symbol: human gene symbol
        :param str human_chr: human chromosome
        :param str human_assert_ids:
        :param str ortholog_species_entrez_gene: Entrez gene identifier for ortholog
        :param str ortholog_species_ensembl_gene: Ensembl gene identifier for ortholog
        :param str ortholog_species_db_id: Species specific database identifier (e.g. MGI:1920453)
        :param str ortholog_species_name: gene name of ortholog
        :param str ortholog_species_symbol: gene symbol of ortholog
        :param str ortholog_species_chr: chromosome identifier (ortholog)
        :param str ortholog_species_assert_ids:
        :param str support:
        :param int hgnc_identifier: HGNC identifier
        :param str hgnc_symbol: HGNC symbol

        :param limit:
            - if `isinstance(limit,int)==True` -> limit
            - if `isinstance(limit,tuple)==True` -> format:= tuple(page_number, results_per_page)
            - if limit == None -> all results
        :type limit: int or tuple(int) or None

        :param bool as_df: if `True` results are returned as :class:`pandas.DataFrame`

        :return:
            - if `as_df == False` -> list(:class:`.models.Keyword`)
            - if `as_df == True`  -> :class:`pandas.DataFrame`
        :rtype: list(:class:`.models.Keyword`) or :class:`pandas.DataFrame`
        """
        q = self.session.query(models.OrthologyPrediction)

        model_queries_config = (
            (ortholog_species, models.OrthologyPrediction.ortholog_species),
            (human_entrez_gene, models.OrthologyPrediction.human_entrez_gene),
            (human_ensembl_gene, models.OrthologyPrediction.human_ensembl_gene),
            (human_name, models.OrthologyPrediction.human_name),
            (human_symbol, models.OrthologyPrediction.human_symbol),
            (human_chr, models.OrthologyPrediction.human_chr),
            (human_assert_ids, models.OrthologyPrediction.human_assert_ids),
            (ortholog_species_entrez_gene, models.OrthologyPrediction.ortholog_species_entrez_gene),
            (ortholog_species_ensembl_gene, models.OrthologyPrediction.ortholog_species_ensembl_gene),
            (ortholog_species_db_id, models.OrthologyPrediction.ortholog_species_db_id),
            (ortholog_species_name, models.OrthologyPrediction.ortholog_species_name),
            (ortholog_species_symbol, models.OrthologyPrediction.ortholog_species_symbol),
            (ortholog_species_chr, models.OrthologyPrediction.ortholog_species_chr),
            (ortholog_species_assert_ids, models.OrthologyPrediction.ortholog_species_assert_ids),
            (support, models.OrthologyPrediction.support),
        )
        q = self.get_model_queries(q, model_queries_config)

        one_to_many_queries_config = (
            (hgnc_identifier, models.HGNC.identifier),
            (hgnc_symbol, models.HGNC.symbol),
        )
        q = self.get_one_to_many_queries(q, one_to_many_queries_config)

        return self._limit_and_df(q, limit, as_df)

    def alias_symbol(self,
                     alias_symbol=None,
                     is_previous_symbol=None,
                     hgnc_symbol=None,
                     hgnc_identifier=None,
                     limit=None,
                     as_df=False):
        """Method to query :class:`.models.AliasSymbol` objects in database

        :param alias_symbol: alias symbol(s)
        :type alias_symbol: str or tuple(str) or None

        :param is_previous_symbol: flag for 'is previous'
        :type is_previous_symbol: bool or tuple(bool) or None

        :param hgnc_symbol: HGNC symbol(s)
        :type hgnc_symbol: str or tuple(str) or None

        :param hgnc_identifier: identifiers(s) in :class:`.models.HGNC`
        :type hgnc_identifier: int or tuple(int) or None

        :param limit:
            - if `isinstance(limit,int)==True` -> limit
            - if `isinstance(limit,tuple)==True` -> format:= tuple(page_number, results_per_page)
            - if limit == None -> all results
        :type limit: int or tuple(int) or None

        :param bool as_df: if `True` results are returned as :class:`pandas.DataFrame`

        :return:
            - if `as_df == False` -> list(:class:`.models.AliasSymbol`)
            - if `as_df == True`  -> :class:`pandas.DataFrame`
        :rtype: list(:class:`.models.AliasSymbol`) or :class:`pandas.DataFrame`

        """
        q = self.session.query(models.AliasSymbol)

        model_queries_config = (
            (alias_symbol, models.AliasSymbol.alias_symbol),
            (is_previous_symbol, models.AliasSymbol.is_previous_symbol),
        )
        q = self.get_model_queries(q, model_queries_config)

        one_to_many_queries_config = (
            (hgnc_symbol, models.HGNC.symbol),
            (hgnc_identifier, models.HGNC.identifier)
        )
        q = self.get_one_to_many_queries(q, one_to_many_queries_config)

        return self._limit_and_df(q, limit, as_df)

    def alias_name(self,
                   alias_name=None,
                   is_previous_name=None,
                   hgnc_symbol=None,
                   hgnc_identifier=None,
                   limit=None,
                   as_df=False):
        """Method to query :class:`.models.AliasName` objects in database

        :param alias_name: alias name(s)
        :type alias_name: str or tuple(str) or None

        :param is_previous_name: flag for 'is previous'
        :type is_previous_name: bool or tuple(bool) or None

        :param hgnc_symbol: HGNC symbol(s)
        :type hgnc_symbol: str or tuple(str) or None

        :param hgnc_identifier: identifiers(s) in :class:`.models.HGNC`
        :type hgnc_identifier: int or tuple(int) or None

        :param limit:
            - if `isinstance(limit,int)==True` -> limit
            - if `isinstance(limit,tuple)==True` -> format:= tuple(page_number, results_per_page)
            - if limit == None -> all results
        :type limit: int or tuple(int) or None

        :param bool as_df: if `True` results are returned as :class:`pandas.DataFrame`

        :return:
            - if `as_df == False` -> list(:class:`.models.AliasSymbol`)
            - if `as_df == True`  -> :class:`pandas.DataFrame`
        :rtype: list(:class:`.models.AliasSymbol`) or :class:`pandas.DataFrame`

        """
        q = self.session.query(models.AliasName)

        model_queries_config = (
            (alias_name, models.AliasName.alias_name),
            (is_previous_name, models.AliasName.is_previous_name),
        )
        q = self.get_model_queries(q, model_queries_config)

        one_to_many_queries_config = (
            (hgnc_symbol, models.HGNC.symbol),
            (hgnc_identifier, models.HGNC.identifier)
        )
        q = self.get_one_to_many_queries(q, one_to_many_queries_config)

        return self._limit_and_df(q, limit, as_df)

    def gene_family(self,
                    family_identifier=None,
                    family_name=None,
                    hgnc_symbol=None,
                    hgnc_identifier=None,
                    limit=None,
                    as_df=False):
        """Method to query :class:`.models.GeneFamily` objects in database

        :param family_identifier: gene family identifier(s)
        :type family_identifier: int or tuple(int) or None

        :param family_name: gene family name(s)
        :type family_name: str or tuple(str) or None

        :param hgnc_symbol: HGNC symbol(s)
        :type hgnc_symbol: str or tuple(str) or None

        :param hgnc_identifier: identifiers(s) in :class:`.models.HGNC`
        :type hgnc_identifier: int or tuple(int) or None

        :param limit:
            - if `isinstance(limit,int)==True` -> limit
            - if `isinstance(limit,tuple)==True` -> format:= tuple(page_number, results_per_page)
            - if limit == None -> all results
        :type limit: int or tuple(int) or None

        :param bool as_df: if `True` results are returned as :class:`pandas.DataFrame`

        :return:
            - if `as_df == False` -> list(:class:`.models.AliasSymbol`)
            - if `as_df == True`  -> :class:`pandas.DataFrame`
        :rtype: list(:class:`.models.AliasSymbol`) or :class:`pandas.DataFrame`

        """
        q = self.session.query(models.GeneFamily)

        model_queries_config = (
            (family_identifier, models.GeneFamily.family_identifier),
            (family_name, models.GeneFamily.family_name),
        )
        q = self.get_model_queries(q, model_queries_config)

        many_to_many_queries_config = (
            (hgnc_symbol, models.GeneFamily.hgncs, models.HGNC.symbol),
            (hgnc_identifier, models.GeneFamily.hgncs, models.HGNC.identifier),
        )
        q = self.get_many_to_many_queries(q, many_to_many_queries_config)

        return self._limit_and_df(q, limit, as_df)

    def ref_seq(self, accession=None, hgnc_symbol=None, hgnc_identifier=None, limit=None, as_df=False):
        """Method to query :class:`.models.RefSeq` objects in database

        :param accession: RefSeq accessionl(s)
        :type accession: str or tuple(str) or None

        :param hgnc_symbol: HGNC symbol(s)
        :type hgnc_symbol: str or tuple(str) or None

        :param hgnc_identifier: identifiers(s) in :class:`.models.HGNC`
        :type hgnc_identifier: int or tuple(int) or None

        :param limit:
            - if `isinstance(limit,int)==True` -> limit
            - if `isinstance(limit,tuple)==True` -> format:= tuple(page_number, results_per_page)
            - if limit == None -> all results
        :type limit: int or tuple(int) or None

        :param bool as_df: if `True` results are returned as :class:`pandas.DataFrame`

        :return:
            - if `as_df == False` -> list(:class:`.models.RefSeq`)
            - if `as_df == True`  -> :class:`pandas.DataFrame`
        :rtype: list(:class:`.models.RefSeq`) or :class:`pandas.DataFrame`

        """
        q = self.session.query(models.RefSeq)

        model_queries_config = (
            (accession, models.RefSeq.accession),
        )
        q = self.get_model_queries(q, model_queries_config)

        many_to_many_queries_config = (
            (hgnc_symbol, models.RefSeq.hgncs, models.HGNC.symbol),
            (hgnc_identifier, models.RefSeq.hgncs, models.HGNC.identifier),
        )
        q = self.get_many_to_many_queries(q, many_to_many_queries_config)

        return self._limit_and_df(q, limit, as_df)

    def rgd(self, rgdid=None, hgnc_symbol=None, hgnc_identifier=None, limit=None, as_df=False):
        """Method to query :class:`.models.RGD` objects in database

        :param rgdid: Rat genome database gene ID(s)
        :type rgdid: str or tuple(str) or None

        :param hgnc_symbol: HGNC symbol(s)
        :type hgnc_symbol: str or tuple(str) or None

        :param hgnc_identifier: identifiers(s) in :class:`.models.HGNC`
        :type hgnc_identifier: int or tuple(int) or None

        :param limit:
            - if `isinstance(limit,int)==True` -> limit
            - if `isinstance(limit,tuple)==True` -> format:= tuple(page_number, results_per_page)
            - if limit == None -> all results
        :type limit: int or tuple(int) or None

        :param bool as_df: if `True` results are returned as :class:`pandas.DataFrame`

        :return:
            - if `as_df == False` -> list(:class:`.models.RGD`)
            - if `as_df == True`  -> :class:`pandas.DataFrame`
        :rtype: list(:class:`.models.RGD`) or :class:`pandas.DataFrame`

        """
        q = self.session.query(models.RGD)

        model_queries_config = (
            (rgdid, models.RGD.rgdid),
        )
        q = self.get_model_queries(q, model_queries_config)

        many_to_many_queries_config = (
            (hgnc_symbol, models.RGD.hgncs, models.HGNC.symbol),
            (hgnc_identifier, models.RGD.hgncs, models.HGNC.identifier),
        )
        q = self.get_many_to_many_queries(q, many_to_many_queries_config)

        return self._limit_and_df(q, limit, as_df)

    def omim(self, omimid=None, hgnc_symbol=None, hgnc_identifier=None, limit=None, as_df=False):
        """Method to query :class:`.models.OMIM` objects in database

        :param omimid: Online Mendelian Inheritance in Man (OMIM) ID(s)
        :type omimid: str or tuple(str) or None

        :param hgnc_symbol: HGNC symbol(s)
        :type hgnc_symbol: str or tuple(str) or None

        :param hgnc_identifier: identifiers(s) in :class:`.models.HGNC`
        :type hgnc_identifier: int or tuple(int) or None

        :param limit:
            - if `isinstance(limit,int)==True` -> limit
            - if `isinstance(limit,tuple)==True` -> format:= tuple(page_number, results_per_page)
            - if limit == None -> all results
        :type limit: int or tuple(int) or None

        :param bool as_df: if `True` results are returned as :class:`pandas.DataFrame`

        :return:
            - if `as_df == False` -> list(:class:`.models.OMIM`)
            - if `as_df == True`  -> :class:`pandas.DataFrame`
        :rtype: list(:class:`.models.OMIM`) or :class:`pandas.DataFrame`

        """
        q = self.session.query(models.OMIM)

        model_queries_config = (
            (omimid, models.OMIM.omimid),
        )
        q = self.get_model_queries(q, model_queries_config)

        one_to_many_queries_config = (
            (hgnc_symbol, models.HGNC.symbol),
            (hgnc_identifier, models.HGNC.identifier)
        )
        q = self.get_one_to_many_queries(q, one_to_many_queries_config)

        return self._limit_and_df(q, limit, as_df)

    def mgd(self, mgdid=None, hgnc_symbol=None, hgnc_identifier=None, limit=None, as_df=False):
        """Method to query :class:`.models.MGD` objects in database

        :param mgdid: Mouse genome informatics database ID(s)
        :type mgdid: str or tuple(str) or None

        :param hgnc_symbol: HGNC symbol(s)
        :type hgnc_symbol: str or tuple(str) or None

        :param hgnc_identifier: identifiers(s) in :class:`.models.HGNC`
        :type hgnc_identifier: int or tuple(int) or None

        :param limit:
            - if `isinstance(limit,int)==True` -> limit
            - if `isinstance(limit,tuple)==True` -> format:= tuple(page_number, results_per_page)
            - if limit == None -> all results
        :type limit: int or tuple(int) or None

        :param bool as_df: if `True` results are returned as :class:`pandas.DataFrame`

        :return:
            - if `as_df == False` -> list(:class:`.models.MGD`)
            - if `as_df == True`  -> :class:`pandas.DataFrame`
        :rtype: list(:class:`.models.MGD`) or :class:`pandas.DataFrame`

        """
        q = self.session.query(models.MGD)

        model_queries_config = (
            (mgdid, models.MGD.mgdid),
        )
        q = self.get_model_queries(q, model_queries_config)

        many_to_many_queries_config = (
            (hgnc_symbol, models.MGD.hgncs, models.HGNC.symbol),
            (hgnc_identifier, models.MGD.hgncs, models.HGNC.identifier),
        )
        q = self.get_many_to_many_queries(q, many_to_many_queries_config)

        return self._limit_and_df(q, limit, as_df)

    def uniprot(self, uniprotid=None, hgnc_symbol=None, hgnc_identifier=None, limit=None, as_df=False):
        """Method to query :class:`.models.UniProt` objects in database

        :param uniprotid: UniProt identifier(s)
        :type uniprotid: str or tuple(str) or None

        :param hgnc_symbol: HGNC symbol(s)
        :type hgnc_symbol: str or tuple(str) or None

        :param hgnc_identifier: identifiers(s) in :class:`.models.HGNC`
        :type hgnc_identifier: int or tuple(int) or None

        :param limit:
            - if `isinstance(limit,int)==True` -> limit
            - if `isinstance(limit,tuple)==True` -> format:= tuple(page_number, results_per_page)
            - if limit == None -> all results
        :type limit: int or tuple(int) or None

        :param bool as_df: if `True` results are returned as :class:`pandas.DataFrame`

        :return:
            - if `as_df == False` -> list(:class:`.models.UniProt`)
            - if `as_df == True`  -> :class:`pandas.DataFrame`
        :rtype: list(:class:`.models.UniProt`) or :class:`pandas.DataFrame`

        """
        q = self.session.query(models.UniProt)

        model_queries_config = (
            (uniprotid, models.UniProt.uniprotid),
        )
        q = self.get_model_queries(q, model_queries_config)

        many_to_many_queries_config = (
            (hgnc_symbol, models.UniProt.hgncs, models.HGNC.symbol),
            (hgnc_identifier, models.UniProt.hgncs, models.HGNC.identifier),
        )
        q = self.get_many_to_many_queries(q, many_to_many_queries_config)

        return self._limit_and_df(q, limit, as_df)

    def ccds(self, ccdsid=None, hgnc_symbol=None, hgnc_identifier=None, limit=None, as_df=False):
        """Method to query :class:`.models.CCDS` objects in database

        :param ccdsid: Consensus CDS ID(s)
        :type ccdsid: str or tuple(str) or None

        :param hgnc_symbol: HGNC symbol(s)
        :type hgnc_symbol: str or tuple(str) or None

        :param hgnc_identifier: identifiers(s) in :class:`.models.HGNC`
        :type hgnc_identifier: int or tuple(int) or None

        :param limit:
            - if `isinstance(limit,int)==True` -> limit
            - if `isinstance(limit,tuple)==True` -> format:= tuple(page_number, results_per_page)
            - if limit == None -> all results
        :type limit: int or tuple(int) or None

        :param bool as_df: if `True` results are returned as :class:`pandas.DataFrame`

        :return:
            - if `as_df == False` -> list(:class:`.models.CCDS`)
            - if `as_df == True`  -> :class:`pandas.DataFrame`
        :rtype: list(:class:`.models.CCDS`) or :class:`pandas.DataFrame`

        """
        q = self.session.query(models.CCDS)

        model_queries_config = (
            (ccdsid, models.CCDS.ccdsid),
        )
        q = self.get_model_queries(q, model_queries_config)

        one_to_many_queries_config = (
            (hgnc_symbol, models.HGNC.symbol),
            (hgnc_identifier, models.HGNC.identifier)
        )
        q = self.get_one_to_many_queries(q, one_to_many_queries_config)

        return self._limit_and_df(q, limit, as_df)

    def pubmed(self, pubmedid=None, hgnc_symbol=None, hgnc_identifier=None, limit=None, as_df=False):
        """Method to query :class:`.models.PubMed` objects in database

        :param pubmedid: alias symbol(s)
        :type pubmedid: str or tuple(str) or None

        :param hgnc_symbol: HGNC symbol(s)
        :type hgnc_symbol: str or tuple(str) or None

        :param hgnc_identifier: identifiers(s) in :class:`.models.HGNC`
        :type hgnc_identifier: int or tuple(int) or None

        :param limit:
            - if `isinstance(limit,int)==True` -> limit
            - if `isinstance(limit,tuple)==True` -> format:= tuple(page_number, results_per_page)
            - if limit == None -> all results
        :type limit: int or tuple(int) or None

        :param bool as_df: if `True` results are returned as :class:`pandas.DataFrame`

        :return:
            - if `as_df == False` -> list(:class:`.models.PubMed`)
            - if `as_df == True`  -> :class:`pandas.DataFrame`
        :rtype: list(:class:`.models.PubMed`) or :class:`pandas.DataFrame`

        """
        q = self.session.query(models.PubMed)

        model_queries_config = (
            (pubmedid, models.PubMed.pubmedid),
        )
        q = self.get_model_queries(q, model_queries_config)

        many_to_many_queries_config = (
            (hgnc_symbol, models.PubMed.hgncs, models.HGNC.symbol),
            (hgnc_identifier, models.PubMed.hgncs, models.HGNC.identifier),
        )
        q = self.get_many_to_many_queries(q, many_to_many_queries_config)

        return self._limit_and_df(q, limit, as_df)

    def ena(self, enaid=None, hgnc_symbol=None, hgnc_identifier=None, limit=None, as_df=False):
        """Method to query :class:`.models.ENA` objects in database

        :param enaid: European Nucleotide Archive (ENA) identifier(s)
        :type enaid: str or tuple(str) or None

        :param hgnc_symbol: HGNC symbol(s)
        :type hgnc_symbol: str or tuple(str) or None

        :param hgnc_identifier: identifiers(s) in :class:`.models.HGNC`
        :type hgnc_identifier: int or tuple(int) or None

        :param limit:
            - if `isinstance(limit,int)==True` -> limit
            - if `isinstance(limit,tuple)==True` -> format:= tuple(page_number, results_per_page)
            - if limit == None -> all results
        :type limit: int or tuple(int) or None

        :param bool as_df: if `True` results are returned as :class:`pandas.DataFrame`

        :return:
            - if `as_df == False` -> list(:class:`.models.ENA`)
            - if `as_df == True`  -> :class:`pandas.DataFrame`
        :rtype: list(:class:`.models.ENA`) or :class:`pandas.DataFrame`

        """
        q = self.session.query(models.ENA)

        model_queries_config = (
            (enaid, models.ENA.enaid),
        )
        q = self.get_model_queries(q, model_queries_config)

        many_to_many_queries_config = (
            (hgnc_symbol, models.ENA.hgncs, models.HGNC.symbol),
            (hgnc_identifier, models.ENA.hgncs, models.HGNC.identifier),
        )
        q = self.get_many_to_many_queries(q, many_to_many_queries_config)

        return self._limit_and_df(q, limit, as_df)

    def enzyme(self, ec_number=None, hgnc_symbol=None, hgnc_identifier=None, limit=None, as_df=False):
        """Method to query :class:`.models.Enzyme` objects in database

        :param ec_number:Enzyme Commission number (EC number)(s)
        :type ec_number: str or tuple(str) or None

        :param hgnc_symbol: HGNC symbol(s)
        :type hgnc_symbol: str or tuple(str) or None

        :param hgnc_identifier: identifiers(s) in :class:`.models.HGNC`
        :type hgnc_identifier: int or tuple(int) or None

        :param limit:
            - if `isinstance(limit,int)==True` -> limit
            - if `isinstance(limit,tuple)==True` -> format:= tuple(page_number, results_per_page)
            - if limit == None -> all results
        :type limit: int or tuple(int) or None

        :param bool as_df: if `True` results are returned as :class:`pandas.DataFrame`

        :return:
            - if `as_df == False` -> list(:class:`.models.Enzyme`)
            - if `as_df == True`  -> :class:`pandas.DataFrame`
        :rtype: list(:class:`.models.Enzyme`) or :class:`pandas.DataFrame`

        """
        q = self.session.query(models.Enzyme)

        model_queries_config = (
            (ec_number, models.Enzyme.ec_number),
        )
        q = self.get_model_queries(q, model_queries_config)

        many_to_many_queries_config = (
            (hgnc_symbol, models.Enzyme.hgncs, models.HGNC.symbol),
            (hgnc_identifier, models.Enzyme.hgncs, models.HGNC.identifier),
        )
        q = self.get_many_to_many_queries(q, many_to_many_queries_config)

        return self._limit_and_df(q, limit, as_df)

    def lsdb(self, lsdb=None, url=None, hgnc_symbol=None, hgnc_identifier=None, limit=None, as_df=False):
        """Method to query :class:`.models.LSDB` objects in database

        :param lsdb: name(s) of the Locus Specific Mutation Database
        :type lsdb: str or tuple(str) or None

        :param url: URL of the Locus Specific Mutation Database
        :type url: str or tuple(str) or None

        :param hgnc_symbol: HGNC symbol(s)
        :type hgnc_symbol: str or tuple(str) or None

        :param hgnc_identifier: identifiers(s) in :class:`.models.HGNC`
        :type hgnc_identifier: int or tuple(int) or None

        :param limit:
            - if `isinstance(limit,int)==True` -> limit
            - if `isinstance(limit,tuple)==True` -> format:= tuple(page_number, results_per_page)
            - if limit == None -> all results
        :type limit: int or tuple(int) or None

        :param bool as_df: if `True` results are returned as :class:`pandas.DataFrame`

        :return:
            - if `as_df == False` -> list(:class:`.models.LSDB`)
            - if `as_df == True`  -> :class:`pandas.DataFrame`
        :rtype: list(:class:`.models.LSDB`) or :class:`pandas.DataFrame`

        """
        q = self.session.query(models.LSDB)

        model_queries_config = (
            (lsdb, models.LSDB.lsdb),
            (url, models.LSDB.url),
        )
        q = self.get_model_queries(q, model_queries_config)

        one_to_many_queries_config = (
            (hgnc_symbol, models.HGNC.symbol),
            (hgnc_identifier, models.HGNC.identifier)
        )
        q = self.get_one_to_many_queries(q, one_to_many_queries_config)

        return self._limit_and_df(q, limit, as_df)
