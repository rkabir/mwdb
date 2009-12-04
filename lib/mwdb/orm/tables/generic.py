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

from __future__ import unicode_literals

from sqlalchemy import *
from sqlalchemy.orm import *

metadata = MetaData()

ar_t = Table('archive', metadata,
             Column('ar_namespace', Integer, nullable=False,
                    server_default='0'),
             Column('ar_title', Unicode(255)),
             Column('ar_text', Binary, nullable=False),
             Column('ar_comment', UnicodeText, nullable=False),
             Column('ar_user', Integer, nullable=False, server_default='0'),
             Column('ar_user_text', Unicode(255)),
             Column('ar_timestamp', Unicode(14), nullable=False,
                    server_default=''),
             Column('ar_minor_edit', SmallInteger, nullable=False,
                    server_default='0'),
             Column('ar_flags', Unicode(6), nullable=False),
             Column('ar_rev_id', Integer),
             Column('ar_text_id', Integer, ForeignKey('text.old_id')),
             Column('ar_deleted', SmallInteger, nullable=False,
                    server_default='0'),
             Column('ar_len', Integer),
             Column('ar_page_id', Integer),
             Column('ar_parent_id', Integer))

cat_t = Table('category', metadata,
              Column('cat_id', Integer, primary_key=True, nullable=False),
              Column('cat_title', Unicode),
              Column('cat_pages', Integer(11), nullable=False,
                     server_default='0'),
              Column('cat_subcats', Integer(11), nullable=False,
                     server_default='0'),
              Column('cat_files', Integer(11), nullable=False,
                     server_default='0'),
              Column('cat_hidden', SmallInteger(3), nullable=False,
                     server_default='0'))

cl_t = Table('categorylinks', metadata,
             # FK: cl_from -> page.page_id
             Column('cl_from', Integer, nullable=False, server_default='0'),
             Column('cl_to', Unicode(255)),
             Column('cl_sortkey', Unicode(70)),
             Column('cl_timestamp', TIMESTAMP(timezone=False),
                    nullable=False, server_default=None))

ct_t = Table('change_tag', metadata,
             Column('ct_rc_id', Integer),
             Column('ct_log_id', Integer),
             Column('ct_rev_id', Integer),
             Column('ct_tag', Unicode(255), nullable=False),
             Column('ct_params', Binary))

el_t = Table('externallinks', metadata,
             Column('el_from', Integer(8), nullable=False,
                    server_default='0'),
             Column('el_to', Unicode, nullable=False),
             Column('el_index', Unicode, nullable=False))


fa_t = Table('filearchive', metadata,
             Column('fa_id', Integer(11), primary_key=True, nullable=False),
             Column('fa_name', Unicode(255)),
             Column('fa_archive_name', Unicode(255)),
             Column('fa_storage_group', Binary(16)),
             Column('fa_storage_key', Unicode(64), server_default=''),
             Column('fa_deleted_user', Integer(11)),
             Column('fa_deleted_timestamp', Unicode(14), server_default=''),
             Column('fa_deleted_reason', UnicodeText),
             Column('fa_size', Integer(8), server_default='0'),
             Column('fa_width', Integer, server_default='0'),
             Column('fa_height', Integer, server_default='0'),
             Column('fa_metadata', Unicode),
             Column('fa_bits', Integer, server_default='0'),
             # XXX: these were ENUMs, change that once implemented!
             Column('fa_media_type', Unicode(20)),
             Column('fa_major_mime', Unicode(20), server_default=''),
             Column('fa_minor_mime', Unicode(32), server_default='unknown'),
             Column('fa_description', Unicode),
             Column('fa_user', Integer, server_default='0'),
             Column('fa_user_text', Unicode(255)),
             Column('fa_timestamp', Unicode(14), server_default=''),
             Column('fa_deleted', SmallInteger, nullable=False,
                    server_default='0'))

## TODO: defined with engine HEAP #Table('hitcounter', metadata,
      #Column('hc_id', Integer, #nullable=False), #)

