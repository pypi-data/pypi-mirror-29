from datetime import datetime
from typing import Any as TAny
from typing import Dict
from typing import NamedTuple
from typing import Optional
from typing import Sequence as TSequence
from typing import Tuple
from typing import Type
from typing import Union


TagClassUniversal = ...  # type: int
TagClassApplication = ...  # type: int
TagClassContext = ...  # type: int
TagClassPrivate = ...  # type: int
TagFormPrimitive = ...  # type: int
TagFormConstructed = ...  # type: int
TagClassReprs = ...  # type: Dict[int, str]


class DecodeError(Exception):
    msg = ...  # type: str
    klass = ...  # type: Type
    decode_path = ...  # type: Tuple[str, ...]
    offset = ...  # type: int

    def __init__(
            self,
            msg: str=...,
            klass: Optional[TAny]=...,
            decode_path: TAny=...,
            offset: int=...,
    ) -> None: ...

class NotEnoughData(DecodeError): ...

class TagMismatch(DecodeError): ...

class InvalidLength(DecodeError): ...

class InvalidOID(DecodeError): ...

class ObjUnknown(ValueError):
    name = ...  # type: str

    def __init__(self, name: str) -> None: ...

class ObjNotReady(ValueError):
    name = ...  # type: str

    def __init__(self, str) -> None: ...

class InvalidValueType(ValueError):
    expected_types = ...  # type: Tuple[Type, ...]

    def __init__(self, expected_types: Tuple[Type, ...]) -> None: ...

class BoundsError(ValueError):
    bound_min = ...  # type: int
    value = ...  # type: int
    bound_max = ...  # type: int

    def __init__(self, bound_min: int, value: int, bound_max: int) -> None: ...

def hexdec(data: str) -> bytes: ...

def hexenc(data: bytes) -> str: ...

def int_bytes_len(num: int, byte_len: int=...) -> int: ...

def zero_ended_encode(num: int) -> bytes: ...

def tag_encode(num: int, klass: int=..., form: int=...) -> bytes: ...

def tag_decode(tag: bytes) -> Tuple[int, int, int]: ...

def tag_ctxp(num: int) -> bytes: ...

def tag_ctxc(num: int) -> bytes: ...

def tag_strip(data: memoryview) -> Tuple[memoryview, int, memoryview]: ...

def len_encode(l: int) -> bytes: ...

def len_decode(data: memoryview) -> Tuple[int, int, memoryview]: ...

class Obj:
    tag = ...  # type: bytes
    optional = ...  # type: bool

    def __init__(
            self,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[TAny]=...,
            optional: bool=...,
    ) -> None: ...

    @property
    def ready(self) -> bool: ...

    @property
    def decoded(self) -> bool: ...

    def copy(self) -> "Obj": ...

    @property
    def tlen(self) -> int: ...

    @property
    def tlvlen(self) -> int: ...

    def encode(self) -> bytes: ...

    def decode(
            self,
            data: bytes,
            offset: int=...,
            leavemm: bool=...,
            decode_path: Tuple[str, ...]=...,
            ctx: Optional[Dict[str, TAny]]=...,
    ) -> Tuple[Obj, bytes]: ...

    @property
    def expled(self) -> bool: ...

    @property
    def expl_tag(self) -> bytes: ...

    @property
    def expl_tlen(self) -> int: ...

    @property
    def expl_llen(self) -> int: ...

    @property
    def expl_offset(self) -> int: ...

    @property
    def expl_vlen(self) -> int: ...

    @property
    def expl_tlvlen(self) -> int: ...


PP = NamedTuple("PP", (
    ("asn1_type_name", str),
    ("obj_name", str),
    ("decode_path", Tuple[str, ...]),
    ("value", Optional[str]),
    ("blob", Optional[Union[bytes, Tuple[str, ...]]]),
    ("optional", bool),
    ("default", bool),
    ("impl", Optional[Tuple[int, int, int]]),
    ("expl", Optional[Tuple[int, int, int]]),
    ("offset", int),
    ("tlen", int),
    ("llen", int),
    ("vlen", int),
    ("expl_offset", int),
    ("expl_tlen", int),
    ("expl_llen", int),
    ("expl_vlen", int),
))


def pp_console_row(
        pp: PP,
        oids: Optional[Dict[str, str]]=...,
        with_offsets: bool=...,
        with_blob: bool=...,
): ...

def pp_console_blob(pp: PP) -> TSequence[str]: ...

def pprint(
        obj: Obj,
        oids: Optional[Dict[str, str]]=...,
        big_blobs: bool=...,
): ...


