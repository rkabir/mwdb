# -*- coding: UTF-8 -*-

# © Copyright 2009 Wolodja Wentland and Johannes Knopp.  All Rights Reserved.

# This file is part of mwdb.
#
# mwdb is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# mwdb is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.  You should have received a copy of the GNU General Public License
# along with mwdb. If not, see <http://www.gnu.org/licenses/>.

from sqlalchemy import *
from sqlalchemy.orm import *

metadata = MetaData()

ar_t = Table(u'archive', metadata,
             Column(u'ar_namespace', Integer, nullable=False, server_default='0'),
             Column(u'ar_title', Unicode(255)),
             Column(u'ar_text', Binary, nullable=False),
             Column(u'ar_comment', UnicodeText, nullable=False),
             Column(u'ar_user', Integer, nullable=False, server_default='0'),
             Column(u'ar_user_text', Unicode(255)),
             Column(u'ar_timestamp', Unicode(14), nullable=False,
                    server_default=''),
             Column(u'ar_minor_edit', SmallInteger, nullable=False,
                    server_default='0'),
             Column(u'ar_flags', Unicode(6), nullable=False),
             Column(u'ar_rev_id', Integer),
             Column(u'ar_text_id', Integer, ForeignKey('text.old_id')),
             Column(u'ar_deleted', SmallInteger, nullable=False, server_default='0'),
             Column(u'ar_len', Integer),
             Column(u'ar_page_id', Integer),
             Column(u'ar_parent_id', Integer))

cat_t = Table(u'category', metadata,
     Column(u'cat_id', Integer, primary_key=True, nullable=False),
     Column(u'cat_title', Unicode),
     Column(u'cat_pages', Integer(11), nullable=False, server_default='0'),
     Column(u'cat_subcats', Integer(11), nullable=False, server_default='0'),
     Column(u'cat_files', Integer(11), nullable=False, server_default='0'),
     Column(u'cat_hidden', SmallInteger(3), nullable=False,
            server_default='0'))

cl_t = Table(u'categorylinks', metadata,
             # FK: cl_from -> page.page_id
             Column(u'cl_from', Integer, nullable=False, server_default='0'),
             Column(u'cl_to', Unicode(255)),
             Column(u'cl_sortkey', Unicode(70)),
             Column(u'cl_timestamp', TIMESTAMP(timezone=False),
                    nullable=False, server_default=None))

ct_t = Table(u'change_tag', metadata,
             Column(u'ct_rc_id', Integer),
             Column(u'ct_log_id', Integer),
             Column(u'ct_rev_id', Integer),
             Column(u'ct_tag', Unicode(255), nullable=False),
             Column(u'ct_params', Binary))

el_t = Table(u'externallinks', metadata,
             Column(u'el_from', Integer(8), nullable=False,
                    server_default='0'),
             Column(u'el_to', Unicode, nullable=False),
             Column(u'el_index', Unicode, nullable=False))


fa_t = Table(u'filearchive', metadata,
             Column(u'fa_id', Integer(11), primary_key=True, nullable=False),
             Column(u'fa_name', Unicode(255)),
             Column(u'fa_archive_name', Unicode(255)),
             Column(u'fa_storage_group', Binary(16)),
             Column(u'fa_storage_key', Unicode(64), server_default=u''),
             Column(u'fa_deleted_user', Integer(11)),
             Column(u'fa_deleted_timestamp', Unicode(14), server_default=u''),
             Column(u'fa_deleted_reason', UnicodeText),
             Column(u'fa_size', Integer(8), server_default='0'),
             Column(u'fa_width', Integer, server_default='0'),
             Column(u'fa_height', Integer, server_default='0'),
             Column(u'fa_metadata', Unicode),
             Column(u'fa_bits', Integer, server_default='0'),
             # XXX: these were ENUMs, change that once implemented!
             Column(u'fa_media_type', Unicode(20)),
             Column(u'fa_major_mime', Unicode(20), server_default=u''),
             Column(u'fa_minor_mime', Unicode(32), server_default=u'unknown'),
             Column(u'fa_description', Unicode),
             Column(u'fa_user', Integer, server_default='0'),
             Column(u'fa_user_text', Unicode(255)),
             Column(u'fa_timestamp', Unicode(14), server_default=''),
             Column(u'fa_deleted', SmallInteger, nullable=False,
                    server_default='0'))

## TODO: defined with engine HEAP #Table(u'hitcounter', metadata,
      #Column(u'hc_id', Integer, #nullable=False), #)

