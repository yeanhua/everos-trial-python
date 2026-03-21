"""多模态 add 编排：resolve → presign → upload → add memory。

保序：object_keys[i] 始终对应 files[i]。
Best-effort fail-fast：尽早发现失败并取消尚未开始的任务。
已在执行中的任务（最多 max_workers 个）无法中断，可能产生孤儿对象。
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Literal, Callable
from concurrent.futures import Future, ThreadPoolExecutor, as_completed

from ._files import FileInput, ResolvedFile, resolve_file, async_resolve_file
from ._errors import MultimodalError, FileResolveError
from ._upload import UploadResult, presign_and_upload, async_presign_and_upload

if TYPE_CHECKING:
    from typing import Awaitable

    from ..resources.memories import MemoriesResource, AsyncMemoriesResource
    from ..types.memory_add_response import MemoryAddResponse


# ─── 同步版本 ───


def upload_files_and_add(
    resource: "MemoriesResource",
    *,
    content: str,
    type: Literal["image", "video", "document"],
    files: list[FileInput],
    user_id: str,
    on_progress: Callable[[str, int, int], None] | None = None,
    max_workers: int = 4,
    raw_add_fn: "Callable[..., MemoryAddResponse]",
    **kwargs: Any,
) -> "MemoryAddResponse":
    """同步编排：顺序解析 → 保序并发上传（best-effort fail-fast）→ add。

    raw_add_fn: 最终 HTTP POST 的可调用对象。Pattern A 中由调用方传入
                super().add（父类的原始 add），确保绕过子类的路由逻辑。
    """

    if not files:
        raise MultimodalError("files cannot be empty when type is not 'text'")

    n = len(files)
    resolved: list[ResolvedFile] = []

    try:
        # Step 1: 顺序解析（保证 resolved[i] 对应 files[i]）
        for i, fi in enumerate(files):
            try:
                resolved.append(resolve_file(fi))
            except Exception as e:
                raise FileResolveError(
                    f"Failed to resolve files[{i}] ({_file_desc(fi)}): {e}"
                ) from e

        # Step 2: 保序并发上传（as_completed + index slot）
        client = resource._client
        results: list[UploadResult | None] = [None] * n
        done_count = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_idx: dict[Future[UploadResult], int] = {}
            futures: list[Future[UploadResult]] = []
            for i in range(n):
                fut = executor.submit(presign_and_upload, client, resolved[i])
                futures.append(fut)
                future_to_idx[fut] = i

            first_error: Exception | None = None
            first_error_idx: int = -1

            for fut in as_completed(future_to_idx):
                idx = future_to_idx[fut]
                try:
                    results[idx] = fut.result()
                    done_count += 1
                    if on_progress:
                        on_progress(results[idx].filename, done_count, n)  # type: ignore
                except Exception as e:
                    first_error = e
                    first_error_idx = idx
                    # Best-effort 取消：只能取消尚未开始执行的 future
                    for other_fut in futures:
                        if other_fut is not fut:
                            other_fut.cancel()
                    break

            if first_error is not None:
                raise MultimodalError(
                    f"Upload failed at files[{first_error_idx}] "
                    f"({resolved[first_error_idx].filename}): {first_error}. "
                    f"Note: up to {max_workers} in-flight uploads may have completed "
                    f"and produced orphan objects in S3."
                ) from first_error

        # Step 3: 调用 raw_add_fn（顺序已保证）
        object_keys = [r.object_key for r in results if r is not None]
        return raw_add_fn(
            content=content,
            type=type,
            object_keys=object_keys,
            user_id=user_id,
            **kwargs,
        )

    finally:
        for r in resolved:
            r.cleanup()


# ─── 异步版本 ───


async def async_upload_files_and_add(
    resource: "AsyncMemoriesResource",
    *,
    content: str,
    type: Literal["image", "video", "document"],
    files: list[FileInput],
    user_id: str,
    on_progress: Callable[[str, int, int], None] | None = None,
    raw_add_fn: "Callable[..., Awaitable[MemoryAddResponse]]",
    **kwargs: Any,
) -> "MemoryAddResponse":
    """异步编排：并发解析（保序）→ 并发上传（fail-fast）→ add。

    raw_add_fn: 最终 HTTP POST 的可调用对象（async callable）。
    """

    if not files:
        raise MultimodalError("files cannot be empty when type is not 'text'")

    n = len(files)
    resolved: list[ResolvedFile] = []

    try:
        # Step 1: 并发解析，保序收集
        resolve_tasks = [async_resolve_file(fi) for fi in files]
        resolve_results = await asyncio.gather(*resolve_tasks, return_exceptions=True)

        for i, result in enumerate(resolve_results):
            if isinstance(result, BaseException):
                for prev in resolve_results[:i]:
                    if isinstance(prev, ResolvedFile):
                        prev.cleanup()
                raise FileResolveError(
                    f"Failed to resolve files[{i}] ({_file_desc(files[i])}): {result}"
                ) from result
            resolved.append(result)

        # Step 2: 并发上传，保序 + fail-fast
        client = resource._client

        task_to_idx: dict[asyncio.Task[UploadResult], int] = {}
        upload_tasks: list[asyncio.Task[UploadResult]] = []
        for i in range(n):
            task = asyncio.create_task(
                async_presign_and_upload(client, resolved[i]),
                name=f"upload-{i}",
            )
            upload_tasks.append(task)
            task_to_idx[task] = i

        results: list[UploadResult | None] = [None] * n

        done, pending = await asyncio.wait(
            upload_tasks, return_when=asyncio.FIRST_EXCEPTION
        )

        first_error: BaseException | None = None
        first_error_idx: int = -1
        for task in done:
            idx = task_to_idx[task]
            exc = task.exception()
            if exc is not None:
                if first_error is None or idx < first_error_idx:
                    first_error = exc
                    first_error_idx = idx
            else:
                results[idx] = task.result()

        if first_error is not None:
            for task in pending:
                task.cancel()
            if pending:
                await asyncio.wait(pending)
            raise MultimodalError(
                f"Upload failed at files[{first_error_idx}] "
                f"({resolved[first_error_idx].filename}): {first_error}"
            ) from first_error

        if pending:
            done2, _ = await asyncio.wait(pending)
            for task in done2:
                idx = task_to_idx[task]
                results[idx] = task.result()

        if on_progress:
            for i, r in enumerate(results):
                if r is not None:
                    on_progress(r.filename, i + 1, n)

        # Step 3: add
        object_keys = [r.object_key for r in results if r is not None]
        return await raw_add_fn(
            content=content,
            type=type,
            object_keys=object_keys,
            user_id=user_id,
            **kwargs,
        )

    finally:
        for r in resolved:
            r.cleanup()


def _file_desc(fi: FileInput) -> str:
    """生成 FileInput 的简短描述用于错误信息。"""
    if fi.path is not None:
        return f"path={fi.path}"
    elif fi.url is not None:
        return f"url={fi.url}"
    else:
        return f"data, filename={fi.filename}"
