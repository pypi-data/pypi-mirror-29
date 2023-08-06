# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Sorting capability
# :Created:   dom 12 feb 2017 12:50:56 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2017 Lele Gaifax
#

from collections import Mapping, Sequence, namedtuple
from enum import Enum
import logging

from sqlalchemy.orm.query import Query

from .json import JSON
from .utils import col_by_name, csv_to_list


log = logging.getLogger(__name__)


class Direction(Enum):
    "Sort direction."

    ASC = '<'
    "Ascending order."

    DESC = '>'
    "Descending order."

    @classmethod
    def make(cls, direction):
        """Helper function to create a new instance.

        The `direction` argument may be either an instance of the class, the name on one of its
        members (like ``"DESC"``) or the symbolic form (like ``">"``).
        """

        if isinstance(direction, cls):
            return direction
        else:
            try:
                return cls[direction]
            except KeyError:
                for d in cls:
                    if d.value == direction:
                        return d

        raise ValueError('Unrecognized sort direction: %r' % direction)

    def __repr__(self):
        return "<%s.%s>" % (self.__class__.__name__, self._name_)


class Sorter(namedtuple('Sorter', 'property, direction')):
    "Represent a single field ordering specification."

    @classmethod
    def make(cls, property, direction=Direction.ASC):
        """Helper to create a new instance.

        The `direction` argument defaults to :data:`Direction.ASC` and gets coerced to a
        :class:`Direction` instance using its :meth:`Direction.make` class method.
        """

        return cls(property, Direction.make(direction))


def extract_sorters(args):
    """Extract sort specification.

    :param args: a dictionary
    :rtype: a list of :class:`Sorter` instances

    Recognize different kinds of specification:

    1. the “old” way: ``?sort_col=fieldname`` or
       ``?sort_col=fieldname&sort_dir=DESC``; `sort_col` may also be a comma-separated-list
       of field names

    2. the “new” way: the ``sorters`` argument is a (possibly JSON encoded) list
       of dictionaries, each containing a ``property`` slot and a ``direction`` slot,
       respectively the field name and the ordering direction

    3. a custom syntax: ``?sort_by_fieldname=DESC``

    The different syntaxes may be specified together, and they will be applied in the order
    above.

    .. note:: the `args` parameter is **modified** in place!
    """

    missing = object()

    sorters = []

    # Old syntax:
    # ?sort_col=fieldname&sort_dir=ASC

    sort_col = args.pop('sort_col', missing)
    sort_dir = Direction.make(args.pop('sort_dir', 'ASC'))

    if sort_col is not missing:
        if isinstance(sort_col, str):
            sorters.extend(Sorter(col, sort_dir) for col in csv_to_list(sort_col))
        elif isinstance(sort_col, Sequence):
            for col in sort_col:
                if not isinstance(col, str):
                    raise ValueError('Unrecognized sort specification: %r' % sort_col)
                sorters.append(Sorter(col, sort_dir))
        else:
            raise ValueError('Unrecognized sort specification: %r' % sort_col)

    # New syntax:
    # sorters=[{"property": "fieldname", "direction": "ASC"}]

    specs = args.pop('sorters', missing)
    if specs is not missing:
        if isinstance(specs, str):
            try:
                specs = JSON.decode(specs)
            except:
                raise ValueError('Invalid JSON encoded sort specification: %r' % specs)
        if not isinstance(specs, Sequence) or isinstance(specs, Sorter):
            specs = [specs]
        for s in specs:
            if isinstance(s, Sorter):
                sorters.append(s)
            elif isinstance(s, str):
                sorters.extend(Sorter(f, Direction.ASC) for f in csv_to_list(s))
            elif isinstance(s, Sequence) and len(s) == 2:
                sorters.append(Sorter(s[0], Direction.make(s[1])))
            elif isinstance(s, Mapping) and 'property' in s:
                sorters.append(Sorter(s['property'],
                                      Direction.make(s.get('direction', Direction.ASC))))
            else:
                raise ValueError('Unrecognized sort specification: %r' % s)

    # Custom syntax

    # This is needed as we are going to change the dictionary
    fnames = list(args.keys())
    for f in fnames:
        if f.startswith('sort_by_'):
            fcol = f[8:]
            if not fcol:
                continue
            fvalue = args.pop(f, missing)
            if fvalue is not missing:
                sorters.append(Sorter(fcol, Direction.make(fvalue)))

    return sorters


def apply_sorters(query, args):
    """Order a given query.

    :param query: an SQLAlchemy ``Query``
    :param args: a dictionary
    :rtype: an SQLAlchemy ``Query``

    `query` may be either a SQL statement or an ORM query.

    The `args` dictionary may contain some special keys, that will be used to build an set of
    ordering specifications.

    .. important:: All these keys will be *consumed*, that is removed from the `args`
                   dictionary.

    sort_col
      the name of the field to sort the result by: it may be a single name or a
      comma-separated-list of column names

    sort_dir
      when `sort_col` is specified, the direction to sort with: it may be either ``"ASC"``, the
      default, or ``"DESC"`` to specify a *DESC*\ ending order

    sort_by_name-of-the-field
      specify both the `name-of-the-field` and the sorting direction

    sorters
      either a single or a list of sort specifications (possibly as a JSON encoded string):
      each one may be either

      * a :class:`Sorter` instance
      * a plain string, the name of a field
      * a comma-separated-list of field names
      * a sequence of two values, respectively the field name and the sort direction
      * a mapping with a slot ``property`` and an optional ``direction`` slot

    The function :func:`extract_sorters()` is used to extract the specifications.
    """

    if isinstance(query, Query):
        stmt = query.statement
    else:
        stmt = query

    for sorter in extract_sorters(args):
        col = col_by_name(stmt, sorter.property)
        if col is not None:
            if sorter.direction is Direction.DESC:
                col = col.desc()
            query = query.order_by(col)
        else:
            log.warning('Requested sort by %r, which does not exist in %s',
                        sorter.property, query)

    return query
