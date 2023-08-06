Installation
============

::

    [instance]
    ...
    eggs =
        ...
        edw.logger
    zcml =
        ...
        edw.logger


Introduction
============

This package creates a new `edw.logger` log facility that logs to
INFO and ERROR the following events:

* Viewed pages - Enabled by default. Can be disabled via environment variable **EDW_LOGGER_PUBLISHER** (e.g.: *EDW_LOGGER_PUBLISHER=false*;
* Raised errors - Enabled by default. Can be disabled via environment variable **EDW_LOGGER_ERRORS** (e.g.: *EDW_LOGGER_ERRORS=false*);
* Added/created/copied/moved/deleted content - Enabled by default. Can be disabled via environment variable **EDW_LOGGER_CONTENT** (e.g.: *EDW_LOGGER_CONTENT=false*);
* ZODB commits - Enabled by default. Can be disabled via environment variable **EDW_LOGGER_DB** (e.g.: *EDW_LOGGER_DB=false*);
* Catalog indexing - Enabled by default. Can be disabled via environment variable **EDW_LOGGER_CATALOG** (e.g.: *EDW_LOGGER_CATALOG=false*);
* Catalog indexing stack trace - Disabled by default. Can be enabled via environment variable **EDW_LOGGER_CATALOG_STACK** (e.g.: *EDW_LOGGER_CATALOG_STACK=true*);

Changelog
=========

1.13 - (2018-03-02)
-------------------
* Fix logging errors caused by recursive Acquisition wrapped objects
  [batradav]

1.12 - (2018-02-28)
-------------------
* Fix zCatalog idxs and metadata report
  [avoinea]

1.11 - (2018-01-18)
-------------------
* Fix integer literals in duration report.
  [batradav]

1.10 - (2018-01-18)
-------------------
* Add zCatalog catalog_object support. Disabled by default.
  [batradav]

1.9 - (2017-05-23)
------------------
* Add 'Action' based on URL on db commits and errors
  [avoinea]

1.8 - (2017-05-23)
------------------
- Fix AttributeError: REQUEST
  [avoinea]

1.7 - (2017-05-16)
------------------
- Fix AttributeError: 'NoneType' object has no attribute 'getUserName'
  [avoinea]

1.6 - (2017-05-16)
------------------
- Add missing LoggerName on db_commit
  [avoinea]

1.5 - (2017-05-16)
------------------
- Enable/disable logging via environment variables
  [avoinea]

1.4 - (2017-05-12)
------------------
- Ignore health.check URLs
  [batradav]

1.3 - (2017-02.21)
------------------
- Fixed cases where traceback contains non-ascii characters
  [olimpiurob refs #82516]
- Add 'font' to ignored content types.
  [batradav]

1.2 - (2017-01-26)
------------------
- Ignore all but GET and POST requests.
  [batradav]

1.1 - (2017-01-19)
------------------
- Added LoggerName in the JSON object [refs #80663 olimpiurob]

1.0 - (2017-01-17)
------------------
- Initial release



