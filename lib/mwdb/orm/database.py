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

import datetime
import logging
import re

from contextlib import contextmanager

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.schema import AddConstraint, DropConstraint

from .. import exceptions
from . import mapper
from .tables import generic as generic_tables
from .tables import postgresql as postgresql_tables

try:
    import psycopg2.extensions as e
    ISOLATION_LEVEL_AUTOCOMMIT = e.ISOLATION_LEVEL_AUTOCOMMIT
    ISOLATION_LEVEL_READ_COMMITTED = e.ISOLATION_LEVEL_READ_COMMITTED
    ISOLATION_LEVEL_SERIALIZABLE = e.ISOLATION_LEVEL_SERIALIZABLE
    del e
except ImportError, imp_err:
    ISOLATION_LEVEL_AUTOCOMMIT = 0
    ISOLATION_LEVEL_READ_COMMITTED = 1
    ISOLATION_LEVEL_SERIALIZABLE = 2
_log = logging.getLogger(__name__)

__all__ = ['Databases', 'PostgreSQLDatabase', 'MySQLDatabase']


class Databases(dict):
    """Handler for multiple database connections.

    This class handles connections to wikipedia databases for multiple
    languages.
    """

    def __init__(self,
                 db_name_regex = r'(?u)wp_(?P<lang>\w+)_(?P<date>\d+)',
                 db_date_format = '%Y%m%d'):
        """Constructor.

        :param db_name_regex:   Regular expression that matches wikipedia
                                databases. It need a lang and a date group.
        :type db_name_regex:    string
        """

        super(Databases, self).__init__(self)

        self.date_format = db_date_format
        self.db_name_regex = db_name_regex

        self.pool_size = 0
        self.pool_recycle = 300

    @property
    def db_name_regex(self):
        return self._db_name_regex

    @db_name_regex.setter
    def db_name_regex(self, value):
        self._db_matcher = re.compile(value)
        self._db_name_regex = value

    @db_name_regex.deleter
    def db_name_regex(self):
        del self._db_matcher
        del self._db_name_regex

    @property
    def date_format(self):
        return self._date_format

    @date_format.setter
    def date_format(self, value):
        self._date_format = value

    @date_format.deleter
    def date_format(self):
        del self._date_format

    @property
    def pool_size(self):
        return self._pool_size

    @pool_size.setter
    def pool_size(self, value):
        self._pool_size = value

    @pool_size.deleter
    def pool_size(self):
        del self._pool_size

    @property
    def pool_recycle(self):
        return self._pool_recycle

    @pool_recycle.setter
    def pool_recycle(self, value):
        self._pool_recycle = value

    @pool_recycle.deleter
    def pool_recycle(self):
        del self._pool_recycle


    def _date_from_match(self, match):
        """Get a datetime object from a database match object

        Note that the given match object *must* provide the 'lang' group!
        """
        return datetime.datetime.strptime(match.group('date'),
                                          self.date_format)

    def _new_database(self, vendor, driver, user, password, host, name,
                      language):
        """Create a new database.

        This method creates a new database for given vendor
        """
        if 'postgresql' == vendor.lower():
            cls = PostgreSQLDatabase
        elif 'mysql' == vendor.lower():
            cls = MySQLDatabase
        else:
            raise ValueError('Unsupported vendor: {0}'.format(vendor))

        new_db = cls(driver, user, password, host, name, language)
        new_db.pool_size = self.pool_size
        new_db.pool_recycle = self.pool_recycle

        return new_db

    def _match_databases(self, db):
        """Get a dictionary of matching databases.

        This method scans the host the given database belongs to, searches for
        databases that match db_name_regex and returns a dictionary of the
        form:

            {
                'lang1': [match1, match2, ..., matchN],
                'lang2': [match1, match2, ..., matchN],
                ...
                'langN': [match1, match2, ..., matchN],
            }

        The given database object *must* implement all_databases!

        :param db:  A Database object
        :type db:   Subclass of mwdb.database.Database
        """
        databases = {}

        # match *all* database names against the regular expression for
        # wikipedia ones and save matches in the dictionary
        for t in db.all_databases():
            m = self._db_matcher.match(t)

            if m is None:
                continue

            try:
                databases.setdefault(m.group('lang'), []).append(m)
            except AttributeError:
                continue

        return databases

    def language_date(self, language):
        """Get the database dump date for given language.
        """
        return self._date_from_match(self._db_matcher.match(
            self[language].name))

    def discover(self, vendor, driver, user, password, host, reflect=True):
        """Discover wikipedia databases.

        This method will discover and activate wikipedia databases on the
        configured host.

        :param vendor:  Database vendor (supported: mysql, postgresql)
        :type vendor:   string

        :param driver:  Driver for connection (psycopg2, mysqldb, ...)
        :type driver:   string

        :param user:    Name of database user
        :type user:     string

        :param password:    Password of given user
        :type password:     string

        :param host:        Hostname (localhost, 127.0.0.1, ...)
        :type host:         string

        :param reflect: Reflect database layout or load predefined table
                        definitions
        :type reflect:  bool
        """
        db = self._new_database(vendor, driver, user, password, host, None,
                                None)

        for lang, mats in self._match_databases(db).iteritems():
            latest = max(mats, key=lambda m: self._date_from_match(m))

            # do we have a newer database for this language already?
            # if yes -> skip this one
            if lang in self:
                existing_date = self.language_date(lang)
                found_date = self._date_from_match(latest)

                if existing_date > found_date:
                    continue

            new_db = self._new_database(vendor, driver, user, password, host,
                                        latest.group(0), latest.group('lang'))
            new_db.connect(reflect)
            new_db.create_mappers()
            self[lang] = new_db


