Examples
========

.. contents::

Schema definition
-----------------

Let's try to parse X.509 certificate. We have to define our structures
based on ASN.1 schema descriptions.

.. list-table::
   :header-rows: 1

   * - ASN.1 specification
     - pyderasn's code
   * - ::

            Certificate  ::=  SEQUENCE  {
                tbsCertificate       TBSCertificate,
                signatureAlgorithm   AlgorithmIdentifier,
                signatureValue       BIT STRING  }
     - ::

            class Certificate(Sequence):
                schema = (
                    ("tbsCertificate", TBSCertificate()),
                    ("signatureAlgorithm", AlgorithmIdentifier()),
                    ("signatureValue", BitString()),
                )
   * - ::

            AlgorithmIdentifier  ::=  SEQUENCE  {
                algorithm    OBJECT IDENTIFIER,
                parameters   ANY DEFINED BY algorithm OPTIONAL  }
     - ::

            class AlgorithmIdentifier(Sequence):
                schema = (
                    ("algorithm", ObjectIdentifier()),
                    ("parameters", Any(optional=True)),
                )
   * - ::

            TBSCertificate  ::=  SEQUENCE  {
                version         [0]  EXPLICIT Version DEFAULT v1,
                serialNumber         CertificateSerialNumber,
                signature            AlgorithmIdentifier,
                issuer               Name,
                validity             Validity,
                subject              Name,
                subjectPublicKeyInfo SubjectPublicKeyInfo,
                issuerUniqueID  [1]  IMPLICIT UniqueIdentifier OPTIONAL,
                subjectUniqueID [2]  IMPLICIT UniqueIdentifier OPTIONAL,
                extensions      [3]  EXPLICIT Extensions OPTIONAL  }
     - ::

            class TBSCertificate(Sequence):
                schema = (
                    ("version", Version(expl=tag_ctxc(0), default="v1")),
                    ("serialNumber", CertificateSerialNumber()),
                    ("signature", AlgorithmIdentifier()),
                    ("issuer", Name()),
                    ("validity", Validity()),
                    ("subject", Name()),
                    ("subjectPublicKeyInfo", SubjectPublicKeyInfo()),
                    ("issuerUniqueID", UniqueIdentifier(impl=tag_ctxp(1), optional=True)),
                    ("subjectUniqueID", UniqueIdentifier(impl=tag_ctxp(2), optional=True)),
                    ("extensions", Extensions(expl=tag_ctxc(3), optional=True)),
                )
   * - ::

            Version  ::=  INTEGER  {  v1(0), v2(1), v3(2)  }
     - ::

            class Version(Integer):
                schema = (("v1", 0), ("v2", 1), ("v3", 2))
   * - ::

            CertificateSerialNumber  ::=  INTEGER
     - ::

            class CertificateSerialNumber(Integer):
                pass
   * - ::

            Validity ::= SEQUENCE {
                notBefore      Time,
                notAfter       Time }
            Time ::= CHOICE {
                utcTime        UTCTime,
                generalTime    GeneralizedTime }
     - ::

            class Validity(Sequence):
                schema = (
                    ("notBefore", Time()),
                    ("notAfter", Time()),
                )
            class Time(Choice):
                schema = (
                    ("utcTime", UTCTime()),
                    ("generalTime", GeneralizedTime()),
                )
   * - ::

            SubjectPublicKeyInfo  ::=  SEQUENCE  {
                algorithm            AlgorithmIdentifier,
                subjectPublicKey     BIT STRING  }
     - ::

            class SubjectPublicKeyInfo(Sequence):
                schema = (
                    ("algorithm", AlgorithmIdentifier()),
                    ("subjectPublicKey", BitString()),
                )
   * - ::

            UniqueIdentifier  ::=  BIT STRING
     - ::

            class UniqueIdentifier(BitString):
                pass
   * - ::

            Name ::= CHOICE { rdnSequence  RDNSequence }

            RDNSequence ::= SEQUENCE OF RelativeDistinguishedName

            RelativeDistinguishedName ::= SET SIZE (1..MAX) OF AttributeTypeAndValue

            AttributeTypeAndValue ::= SEQUENCE { type AttributeType, value AttributeValue }

            AttributeType ::= OBJECT IDENTIFIER

            AttributeValue ::= ANY -- DEFINED BY AttributeType
     - ::

            class Name(Choice):
                schema = (("rdnSequence", RDNSequence()),)
            class RDNSequence(SequenceOf):
                schema = RelativeDistinguishedName()
            class RelativeDistinguishedName(SetOf):
                schema = AttributeTypeAndValue()
                bounds = (1, float("+inf"))
            class AttributeTypeAndValue(Sequence):
                schema = (
                    ("type", AttributeType()),
                    ("value", AttributeValue()),
                )
            class AttributeType(ObjectIdentifier):
                pass
            class AttributeValue(Any):
                pass
   * - ::

            Extensions ::=  SEQUENCE SIZE (1..MAX) OF Extension

            Extension  ::=  SEQUENCE  {
                extnID      OBJECT IDENTIFIER,
                critical    BOOLEAN DEFAULT FALSE,
                extnValue   OCTET STRING
                }
     - ::

            class Extensions(SequenceOf):
                schema = Extension()
                bounds = (1, float("+inf"))
            class Extension(Sequence):
                schema = (
                    ("extnID", ObjectIdentifier()),
                    ("critical", Boolean(default=False)),
                    ("extnValue", OctetString()),
                )

