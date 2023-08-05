Tilapya: TransLink API, in Python
=================================

**Tilapya** is a Python wrapper around the `TransLink Open API <https://developer.translink.ca/>`_,
which provides real-time transit information for the Metro Vancouver region.

Tilapya has three interfaces which correspond directly to components of the TransLink Open API:

* **RTTI**: Real-Time Transit Information
* **RTDS**: Regional Traffic Data System
* **GTFSRT**: GTFS-realtime feeds

Tilapya is more than a thin wrapper around the underlying REST APIs.
It smooths over some of the quirky and inconvenient responses,
and guarantees a consistent schema in returned responses.


Installation
------------

Install Tilapya using `pip <https://pip.pypa.io>`_::

    $ pip install tilapya

The source is also `available on GitHub <https://github.com/carsonyl/tilapya>`_.

Getting started
---------------

Use of the TransLink Open API, and thus Tilapya, requires an API key.
If you don't already have an API key, you can get one by registering for an account at
https://developer.translink.ca/Account/Register.


=======
History
=======

0.1.0
------------------

* Initial version.


