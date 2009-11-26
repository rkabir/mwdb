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

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.sql import *

from mwdb.mediawiki.pages import Page, Article, Template, Category
from mwdb.mediawiki.pages import PageLink, CategoryLink, LanguageLink
from mwdb.mediawiki.text import PageText, Revision

_log = logging.getLogger(__name__)


def init_mappers(metadata, language):
    pages = metadata.tables['page']
    texts = metadata.tables['text']
    pagelinks = metadata.tables['pagelinks']
    catlinks = metadata.tables['categorylinks']
    langlinks = metadata.tables['langlinks']
    revisions = metadata.tables['revision']

    # you might think wtf now... but do not fear and have a look at:
        # http://www.sqlalchemy.org/trac/wiki/UsageRecipes/EntityName

    # the basic idea is to get anonymous subclasses for each language. the
    # class name is that of the base class prefixed with the language
    # identifier. so an english article will have the class EN_Article

    _log.debug('Create classes for language: {0}'.format(language))

    Page_cls = type.__new__(type,
                            b'{0}_{1}'.format(language.upper(), 'Page'),
                            (Page, ), {})
    Page_cls.language = language

    Article_cls = type.__new__(type,
                               b'{0}_{1}'.format(language.upper(), 'Article'),
                               (Article, Page_cls, ), {})
    Article_cls.language = language

    Template_cls = type.__new__(type,
                                b'{0}_{1}'.format(language.upper(),
                                                  'Template'),
                                (Template, Page_cls, ), {})
    Template_cls.language = language

    Category_cls = type.__new__(type,
                                b'{0}_{1}'.format(language.upper(),
                                                  'Category'),
                                (Category, Page_cls, ), {})
    Category_cls.language = language

    #CategoryLink_cls =  type.__new__(type, language,
    #(CategoryLink, Page_cls,), {})

    PageText_cls = type.__new__(type,
                                b'{0}_{1}'.format(language.upper(), 'Text'),
                                (PageText, ), {})
    PageText_cls.language = language

    Revision_cls = type.__new__(type,
                                b'{0}_{1}'.format(language.upper(), 'Revision'),
                                (Revision, ), {})
    Revision_cls.language = language

    PageLink_cls = type.__new__(type,
                                b'{0}_{1}'.format(language.upper(),
                                                  'PageLink'),
                                (PageLink, ), {})
    PageLink_cls.language = language

    LanguageLink_cls = type.__new__(type,
                                    b'{0}_{1}'.format(language.upper(),
                                                      'LanguageLink'),
                                    (LanguageLink, ), {})
    LanguageLink.language = language

    #Class-Dictionary:
    classes = {'Page': Page_cls,
               'Article': Article_cls,
               'Template': Template_cls,
               'Category': Category_cls,
               'PageLink': PageLink_cls,
               'LanguageLink': LanguageLink_cls,
               'PageText': PageText_cls,
               'Revision': Revision_cls}

    _log.debug('{0}: Map {1}_Page'.format(language, language.upper()))
    page_m = mapper(Page_cls, pages,
                    include_properties = ['id', 'namespace', 'title',
                                          'is_redirect', 'text'],
                    properties = {
                        'id': pages.c.page_id,
                        'namespace': pages.c.page_namespace,
                        'title': pages.c.page_title,
                        'is_redirect': pages.c.page_is_redirect,
                        'categories': relation(
                            Category_cls,
                            secondary = catlinks,
                            primaryjoin = pages.c.page_id == catlinks.c.cl_from,
                            secondaryjoin = and_(
                                pages.c.page_namespace == 14,
                                catlinks.c.cl_to == pages.c.page_title),
                            foreign_keys = [catlinks.c.cl_from,
                                            catlinks.c.cl_to],
                            backref = backref('subcategories')),
                        '_category_query': relation(
                            Category_cls,
                            secondary = catlinks,
                            primaryjoin = pages.c.page_id == catlinks.c.cl_from,
                            secondaryjoin = and_(
                                pages.c.page_namespace == 14,
                                catlinks.c.cl_to == pages.c.page_title),
                            foreign_keys = [catlinks.c.cl_from,
                                            catlinks.c.cl_to],
                            lazy = 'dynamic',
                            backref = backref('subcategory_query',
                                              lazy = 'dynamic'),
                        ),
                        'latest_text': relation(
                            PageText_cls,
                            primaryjoin = pages.c.page_latest == texts.c.old_id,
                            foreign_keys = [pages.c.page_latest],
                            backref = backref('page', uselist = False),
                            uselist = False,
                        ),
                        'revisions': relation(
                            Revision_cls,
                            primaryjoin = pages.c.page_id == revisions.c.rev_page,
                            backref = backref('page'),
                            foreign_keys = [revisions.c.rev_page],
                        ),
                        'article_links': relation(
                            PageLink_cls,
                            primaryjoin = and_(
                                pagelinks.c.pl_namespace == 0,
                                pages.c.page_id == pagelinks.c.pl_from),
                            foreign_keys=[pagelinks.c.pl_from],
                            lazy = True,
                        ),
                        'article_links_in': relation(
                            PageLink_cls,
                            primaryjoin = and_(
                                pagelinks.c.pl_namespace == 0,
                                pagelinks.c.pl_title == pages.c.page_title),
                            foreign_keys = [pagelinks.c.pl_title],
                            lazy = True),
                        'language_links': relation(
                            LanguageLink_cls,
                            primaryjoin = pages.c.page_id == langlinks.c.ll_from,
                            foreign_keys = [langlinks.c.ll_from],
                            lazy = True)},
                        primary_key = [pages.c.page_id],
                        polymorphic_on = pages.c.page_namespace,
                        polymorphic_identity = -42)

    _log.debug('{0}: Map {1}_Article'.format(language, language.upper()))
    article_m = mapper(Article_cls,
                       inherits = page_m,
                       primary_key = [pages.c.page_id],
                       polymorphic_on = pages.c.page_namespace,
                       polymorphic_identity = 0)

    _log.debug('{0}: Map {1}_Template'.format(language, language.upper()))
    template_m = mapper(Template_cls,
                        inherits = page_m,
                        primary_key = [pages.c.page_id],
                        polymorphic_on = pages.c.page_namespace,
                        polymorphic_identity = 10)

    _log.debug('{0}: Map {1}_Category'.format(language, language.upper()))
    cat_m = mapper(Category_cls,
                   inherits = page_m,
                   primary_key = [pages.c.page_id],
                   polymorphic_on = pages.c.page_namespace,
                   polymorphic_identity = 14,
                   properties = {
                       'member_pages': relation(
                           Article_cls,
                           secondary = catlinks,
                           primaryjoin = pages.c.page_title == catlinks.c.cl_to,
                           secondaryjoin = and_(pages.c.page_namespace == 0,
                                                catlinks.c.cl_from == pages.c.page_id),
                           foreign_keys = [catlinks.c.cl_to,
                                           catlinks.c.cl_from]),
                       '_member_page_query': relation(
                           Article_cls,
                           secondary = catlinks,
                           primaryjoin = pages.c.page_title == catlinks.c.cl_to,
                           secondaryjoin = and_(pages.c.page_namespace == 0,
                                                catlinks.c.cl_from == pages.c.page_id),
                           lazy = 'dynamic',
                           foreign_keys = [catlinks.c.cl_to,
                                           catlinks.c.cl_from])})

    _log.debug('{0}: Map {1}_PageLink'.format(language, language.upper()))
    pagelinks_m = mapper(PageLink_cls,
                         pagelinks,
                         properties = {
                             'title': pagelinks.c.pl_title,
                             'namespace': pagelinks.c.pl_namespace,
                             'source_id': pagelinks.c.pl_from,
                             'goal': relation(
                                 Article_cls,
                                 primaryjoin = and_(
                                     pages.c.page_namespace == 0,
                                     pagelinks.c.pl_title == pages.c.page_title),
                                 foreign_keys = [pagelinks.c.pl_title]),
                             'source_page': relation(
                                 Article_cls,
                                 primaryjoin = pagelinks.c.pl_from == pages.c.page_id,
                                 foreign_keys = [pagelinks.c.pl_from])},
                         primary_key = [pagelinks.c.pl_from,
                                        pagelinks.c.pl_namespace,
                                        pagelinks.c.pl_title])

    _log.debug('{0}: Map {1}_LanguageLink'.format(language, language.upper()))
    langlinks_m = mapper(LanguageLink_cls,
                         langlinks,
                         properties = {
                             'title': langlinks.c.ll_title,
                             'lang': langlinks.c.ll_lang,
                             'source_id': langlinks.c.ll_from,
                             'source_page': relation(
                                 Article_cls,
                                 primaryjoin = langlinks.c.ll_from == pages.c.page_id,
                                 foreign_keys = [langlinks.c.ll_from])},
                         primary_key = [langlinks.c.ll_from,
                                        langlinks.c.ll_lang])

    _log.debug('{0}: Map {1}_PageText'.format(language, language.upper()))
    text_m = mapper(PageText_cls,
                    texts,
                    properties = {
                        'id': texts.c.old_id,
                        'text': texts.c.old_text})

    _log.debug('{0}: Map {1}_Revision'.format(language, language.upper()))
    revision_m = mapper(Revision_cls,
                        revisions,
                        properties = {
                            'id': revisions.c.rev_id,
                            'comment': revisions.c.rev_comment,
                            'timestamp': revisions.c.rev_timestamp,
                            'text': relation(
                                PageText_cls,
                                primaryjoin = revisions.c.rev_text_id == texts.c.old_id,
                                foreign_keys = [revisions.c.rev_text_id],
                                uselist = False,
                                backref = backref('revision', uselist = False))})

    return classes
