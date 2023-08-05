******************
User Guide
******************


Quick Example
=============
Here is an incomplete example. See :ref:`advanced-example` below for a more detailed description.

.. before-usage-example

.. code-block:: python

    from mypolr import PolrApi, exceptions

    # Replace with your values
    server_url = 'polr.example.com'
    api_key = '1234567890abcdef'

    # Example url to shorten
    long_url = 'https://some.long.example.com/long/url'

    # Create PolrApi instance
    api = PolrApi(server_url, api_key)

    # Make short urls
    shorted_url = api.shorten(long_url)
    custom_url = api.shorten(long_url, custom=CUSTOM_ENDING)

    # Given a short url ending, find full url and stats:
    lookup_dict = api.lookup(SHORT_URL_ENDING)
    full_url = lookup_dict.get('long_url')
    n_clicks = lookup_dict.get('clicks')

    # Secret urls have an additional key after the short url ending
    # E.g the format <polr root folder> / SHORT_URL_ENDING / URL_KEY:
    secret_url = api.shorten(long_url, is_secret=True)
    # Secret lookups require url_key:
    secret_lookup = api.lookup(SHORT_URL_ENDING, url_key=URL_KEY)

.. after-usage-example

.. before-advanced-example
.. _advanced-example:

Advanced Usage
==============
This section is more thorough than the one above,
and covers the various errors and edge cases you might encounter with the Polr Project API.

The following examples assume the Polr Project to be installed on a server at `https://ti.ny`,
and that a valid API_KEY is stored in a separate module ``my_secrets``.

Set up API
----------
This is how the API would be set up given the aforementioned (and arbitrary) assumptions:


.. code-block:: python

    from mypolr import PolrApi, exceptions
    from my_secrets import api_key

    # Example url to shorten
    long_url = 'https://stackoverflow.com/questions/tagged/python'

    # Your api server url
    server_url = 'https://ti.ny'

    # Create PolrApi instance
    api = PolrApi(server_url, api_key)


Shorten long URLs
-----------------

Given a long url, the :any:`PolrApi.shorten`-method produces a short url on the form ``https://ti.ny / URL_ENDING``:

.. code-block:: python

    try:
        # Generate a short url with automatic mapping
        automatic_url = api.shorten(long_url)
        # Generate a short url with the ending 'soPython'
        custom_url = api.shorten(long_url, custom_ending='soPython')

        print(automatic_url)    # E.g. https://ti.ny/5N3f8
        print(custom_url)       # E.g. https://ti.ny/soPython
    except exceptions.UnauthorizedKeyError:
        print('API_KEY invalid or inactive.')
    except exceptions.CustomEndingUnavailable:
        print('Custom ending is already in use: choose another.')
    except exceptions.QuotaExceededError:
        print('User account associated with API_KEY has exceeded their quota.')
    except exceptions.ServerOrConnectionError:
        print('Check server and/or connection status.')
    except exceptions.BadApiRequest:
        print('Something was wrong with the request to server.')
    except exceptions.BadApiResponse:
        print('Response from server was not valid JSON.')

.. _lookup_example:

Lookup short URLs
-----------------
The :any:`PolrApi.lookup`-method accepts either a short url ending, or a full short url, and returns ``False`` if no
url is found, or returns a dictionary of info about the link.

.. code-block:: python

    try:
        # Lookup short url to get info
        url_info = api.lookup('https://ti.ny/soPython')
        url_info = api.lookup('soPython')
        if url_info is False:
            print('No url found with that ending.')
        else:
            print('Long url is: {}'.format(url_info.get('long_url')))
    except exceptions.UnauthorizedKeyError:
        print('API_KEY invalid or inactive.')
    except exceptions.ServerOrConnectionError:
        print('Check server and/or connection status.')
    except exceptions.BadApiRequest:
        print('Something was wrong with the request to server.')
    except exceptions.BadApiResponse:
        print('Response from server was not valid JSON.')

