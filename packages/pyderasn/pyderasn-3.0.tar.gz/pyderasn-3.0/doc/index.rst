========================================
PyDERASN -- ASN.1 DER library for Python
========================================

..

    I'm going to build my own ASN.1 library with slots and blobs!
    (C) PyDERASN's author

`ASN.1 <https://en.wikipedia.org/wiki/ASN.1>`__ (Abstract Syntax
Notation One) is a standard for abstract data serialization.
`DER <https://en.wikipedia.org/wiki/Distinguished_Encoding_Rules>`__
(Distinguished Encoding Rules) is a subset of encoding rules suitable
and widely used in cryptography-related stuff. PyDERASN is yet another
library for dealing with the data encoded that way. Although ASN.1 is
written more than 30 years ago by wise Ancients (taken from ``pyasn1``'s
README), it is still often can be seen anywhere in our life.

PyDERASN is `free software <https://www.gnu.org/philosophy/free-sw.html>`__,
licenced under `GNU LGPLv3+ <https://www.gnu.org/licenses/lgpl-3.0.html>`__.

.. figure:: pprinting.png
   :alt: Pretty printing example output

   An example of pretty printed X.509 certificate with automatically
   parsed DEFINED BY fields.

.. toctree::
   :maxdepth: 1

   features
   examples
   reference
   news
   install
   download
   thanks
   feedback
