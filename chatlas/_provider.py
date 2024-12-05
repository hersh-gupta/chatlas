from __future__ import annotations

from abc import ABC, abstractmethod
from typing import (
    Any,
    AsyncIterable,
    Generic,
    Iterable,
    Literal,
    Optional,
    TypeVar,
    overload,
)

from pydantic import BaseModel

from ._tools import Tool
from ._turn import Turn

ChatCompletionT = TypeVar("ChatCompletionT")
ChatCompletionChunkT = TypeVar("ChatCompletionChunkT")
# A dictionary representation of a chat completion
ChatCompletionDictT = TypeVar("ChatCompletionDictT")


class Provider(
    ABC, Generic[ChatCompletionT, ChatCompletionChunkT, ChatCompletionDictT]
):
    """
    A model provider interface for a [](`~chatlas.Chat`).

    This abstract class defines the interface a model provider must implement in
    order to be used with a [](`~chatlas.Chat`) instance. The provider is
    responsible for performing the actual chat completion, and for handling the
    streaming of the completion results.

    Note that this class is exposed for developers who wish to implement their
    own provider. In general, you should not need to interact with this class
    directly.
    """

    @overload
    @abstractmethod
    def chat_perform(
        self,
        *,
        stream: Literal[False],
        turns: list[Turn],
        tools: dict[str, Tool],
        data_model: Optional[type[BaseModel]],
        kwargs: Any,
    ) -> ChatCompletionT: ...

    @overload
    @abstractmethod
    def chat_perform(
        self,
        *,
        stream: Literal[True],
        turns: list[Turn],
        tools: dict[str, Tool],
        data_model: Optional[type[BaseModel]],
        kwargs: Any,
    ) -> Iterable[ChatCompletionChunkT]: ...

    @abstractmethod
    def chat_perform(
        self,
        *,
        stream: bool,
        turns: list[Turn],
        tools: dict[str, Tool],
        data_model: Optional[type[BaseModel]],
        kwargs: Any,
    ) -> Iterable[ChatCompletionChunkT] | ChatCompletionT: ...

    @overload
    @abstractmethod
    async def chat_perform_async(
        self,
        *,
        stream: Literal[False],
        turns: list[Turn],
        tools: dict[str, Tool],
        data_model: Optional[type[BaseModel]],
        kwargs: Any,
    ) -> ChatCompletionT: ...

    @overload
    @abstractmethod
    async def chat_perform_async(
        self,
        *,
        stream: Literal[True],
        turns: list[Turn],
        tools: dict[str, Tool],
        data_model: Optional[type[BaseModel]],
        kwargs: Any,
    ) -> AsyncIterable[ChatCompletionChunkT]: ...

    @abstractmethod
    async def chat_perform_async(
        self,
        *,
        stream: bool,
        turns: list[Turn],
        tools: dict[str, Tool],
        data_model: Optional[type[BaseModel]],
        kwargs: Any,
    ) -> AsyncIterable[ChatCompletionChunkT] | ChatCompletionT: ...

    @abstractmethod
    def stream_text(self, chunk: ChatCompletionChunkT) -> Optional[str]: ...

    @abstractmethod
    def stream_merge_chunks(
        self,
        completion: Optional[ChatCompletionDictT],
        chunk: ChatCompletionChunkT,
    ) -> ChatCompletionDictT: ...

    @abstractmethod
    def stream_turn(
        self,
        completion: ChatCompletionDictT,
        has_data_model: bool,
        stream: Any,
    ) -> Turn: ...

    @abstractmethod
    async def stream_turn_async(
        self,
        completion: ChatCompletionDictT,
        has_data_model: bool,
        stream: Any,
    ) -> Turn: ...

    @abstractmethod
    def value_turn(
        self,
        completion: ChatCompletionT,
        has_data_model: bool,
    ) -> Turn: ...