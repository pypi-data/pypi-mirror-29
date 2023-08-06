# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Tests for sort functions
# :Created:   dom 12 feb 2017 14:49:18 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2017 Lele Gaifax
#

from __future__ import absolute_import

import pytest

from metapensiero.sqlalchemy.proxy.sorters import (
    Direction,
    Sorter,
    extract_sorters,
    )


@pytest.mark.parametrize('args,expected', [
    ( dict(sorters=[Sorter('foo', Direction.ASC)]),
      [('foo', Direction.ASC)] ),
    ( dict(sorters='{"property":"foo"}'),
      [('foo', Direction.ASC)] ),
    ( dict(sort_col='foo'),
      [('foo', Direction.ASC)] ),
    ( dict(sort_col='foo,bar'),
      [('foo', Direction.ASC), ('bar', Direction.ASC)] ),
    ( dict(sort_col=['foo', 'bar']),
      [('foo', Direction.ASC), ('bar', Direction.ASC)] ),
    ( dict(sort_col='foo', sort_dir='ASC'),
      [('foo', Direction.ASC)] ),
    ( dict(sort_col='foo', sort_dir='DESC'),
      [('foo', Direction.DESC)] ),
    ( dict(sort_col='foo', sort_dir=Direction.ASC),
      [('foo', Direction.ASC)] ),
    ( dict(sort_col='foo', sort_dir=Direction.DESC),
      [('foo', Direction.DESC)] ),
    ( dict(sorters=Sorter('foo', Direction.DESC)),
      [('foo', Direction.DESC)] ),
    ( dict(sorters={'property': 'foo'}),
      [('foo', Direction.ASC)] ),
    ( dict(sorters=['foo, bar']),
      [('foo', Direction.ASC), ('bar', Direction.ASC)] ),
    ( dict(sorters=('foo, bar',)),
      [('foo', Direction.ASC), ('bar', Direction.ASC)] ),
    ( dict(sort_by_foo='ASC'),
      [('foo', Direction.ASC)] ),
    ( dict(sort_by_foo='DESC'),
      [('foo', Direction.DESC)] ),
])
def test_extract_sorters(args, expected):
    assert extract_sorters(args) == expected


@pytest.mark.parametrize('args', [
    dict(sort_col=123),
    dict(sort_col=[1,2,3]),
    dict(sort_col=None),
    dict(sorters={'foo': 'bar'}),
    dict(sorters=('foo, bar, zar')),
    dict(sorters='foo, bar'),
    dict(sort_by_foo=1),
])
def test_bad_specification(args):
    with pytest.raises(ValueError):
        extract_sorters(args)


def test_make_sorter():
    assert Sorter.make('foo') == Sorter('foo', Direction.ASC)
    assert Sorter.make('foo', '>') == Sorter('foo', Direction.DESC)
    assert Sorter.make('foo', 'DESC') == Sorter('foo', Direction.DESC)
    with pytest.raises(ValueError):
        Sorter.make('foo', 'bar')
