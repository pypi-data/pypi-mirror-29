
**This is just a fork of `cbor2`_ by Alex Grönholm.**

.. _cbor2: https://github.com/agronholm/cbor2

This library provides encoding and decoding for the Concise Binary Object Representation (CBOR)
(`RFC 7049`_) serialization format.

There exists another Python CBOR implementation (cbor) which is faster on CPython due to its C
extensions. On PyPy, cbor2 and cbor are almost identical in performance. The other implementation
also lacks documentation and a comprehensive test suite, does not support most standard extension
tags and is known to crash (segfault) when passed a cyclic structure (say, a list containing
itself).

.. _RFC 7049: https://tools.ietf.org/html/rfc7049

Upstream project links
-------------

* `Documentation <http://cbor2.readthedocs.org/>`_
* `Source code <https://github.com/agronholm/cbor2>`_
* `Issue tracker <https://github.com/agronholm/cbor2/issues>`_
