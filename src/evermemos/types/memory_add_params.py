# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["MemoryAddParams"]


class MemoryAddParams(TypedDict, total=False):
    content: Required[str]

    user_id: Required[str]

    object_keys: SequenceNotStr[str]

    type: Literal["text", "image", "video", "document"]
