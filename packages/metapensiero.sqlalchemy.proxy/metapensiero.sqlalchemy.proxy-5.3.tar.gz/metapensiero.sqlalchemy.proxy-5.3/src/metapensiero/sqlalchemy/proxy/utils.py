# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Utility functions
# :Created:   mer 03 feb 2016 10:56:36 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017 Lele Gaifax
#

from datetime import datetime
import logging

from sqlalchemy import Column
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import ColumnCollection
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.types import TypeDecorator

from .json import JSON


log = logging.getLogger(__name__)


def get_exception_message(e):
    """Extract the error message from the given exception.

    :param e: an Exception instance
    :rtype: a unicode string
    """

    msg = str(e)
    if isinstance(msg, bytes):
        for enc in ('utf-8', 'latin1'):
            try:
                msg = msg.decode(enc)
            except UnicodeDecodeError:
                pass
            else:
                break
        else:
            msg = msg.decode('utf-8', errors='replace')
    return msg


def get_column_type(column):
    """Return the concrete type of a column."""

    ctype = column.type
    if isinstance(ctype, TypeDecorator):
        ctype = ctype.impl
    return ctype


def col_by_name(query, colname):
    "Helper: find the (first) column with the given name."

    # First look in the selected columns
    for c in query.inner_columns:
        try:
            if c.name == colname:
                return c
        except AttributeError:
            if isinstance(c, BinaryExpression):
                l, r = c._orig
                if (isinstance(l, Column) and l.name == colname
                    or
                    isinstance(r, Column) and r.name == colname):
                    return c
            else:
                log.warning('Unhandled inner column type: %r', type(c).__name__)

    # Then in the froms
    for f in query.froms:
        columns = f.columns

        # The FROM may not be a plain table: this happens for example when we are selecting
        # from a PG function; in that case, there's little we can do here

        if not isinstance(columns, ColumnCollection):
            continue

        c = columns.get(colname)
        if c is not None:
            return c

        papables = [c for c in columns if c.key == colname]
        if len(papables)>=1:
            c = papables[0]
            if len(papables)>1:
                log.warning('Ambiguous column name "%s" in %s:'
                            ' selecting "%s"', colname, str(query), c)
            return c

        papables = [c for c in columns if c.name.endswith('_'+colname)]
        if len(papables)>=1:
            c = papables[0]
            if len(papables)>1:
                log.warning('Ambiguous column name "%s" in %s:'
                            ' selecting "%s"', colname, str(query), c)
            return c


def create_change_saver(adaptor=None, save_changes=None,
                        modified_slot_name='modified_records',
                        deleted_slot_name='deleted_records',
                        inserted_ids_slot='inserted_ids',
                        modified_ids_slot='modified_ids',
                        deleted_ids_slot='deleted_ids',
                        result_slot='root',
                        success_slot='success',
                        message_slot='message'): # pragma: nocover
    """Function factory to implement the standard POST handler for a proxy.

    :param adaptor: a function that adapts the changes before application
    :param save_changes: the function that concretely applies the changes
    :param modified_slot_name: a string, by default 'modified_records'
    :param deleted_slot_name: a string, by default 'deleted_records'
    :param inserted_ids_slot: a string, by default 'inserted_ids'
    :param modified_ids_slot: a string, by default 'modified_ids'
    :param deleted_ids_slot: a string, by default 'deleted_ids'
    :param result_slot: a string, by default 'root'
    :param success_slot: a string, by default 'success'
    :param message_slot: a string, by default 'message'
    :returns: a dictionary, with a boolean `success` slot with a
        ``True`` value if the operation was completed without errors,
        ``False`` otherwise: in the latter case the `message` slot
        contains the reason for the failure. Three other slots carry
        lists of dictionaries with the ids of the *inserted*,
        *modified* and *deleted* records.

    This implements the generic behaviour we need to save changes back to
    the database.

    The `adaptor` function takes four arguments, respectively the SA
    session, the request, a list of added/modified records and a list
    of deleted records; it must return two (possibly modified) lists,
    one containing added/modified records and the other with the
    records to delete, e.g.::

        def adaptor(sa_session, request, modified_recs, deleted_recs):
            # do any step to adapt incoming data
            return modified_recs, deleted_recs
    """

    def workhorse(sa_session, request, **args):
        mr = JSON.decode(args[modified_slot_name])
        dr = JSON.decode(args[deleted_slot_name])

        if adaptor is not None:
            try:
                mr, dr = adaptor(sa_session, request, mr, dr)
            except Exception as e:
                log.critical('Could not adapt changes: %s', e, exc_info=True)
                return {
                    success_slot: False,
                    message_slot: 'Internal error, consult application log'
                }

        try:
            iids, mids, dids = save_changes(sa_session, request, mr, dr)
            status = True
            statusmsg = "Ok"
        except SQLAlchemyError as e:
            msg = get_exception_message(e)
            log.error('Could not save changes to the database: %s', msg)
            status = False
            statusmsg = msg.split('\n')[0]
            iids = mids = dids = None
        except Exception as e:
            msg = get_exception_message(e)
            log.critical('Could not save changes to the database: %s',
                         msg, exc_info=True)
            status = False
            statusmsg = 'Internal error, consult application log.'
            iids = mids = dids = None

        return { success_slot: status,
                 message_slot: statusmsg,
                 inserted_ids_slot: iids,
                 modified_ids_slot: mids,
                 deleted_ids_slot: dids,
               }

    return workhorse


def csv_to_list(csv):
    """Build a list of strings from a CSV or JSON array.

    :param csv: a string containing either a ``CSV`` or a JSON array
    :rtype: a Python list

    This is very simplicistic: since its used to transfer a list of field names, that is plain
    ASCII strings, JSON escapes are not even considered.

    `csv` may be either a plain CSV string such as ``first,second,third`` or a JSON array, such
    as ``["first","second","third"]``.
    """

    if csv.startswith('[') and csv.endswith(']'):
        res = [v[1:-1] for v in csv[1:-1].split(',')]
    else:
        res = [v.strip() for v in csv.split(',')]
    return res
