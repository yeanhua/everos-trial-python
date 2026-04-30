"""文件输入抽象与流式解析。"""

from __future__ import annotations

import os
import tempfile
import mimetypes
from typing import Union, BinaryIO
from pathlib import Path
from dataclasses import dataclass
from urllib.parse import unquote, urlparse

import httpx

from ._errors import FileResolveError

_DEFAULT_MAX_DOWNLOAD_SIZE = 100 * 1024 * 1024  # 100MB
_DEFAULT_DOWNLOAD_TIMEOUT = 60.0  # seconds
_STREAM_CHUNK_SIZE = 64 * 1024   # 64KB


@dataclass
class FileInput:
    """统一的文件输入抽象。三种来源互斥。

    Examples:
        FileInput(path="./photo.jpg")
        FileInput(url="https://example.com/image.png")
        FileInput(data=b"raw bytes", filename="data.bin", content_type="application/octet-stream")
    """

    path: Union[str, Path, None] = None
    url: Union[str, None] = None
    data: Union[bytes, BinaryIO, None] = None
    content_type: Union[str, None] = None
    filename: Union[str, None] = None

    def __post_init__(self) -> None:
        sources = sum(x is not None for x in [self.path, self.url, self.data])
        if sources == 0:
            raise ValueError("FileInput requires at least one of: path, url, data")
        if sources > 1:
            raise ValueError("FileInput accepts only one of: path, url, data")


@dataclass
class ResolvedFile:
    """文件解析结果 — 持有文件路径，不持有 bytes。

    Attributes:
        file_path: 本地文件的绝对路径（原始文件或临时下载文件）
        content_type: MIME 类型
        filename: 原始文件名
        size: 文件大小（bytes）
        is_temp: 是否为临时文件（URL 下载产生，需要调用方清理）
    """

    file_path: Path
    content_type: str
    filename: str
    size: int
    is_temp: bool = False

    def cleanup(self) -> None:
        """清理临时文件。"""
        if self.is_temp and self.file_path.exists():
            self.file_path.unlink()

    def open(self) -> BinaryIO:
        """打开文件用于流式读取。"""
        return open(self.file_path, "rb")


def resolve_file(
    file_input: FileInput,
    *,
    max_download_size: int = _DEFAULT_MAX_DOWNLOAD_SIZE,
    download_timeout: float = _DEFAULT_DOWNLOAD_TIMEOUT,
) -> ResolvedFile:
    """将 FileInput 解析为 ResolvedFile（同步）。"""

    if file_input.path is not None:
        return _resolve_from_path(file_input)
    elif file_input.url is not None:
        return _resolve_from_url(file_input, max_download_size, download_timeout)
    elif file_input.data is not None:
        return _resolve_from_data(file_input)
    else:
        raise FileResolveError("No file source provided")


async def async_resolve_file(
    file_input: FileInput,
    *,
    max_download_size: int = _DEFAULT_MAX_DOWNLOAD_SIZE,
    download_timeout: float = _DEFAULT_DOWNLOAD_TIMEOUT,
) -> ResolvedFile:
    """将 FileInput 解析为 ResolvedFile（异步）。"""

    if file_input.path is not None:
        import anyio
        return await anyio.to_thread.run_sync(lambda: _resolve_from_path(file_input))  # type: ignore[reportUnknownMemberType]
    elif file_input.url is not None:
        return await _async_resolve_from_url(file_input, max_download_size, download_timeout)
    elif file_input.data is not None:
        return _resolve_from_data(file_input)
    else:
        raise FileResolveError("No file source provided")


# ─── 内部实现 ───


def _resolve_from_path(fi: FileInput) -> ResolvedFile:
    """本地文件：验证存在性，不读取内容。"""
    p = Path(fi.path).resolve()  # type: ignore[arg-type]
    if not p.exists():
        raise FileResolveError(f"File not found: {p}")
    if not p.is_file():
        raise FileResolveError(f"Not a file: {p}")

    size = p.stat().st_size
    ct = fi.content_type or mimetypes.guess_type(str(p))[0] or "application/octet-stream"
    fn = fi.filename or p.name
    return ResolvedFile(file_path=p, content_type=ct, filename=fn, size=size, is_temp=False)


