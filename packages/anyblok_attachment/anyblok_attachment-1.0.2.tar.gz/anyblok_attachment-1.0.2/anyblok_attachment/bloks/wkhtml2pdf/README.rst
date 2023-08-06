.. This file is a part of the AnyBlok / Attachment project
..
..    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

Memento
~~~~~~~

Define tools to convert HTML to PDF with wkhtmltopdf.

To use WkHtml2Pdf in your template is easy::

    @register(Model.Attachment.Template)
    class MyTemplate(Mixin.WkHtml2Pdf):
        ... # template configuration

        def render(self, data):
            html_content = ...
            return self.wkhtml2pdf(html_content)

You may define one or more configuration::

    page_A4 = registry.Attachment.WkHtml2Pdf.Page.insert(
        label="A4", size="A4")
    page_postal_label = registry.Attachment.WkHtml2Pdf.Page.insert(
        label="Postal carrier 1", height=80, width=120)
    wkhtml2pdf = registry.Attachment.WkHtml2Pdf.insert(
        label="A4", page=page_A4, margin_top=20)
    template = registry.Attachment.Template.insert(
        ...,
        wkhtml2pdf_configuration=wkhtml2pdf
    )
    doc = registry.Attachment.Document.insert(
        template=template, data=...)
    doc.get_file()