img_t = Table('image', metadata,
              Column('img_name', Unicode(255), primary_key=True),
              Column('img_size', Integer, nullable=False),
              Column('img_width', Integer, nullable=False),
              Column('img_height', Integer, nullable=False),
              Column('img_metadata', UnicodeText, nullable=False),
              Column('img_bits', Integer, nullable=False,
                     server_default='0'),
              Column('img_media_type', Unicode(16), server_default=None),
              Column('img_major_mime', Unicode(16), nullable=False,
                     server_default='unknown'),
              Column('img_minor_mime', Unicode(32), nullable=False,
                     server_default='unknown'),
              Column('img_description', UnicodeText, nullable=False),
              Column('img_user', Integer, nullable=False,
                     server_default='0'),
              Column('img_user_text', Unicode(255)),
              Column('img_timestamp', Unicode(14), nullable=False,
                     server_default=''),
              Column('img_sha1', Unicode(32), nullable=False,
                     server_default=''))

il_t = Table('imagelinks', metadata,
             # FK: il_from -> page.page_id
             Column('il_from', Integer, nullable=False, server_default='0'),
             Column('il_to', Unicode))

iw_t = Table('interwiki', metadata,
             Column('iw_prefix', Unicode(32), nullable=False),
             Column('iw_url', Unicode, nullable=False),
             Column('iw_local', Boolean, nullable=False),
             Column('iw_trans', SmallInteger, nullable=False,
                    server_default='0'))

ipb_t = Table('ipblocks', metadata,
              Column('ipb_id', Integer, primary_key=True, nullable=False),
              Column('ipb_address', Unicode, nullable=False),
              Column('ipb_user', Integer, nullable=False,
                     server_default='0'),
              Column('ipb_by', Integer, nullable=False, server_default='0'),
              Column('ipb_by_text', Unicode(255)),
              Column('ipb_reason', UnicodeText, nullable=False),
              Column('ipb_timestamp', Unicode(14), nullable=False,
                     server_default=''),
              Column('ipb_auto', Boolean, nullable=False,
                     server_default='False'),
              Column('ipb_anon_only', Boolean, nullable=False,
                     server_default='False'),
              Column('ipb_create_account', Boolean, nullable=False,
                     server_default='True'),
              Column('ipb_enable_autoblock', Boolean, nullable=False,
                     server_default='True'),
              Column('ipb_expiry', Unicode(14), nullable=False,
                     server_default=''),
              Column('ipb_range_start', Unicode, nullable=False),
              Column('ipb_range_end', Unicode, nullable=False),
              Column('ipb_deleted', Boolean, nullable=False,
                     server_default='False'),
              Column('ipb_block_email', Boolean, nullable=False,
                     server_default='False'),
              Column('ipb_allow_usertalk', Boolean, nullable=False,
                     server_default='False'))

job_t = Table('job', metadata,
              Column('job_id', SmallInteger, primary_key=True,
                     nullable=False),
              Column('job_cmd', Unicode(60), nullable=False,
                     server_default=''),
              Column('job_namespace', Integer, nullable=False),
              Column('job_title', Unicode(255)),
              Column('job_params', Unicode, nullable=False))

ll_t = Table('langlinks', metadata,
             # FK: ll_from -> page.page_id
             Column('ll_from', Integer, nullable=False, server_default='0',
                    primary_key=True),
             Column('ll_lang', Binary(20), nullable=False,
                    server_default=''),
             Column('ll_title', Unicode(255), nullable=False,
                    server_default=''))

log_t = Table('logging', metadata,
              Column('log_id', Integer, primary_key=True, nullable=False),
              Column('log_type', Unicode(10), nullable=False,
                     server_default=''),
              Column('log_action', Unicode(10), nullable=False,
                     server_default=''),
              Column('log_timestamp', Unicode(14), nullable=False,
                     server_default='19700101000000'),
              # FK: log_user -> user.user_id
              Column('log_user', Integer, nullable=False,
                     server_default='0'),
              Column('log_namespace', Integer, nullable=False,
                     server_default='0'),
              Column('log_title', Unicode(255)),
              Column('log_comment', Unicode(255), nullable=False,
                     server_default=''),
              Column('log_params', Unicode, nullable=False),
              Column('log_deleted', SmallInteger, nullable=False,
                     server_default='0'))


