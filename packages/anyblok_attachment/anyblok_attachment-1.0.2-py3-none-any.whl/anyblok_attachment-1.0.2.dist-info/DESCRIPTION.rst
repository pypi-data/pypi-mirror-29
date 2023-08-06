.. This file is a part of the AnyBlok / Attachment project
..
..    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. image:: https://travis-ci.org/AnyBlok/anyblok_attachment.svg?branch=master
    :target: https://travis-ci.org/AnyBlok/anyblok_attachment
    :alt: Build status

.. image:: https://coveralls.io/repos/github/AnyBlok/anyblok_attachment/badge.svg?branch=master
    :target: https://coveralls.io/github/AnyBlok/anyblok_attachment?branch=master
    :alt: Coverage

.. image:: https://img.shields.io/pypi/v/anyblok_attachment.svg
   :target: https://pypi.python.org/pypi/anyblok_attachment/
   :alt: Version status

.. image:: https://readthedocs.org/projects/anyblok-attachment/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://doc.anyblok-attachment.anyblok.org/?badge=latest


AnyBlok / Dramatiq
==================

Improve AnyBlok `AnyBlok <http://doc.anyblok.org>`_ to add attachment and report
system.

AnyBlok / Attachment is released under the terms of the `Mozilla Public License`.

See the `latest documentation <http://doc.anyblok-attachment.anyblok.org/>`_

.. This file is a part of the AnyBlok / Attachment project
..
..    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

Front Matter
============

Information about the AnyBlok / Attachment project.

Project Homepage
----------------

AnyBlok is hosted on `github <http://github.com>`_ - the main project
page is at https://github.com/AnyBlok/anyblok_attachment. Source code is
tracked here using `GIT <https://git-scm.com>`_.

Releases and project status are available on Pypi at
http://pypi.python.org/pypi/anyblok_attachment.

The most recent published version of this documentation should be at
http://doc.anyblok-attachment.anyblok.org.

Project Status
--------------

AnyBlok with attachment is currently in beta status and is expected to be fairly
stable.   Users should take care to report bugs and missing features on an as-needed
basis.  It should be expected that the development version may be required
for proper implementation of recently repaired issues in between releases;

Installation
------------

Install released versions of AnyBlok from the Python package index with
`pip <http://pypi.python.org/pypi/pip>`_ or a similar tool::

    pip install anyblok_attachment

Installation via source distribution is via the ``setup.py`` script::

    python setup.py install

Installation will add the ``anyblok`` commands to the environment.

Unit Test
---------

Run the test with ``nose``::

    pip install nose
    nosetests anyblok_attachment/tests

Dependencies
------------

AnyBlok / Attachment works with **Python 3.3** and later. The install process will
ensure that `AnyBlok <http://doc.anyblok.org>`_ is installed, in addition to other 
dependencies. The latest version of them is strongly recommended.

Author
------

Jean-Sébastien Suzanne

Contributors
------------

`Anybox <http://anybox.fr>`_ team:

* Jean-Sébastien Suzanne

`Sensee <http://sensee.com>`_ team:

* Franck Bret

Bugs
----

Bugs and feature enhancements to AnyBlok should be reported on the `Issue
tracker <https://github.com/AnyBlok/anyblok_attachment/issues>`_.

.. This file is a part of the AnyBlok / Attachment project
..
..    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

.. contents::

CHANGELOG
=========

1.0.2 (2018-02-24)
------------------

* [REF] Anyblok 0.17.0 changed setter to add application and application 
  groups, So I had to adapt the existing to use new setter

1.0.1 (2018-01-11)
------------------

* [FIX] ``Mixin.WkHtml2Pdf`` check also if the configuration changed for 
  **Template.check_if_file_must_be_generated**

1.0.0 (2018-01-10)
------------------

* [ADD] **attachment** blok: stock versionned file
* [ADD] **report** blok: create versionned file from template
* [ADD] **report-format** blok: template type
* [ADD] **wkhtml2pdf** blok: convert html to pdf in the template