def _resolve_from_url(
    fi: FileInput, max_size: int, timeout: float
) -> ResolvedFile:
    """URL 文件：流式下载到临时文件，边下边计数，超限立即中断。"""
    tmp_fd, tmp_path = tempfile.mkstemp(prefix="everostrial_")
    tmp_file = Path(tmp_path)
    downloaded = 0

    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            with client.stream("GET", fi.url) as resp:  # type: ignore[arg-type]
                resp.raise_for_status()

                ct_header = resp.headers.get("content-type", "application/octet-stream")
                ct_header = ct_header.split(";")[0].strip()

                with os.fdopen(tmp_fd, "wb") as f:
                    for chunk in resp.iter_bytes(chunk_size=_STREAM_CHUNK_SIZE):
                        downloaded += len(chunk)
                        if downloaded > max_size:
                            raise FileResolveError(
                                f"URL download exceeds {max_size} bytes limit "
                                f"(downloaded {downloaded} bytes so far). "
                                f"Use the low-level storage API for large files."
                            )
                        f.write(chunk)
                    tmp_fd = -1  # fd 已通过 os.fdopen 关闭

    except FileResolveError:
        tmp_file.unlink(missing_ok=True)
        raise
    except Exception as e:
        tmp_file.unlink(missing_ok=True)
        if tmp_fd >= 0:
            os.close(tmp_fd)
        raise FileResolveError(f"Failed to download from {fi.url}: {e}") from e

    ct = fi.content_type or ct_header
    fn = fi.filename or _filename_from_url(fi.url)  # type: ignore[arg-type]
    return ResolvedFile(
        file_path=tmp_file, content_type=ct, filename=fn,
        size=downloaded, is_temp=True,
    )


async def _async_resolve_from_url(
    fi: FileInput, max_size: int, timeout: float,
) -> ResolvedFile:
    """异步版流式 URL 下载。"""
    tmp_fd, tmp_path = tempfile.mkstemp(prefix="everostrial_")
    tmp_file = Path(tmp_path)
    downloaded = 0

    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            async with client.stream("GET", fi.url) as resp:  # type: ignore[arg-type]
                resp.raise_for_status()

                ct_header = resp.headers.get("content-type", "application/octet-stream")
                ct_header = ct_header.split(";")[0].strip()

                with os.fdopen(tmp_fd, "wb") as f:
                    async for chunk in resp.aiter_bytes(chunk_size=_STREAM_CHUNK_SIZE):
                        downloaded += len(chunk)
                        if downloaded > max_size:
                            raise FileResolveError(
                                f"URL download exceeds {max_size} bytes limit"
                            )
                        f.write(chunk)
                    tmp_fd = -1

    except FileResolveError:
        tmp_file.unlink(missing_ok=True)
        raise
    except Exception as e:
        tmp_file.unlink(missing_ok=True)
        if tmp_fd >= 0:
            os.close(tmp_fd)
        raise FileResolveError(f"Failed to download from {fi.url}: {e}") from e

    ct = fi.content_type or ct_header
    fn = fi.filename or _filename_from_url(fi.url)  # type: ignore[arg-type]
    return ResolvedFile(
        file_path=tmp_file, content_type=ct, filename=fn,
        size=downloaded, is_temp=True,
    )


def _resolve_from_data(fi: FileInput) -> ResolvedFile:
    """bytes/BinaryIO：分块写入临时文件，BinaryIO 不全量读入内存。"""
    tmp_fd, tmp_path = tempfile.mkstemp(prefix="everostrial_")
    total_size = 0

    with os.fdopen(tmp_fd, "wb") as f:
        if isinstance(fi.data, bytes):
            f.write(fi.data)
            total_size = len(fi.data)
        else:
            # BinaryIO：分块流式写入，内存峰值 = _STREAM_CHUNK_SIZE
            while True:
                chunk = fi.data.read(_STREAM_CHUNK_SIZE)  # type: ignore
                if not chunk:
                    break
                f.write(chunk)
                total_size += len(chunk)

    ct = fi.content_type or "application/octet-stream"
    fn = fi.filename or "upload"
    return ResolvedFile(
        file_path=Path(tmp_path), content_type=ct, filename=fn,
        size=total_size, is_temp=True,
    )


def _filename_from_url(url: str) -> str:
    parsed = urlparse(url)
    path = unquote(parsed.path)
    name = Path(path).name
    return name if name else "download"
