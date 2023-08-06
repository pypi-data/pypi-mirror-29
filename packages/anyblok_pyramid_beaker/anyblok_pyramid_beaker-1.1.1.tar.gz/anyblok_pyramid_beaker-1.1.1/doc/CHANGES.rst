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
