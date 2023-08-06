# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Filters details
# :Created:   sab 11 feb 2017 11:05:49 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2017 Lele Gaifax
#

from collections import Mapping, Sequence, namedtuple
from enum import Enum
import logging

from sqlalchemy import String, and_, not_, or_
from sqlalchemy.orm.query import Query

from .json import JSON
from .types import get_adaptor_for_sa_type
from .utils import col_by_name, csv_to_list, get_column_type


log = logging.getLogger(__name__)


def _op_between(c, t, v, a):
    if isinstance(v, Sequence) and not isinstance(v, str) and len(v) == 2:
        start, end = v
    elif isinstance(v, Mapping) and ('start' in v or 'end' in v):
        start = v.get('start', None)
        end = v.get('end', None)
    elif isinstance(v, str) and '><' in v:
        # Should never happen, but just in case...
        start, end = v.split('><')
    else:
        raise ValueError('Bad value for BETWEEN operator: %r' % (v,))

    if start is not None and end is not None:
        return c.between(a(start), a(end))
    elif start is not None:
        return c >= a(start)
    elif end is not None:
        return c <= a(end)
    else:
        raise ValueError('Range ends cannot be both None')


def _op_in(c, values):
    if None in values:
        values = list(filter(None, values))
        if len(values) > 1:
            return or_(c == None, c.in_(values))
        else:
            return or_(c == None, c == values[0])
    else:
        if len(values) > 1:
            return c.in_(values)
        else:
            return c == values[0]


def _op_not_equal(c, t, v, a):
    if isinstance(v, str) and not isinstance(t, String) and ',' in v:
        v = v.split(',')
    if isinstance(v, Sequence) and not isinstance(v, str):
        return not_(_op_in(c, [a(value) for value in v]))
    else:
        return c != a(v)


def _op_equal(c, t, v, a):
    if isinstance(v, str) and not isinstance(t, String) and ',' in v:
        v = v.split(',')
    if isinstance(v, Sequence) and not isinstance(v, str):
        return _op_in(c, [a(value) for value in v])
    else:
        return c == a(v)


def _op_startswith(c, t, v, a):
    if isinstance(t, String):
        if v:
            v = a(v).replace('%', '\\%')
        return c.ilike(v + '%')
    return c.startswith(a(v))


def _op_contains(c, t, v, a):
    if isinstance(t, String):
        if v:
            v = a(v).replace('%', '\\%')
        return c.ilike('%' + v + '%')
    return c.contains(a(v))


class Operator(Enum):
    "Some kind of comparison operator between a field and a value."

    # NB: shorter operators MUST come last!

    BETWEEN = ('><', _op_between)
    """The field value must be within a given *range* of values.

    The *range* may be a tuple of two values, a dictionary with either a ``start`` or ``end``
    key or both.
    """

    GREATER_OR_EQUAL = ('>=', lambda c, t, v, a: c >= a(v))
    "The field value must be equal or greater than the specified value."

    LESSER_OR_EQUAL = ('<=', lambda c, t, v, a: c <= a(v))
    "The field value must be equal or less than the specified value."

    NOT_EQUAL = ('<>', _op_not_equal)
    "The field value must be different than the specified value."

    STARTSWITH = ('~=', _op_startswith)
    """The field value must start with the given value.

    For string columns it uses `ilike()`__ with a pattern ``value%``, otherwise
    it uses `startswith()`__ and the exact semantic is determined by the data type.

    __ http://docs.sqlalchemy.org/en/rel_1_1/core/metadata.html#sqlalchemy.schema.Column.ilike
    __ http://docs.sqlalchemy.org/en/rel_1_1/core/metadata.html#sqlalchemy.schema.Column.startswith
    """

    CONTAINS = ('~', _op_contains)
    """The field value must contain the given value.

    For string columns it uses `ilike()`__ with a pattern ``%value%``, otherwise
    it uses `contains()`__ and the exact semantic is determined by the data type.

    __ http://docs.sqlalchemy.org/en/rel_1_1/core/metadata.html#sqlalchemy.schema.Column.ilike
    __ http://docs.sqlalchemy.org/en/rel_1_1/core/metadata.html#sqlalchemy.schema.Column.contains
    """

    EQUAL = ('=', _op_equal)
    "The field value must match the given value."

    GREATER = ('>', lambda c, t, v, a: c > a(v))
    "The field value must be greater than the specified value."

    LESSER = ('<', lambda c, t, v, a: c < a(v))
    "The field value must be less than the specified value."

    @classmethod
    def make(cls, operator):
        """Helper to create a new instance.

        The `operator` argument may be either an instance of the class, the name of one of its
        members (like ``"BETWEEN"``) or the symbolic operator (like ``"><"``).
        """

        if isinstance(operator, cls):
            return operator

        try:
            return cls[operator]
        except KeyError:
            for o in cls:
                if o.value[0] == operator:
                    return o

        raise ValueError('Unrecognized filter operator: %r' % operator)

    def __init__(self, operator, filter_factory):
        self.operator = operator
        self.filter_factory = filter_factory

    def __repr__(self):
        return "<%s.%s>" % (self.__class__.__name__, self._name_)

    def filter(self, column, value):
        "Return a filter expression that compares `column` with `value`."

        ctype = get_column_type(column)
        adaptor = get_adaptor_for_sa_type(ctype)
        return self.filter_factory(column, ctype, value, adaptor)


