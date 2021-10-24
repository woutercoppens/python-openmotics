"""Asynchronous Python client for OpenMotics."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional
import asyncio
import json

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401


class Shutters:
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
    ) -> Shutters:
        """Return an Agreement object from a data dictionary."""
        return Shutters(
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
        path = f"/base/installations/{installation_id}/shutters"
        if filter:
            query_params = {"filter": filter}
            return await self.api_client.get(path, params=query_params)
        
        return await self.api_client.get(path)

    async def by_id(
        self,
        installation_id: str = None,
        shutter_id: str = None,
    ):
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}"
        return await self.api_client.get(path)

    async def up(
        self,
        installation_id: str = None,
        shutter_id: str = None,
    ):
        path = "/base/installations/{installation_id}/shutters/{shutter_id}/up"
        return await self.api_client.post(path)

    async def down(
        self,
        installation_id: str = None,
        shutter_id: str = None,
    ):
        path = "/base/installations/{installation_id}/shutters/{shutter_id}/down"
        return await self.api_client.post(path)

    async def stop(
        self,
        installation_id: str = None,
        shutter_id: str = None,
    ):
        path = "/base/installations/{installation_id}/shutters/{shutter_id}/stop"
        return await self.api_client.post(path)

    # def change_direction()
    # Deprecated in favor of .../shutters/:id/up and .../shutters/:id/down.
    
    async def change_position(
        self,
        installation_id: str = None,
        shutter_id: str = None,
        position: str= None,
    ):
        path = "/base/installations/{installation_id}/shutters/{shutter_id}/change_position"
        payload = json.dumps(
            {
                "position": position,
            }
        )
        return await self.api_client.post(path, data=payload)


    async def change_relative_position(
        self,
        installation_id: str = None,
        shutter_id: str = None,
        offset: str= None,
    ):
        path = "/base/installations/{installation_id}/shutters/{shutter_id}/change_relative_position"
        payload = json.dumps(
            {
                "offset": offset,
            }
        )
        return await self.api_client.post(path, data=payload)

    async def lock(
        self,
        installation_id: str = None,
        shutter_id: str = None,
    ):
        path = "/base/installations/{installation_id}/shutters/{shutter_id}/lock"
        return await self.api_client.post(path)

    async def unlock(
        self,
        installation_id: str = None,
        shutter_id: str = None,
    ):
        path = "/base/installations/{installation_id}/shutters/{shutter_id}/unlock"
        return await self.api_client.post(path)

    async def preset(
        self,
        installation_id: str = None,
        shutter_id: str = None,
        position: str= None,
    ):
        path = "/base/installations/{installation_id}/shutters/{shutter_id}/preset"
        payload = json.dumps(
            {
                "position": position,
            }
        )
        return await self.api_client.post(path, data=payload)

    async def move_to_preset(
        self,
        installation_id: str = None,
        shutter_id: str = None,
        position: str= None,
    ):
        path = "/base/installations/{installation_id}/shutters/{shutter_id}/move"
        return await self.api_client.post(path)
