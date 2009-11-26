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

    def __unicode__(self):
        return '{0}({1})'.format(self.__class__.__name__,
                                 self.page.title.encode('utf8'))

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__,
                                 repr(self.page.title))

    @property
    def timestamp(self):
        return self.revision.timestamp

class Revision(object):
    """A Revision"""

    def __unicode__(self):
        return '{0}({1}, {2})'.format(self.__class__.__name__,
                                      self.page.title.encode('utf8'),
                                      self.timestamp)

    def __repr__(self):
        return '{0}({1}, {2})'.format(self.__class__.__name__,
                                      repr(self.page.title),
                                      self.timestamp)