class Database(object):
    """Base class for vendor specific databases"""

    def __init__(self, vendor, driver, user, password, host, db_name,
                 language):
        super(Database, self).__init__()

        self.vendor = vendor
        self.driver = driver
        self.user = user
        self.host = host
        self.password = password
        self.name = db_name
        self.language = language

        if self.vendor == 'postgresql':
            self._admin_engine = create_engine(
                '{0.vendor}+{0.driver}://{0.user}:{0.password}@{0.host}' \
                '/postgres'.format(self))
        elif self.vendor == 'mysql':
            self._admin_engine = create_engine(
                '{0.vendor}+{0.driver}://{0.user}:{0.password}@' \
                '{0.host}'.format(self))
        self._session = None
        self._engine = None

        self.pool_size = 0
        self.pool_recycle = 300


    # ----------
    # Properties

    @property
    def session(self):
        if self._session is None:
            self._session = self._Session()
        return self._session

    @property
    def engine(self):
        return self._engine

    @property
    def table_names(self):
        return self._metadata.tables.keys()

    @property
    def vendor(self):
        return self._vendor

    @vendor.setter
    def vendor(self, value):
        self._vendor = value

    @vendor.deleter
    def vendor(self):
        del self._vendor

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value

    @driver.deleter
    def driver(self):
        del self._driver

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @user.deleter
    def user(self):
        del self._user

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @password.deleter
    def password(self):
        del self._password

    @property
    def pool_size(self):
        return self._pool_size

    @pool_size.setter
    def pool_size(self, value):
        self._pool_size = value

    @pool_size.deleter
    def pool_size(self):
        del self._pool_size

    @property
    def pool_recycle(self):
        return self._pool_recycle

    @pool_recycle.setter
    def pool_recycle(self, value):
        self._pool_recycle = value

    @pool_recycle.deleter
    def pool_recycle(self):
        del self._pool_recycle

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @host.deleter
    def host(self):
        del self._host

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @name.deleter
    def name(self):
        del self._name

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        self._language = value

    @language.deleter
    def language(self):
        del self._language

    # -----------------------------------------
    # Common methods to all Database subclasses

    def connect(self, reflect=True):
        """Connect to database and initialise session

        :param reflect: Reflect database layout or load pre defined table
                        definitions
        :type reflect:  bool
        """
        _log.debug('{0.name}: Connecting'.format(self))
        self._engine = create_engine(
            '{0.vendor}+{0.driver}://{0.user}:{0.password}@{0.host}' \
            '/{0.name}'.format(self),
            echo=False,
            assert_unicode=True,
            convert_unicode=True,
            pool_size = self.pool_size,
            pool_recycle = self.pool_recycle)

        _log.debug('{0.name}: Create session and metadata'.format(self))
        self._Session = sessionmaker(bind=self.engine)
        self._metadata = MetaData(bind=self.engine)

        if reflect:
            self.reflect()
        else:
            self.tables_to_metadata()

    def create_mappers(self):
        """Create mappers for this database"""
        try:
            self.classes = mapper.init_mappers(self._metadata, self.language)
        except KeyError, k_err:
            _log.error('Could not create mappers: {0}'.format(repr(k_err)))

    def reflect(self):
        """Update database metadata"""
        _log.debug('{0.name}: Reflecting tables'.format(self))
        self._metadata.clear()
        self._metadata.reflect()

    def drop_table(self, table_name):
        """Drop table with given name

        :param table_name:  Name of the table to create
        :type table_name:   string
        """
        try:
            _log.debug('{0.name}.{1}: Drop'.format(self, table_name))
            tbl = self.get_table(table_name)
            tbl.drop()
            self.reflect()
        except KeyError, k_err:
            _log.debug('{0.name}.{1}: Missing table definition'.format(
                self, table_name))
            raise ValueError('Undefined Table: {0}'.format(table_name))

    def get_table(self, table_name):
        """Get table with given name

        :param table_name:  Name of the table to create
        :type table_name:   string
        """
        try:
            _log.debug('{0.name}.{1}: Get table instance'.format(
                self, table_name))

            return self._metadata.tables[table_name]
        except KeyError, k_err:
            _log.error('Missing table definition for: {0.name}.{1}'.format(
                self, table_name))
            raise ValueError('Undefined Table: {0.name}.{1}'.format(
                self, table_name))


