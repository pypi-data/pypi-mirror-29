# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Test types adapters
# :Created:   sab 22 lug 2017 12:04:06 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2017 Lele Gaifax
#

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Boolean, Date, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID as SA_UUID

from metapensiero.sqlalchemy.proxy.types import (
    _adapt_boolean,
    _adapt_date,
    _adapt_datetime,
    _adapt_integer,
    _adapt_null,
    get_adaptor_for_sa_type,
    get_metadata_for_sa_type,
    register_sa_type_adaptor,
    register_sa_type_metadata,
)


def test_boolean():
    adaptor = get_adaptor_for_sa_type(Boolean)
    assert adaptor is _adapt_boolean

    assert adaptor(None) is None
    assert adaptor('') is None
    assert adaptor('NULL') is None
    assert adaptor('false') is False
    assert adaptor('true') is True
    assert adaptor(0) is False
    assert adaptor(1) is True
    assert adaptor(False) is False
    assert adaptor(True) is True


def test_date():
    adaptor = get_adaptor_for_sa_type(Date)
    assert adaptor is _adapt_date

    assert adaptor(None) is None
    assert adaptor('') is None
    assert adaptor('NULL') is None
    assert adaptor('1968-03-18') == date(1968, 3, 18)
    assert adaptor(date(1968, 3, 18)) == date(1968, 3, 18)


def test_datetime():
    adaptor = get_adaptor_for_sa_type(DateTime)
    assert adaptor is _adapt_datetime

    assert adaptor(None) is None
    assert adaptor('') is None
    assert adaptor('NULL') is None
    assert adaptor('1968-03-18T10:10:10') == datetime(1968, 3, 18, 10, 10, 10)
    assert adaptor(datetime(1968, 3, 18, 10, 10, 10)) == datetime(1968, 3, 18, 10, 10, 10)


def test_integer():
    adaptor = get_adaptor_for_sa_type(Integer)
    assert adaptor is _adapt_integer

    assert adaptor(None) is None
    assert adaptor('') is None
    assert adaptor('NULL') is None
    assert adaptor('1') == 1
    assert adaptor(1) == 1


def _adapt_uuid(s, _uuid=UUID):
    if s is None or s == 'NULL':
        res = None
    elif isinstance(s, str):
        res = _uuid(s) if s else None
    elif isinstance(s, int):
        res = _uuid(int=s)
    else:
        res = s
    return res


def test_uuid():
    adaptor = get_adaptor_for_sa_type(SA_UUID)
    assert adaptor is _adapt_null

    assert adaptor(None) is None
    assert adaptor('') is None
    assert adaptor('NULL') is None
    assert adaptor(0) == 0
    assert adaptor(UUID(int=0)) == UUID(int=0)

    assert get_adaptor_for_sa_type(SA_UUID()) is _adapt_null

    register_sa_type_adaptor(SA_UUID, _adapt_uuid)

    adaptor = get_adaptor_for_sa_type(SA_UUID)
    assert adaptor is _adapt_uuid

    adaptor = get_adaptor_for_sa_type(SA_UUID())
    assert adaptor is _adapt_uuid

    assert adaptor(None) is None
    assert adaptor(123) == UUID(int=123)
    assert adaptor('00000000-0000-0000-0000-000000000000') == UUID(int=0)


def test_unknown():
    class M:
        pass

    adaptor = get_adaptor_for_sa_type(M)
    assert adaptor is _adapt_null


def test_register_metadata():
    meta = get_metadata_for_sa_type(SA_UUID)
    assert meta == get_metadata_for_sa_type(str)

    register_sa_type_metadata(SA_UUID, {'type': 'uuid', 'width': 100})

    meta = get_metadata_for_sa_type(SA_UUID())
    assert meta['type'] == 'uuid'
    assert meta['width'] == 100

    register_sa_type_metadata(SA_UUID, {'width': 200})

    meta = get_metadata_for_sa_type(SA_UUID())
    assert meta['type'] == 'uuid'
    assert meta['width'] == 200