class Boolean(Obj):
    tag_default = ...  # type: bytes
    asn1_type_name = ...  # type: str
    default = ...  # type: "Boolean"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["Boolean", bool]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["Boolean", bool]]=...,
            optional: bool=...,
    ) -> None: ...

    @property
    def ready(self) -> bool: ...

    def copy(self) -> "Boolean": ...

    def __call__(
            self,
            value: Optional[Union["Boolean", bool]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["Boolean", bool]]=...,
            optional: Optional[bool]=...,
    ) -> "Boolean": ...

    def pps(self, decode_path: Tuple[str, ...]=...) -> TSequence[PP]: ...


class Integer(Obj):
    tag_default = ...  # type: bytes
    asn1_type_name = ...  # type: str
    specs = ...  # type: Dict[str, int]
    default = ...  # type: "Integer"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["Integer", int, str]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["Integer", int, str]]=...,
            optional: bool=...,
    ) -> None: ...

    @property
    def ready(self) -> bool: ...

    def copy(self) -> "Integer": ...

    @property
    def named(self) -> Optional[str]: ...

    def __call__(
            self,
            value: Optional[Union["Integer", int, str]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["Integer", int, str]]=...,
            optional: Optional[bool]=...,
    ) -> "Integer": ...

    def __int__(self) -> int: ...

    def pps(self, decode_path: Tuple[str, ...]=...) -> TSequence[PP]: ...


class BitString(Obj):
    tag_default = ...  # type: bytes
    asn1_type_name = ...  # type: str
    specs = ...  # type: Dict[str, int]
    default = ...  # type: "BitString"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["BitString", bytes, Tuple[str, ...]]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["BitString", bytes, Tuple[str, ...]]]=...,
            optional: bool=...,
    ) -> None: ...

    @property
    def ready(self) -> bool: ...

    def copy(self) -> "BitString": ...

    @property
    def bit_len(self) -> int: ...

    @property
    def named(self) -> TSequence[str]: ...

    def __call__(
            self,
            value: Optional[Union["BitString", bytes, Tuple[str, ...]]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["BitString", bytes, Tuple[str, ...]]]=...,
            optional: Optional[bool]=...,
    ) -> "BitString": ...

    def __bytes__(self) -> bytes: ...

    def pps(self, decode_path: Tuple[str, ...]=...) -> TSequence[PP]: ...


class OctetString(Obj):
    tag_default = ...  # type: bytes
    asn1_type_name = ...  # type: str
    default = ...  # type: "OctetString"
    optional = ...  # type: bool
    defined = ...  # type: Tuple[ObjectIdentifier, Obj]

    def __init__(
            self,
            value: Optional[Union["OctetString", bytes]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["OctetString", bytes]]=...,
            optional: bool=...,
    ) -> None: ...

    @property
    def ready(self) -> bool: ...

    def copy(self) -> "OctetString": ...

    def __call__(
            self,
            value: Optional[Union["OctetString", bytes]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["OctetString", bytes]]=...,
            optional: Optional[bool]=...,
    ) -> "OctetString": ...

    def __bytes__(self) -> bytes: ...

    def pps(self, decode_path: Tuple[str, ...]=...) -> TSequence[PP]: ...


class Null(Obj):
    tag_default = ...  # type: bytes
    asn1_type_name = ...  # type: str
    default = ...  # type: "Null"
    optional = ...  # type: bool

    def __init__(
            self,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            optional: bool=...,
    ) -> None: ...

    @property
    def ready(self) -> bool: ...

    def copy(self) -> "Null": ...

    def __call__(
            self,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            optional: Optional[bool]=...,
    ) -> "Null": ...

    def pps(self, decode_path: Tuple[str, ...]=...) -> TSequence[PP]: ...


class ObjectIdentifier(Obj):
    tag_default = ...  # type: bytes
    asn1_type_name = ...  # type: str
    default = ...  # type: "ObjectIdentifier"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["ObjectIdentifier", str, Tuple[int, ...]]]=...,
            defines: Optional[Sequence[Tuple[str, Dict["ObjectIdentifier", Obj]]]],
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["ObjectIdentifier", str, Tuple[int, ...]]]=...,
            optional: bool=...,
    ) -> None: ...

    @property
    def ready(self) -> bool: ...

    def copy(self) -> "ObjectIdentifier": ...

    def __call__(
            self,
            value: Optional[Union["ObjectIdentifier", str, Tuple[int, ...]]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["ObjectIdentifier", str, Tuple[int, ...]]]=...,
            optional: Optional[bool]=...,
    ) -> "ObjectIdentifier": ...

    def __add__(
            self,
            their: Union["ObjectIdentifier", Tuple[int, ...]],
    ) -> "ObjectIdentifier": ...

    def pps(self, decode_path: Tuple[str, ...]=...) -> TSequence[PP]: ...


