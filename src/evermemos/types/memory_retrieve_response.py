# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["MemoryRetrieveResponse"]


class MemoryRetrieveResponse(BaseModel):
    id: str

    content: str

    created_at: datetime

    type: str

    user_id: str

    metadata: Optional[Dict[str, str]] = None
    """Arbitrary key-value metadata (new in v3)"""

    object_keys: Optional[List[str]] = None

    tags: Optional[List[str]] = None
    """User-defined tags (added in v2)"""
