# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evermemos import EverMemOs, AsyncEverMemOs
from tests.utils import assert_matches_type
from evermemos.types import StorageCreatePresignedURLResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStorage:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_presigned_url(self, client: EverMemOs) -> None:
        storage = client.storage.create_presigned_url(
            content_type="content_type",
            filename="filename",
        )
        assert_matches_type(StorageCreatePresignedURLResponse, storage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_presigned_url_with_all_params(self, client: EverMemOs) -> None:
        storage = client.storage.create_presigned_url(
            content_type="content_type",
            filename="filename",
            file_size=0,
        )
        assert_matches_type(StorageCreatePresignedURLResponse, storage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create_presigned_url(self, client: EverMemOs) -> None:
        response = client.storage.with_raw_response.create_presigned_url(
            content_type="content_type",
            filename="filename",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        storage = response.parse()
        assert_matches_type(StorageCreatePresignedURLResponse, storage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create_presigned_url(self, client: EverMemOs) -> None:
        with client.storage.with_streaming_response.create_presigned_url(
            content_type="content_type",
            filename="filename",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            storage = response.parse()
            assert_matches_type(StorageCreatePresignedURLResponse, storage, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncStorage:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_presigned_url(self, async_client: AsyncEverMemOs) -> None:
        storage = await async_client.storage.create_presigned_url(
            content_type="content_type",
            filename="filename",
        )
        assert_matches_type(StorageCreatePresignedURLResponse, storage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_presigned_url_with_all_params(self, async_client: AsyncEverMemOs) -> None:
        storage = await async_client.storage.create_presigned_url(
            content_type="content_type",
            filename="filename",
            file_size=0,
        )
        assert_matches_type(StorageCreatePresignedURLResponse, storage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create_presigned_url(self, async_client: AsyncEverMemOs) -> None:
        response = await async_client.storage.with_raw_response.create_presigned_url(
            content_type="content_type",
            filename="filename",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        storage = await response.parse()
        assert_matches_type(StorageCreatePresignedURLResponse, storage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create_presigned_url(self, async_client: AsyncEverMemOs) -> None:
        async with async_client.storage.with_streaming_response.create_presigned_url(
            content_type="content_type",
            filename="filename",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            storage = await response.parse()
            assert_matches_type(StorageCreatePresignedURLResponse, storage, path=["response"])

        assert cast(Any, response.is_closed) is True