class PostgreSQLDatabase(Database):
    """PostgreSQL database"""

    def __init__(self, driver, user, password, host, db_name, language):
        super(PostgreSQLDatabase, self).__init__('postgresql', driver, user,
                                                 password, host, db_name,
                                                 language)

    def __repr__(self):
        return 'PostgreSQLDatabase({0.host}, {0.name})'.format(self)

    # ---------------
    # Private methods

    @contextmanager
    def _autocommit_admin_conn(self):
        """Contextmanager for admin sessions with transaction level set to
        AUTOCOMMIT.
        """
        try:
            conn = self._admin_engine.connect()
            old_isolation_level = conn.connection.isolation_level
            conn.connection.set_isolation_level(
                ISOLATION_LEVEL_AUTOCOMMIT)
            yield conn
        finally:
            conn.connection.set_isolation_level(old_isolation_level)

    @contextmanager
    def _admin_conn(self):
        """Contextmanager for admin engine connections.
        """
        yield self._admin_engine.connect()

    @contextmanager
    def _conn(self):
        yield self._engine.connect()

    def _get_pkey_columns(self, table_name):
        """Get primary key column definition for given table"""
        try:
            _log.debug('{0.name}.{1}: Get pkey columns'.format(
                self, table_name))
            return postgresql_tables.pkey_columns[table_name]
        except KeyError, k_err:
            _log.warning('{0.name}.{1}: Undefined pkey columns'.format(
                self, table_name))
            return None

    def _get_index_definitions(self, table_name):
        """Get index column definitions for given table"""
        try:
            _log.debug('{0.name}.{1}: Get index definitions'.format(
                self, table_name))
            return postgresql_tables.indexed_columns[table_name]
        except KeyError, k_err:
            _log.warning('{0.name}.{1}: No indexes defined'.format(
                self, table_name))
            return None

    def _new_pkey_constraint(self, table_name):
        """Create a new primary key constraint

        :param table_name:  Name of the table for which to create a pkey
                            constraint
        :type table_name:   string
        """
        pk_cols = self._get_pkey_columns(table_name)

        if pk_cols is None:
            return None

        tbl = self.get_table(table_name)

        _log.debug('{0.name}.{1}: Create pkey instance'.format(
            self, table_name))

        try:
            return PrimaryKeyConstraint(
                *[tbl.c[pk] for pk in pk_cols],
                **{
                    str('name'): '{0}_pkey'.format(table_name),
                })
        except KeyError, k_err:
            _log.debug('{0.name}.{1}: Error in pkey definition: {2}'.format(
                self, table_name, pk_cols))
            raise exceptions.PrimaryKeyConstraintError(
                '{0.name}.{1}: Error in pkey definition: {2}'.format(
                    self, table_name, pk_cols))

    def _new_indexes(self, table_name):
        """Create new indexes for given table

        :param table_name:  Name of the table for which to create indexes
        :type table_name:   string
        """
        index_defs = self._get_index_definitions(table_name)
        tbl = self.get_table(table_name)

        if index_defs is None:
            return []

        try:
            _log.debug('{0.name}.{1}: Create index instance'.format(
                self, table_name))

            # New index name will consist of the joined colum names:
            # tbl.newt_column, tbl.witch_column ->
            #   tbl_newt_column_tbl_witch_column
            return [
                Index('_'.join(icols), *[tbl.c[icol] for icol in icols])
                    for icols in index_defs]
        except KeyError, k_err:
            _log.error('{0.name}.{1}: Error in index definition: {2}'.format(
                self, table_name, index_defs))
            raise exceptions.IndexError(
                '{0.name}.{1}: Error in index definition: {2}'.format(
                    self, table_name, index_defs))

    def all_databases(self):
        """Get a list of all databases on this DBs host"""
        _log.debug('{0.host}: List all databases'.format(self))

        with self._admin_conn() as conn:
            return [d[0] for d in conn.execute(
                'SELECT datname FROM pg_database;').fetchall()]

    # -----------------------
    # Database administration

    def analyze(self):
        """ANALYZE this database"""
        _log.debug('{0.name}: Analyze'.format(self))
        self.engine.execute('ANALYZE')

    def create(self):
        """Create this database"""
        _log.debug('{0.name}: Create'.format(self))
        with self._autocommit_admin_conn() as conn:
            conn.execute('CREATE DATABASE {0.name}'.format(self))

    def drop(self):
        """Drop this database"""
        _log.debug('{0.name}: Drop'.format(self))
        with self._autocommit_admin_conn() as conn:
            conn.execute('DROP DATABASE {0.name}'.format(self))

    def vacuum(self):
        """VACUUM this database"""
        _log.debug('{0.name}: Vacuum'.format(self))
        with self._autocommit_admin_conn() as conn:
            conn.execute('VACUUM')

    # --------------------
    # Table administration

    def create_table(self, table_name, pkey=True, index=True):
        """Create table with given name

        :param table_name:  Name of the table to create
        :type table_name:   string

        :param pkey:        Create primary key constraint for this table
        :type pkey:         bool

        :param index:       Create indexes for this table
        :type index:        bool
        """
        try:
            tbl = postgresql_tables.metadata.tables[table_name]

            _log.debug('{0.name}.{1}: Create'.format(self, table_name))
            tbl.create(bind=self._engine)

            self.reflect()

            if pkey:
                self.create_pkey_constraint(table_name)

            if index:
                self.create_indexes(table_name)

        except KeyError, k_err:
            _log.debug('{0.name}.{1}: Missing table definition'.format(
                self, table_name))
            raise ValueError('{0.name}.{1}: Missing table definition'.format(
                self, table_name))

    def tables_to_metadata(self):
        """Load predefined table definitions"""
        self.reflect()
        found_tables = self._metadata.tables.keys()
        self._metadata.clear()

        _log.debug('{0.name}: Load predefined table definitions'.format(self))
        for table in postgresql_tables.tables:
            if table.name in found_tables:

                _log.debug('{0.name}.{1}: Load definition'.format(
                    self, table.name))

                table.tometadata(self._metadata)

    def truncate_table(self, table_name):
        """Truncate table with given name.

        :param table_name:  Name of the table to truncate
        :type table_name:   string
        """
        _log.debug('{0.name}.{1}: Truncate'.format(
            self, table_name))

        with self._conn() as conn:
            conn.execute('BEGIN')
            conn.execute('TRUNCATE TABLE {0} RESTART IDENTITY'.format(
                table_name))
            conn.execute('COMMIT')

    # -----------------
    # Table constraints

    def create_pkey_constraint(self, table_name):
        """Create primary key constraint for given table

        :param table_name:  Name of the table for which a pkey constraint
                            should be created.
        :type table_name:   string
        """
        pkey = self._new_pkey_constraint(table_name)

        if pkey is not None:
            _log.debug('{0.name}.{1}: Add pkey constraint: {2}'.format(
                self, table_name, pkey.name))
            self._engine.execute(AddConstraint(pkey))
        else:
            _log.debug('{0.name}.{1}: No pkey defined'.format(
                self, table_name))

    def drop_pkey_constraint(self, table_name):
        """Drop primary key constraint on given table.

        :param table_name:  Table for which pkey constraint should be dropped
        :type table_name:   string
        """
        pkey = self.get_table(table_name).primary_key

        if not pkey.columns.keys():
            _log.debug('{0.name}.{1}: No pkey constraint found'.format(
                self, table_name))
            return
        else:
            _log.debug('{0.name}.{1}: Pkey constraint on columns: {2}'.format(
                self, table_name, ', '.join(pkey.columns.keys())))
            _log.debug('{0.name}.{1}: Drop pkey constraint'.format(
                self, table_name))
            self._engine.execute(
                'ALTER TABLE "{0}" DROP CONSTRAINT {0}_pkey;'.format(
                    table_name))
        self.reflect()

    # -------
    # Indexes

    def create_indexes(self, table_name):
        """Add indexes for given table

        :param table_name:  Name of the table for which to create indexes
        :type table_name:   string
        """
        for idx in self._new_indexes(table_name):
            _log.debug('{0.name}.{1}: Creating index: {2.name}'.format(
                self, table_name, idx))
            idx.create(bind=self._engine)

    def drop_indexes(self, table_name):
        """Drop indexes on given table.

        :param table_name:  Table for which index should be dropped
        :type table_name:   string

        :return:            Dropped indexes
        :rtype:             set
        """
        tbl = self.get_table(table_name)
        for idx in tbl.indexes:
            _log.debug('{0.name}.{1}: Dropping index: {2.name}'.format(
                self, table_name, idx))
            idx.drop()
        self.reflect()


