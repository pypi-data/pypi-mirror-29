.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

=================================
collective.restapi.navigationtree
=================================

.. image:: http://img.shields.io/pypi/v/collective.restapi.navigationtree.svg
      :target: https://pypi.python.org/pypi/collective.restapi.navigationtree

.. image:: https://img.shields.io/travis/collective/collective.restapi.navigationtree/master.svg
       :target: http://travis-ci.org/collective/collective.restapi.navigationtree

.. image:: https://img.shields.io/coveralls/collective/collective.restapi.navigationtree/master.svg
       :target: https://coveralls.io/r/collective/collective.restapi.navigationtree


This Plone plugin provides a REST endpoint to query the site's navigation tree.
The endpoint name is ``@navigationtree``,
and can be considered an extension to ``plone.restapi``'s ``@navigation`` endpoint, 
since the latter only returns the top level navigation menu items.
``collective.restapi.navigationtree`` depends on the ``webcouturier.dropdownmenu`` plugin to build the navigation tree,
and honors the same configuration settings as ``webcouturier.dropdownmenu``.
Thus, the maximum depth of the tree can be set in the ``webcouturier.dropdownmenu`` configlet.

Tested on Plone 4.3, 5.0 and 5.1 with Archetypes and Dexterity.


Features
--------

- Simply ``GET @navigationtree``
- Extends the ``@navigation`` endpoint of ``plone.restapi`` by building a full navigation tree of the site, instead of limiting itself to just the top level navigation menu.
- Depends on ``webcouturier.dropdownmenu``, thus is ideal for sites that already use this plugin for their navigation menu.
- Honors all the configuration settings in Plone's _Navigation_ control panel.
- Honors all the configuration settings in ``@@dropdown-controlpanel``.
- In particular, you can set the depth of the navigation tree in ``webcouturier.dropdownmenu``'s configlet.


Examples
--------

Getting the navigation tree::

    GET /plone/@navigationtree HTTP/1.1
    Accept: application/json
    Authorization: Basic YWRtaW46c2VjcmV0

(Authorization is optional.)

Example response::

    {
        "@id": "http://localhost:8080/Plone/@navigationtree",
        "items": [
            {
                "@id": "http://localhost:8080/Plone",
                "description": "",
                "items": "",
                "title": "Home"
            },
            {
                "@id": "http://localhost:8080/Plone/news",
                "description": "Site News",
                "items": [
                    {
                        "@id": "http://localhost:8080/Plone/news/some-news",
                        "description": "",
                        "title": "Some News"
                    }
                ],
                "title": "News"
            },
            {
                "@id": "http://localhost:8080/Plone/events",
                "description": "Site Events",
                "items": [],
                "title": "Events"
            },
            {
                "@id": "http://localhost:8080/Plone/Members",
                "description": "Site Users",
                "items": [],
                "title": "Users"
            }
        ]
    }

Installation
------------

Install collective.restapi.navigationtree by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.restapi.navigationtree


and then running ``bin/buildout``.  
This will automatically install webcouturier.dropdownmenu and plone.restapi,
so you should pin the versions of these add-ons according to the version of Plone you are running.


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.restapi.navigationtree/issues
- Source Code: https://github.com/collective/collective.restapi.navigationtree
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know in the issue tracker.


License
-------

The project is licensed under the GPLv2.
