# -*- coding: utf-8 -*-

from .database import BaseDbManager
from collections import Iterable
from pandas import read_sql
from . import models

# from sqlalchemy import distinct


class QueryManager(BaseDbManager):
    """Query interface to database."""

    def _limit_and_df(self, query, limit, as_df=False):
        """adds a limit (limit==None := no limit) to any query and allow a return as pandas.DataFrame

        :param bool as_df: if is set to True results return as pandas.DataFrame
        :param `sqlalchemy.orm.query.Query` query: SQL Alchemy query
        :param int,tuple limit: maximum number of results
        :return: query result of pyctd.manager.models.XY objects
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
            results = query.all()

        return results

    def get_model_queries(self, query_obj, model_queries_config):
        for search4, model_attrib in model_queries_config:

            if search4 is not None:
                query_obj = self._model_query(query_obj, search4, model_attrib)
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

        if isinstance(search4, str):
            query_obj = query_obj.join(model).filter(model_attrib.like(search4))

        elif isinstance(search4, int):
            query_obj = query_obj.join(model).filter(model_attrib == search4)

        elif isinstance(search4, Iterable):
            query_obj = query_obj.join(model).filter(model_attrib.in_(search4))

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

    def hgnc(self, name=None, symbol=None, identifier=None, status=None, uuid=None, locus_group=None,
             locus_type=None, date_name_changed=None, date_modified=None, date_symbol_changed=None,
             date_approved_reserved=None, ensembl_gene=None, horde=None, vega=None, lncrnadb=None,
             entrez=None, mirbase=None, iuphar=None, ucsc=None, snornabase=None, intermediatefilamentdb=None,
             pseudogeneorg=None, bioparadigmsslc=None, locationsortable=None,
             merop=None, location=None, cosmic=None, imgt=None, limit=None, as_df=False):
        """Method to query :class:`pyhgnc.manager.models.Pmid`


        :param str name:
        :param str symbol:
        :param int identifier:
        :param str status:
        :param str uuid:
        :param str locus_group:
        :param str locus_type:
        :param date date_name_changed:
        :param date date_modified:
        :param date date_symbol_changed:
        :param date date_approved_reserved:
        :param str ensembl_gene:
        :param str horde:
        :param str vega:
        :param str lncrnadb:
        :param str entrez:
        :param str mirbase:
        :param str iuphar:
        :param str ucsc:
        :param str snornabase:
        :param str intermediatefilamentdb:
        :param str pseudogeneorg:
        :param str bioparadigmsslc:
        :param str locationsortable:
        :param str merop:
        :param str location:
        :param str cosmic:
        :param str imgt:
        :param int,tuple limit: number of results, if limit=`None`, all results returned
        :param bool as_df: if `True` results are returned as :class:`pandas.DataFrame`
        :return: list of :class:`pyuniprot.manager.models.Keyword` objects or :class:`pandas.DataFrame`
        """
        q = self.session.query(models.HGNC)

        model_queries_config = (
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
            (intermediatefilamentdb, models.HGNC.intermediatefilamentdb),
            (pseudogeneorg, models.HGNC.pseudogeneorg),
            (bioparadigmsslc, models.HGNC.bioparadigmsslc),
            (locationsortable, models.HGNC.locationsortable),
            (merop, models.HGNC.merop),
            (location, models.HGNC.location),
            (cosmic, models.HGNC.cosmic),
            (imgt, models.HGNC.imgt),
        )
        q = self.get_model_queries(q, model_queries_config)

        many_to_many_queries_config = (
            (pmid, models.Entry.pmids, models.Pmid.pmid),
            (keyword, models.Entry.keywords, models.Keyword.name),
            (subcellular_location, models.Entry.subcellular_locations, models.SubcellularLocation.location),
            (tissue_in_reference, models.Entry.tissue_in_references, models.TissueInReference.tissue)
        )
        q = self.get_many_to_many_queries(q, many_to_many_queries_config)

        return self._limit_and_df(q, limit, as_df)

