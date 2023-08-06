# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- ORM variant of the proxy
# :Created:   mer 03 feb 2016 11:09:01 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017 Lele Gaifax
#

import logging

from sqlalchemy import and_
from sqlalchemy.orm import ColumnProperty, class_mapper
from sqlalchemy.orm.query import Query

from .base import ProxiedBase
from .filters import apply_filters
from .utils import col_by_name


log = logging.getLogger(__name__)


class ProxiedEntity(ProxiedBase):
    """Specialize :py:class:`.base.ProxiedBase` to deal with SQLAlchemy ORM queries.

    An instance of this class wraps an *entity*, that is a SQLAlchemy
    mapped class. When called it builds a query, eventually applying
    filters specified by the arguments and returning the results set.
    """

    def __init__(self, entity, fields=None, metadata=None):
        """Initialize the proxy.

        :param entity: a SQLAlchemy mapped class, or an ORM query
        :param fields: a list of field names
        :param metadata: a dictionary

        When `fields` is not specified, it is automatically computed
        from the list of columns of the mapped table, extended with
        the properties defined on the entity itself.

        `metadata` is a dictionary, containing extra information
        about fields: when possibile, these info are collected from
        the SA definition (each field has a `info` dictionary); for
        computed fields when the returned value does not correspond to
        a physical field, or simply to override/expand such
        information on a per query basis, you may pass an additional
        dictionary of values, keyed on the field name.
        """

        super(ProxiedEntity, self).__init__()

        if isinstance(entity, Query):
            self.query = entity
            ez = entity._entity_zero()
            try:
                self.entity = ez.entity
            except AttributeError:
                # SA 1.0.x
                self.entity = ez.entity_zero.entity
        else:
            self.query = None
            self.entity = entity

        if fields is None:
            fields = [prop.key
                      for prop in class_mapper(self.entity).iterate_properties
                      if isinstance(prop, ColumnProperty)]
            fields.extend([a for a in dir(self.entity)
                           if (not a.startswith('_')
                               and isinstance(getattr(self.entity, a), property)
                               and a not in fields)])
        self.fields = fields
        self.metadata = metadata

    def filterQueryWithArgs(self, session, conditions, args):
        """Construct a filtered query on the wrapped entity.

        :param session: an SQLAlchemy ``Session``
        :param conditions: a list of SQLAlchemy expressions
        :param args: a dictionary
        :rtype: an ORM query

        The query gets then massaged by :py:func:`.filters.apply_filters()`, further
        filtered and modified as specified by the `args` dictionary.

        Return the altered query.
        """

        if self.query is None:
            query = session.query(self.entity)
        else:
            query = self.query
            query.session = session

        if conditions:
            if len(conditions)>1:
                query = query.filter(and_(*conditions))
            else:
                query = query.filter(conditions[0])

        query, self.only_cols = apply_filters(query, args)
        return query

    def getColumns(self, query):
        """Return the columns specified by `self.fields`."""

        stmt = query.statement
        oc = self.only_cols
        columns = []
        for n in self.fields:
            if oc is None or n in oc:
                col = col_by_name(stmt, n)
                if col is None:
                    col = n
                columns.append(col)
        return columns

    def getCount(self, session, query):
        """Execute a query to get the actual count of matching records."""

        return query.count()

    def getResult(self, session, query, asdict):
        """Execute the query in the given session, returning the result."""

        result = query.all()
        if asdict:
            oc = self.only_cols
            result = [dict((f, getattr(o, f))
                           for f in self.fields
                           if oc is None or f in oc)
                      for o in result]
        return result

    def getMetadata(self, query, countslot, resultslot, successslot):
        """Augment superclass implementation with primary key name."""

        result = super(ProxiedEntity, self).getMetadata(query,
                                                        countslot, resultslot,
                                                        successslot)

        pk = class_mapper(self.entity).primary_key
        if len(pk) == 1:
            result['primary_key'] = pk[0].name
        else:
            result['primary_key'] = tuple(c.name for c in pk)

        return result
