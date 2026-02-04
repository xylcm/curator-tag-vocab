from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Translation(_message.Message):
    __slots__ = ()
    LANG_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    lang: str
    text: str
    def __init__(self, lang: _Optional[str] = ..., text: _Optional[str] = ...) -> None: ...

class Tag(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    SUB_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TRANSLATIONS_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    context: str
    category: str
    sub_category: str
    translations: _containers.RepeatedCompositeFieldContainer[Translation]
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., context: _Optional[str] = ..., category: _Optional[str] = ..., sub_category: _Optional[str] = ..., translations: _Optional[_Iterable[_Union[Translation, _Mapping]]] = ...) -> None: ...

class Category(_message.Message):
    __slots__ = ()
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    TRANSLATIONS_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    available: bool
    translations: _containers.RepeatedCompositeFieldContainer[Translation]
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., available: _Optional[bool] = ..., translations: _Optional[_Iterable[_Union[Translation, _Mapping]]] = ...) -> None: ...

class TagVocabulary(_message.Message):
    __slots__ = ()
    VERSION_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_TIME_FIELD_NUMBER: _ClassVar[int]
    VOCAB_SIZE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    version: str
    modified_time: str
    vocab_size: int
    tags: _containers.RepeatedCompositeFieldContainer[Tag]
    categories: _containers.RepeatedCompositeFieldContainer[Category]
    def __init__(self, version: _Optional[str] = ..., modified_time: _Optional[str] = ..., vocab_size: _Optional[int] = ..., tags: _Optional[_Iterable[_Union[Tag, _Mapping]]] = ..., categories: _Optional[_Iterable[_Union[Category, _Mapping]]] = ...) -> None: ...
