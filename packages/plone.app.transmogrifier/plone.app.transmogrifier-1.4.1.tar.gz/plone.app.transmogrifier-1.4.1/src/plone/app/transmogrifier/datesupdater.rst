DatesUpdater section
--------------------

This blueprint sets creation, modification and effective dates on objects.

Blueprint name: ``plone.app.transmogrifier.datesupdater``

Option path-key: The key for the path to the object.

Option creation-key: The key for the creation date.

Option modification-key: The key for the modification date.

Option effective-key: The key for the effective date.

Option expiration-key: The key for the expiration date.

::

    >>> import pprint
    >>> pipeline = """
    ... [transmogrifier]
    ... pipeline =
    ...     schemasource
    ...     datesupdater
    ...     logger
    ...
    ... [schemasource]
    ... blueprint = plone.app.transmogrifier.tests.schemasource
    ...
    ... [datesupdater]
    ... blueprint = plone.app.transmogrifier.datesupdater
    ... path-key = _path
    ... creation-key = creation_date
    ... modification-key = modification_date
    ... effective-key = effective_date
    ... expiration-key = expiration_date
    ...
    ... [logger]
    ... blueprint = collective.transmogrifier.sections.logger
    ... name = logger
    ... """
    >>> registerConfig(u'plone.app.transmogrifier.tests.datesupdater', pipeline)

    >>> transmogrifier(u'plone.app.transmogrifier.tests.datesupdater')


Print out the source structure::

    >>> print handler
    logger INFO
        {'_path': '/spam/eggs/foo',
       'creation_date': DateTime('2010/10/10 00:00:00 UTC'),
       'effective_date': DateTime('2010/10/10 00:00:00 UTC'),
       'expiration_date': DateTime('2012/12/12 00:00:00 UTC'),
       'modification_date': DateTime('2011/11/11 00:00:00 UTC')}
    logger INFO
        {'_path': '/spam/eggs/bar',
       'creation_date': DateTime('2010/10/10 00:00:00 UTC')}
    logger INFO
        {'_path': '/spam/eggs/baz',
       'modification_date': DateTime('2011/11/11 00:00:00 UTC')}
    logger INFO
        {'_path': '/spam/eggs/qux',
       'effective_date': DateTime('2010/10/10 00:00:00 UTC')}
    logger INFO
        {'_path': '/spam/eggs/norf',
       'expiration_date': DateTime('2012/12/12 00:00:00 UTC')}
    logger INFO
        {'_path': 'not/existing/bar',
       'creation_date': DateTime('2010/10/10 00:00:00 UTC'),
       'effective_date': DateTime('2010/10/10 00:00:00 UTC'),
       'expiration_date': DateTime('2012/12/12 00:00:00 UTC'),
       'modification_date': DateTime('2011/11/11 00:00:00 UTC')}
    logger INFO
        {'creation_date': DateTime('2010/10/10 00:00:00 UTC'),
       'effective_date': DateTime('2010/10/10 00:00:00 UTC'),
       'expiration_date': DateTime('2012/12/12 00:00:00 UTC'),
       'modification_date': DateTime('2011/11/11 00:00:00 UTC')}


That was changed on the object::

    >>> pprint.pprint(plone.updated)
    [('spam/eggs/foo', 'creation_date', DateTime('2010/10/10 00:00:00 UTC')),
     ('spam/eggs/foo', 'modification_date', DateTime('2011/11/11 00:00:00 UTC')),
     ('spam/eggs/foo', 'effective_date', DateTime('2010/10/10 00:00:00 UTC')),
     ('spam/eggs/foo', 'expiration_date', DateTime('2012/12/12 00:00:00 UTC')),
     ('spam/eggs/bar', 'creation_date', DateTime('2010/10/10 00:00:00 UTC')),
     ('spam/eggs/baz', 'modification_date', DateTime('2011/11/11 00:00:00 UTC')),
     ('spam/eggs/qux', 'effective_date', DateTime('2010/10/10 00:00:00 UTC')),
     ('spam/eggs/norf', 'expiration_date', DateTime('2012/12/12 00:00:00 UTC'))]
