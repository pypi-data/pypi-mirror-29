# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Tests for filter functions
# :Created:   mer 03 feb 2016 11:23:52 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017 Lele Gaifax
#

from __future__ import absolute_import

import pytest

from metapensiero.sqlalchemy.proxy.filters import (
    Filter,
    Operator,
    extract_filters,
    split_operator_and_value,
    )
from fixture import persons


@pytest.mark.parametrize('value,expected', [
    ( 'foo', (Operator.EQUAL, 'foo') ),
    ( '<>foo', (Operator.NOT_EQUAL, 'foo') ),
    ( '=foo', (Operator.EQUAL, 'foo') ),
    ( '~foo', (Operator.CONTAINS, 'foo') ),
    ( '~=foo', (Operator.STARTSWITH, 'foo') ),
    ( '>foo', (Operator.GREATER, 'foo') ),
    ( '>=foo', (Operator.GREATER_OR_EQUAL, 'foo') ),
    ( '<foo', (Operator.LESSER, 'foo') ),
    ( '<=foo', (Operator.LESSER_OR_EQUAL, 'foo') ),
    ( 'foo><bar', (Operator.BETWEEN, ('foo', 'bar')) ),
])
def test_split_operator_and_value(value, expected):
    assert split_operator_and_value(value) == expected


@pytest.mark.parametrize('args,expected', [
    ( dict(filter_col='foo', filter_value='bar'),
      [('foo', 'bar', Operator.EQUAL)] ),
    ( dict(filter_col='foo', filter_value='<>bar'),
      [('foo', 'bar', Operator.NOT_EQUAL)] ),
    ( dict(filter_col='foo', filter_value='start><stop'),
      [('foo', ('start', 'stop'), Operator.BETWEEN)] ),
    ( dict(filter_col='foo'), [] ),
    ( dict(filter=[dict(property='foo', value='bar', operator='<')]),
      [('foo', 'bar', Operator.LESSER)] ),
    ( dict(filters=[dict(property='foo', value='bar', operator='<=')]),
      [('foo', 'bar', Operator.LESSER_OR_EQUAL)] ),
    ( dict(filter=[dict(property='foo', value=1, operator='<')]),
      [('foo', 1, Operator.LESSER)] ),
    ( dict(filter=[dict(property='foo', operator='<')]), [] ),
    ( dict(filter='[{"property": "foo", "value": "bar", "operator": "<"}]'),
      [('foo', 'bar', Operator.LESSER)] ),
    ( dict(filter_by_='bar'), [] ),
    ( dict(filter_by_foo='bar'),
      [('foo', 'bar', Operator.EQUAL)] ),
    ( dict(filter=[dict(property='foo', value='bar')]),
      [('foo', 'bar', Operator.CONTAINS)] ),
    ( dict(filters=[dict(property='foo', value="=bar")]),
      [('foo', 'bar', Operator.EQUAL)] ),
    ( dict(filter=[dict(property='foo', value='bar', operator=Operator.NOT_EQUAL)]),
      [('foo', 'bar', Operator.NOT_EQUAL)] ),
    ( dict(filter=[Filter('foo', 'bar', Operator.LESSER)]),
      [('foo', 'bar', Operator.LESSER)] ),
])
def test_extract_filters(args, expected):
    assert extract_filters(args) == expected


@pytest.mark.parametrize('args', [
    dict(filter=[dict(property='foo', value='bar', operator='???')]),
])
def test_bad_filters(args):
    with pytest.raises(ValueError):
        extract_filters(args)


@pytest.mark.parametrize('column,args', [
    ( persons.c.firstname,
      dict(filter=[dict(property='foo', value=('bar','car','zar'), operator='><')]) ),
    ( persons.c.firstname,
      dict(filter=[dict(property='foo', value=(None, None), operator='><')]) ),
    ( persons.c.firstname,
      dict(filter_col='firstname', filter_value='><car') ),
])
def test_bad_filter_values(column, args):
    conds = extract_filters(args)
    assert len(conds) == 1
    cond = conds[0]
    with pytest.raises(ValueError):
        cond.operator.filter(column, cond.value)