def split_operator_and_value(value, default_operator=Operator.EQUAL):
    """Given a string `value`, recognize possible prefix comparison operator.

    If `value` is a string that starts with a known operator, split the value returning a tuple
    like ``(Operator.XXX, remaining-value)``; if it contains the ``><`` operator, return
    ``(Operator.BETWEEN, (start, end))``; otherwise return ``(Operator.EQUAL, value)``.
    """

    if isinstance(value, str):
        for op in Operator:
            if value.startswith(op.operator):
                return op, value[len(op.operator):]

        if '><' in value:
            return Operator.BETWEEN, tuple(value.split('><', 1))

    return default_operator, value


class Filter(namedtuple('Filter', 'property, value, operator')):
    "Represent a single filter condition."

    @classmethod
    def make(cls, property, value, operator=Operator.EQUAL):
        """Helper to create a new instance.

        The `operator` gets coerced to an :class:`Operator` instance using its
        :meth:`Operator.make` class method.
        """

        return cls(property, value, Operator.make(operator))

    def filter(self, statement):
        column = col_by_name(statement, self.property)
        if column is not None:
            try:
                return self.operator.filter(column, self.value)
            except Exception as e: # pragma: no cover
                log.error('Error filtering on condition %r', self)
                raise


def extract_filters(args):
    """Extract filter conditions.

    :param args: a dictionary, usually request.params
    :rtype: a list of :class:`Filter` instances

    Recognize three possible syntaxes specifying filtering conditions:

    1. the “old” way: ``?filter_col=fieldname&filter_value=1``

    2. the “new” way: a ``filter`` or ``filters`` argument with a (possibly JSON encoded) array
       of dictionaries, each containing a ``property`` slot with the field name as value, an
       ``operator`` slot and a ``value`` slot

    3. a custom syntax: ``?filter_by_fieldname=1``

    The different syntaxes may be specified together, and they will be applied in the order
    above.

    .. note:: the `args` parameter is **modified** in place!
    """

    missing = object()

    result = []

    # Old syntax:
    # ?filter_col=fieldname&filter_value=1

    fcol = args.pop('filter_col', missing)
    fvalue = args.pop('filter_value', missing)

    if fcol is not missing and fvalue is not missing:
        operator, value = split_operator_and_value(fvalue)
        result.append(Filter(fcol, value, operator))

    # New syntax:
    # filter=[{"property": "fieldname", "operator": "=", "value": "1"},...]

    # Recognize both "filter" and "filters": the former is the standard ExtJS 4
    # `filterParam` setting, the latter is the old name; handling both allows
    # the trick of dinamically augmenting the static conditions written in the URL

    filters = []

    for fpropname in ('filter', 'filters'):
        filter = args.pop(fpropname, missing)
        if filter is not missing:
            if isinstance(filter, str):
                filter = JSON.decode(filter)
            filters.extend(filter)

    for f in filters:
        if isinstance(f, Filter):
            result.append(f)
        else:
            fcol = f.get('property', missing)
            if fcol is missing:
                continue

            fvalue = f.get('value', missing)
            if fvalue is missing:
                continue
            else:
                ilop, fvalue = split_operator_and_value(fvalue, Operator.CONTAINS)

            operator = f.get('operator', ilop)

            result.append(Filter.make(fcol, fvalue, operator))

    # Yet another syntax:
    # ?filter_by_fieldname=1

    # This is needed as we are going to change the dictionary
    fnames = list(args.keys())
    for f in fnames:
        if f.startswith('filter_by_'):
            fcol = f[10:]
            if not fcol:
                continue
            fvalue = args.pop(f, missing)
            if fvalue is not missing:
                result.append(Filter(fcol, fvalue, Operator.EQUAL))

    return result


