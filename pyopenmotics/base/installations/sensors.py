"""Asynchronous Python client for OpenMotics."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional
import asyncio
# import json

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401


class Sensors:
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
    ) -> Sensors:
        """Return an Agreement object from a data dictionary."""
        return Sensors(
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
        path = f"/base/installations/{installation_id}/sensors"
        if filter:
            query_params = {"filter": filter}
            return await self.api_client.get(path, params=query_params)
        
        return await self.api_client.get(path)

    async def by_id(
        self,
        installation_id: str = None,
        sensor_id: str = None,
    ):
        path = f"/base/installations/{installation_id}/sensors/{sensor_id}"
        return await self.api_client.get(path)

    async def historical(
        self,
        installation_id: str = None,
        sensor_id: str = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        resolution: Optional[str] = '5m',
        group_function: Optional[str] = 'last',
        use_active_hours: Optional[bool] = False,
        time_format: Optional[str] = 'iso'
    ):
        """
        {
          "data": {
            "time": "1970-01-01T00:10:00",
            "tags": {
                "sensor_id": "6",
                "sensor_name": "Sensor 0",
                "gateway_id": 1
            },
        "values": {
          "temperature": 22.1
            }
        },
        "_acl": null,
        "_error": null
        }
        """
        path = f"/base/installations/{installation_id}/sensors/{sensor_id}/historical?start={start}&end={end}&resolution={resolution}&group_function={group_function}&use_active_hours={use_active_hours}&time_format={time_format}"
        return await self.api_client.get(path)
