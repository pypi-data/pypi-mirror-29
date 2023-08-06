Accern for Python
=================

.. image:: https://raw.githubusercontent.com/Accern/accern-python/master/docs/_static/accern.png
  :target: _static/accern.png

|pypi| |circleci| |sphinx|

.. snip

A python library to consume Accern Realtime Streaming and REST API and get
historical data.

Overview
--------

Accern is a fast-growing NYC startup that is disrupting the way quantitative
hedge funds can gain a competitive advantage using news and social media data.
It currently has the world’s largest financial news coverage, covering over
1 billion public news websites, blogs, financial documents, and social media
websites. Furthermore, Accern derives proprietary analytics from each news
story to help quantitative hedge funds make accurate trading decisions.

Accern consolidates multiple news data feeds into one to help drastically reduce
costs of both small and large hedge funds. With Accern proprietary data filters, we
are able to deliver relevant articles to clients with a 99 percent accuracy rate.
Accern’s delivery mechanism is a RESTful API where it delivers derived analytics
from news articles, including the original article URLs so quantitative hedge
funds can derive their own analytics in-house from the relevant articles.

The Accern library for Python helps users get fast, flexible data structures from
Accern's Streaming and REST APIs and batch historical data.

.. snap

Install
------------

.. code-block:: console

    pip install accern

Quick Start
---------------

1. Contact `support@accern.com`. and inquire about an Accern API token.

2. To quickly start using the Accern API, create an API instance and pass your token:

.. code-block:: python

    from accern import API
    token = 'YOUR TOKEN'
    Client = API(token)

3. Pass params to get filtered data and make an API request.

.. code-block:: python

    schema = {
        'filters': {
            'entity_ticker': 'AAPL'
        }
    }
    resp = Client.request(schema)

3. Accern ``Historical API`` will be available in the future releases.

For more information see the `full documentation
<https://accern-python.readthedocs.io>`_ on Read The Docs.


.. |circleci| image:: https://circleci.com/gh/Accern/accern-python.svg?style=shield&circle-token=4a51eaa89bd79c92bb9df0e48642146ad7091afc
   :target: https://circleci.com/gh/Accern/accern-python

.. |sphinx| image:: https://readthedocs.org/projects/accern-python/badge/?version=latest
   :target: http://accern-python.readthedocs.io/en/latest/?badge=latest

.. |pypi| image:: https://badge.fury.io/py/Accern.svg
   :target: https://badge.fury.io/py/Accern
