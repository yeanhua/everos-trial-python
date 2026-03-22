# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["StorageCreatePresignedURLResponse"]


class StorageCreatePresignedURLResponse(BaseModel):
    expires_in: int

    object_key: str

    presigned_url: str