img_t = Table(u'image', metadata,
              Column(u'img_name', Unicode(255), primary_key=True),
              Column(u'img_size', Integer, nullable=False),
              Column(u'img_width', Integer, nullable=False),
              Column(u'img_height', Integer, nullable=False),
              Column(u'img_metadata', UnicodeText, nullable=False),
              Column(u'img_bits', Integer, nullable=False,
                     server_default='0'),
              Column(u'img_media_type', Unicode(16), server_default=None),
              Column(u'img_major_mime', Unicode(16), nullable=False,
                     server_default='unknown'),
              Column(u'img_minor_mime', Unicode(32), nullable=False,
                     server_default='unknown'),
              Column(u'img_description', UnicodeText, nullable=False),
              Column(u'img_user', Integer, nullable=False,
                     server_default='0'),
              Column(u'img_user_text', Unicode(255)),
              Column(u'img_timestamp', Unicode(14), nullable=False,
                     server_default=''),
              Column(u'img_sha1', Unicode(32), nullable=False,
                     server_default=''))

il_t = Table(u'imagelinks', metadata,
             # FK: il_from -> page.page_id
             Column(u'il_from', Integer, nullable=False, server_default='0'),
             Column(u'il_to', Unicode))

iw_t = Table(u'interwiki', metadata,
             Column(u'iw_prefix', Unicode(32), nullable=False),
             Column(u'iw_url', Unicode, nullable=False),
             Column(u'iw_local', Boolean, nullable=False),
             Column(u'iw_trans', SmallInteger, nullable=False,
                    server_default='0'))

ipb_t = Table(u'ipblocks', metadata,
              Column(u'ipb_id', Integer, primary_key=True, nullable=False),
              Column(u'ipb_address', Unicode, nullable=False),
              Column(u'ipb_user', Integer, nullable=False,
                     server_default='0'),
              Column(u'ipb_by', Integer, nullable=False, server_default='0'),
              Column(u'ipb_by_text', Unicode(255)),
              Column(u'ipb_reason', UnicodeText, nullable=False),
              Column(u'ipb_timestamp', Unicode(14), nullable=False,
                     server_default=''),
              Column(u'ipb_auto', Boolean, nullable=False,
                     server_default='False'),
              Column(u'ipb_anon_only', Boolean, nullable=False,
                     server_default='False'),
              Column(u'ipb_create_account', Boolean, nullable=False,
                     server_default='True'),
              Column(u'ipb_enable_autoblock', Boolean, nullable=False,
                     server_default='True'),
              Column(u'ipb_expiry', Unicode(14), nullable=False,
                     server_default=''),
              Column(u'ipb_range_start', Unicode, nullable=False),
              Column(u'ipb_range_end', Unicode, nullable=False),
              Column(u'ipb_deleted', Boolean, nullable=False,
                     server_default='False'),
              Column(u'ipb_block_email', Boolean, nullable=False,
                     server_default='False'),
              Column(u'ipb_allow_usertalk', Boolean, nullable=False,
                     server_default='False'))

job_t = Table(u'job', metadata,
              Column(u'job_id', SmallInteger, primary_key=True,
                     nullable=False),
              Column(u'job_cmd', Unicode(60), nullable=False,
                     server_default=u''),
              Column(u'job_namespace', Integer, nullable=False),
              Column(u'job_title', Unicode(255)),
              Column(u'job_params', Unicode, nullable=False))

ll_t = Table(u'langlinks', metadata,
             # FK: ll_from -> page.page_id
             Column(u'll_from', Integer, nullable=False, server_default='0',
                    primary_key=True),
             Column(u'll_lang', Binary(20), nullable=False,
                    server_default=''),
             Column(u'll_title', Unicode(255), nullable=False,
                    server_default=''))

log_t = Table(u'logging', metadata,
              Column(u'log_id', Integer, primary_key=True, nullable=False),
              Column(u'log_type', Unicode(10), nullable=False,
                     server_default=u''),
              Column(u'log_action', Unicode(10), nullable=False,
                     server_default=u''),
              Column(u'log_timestamp', Unicode(14), nullable=False,
                     server_default=u'19700101000000'),
              # FK: log_user -> user.user_id
              Column(u'log_user', Integer, nullable=False,
                     server_default='0'),
              Column(u'log_namespace', Integer, nullable=False,
                     server_default='0'),
              Column(u'log_title', Unicode(255)),
              Column(u'log_comment', Unicode(255), nullable=False,
                     server_default=u''),
              Column(u'log_params', Unicode, nullable=False),
              Column(u'log_deleted', SmallInteger, nullable=False,
                     server_default='0'))


