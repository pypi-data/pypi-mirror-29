
======================
XREA API wrapper
======================
.. image:: https://img.shields.io/pypi/v/xrea.svg
    :target: https://pypi.python.org/pypi/xrea

.. image:: https://img.shields.io/pypi/l/xrea.svg
    :target: https://pypi.python.org/pypi/xrea

.. image:: https://img.shields.io/pypi/pyversions/xrea.svg
    :target: https://pypi.python.org/pypi/xrea

This package is simple implementation of XREA API(https://apidoc.xrea.com) wrapper with Python 3.

"XREA" is the web hosting service in Japan.

Short description in Japanese
=============================
このPythonパッケージはXREA API(https://apidoc.xrea.com)のラッパーです。
Python3系(3.4以降)で使えます。


Supported services
==================

- XREA(https://www.xrea.com)
- CoreServer(https://www.coreserver.jp)


Requirements
============

works with

- Python 3.4+
- requests

Installation
============

via pipenv
-----------

.. code:: bash

    $ pipenv install xrea


via pip
--------

.. code:: bash

    $ pip install xrea

via setup.py
-------------

.. code:: bash

    $ python setup.py install


Examples
==========

Init:

.. code:: pycon

    >>> from xrea import Xrea # for CoreServer: from xrea import CoreServer
    ...
    ... account = "foo" # your account
    ... server_name = "z123456.xrea.com" # your server
    ... api_secret_key = "zajxTrzkHBGkRRfvWs5w397jZFqQKC8L" # your api_secret_key
    >>> xrea = Xrea(account=account, server_name=server_name, api_secret_key=api_secret_key)

    # for CoreServer
    # xrea = CoreServer(account=account, server_name=server_name, api_secret_key=api_secret_key)

Call site/list without optional params:

.. code:: pycon

    >>> response = xrea.site.list()
    >>> pprint(response.result)
    {'1': {'domain': 'blank',
           'ip': '11.22.33.44,
           'no': 1,
           'nodir': 0,
           'phpver': 'php71',
           'redirect_url': '',
           'ssl_info': [],
           'ssl_status': 0},
     '2': {'domain': 'abcde.example.info',
           'ip': '11.22.33.44',
           'no': 2,
           'nodir': 0,
           'phpver': 'php71',
           'redirect_url': '',
           'ssl_info': [],
           'ssl_status': 1}}

Call log/log_list with optional params:

.. code:: pycon

    >>> response2 = xrea.log.log_list(type='analog')
    >>> pprint(response2.result)
    {'abcde.example.info': [{'filedate': '2018-01-14',
                             'filename': 'abcde.example.info.html'},
                            {'filedate': '2018-01-13',
                             'filename': 'abcde.example.info.1.html'}]}

Call aaa/bbb (not valid)

.. code:: pycon

    >>> response3 = xrea.aaa.bbb(foo='12345')
    xrea.error.XreaApiResponseError: [status: 404, error: 100002]page_name:正しくありません


Author
=======

**NAKAMORI Ryosuke** - https://github.com/tpdn

Licence
========

BSD-2-Clause
