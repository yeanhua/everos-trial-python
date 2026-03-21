"""多模态上传相关异常。"""


class MultimodalError(Exception):
    """多模态操作的基类异常。"""
    pass


class FileResolveError(MultimodalError):
    """文件解析失败（路径不存在、URL 下载失败、文件过大等）。"""
    pass


class UploadError(MultimodalError):
    """S3 上传失败。"""
    pass
