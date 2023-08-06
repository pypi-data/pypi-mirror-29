# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Types helpers
# :Created:   sab 22 lug 2017 10:23:36 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2017 Lele Gaifax
#

from collections import OrderedDict
from datetime import datetime
from inspect import isclass

from sqlalchemy import (
    Boolean, Date, DateTime, Integer, Interval, Numeric, String, Text, Time, Unicode,
    UnicodeText)


##
## ADAPTORS
##

def _adapt_integer(s):
    if s is None or s == 'NULL':
        res = None
    elif isinstance(s, str):
        res = int(s) if s else None
    else:
        res = int(s)
    return res

def _adapt_date(s, _strptime=datetime.strptime):
    if s is None or s == 'NULL':
        res = None
    elif isinstance(s, str):
        if s:
            res = _strptime(s, "%Y-%m-%d").date()
        else:
            res = None
    else:
        res = s
    return res

def _adapt_datetime(s, _strptime=datetime.strptime):
    if s is None or s == 'NULL':
        res = None
    elif isinstance(s, str):
        if s:
            res = _strptime(s, "%Y-%m-%dT%H:%M:%S")
        else:
            res = None
    else:
        res = s
    return res

def _adapt_boolean(s):
    if s is None or s == 'NULL':
        res = None
    elif isinstance(s, str):
        if s:
            res = s.lower() == 'true'
        else:
            res = None
    else:
        res = bool(s)
    return res

def _adapt_null(s):
    if s is None or s == 'NULL':
        res = None
    elif isinstance(s, str):
        if s:
            res = s
        else:
            res = None
    else:
        res = s
    return res


_sqlalchemy_adaptors = OrderedDict((
    (Integer, _adapt_integer),
    (Date, _adapt_date),
    (DateTime, _adapt_datetime),
    (Boolean, _adapt_boolean),
))


def _lookup_class(mapping, cls):
    # Idea stolen from Agronholm's cbor2
    function = mapping.get(cls)
    if function is None:
        for probe, function in mapping.items():
            if issubclass(cls, probe):
                mapping[cls] = function
                break
        else:
            function = None
    return function


def register_sa_type_adaptor(cls, function):
    """Register an adaptor `function` for the given SQLAlchemy `cls` type.

    :param cls: a class
    :param function: a callable, accepting one argument and returning a value compatible with
                     `cls`
    """

    assert isclass(cls)
    _sqlalchemy_adaptors[cls] = function


def get_adaptor_for_sa_type(satype):
    """Get an adaptor for the given type.

    :param satype: an SQLAlchemy ``TypeEngine``
    :rtype: a function

    Return a function that adapts its unique argument to the given `satype`.
    In particular, an empty string value or ``"NULL"`` are converted to ``None``.
    """

    cls = satype if isclass(satype) else type(satype)
    adaptor = _lookup_class(_sqlalchemy_adaptors, cls)
    if adaptor is None:
        adaptor = _adapt_null
    return adaptor


##
## METADATA
##

_default_type_metadata = OrderedDict((
    (String, {
        'type': 'string'}),
    (Unicode, {
        'type': 'string'}),
    (Text, {
        'type': 'text'}),
    (UnicodeText, {
        'type': 'text'}),
    (Boolean, {
        'type': 'boolean'}),
    (Numeric, {
        'type': 'numeric',
        'align': 'right'}),
    (Integer, {
        'type': 'integer',
        'align': 'right'}),
    (DateTime, {
        'type': 'datetime'}),
    (Date, {
        'type': 'date'}),
    (Time, {
        'type': 'time',
        'align': 'right'}),
    (Interval, {
        'type': 'interval',
        'align': 'right',
        'timedelta': True}),
    (str, {
        'type': 'string'}),
))


def register_sa_type_metadata(cls, meta, merge=True):
    """Register/override metadata information for the given SQLAlchemy `cls` type.

    :param cls: a class
    :param meta: a dictionary
    :param merge: a boolean

    If `cls` is already registered and `merge` is ``True`` (the default), then `meta` will
    overwrite existing information, basically doing ``existing.update(meta)``.
    """

    assert isclass(cls)
    if merge and cls in _default_type_metadata:
        _default_type_metadata[cls].update(meta)
    else:
        _default_type_metadata[cls] = meta


def get_metadata_for_sa_type(satype):
    """Get base metadata for the given type.

    :param satype: an SQLAlchemy ``TypeEngine`` or an instance of it
    :rtype: a dictionary

    Return a dictionary containing the base metadata information for the given `satype`.
    """

    cls = satype if isclass(satype) else type(satype)
    meta = _lookup_class(_default_type_metadata, cls)
    if meta is None:
        meta = _lookup_class(_default_type_metadata, str)
    return meta
