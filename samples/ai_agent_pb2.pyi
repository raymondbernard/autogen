from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AI(_message.Message):
    __slots__ = ["date", "message", "system", "open", "score", "high", "low"]
    DATE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_STR: _ClassVar[str]
    SYSTEM_STR: _ClassVar[str]
    OPEN_FIELD_NUMBER: _ClassVar[str]
    SCORE_FIELD_NUMBER: _ClassVar[str]
    HIGH_FIELD_NUMBER: _ClassVar[str]
    LOW_FIELD_NUMBER: _ClassVar[str]
    date: str
    message: str
    system: str 
    open: str
    score: str
    high: str
    low: str
    def __init__(self, date: _Optional[str] = ..., message: _Optional[str] = ..., system: _Optional[str] = ..., open: _Optional[str] = ..., score: _Optional[str] = ..., high: _Optional[str] = ..., low: _Optional[str] = ...) -> None: ...
