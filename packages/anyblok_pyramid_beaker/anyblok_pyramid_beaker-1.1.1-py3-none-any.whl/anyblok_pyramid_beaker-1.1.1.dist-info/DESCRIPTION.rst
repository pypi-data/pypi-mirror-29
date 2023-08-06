.. This file is a part of the AnyBlok / Pyramid / Beaker project
..
..    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. image:: https://travis-ci.org/AnyBlok/AnyBlok_Pyramid_Beaker.svg?branch=master
    :target: https://travis-ci.org/AnyBlok/AnyBlok_Pyramid_Beaker
    :alt: Build status

.. image:: https://coveralls.io/repos/github/AnyBlok/AnyBlok_Pyramid_Beaker/badge.svg?branch=master
    :target: https://coveralls.io/github/AnyBlok/AnyBlok_Pyramid_Beaker?branch=master
    :alt: Coverage

.. image:: https://img.shields.io/pypi/v/AnyBlok_Pyramid_Beaker.svg
   :target: https://pypi.python.org/pypi/AnyBlok_Pyramid_Beaker/
   :alt: Version status

.. image:: https://readthedocs.org/projects/anyblok-pyramid-beaker/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://doc.anyblok-pyramid-beaker.anyblok.org/en/latest/?badge=latest


AnyBlok / Pyramid / Beaker
==========================

AnyBlok / Pyramid / Beaker make the link between `AnyBlok / Pyramid <http://doc.anyblok-pyramid.anyblok.org>`_,
`Pyramid <http://pyramid.readthedocs.org/>`_ and `Beaker <http://docs.pylonsproject.org/projects/pyramid_beaker/en/latest/>`_

AnyBlok / Pyramid / Beaker is released under the terms of the `Mozilla Public License`.

See the `latest documentation <http://doc.anyblok-pyramid-beaker.anyblok.org/>`_

.. This file is a part of the AnyBlok / Pyramid / Beaker project
..
..    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. contents::

Front Matter
============

Information about the AnyBlok / Pyramid / Beaker project.

Project Homepage
----------------

AnyBlok is hosted on `github <http://github.com>`_ - the main project
page is at https://github.com/AnyBlok/AnyBlok_Pyramid_Beaker. Source code is
tracked here using `GIT <https://git-scm.com>`_.

Releases and project status are available on Pypi at
http://pypi.python.org/pypi/anyblok_pyramid_beaker.

The most recent published version of this documentation should be at
http://doc.anyblok-pyramid-beaker.anyblok.org.

Project Status
--------------

AnyBlok with Pyramid is currently in beta status and is expected to be fairly
stable.   Users should take care to report bugs and missing features on an as-needed
basis.  It should be expected that the development version may be required
for proper implementation of recently repaired issues in between releases;
the latest master is always available at http://bitbucket.org/jssuzanne/anyblok_pyramid_beaker/get/default.tar.gz.

Installation
------------

Install released versions of AnyBlok from the Python package index with
`pip <http://pypi.python.org/pypi/pip>`_ or a similar tool::

    pip install anyblok_pyramid_beaker

Installation via source distribution is via the ``setup.py`` script::

    python setup.py install

Installation will add the ``anyblok``and ``anyblok_pyramid`` commands to the environment.

Unit Test
---------

Run the test with ``nose``::

    pip install nose
    nosetests anyblok_pyramid_beaker/tests

Dependencies
------------

AnyBlok works with **Python 3.3** and later. The install process will
ensure that `AnyBlok <http://doc.anyblok.org>`_,
`AnyBlok / Pyramid <http://doc.anyblok-pyramid.anybox.org>`_ 
are installed, in addition to other dependencies. The latest version of them 
is strongly recommended.


Contributing (hackers needed!)
------------------------------

Anyblok / Pyramid / Beaker is at a very early stage, feel free to fork, talk 
with core dev, and spread the word!

Author
------

Jean-Sébastien Suzanne

Contributors
------------

`Anybox <http://anybox.fr>`_ team:

* Jean-Sébastien Suzanne

Bugs
----

Bugs and feature enhancements to AnyBlok should be reported on the `Issue
tracker <https://github.org/AnyBlok/Anyblok_Pyramid_Beaker/issues>`_.

.. This file is a part of the AnyBlok / Pyramid / Beaker project
..
..    Copyright (C) 2015 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..    Copyright (C) 2016 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. contents::

CHANGELOG
=========

1.1.1 (2018-02-27)
------------------

* [REF] Anyblok 0.17.0 changed setter to add application and application 
  groups, So I had to adapt the existing to use new setter

1.1.0 (2017-10-14)
------------------

* [REF] config use the Configuration.add_configuration_groups

1.0.0 (2016-07-11)
------------------

* [REF] adapt to AnyBlok 0.9.0 and AnyBlok / Pyramid 0.7.0
* [REF] replace set/get callable by plugin get_db_name
* [REF] Update doc

O.2.0 (2016-06-22)
------------------

* [FIX] utf-8 encoding need for readthedocs

0.1.0 (2016-04-18)
------------------

* [ADD] beaker setting and pyramid config
* [ADD] db_name is store in the session and use it for anyblok_pyramid request
  ``anyblok.registry`` property


