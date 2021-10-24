"""Asynchronous Python client for OpenMotics."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional
import asyncio
# import json

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401


class Groupactions:
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
    ) -> Groupactions:
        """Return an Agreement object from a data dictionary."""
        return Groupactions(
            id=data.get("id"),
            name=data.get("name"),
            user_role=data.get("user_role"),
            features=data.get("features"),
        )

    async def all(
        self,
        installation_id: str = None,
        filter: Optional[str] = None,
    ):
        """
        [{
            "_version": <version>,
            "actions": [
                <action type>, <action number>, 
                <action type>, <action number>, 
                ...
            ],
        "id": <id>,
        "location": {
            "installation_id": <installation id>
        },
        "name": "<name>"
        }
        """
        path = f"/base/installations/{installation_id}/groupactions"
        if filter:
            query_params = {'filter': filter}
            return await self.api_client.get(path, params=query_params)
        
        return await self.api_client.get(path)

    async def by_id(
        self,
        installation_id: str = None,
        groupaction_id: str = None,
    ):
        path = f"/base/installations/{installation_id}/groupactions/{groupaction_id}"
        return await self.api_client.get(path)

    async def trigger(
        self,
        installation_id: str = None,
        groupaction_id: str = None,
    ):
        path = f"/base/installations/{installation_id}/groupactions/{groupaction_id}/trigger"
        return await self.api_client.post(path)

    async def by_usage(
        self,
        installation_id: str = None,
        groupaction_usage: str = None,
    ):
        path = f"/base/installations/{installation_id}/groupactions"
        query_params = {'usage': groupaction_usage.upper()}
        return await self.api_client.get(path, params=query_params)

    def scenes(self, installation_id):
        return self.by_usage(self, installation_id, "SCENE")