math_t = Table(u'math', metadata,
               Column(u'math_inputhash', Binary(16), nullable=False),
               Column(u'math_outputhash', Binary(16), nullable=False),
               Column(u'math_html_conservativeness', SmallInteger,
                      nullable=False),
               Column(u'math_html', UnicodeText),
               Column(u'math_mathml', UnicodeText))

#objc_t = Table(u'objectcache', metadata,
               #Column(u'keyname', Unicode(255), #primary_key=True, #),
               #Column(u'value', Binary(None)),
               #Column(u'exptime', DATETIME(timezone=False)),
              #)


oi_t = Table(u'oldimage', metadata,
             Column(u'oi_name', Unicode(255)),
             Column(u'oi_archive_name', Unicode(255)),
             Column(u'oi_size', Integer, nullable=False, server_default='0'),
             Column(u'oi_width', Integer, nullable=False, server_default='0'),
             Column(u'oi_height', Integer, nullable=False,
                    server_default='0'),
             Column(u'oi_bits', Integer, nullable=False, server_default='0'),
             Column(u'oi_description', Unicode, nullable=False),
             Column(u'oi_user', Integer, nullable=False, server_default='0'),
             Column(u'oi_user_text', Unicode(255)),
             Column(u'oi_timestamp', Unicode(14), nullable=False,
                    server_default=''),
             Column(u'oi_metadata', Unicode, nullable=False),
             # XXX: ENUM here!! for psql?
             Column(u'oi_media_type', Unicode),
             Column(u'oi_major_mime', Unicode(16), nullable=False,
                    server_default='unknown'),
             Column(u'oi_minor_mime', Unicode(32), nullable=False,
                    server_default=u'unknown'),
             Column(u'oi_deleted', SmallInteger, nullable=False,
                    server_default='0'),
             Column(u'oi_sha1', Unicode(32), nullable=False,
                    server_default=u''))

page_t = Table(u'page', metadata,
               Column(u'page_id', Integer, primary_key=True, nullable=False),
               Column(u'page_namespace', Integer),
               Column(u'page_title', Unicode(255), nullable=False),
               Column(u'page_restrictions', Unicode, nullable=False),
               Column(u'page_counter', Integer, nullable=True,
                      server_default='0'),
               Column(u'page_is_redirect', SmallInteger, nullable=False,
                      server_default='0'),
               Column(u'page_is_new', SmallInteger, nullable=False,
                      server_default='0'),
               Column(u'page_random', Float, nullable=False),
               Column(u'page_touched', Unicode(14), nullable=False,
                      server_default=u''),
               Column(u'page_latest', Integer, nullable=False),
               Column(u'page_len', Integer, nullable=False))

pl_t = Table(u'pagelinks', metadata,
             # FK: pl_from -> page.page_id
             Column(u'pl_from', Integer, nullable=False, server_default='0',
                    primary_key=True),
             Column(u'pl_namespace', Integer, nullable=False,
                    server_default='0'),
             Column(u'pl_title', Unicode))

pr_t = Table(u'page_restrictions', metadata,
             # FK: pr_page -> page.page_id
             Column(u'pr_page', Integer, nullable=False),
             Column(u'pr_type', Binary(60), nullable=False),
             Column(u'pr_level', Binary(60), nullable=False),
             Column(u'pr_cascade', SmallInteger, nullable=False),
             Column(u'pr_user', Integer),
             Column(u'pr_expiry', Binary(14)),
             Column(u'pr_id', Integer, primary_key=True, nullable=False))

pt_t = Table(u'protected_titles', metadata,
             Column(u'pt_namespace', Integer, nullable=False),
             Column(u'pt_title', Unicode(255)),
             Column(u'pt_user', Integer, nullable=False),
             Column(u'pt_reason', Unicode),
             Column(u'pt_timestamp', Unicode(14), nullable=False),
             Column(u'pt_expiry', Unicode(14), nullable=False,
                    server_default=u''),
             Column(u'pt_create_perm', Binary(60), nullable=False))


qc_t = Table(u'querycache', metadata,
             Column(u'qc_type', Binary(32), nullable=False),
             Column(u'qc_value', Integer, nullable=False, server_default='0'),
             Column(u'qc_namespace', Integer, nullable=False,
                    server_default='0'),
             Column(u'qc_title', Unicode(255)))

