"""Asynchronous Python client for OpenMotics.

A light can be represented in 2 different ways: some gateways support lights with all
their capabilities (color etc.), while others consider lights as a type of outputs
(see /outputs).
This section documents the gateways having full Light support.
"""
from __future__ import annotations

# import asyncio
import json
from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401


class Lights:
    """Doc String."""

    # id: Optional[str] = None
    # name: Optional[str] = None
    # version: Optional[str] = None
    # user_role: Optional[list[str]] = None
    # features: Optional[list[str]] = None
    # payload: dict[str, any] | None = None

    def __init__(self, api_client: Api):
        """Doc String."""

        self.api_client = api_client

    def all(
        self,
        installation_id: str = None,
    ) -> Any:
        """Doc String."""

        # [{
        #     'name': 'name1',
        #     'capabilities': ['ON_OFF', 'RANGE', 'WHITE_TEMP', 'FULL_COLOR'],
        #     'location': {
        #         'floor_coordinates': {'x': None, 'y': None},
        #         'installation_id': 1,
        #         'floor_id': None,
        #         'room_id': None}
        #         }
        #     'metadata': None,
        #     'status': {'on': False, 'locked': False, 'manual_override': False},
        #     'last_state_change': 1633099611.275243,
        #     'id': 18,
        #     '_version': 1.0
        #     },{
        #     'name': 'name2',
        #     ...

        path = f"/base/installations/{installation_id}/lights"
        return self.api_client.get(path)

    def by_id(
        self,
        installation_id: str = None,
        light_id: str = None,
    ) -> Any:
        """Doc String."""

        # {
        #     'name': 'name1',
        #     'capabilities': ['ON_OFF', 'RANGE', 'WHITE_TEMP', 'FULL_COLOR'],
        #     'location': {
        #         'floor_coordinates': {'x': None, 'y': None},
        #         'installation_id': 1,
        #         'floor_id': None,
        #         'room_id': None}
        #         }
        #     'metadata': None,
        #     'status': {'on': False, 'locked': False, 'manual_override': False},
        #     'last_state_change': 1633099611.275243,
        #     'id': 18,
        #     '_version': 1.0
        # }

        path = f"/base/installations/{installation_id}/lights/{light_id}"
        return self.api_client.get(path)

    def turn_on(
        self,
        installation_id: str = None,
        light_id: str = None,
        value: int | None = 100,
        temperature: int | None = None,
        hue: int | None = None,
        saturation: int | None = None,
        red: int | None = None,
        green: int | None = None,
        blue: int | None = None,
    ):
        """Doc String."""
        path = f"/base/installations/{installation_id}/lights/{light_id}/turn_on"
        # {
        #     "value": <0 - 100>,
        #     "temperature": <int>,
        #     "hue": <0 - 360>,
        #     "saturation": <0 - 100>,
        #     "red": <0 - 255>,
        #     "green": <0 - 255>,
        #     "blue": <0 - 255>
        #     }
        payload = json.dumps(
            {
                "value": value,
                "temperature": temperature,
                "hue": hue,
                "saturation": saturation,
                "red": red,
                "green": green,
                "blue": blue,
            }
        )
        return self.api_client.post(path, body=payload)

    def turn_off(
        self,
        installation_id: str = None,
        light_id: str = None,
    ):
        """Doc String."""
        path = f"/base/installations/{installation_id}/lights/{light_id}/turn_off"
        return self.api_client.post(path)

    def location(
        self,
        installation_id: str = None,
        light_id: str = None,
        floor_id: str = None,
        floor_coordinates_x: str = None,
        floor_coordinates_y: str = None,
    ):
        """Doc String."""

        path = f"/base/installations/{installation_id}/lights/{light_id}/location"
        payload = json.dumps(
            {
                "floor_id": floor_id,
                "floor_coordinates": {
                    "x": floor_coordinates_x,
                    "y": floor_coordinates_y,
                },
            }
        )
        return self.api_client.post(path, body=payload)
