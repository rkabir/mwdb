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

class PageText(object):
    """A Text."""

    def __repr__(self):
        return '{0.__class__.__name__}({0.title!r})'.format(self)

    def __str__(self):
        return unicode(self).encode('utf8')

    def __unicode__(self):
        return '{0.__class__.__name__}({0.title})'.format(self)

    @property
    def timestamp(self):
        return self.revision.timestamp

class Revision(object):
    """A Revision"""

    def __repr__(self):
        return '{0.__class__.__name__}({0.title!r}, {0.timestamp})'.format(
            self)

    def __str__(self):
        return unicode(self).encode('utf8')

    def __unicode__(self):
        return '{0.__class__.__name__}({0.title}, {0.timestamp})'.format(self)
