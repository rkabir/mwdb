# -*- coding: UTF-8 -*-

# © Copyright 2009 Wolodja Wentland and Johannes Knopp.
# All Rights Reserved.

# This file is part of mwdb.
#
# mwdb is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mwdb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with mwdb. If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
from __future__ import unicode_literals

import logging

from . import orm
from . import mediawiki

from .mediawiki.wikipedia import Wikipedia


class NullHandler(logging.Handler):
    def emit(self, record):
        pass

_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)
_log.addHandler(NullHandler())

databases = orm.database.Databases()