We are ready to decode PayPal's certificate from Go `encoding/asn1
<https://golang.org/pkg/encoding/asn1/>`__ test suite (assuming that
it's DER encoded representation is already in ``raw`` variable)::

    >>> crt, tail = Certificate().decode(raw)
    >>> crt
    Certificate SEQUENCE[TBSCertificate SEQUENCE[[0] EXPLICIT Version
        INTEGER v3 OPTIONAL, CertificateSerialNumber INTEGER 61595,
        AlgorithmIdentifier SEQUENCE[OBJECT IDENTIFIER 1.2.840.113549.1.1.5...

Pretty printing
---------------

There is huge output. Let's pretty print it::

    >>> print(pprint(crt))
        0   [1,3,1604] Certificate SEQUENCE
        4   [1,3,1453]  . tbsCertificate: TBSCertificate SEQUENCE
       10-2 [1,1,   1]  . . version: [0] EXPLICIT Version INTEGER v3 OPTIONAL
       13   [1,1,   3]  . . serialNumber: CertificateSerialNumber INTEGER 61595
       18   [1,1,  13]  . . signature: AlgorithmIdentifier SEQUENCE
       20   [1,1,   9]  . . . algorithm: OBJECT IDENTIFIER 1.2.840.113549.1.1.5
       31   [0,0,   2]  . . . parameters: [UNIV 5] ANY OPTIONAL
                        . . . . 05:00
       33   [0,0, 278]  . . issuer: Name CHOICE rdnSequence
       33   [1,3, 274]  . . . rdnSequence: RDNSequence SEQUENCE OF
       37   [1,1,  11]  . . . . 0: RelativeDistinguishedName SET OF
       39   [1,1,   9]  . . . . . 0: AttributeTypeAndValue SEQUENCE
       41   [1,1,   3]  . . . . . . type: AttributeType OBJECT IDENTIFIER 2.5.4.6
       46   [0,0,   4]  . . . . . . value: [UNIV 19] AttributeValue ANY
                        . . . . . . . 13:02:45:53
    [...]
     1461   [1,1,  13]  . signatureAlgorithm: AlgorithmIdentifier SEQUENCE
     1463   [1,1,   9]  . . algorithm: OBJECT IDENTIFIER 1.2.840.113549.1.1.5
     1474   [0,0,   2]  . . parameters: [UNIV 5] ANY OPTIONAL
                        . . . 05:00
     1476   [1,2, 129]  . signatureValue: BIT STRING 1024 bits
                        . . 68:EE:79:97:97:DD:3B:EF:16:6A:06:F2:14:9A:6E:CD
                        . . 9E:12:F7:AA:83:10:BD:D1:7C:98:FA:C7:AE:D4:0E:2C
     [...]

    Trailing data: 0a

Let's parse that output, human::

       10-2 [1,1,   1]  . . version: [0] EXPLICIT Version INTEGER v3 OPTIONAL
       ^  ^  ^ ^    ^   ^   ^        ^            ^       ^       ^  ^
       0  1  2 3    4   5   6        7            8       9       10 11

::

       20   [1,1,   9]  . . . algorithm: OBJECT IDENTIFIER 1.2.840.113549.1.1.5
       ^     ^ ^    ^   ^     ^          ^                 ^
       0     2 3    4   5     6          9                 10

::

       33   [0,0, 278]  . . issuer: Name CHOICE rdnSequence
       ^     ^ ^    ^   ^   ^       ^    ^      ^
       0     2 3    4   5   6       8    9      10

:0:
 Offset of the object, where its DER encoding begins.
 Pay attention that it does **not** include explicit tag.
:1:
 If explicit tag exists, then this is its length (tag + encoded length).
:2:
 Length of object's tag. For example CHOICE does not have its own tag,
 so it is zero.
:3:
 Length of encoded length.
:4:
 Length of encoded value.
:5:
 Visual indentation to show the depth of object in the hierarchy.
:6:
 Object's name inside SEQUENCE/CHOICE.
:7:
 If either IMPLICIT or EXPLICIT tag is set, then it will be shown
 here. "IMPLICIT" is omitted.
:8:
 Object's class name, if set. Omitted if it is just an ordinary simple
 value (like with ``algorithm`` in example above).
:9:
 Object's ASN.1 type.
:10:
 Object's value, if set. Can consist of multiple words (like OCTET/BIT
 STRINGs above). We see ``v3`` value in Version, because it is named.
 ``rdnSequence`` is the choice of CHOICE type.
:11:
 Possible other flags like OPTIONAL and DEFAULT, if value equals to the
 default one, specified in the schema.

As command line utility
-----------------------

You can decode DER files using command line abilities and get the same
picture as above by executing::

    % python -m pyderasn --schema tests.test_crts:Certificate path/to/file

If there is no schema for you file, then you can try parsing it without,
but of course IMPLICIT tags will often make it impossible. But result is
good enough for the certificate above::

    % python -m pyderasn path/to/file
        0   [1,3,1604]  . >: SEQUENCE OF
        4   [1,3,1453]  . . >: SEQUENCE OF
        8   [0,0,   5]  . . . . >: [0] ANY
                        . . . . . A0:03:02:01:02
       13   [1,1,   3]  . . . . >: INTEGER 61595
       18   [1,1,  13]  . . . . >: SEQUENCE OF
       20   [1,1,   9]  . . . . . . >: OBJECT IDENTIFIER 1.2.840.113549.1.1.5
       31   [1,1,   0]  . . . . . . >: NULL
       33   [1,3, 274]  . . . . >: SEQUENCE OF
       37   [1,1,  11]  . . . . . . >: SET OF
       39   [1,1,   9]  . . . . . . . . >: SEQUENCE OF
       41   [1,1,   3]  . . . . . . . . . . >: OBJECT IDENTIFIER 2.5.4.6
       46   [1,1,   2]  . . . . . . . . . . >: PrintableString PrintableString ES
    [...]
     1409   [1,1,  50]  . . . . . . >: SEQUENCE OF
     1411   [1,1,   8]  . . . . . . . . >: OBJECT IDENTIFIER 1.3.6.1.5.5.7.1.1
     1421   [1,1,  38]  . . . . . . . . >: OCTET STRING 38 bytes
                        . . . . . . . . . 30:24:30:22:06:08:2B:06:01:05:05:07:30:01:86:16
                        . . . . . . . . . 68:74:74:70:3A:2F:2F:6F:63:73:70:2E:69:70:73:63
                        . . . . . . . . . 61:2E:63:6F:6D:2F
     1461   [1,1,  13]  . . >: SEQUENCE OF
     1463   [1,1,   9]  . . . . >: OBJECT IDENTIFIER 1.2.840.113549.1.1.5
     1474   [1,1,   0]  . . . . >: NULL
     1476   [1,2, 129]  . . >: BIT STRING 1024 bits
                        . . . 68:EE:79:97:97:DD:3B:EF:16:6A:06:F2:14:9A:6E:CD
                        . . . 9E:12:F7:AA:83:10:BD:D1:7C:98:FA:C7:AE:D4:0E:2C
    [...]

If you have got dictionaries with ObjectIdentifiers, like example one
from ``tests/test_crts.py``::

    some_oids = {
        "1.2.840.113549.1.1.1": "id-rsaEncryption",
        "1.2.840.113549.1.1.5": "id-sha1WithRSAEncryption",
        [...]
        "2.5.4.10": "id-at-organizationName",
        "2.5.4.11": "id-at-organizationalUnitName",
    }

then you can pass it to pretty printer to see human readable OIDs::

    % python -m pyderasn --oids tests.test_crts:some_oids path/to/file
    [...]
       37   [1,1,  11]  . . . . . . >: SET OF
       39   [1,1,   9]  . . . . . . . . >: SEQUENCE OF
       41   [1,1,   3]  . . . . . . . . . . >: OBJECT IDENTIFIER id-at-countryName (2.5.4.6)
       46   [1,1,   2]  . . . . . . . . . . >: PrintableString PrintableString ES
       50   [1,1,  18]  . . . . . . >: SET OF
       52   [1,1,  16]  . . . . . . . . >: SEQUENCE OF
       54   [1,1,   3]  . . . . . . . . . . >: OBJECT IDENTIFIER id-at-stateOrProvinceName (2.5.4.8)
       59   [1,1,   9]  . . . . . . . . . . >: PrintableString PrintableString Barcelona
       70   [1,1,  18]  . . . . . . >: SET OF
       72   [1,1,  16]  . . . . . . . . >: SEQUENCE OF
       74   [1,1,   3]  . . . . . . . . . . >: OBJECT IDENTIFIER id-at-localityName (2.5.4.7)
       79   [1,1,   9]  . . . . . . . . . . >: PrintableString PrintableString Barcelona
    [...]

Descriptive errors
------------------

If you have bad DER, then errors will show you where error occurred::

    % python -m pyderasn --schema tests.test_crts:Certificate path/to/bad/file
    Traceback (most recent call last):
    [...]
    pyderasn.DecodeError: UTCTime (tbsCertificate.validity.notAfter.utcTime) (at 328) invalid UTCTime format

::

    % python -m pyderasn path/to/bad/file
    [...]
    pyderasn.DecodeError: UTCTime (0.SequenceOf.4.SequenceOf.1.UTCTime) (at 328) invalid UTCTime format

You can see, so called, decode path inside the structures:
``tbsCertificate`` -> ``validity`` -> ``notAfter`` -> ``utcTime`` and
that object at byte 328 is invalid.

X.509 certificate creation
--------------------------

Let's create some simple self-signed X.509 certificate from the ground::

    tbs = TBSCertificate()
    tbs["serialNumber"] = CertificateSerialNumber(10143011886257155224)

    sign_algo_id = AlgorithmIdentifier()
    sign_algo_id["algorithm"] = ObjectIdentifier("1.2.840.113549.1.1.5")
    sign_algo_id["parameters"] = Any(Null())
    tbs["signature"] = sign_algo_id

    rdnSeq = RDNSequence()
    for oid, klass, text in (
            ("2.5.4.6", PrintableString, "XX"),
            ("2.5.4.8", PrintableString, "Some-State"),
            ("2.5.4.7", PrintableString, "City"),
            ("2.5.4.10", PrintableString, "Internet Widgits Pty Ltd"),
            ("2.5.4.3", PrintableString, "false.example.com"),
            ("1.2.840.113549.1.9.1", IA5String, "false@example.com"),
    ):
        attr = AttributeTypeAndValue()
        attr["type"] = AttributeType(oid)
        attr["value"] = AttributeValue(klass(text))
        rdn = RelativeDistinguishedName()
        rdn.append(attr)
        rdnSeq.append(rdn)
    issuer = Name()
    issuer["rdnSequence"] = rdnSeq
    tbs["issuer"] = issuer
    tbs["subject"] = issuer

    validity = Validity()
    validity["notBefore"] = Time(("utcTime", UTCTime(datetime(2009, 10, 8, 0, 25, 53))))
    validity["notAfter"] = Time(("utcTime", UTCTime(datetime(2010, 10, 8, 0, 25, 53))))
    tbs["validity"] = validity

    spki = SubjectPublicKeyInfo()
    spki_algo_id = sign_algo_id.copy()
    spki_algo_id["algorithm"] = ObjectIdentifier("1.2.840.113549.1.1.1")
    spki["algorithm"] = spki_algo_id
    spki["subjectPublicKey"] = BitString(hexdec("".join((
        "3048024100cdb7639c3278f006aa277f6eaf42902b592d8cbcbe38a1c92ba4695",
        "a331b1deadeadd8e9a5c27e8c4c2fd0a8889657722a4f2af7589cf2c77045dc8f",
        "deec357d0203010001",
    ))))
    tbs["subjectPublicKeyInfo"] = spki

    crt = Certificate()
    crt["tbsCertificate"] = tbs
    crt["signatureAlgorithm"] = sign_algo_id
    crt["signatureValue"] = BitString(hexdec("".join((
        "a67b06ec5ece92772ca413cba3ca12568fdc6c7b4511cd40a7f659980402df2b",
        "998bb9a4a8cbeb34c0f0a78cf8d91ede14a5ed76bf116fe360aafa8821490435",
    ))))
    crt.encode()

And we will get the same certificate used in Go's library tests.

DEFINED BY fields
-----------------

Here is only very simple example how you can define Any/OctetString
fields automatic decoding::

    class AttributeTypeAndValue(Sequence):
        schema = (
            ((("type",), AttributeType(defines=("value", {
                id_at_countryName: PrintableString(),
                id_at_stateOrProvinceName: PrintableString(),
                id_at_localityName: PrintableString(),
                id_at_organizationName: PrintableString(),
                id_at_commonName: PrintableString(),
            }))),),
            ("value", AttributeValue()),
        )

And when you will try to decode X.509 certificate with it, your pretty
printer will show::

       34   [0,0, 149]  . . issuer: Name CHOICE rdnSequence
       34   [1,2, 146]  . . . rdnSequence: RDNSequence SEQUENCE OF
       37   [1,1,  11]  . . . . 0: RelativeDistinguishedName SET OF
       39   [1,1,   9]  . . . . . 0: AttributeTypeAndValue SEQUENCE
       41   [1,1,   3]  . . . . . . type: AttributeType OBJECT IDENTIFIER id-at-countryName (2.5.4.6)
       46   [0,0,   4]  . . . . . . value: [UNIV 19] AttributeValue ANY
                        . . . . . . . 13:02:58:58
       46   [1,1,   2]  . . . . . . . DEFINED BY (2.5.4.6): PrintableString PrintableString XX
       50   [1,1,  19]  . . . . 1: RelativeDistinguishedName SET OF
       52   [1,1,  17]  . . . . . 0: AttributeTypeAndValue SEQUENCE
       54   [1,1,   3]  . . . . . . type: AttributeType OBJECT IDENTIFIER id-at-stateOrProvinceName (2.5.4.8)
       59   [0,0,  12]  . . . . . . value: [UNIV 19] AttributeValue ANY
                        . . . . . . . 13:0A:53:6F:6D:65:2D:53:74:61:74:65
       59   [1,1,  10]  . . . . . . . DEFINED BY (2.5.4.8): PrintableString PrintableString Some-State
       71   [1,1,  13]  . . . . 2: RelativeDistinguishedName SET OF
       73   [1,1,  11]  . . . . . 0: AttributeTypeAndValue SEQUENCE
       75   [1,1,   3]  . . . . . . type: AttributeType OBJECT IDENTIFIER id-at-localityName (2.5.4.7)
       80   [0,0,   6]  . . . . . . value: [UNIV 19] AttributeValue ANY
                        . . . . . . . 13:04:43:69:74:79
       80   [1,1,   4]  . . . . . . . DEFINED BY (2.5.4.7): PrintableString PrintableString City
       86   [1,1,  33]  . . . . 3: RelativeDistinguishedName SET OF
       88   [1,1,  31]  . . . . . 0: AttributeTypeAndValue SEQUENCE
       90   [1,1,   3]  . . . . . . type: AttributeType OBJECT IDENTIFIER id-at-organizationName (2.5.4.10)
       95   [0,0,  26]  . . . . . . value: [UNIV 19] AttributeValue ANY
                        . . . . . . . 13:18:49:6E:74:65:72:6E:65:74:20:57:69:64:67:69
                        . . . . . . . 74:73:20:50:74:79:20:4C:74:64
       95   [1,1,  24]  . . . . . . . DEFINED BY (2.5.4.10): PrintableString PrintableString Internet Widgits Pty Ltd

:ref:`Read more <definedby>` about that feature.
