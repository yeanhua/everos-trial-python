"""MemoriesResourceWithMultimodal — Pattern A（继承 override）。

继承 Stainless 生成的 MemoriesResource，override add() 增加多模态路由。
生成文件保持原样，只在 _client.py 中替换资源实例（由 make apply-ext 完成）：

    self.memories = MemoriesResourceWithMultimodal(self)

对比 patch 方案的优势：
  - 不修改生成文件（memories.py 保持纯生成形式）
  - 无需 _add_raw 重命名，Stainless 三路合并更干净
  - 继承链清晰，IDE 类型推断完整
"""

from __future__ import annotations

from typing import Callable, List, Optional, TYPE_CHECKING

from ._errors import MultimodalError
from ._files import FileInput

# 兼容两种 SDK 布局：
#   Stainless 生成（扁平）: resources/memories.py  → from ..resources.memories import MemoriesResource
#   sdk_stub（包）:         resources/memories/memories.py → from ..resources.memories.memories import MemoriesResource
try:
    from ..resources.memories.memories import MemoriesResource  # sdk_stub / package layout
except ModuleNotFoundError:
    from ..resources.memories import MemoriesResource  # type: ignore[no-redef]  # Stainless flat layout

if TYPE_CHECKING:
    from ..types.memory_add_response import MemoryAddResponse

_ALLOWED_TYPES = frozenset({"text", "image", "video", "document"})


class MemoriesResourceWithMultimodal(MemoriesResource):
    """继承生成的 MemoriesResource，override add() 增加多模态路由。"""

    def add(
        self,
        *,
        content: str,
        type: str = "text",
        user_id: str,
        files: Optional[List[FileInput]] = None,
        on_progress: Optional[Callable[[str, int, int], None]] = None,
        max_workers: int = 4,
        object_keys: Optional[List[str]] = None,
        **kwargs,
    ) -> "MemoryAddResponse":
        """添加记忆 — 纯文本和多模态统一入口。

        路由逻辑（由 type 字段决定）：
        - type="text"（默认）：直接 POST，现有行为零改动
        - type="image"/"video"/"document" + files：SDK 自动 presign → upload → POST
        - type!="text" + object_keys：底层逃生舱，跳过 SDK 上传
        """
        # ─── 早期校验 ───
        if type not in _ALLOWED_TYPES:
            raise MultimodalError(
                f"type='{type}' is not supported. "
                f"Allowed values: {', '.join(sorted(_ALLOWED_TYPES))}"
            )

        if files and object_keys is not None:
            raise MultimodalError(
                "files and object_keys are mutually exclusive — "
                "pass files for SDK-managed upload, or object_keys for pre-uploaded files, not both."
            )

        # 路径 1：纯文本 — 零改动
        if type == "text":
            if files:
                raise MultimodalError(
                    "files parameter is not allowed when type='text'. "
                    "Set type to 'image', 'video', or 'document' for multimodal content."
                )
            return super().add(content=content, type=type, user_id=user_id, **kwargs)

        # 路径 2：底层逃生舱 — 用户已手动上传
        if object_keys is not None:
            return super().add(
                content=content, type=type, user_id=user_id,
                object_keys=object_keys, **kwargs,
            )

        # 路径 3：高层多模态 — SDK 自动编排
        if not files:
            raise MultimodalError(
                f"files is required when type='{type}'. "
                f"Provide files=[FileInput(...)] or use object_keys for pre-uploaded files."
            )

        from ._multimodal import upload_files_and_add  # noqa: PLC0415

        return upload_files_and_add(
            self,
            content=content,
            type=type,
            files=files,
            user_id=user_id,
            on_progress=on_progress,
            max_workers=max_workers,
            raw_add_fn=super().add,
            **kwargs,
        )
