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

import itertools
import logging

import mwdb

from sqlalchemy.orm import object_mapper
from sqlalchemy.ext.associationproxy import association_proxy

from . import wikipedia

_log = logging.getLogger(__name__)

class PageLink(object):
    """A PageLink"""

    def __repr__(self):
        return '{0.__class__.__name__}({0.title!r})'.format(self)

    def __str__(self):
        return unicode(self).encode('utf8')

    def __unicode__(self):
        return '{0.__class__.__name__}({0.title})'.format(self)

    @property
    def language(self):
        return object_mapper(self).language


class CategoryLink(object):
    """A CategoryLink"""

    def __repr__(self):
        return '{0.__class__.__name__}({0.title!r})'.format(self)

    def __str__(self):
        return unicode(self).encode('utf8')

    def __unicode__(self):
        return '{0.__class__.__name__}({0.title})'.format(self)


class LanguageLink(object):
    """A LanguageLink"""

    def __repr__(self):
        return '{0.__class__.__name__}({0.lang!r}, {0.title!r})'.format(
            self)

    def __str__(self):
        return unicode(self).encode('utf8')

    def __unicode__(self):
        return '{0.__class__.__name__}({0.lang}, {0.title})'.format(self)


class Page(object):
    """A Page.

    This is the base class for all Wikipedia page types.
    """

    def __repr__(self):
        return '{0.__class__.__name__}({0.title!r})'.format(self)

    def __str__(self):
        return unicode(self).encode('utf8')

    def __unicode__(self):
        return '{0.__class__.__name__}({0.title})'.format(self)

    def iter_translations(self):
        raise NotImplementedError('Implement this method in a subclass')

    @property
    def raw_text(self):
        return self.latest_text.text

    def iter_categories_startwith(self, string, batch_size=42):
        """All categories of this Page whose titles start with the given
        string.

        :param string:  Category title must start with this string.
        :type string:   str

        :param batch_size:  Number of categories that will be fetched
                            simultaneously from the database.
        :type batch_size:   int
        """
        c_cls = mwdb.databases[self.language].classes['Category']
        return self._category_query.filter(
            c_cls.title.like(u'{0}%%'.format(string))).yield_per(batch_size)

    def iter_categories_endwith(self, string, batch_size=42):
        """All categories of this Page whose titles end with the given
        string.

        :param string:  Category title must end with this string.
        :type string:   str

        :param batch_size:  Number of categories that will be fetched
                            simultaneously from the database.
        :type batch_size:   int
        """
        c_cls = mwdb.databases[self.language].classes['Category']
        return self._category_query.filter(
            c_cls.title.like(u'%%{0}'.format(string))).yield_per(batch_size)

    def iter_categories_contain(self, string, batch_size=42):
        """All categories of this Page whose titles contain the given
        string.

        :param string:  Category title must contain this string.
        :type string:   str

        :param batch_size:  Number of categories that will be fetched
                            simultaneously from the database.
        :type batch_size:   int
        """
        c_cls = mwdb.databases[self.language].classes['Category']
        return self._category_query.filter(
            c_cls.title.like(u'%%{0}%%'.format(string))).yield_per(batch_size)


class Article(Page):
    """An Article"""

    _linked_articles = association_proxy('article_links', 'goal')
    _linked_from_articles = association_proxy('article_links_in', 'source_page')

    def iter_linked_article_titles(self):
        return (t.title for t in self.article_links)

    def iter_linked_articles(self):
        return itertools.ifilter(lambda x:x, self._linked_articles)

    def iter_linked_from_articles(self):
        return itertools.ifilter(lambda x:x, self._linked_from_articles)

    def iter_translations(self):
        present_langs = mwdb.databases.keys()
        return (article for article in
                (mwdb.Wikipedia(ll.lang.replace('-', '_')).get_article(ll.title)
                 for ll in self.language_links
                 if ll.lang.replace('-', '_') in present_langs)
                if article)


class Template(Page):
    pass


class Category(Page):
    """A Category"""

    def iter_translations(self):
        present_langs = mwdb.databases.keys()
        return (cat for cat in
                (mwdb.Wikipedia(ll.lang.replace('-', '_')).get_category(ll.title)
                 for ll in self.language_links
                 if ll.lang.replace('-', '_') in present_langs)
                if cat)

    def iter_subcategories_startwith(self, string, batch_size=42):
        """All subcategories whose titles start with the given string.

        :param string:  Category title must start with this string.
        :type string:   str

        :param batch_size:  Number of categories that will be fetched
                            simultaneously from the database.
        :type batch_size:   int
        """
        c_cls = mwdb.databases[self.language].classes['Category']
        return self._subcategory_query.filter(
            c_cls.title.like('{0}%%'.format(string))).yield_per(batch_size)

    def iter_subcategories_endwith(self, string, batch_size=42):
        """All subcategories whose titles end with the given string.

        :param string:  Category title must end with this string.
        :type string:   str

        :param batch_size:  Number of categories that will be fetched
                            simultaneously from the database.
        :type batch_size:   int
        """
        c_cls = mwdb.databases[self.language].classes['Category']
        return self._subcategory_query.filter(
            c_cls.title.like('%%{0}'.format(string))).yield_per(batch_size)

    def iter_subcategories_contain(self, string, batch_size=42):
        """All subcategories whose titles contain the given string.

        :param string:  Category title must contain this string.
        :type string:   str

        :param batch_size:  Number of categories that will be fetched
                            simultaneously from the database.
        :type batch_size:   int
        """
        c_cls = mwdb.databases[self.language].classes['Category']
        return self._subcategory_query.filter(
            c_cls.title.like(u'%%{0}%%'.format(string))).yield_per(batch_size)

    def iter_member_page_startwith(self, string, batch_size=42):
        """All pages that belong to this category whose titles start with the
        given string.

        :param string:  Page titles must start with this string.
        :type string:   str

        :param batch_size:  Number of pages that will be fetched
                            simultaneously from the database.
        :type batch_size:   int
        """
        c_cls = mwdb.databases[self.language].classes['Category']
        return self._member_page_query.filter(
            c_cls.title.like('{0}%%'.format(string))).yield_per(batch_size)

    def iter_member_page_endwith(self, string, batch_size=42):
        """All pages that belong to this category whose titles end with the
        given string.

        :param string:  Page titles must end with this string.
        :type string:   str

        :param batch_size:  Number of pages that will be fetched
                            simultaneously from the database.
        :type batch_size:   int
        """
        c_cls = mwdb.databases[self.language].classes['Article']
        return self._member_page_query.filter(
            c_cls.title.like(u'%%{0}'.format(string))).yield_per(batch_size)

    def iter_member_page_contain(self, string, batch_size=42):
        """All pages that belong to this category whose titles contain the
        given string.

        :param string:  Page titles must contain this string.
        :type string:   str

        :param batch_size:  Number of pages that will be fetched
                            simultaneously from the database.
        :type batch_size:   int
        """
        c_cls = mwdb.databases[self.language].classes['Category']
        return self._member_page_query.filter(
            c_cls.title.like('%%{0}%%'.format(string))).yield_per(batch_size)