class Enumerated(Integer):
    tag_default = ...  # type: bytes
    asn1_type_name = ...  # type: str
    default = ...  # type: "Enumerated"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["Enumerated", str, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["Enumerated", str, int]]=...,
            optional: bool=...,
    ) -> None: ...

    def copy(self) -> "Enumerated": ...

    def __call__(  # type: ignore
            self,
            value: Optional[Union["Enumerated", str, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["Enumerated", str, int]]=...,
            optional: Optional[bool]=...,
    ) -> "Enumerated": ...


class CommonString(OctetString):
    def pps(
            self,
            decode_path: Tuple[str, ...]=...,
            no_unicode: bool=...,
    ) -> TSequence[PP]: ...


class UTF8String(CommonString):
    tag_default = ...  # type: bytes
    encoding = ...  # type: str
    asn1_type_name = ...  # type: str
    default = ...  # type: "UTF8String"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["UTF8String", str, bytes]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["UTF8String", str, bytes]]=...,
            optional: bool=...,
    ) -> None: ...

    def __str__(self) -> str: ...


class NumericString(CommonString):
    tag_default = ...  # type: bytes
    encoding = ...  # type: str
    asn1_type_name = ...  # type: str
    default = ...  # type: "NumericString"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["NumericString", str, bytes]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["NumericString", str, bytes]]=...,
            optional: bool=...,
    ) -> None: ...


class PrintableString(CommonString):
    tag_default = ...  # type: bytes
    encoding = ...  # type: str
    asn1_type_name = ...  # type: str
    default = ...  # type: "PrintableString"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["PrintableString", str, bytes]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["PrintableString", str, bytes]]=...,
            optional: bool=...,
    ) -> None: ...


class TeletexString(CommonString):
    tag_default = ...  # type: bytes
    encoding = ...  # type: str
    asn1_type_name = ...  # type: str
    default = ...  # type: "TeletexString"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["TeletexString", str, bytes]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["TeletexString", str, bytes]]=...,
            optional: bool=...,
    ) -> None: ...


class T61String(TeletexString):
    asn1_type_name = ...  # type: str
    default = ...  # type: "T61String"
    optional = ...  # type: bool


class VideotexString(CommonString):
    tag_default = ...  # type: bytes
    encoding = ...  # type: str
    asn1_type_name = ...  # type: str
    default = ...  # type: "VideotexString"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["VideotexString", str, bytes]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["VideotexString", str, bytes]]=...,
            optional: bool=...,
    ) -> None: ...


class IA5String(CommonString):
    tag_default = ...  # type: bytes
    encoding = ...  # type: str
    asn1_type_name = ...  # type: str
    default = ...  # type: "IA5String"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["IA5String", str, bytes]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["IA5String", str, bytes]]=...,
            optional: bool=...,
    ) -> None: ...


class UTCTime(CommonString):
    tag_default = ...  # type: bytes
    encoding = ...  # type: str
    asn1_type_name = ...  # type: str
    default = ...  # type: "UTCTime"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["UTCTime", datetime]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["UTCTime", datetime]]=...,
            optional: bool=...,
    ) -> None: ...

    def todatetime(self) -> datetime: ...

    def pps(self, decode_path: Tuple[str, ...]=...) -> TSequence[PP]: ...  # type: ignore


class GeneralizedTime(UTCTime):
    tag_default = ...  # type: bytes
    asn1_type_name = ...  # type: str
    default = ...  # type: "GeneralizedTime"
    optional = ...  # type: bool

    def todatetime(self) -> datetime: ...


class GraphicString(CommonString):
    tag_default = ...  # type: bytes
    encoding = ...  # type: str
    asn1_type_name = ...  # type: str
    default = ...  # type: "GraphicString"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["GraphicString", str, bytes]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["GraphicString", str, bytes]]=...,
            optional: bool=...,
    ) -> None: ...


class VisibleString(CommonString):
    tag_default = ...  # type: bytes
    encoding = ...  # type: str
    asn1_type_name = ...  # type: str
    default = ...  # type: "VisibleString"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["VisibleString", str, bytes]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["VisibleString", str, bytes]]=...,
            optional: bool=...,
    ) -> None: ...


class ISO646String(VisibleString):
    asn1_type_name = ...  # type: str
    default = ...  # type: "ISO646String"
    optional = ...  # type: bool


class GeneralString(CommonString):
    tag_default = ...  # type: bytes
    encoding = ...  # type: str
    asn1_type_name = ...  # type: str
    default = ...  # type: "GeneralString"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["GeneralString", str, bytes]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["GeneralString", str, bytes]]=...,
            optional: bool=...,
    ) -> None: ...


class UniversalString(CommonString):
    tag_default = ...  # type: bytes
    encoding = ...  # type: str
    asn1_type_name = ...  # type: str
    default = ...  # type: "UniversalString"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["UniversalString", str, bytes]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["UniversalString", str, bytes]]=...,
            optional: bool=...,
    ) -> None: ...


