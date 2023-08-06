# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Async proxies
# :Created:   gio 09 lug 2015 15:05:19 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2015, 2016, 2017 Lele Gaifax
#

import asyncio
import logging

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import Selectable

from .core import ProxiedQuery
from .sorters import apply_sorters


log = logging.getLogger(__name__)


class AsyncProxiedQuery(ProxiedQuery):
    """An asyncio variant of the ``ProxiedQuery``."""

    def __init__(self, query, metadata=None, loop=None):
        super().__init__(query, metadata)
        self.loop = loop

    @asyncio.coroutine
    def getCount(self, session, query):
        "Async reimplementation of :meth:`ProxiedQuery.getCount`."

        pivot = next(query.inner_columns)
        simple = query.with_only_columns([pivot])
        tquery = select([func.count()], from_obj=simple.alias('cnt'))
        res = yield from session.execute(tquery, self.params)
        count = yield from res.scalar()
        return count

    @asyncio.coroutine
    def getResult(self, session, query, asdict):
        "Async reimplementation of :meth:`ProxiedQuery.getResult`."

        if isinstance(query, Selectable):
            res = yield from session.execute(query, self.params)
            rows = yield from res.fetchall()
            if asdict:
                fn2key = dict((c.name, c.key) for c in self.getColumns(query))
                result = [dict((fn2key[fn], r[fn]) for fn in fn2key) for r in rows]
            else:
                result = rows
        else:
            result = None
        return result

    @asyncio.coroutine
    def __call__(self, session, *conditions, **args):
        "Async reimplementation of superclass' ``__call__()``."

        (query, result, asdict,
         resultslot, successslot, messageslot, countslot, metadataslot,
         start, limit) = self.prepareQueryFromConditionsAndArgs(session, conditions, args)

        try:
            if limit != 0:
                if countslot:
                    count = yield from self.getCount(session, query)
                    result[countslot] = count

                if resultslot:
                    query = apply_sorters(query, args)
                    if start:
                        query = query.offset(start)
                    if limit:
                        query = query.limit(limit)
                    rows = yield from self.getResult(session, query, asdict)
                    result[resultslot] = rows

            if metadataslot:
                result[metadataslot] = self.getMetadata(query,
                                                        countslot,
                                                        resultslot,
                                                        successslot)

            result[successslot] = True
            result[messageslot] = 'Ok'
        except SQLAlchemyError as e: # pragma: nocover
            log.error("Error executing %s: %s", query, e)
            raise
        except: # pragma: nocover
            log.exception("Unhandled exception executing %s", query)
            raise

        if resultslot is True:
            return result[resultslot]
        else:
            return result
