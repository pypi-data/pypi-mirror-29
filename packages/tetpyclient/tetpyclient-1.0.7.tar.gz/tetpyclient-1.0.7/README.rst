
===========================================================
TetPyClient - The Python API SDK for Tetration Analytics
===========================================================

TetPyClient is the Tetration Analytics SDK API for Python, which allows
Python developers to use the Tetration REST API (called OpenAPI). The latest
documentation may be found under the User Guide on the Tetration UI.

Quick Start
-----------
Python 2.7 (or above) or Python 3.6 (or above) is required.
To install the library, use ``pip install``:

.. code-block:: sh

    $ pip install tetpyclient
    $ python
    >>> from tetpyclient import RestClient
    >>> rc = RestClient('<API_ENDPOINT>', credentials_file='<CREDENTIALS_FILE_PATH>')
    >>> resp = rc.get(...)
    >>> print resp.status_code, resp.text

Development
-----------

Please see the Tetration Analytics User Guide section on OpenAPI for
reference on how to generate API keys and examples to use the REST client.

Getting Help
------------

Please contact support@tetrationanalytics.com.
