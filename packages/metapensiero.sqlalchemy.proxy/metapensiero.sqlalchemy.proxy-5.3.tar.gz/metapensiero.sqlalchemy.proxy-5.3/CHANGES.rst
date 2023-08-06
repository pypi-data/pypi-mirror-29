Changes
-------

5.3 (2018-03-15)
~~~~~~~~~~~~~~~~

* The Pyramid ``expose()`` decorator now forwards unrecognized keyword arguments to the proxy
  call


5.2 (2018-03-12)
~~~~~~~~~~~~~~~~

* Handle extraction of metadata from a BinaryExpression such as ``SELECT jsonfield['attr']``


5.1 (2018-03-08)
~~~~~~~~~~~~~~~~

* When a column has a *default* value, and it is directly computable (i.e. it is not a server
  side default), then extract it into its metadata


5.0 (2017-07-22)
~~~~~~~~~~~~~~~~

.. warning:: This release **breaks** backward compatibility in several ways!

* More versatile way to add/override basic metadata information (see
  ``register_sa_type_metadata()``)

* More versatile way to use different JSON library or encode/decode settings (see
  ``register_json_decoder_encoder()``): although the default implementation is still based on
  nssjson__, it is *not* required by default anymore at install time

* Basic metadata changed:

  - the `width` slot for all fields is gone, it's more reasonably computed by the actual UI
    framework in use: it was rather arbitrary anyway, and set to ``length * 10`` for String
    columns

  - the `length` slot is present only for ``String`` columns

  - the `type` slot now basically follows the SQLAlchemy nomenclature, in particular:

    Integer
      is now ``integer`` instead of ``int``

    BigInteger
      is now ``integer``, instead of ``int`` with an arbitrarily different ``width`` than the
      one used for Integer

    Numeric
      is now ``numeric`` instead of ``float``

    DateTime
      is now ``datetime`` instead of ``date`` with `timestamp` set to ``True``

    Time
      is now ``time`` instead of ``date`` with `time` set to ``True``

    Interval
      is now ``interval`` instead of ``string`` with ``timedelta`` set to ``True``

    Text
      is now ``text`` instead of ``string`` with an arbitrary `width` of ``50``

    UnicodeText
      is now ``text```

    Unicode
      is now ``string``

  - the `format` slot for DateTime, Date and Time fields is gone, as it was ExtJS specific

__ https://pypi.python.org/pypi/nssjson


4.8 (2017-06-17)
~~~~~~~~~~~~~~~~

* Use a tuple instead of a list for the `foreign_keys` slot in metadata, and for the
  `primary_key` too when it is composed by more than one column


4.7 (2017-05-18)
~~~~~~~~~~~~~~~~

* Properly recognize SA Interval() columns


4.6 (2017-05-08)
~~~~~~~~~~~~~~~~

* Handle big integers in metadata information


4.5 (2017-04-10)
~~~~~~~~~~~~~~~~

* Fix a crash when applying a filter on a non-existing column in a statement selecting from a
  function


4.4 (2017-04-01)
~~~~~~~~~~~~~~~~

* Rename filter operator ``CONTAINED`` to ``CONTAINS``, and reimplement it to cover different
  data types, in particular PostgreSQL's ranges


4.3 (2017-03-22)
~~~~~~~~~~~~~~~~

* Minor tweak, no externally visible changes


4.2 (2017-03-10)
~~~~~~~~~~~~~~~~

* Reduce clutter, generating a simpler representation of Operator and Direction enums


4.1 (2017-02-13)
~~~~~~~~~~~~~~~~

* Fix an oversight in Filter tuple slots positions, to simplify Filter.make() implementation


4.0 (2017-02-13)
~~~~~~~~~~~~~~~~

* From now on, a Python3-only package

* Backward incompatible sorters and filters refactor, to make interaction easier for code using
  the library

* Drop obsolete Pylons extension


3.6 (2017-01-11)
~~~~~~~~~~~~~~~~

* New Sphinx documentation

* Field's metadata now carries also information about foreign keys

* Handle literal columns in core queries


3.5 (2016-12-29)
~~~~~~~~~~~~~~~~

* Fix incompatibility issue with SQLAlchemy 1.1.x when using ORM


3.4 (2016-03-12)
~~~~~~~~~~~~~~~~

* Better recognition of boolean argument values, coming from say an HTTP channel as string
  literals

* Use tox to run the tests


3.3 (2016-02-23)
~~~~~~~~~~~~~~~~

* Handle the case when the column type cannot be determined


3.2 (2016-02-19)
~~~~~~~~~~~~~~~~

* Fix corner case with queries ordered by a subselect


3.1 (2016-02-07)
~~~~~~~~~~~~~~~~

* Fix metadata extraction of labelled columns on joined tables

* Adjust size of time fields and align them to the right


3.0 (2016-02-03)
~~~~~~~~~~~~~~~~

* Internal, backward incompatible code reorganization, splitting the main module into smaller
  pieces

* Handle corner cases with joined queries involving aliased tables


Previous changes are here__.

__ https://bitbucket.org/lele/metapensiero.sqlalchemy.proxy/src/master/OLDERCHANGES.rst
