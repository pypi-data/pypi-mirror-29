django-puppeteer-pdf
==================

.. image:: https://badge.fury.io/py/django-puppeteer-pdf.png
    :target: http://badge.fury.io/py/django-puppeteer-pdf
    :alt: Latest version

.. image:: https://travis-ci.org/namespace/django-puppeteer-pdf.png?branch=master
   :target: https://travis-ci.org/namespace/django-puppeteer-pdf
   :alt: Travis-CI

.. image:: https://img.shields.io/pypi/dm/django-puppeteer-pdf.svg
    :target: https://badge.fury.io/py/django-puppeteer-pdf
    :alt: Number of PyPI downloads on a month


Converts HTML to PDF
--------------------

Provides Django views to wrap the HTML to PDF conversion of the `puppeteer <https://github.com/GoogleChrome/puppeteer>`_.

Forked from: `django-wkhtmltopdf <https://github.com/incuna/django-wkhtmltopdf>`_.

Requirements
------------

Install the `puppeteer-pdf cli  <https://www.npmjs.com/package/puppeteer-pdf>`_.

Python 2.6+ and 3.3+ are supported.


Installation
------------

Run ``pip install django-puppeteer-pdf``.

Add ``'puppeteer_pdf'`` to ``INSTALLED_APPS`` in your ``settings.py``.

By default it will execute the first ``puppeteer-pdf`` command found on your ``PATH``.

If you can't add puppeteer-pdf to your ``PATH``, you can set ``PUPPETEER_PDF_CMD`` to a
specific executable:

e.g. in ``settings.py``: ::

    PUPPETEER_PDF_CMD = '/path/to/my/puppeteer-pdf'

or alternatively as env variable: ::

    export PUPPETEER_PDF_CMD=/path/to/my/puppeteer-pdf

You may also set ``PUPPETEER_PDF_CMD_OPTIONS`` in ``settings.py`` to a dictionary
of default command-line options.

The default is: ::

    PUPPETEER_PDF_CMD_OPTIONS = {
        'format': 'A4',
    }

Documentation
-------------

Documentation is available at http://django-puppeteer-pdf.readthedocs.org/en/latest/.

License
-------

MIT licensed. See the bundled `LICENSE <https://github.com/namespace/django-puppeteer-pdf/blob/master/LICENSE>`_ file for more details.
