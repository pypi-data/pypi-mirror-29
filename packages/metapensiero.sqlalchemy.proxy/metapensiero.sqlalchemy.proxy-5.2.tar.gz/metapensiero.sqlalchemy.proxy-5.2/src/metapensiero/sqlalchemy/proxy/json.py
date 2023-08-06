# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- nssjson glue
# :Created:   gio 04 dic 2008 13:56:51 CET
# :Author:    Lele Gaifax <lele@nautilus.homeip.net>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008, 2009, 2010, 2012, 2013, 2014, 2016, 2017 Lele Gaifax
#

class JSON:
    """
    Namespace-class to make it easier replacing the actual implementation of the methods using
    a different JSON library such as `python-rapidjson`__.

    __ https://pypi.python.org/pypi/python-rapidjson
    """

    @staticmethod
    def decode(s):
        """Parse `s`, a JSON encoded string, and return the equivalent Python structure.

        This is implemented on top of nssjson__, to handle ``UUID``, ``datetime``, ``date`` and
        ``Decimal`` data types.

        __ https://pypi.python.org/pypi/nssjson
        """

        import decimal
        from nssjson import JSONDecoder, JSONEncoder
        json2py = JSONDecoder(handle_uuid=True,
                              parse_float=decimal.Decimal,
                              iso_datetime=True).decode
        JSON.decode = staticmethod(json2py)
        return json2py(s)

    @staticmethod
    def encode(o):
        """Encode `o`, an arbitrary Python object, into a JSON encoded string.

        This is implemented on top of nssjson__, to handle ``UUID``, ``datetime``, ``date`` and
        ``Decimal`` data types.

        __ https://pypi.python.org/pypi/nssjson
        """

        from nssjson import JSONEncoder
        py2json = JSONEncoder(separators=(',', ':'),
                              handle_uuid=True,
                              use_decimal=True,
                              iso_datetime=True).encode
        JSON.encode = staticmethod(py2json)
        return py2json(o)


def register_json_decoder_encoder(decode, encode):
    "Replace the JSON `decode` and `encode` functions."

    JSON.decode = decode if isinstance(decode, staticmethod) else staticmethod(decode)
    JSON.encode = encode if isinstance(encode, staticmethod) else staticmethod(encode)
