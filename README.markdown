mwdb
====

mwdb is a [Python][] library for working with data in [MediaWiki][] databases
like those from Wikipedia. It is useful for researchers in the fields of
Computational Linguistics, Machine Learning, Knowledge Representation ...

Features
--------

* Simultaneous access to data in all languages available from Wikipedia
* No conversion of Wikipedia database dumps needed
* Automatic database discovery
* Distributed databases
* Supports [PostgreSQL][] and [MySQL][]
* Object Relational mapper written in [SQLAlchemy][]
* Markup handling with [mwlib][]
* Database, table and index administration for PostgreSQL
* Open source :-)

Install
-------

Just move `./lib/mwdb` into your `$PYTHONPATH`

Example
-------

You need to import mwdb and mwdb.orm:

    In [1]: import mwdb, mwdb.orm

Initialising databases is done with `mwdb.orm.databases.discover`.
This method takes five arguments, namely `vendor` (`postgresql` or
`mysql`), dialect (`psycopg2`, `mysqldb`, ...), the name of the
database user, her password and the host the databases are found on.
`discover` will find all MediaWiki databases that adhere to a naming
scheme following the regular expression
`wp_(?P<lang>\w+)_(?P<date>\d+)`.

If you follow a different naming scheme you can easily change this by
setting `mwdb.orm.databases.db_name_regex` to the regular expression of your
choice prior to discovery. It is of uttermost importance that the provided
regular expressions has *named* groups `lang` and `date`.

If you decided not to follow the date format in the Wikipedia dumps (%Y%m%d)
you can set a new format on `mwdb.orm.databases.db_date_format`, but why would
you do that?

    In [2]: mwdb.orm.databases.discover_databases(
                'postgresql', 'psycopg2', 'user','password','host')

Access to Wikipedia articles is provided through instances of
`mwdb.Wikipedia('language'):

    In [3]: hh = mwdb.Wikipedia('de').get_article(u'Hamburg')

Article instances provide access to categories, linked articles,
different link types and even articles in other languages this article
is linked to:

    In [4]: hh.translated_articles
    Out[4]: [NL_Article(u'Hamburg'), SW_Article(u'Hamburg')]

    In [5]: hh.translated_articles[0].language
    Out[5]: 'nl'

    In [6]: hh.translated_articles[0].linked_articles
    Out[6]:
    [NL_Article(u'2008'),
     NL_Article(u'Alfred_Schnittke'),
     NL_Article(u'Alfred_Wegener'),
     NL_Article(u'Amsterdam'),
     NL_Article(u'Anastas\xc3\xada_Keles\xc3\xaddou'),
     ...
     NL_Article(u'Wolgast')]

    In [7]: hh.categories
    Out[7]:
    [DE_Category(u'Gemeinde_in_Deutschland'),
     DE_Category(u'Hamburg'),
     DE_Category(u'Hansestadt'),
     DE_Category(u'Kreisfreie_Stadt_in_Deutschland'),
     DE_Category(u'Land_(Deutschland)'),
     DE_Category(u'Millionenstadt'),
     DE_Category(u'Ort_mit_Seehafen'),
     DE_Category(u'Reichsstadt'),
     DE_Category(u'Wikipedia:Lesenswert'),
     DE_Category(u'Wikipedia:Quellen_fehlen')]
     ...

[PostgreSQL] : http://www.postgresql.org
[MySQL]      : http://www.mysql.com
[SQLAlchemy] : http://www.sqlalchemy.org
[mwlib]      : http://code.pediapress.com/wiki/wiki/mwlib
[Python]     : http://python.org
[Wikipedia]  : http://wikipedia.org
[MediaWiki]  : http://www.mediawiki.org
