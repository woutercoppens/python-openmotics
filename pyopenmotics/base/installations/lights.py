"""Asynchronous Python client for OpenMotics.

A light can be represented in 2 different ways: some gateways support lights with all their capabilities (color etc.), while others consider lights as a type of outputs (see /outputs).
This section documents the gateways having full Light support.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional
import asyncio
import json

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401


class Lights:
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
    ) -> Lights:
        """Return an Agreement object from a data dictionary."""
        return Lights(
            id=data.get("id"),
            name=data.get("name"),
            user_role=data.get("user_role"),
            features=data.get("features"),
        )

    async def all(
        self,
        installation_id: str = None,
    ):
        """
        [{
            'name': 'name1',
            'capabilities': ['ON_OFF', 'RANGE', 'WHITE_TEMP', 'FULL_COLOR'],
            'location': {
                'floor_coordinates': {'x': None, 'y': None},
                'installation_id': 1,
                'floor_id': None,
                'room_id': None}
                }
            'metadata': None,
            'status': {'on': False, 'locked': False, 'manual_override': False},
            'last_state_change': 1633099611.275243,
            'id': 18,
            '_version': 1.0
            },{
            'name': 'name2',
            ...
        """
        path = f"/base/installations/{installation_id}/lights"
        return await self.api_client.get(path)

    async def by_id(
        self,
        installation_id: str = None,
        light_id: str = None,
    ):
        """
        {
            'name': 'name1',
            'capabilities': ['ON_OFF', 'RANGE', 'WHITE_TEMP', 'FULL_COLOR'],
            'location': {
                'floor_coordinates': {'x': None, 'y': None},
                'installation_id': 1,
                'floor_id': None,
                'room_id': None}
                }
            'metadata': None,
            'status': {'on': False, 'locked': False, 'manual_override': False},
            'last_state_change': 1633099611.275243,
            'id': 18,
            '_version': 1.0
        }
        """
        path = f"/base/installations/{installation_id}/lights/{light_id}"
        return await self.api_client.get(path)

    async def turn_on(
        self,
        installation_id: str = None,
        light_id: str = None,
        value: Optional[int] = 100,
        temperature: Optional[int] = None,
        hue: Optional[int] = None,
        saturation: Optional[int] = None,
        red: Optional[int] = None,
        green: Optional[int] = None,
        blue: Optional[int] = None,
    ):
        path = f"/base/installations/{installation_id}/lights/{light_id}/turn_on"
        """ { 
            "value": <0 - 100>,
            "temperature": <int>,
            "hue": <0 - 360>,
            "saturation": <0 - 100>,
            "red": <0 - 255>,
            "green": <0 - 255>,
            "blue": <0 - 255>
            } 
        """
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
        return await self.api_client.post(path, json=payload)

    async def turn_off(
        self,
        installation_id: str = None,
        ligth_id: str = None,
    ):
        path = f"/base/installations/{installation_id}/lights/{light_id}/turn_off"
        return await self.api_client.post(path)

    async def location(
        self,
        installation_id: str = None,
        light_id: str = None,
        floor_id: str = None,
        floor_coordinates_x: str = None,
        floor_coordinates_y: str = None,
    ):
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
        return await self.api_client.post(path, data=payload)