math_t = Table('math', metadata,
               Column('math_inputhash', Binary(16), nullable=False),
               Column('math_outputhash', Binary(16), nullable=False),
               Column('math_html_conservativeness', SmallInteger,
                      nullable=False),
               Column('math_html', UnicodeText),
               Column('math_mathml', UnicodeText))

#objc_t = Table('objectcache', metadata,
               #Column('keyname', Unicode(255), #primary_key=True, #),
               #Column('value', Binary(None)),
               #Column('exptime', DATETIME(timezone=False)),
              #)


oi_t = Table('oldimage', metadata,
             Column('oi_name', Unicode(255)),
             Column('oi_archive_name', Unicode(255)),
             Column('oi_size', Integer, nullable=False, server_default='0'),
             Column('oi_width', Integer, nullable=False, server_default='0'),
             Column('oi_height', Integer, nullable=False,
                    server_default='0'),
             Column('oi_bits', Integer, nullable=False, server_default='0'),
             Column('oi_description', Unicode, nullable=False),
             Column('oi_user', Integer, nullable=False, server_default='0'),
             Column('oi_user_text', Unicode(255)),
             Column('oi_timestamp', Unicode(14), nullable=False,
                    server_default=''),
             Column('oi_metadata', Unicode, nullable=False),
             # XXX: ENUM here!! for psql?
             Column('oi_media_type', Unicode),
             Column('oi_major_mime', Unicode(16), nullable=False,
                    server_default='unknown'),
             Column('oi_minor_mime', Unicode(32), nullable=False,
                    server_default='unknown'),
             Column('oi_deleted', SmallInteger, nullable=False,
                    server_default='0'),
             Column('oi_sha1', Unicode(32), nullable=False,
                    server_default=''))

page_t = Table('page', metadata,
               Column('page_id', Integer, primary_key=True, nullable=False),
               Column('page_namespace', Integer),
               Column('page_title', Unicode(255), nullable=False),
               Column('page_restrictions', Unicode, nullable=False),
               Column('page_counter', Integer, nullable=True,
                      server_default='0'),
               Column('page_is_redirect', SmallInteger, nullable=False,
                      server_default='0'),
               Column('page_is_new', SmallInteger, nullable=False,
                      server_default='0'),
               Column('page_random', Float, nullable=False),
               Column('page_touched', Unicode(14), nullable=False,
                      server_default=''),
               Column('page_latest', Integer, nullable=False),
               Column('page_len', Integer, nullable=False))

pl_t = Table('pagelinks', metadata,
             # FK: pl_from -> page.page_id
             Column('pl_from', Integer, nullable=False, server_default='0',
                    primary_key=True),
             Column('pl_namespace', Integer, nullable=False,
                    server_default='0'),
             Column('pl_title', Unicode))

pr_t = Table('page_restrictions', metadata,
             # FK: pr_page -> page.page_id
             Column('pr_page', Integer, nullable=False),
             Column('pr_type', Binary(60), nullable=False),
             Column('pr_level', Binary(60), nullable=False),
             Column('pr_cascade', SmallInteger, nullable=False),
             Column('pr_user', Integer),
             Column('pr_expiry', Binary(14)),
             Column('pr_id', Integer, primary_key=True, nullable=False))

pt_t = Table('protected_titles', metadata,
             Column('pt_namespace', Integer, nullable=False),
             Column('pt_title', Unicode(255)),
             Column('pt_user', Integer, nullable=False),
             Column('pt_reason', Unicode),
             Column('pt_timestamp', Unicode(14), nullable=False),
             Column('pt_expiry', Unicode(14), nullable=False,
                    server_default=''),
             Column('pt_create_perm', Binary(60), nullable=False))


qc_t = Table('querycache', metadata,
             Column('qc_type', Binary(32), nullable=False),
             Column('qc_value', Integer, nullable=False, server_default='0'),
             Column('qc_namespace', Integer, nullable=False,
                    server_default='0'),
             Column('qc_title', Unicode(255)))

