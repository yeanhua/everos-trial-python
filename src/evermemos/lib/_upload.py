"""Presigned URL 获取与流式 S3 上传。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import httpx

from ._errors import UploadError
from ._files import ResolvedFile

if TYPE_CHECKING:
    from .._client import EverMemOS, AsyncEverMemOS


@dataclass
class UploadResult:
    """单个文件上传结果。"""
    object_key: str
    filename: str
    content_type: str
    size: int


_UPLOAD_TIMEOUT = 120.0
_MAX_RETRIES = 3
_CHUNK_SIZE = 64 * 1024  # 64KB


def presign_and_upload(
    client: "EverMemOS",
    resolved: ResolvedFile,
) -> UploadResult:
    """同步：presign → 流式 PUT 上传到 S3。"""

    presign_resp = client.storage.create_presigned_url(
        filename=resolved.filename,
        content_type=resolved.content_type,
        file_size=resolved.size,
    )

    _stream_upload_to_s3(
        presigned_url=presign_resp.presigned_url,
        resolved=resolved,
    )

    return UploadResult(
        object_key=presign_resp.object_key,
        filename=resolved.filename,
        content_type=resolved.content_type,
        size=resolved.size,
    )


async def async_presign_and_upload(
    client: "AsyncEverMemOS",
    resolved: ResolvedFile,
) -> UploadResult:
    """异步：presign → 流式 PUT 上传到 S3。"""

    presign_resp = await client.storage.create_presigned_url(
        filename=resolved.filename,
        content_type=resolved.content_type,
        file_size=resolved.size,
    )

    await _async_stream_upload_to_s3(
        presigned_url=presign_resp.presigned_url,
        resolved=resolved,
    )

    return UploadResult(
        object_key=presign_resp.object_key,
        filename=resolved.filename,
        content_type=resolved.content_type,
        size=resolved.size,
    )


# ─── 流式 S3 上传 ───


def _file_chunk_iter(resolved: ResolvedFile):
    """生成器：流式读取文件分块。"""
    with resolved.open() as f:
        while True:
            chunk = f.read(_CHUNK_SIZE)
            if not chunk:
                break
            yield chunk


def _stream_upload_to_s3(presigned_url: str, resolved: ResolvedFile) -> None:
    """同步流式 PUT —— 文件不整体读入内存。"""
    last_error = None
    for attempt in range(_MAX_RETRIES):
        try:
            with httpx.Client(timeout=_UPLOAD_TIMEOUT) as http:
                resp = http.put(
                    presigned_url,
                    content=_file_chunk_iter(resolved),
                    headers={
                        "Content-Type": resolved.content_type,
                        "Content-Length": str(resolved.size),
                    },
                )
                resp.raise_for_status()
                return
        except (httpx.TimeoutException, httpx.HTTPStatusError) as e:
            last_error = e
            if isinstance(e, httpx.HTTPStatusError) and e.response.status_code < 500:
                raise UploadError(
                    f"S3 upload failed (HTTP {e.response.status_code}): {e.response.text}"
                ) from e

    raise UploadError(f"S3 upload failed after {_MAX_RETRIES} attempts") from last_error


async def _async_stream_upload_to_s3(presigned_url: str, resolved: ResolvedFile) -> None:
    """异步流式 PUT。"""
    import anyio

    async def _async_chunks():
        f = await anyio.to_thread.run_sync(resolved.open)
        try:
            while True:
                chunk = await anyio.to_thread.run_sync(lambda: f.read(_CHUNK_SIZE))
                if not chunk:
                    break
                yield chunk
        finally:
            await anyio.to_thread.run_sync(f.close)

    last_error = None
    for attempt in range(_MAX_RETRIES):
        try:
            async with httpx.AsyncClient(timeout=_UPLOAD_TIMEOUT) as http:
                resp = await http.put(
                    presigned_url,
                    content=_async_chunks(),
                    headers={
                        "Content-Type": resolved.content_type,
                        "Content-Length": str(resolved.size),
                    },
                )
                resp.raise_for_status()
                return
        except (httpx.TimeoutException, httpx.HTTPStatusError) as e:
            last_error = e
            if isinstance(e, httpx.HTTPStatusError) and e.response.status_code < 500:
                raise UploadError(
                    f"S3 upload failed (HTTP {e.response.status_code}): {e.response.text}"
                ) from e

    raise UploadError(f"S3 upload failed after {_MAX_RETRIES} attempts") from last_error
