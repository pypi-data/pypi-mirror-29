Reloadable
==========

|Build Status| |codecov| |Python Versions| |pypi|

Reruns a function upon failure

Usage
-----

Reloadable
==========

The function ``my_func`` will run indefinitely until it stops raising exceptions,
which will never happen in this case.

.. code-block:: python

    from reloadable import reloadable

    @reloadable()
    def my_func():
        raise Exception('Oops')

This module is useful when we want to run something forever, like a code
that connects to a queue en fetches messages. Eventually it may disconnect and
raise an error trying to fetch a message, so reloadable can retry connecting.

.. code-block:: python

    @reloadable()
    def get_message():
        conn = Queue(host='...', password='...')

        while True:
            message = conn.fetch_message()
            # probably process message afterwards...

You can config a callback function that receives an exception, which will be
called if it occurs.

.. code-block:: python

    def shit_happens(exception):
        logger.exception(exception)

    @reloadable(exception_callback=shit_happens)
    def dont_stop():
        raise Exception('Deal with it')

You can also wait some time before the next respawn

.. code-block:: python

    @reloadable(sleep_time=7)  # wait 7 seconds before running `get_message` after a failure 
    def get_message():
        # some code...

You can always stop reloadable with a ``KeyboardInterrupt`` exception
(usually triggered by ``^C``, but not necessarily).

Another option is to configure the stop condition exception.

.. code-block:: python

    @reloadable(stop_condition_exception=ValueError)
    def i_will_stop():
        raise ValueError('something went wrong')

Or you can define it globally, which will be used if local stop condition wasn't defined

.. code-block:: python

    from reloadable import reloadable, configure

    configure(stop_condition_exception=KeyError)

    @reloadable()
    def i_will_stop():
        raise KeyError('...')

You may also want to limit the number of times that the decorator should try
rerun the function. If the function is called ``max_reloads`` times without a
success, it raises the last error.

.. code-block:: python

    from reloadable import reloadable

    @reloadable(max_reloads=2)
    def a_func():
        raise KeyError('...')

Alternatively you can disable the reloadable decorator via configuration,
which is useful during unittests.

.. code-block:: python

    from reloadable import configure, reloadable

    configure(enabled=False)

    @reloadable()  # When disabled, it does nothing
    def i_am_free():
        return '\o/'


Retry on Error
==============

The ``@retry_on_error`` decorator is useful when you want to retry something on
error, but return the result once the decorated function finishes it's
execution with success.

.. code-block:: python

   import requests
   from reloadable.decorators import retry_on_error


   @retry_on_error(max_reloads=3)
   def my_request():
       response = requests.get("https://www.sieve.com.br")

       # raises an error for 4xx and 5xx status codes
       response.raise_for_status()

       return response.content

Tests
-----
``python -m unittest -v tests``

Installation
------------
``pip install reloadable``


.. |Build Status| image:: https://travis-ci.org/diogommartins/reloadable.svg?branch=master
   :target: https://travis-ci.org/diogommartins/reloadable

.. |codecov| image:: https://codecov.io/gh/diogommartins/reloadable/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/diogommartins/reloadable

.. |pypi| image:: https://img.shields.io/pypi/v/reloadable.svg
   :target: https://pypi.python.org/pypi/reloadable

.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/reloadable.svg
   :target: https://pypi.python.org/pypi/reloadable