qcc_t = Table('querycachetwo', metadata,
              Column('qcc_type', Unicode(32), nullable=False),
              Column('qcc_value', Integer, nullable=False,
                     server_default='0'),
              Column('qcc_namespace', Integer, nullable=False,
                     server_default='0'),
              Column('qcc_title', Unicode(255)),
              Column('qcc_namespacetwo', Integer, nullable=False,
                     server_default='0'),
              Column('qcc_titletwo', Unicode(255)))

qci_t = Table('querycache_info', metadata,
              Column('qci_type', Unicode(32), nullable=False,
                     server_default=''),
              Column('qci_timestamp', Unicode(14), nullable=False,
                     server_default='19700101000000'))

rc_t = Table('recentchanges', metadata,
             Column('rc_id', Integer, primary_key=True, nullable=False),
             Column('rc_timestamp', Unicode(14), nullable=False,
                    server_default=''),
             Column('rc_cur_time', Unicode(14), nullable=False,
                    server_default=''),
             # FK: rc_user -> user.user_id
             Column('rc_user', Integer, nullable=False, server_default='0'),
             Column('rc_user_text', Unicode(255)),
             Column('rc_namespace', Integer, nullable=False,
                    server_default='0'),
             Column('rc_title', Unicode(255)),
             Column('rc_comment', Unicode(255)),
             Column('rc_minor', SmallInteger, nullable=False,
                    server_default='0'),
             Column('rc_bot', SmallInteger, nullable=False,
                    server_default='0'),
             Column('rc_new', SmallInteger, nullable=False,
                    server_default='0'),
             # FK: rc_cur_id -> page.page_id
             Column('rc_cur_id', Integer, nullable=False,
                    server_default='0'),
             # FK: rc_this_oldid -> revision.rev_id
             Column('rc_this_oldid', Integer, nullable=False,
                    server_default='0'),
             # FK: rc_this_oldid -> revision.rev_id
             Column('rc_last_oldid', Integer, nullable=False,
                    server_default='0'),
             Column('rc_type', SmallInteger, nullable=False,
                    server_default='0'),
             Column('rc_moved_to_ns', SmallInteger, nullable=False,
                    server_default='0'),
             Column('rc_moved_to_title', Unicode(255)),
             Column('rc_patrolled', SmallInteger, nullable=False,
                    server_default='0'),
             Column('rc_ip', Unicode(40), nullable=False,
                    server_default=''),
             Column('rc_old_len', Integer),
             Column('rc_new_len', Integer),
             Column('rc_deleted', SmallInteger, nullable=False,
                    server_default='0'),
             Column('rc_logid', Integer, nullable=False, server_default='0'),
             Column('rc_log_type', Unicode(255)),
             Column('rc_log_action', Unicode(255)),
             Column('rc_params', Binary))

rd_t = Table('redirect', metadata,
             # FK: rd_from -> page.page_id
             Column('rd_from', Integer, primary_key=True, nullable=False,
                    server_default='0'),
             Column('rd_namespace', Integer, nullable=False,
                    server_default='0'),
             Column('rd_title', Unicode(255)))

rev_t = Table('revision', metadata,
              Column('rev_id', Integer, primary_key=True, nullable=False),
              # FK: rev_page -> page.page_id
              Column('rev_page', Integer, nullable=False),
              # FK: rev_text_id -> text.old_id
              Column('rev_text_id', Integer, nullable=False),
              Column('rev_comment', Unicode(255), nullable=False),
              # FK: rev_user -> user.user_id
              Column('rev_user', Integer, nullable=False,
                     server_default='0'),
              Column('rev_user_text', Unicode(255)),
              Column('rev_timestamp', Unicode(14), nullable=False,
                     server_default=''),
              Column('rev_minor_edit', SmallInteger, nullable=False,
                     server_default='0'),
              Column('rev_deleted', SmallInteger, nullable=False,
                     server_default='0'),
              Column('rev_len', Integer),
              Column('rev_parent_id', Integer))

si_t = Table('searchindex', metadata,
             Column('si_page', Integer, nullable=False),
             Column('si_title', Unicode(255), nullable=False,
                    server_default=''),
             Column('si_text', UnicodeText, nullable=False))

