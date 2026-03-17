# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["StorageGeneratePresignedURLParams"]


class StorageGeneratePresignedURLParams(TypedDict, total=False):
    content_type: Required[str]

    filename: Required[str]

    file_size: int
    """File size in bytes (optional, for server validation)"""