class BMPString(CommonString):
    tag_default = ...  # type: bytes
    encoding = ...  # type: str
    asn1_type_name = ...  # type: str
    default = ...  # type: "BMPString"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["BMPString", str, bytes]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["BMPString", str, bytes]]=...,
            optional: bool=...,
    ) -> None: ...


class Choice(Obj):
    tag_default = ...  # type: bytes
    asn1_type_name = ...  # type: str
    specs = ...  # type: Dict[str, Obj]
    default = ...  # type: "Choice"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["Choice", Tuple[str, Obj]]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["Choice", Tuple[str, Obj]]]=...,
            optional: bool=...,
    ) -> None: ...

    @property
    def ready(self) -> bool: ...

    def copy(self) -> "Choice": ...

    def __call__(
            self,
            value: Optional[Union["Choice", Tuple[str, Obj]]]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["Choice", Tuple[str, Obj]]]=...,
            optional: Optional[bool]=...,
    ) -> "Choice": ...

    def __getitem__(self, key: str) -> Optional[Obj]: ...

    def __setitem__(self, key: str, value: Obj) -> None: ...

    @property
    def choice(self) -> str: ...

    @property
    def value(self) -> Obj: ...

    @property
    def tlen(self) -> int: ...

    @property
    def decoded(self) -> bool: ...

    def pps(self, decode_path: Tuple[str, ...]=...) -> TSequence[PP]: ...


class PrimitiveTypes(Choice):
    schema = ...  # type: Dict[str, Obj]


class Any(Obj):
    tag_default = ...  # type: bytes
    asn1_type_name = ...  # type: str
    default = ...  # type: "Any"
    optional = ...  # type: bool
    defined = ...  # type: Tuple[ObjectIdentifier, Obj]

    def __init__(
            self,
            value: Optional[Union[Obj, bytes]]=...,
            expl: Optional[bytes]=...,
            optional: bool=...,
    ) -> None: ...

    @property
    def ready(self) -> bool: ...

    def copy(self) -> "Any": ...

    def __call__(
            self,
            value: Optional[Union[Obj, bytes]]=...,
            expl: Optional[bytes]=...,
            optional: Optional[bool]=...,
    ) -> "Any": ...

    def __bytes__(self) -> bytes: ...

    @property
    def tlen(self) -> int: ...

    def pps(self, decode_path: Tuple[str, ...]=...) -> TSequence[PP]: ...


class Sequence(Obj):
    tag_default = ...  # type: bytes
    asn1_type_name = ...  # type: str
    specs = ...  # type: Dict[str, Obj]
    default = ...  # type: "Sequence"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional["Sequence"]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional["Sequence"]=...,
            optional: bool=...,
    ) -> None: ...

    @property
    def ready(self) -> bool: ...

    def copy(self) -> "Sequence": ...

    def __call__(
            self,
            value: Optional["Sequence"]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional["Sequence"]=...,
            optional: Optional[bool]=...,
    ) -> "Sequence": ...

    def __getitem__(self, key: str) -> Optional[Obj]: ...

    def __setitem__(self, key: str, value: Obj) -> None: ...

    def pps(self, decode_path: Tuple[str, ...]=...) -> TSequence[PP]: ...


class Set(Sequence):
    tag_default = ...  # type: bytes
    asn1_type_name = ...  # type: str
    default = ...  # type: "Set"
    optional = ...  # type: bool


class SequenceOf(Obj):
    tag_default = ...  # type: bytes
    asn1_type_name = ...  # type: str
    spec = ...  # type: Obj
    default = ...  # type: "SequenceOf"
    optional = ...  # type: bool

    def __init__(
            self,
            value: Optional[Union["SequenceOf", TSequence[Obj]]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["SequenceOf", TSequence[Obj]]]=...,
            optional: Optional[bool]=...,
    ) -> None: ...

    @property
    def ready(self) -> bool: ...

    def copy(self) -> "SequenceOf": ...

    def __call__(
            self,
            value: Optional[Union["SequenceOf", TSequence[Obj]]]=...,
            bounds: Optional[Tuple[int, int]]=...,
            impl: Optional[bytes]=...,
            expl: Optional[bytes]=...,
            default: Optional[Union["SequenceOf", TSequence[Obj]]]=...,
            optional: Optional[bool]=...,
    ) -> "SequenceOf": ...

    def __getitem__(self, key: int) -> Obj: ...

    def __iter__(self) -> TSequence[Obj]: ...

    def append(self, value: Obj) -> None: ...

    def pps(self, decode_path: Tuple[str, ...]=...) -> TSequence[PP]: ...


class SetOf(SequenceOf):
    tag_default = ...  # type: bytes
    asn1_type_name = ...  # type: str
    default = ...  # type: "SetOf"
    optional = ...  # type: bool


def obj_by_path(pypath: str) -> TAny: ...