Lookup result
'''''''''''''
Response of a successful lookup is a dictionary á la something like this:

.. code-block:: python

    {
        'clicks': 42,
        'created_at':
            {
                'date': '2017-12-03 00:40:45.000000',
                'timezone': 'UTC',
                'timezone_type': 3
            },
        'long_url': 'https://stackoverflow.com/questions/tagged/python',
        'updated_at':
            {
                'date': '2017-12-03 00:40:45.000000',
                'timezone': 'UTC',
                'timezone_type': 3
            }
    }


Secret URLs
-----------

Secret urls differ from normal short urls in the way that they have the form ``https://ti.ny / URL_ENDING / URL_KEY``.
The additional part, URL_KEY, is required as a parameter when doing lookup of secret urls.

.. code-block:: python

    # Working with secret urls
    secret_long_url = 'https://stackoverflow.com/questions/tagged/cryptography'

    # Can still use both automatic or custom mapping
    secret_url = api.shorten(secret_long_url, is_secret=True)
    secret_custom_url = api.shorten(secret_long_url, custom_ending='soSecret', is_secret=True)

    print(secret_url)           # E.g. https://ti.ny/gztns/bXL2
    print(secret_custom_url)    # E.g. https://ti.ny/soSecret/F3iH

    try:
        secret_url_info = api.lookup('soPython', url_key='F3iH')
    except exceptions.UnauthorizedKeyError:
        print('Your URL_KEY is wrong, or the API_KEY is invalid.')

.. note:: The ``exceptions.UnauthorizedKeyError`` in the previous example is the sole catch
          in order to simplify the example about secret lookups,
          but as seen in :ref:`lookup_example` above,
          this isn't the only exception that could be raised.

Ignoring Errors
---------------
The :any:`exceptions.no_raise`-decorator has been applied to both
:any:`PolrApi.shorten_no_raise` and :any:`PolrApi.lookup_no_raise`,
and will act as their corresponding normal methods,
but will return ``None`` instead of raising **module** exceptions upon errors.

The :any:`PolrApi.lookup_no_raise`-method still returns ``False`` when no url is found (if no error occurs).

.. code-block:: python

    # Use the _no_raise-methods to return None instead of exceptions as above
    short_url = api.shorten_no_raise(long_url)
    url_info = api.lookup_no_raise('soPython')

    if short_url is None:
        print('There was an error with the url shortening process.')

    if url_info is False:
        print('No url with that ending.')
    elif url_info is None:
        print('There was an error with the url lookup process.')

.. warning:: Even though the use of `\*_no_raise`-methods allows for easy check of failure/success,
             there is no feedback of what went wrong upon failure.

.. note:: The `\*_no_raise`-methods will still raise *other* exceptions, and
          **ONLY** errors derived from :any:`MypolrError` will instead return ``None``.

.. after-advanced-example

CLI usage
=========

CLI-support was added in *version 1.3* and is supported for Python >= 3.4.

Examples
--------

Assuming Polr Project is intalled on *https://ti.ny* and that your API_KEY is *abcdef1234567890*,
below is a few examples. Read full description of the interface further down.

Basic example, performs the default :any:`PolrApi.shorten` action.

.. code-block:: none

   python -m mypolr http://some.long.example.com --server https://ti.ny --key abcdef1234567890

Set ``-l``/``--lookup`` option to perform :any:`PolrApi.lookup` action.

.. code-block:: none

   python -m mypolr https://ti.ny/5Bn8V --lookup

In the previous example, no server configuration values were used.
They, including the key, can be saved **in plaintext** to *~/.mypolr/config.ini* with the ``--save`` option.
This will load the saved values if not presented upon invocation.

.. code-block:: none

   python -m mypolr --server https://ti.ny --key abcdef1234567890 --save

Clear the *config.ini*-file with the ``--clear`` option.

.. code-block:: none

   python -m mypolr --clear

CLI description
---------------

.. argparse::
   :module: mypolr.cli
   :func: make_argparser
   :prog: mypolr
