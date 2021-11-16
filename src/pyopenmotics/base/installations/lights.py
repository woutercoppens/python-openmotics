"""Asynchronous Python client for OpenMotics.

A light can be represented in 2 different ways: some gateways support lights with all
their capabilities (color etc.), while others consider lights as a type of outputs
(see /outputs).
This section documents the gateways having full Light support.
"""
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401


class Lights:
    """A Light object represents a output device."""

    def __init__(self, api_client: Api):
        """Init the light object.

        Args:
            api_client: Api
        """

        self.api_client = api_client

    def all(  # noqa: A003
        self,
        installation_id: int,
    ) -> dict[str, Any]:
        """Get a list of all lights objects.

        Args:
            installation_id: int

        Returns:
            Dict with all lights

        # noqa: E800
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
        """
        path = f"/base/installations/{installation_id}/lights"
        return self.api_client.get(path)

    def by_id(
        self,
        installation_id: int,
        light_id: int,
    ) -> dict[str, Any]:
        """Get light by id.

        Args:
            installation_id: int
            light_id: int

        Returns:
            Returns a light with id

        # noqa: E800
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
        """
        path = f"/base/installations/{installation_id}/lights/{light_id}"
        return self.api_client.get(path)

    # pylint: disable=too-many-arguments
    def turn_on(
        self,
        installation_id: int,
        light_id: int,
        value: int | None = 100,
        temperature: int | None = None,
        hue: int | None = None,
        saturation: int | None = None,
        red: int | None = None,
        green: int | None = None,
        blue: int | None = None,
    ) -> dict[str, Any]:
        """Turn on a specified light object.

        Args:
            installation_id: int
            light_id: int
            value: <0 - 100>
            temperature: <int>
            hue: <0 - 360>
            saturation: <0 - 100>
            red: <0 - 255>
            green: <0 - 255>
            blue: <0 - 255>

        Returns:
            Returns a light with id
        """
        path = f"/base/installations/{installation_id}/lights/{light_id}/turn_on"
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
        return self.api_client.post(path, json=payload)

    def turn_off(
        self,
        installation_id: int,
        light_id: int,
    ) -> dict[str, Any]:
        """Turn off a specified light object.

        Args:
            installation_id: int
            light_id: int

        Returns:
            Returns a light with id
        """

        path = f"/base/installations/{installation_id}/lights/{light_id}/turn_off"
        return self.api_client.post(path)

    # pylint: disable=too-many-arguments
    def location(
        self,
        installation_id: int,
        light_id: int,
        floor_id: str = None,
        floor_coordinates_x: str = None,
        floor_coordinates_y: str = None,
    ) -> dict[str, Any]:
        """Set the location of a light.

        Args:
            installation_id: int
            light_id: int
            floor_id: str = None
            floor_coordinates_x: str = None
            floor_coordinates_y: str = None

        Returns:
            Dict
        """

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
        return self.api_client.post(path, json=payload)
