mwdb
====

mwdb is a [Python] [py] library for working with data in [MediaWiki] [mw]
databases like those from [Wikipedia] [wp]. It is useful for researchers in the
fields of Computational Linguistics, Machine Learning, Knowledge Representation
...

Features
--------

* Simultaneous access to data in all languages available from Wikipedia
* No conversion of Wikipedia database dumps needed
* Automatic database discovery
* Distributed databases
* Supports [PostgreSQL] [psql] and [MySQL] [mysql]
* Object Relational mapper written in [SQLAlchemy] [sa]
* Database, table and index administration for PostgreSQL
* Open source :-)

Example
-------

You need to import mwdb:

    >>>  import mwdb

Initialising databases is done with `mwdb.databases.discover`. This method
takes five arguments, namely `vendor` (`postgresql` or `mysql`), dialect
(`psycopg2`, `mysqldb`, ...), the name of the database user, her password and
the host the databases are found on. `discover` will find all MediaWiki
databases that adhere to a naming scheme following the regular expression
`wp_(?P<lang>\w+)_(?P<date>\d+)`.

If you follow a different naming scheme you can easily change this by setting
`mwdb.databases.db_name_regex` to the regular expression of your choice prior
to discovery. It is of uttermost importance that the provided regular
expressions has the *named* groups `lang` and `date`.

If you decided not to follow the date format in the Wikipedia dumps (%Y%m%d)
you can set a new format on `mwdb.orm.databases.db_date_format`, but why would
you do that?

    >>> mwdb.databases.discover_databases(
    ... 'postgresql', 'psycopg2', 'user', 'password', 'host')

Access to Wikipedia articles is provided through instances of
`mwdb.Wikipedia:

    >>> hh = mwdb.Wikipedia('de').get_article(u'Hamburg')

Article instances provide access to categories, linked articles, different link
types and even the corresponding article in other languages:

    >>> list(hh.iter_translations())
    [AF_Article(u'Hamburg'),
    ALS_Article(u'Hamburg'), ...,
     ZH_Article(u'\u6c49\u5821'),
     ZH_MIN_NAN_Article(u'Hamburg'),
     ZH_YUE_Article(u'\u6f22\u5821')]

    >>> list(hh.iter_translations())[102].language
    u'zh'

    >>> zh_hh = list(hh.iter_translations())[102]
    >>> for art in zh_hh.iter_linked_articles():
    ...     print art
    ...
    ZH_Article(1520年代)
    ZH_Article(1768年)
    ZH_Article(1874年)
    ZH_Article(1876年)
    ...
    ZH_Article(马赛)
    ZH_Article(高地德语)
    ZH_Article(黑森)

    >>> hh.categories
    [DE_Category(u'Bundesland_(Deutschland)'),
     DE_Category(u'Deutsche_Landeshauptstadt'),
     DE_Category(u'Gemeinde_in_Deutschland'),
     DE_Category(u'Hamburg'),
     DE_Category(u'Hansestadt'),
     DE_Category(u'Kreisfreie_Stadt_in_Deutschland'),
     DE_Category(u'Millionenstadt'),
     DE_Category(u'Ort_mit_Seehafen'),
     DE_Category(u'Reichsstadt'),
     ... ]

[psql]: http://www.postgresql.org
[mysql]: http://www.mysql.com
[sa]: http://www.sqlalchemy.org
[py]: http://python.org
[wp]: http://wikipedia.org
[mw]: http://www.mediawiki.org
