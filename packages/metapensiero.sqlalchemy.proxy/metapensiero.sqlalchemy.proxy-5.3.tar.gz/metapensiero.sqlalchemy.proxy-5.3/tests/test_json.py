# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Test JSON utils
# :Created:   dom 07 apr 2013 15:22:57 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2013, 2014, 2015, 2016, 2017 Lele Gaifax
#

from __future__ import absolute_import

from datetime import date, datetime, time
from decimal import Decimal
from uuid import uuid1

import pytest

from metapensiero.sqlalchemy.proxy.json import JSON, register_json_decoder_encoder


def test_date_jsonification():
    d = date(1968, 3, 18)
    assert JSON.decode(JSON.encode(d)) == d


def test_time_jsonification():
    t = time(10, 11, 12)
    assert JSON.decode(JSON.encode(t)) == t


def test_datetime_jsonification():
    dt = datetime(1968, 3, 18, 10, 10, 0)
    assert JSON.decode(JSON.encode(dt)) == dt


def test_decimal_jsonification():
    d = Decimal('3.1415926')
    assert JSON.decode(JSON.encode(d)) == d


def test_uuid_jsonification():
    u = uuid1()
    assert JSON.decode(JSON.encode(u)) == u


def test_plain_strings():
    s = 'aa:bb:cc'
    assert JSON.decode(JSON.encode(s)) == s

    s = 'aaaa-bb-cc'
    assert JSON.decode(JSON.encode(s)) == s

    s = 'aaaa-bb-ccTdd:ee:ff'
    assert JSON.decode(JSON.encode(s)) == s


def test_unjsonable():
    class Foo(object):
        pass

    f = Foo()
    with pytest.raises(TypeError):
        JSON.encode(f)

    from decimal import Decimal
    from nssjson import JSONDecoder, JSONEncoder

    json2py = JSONDecoder(
        handle_uuid=True,
        parse_float=Decimal,
        iso_datetime=True,
        object_hook=lambda d: Foo() if d.get('__class__') == 'Foo' else d).decode

    class FooEncoder(JSONEncoder):
        def default(self, o):
            if isinstance(o, Foo):
                return {'__class__': 'Foo'}
            else:
                return super().default(o)

    py2json = FooEncoder(separators=(',', ':'),
                         handle_uuid=True,
                         use_decimal=True,
                         iso_datetime=True).encode

    register_json_decoder_encoder(json2py, py2json)

    assert isinstance(JSON.decode(JSON.encode(f)), Foo)
