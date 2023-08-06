.. This file is a part of the AnyBlok / Attachment project
..
..    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

Memento
~~~~~~~

The document historize the version::

    doc = registry.Attachment.Document.insert(...)
    assert doc.type == 'latest'
    assert doc.previous_version is None

    doc.data = {'other': 'data'}
    assert doc.previous_version is not None
    assert doc.previous_version.type == 'historized'

You can get:

* All document::

      registry.Attachment.Document.query().all()

* Only the latest::

      registry.Attachment.Document.Latest.query().all()

* Only the historized::

      registry.Attachment.Document.History.query().all()

.. note::

    If one entry changed and a file is available then a historied version
    will be autmaticly created.

    The historized version get the latest version of the document and a new version is 
    added to the document