class MySQLDatabase(Database):
    """MySQL database"""

    def __init__(self, driver, user, password, host, db_name, language):
        super(MySQLDatabase, self).__init__('mysql', driver, user,
                                            password, host, db_name,
                                            language)

    def __repr__(self):
        return 'MySQLDatabase({0.host}, {0.name})'.format(self)

    def all_databases(self):
        """Get a list of all databases on this DBs host"""

        _log.debug('{0.host}: List all databases'.format(self))

        return (d[0] for d in self.admin_session.execute(
            'SHOW DATABASES;').fetchall())

    # -----------------------
    # Database administration

    def create(self):
        """Create this database"""
        _log.debug('{0.name}: Create'.format(self))
        self.admin_session.execute('CREATE DATABASE {0.name}'.format(self))

    def drop(self):
        """Drop this database"""
        _log.debug('{0.name}: Drop'.format(self))
        self.admin_session.execute('DROP DATABASE {0.name}'.format(self))

    # -------
    # Indexes

    def create_indexes(self, table_name):
        """Add indexes for given table

        :param table_name:  Name of the table for which to create indexes
        :type table_name:   string
        """
        raise NotImplementedError()

    def drop_indexes(self, table_name):
        """Drop indexes on given table.

        :param table_name:  Table for which index should be dropped
        :type table_name:   string
        """
        raise NotImplementedError()

    # --------------------
    # Table administration

    def create_table(self, table_name, pkey=True, index=True):
        """Create table with given name

        :param table_name:  Name of the table to create
        :type table_name:   string

        :param pkey:        Create primary key constraint
        :type pkey:         bool

        :param index:       Create indexes
        :type index:        bool
        """
        raise NotImplementedError()

    def tables_to_metadata(self):
        """Load predefined table definitions"""

        _log.debug('{0.name}: Load predefined table definitions'.format(self))

        self.reflect()
        found_tables = self._metadata.tables.keys()
        self._metadata.clear()

        for table in generic_tables.tables:
            if table.name in found_tables:
                _log.debug('{0.name}.{1}: Load definition'.format(
                    self, table.name))
                table.tometadata(self._metadata)

    def truncate_table(self, table_name):
        """Truncate table with given name.

        :param table_name:  Name of the table to truncate
        :type table_name:   string
        """
        raise NotImplementedError()


    # -----------------
    # Table constraints

    def create_pkey_constraint(self, table_name):
        """Create primary key constraint for given table

        :param table_name:  Name of the table for which a pkey constraint
                            should be created.
        :type table_name:   string
        """
        raise NotImplementedError()

    def drop_pkey_constraint(self, table_name):
        """Drop primary key constraint on given table.

        :param table_name:  Table for which pkey constraint should be dropped
        :type table_name:   string
        """
        raise NotImplementedError()

    # -------
    # Indexes

    def create_indexes(self, table_name):
        """Add indexes for given table

        :param table_name:  Name of the table for which to create indexes
        :type table_name:   string
        """
        raise NotImplementedError()

    def drop_indexes(self, table_name):
        """Drop indexes on given table.

        :param table_name:  Table for which index should be dropped
        :type table_name:   string

        :return:            Dropped indexes
        :rtype:             set
        """
        raise NotImplementedError()
