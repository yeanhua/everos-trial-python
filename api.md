# Memories

Types:

```python
from everostrial.types import MemoryRetrieveResponse, MemoryAddResponse
```

Methods:

- <code title="get /api/v1/memories/{id}">client.memories.<a href="./src/everostrial/resources/memories.py">retrieve</a>(id) -> <a href="./src/everostrial/types/memory_retrieve_response.py">MemoryRetrieveResponse</a></code>
- <code title="post /api/v1/memories">client.memories.<a href="./src/everostrial/resources/memories.py">add</a>(\*\*<a href="src/everostrial/types/memory_add_params.py">params</a>) -> <a href="./src/everostrial/types/memory_add_response.py">MemoryAddResponse</a></code>

# Storage

Types:

```python
from everostrial.types import StorageCreatePresignedURLResponse
```

Methods:

- <code title="post /api/v1/storage/presign">client.storage.<a href="./src/everostrial/resources/storage.py">create_presigned_url</a>(\*\*<a href="src/everostrial/types/storage_create_presigned_url_params.py">params</a>) -> <a href="./src/everostrial/types/storage_create_presigned_url_response.py">StorageCreatePresignedURLResponse</a></code>
