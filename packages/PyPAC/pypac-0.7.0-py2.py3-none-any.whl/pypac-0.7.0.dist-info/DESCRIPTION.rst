PyPAC: Proxy auto-config for Python
===================================

.. image:: https://img.shields.io/pypi/v/pypac.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/pypac
.. image:: https://readthedocs.org/projects/pypac/badge/?version=latest
    :target: https://pypac.readthedocs.io/en/latest/?badge=latest
.. image:: https://img.shields.io/travis/carsonyl/pypac.svg?maxAge=2592000
    :target: https://travis-ci.org/carsonyl/pypac
.. image:: https://ci.appveyor.com/api/projects/status/y7nxvu2feu87i39t/branch/master?svg=true
    :target: https://ci.appveyor.com/project/rbcarson/pypac/branch/master
.. image:: https://img.shields.io/coveralls/carsonyl/pypac/HEAD.svg?maxAge=2592000
    :target: https://coveralls.io/github/carsonyl/pypac
.. image:: https://img.shields.io/codacy/grade/71ac103b491d44efb94976ca5ea5d89c.svg?maxAge=2592000
    :target: https://www.codacy.com/app/carsonyl/pypac

PyPAC is a pure-Python library for finding `proxy auto-config (PAC)`_ files and making HTTP requests
that respect them. PAC files are often used in organizations that need fine-grained and centralized control
of proxy settings.

.. _proxy auto-config (PAC): https://en.wikipedia.org/wiki/Proxy_auto-config

PyPAC provides a subclass of a `Requests <http://docs.python-requests.org/en/master/>`_ ``Session``,
so you can start using it immediately, with any PAC file transparently discovered and honoured:

.. code-block:: python

    >>> from pypac import PACSession
    >>> session = PACSession()
    >>> session.get('http://example.org')
    ...

If a PAC file isn't found, then ``PACSession`` acts exactly like a regular ``Session``.

PyPAC can find PAC files according to the DNS portion of the `Web Proxy Auto-Discovery (WPAD)`_ protocol.
On Windows, PyPAC can also obtain the PAC file URL from the Internet Options dialog, via the registry.

.. _Web Proxy Auto-Discovery (WPAD): https://en.wikipedia.org/wiki/Web_Proxy_Autodiscovery_Protocol

If you're looking to add *basic* PAC functionality to a library that you're using,
try the :func:`pac_context_for_url <pypac.pac_context_for_url>` context manager:

.. code-block:: python

   from pypac import pac_context_for_url
   import boto3

   with pac_context_for_url('https://example.amazonaws.com'):
       client = boto3.client('sqs')
       client.list_queues()

This sets up proxy environment variables at the start of the scope, based on any auto-discovered PAC and the given URL.
:func:`pac_context_for_url <pypac.pac_context_for_url>` should work for any library
that honours proxy environment variables.


Features
--------

* The same Requests API that you already know and love
* Honour PAC setting from Windows Internet Options
* Follow DNS Web Proxy Auto-Discovery protocol
* Proxy authentication pass-through
* Proxy failover and load balancing

PyPAC supports Python 2.7 and 3.4+.


Installation
------------

Install PyPAC using `pip <https://pip.pypa.io>`_::

    $ pip install pypac


Documentation
-------------

PyPAC's documentation is available at http://pypac.readthedocs.io/.


0.7.0 (2018-02-21)
------------------

- Drop support for Python 3.3.
- Add doc explaining how to use ``pac_context_for_url``.
- Internal changes to dev and test processes.


0.6.0 (2018-01-28)
------------------

- Add ``pac_context_for_url``, a context manager that adds basic PAC functionality
  through proxy environment variables.


0.5.0 (2018-01-18)
------------------

- Accept PAC files served with no ``Content-Type`` header.


0.4.0 (2017-11-07)
------------------

- Add ``recursion_limit`` keyword argument to ``PACSession`` and ``PACFile``.
  The default is an arbitrarily high value (10000), which should cover most applications.
- Exclude port numbers from ``host`` passed to ``FindProxyForURL(url, host)``.


0.3.1 (2017-06-23)
------------------

- Update GitHub username.


0.3.0 (2017-04-12)
------------------
- Windows: Get system auto-proxy config setting using ``winreg`` module.
- Windows: Accept local filesystem paths from system proxy auto-config setting.
- Raise ``PacComplexityError`` when recursion limit is hit while parsing PAC file.
- Support setting ``PACSession.proxy_auth`` and ``ProxyResolver.proxy_auth`` after constructing an instance.
- Narrative docs.


0.2.1 (2017-01-19)
------------------

- Require Js2Py >= 0.43 for Python 3.6 support, and to avoid needing to monkeypatch out ``pyimport``.


0.1.0 (2016-06-12)
------------------

- First release.


