# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Query builders
# :Created:   sab 18 ott 2008 23:59:34 CEST
# :Author:    Lele Gaifax <lele@nautilus.homeip.net>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008, 2009, 2010, 2012, 2013, 2014, 2015, 2016 Lele Gaifax
#

"""
This module implements some facilities that makes it very easy to
rework arbitrary SQLAlchemy queries applying some filter conditions,
constraining the actual selected columns, batched results, obtaining a
meta description of the resultset, eventually marshalled in JSON, or
as a list of plain dictionaries instead of the SQLAlchemy rows, and so
on.
"""
