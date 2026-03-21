# Memories

Types:

```python
from evermemos.types import MemoryRetrieveResponse, MemoryAddResponse
```

Methods:

- <code title="get /api/v1/memories/{id}">client.memories.<a href="./src/evermemos/resources/memories.py">retrieve</a>(id) -> <a href="./src/evermemos/types/memory_retrieve_response.py">MemoryRetrieveResponse</a></code>
- <code title="post /api/v1/memories">client.memories.<a href="./src/evermemos/resources/memories.py">add</a>(\*\*<a href="src/evermemos/types/memory_add_params.py">params</a>) -> <a href="./src/evermemos/types/memory_add_response.py">MemoryAddResponse</a></code>

# Storage

Types:

```python
from evermemos.types import StorageCreatePresignedURLResponse
```

Methods:

- <code title="post /api/v1/storage/presign">client.storage.<a href="./src/evermemos/resources/storage.py">create_presigned_url</a>(\*\*<a href="src/evermemos/types/storage_create_presigned_url_params.py">params</a>) -> <a href="./src/evermemos/types/storage_create_presigned_url_response.py">StorageCreatePresignedURLResponse</a></code>
