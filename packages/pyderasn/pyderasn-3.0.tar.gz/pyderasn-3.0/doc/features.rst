Features
========

* Basic ASN.1 data types (X.208): BOOLEAN, INTEGER, BIT STRING, OCTET
  STRING, NULL, OBJECT IDENTIFIER, ENUMERATED, all strings, UTCTime,
  GeneralizedTime, CHOICE, ANY, SEQUENCE (OF), SET (OF)
* Size :ref:`constraints <bounds>` checking
* Working with sequences as high level data objects with ability to
  (un)marshall them
* Python 2.7/3.5 compatibility

Why yet another library? `pyasn1 <https://github.com/etingof/pyasn1>`__
had all of this a long time ago. PyDERASN resembles it in many ways. In
practice it should be relatively easy to convert ``pyasn1``'s code to
``pyderasn``'s one. But additionally it offers:

* Small, simple and trying to be reviewable code. Just a single file
* Automatic decoding of :ref:`DEFINED BY <definedby>` fields
* Ability to know :ref:`exact decoded <decoding>` objects offsets and
  lengths inside the binary
* :ref:`Pretty printer <pprinting>` and command-line decoder, that could
  conveniently replace utilities like either ``dumpasn1`` or
  ``openssl asn1parse``
* Some kind of strong typing: SEQUENCEs require the exact **type** of
  settable values, even when they are inherited
* However they do not require tags matching: IMPLICIT/EXPLICIT tags will
  be set automatically in the given sequence
* ``__slots__`` friendliness
* Could be significantly faster. For example parsing of CACert.org's CRL
  under Python 3.5.2:

    :``python -m pyderasn revoke.crl``:
     ~2 min
    :``python -m pyderasn --schema path.to.CertificateList revoke.crl``:
     ~38 sec
    :``pyasn1.decode(asn1Spec=pyasn1.CertificateList())``:
     ~22 min (``pyasn1 == 0.2.3``)

There are drawbacks:

* No old Python versions support
* No BER/CER support
* PyDERASN does **not** have object recreation capable ``repr``-s::

    pyderasn>>> repr(algo_id)
    AlgorithmIdentifier SEQUENCE[OBJECT IDENTIFIER 1.3.14.3.2.26, [UNIV 5] ANY 0500 OPTIONAL]

    pyasn1>>> repr(algo_id)
    AlgorithmIdentifier().setComponents(ObjectIdentifier('1.3.14.3.2.26'), Any(hexValue='0500'))

* Strings are not validated in any way, except just trying to be decoded
  in ``ascii``, ``iso-8859-1``, ``utf-8/16/32`` correspondingly
* No REAL, RELATIVE OID, EXTERNAL, INSTANCE OF, EMBEDDED PDV, CHARACTER STRING
