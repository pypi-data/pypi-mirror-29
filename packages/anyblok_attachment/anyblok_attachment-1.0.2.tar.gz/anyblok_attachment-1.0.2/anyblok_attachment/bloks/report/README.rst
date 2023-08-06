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

The main goal is to create document in function of template

Add a new template::

    template = registry.Attachment.Template.insert(...)

Add a Document without file but with a Template::

    document = registry.Attachment.Document.insert(template=template, ...)
    document.generate_file()

.. warning::

    the ``get_file`` method may re-create the document with historization if the data have been changed


``Model.Attachment.Parser``
```````````````````````````

It is an unSQL model, the goal is to transform the data from ``Model.Attachment.Document`` to Json format to create the file::

    @register(Model.Attachment.Parser)
    class MyParser(Model.Attachment.Parser):

        @classmethod
        def serialize(cls, data):
            # return serialize data

        @classmethod
        def check_if_file_must_be_generated(cls, template, document):
            # return a Boolean to know if the file must be regenerate


``Model.Attachment.Template``
`````````````````````````````

The template describe how to generate the document file in function of of the data in the document.

The ``Model.Attachment.Template`` can be used directly an Template type class must be add with polymorphism::

    @register(Model.Attachment)
    class Template:

        def get_template_type(self):
            res = super(MyTemplateType, self).get_template_type()
            res.update({'MyTemplateType': 'My type label'})
            return res


    @register(Model.Attachment.Template)
    class MyTemplateType(Model.Attachment.Template):
        TYPE = 'MyTypeOfTemplate'

        uuid = UUID(primary_key=True, nullable=False, binary=False, 
                    foreign_key=Model.Attachment.Template.use('uuid').options(ondelete='cascade'))
        # other field need for the template

        def render(self):
            # generate a file
            return file

or on the same table::

    @register(Model.Attachment)
    class Template:

        def get_template_type(self):
            res = super(MyTemplateType, self).get_template_type()
            res.update({'MyTemplateType': 'My type label'})
            return res


    @register(Model.Attachment.Template,
              tablename=Model.Attachment.Template)
    class MyTemplateType(Model.Attachment.Template):
        TYPE = 'MyTypeOfTemplate'

        def render(self):
            # generate a file
            return file
