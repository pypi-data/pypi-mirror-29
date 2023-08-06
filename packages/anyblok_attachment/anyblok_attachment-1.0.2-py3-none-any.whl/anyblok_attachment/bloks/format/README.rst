.. This file is a part of the AnyBlok / Attachment project
..
..    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

Memento
~~~~~~~

Simple python templating formatage

template file exemple::

    <!doctype html>
    <html>
        <head>
            <title>{title}</title>
        </head>
        <body>
            {description}
        </body>
    </html>

add the documment and create file::

    template = registry.Attachment.Template.Format.insert(
        template_path='path/of/the/python.template',
        contenttype='text/html',
        filename='mypage.html')
    document = registry.Attachment.Document.insert(
        template=template,
        data={'title': 'My page', 'description': 'Hello world !!'}
    )
    document.get_file()

>>>::

    {
        'contenttype': 'text/html',
        'file': b'<!doctype html>\n<html>\n    <head>\n        <title>My page</title>'
                b'\n    </head>\n    <body>\n        Hello world !!\n    </body>\n<'
                b'/html>\n',
        'file_added_at': datetime.datetime(2018, 1, 4, 9, 22, 56, 922346, tzinfo=<DstTzInfo 'CET' CET+1:00:00 STD>),
        'filename': 'mypage.html',
        'filesize': 131,
        'hash': b'\xf0\xe2?\xebk\xb4\x15\x0f\xb2\x9cT\x08\xee#\x02\xe2\xbe\xa16\x8d'
                b'\xc8\xcda\x91;\xba2\x9c\x9dUF\x10'}

    }
