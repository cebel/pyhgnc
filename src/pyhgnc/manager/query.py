# -*- coding: utf-8 -*-

from .database import BaseDbManager
from . import models
from sqlalchemy import distinct
from pandas import read_sql

class QueryManager(BaseDbManager):
    """Query interface to database."""

    def _limit_and_df(self, query, limit, as_df=False):
        """adds a limit (limit==None := no limit) to any query and allow a return as pandas.DataFrame

        :param bool as_df: if is set to True results return as pandas.DataFrame
        :param `sqlalchemy.orm.query.Query` query: SQL Alchemy query
        :param int limit: maximum number of results
        :return: query result of pyctd.manager.models.XY objects
        """
        if limit:
            query = query.limit(limit)

        if as_df:
            results = read_sql(query.statement, self.engine)
        else:
            results = query.all()

        return results


