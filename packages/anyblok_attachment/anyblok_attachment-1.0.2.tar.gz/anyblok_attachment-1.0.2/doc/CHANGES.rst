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