ss_t = Table('site_stats', metadata,
             Column('ss_row_id', Integer, nullable=False),
             Column('ss_total_views', Integer, server_default='0'),
             Column('ss_total_edits', Integer, server_default='0'),
             Column('ss_good_articles', Integer, server_default='0'),
             Column('ss_total_pages', Integer, server_default='-1'),
             Column('ss_users', Integer, server_default='-1'),
             Column('ss_active_users', Integer, server_default='-1'),
             Column('ss_admins', Integer, server_default='-1'),
             Column('ss_images', Integer, server_default='0'))

ts_t = Table('tag_summary', metadata,
             Column('ts_rc_id', Integer),
             Column('ts_log_id', Integer),
             Column('ts_rev_id', Integer),
             Column('ts_tags', Unicode, nullable=False))

tl_t = Table('templatelinks', metadata,
             # FK: tl_from -> page.page_id
             Column('tl_from', Integer, nullable=False, server_default='0'),
             Column('tl_namespace', Integer, nullable=False,
                    server_default='0'),
             Column('tl_title', Unicode(255)))

text_t = Table('text', metadata,
               Column('old_id', Integer, primary_key=True, nullable=False),
               Column('old_text', UnicodeText, nullable=False),
               Column('old_flags', Unicode, nullable=False))

tb_t = Table('trackbacks', metadata,
             Column('tb_id', Integer, primary_key=True, nullable=False),
             # FK: tb_page -> page.page_id
             Column('tb_page', Integer),
             Column('tb_title', Unicode(255), nullable=False),
             Column('tb_url', Unicode, nullable=False),
             Column('tb_ex', UnicodeText),
             Column('tb_name', Unicode(255)))

Table('transcache', metadata,
      Column('tc_url', Unicode(255), nullable=False),
      Column('tc_contents', UnicodeText),
      Column('tc_time', Integer(11), nullable=False))

ul_t = Table('updatelog', metadata,
             Column('ul_key', Unicode(255), primary_key=True,
                    nullable=False))

user_t = Table('user', metadata,
               Column('user_id', Integer, primary_key=True, nullable=False),
               Column('user_name', Unicode(255)),
               Column('user_real_name', Unicode(255)),
               Column('user_password', Unicode, nullable=False),
               Column('user_newpassword', Unicode, nullable=False),
               Column('user_newpass_time', Unicode(14)),
               Column('user_email', Unicode, nullable=False),
               Column('user_options', Unicode, nullable=False),
               Column('user_touched', Unicode(14), nullable=False,
                      server_default=''),
               Column('user_token', Unicode(32), nullable=False,
                      server_default=''),
               Column('user_email_authenticated', Unicode(14)),
               Column('user_email_token', Unicode(32)),
               Column('user_email_token_expires', Unicode(14)),
               Column('user_registration', Unicode(14)),
               Column('user_editcount', Integer))

ug_t = Table('user_groups', metadata,
             # FK: ug_user -> user.user_id
             Column('ug_user', Integer, nullable=False, server_default='0'),
             Column('ug_group', Unicode(16), nullable=False,
                    server_default=''))

usertalk_t = Table('user_newtalk', metadata,
                   Column('user_id', Integer, nullable=False,
                          server_default='0'),
                   Column('user_ip', Unicode(40), nullable=False,
                          server_default=''),
                   Column('user_last_timestamp', Unicode(14), nullable=False,
                          server_default=''))

vt_t = Table('valid_tag', metadata,
             Column('vt_tag', Unicode(255), primary_key=True,
                    nullable=False))

wl_t = Table('watchlist', metadata,
             Column('wl_user', Integer, nullable=False),
             Column('wl_namespace', Integer, nullable=False,
                    server_default='0'),
             Column('wl_title', Unicode(255)),
             Column('wl_notificationtimestamp', Unicode(14)))

pp_t = Table('page_props', metadata,
             Column('pp_page', Integer, nullable=False),
             Column('pp_propname', Unicode(60), nullable=False),
             Column('pp_value',Binary, nullable=False))

tables = [obj for obj in locals().values() if isinstance(obj, Table)]
