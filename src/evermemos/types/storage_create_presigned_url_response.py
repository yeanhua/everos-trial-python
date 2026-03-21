# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["StorageCreatePresignedURLResponse"]


class StorageCreatePresignedURLResponse(BaseModel):
    expires_in: int
    """URL expiration in seconds"""

    object_key: str
    """Object key in storage bucket"""

    presigned_url: str
    """S3 presigned PUT URL"""
