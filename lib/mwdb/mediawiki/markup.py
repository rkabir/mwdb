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

from .. import siteinfo

site_info = siteinfo.SiteInformation()

def wikify(title):
    """Wikify title.

    Essentially just replacement of spaces with underscores

    :param title:   The title to wikify
    :type title:    string
    """
    return title.replace(' ', '_')

def strip_namespace(title, lang, namespace):
    """Strip given namespace from title

    This method will strip all substrings that are used in the given
    language for the given namespace from title.

    :param title:   The title to strip
    :type title:    string

    :param lang:    Language code
    :type lang:     string

    :param namespace:   The namespace to strip
    :type namespace:    int
    """
    namespace_strings = site_info.get_namespace_names(lang, namespace)
    for ns in (wikify(ns) for ns in namespace_strings):
        if title.startswith('{0}:'.format(ns)):
            return title.replace('{0}:'.format(ns), '', 1)
    return title

def clean_title(title, lang, namespace):
    """Clean title.

    This method will remove namespace prefixes and replace spaces with
    underscores.

    :param title:   The title to strip
    :type title:    string

    :param lang:    Language code
    :type lang:     string

    :param namespace:   The namespace to strip
    :type namespace:    int
    """
    return wikify(strip_namespace(title, lang, namespace))
