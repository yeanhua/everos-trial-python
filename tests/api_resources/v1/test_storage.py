# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from everos_trial import EverosTrial, AsyncEverosTrial
from everos_trial.types.v1 import StorageGeneratePresignedURLResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStorage:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_generate_presigned_url(self, client: EverosTrial) -> None:
        storage = client.v1.storage.generate_presigned_url(
            content_type="content_type",
            filename="filename",
        )
        assert_matches_type(StorageGeneratePresignedURLResponse, storage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_generate_presigned_url_with_all_params(self, client: EverosTrial) -> None:
        storage = client.v1.storage.generate_presigned_url(
            content_type="content_type",
            filename="filename",
            file_size=0,
        )
        assert_matches_type(StorageGeneratePresignedURLResponse, storage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_generate_presigned_url(self, client: EverosTrial) -> None:
        response = client.v1.storage.with_raw_response.generate_presigned_url(
            content_type="content_type",
            filename="filename",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        storage = response.parse()
        assert_matches_type(StorageGeneratePresignedURLResponse, storage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_generate_presigned_url(self, client: EverosTrial) -> None:
        with client.v1.storage.with_streaming_response.generate_presigned_url(
            content_type="content_type",
            filename="filename",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            storage = response.parse()
            assert_matches_type(StorageGeneratePresignedURLResponse, storage, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncStorage:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_generate_presigned_url(self, async_client: AsyncEverosTrial) -> None:
        storage = await async_client.v1.storage.generate_presigned_url(
            content_type="content_type",
            filename="filename",
        )
        assert_matches_type(StorageGeneratePresignedURLResponse, storage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_generate_presigned_url_with_all_params(self, async_client: AsyncEverosTrial) -> None:
        storage = await async_client.v1.storage.generate_presigned_url(
            content_type="content_type",
            filename="filename",
            file_size=0,
        )
        assert_matches_type(StorageGeneratePresignedURLResponse, storage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_generate_presigned_url(self, async_client: AsyncEverosTrial) -> None:
        response = await async_client.v1.storage.with_raw_response.generate_presigned_url(
            content_type="content_type",
            filename="filename",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        storage = await response.parse()
        assert_matches_type(StorageGeneratePresignedURLResponse, storage, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_generate_presigned_url(self, async_client: AsyncEverosTrial) -> None:
        async with async_client.v1.storage.with_streaming_response.generate_presigned_url(
            content_type="content_type",
            filename="filename",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            storage = await response.parse()
            assert_matches_type(StorageGeneratePresignedURLResponse, storage, path=["response"])

        assert cast(Any, response.is_closed) is True
