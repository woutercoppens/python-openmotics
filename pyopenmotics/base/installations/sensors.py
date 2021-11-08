"""Asynchronous Python client for OpenMotics."""
from __future__ import annotations

# import asyncio
from typing import TYPE_CHECKING, Any, Optional

# import json

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401


class Sensors:
    # id: Optional[str] = None
    # name: Optional[str] = None
    # version: Optional[str] = None
    # user_role: Optional[list[str]] = None
    # features: Optional[list[str]] = None

    def __init__(self, api_client: Api = None):
        self.api_client = api_client

    def all(
        self,
        installation_id: str = None,
        sensors_filter: Optional[str] = None,
    ) -> Any:
        path = f"/base/installations/{installation_id}/sensors"
        if sensors_filter:
            query_params = {"filter": sensors_filter}
            return self.api_client.get(path, params=query_params)

        return self.api_client.get(path)

    def by_id(
        self,
        installation_id: str = None,
        sensor_id: str = None,
    ):
        path = f"/base/installations/{installation_id}/sensors/{sensor_id}"
        return self.api_client.get(path)

    def historical(
        self,
        installation_id: str = None,
        sensor_id: str = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        resolution: Optional[str] = "5m",
        group_function: Optional[str] = "last",
        use_active_hours: Optional[bool] = False,
        time_format: Optional[str] = "iso",
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
        # E501 line too long
        path = (
            f"/base/installations/{installation_id}/sensors/{sensor_id}"
            f"/historical?start={start}&end={end}&resolution={resolution}"
            f"&group_function={group_function}&use_active_hours={use_active_hours}"
            f"&time_format={time_format}"
        )
        return self.api_client.get(path)
