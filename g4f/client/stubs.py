from __future__ import annotations

from typing import Optional, List, Dict
from time import time

from .helper import filter_none

try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel():
        @classmethod
        def construct(cls, **data):
            new = cls()
            for key, value in data.items():
                setattr(new, key, value)
            return new
    class Field():
        def __init__(self, **config):
            pass

class ChatCompletionChunk(BaseModel):
    id: str
    object: str
    created: int
    model: str
    provider: Optional[str]
    choices: List[ChatCompletionDeltaChoice]

    @classmethod
    def construct(
        cls,
        content: str,
        finish_reason: str,
        completion_id: str = None,
        created: int = None
    ):
        return super().construct(
            id=f"chatcmpl-{completion_id}" if completion_id else None,
            object="chat.completion.cunk",
            created=created,
            model=None,
            provider=None,
            choices=[ChatCompletionDeltaChoice.construct(
                ChatCompletionDelta.construct(content),
                finish_reason
            )]
        )

class ChatCompletionMessage(BaseModel):
    role: str
    content: str

    @classmethod
    def construct(cls, content: str):
        return super().construct(role="assistant", content=content)

class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatCompletionMessage
    finish_reason: str

    @classmethod
    def construct(cls, message: ChatCompletionMessage, finish_reason: str):
        return super().construct(index=0, message=message, finish_reason=finish_reason)

class ChatCompletion(BaseModel):
    id: str
    object: str
    created: int
    model: str
    provider: Optional[str]
    choices: List[ChatCompletionChoice]
    usage: Dict[str, int] = Field(examples=[{
        "prompt_tokens": 0, #prompt_tokens,
        "completion_tokens": 0, #completion_tokens,
        "total_tokens": 0, #prompt_tokens + completion_tokens,
    }])

    @classmethod
    def construct(
        cls,
        content: str,
        finish_reason: str,
        completion_id: str = None,
        created: int = None
    ):
        return super().construct(
            id=f"chatcmpl-{completion_id}" if completion_id else None,
            object="chat.completion",
            created=created,
            model=None,
            provider=None,
            choices=[ChatCompletionChoice.construct(
                ChatCompletionMessage.construct(content),
                finish_reason
            )],
            usage={
                "prompt_tokens": 0, #prompt_tokens,
                "completion_tokens": 0, #completion_tokens,
                "total_tokens": 0, #prompt_tokens + completion_tokens,
            }
        )

class ChatCompletionDelta(BaseModel):
    role: str
    content: str

    @classmethod
    def construct(cls, content: Optional[str]):
        return super().construct(role="assistant", content=content)

class ChatCompletionDeltaChoice(BaseModel):
    index: int
    delta: ChatCompletionDelta
    finish_reason: Optional[str]

    @classmethod
    def construct(cls, delta: ChatCompletionDelta, finish_reason: Optional[str]):
        return super().construct(index=0, delta=delta, finish_reason=finish_reason)

class Image(BaseModel):
    url: Optional[str]
    b64_json: Optional[str]
    revised_prompt: Optional[str]

    @classmethod
    def construct(cls, url: str = None, b64_json: str = None, revised_prompt: str = None):
        return super().construct(**filter_none(
            url=url,
            b64_json=b64_json,
            revised_prompt=revised_prompt
        ))

class ImagesResponse(BaseModel):
    data: List[Image]
    model: str
    provider: str
    created: int

    @classmethod
    def construct(cls, data: List[Image], created: int = None, model: str = None, provider: str = None):
        if created is None:
            created = int(time())
        return super().construct(
            data=data,
            model=model,
            provider=provider,
            created=created
        )