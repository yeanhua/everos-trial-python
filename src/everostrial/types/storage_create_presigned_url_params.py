# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["StorageCreatePresignedURLParams"]


class StorageCreatePresignedURLParams(TypedDict, total=False):
    content_type: Required[str]

    filename: Required[str]

    file_size: int
