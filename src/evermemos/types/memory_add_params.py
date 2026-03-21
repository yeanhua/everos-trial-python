# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["MemoryAddParams"]


class MemoryAddParams(TypedDict, total=False):
    content: Required[str]
    """Memory text content"""

    user_id: Required[str]
    """Owner user ID"""

    object_keys: SequenceNotStr[str]
    """S3 object keys from presigned upload (required when type != text)"""

    type: Literal["text", "image", "video", "document"]
    """Memory type — drives multimodal routing in SDK"""
