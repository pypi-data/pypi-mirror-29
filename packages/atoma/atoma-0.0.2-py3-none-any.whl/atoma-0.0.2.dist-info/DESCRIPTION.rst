Atoma
=====

.. image:: https://travis-ci.org/NicolasLM/atoma.svg?branch=master
    :target: https://travis-ci.org/NicolasLM/atoma
.. image:: https://coveralls.io/repos/github/NicolasLM/atoma/badge.svg?branch=master
    :target: https://coveralls.io/github/NicolasLM/atoma?branch=master

Atom and RSS feed parser for Python 3.

Quickstart
----------

Install Atoma with pip::

   pip install atoma

Load and parse an Atom XML file:

.. code:: python

    >>> import atoma
    >>> feed = atoma.parse_rss_file('rss-feed.xml')
    >>> feed.description
    'The blog relating the daily life of web agency developers'
    >>> len(feed.items)
    5

Parsing feeds from the Internet is easy as well:

.. code:: python

    >>> import atoma, requests
    >>> response = requests.get('http://lucumr.pocoo.org/feed.atom')
    >>> feed = atoma.parse_atom_bytes(response.content)
    >>> feed.title.value
    "Armin Ronacher's Thoughts and Writings"

Features
--------

* RSS 2.0 - `RSS 2.0 Specification <http://cyber.harvard.edu/rss/rss.html>`_
* Atom Syndication Format v1 - `RFC4287 <https://tools.ietf.org/html/rfc4287>`_
* Typed: feeds decomposed into meaningful Python objects
* Secure: uses defusedxml to load untrusted feeds
* Compatible with Python 3.6+

Security warning
----------------

If you use this library to display content from feeds in a web page, you NEED
to clean the HTML contained in the feeds to prevent `Cross-site scripting (XSS)
<https://en.wikipedia.org/wiki/Cross-site_scripting>`_. The `bleach
<https://github.com/mozilla/bleach>`_ library is recommended for cleaning feeds.

Useful Resources
----------------

To use this library a basic understanding of feeds is required. For Atom, the
`Introduction to Atom <https://validator.w3.org/feed/docs/atom.html>`_ is a must
read. The `RFC 4287 <https://tools.ietf.org/html/rfc4287>`_ can help lift some
ambiguities. Finally the `feed validator <https://validator.w3.org/feed/>`_ is
great to test hand-crafted feeds.

For RSS, the `specification <http://cyber.harvard.edu/rss/rss.html>`_ and
`rssboard.org <http://www.rssboard.org>`_ have a ton of information and
examples.

Non-implemented Features
------------------------

Some seldom used features are not implemented:

* XML signature and encryption
* Atom and most RSS extensions
* Atom content other than `text`, `html` and `xhtml`

License
-------

MIT
Copyright (c) 2018 Nicolas Le Manchet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