def apply_filters(query, args):
    """Filter a given query.

    :param query: an SQLAlchemy ``Query``
    :param args: a dictionary
    :rtype: a tuple

    `query` may be either a SQL statement (not necessarily a ``SELECT``) or an ORM query.

    The `args` dictionary may contain some special keys, that will be used to build a filter
    expression, or to change the query in particular ways.

    .. important:: All these keys will be *consumed*, that is removed from the `args`
                   dictionary.

    filter_col
      the name of the field going to be filtered

    filter_value
      value of the filter

    filter_by_name-of-the-field
      specify both the `name-of-the-field` and the value to apply

    filter (or filters)
      a sequence of filter specifications, or a JSON string containing a list of dictionaries:
      each dictionary must contain a ``property`` and a ``value`` slots and an optional
      ``operator`` which is prepended to the given value, if it already does not when specified

    only_cols
      filter the selected columns of the query, using only fields specified with this argument,
      assumed to be a comma separated list of field names

    query
      this is used combined with `fields`: if present, its value will be searched in the
      specified fields, within an ``OR`` expression

    fields
      this is a list of field names that selects which fields will be compared to the `query`
      value

    The function :py:func:`extract_filters()` is used to build the filter expression.

    Returns a tuple with the modified query in the first slot, and another which is either
    ``None`` or the list of columns specified by `only_cols`.
    """

    if isinstance(query, Query):
        stmt = query.statement
    else:
        stmt = query

    filters = []
    for filter in extract_filters(args):
        filter = filter.filter(stmt)
        if filter is not None:
            filters.append(filter)

    if filters:
        if len(filters)>1:
            expr = and_(*filters)
        else:
            expr = filters[0]
        if isinstance(query, Query):
            query = query.filter(expr)
        else:
            query = query.where(expr)

    only_cols = args.pop('only_cols', None)

    qvalue = args.pop('query', None)
    qfields = args.pop('fields', only_cols)

    if qvalue:
        operator, value = split_operator_and_value(qvalue, Operator.CONTAINS)

        if qfields is None:
            columns = [c for c in stmt.inner_columns
                       if isinstance(get_column_type(c), String)]
        elif isinstance(qfields, str):
            columns = []
            for f in csv_to_list(qfields):
                column = col_by_name(stmt, f)
                if column is not None:
                    columns.append(column)
                else:
                    log.warning('Ignoring query filter on non-existing column %r', f)

        conds = []
        for column in columns:
            conds.append(operator.filter(column, value))

        if conds:
            if len(conds)>1:
                cond = or_(*conds)
            else:
                cond = conds[0]
            if isinstance(query, Query):
                query = query.filter(cond)
            else:
                query = query.where(cond)

    if only_cols:
        if isinstance(only_cols, str):
            only_cols = csv_to_list(only_cols)
        if not isinstance(query, Query):
            cols = [col for col in [col_by_name(query, c) for c in only_cols]
                    if col is not None]
            if not cols:
                raise ValueError("No valid column in only_cols='%s'" % only_cols)
            query = query.with_only_columns(cols)

    return query, only_cols