@pytest.mark.parametrize('column,args,expected_snippet', [
    ( persons.c.firstname,
      dict(filter_col='firstname', filter_value='bar'),
      'firstname = ' ),
    ( persons.c.firstname,
      dict(filter_col='firstname', filter_value='bar><car'),
      'firstname BETWEEN ' ),
    ( persons.c.firstname,
      dict(filter_col='firstname', filter_value=None),
      'firstname IS NULL' ),
    ( persons.c.firstname,
      dict(filter_col='firstname', filter_value="NULL"),
      'firstname IS NULL' ),
    ( persons.c.firstname,
      dict(filter_col='firstname', filter_value="<>NULL"),
      'firstname IS NOT NULL' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value='bar><car', operator='><')]),
      'firstname BETWEEN ' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value=('bar','car'), operator='><')]),
      'firstname BETWEEN ' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value=dict(start='bar', end='car'),
                        operator='><')]),
      'firstname BETWEEN ' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value=dict(start='bar'),
                        operator='><')]),
      'firstname >= ' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value=dict(start='bar', end=None),
                        operator='><')]),
      'firstname >= ' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value=dict(end='car'),
                        operator='><')]),
      'firstname <= ' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value=dict(start=None, end='car'),
                        operator='><')]),
      'firstname <= ' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value='bar', operator='>=')]),
      'firstname >= ' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value='bar', operator='<=')]),
      'firstname <= ' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value='bar', operator='~=')]),
      'LIKE ' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value='bar', operator='<>')]),
      'firstname != ' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value='foo,bar', operator='<>')]),
      'firstname != ' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value=1, operator='<>')]),
      'id != ' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value='1', operator='<>')]),
      'id != ' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value='1,2,3', operator='<>')]),
      'id NOT IN (' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value=(1,2,3), operator='<>')]),
      'id NOT IN (' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value=(1,2,3,None), operator='<>')]),
      'id IS NULL OR ' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value=(1,None), operator='<>')]),
      'id IS NULL OR ' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value=(1,None), operator='<>')]),
      'id = ' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value='1,2,3,NULL', operator='<>')]),
      'id IS NULL OR ' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value='bar', operator='~')]),
      'LIKE ' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value='bar', operator='=')]),
      'firstname = ' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value='foo,bar', operator='=')]),
      'firstname = ' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value=1, operator='=')]),
      'id = ' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value='1', operator='=')]),
      'id = ' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value='1,2,3', operator='=')]),
      'id IN (' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value=(1,2,3), operator='=')]),
      'id IN (' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value=(1,2,3,None), operator='=')]),
      'id IS NULL OR ' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value=(1,None), operator='=')]),
      'id IS NULL OR ' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value=(1,None), operator='=')]),
      'id = ' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value=(1,), operator='=')]),
      'id = ' ),
    ( persons.c.id,
      dict(filter=[dict(property='id', value='1,2,3,NULL', operator='=')]),
      'id IS NULL OR ' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value='bar', operator='>')]),
      'firstname > ' ),
    ( persons.c.firstname,
      dict(filter=[dict(property='firstname', value='bar', operator='<')]),
      'firstname < ' ),
    ( persons.c.timestamp,
      dict(filter_col='timestamp', filter_value='2008-08-01T10:10:10,2009-07-01T12:12:12'),
      'timestamp IN (' ),
    ( persons.c.timestamp,
      dict(filter_col='timestamp', filter_value='2008-08-01T10:10:10><2009-07-01T12:12:12'),
      'timestamp BETWEEN ' ),
])
def test_operators(column, args, expected_snippet):
    conds = extract_filters(args)
    assert len(conds) == 1
    cond = conds[0]
    filter = cond.operator.filter(column, cond.value)
    assert expected_snippet in str(filter)


def test_make_filter():
    assert Filter.make('foo', 'bar') == Filter('foo', 'bar', Operator.EQUAL)
    assert Filter.make('foo', 'bar', 'EQUAL') == Filter('foo', 'bar', Operator.EQUAL)
    assert Filter.make('foo', 'bar', '<>') == Filter('foo', 'bar', Operator.NOT_EQUAL)
    assert Filter.make('foo', 'bar', 'NOT_EQUAL') == Filter('foo', 'bar', Operator.NOT_EQUAL)
    with pytest.raises(ValueError):
        Filter.make('foo', 'bar', 'zar')
