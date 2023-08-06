# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Abstract base class
# :Created:   mer 03 feb 2016 11:03:22 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017, 2018 Lele Gaifax
#

from collections import Callable, Mapping
import logging

from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime, Integer, Interval,
                        Numeric, String, Text, Time)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.elements import BinaryExpression, TextClause

from .sorters import apply_sorters
from .types import get_metadata_for_sa_type


log = logging.getLogger(__name__)


class MetaInfo(Mapping):
    "Helper class, a dictionary where values can be callables"

    def __init__(self, name, info):
        self.name = name
        if isinstance(info, Callable):
            info = info(name)
        self.info = info

    def __getitem__(self, key):
        item = self.info.get(key)
        if isinstance(item, Callable):
            item = item(self.name, key)
        return item

    def __contains__(self, key):
        return key in self.info

    def __iter__(self):
        return iter(self.info)

    def __len__(self):
        return len(self.info)


class ProxiedBase(object):
    """Abstract base for the proxy thingie."""

    def translate(self, msg):
        "Stub implementation of l10n basic function, to be overridden."

        return msg

    def prepareQueryFromConditionsAndArgs(self, session, conditions, args):
        """Extract special meaning keyword arguments and return them, with a filtered query.

        :param session: an SQLAlchemy ``Session``
        :param conditions: a list of SQLAlchemy expressions
        :param args: a dictionary
        :rtype: a tuple of 12 values
        """

        start = args.pop('start', None)
        if start is not None:
            start = int(start)
        limit = args.pop('limit', None)
        if limit is not None:
            limit = int(limit)

        resultslot = args.pop('result', True)
        if resultslot in ('False', 'None', 'false', ''):
            resultslot = False
        elif resultslot in ('True', 'true'):
            resultslot = True

        slot = args.pop('success', 'success')
        if slot in (False, 'False', 'None', 'false', ''):
            successslot = False
        else:
            if slot in (True, 'True', 'true'):
                slot = 'success'
            successslot = resultslot is not True and slot

        slot = args.pop('message', 'message')
        if slot in (False, 'False', 'None', 'false', ''):
            messageslot = False
        else:
            if slot in (True, 'True', 'true'):
                slot = 'message'
            messageslot = resultslot is not True and slot

        slot = args.pop('count', None)
        if slot in (False, 'False', 'None', 'false', ''):
            countslot = False
        else:
            if slot in (True, 'True', 'true'):
                slot = 'count'
            countslot = resultslot is not True and slot

        slot = args.pop('metadata', None)
        if slot in (False, 'False', 'None', 'false', ''):
            metadataslot = False
        else:
            if slot in (True, 'True', 'true'):
                slot = 'metadata'
            metadataslot = resultslot is not True and slot

        asdict = args.pop('asdict', False)
        if asdict in ('False', 'None', 'false', ''):
            asdict = False

        result = {}
        if successslot:
            result[successslot] = False

        query = self.filterQueryWithArgs(session, conditions, args)

        return (query, result, asdict,
                resultslot, successslot, messageslot, countslot, metadataslot,
                start, limit)

    def __call__(self, session, *conditions, **args):
        """Apply filter conditions, execute the query and return results.

        :param session: an SQLAlchemy ``Session``
        :param conditions: a list of SQLAlchemy expressions
        :param args: a dictionary
        :rtype: depending on the arguments, either a dictionary, a list of tuples or a JSON
                string

        The first argument is the SQLAlchemy `session`, mandatory. All remaining arguments are
        eventually used to filter and change the query. Unused arguments remains accessible
        when the query is finally called.

        Some keyword arguments have special meaning:

        start
          This is the start of the interested range of records

        limit
          This is the maximum number of returned records

        result
          When ``False`` or ``None`` (or the strings ``"False"``, ``"None"`` and ``"false"``)
          means that no result set will be returned (reasonably either `metadata` or `count`
          are given); when ``True`` (or the strings ``"True"`` and ``"true"``), most of the
          other options are ignored and **only** the native Python results is returned;
          otherwise it's a string, the name of the *slot* of the returned dictionary containing
          the results set.

          ``True`` by default.

        success
          If `result` is not ``True``, this is a string used as the name of the slot containing
          execution status, that will be a boolean flag, ``True`` to indicate successfull
          execution, ``False`` otherwise.

          By default it's ``"success"``.

        message
          If `result` is not ``True``, this is a string used as the name of the slot containing
          execution message, that will either ``"Ok"`` when everything went good, otherwise a
          string with a possible reason of the failure.

          By default it's ``"message"``.

        count
          If `result` is not ``True``, this may be a string used as the name of the slot
          containing the total number of records that satisfy the conditions, ignoring the
          eventual range specified with `start` and `limit`. When ``False`` or ``None`` (the
          default) the count won't be computed.

        metadata
          If `result` is not ``True``, this may be the name of the slot containing a
          description of the result. See :meth:`getMetadata()` for details.

          ``None``, the default, disables the feature.

        asdict
          When you want to deal with plain Python dictionaries, one for each row, instead of
          the standard SQLAlchemy `resultset`, set this to ``True``. ``False`` by default.

        All these keywords are pulled (that is, removed) from the execution *context* of the
        query.
        """

        (query, result, asdict,
         resultslot, successslot, messageslot, countslot, metadataslot,
         start, limit) = self.prepareQueryFromConditionsAndArgs(session, conditions, args)

        try:
            if limit != 0:
                if countslot:
                    result[countslot] = self.getCount(session, query)

                if resultslot:
                    query = apply_sorters(query, args)
                    if start:
                        query = query.offset(start)
                    if limit:
                        query = query.limit(limit)
                    result[resultslot] = self.getResult(session, query, asdict)

            if metadataslot:
                result[metadataslot] = self.getMetadata(query,
                                                        countslot,
                                                        resultslot,
                                                        successslot)

            if successslot:
                result[successslot] = True

            if messageslot:
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

    def filterQueryWithArgs(self, session, conditions, args):
        """Apply filter conditions to the query.

        :param session: an SQLAlchemy ``Session``
        :param conditions: a list of SQLAlchemy expressions
        :param args: a dictionary
        :rtype: either a core SQL statement or an ORM query
        """

        raise NotImplemented('%s should reimplement this method',
                             self.__class__) # pragma: nocover

    def getColumns(self, query):
        """Return the columns of the given `query`."""

        raise NotImplemented('%s should reimplement this method',
                             self.__class__) # pragma: nocover

    def getCount(self, session, query):
        """Execute a query to get the actual count of matching records."""

        raise NotImplemented('%s should reimplement this method',
                             self.__class__) # pragma: nocover

    def getMetadata(self, query, countslot, resultslot, successslot):
        """Description of the result.

        :param query: an SQLAlchemy ``Query``
        :param countslot: a string or ``None``
        :param resultslot: a string or ``None``
        :param successslot: a string or ``None``
        :rtype: a dictionary

        For each selected field in the query, this method builds a dictionary containing the
        following keys:

        name
          the name of the field

        type
          the type of the field

        label
          the localized header for the field

        hint
          a longer description of the field, also localized

        length
          the size in characters, for String columns

        decimals
          the scale of the number, for Numeric columns

        These dictionaries are collected in a list, called ``fields``.

        The information about each field is extracted by two sources:

        1. `self.metadata`, a dictionary keyed on field names: each slot may be either a
           dictionary or a callable accepting the field name as parameter and returning the
           actual dictionary

        2. field column `info`, either a dictionary or a callable accepting the field name as
           parameter and returning the actual dictionary

        Also the value of any single slot in the information dictionary may be either a scalar
        value or a callable accepting two parameters, the name of the field and the name of the
        slot, returning the actual scalar information, for example:

        .. code-block:: python

          def birthdate_info(name):
              return {
                  'min': date(1980, 1, 1),
                  'max': lambda fname, iname: date.today()
              }

          persons = Table('persons', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('firstname', String,
                                 info=dict(label="First name",
                                           hint="The first name of the person")),
                          Column('lastname', String),
                          Column('birthdate', Date, info=birthdate_info),
                          Column('timestamp', DateTime),
                          Column('smart', Boolean, default=True),
                          Column('somevalue', Integer),
                          Column('title', Title),
                          Column('WeirdFN', String, key='goodfn'),
                          )

        The value coming from proxy's `metadata` takes precedence over the one from the
        column's `info`.

        Both dictionaries can contain any arbitrary extra slots that the caller may use for
        whatever reason.

        With the exception of `name`, everything can be overridden by `self.metadata`.

        Given the table above and the following proxy:

        .. code-block:: python

          pc = persons.c
          query = select([pc.id, pc.firstname, pc.lastname, pc.birthdate])
          meta = dict(lastname=dict(label='Last name',
                                    hint='Family name of the person',
                                    nullable=False))
          proxy = ProxiedQuery(query, meta)

        the call ``proxy(Session(), result=False, limit=0, metadata='meta')``
        returns something like::

          {
            'message': 'Ok',
            'meta': {
              'fields': [{
                  'align': 'right',
                  'hidden': True,
                  'hint': '',
                  'label': 'Id',
                  'name': 'id',
                  'nullable': False,
                  'readonly': True,
                  'type': 'integer'
                }, {
                  'hint': 'The first name of the person',
                  'label': 'First name',
                  'length': 10,
                  'name': 'firstname',
                  'nullable': True,
                  'type': 'string'
                }, {
                  'hint': 'Family name of the person',
                  'label': 'Last name',
                  'length': 10,
                  'name': 'lastname',
                  'nullable': False,
                  'type': 'string'
                }, {
                  'hint': '',
                  'label': 'Birthdate',
                  'max': datetime.date(2017, 1, 11),
                  'min': datetime.date(1980, 1, 1),
                  'name': 'birthdate',
                  'nullable': True,
                  'type': 'date'
                }, {
                  'hint': '',
                  'label': 'Smart',
                  'name': 'smart',
                  'default': True,
                  'type': 'boolean'
                } ...
              ],
              'primary_key': 'id',
              'success_slot': 'success'
            },
            'success': True
          }
        """

        fields = []

        t = self.translate

        for c in self.getColumns(query):
            meta = dict()
            cinfo = None
            if isinstance(c, str):
                name = c
                ctype = str
            elif isinstance(c, TextClause):
                name = c.text
                ctype = str
            else:
                if isinstance(c, BinaryExpression):
                    if isinstance(c.left, Column):
                        # e.g. jsonfield['foo']
                        c = c.left
                    elif isinstance(c.right, Column):
                        c = c.right
                    else:
                        raise NotImplementedError("Don't know how to deal with %r,"
                                                  " left=%r and right=%r"
                                                  % (c, c.left, c.right))
                name = c.name
                ctype = c.type
                if not isinstance(ctype, Interval):
                    # Surprisingly, SA Interval impl is a DateTime...
                    try:
                        ctype = ctype.impl
                    except AttributeError:
                        pass
                cinfo = getattr(c, 'info', None)
                if cinfo:
                    cinfo = MetaInfo(name, cinfo)
                elif isinstance(c, Column):
                    # Maybe it's been aliased?
                    origt = getattr(c.table, 'original', None)
                    if origt is not None:
                        origc = origt.c[c.key]
                        cinfo = getattr(origc, 'info', None)
                        if cinfo:
                            cinfo = MetaInfo(name, cinfo)
                else:
                    # Or a labelled column?
                    base_cols = getattr(c, 'base_columns', None)
                    if base_cols is not None:
                        for bc in base_cols:
                            cinfo = getattr(bc, 'info', None)
                            if cinfo:
                                cinfo = MetaInfo(name, cinfo)
                                break

            fmeta = self.metadata and self.metadata.get(name)

            # An explicit ``False`` means skip the field completely
            if fmeta is False:
                continue

            if fmeta is not None:
                fmeta = MetaInfo(name, fmeta)

            meta.update(get_metadata_for_sa_type(ctype))

            if isinstance(ctype, Numeric):
                try:
                    meta['decimals'] = ctype.scale
                except AttributeError: # pragma: no cover
                    pass
            elif isinstance(ctype, String):
                flen = ctype.length
                meta['length'] = flen or 1

            fks = getattr(c, 'foreign_keys', False)
            if getattr(c, 'primary_key', False) or fks:
                meta['hidden'] = True
                meta['readonly'] = True

            if fks:
                meta['foreign_keys'] = tuple(fk.target_fullname for fk in fks)

            meta['nullable'] = getattr(c, 'nullable', False)

            label = fmeta and fmeta.get('label')
            if not label:
                label = cinfo and cinfo.get('label')
            if not label:
                label = name.capitalize()
            else:
                label = t(label)

            hint = fmeta and fmeta.get('hint')
            if not hint:
                hint = cinfo and cinfo.get('hint')
            if not hint:
                hint = ''
            else:
                hint = t(hint)

            # Take info at SA table definition as defaults
            if cinfo is not None:
                meta.update(cinfo)

            # Possibly overridable by metadata
            if fmeta is not None:
                meta.update(fmeta)

            # Override localized strings
            meta['label'] = label
            meta['hint'] = hint
            if 'dictionary' in meta:
                if isinstance(meta['dictionary'], Mapping):
                    meta['dictionary'] = {
                        k: t(v) for k, v in meta['dictionary'].items()}
                else:
                    meta['dictionary'] = [
                        [k, t(v)] for k, v in meta['dictionary']]

            if 'default' not in meta and getattr(c, 'default', None) is not None:
                default = c.default
                if not default.is_clause_element:
                    if default.is_callable:
                        meta['default'] = c.default.arg(None)
                    else:
                        meta['default'] = c.default.arg

            # Do this last, so it cannot be overridden
            meta['name'] = name

            fields.append(meta)

        result = dict(fields=fields)
        if countslot:
            result['count_slot'] = countslot
        if resultslot:
            result['root_slot'] = resultslot
        if successslot:
            result['success_slot'] = successslot

        return result

    def getResult(self, session, query, asdict):
        """Execute the query in the given session, returning the result.

        :param session: an SQLAlchemy ``Session``
        :param query: an SQLAlchemy ``Query``
        :param asdict: a boolean

        If `asdict` is ``False`` then this should return either a `ResultProxy`__ (for SQL
        selects) or a list of entities (when the query is at the ORM level), otherwise they
        should be translated into a list of dictionaries.

        __ http://docs.sqlalchemy.org/en/latest/core/connections.html\
           #sqlalchemy.engine.ResultProxy
        """

        raise NotImplemented('%s should reimplement this method',
                             self.__class__) # pragma: nocover
