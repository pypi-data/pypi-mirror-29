===============================
``pyramid_oereb`` (ÖREB-Server)
===============================

|Build Status|

``pyramid_oereb`` is an open-source implementation of the server side part for the swiss `"Cadastre of
Public-law Restrictions on landownership" (PLR-cadastre) <https://www.cadastre.ch/en/oereb.html>`__.

It is written in Python and designed as a plugin for the `Pyramid Web Framework
<http://docs.pylonsproject.org/projects/pyramid/en/latest/>`__. This allows *pyramid\_oereb* to be included in
any Pyramid web application.

Please refer to the `documentation <https://camptocamp.github.io/pyramid_oereb/doc/>`__ for detailed
information and instructions for installation and configuration.

If you are interested in contributing or extending the project, take a look at the
`contribution page <https://camptocamp.github.io/pyramid_oereb/doc/master/contrib/>`__.

.. |Build Status| image:: https://travis-ci.org/camptocamp/pyramid_oereb.svg?branch=master
   :target: https://travis-ci.org/camptocamp/pyramid_oereb


---------
Changelog
---------

1.0.1
*****

- introduce configurable pdf print service (print proxy)
- enable proxy configuration for external web api usage
- fix standard database
- improve python 3 compatibility
- minor bug fixing

1.0.0
*****

- improved doc
- fix bug for doc creation on python 3.6

1.0.0-beta.1
************

- first approach of OEREB server
- improved documentation on https://camptocamp.github.io/pyramid_oereb/doc/
- cleaned and reorganized code
- binding to OEREB-LEX and GeoAdmin-Api-Address-Service
  (http://api.geo.admin.ch/services/sdiservices.html#search) as sources
- providing pyconizer as icon generator (https://pypi.python.org/pypi/pyconizer)
- proxy binding of geomapfish_print for pdf output as renderer
  (http://mapfish.github.io/mapfish-print-doc/#/overview)
- providing extensive standard configuration for out-of-the-box-usage
- general bug fixing
- add python 3.x support

1.0.0-alpha.2
*************

-  proceed with renderer for xml and json
-  add metadata for embeddable flavour
-  images accessible via URL
-  add configurable methods for processing
-  improve geometry handling
-  add documentation on https://camptocamp.github.io/pyramid_oereb/doc/
-  several bugfixes

1.0.0-alpha.1
*************

-  first running approach of server
-  main web services are available (not all formats are implemented yet)
-  standard configuration can be used to run server out of the box
-  see README for more details

0.0.1
*****

-  initial version


