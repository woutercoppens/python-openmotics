"""Asynchronous Python client for OpenMotics."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional
import asyncio
# import json

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401


class Inputs:
    id: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    user_role: Optional[list[str]] = None
    features: Optional[list[str]] = None

    def __init__(self, api_client: Api = None):
        self.api_client = api_client

    @staticmethod
    def from_dict(
        data: Dict[str, Any],
    ) -> Inputs:
        """Return an Agreement object from a data dictionary."""
        return Inputs(
            id=data.get("id"),
            name=data.get("name"),
            user_role=data.get("user_role"),
            features=data.get("features"),
        )

    async def all(
        self,
        installation_id: str = None,
    ):
        path = f"/base/installations/{installation_id}/inputs"
        return await self.api_client.get(path)

    async def by_id(
        self,
        installation_id: str = None,
        input_id: str = None,
    ):
        path = f"/base/installations/{installation_id}/inputs/{input_id}"
        return await self.api_client.get(path)

