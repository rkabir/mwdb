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
from __future__ import with_statement

import glob
import json
import logging
import sys
import os

from . import build_info

_log = logging.getLogger(__name__)

canonical_namespaces = {
    -2: 'Media',
    -1: 'Special',
    0: '',
    1: 'Talk',
    2: 'User',
    3: 'User talk',
    4: 'Project',
    5: 'Project talk',
    6: 'File',
    7: 'File talk',
    8: 'MediaWiki',
    9: 'MediaWiki talk',
    10: 'Template',
    11: 'Template talk',
    12: 'Help',
    13: 'Help talk',
    14: 'category',
    15: 'Category talk',
    100: 'Portal',
    101: 'Portal talk',
}


class SiteInformation(object):
    """Information about wikipedia sites.

    This class provides access to information about Wikipedia sites, such as
    their URL or namespace names.

    :ivar languages:    Set of known Wikipedia languages
    :type languages:    set

    :ivar namespace_names:  Dictionary containing list of namespace names for
                            all known languages
    :type namespace_names:  dict

    :ivar _only_canonical:  Boolean. If true only information on canonical
                            namespaces is available.
    :type _only_canonical:  bool
    """

    def __init__(self):
        """Constructor"""
        self.languages = set([])
        self._namespace_names = {}
        self._read_information()

    def _read_information(self):
        """Read information from siteinfo json files"""

        for fp_path in glob.iglob(os.path.join(build_info.DATA_DIR, 'mwdb',
                                               'siteinfo' '*.json')):
            _log.debug('Reading site information from: {0}'.format(fp_path))
            try:
                with open(fp_path) as fp:
                    siteinfo = json.load(fp)['query']
                    lang = siteinfo['general']['lang']
                    self.languages.add(lang)
                    self._load_namespaces(siteinfo)
            except (IOError, KeyError), err:
                _log.error('Could not read {0}: {1}'.format(
                    os.path.basename(fp_path), err))
                continue

    def _load_namespaces(self, siteinfo):
        """Load namespace information

        :param siteinfo:    Dictionary from siteinfo json file
        :type siteinfo:     dict
        """
        lang = siteinfo['general']['lang']
        lang_ns = {}

        for ns_dict in siteinfo['namespaces'].itervalues():
            ns_id = ns_dict['id']
            if '*' in ns_dict:
                lang_ns.setdefault(ns_id, set([])).add(ns_dict['*'])

            if 'canonical' in ns_dict:
                lang_ns.setdefault(ns_id, set([])).add(
                    ns_dict['canonical'])
            else:
                lang_ns.setdefault(ns_id, set([])).add(
                    canonical_namespaces[ns_id])

        for alias_dict in siteinfo['namespacealiases']:
            lang_ns.setdefault(alias_dict['id'], set([])).add(alias_dict['*'])

        self._namespace_names[lang] = lang_ns

    def get_namespace_names(self, lang, namespace):
        """Get namespace names.

        This method will return all known namespace names for given language
        and namespace. If the namespace names could not be read due to missing
        json files for that language only the canonical namespace are
        returned.

        :param lang:    Language code
        :type lang:     string

        :param namespace:   Namespace number
        :type namespace:    int
        """
        try:
            return self._namespace_names[lang][namespace]
        except KeyError, k_err:
            _log.warning('No namespace information available for' \
                       'language: {0}'.format(lang))
            return canonical_namespaces[namespace]

siteinfo = SiteInformation()
