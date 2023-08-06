========
Examples
========

------------------
Mensa Morgenstelle
------------------

You can crawl and parse the menues of Mensa Morgenstelle with

.. code:: python

    >>> from stuweparser import crawler, parser
    >>> url_morgenstelle = "http://www.my-stuwe.de/mensa/mensa-morgenstelle-tuebingen"
    >>> html_morgenstelle = crawler.crawl(url_morgenstelle)
    >>> menues_morgenstelle = parser.parse_menues(html_morgenstelle)


-------------------
Mensa Wilhelmstraße
-------------------

You can crawl and parse the menues of Mensa Wilhelmstrasse with

.. code:: python

    >>> from stuweparser import crawler, parser
    >>> url_wilhelmstrasse = "http://www.my-stuwe.de/mensa/mensa-wilhelmstrasse-tuebingen"
    >>> html_wilhelmstrasse = crawler.crawl(url_wilhelmstrasse)
    >>> menues_wilhelmstrasse = parser.parse_menues(html_wilhelmstrasse)