qcc_t = Table(u'querycachetwo', metadata,
              Column(u'qcc_type', Unicode(32), nullable=False),
              Column(u'qcc_value', Integer, nullable=False,
                     server_default='0'),
              Column(u'qcc_namespace', Integer, nullable=False,
                     server_default='0'),
              Column(u'qcc_title', Unicode(255)),
              Column(u'qcc_namespacetwo', Integer, nullable=False,
                     server_default='0'),
              Column(u'qcc_titletwo', Unicode(255)))

qci_t = Table(u'querycache_info', metadata,
              Column(u'qci_type', Unicode(32), nullable=False,
                     server_default=''),
              Column(u'qci_timestamp', Unicode(14), nullable=False,
                     server_default='19700101000000'))

rc_t = Table(u'recentchanges', metadata,
             Column(u'rc_id', Integer, primary_key=True, nullable=False),
             Column(u'rc_timestamp', Unicode(14), nullable=False,
                    server_default=u''),
             Column(u'rc_cur_time', Unicode(14), nullable=False,
                    server_default=u''),
             # FK: rc_user -> user.user_id
             Column(u'rc_user', Integer, nullable=False, server_default='0'),
             Column(u'rc_user_text', Unicode(255)),
             Column(u'rc_namespace', Integer, nullable=False,
                    server_default='0'),
             Column(u'rc_title', Unicode(255)),
             Column(u'rc_comment', Unicode(255)),
             Column(u'rc_minor', SmallInteger, nullable=False,
                    server_default='0'),
             Column(u'rc_bot', SmallInteger, nullable=False,
                    server_default='0'),
             Column(u'rc_new', SmallInteger, nullable=False,
                    server_default='0'),
             # FK: rc_cur_id -> page.page_id
             Column(u'rc_cur_id', Integer, nullable=False,
                    server_default='0'),
             # FK: rc_this_oldid -> revision.rev_id
             Column(u'rc_this_oldid', Integer, nullable=False,
                    server_default='0'),
             # FK: rc_this_oldid -> revision.rev_id
             Column(u'rc_last_oldid', Integer, nullable=False,
                    server_default='0'),
             Column(u'rc_type', SmallInteger, nullable=False,
                    server_default='0'),
             Column(u'rc_moved_to_ns', SmallInteger, nullable=False,
                    server_default='0'),
             Column(u'rc_moved_to_title', Unicode(255)),
             Column(u'rc_patrolled', SmallInteger, nullable=False,
                    server_default='0'),
             Column(u'rc_ip', Unicode(40), nullable=False,
                    server_default=u''),
             Column(u'rc_old_len', Integer),
             Column(u'rc_new_len', Integer),
             Column(u'rc_deleted', SmallInteger, nullable=False,
                    server_default='0'),
             Column(u'rc_logid', Integer, nullable=False, server_default='0'),
             Column(u'rc_log_type', Unicode(255)),
             Column(u'rc_log_action', Unicode(255)),
             Column(u'rc_params', Binary))

rd_t = Table(u'redirect', metadata,
             # FK: rd_from -> page.page_id
             Column(u'rd_from', Integer, primary_key=True, nullable=False,
                    server_default='0'),
             Column(u'rd_namespace', Integer, nullable=False,
                    server_default='0'),
             Column(u'rd_title', Unicode(255)))

rev_t = Table(u'revision', metadata,
              Column(u'rev_id', Integer, primary_key=True, nullable=False),
              # FK: rev_page -> page.page_id
              Column(u'rev_page', Integer, nullable=False),
              # FK: rev_text_id -> text.old_id
              Column(u'rev_text_id', Integer, nullable=False),
              Column(u'rev_comment', Unicode(255), nullable=False),
              # FK: rev_user -> user.user_id
              Column(u'rev_user', Integer, nullable=False,
                     server_default='0'),
              Column(u'rev_user_text', Unicode(255)),
              Column(u'rev_timestamp', Unicode(14), nullable=False,
                     server_default=''),
              Column(u'rev_minor_edit', SmallInteger, nullable=False,
                     server_default='0'),
              Column(u'rev_deleted', SmallInteger, nullable=False,
                     server_default='0'),
              Column(u'rev_len', Integer),
              Column(u'rev_parent_id', Integer))

si_t = Table(u'searchindex', metadata,
             Column(u'si_page', Integer, nullable=False),
             Column(u'si_title', Unicode(255), nullable=False,
                    server_default=u''),
             Column(u'si_text', UnicodeText, nullable=False))

