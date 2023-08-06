more-executors
==============

|Build Status| |Coverage Status|

-  `API documentation <https://rohanpm.github.io/more-executors/>`__
-  `Source <https://github.com/rohanpm/more-executors>`__
-  `PyPI <https://pypi.python.org/pypi/more-executors>`__

This library is intended for use with the
```concurrent.futures`` <https://docs.python.org/3/library/concurrent.futures.html>`__
module. It includes a collection of ``Executor`` implementations in
order to extend the behavior of ``Future`` objects.

Features
--------

-  Futures with implicit retry
-  Futures with transformed output values
-  Futures resolved by a caller-provided polling function
-  Convenience API for creating executors

See the `API
documentation <https://rohanpm.github.io/more-executors/>`__ for
detailed information on usage.

Example
-------

This example combines the map and retry executors to create futures for
HTTP requests running concurrently, decoding JSON responses within the
future and retrying on error.

.. code:: python

    import requests
    from concurrent.futures import as_completed
    from more_executors import Executors


    def get_json(response):
        response.raise_for_status()
        return (response.url, response.json())


    def fetch_urls(urls):
        # Configure an executor:
        # - run up to 4 requests concurrently, in separate threads
        # - run get_json on each response
        # - retry up to several minutes on any errors
        executor = Executors.\
            thread_pool(max_workers=4).\
            with_map(get_json).\
            with_retry()

        # Submit requests for each given URL
        futures = [executor.submit(requests.get, url)
                   for url in urls]

        # Futures API works as normal; we can block on the completed
        # futures and map/retry happens implicitly
        for future in as_completed(futures):
            (url, data) = future.result()
            do_something(url, data)

License
-------

GPLv3

.. |Build Status| image:: https://travis-ci.org/rohanpm/more-executors.svg?branch=master
   :target: https://travis-ci.org/rohanpm/more-executors
.. |Coverage Status| image:: https://coveralls.io/repos/github/rohanpm/more-executors/badge.svg?branch=master
   :target: https://coveralls.io/github/rohanpm/more-executors?branch=master


