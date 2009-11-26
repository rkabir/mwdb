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

import sqlalchemy.orm.exc as orm_exc
import mwdb

from . import markup

class Wikipedia(object):
    """Wikipedia in a single language."""

    def __init__(self, language):
        self.language = language

    def __repr__(self):
        representation = 'Wikipedia({0.language})'.format(self)
        return representation.encode('utf8')

    def articles(self, batch_size=500):
        """Article generator.

        This method returns all articles in this Wikipedia language version.

        :param batch_size:  Number of articles that will be fetched
                            simultaneously from the database.
        :type batch_size:   int
        """
        art_cls = mwdb.databases[self.language].classes['Article']
        session = mwdb.databases[self.language].session
        return session.query(art_cls).yield_per(batch_size)

    def categories(self, batch_size=500):
        """Category generator.

        This method returns all articles in this Wikipedia language version.

        :param batch_size:  Number of articles that will be fetched
                            simultaneously from the database.
        :type batch_size:   int
        """
        art_cls = mwdb.databases[self.language].classes['Category']
        session = mwdb.databases[self.language].session
        return session.query(art_cls).yield_per(batch_size)

    def get_article(self, title):
        title = markup.wikify(title)
        cl = mwdb.databases[self.language].classes['Article']
        session = mwdb.databases[self.language].session
        try:
            return session.query(cl).filter_by(title=title).one()
        except orm_exc.NoResultFound, e:
            return None

    def get_category(self, title):
        title = markup.clean_title(title, self.language, 14)
        cl = mwdb.databases[self.language].classes['Category']
        session = mwdb.databases[self.language].session
        try:
            return session.query(cl).filter_by(title=title).one()
        except orm_exc.NoResultFound, e:
            return None
