# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["V1AddMemoryResponse"]


class V1AddMemoryResponse(BaseModel):
    id: str

    content: str

    created_at: datetime

    type: str

    user_id: str

    object_keys: Optional[List[str]] = None