ss_t = Table(u'site_stats', metadata,
             Column(u'ss_row_id', Integer, nullable=False),
             Column(u'ss_total_views', Integer, server_default='0'),
             Column(u'ss_total_edits', Integer, server_default='0'),
             Column(u'ss_good_articles', Integer, server_default='0'),
             Column(u'ss_total_pages', Integer, server_default='-1'),
             Column(u'ss_users', Integer, server_default='-1'),
             Column(u'ss_active_users', Integer, server_default='-1'),
             Column(u'ss_admins', Integer, server_default='-1'),
             Column(u'ss_images', Integer, server_default='0'))

ts_t = Table(u'tag_summary', metadata,
             Column(u'ts_rc_id', Integer),
             Column(u'ts_log_id', Integer),
             Column(u'ts_rev_id', Integer),
             Column(u'ts_tags', Unicode, nullable=False))

tl_t = Table(u'templatelinks', metadata,
             # FK: tl_from -> page.page_id
             Column(u'tl_from', Integer, nullable=False, server_default='0'),
             Column(u'tl_namespace', Integer, nullable=False,
                    server_default='0'),
             Column(u'tl_title', Unicode(255)))

text_t = Table(u'text', metadata,
               Column(u'old_id', Integer, primary_key=True, nullable=False),
               Column(u'old_text', UnicodeText, nullable=False),
               Column(u'old_flags', Unicode, nullable=False))

tb_t = Table(u'trackbacks', metadata,
             Column(u'tb_id', Integer, primary_key=True, nullable=False),
             # FK: tb_page -> page.page_id
             Column(u'tb_page', Integer),
             Column(u'tb_title', Unicode(255), nullable=False),
             Column(u'tb_url', Unicode, nullable=False),
             Column(u'tb_ex', UnicodeText),
             Column(u'tb_name', Unicode(255)))

Table(u'transcache', metadata,
      Column(u'tc_url', Unicode(255), nullable=False),
      Column(u'tc_contents', UnicodeText),
      Column(u'tc_time', Integer(11), nullable=False))

ul_t = Table(u'updatelog', metadata,
             Column(u'ul_key', Unicode(255), primary_key=True,
                    nullable=False))

user_t = Table(u'user', metadata,
               Column(u'user_id', Integer, primary_key=True, nullable=False),
               Column(u'user_name', Unicode(255)),
               Column(u'user_real_name', Unicode(255)),
               Column(u'user_password', Unicode, nullable=False),
               Column(u'user_newpassword', Unicode, nullable=False),
               Column(u'user_newpass_time', Unicode(14)),
               Column(u'user_email', Unicode, nullable=False),
               Column(u'user_options', Unicode, nullable=False),
               Column(u'user_touched', Unicode(14), nullable=False,
                      server_default=u''),
               Column(u'user_token', Unicode(32), nullable=False,
                      server_default=u''),
               Column(u'user_email_authenticated', Unicode(14)),
               Column(u'user_email_token', Unicode(32)),
               Column(u'user_email_token_expires', Unicode(14)),
               Column(u'user_registration', Unicode(14)),
               Column(u'user_editcount', Integer))

ug_t = Table(u'user_groups', metadata,
             # FK: ug_user -> user.user_id
             Column(u'ug_user', Integer, nullable=False, server_default='0'),
             Column(u'ug_group', Unicode(16), nullable=False,
                    server_default=''))

usertalk_t = Table(u'user_newtalk', metadata,
                   Column(u'user_id', Integer, nullable=False,
                          server_default='0'),
                   Column(u'user_ip', Unicode(40), nullable=False,
                          server_default=''),
                   Column(u'user_last_timestamp', Unicode(14), nullable=False,
                          server_default=''))

vt_t = Table(u'valid_tag', metadata,
             Column(u'vt_tag', Unicode(255), primary_key=True,
                    nullable=False))

wl_t = Table(u'watchlist', metadata,
             Column(u'wl_user', Integer, nullable=False),
             Column(u'wl_namespace', Integer, nullable=False,
                    server_default='0'),
             Column(u'wl_title', Unicode(255)),
             Column(u'wl_notificationtimestamp', Unicode(14)))

pp_t = Table(u'page_props', metadata,
             Column(u'pp_page', Integer, nullable=False),
             Column(u'pp_propname', Unicode(60), nullable=False),
             Column(u'pp_value',Binary, nullable=False))

tables = [obj for obj in locals().values() if isinstance(obj, Table)]
