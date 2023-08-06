crawlster - small and light web crawlers
========================================

.. image:: https://readthedocs.org/projects/crawlster/badge/?version=latest
   :target: http://crawlster.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/vladcalin/crawlster.svg?branch=master
   :target: https://travis-ci.org/vladcalin/crawlster

A simple, lightweight web crawling framework


Features:

- HTTP crawling
- Various data extraction methods (regex, css selectors, xpath)
- Very configurable and extensible


What is crawlster?
------------------

Crawlster is a web crawling library designed to build lightweight and reusable
web crawlers. It is very extensible and provides many shortcuts for the most common
tasks in a web crawler, such as HTTP request sending and parsing and info
extraction.

It was created out of need of a lighter framework for web crawling, as an
alternative to `Scrapy <https://scrapy.org/>`_.


Installation
------------

From PyPi:

::

    pip install crawlster


From source:

::

    git clone https://github.com/vladcalin/crawlster.git
    cd crawlster
    python setup.py install


Quick example
-------------

This is the hello world equivalent for this library:


::

   import crawlster
   from crawlster.handlers import JsonLinesHandler


   class MyCrawler(crawlster.Crawlster):
       # items will be saved to items.jsonl
       item_handler = JsonLinesHandler('items.jsonl')

       @crawlster.start
       def step_start(self, url):
           resp = self.http.get(url)
           # we select elements with the expression and we are interested
           # only in the 'href' attribute. Also, we get only the first result
           # for this example
           events_uri = self.extract.css(resp.text, '#events > a', attr='href')[0]
           # we specify what method should be called next
           self.schedule(self.step_events_page, self.urls.join(url, events_uri))

       def step_events_page(self, url):
           resp = self.http.get(url)
           # We extract the content/text of all the selected titles
           events = self.extract.css(resp.text, 'h3.event-title a', content=True)
           for event_name in events:
               # submitting items to be processed by the item handler
               self.submit_item({'event': event_name})


   if __name__ == '__main__':
       # defining the configuration
       config = crawlster.Configuration({
           # the start pages
           'core.start_urls': ['https://www.python.org/'],
           # the method that will process the start pages
           'core.start_step': 'step_start',
           # to see in-depth what happens
           'log.level': 'debug'
       })
       # starting the crawler
       crawler = MyCrawler(config)
       # this will block until everything finishes
       crawler.start()
       # printing some run stats, such as the number of requests, how many items
       # were submitted, etc.
       print(crawler.stats.dump())


Running the above code will fetch the event names from python.org and save them
in a ``items.jsonl`` file in the current directory.

For more advanced usage, consult the
`documentation <http://crawlster.readthedocs.io/en/latest/>`_.

