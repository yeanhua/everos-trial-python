# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from everos_trial import EverosTrial, AsyncEverosTrial
from everos_trial.types import V1AddMemoryResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestV1:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_add_memory(self, client: EverosTrial) -> None:
        v1 = client.v1.add_memory(
            content="content",
            user_id="user_id",
        )
        assert_matches_type(V1AddMemoryResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_add_memory_with_all_params(self, client: EverosTrial) -> None:
        v1 = client.v1.add_memory(
            content="content",
            user_id="user_id",
            object_keys=["string"],
            type="text",
        )
        assert_matches_type(V1AddMemoryResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_add_memory(self, client: EverosTrial) -> None:
        response = client.v1.with_raw_response.add_memory(
            content="content",
            user_id="user_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert_matches_type(V1AddMemoryResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_add_memory(self, client: EverosTrial) -> None:
        with client.v1.with_streaming_response.add_memory(
            content="content",
            user_id="user_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert_matches_type(V1AddMemoryResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncV1:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_add_memory(self, async_client: AsyncEverosTrial) -> None:
        v1 = await async_client.v1.add_memory(
            content="content",
            user_id="user_id",
        )
        assert_matches_type(V1AddMemoryResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_add_memory_with_all_params(self, async_client: AsyncEverosTrial) -> None:
        v1 = await async_client.v1.add_memory(
            content="content",
            user_id="user_id",
            object_keys=["string"],
            type="text",
        )
        assert_matches_type(V1AddMemoryResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_add_memory(self, async_client: AsyncEverosTrial) -> None:
        response = await async_client.v1.with_raw_response.add_memory(
            content="content",
            user_id="user_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert_matches_type(V1AddMemoryResponse, v1, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_add_memory(self, async_client: AsyncEverosTrial) -> None:
        async with async_client.v1.with_streaming_response.add_memory(
            content="content",
            user_id="user_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert_matches_type(V1AddMemoryResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True
