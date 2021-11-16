"""Asynchronous Python client for OpenMotics."""
from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401

logger = logging.getLogger(__name__)


class Outputs:
    """A Output object represents a output device.

    An Output is connected to an appliance (e.g. a light, valve, socket, ...)
    and can be used to control that appliance.
    """

    def __init__(self, api_client: Api):
        """Init the output object.

        Args:
            api_client: Api
        """
        self.api_client = api_client

    def all(  # noqa: A003
        self,
        installation_id: int,
    ) -> dict[str, Any]:
        """Get a list of all output objects.

        Args:
            installation_id: int

        Returns:
            Dict with all outputs

        # noqa: E800
        # [{
        #   'name': 'name1',
        #   'type': 'OUTLET',
        #   'capabilities': ['ON_OFF'],
        #   'location': {'floor_coordinates': {'x': None, 'y': None},
        #   'installation_id': 21,
        #   'gateway_id': 408,
        #   'floor_id': None,
        #   'room_id': None},
        #   'metadata': None,
        #   'status': {'on': False, 'locked': False, 'manual_override': False},
        #   'last_state_change': 1633099611.275243,
        #   'id': 18,
        #   '_version': 1.0
        #   },{
        #   'name': 'name2',
        #   'type': 'OUTLET',
        #   ...
        """
        path = f"/base/installations/{installation_id}/outputs"
        return self.api_client.get(path)

    def by_filter(
        self,
        installation_id: int,
        output_filter: str,
    ) -> dict[str, Any]:
        """Get a list of all output objects.

        Args:
            installation_id: int
            output_filter: str

        Returns:
            Dict with all outputs

        # noqa: E800
        # [{
        #     'name': 'name1',
        #     'type': 'OUTLET',
        #     'capabilities': ['ON_OFF'],
        #     'location': {'floor_coordinates': {'x': None, 'y': None},
        #     'installation_id': 21,
        #     'gateway_id': 408,
        #     'floor_id': None,
        #     'room_id': None},
        #     'metadata': None,
        #     'status': {'on': False, 'locked': False, 'manual_override': False},
        #     'last_state_change': 1633099611.275243,
        #     'id': 18,
        #     '_version': 1.0
        #     },{
        #     'name': 'name2',
        #     'type': 'OUTLET',
        #     ...
        """
        path = f"/base/installations/{installation_id}/outputs"
        query_params = {"filter": output_filter}
        return self.api_client.get(
            path=path,
            params=query_params,
        )

    def by_id(
        self,
        installation_id: int,
        output_id: int,
    ) -> dict[str, Any]:
        """Get output by id.

        Args:
            installation_id: int
            output_id: int

        Returns:
            Returns a output with id

        # noqa: E800
        # {
        #     'name': 'Dinning Table',
        #     'type': 'OUTLET',
        #     'capabilities': ['ON_OFF', 'RANGE'],
        #     'location': {'floor_coordinates': {'x': 59, 'y': 55},
        #     'installation_id': 21,
        #     'gateway_id': 408,
        #     'floor_id': None,
        #     'room_id': None},
        #     'metadata': None,
        #     'status': {'on': False, 'locked': False,
        #                'value': 100, 'manual_override': False},
        #     'last_state_change': 1634799514.671482,
        #     'id': 70,
        #     '_version': 1.0
        # }
        """
        path = f"/base/installations/{installation_id}/outputs/{output_id}"
        return self.api_client.get(path)

    def toggle(
        self,
        installation_id: int,
        output_id: int,
    ) -> dict[str, Any]:
        """Toggle a specified Output object.

        Args:
            installation_id: int
            output_id: int

        Returns:
            Returns a output with id
        """
        path = f"/base/installations/{installation_id}/outputs/{output_id}/toggle"
        return self.api_client.post(path)

    def turn_on(
        self,
        installation_id: int,
        output_id: int,
        value: int | None = 100,
    ) -> dict[str, Any]:
        """Turn on a specified Output object.

        Args:
            installation_id: int
            output_id: int
            value: <0 - 100>

        Returns:
            Returns a output with id
        """
        path = f"/base/installations/{installation_id}/outputs/{output_id}/turn_on"
        payload = {"value": value}
        return self.api_client.post(path, json=payload)

    def turn_off(
        self,
        installation_id: int,
        output_id: int | None = None,
    ) -> dict[str, Any]:
        """Turn off a specified Output object.

        Args:
            installation_id: int
            output_id: int

        Returns:
            Returns a output with id
        """
        if output_id is None:
            # Turn off all lights
            path = f"/base/installations/{installation_id}/outputs/turn_off"
        else:
            # Turn off light with id
            path = f"/base/installations/{installation_id}/outputs/{output_id}/turn_off"
        return self.api_client.post(path)

    def location(
        self,
        installation_id: int,
        output_id: int,
        floor_id: str = None,
        floor_coordinates_x: str = None,
        floor_coordinates_y: str = None,
    ) -> dict[str, Any]:
        """Get all output at this location.

        Args:
            installation_id: int
            output_id: int
            floor_id: str
            floor_coordinates_x: str
            floor_coordinates_y: str

        Returns:
            Returns the outputs at location
        """
        path = f"/base/installations/{installation_id}/outputs/{output_id}/location"
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

    def by_type(
        self,
        installation_id: int,
        output_type: str,
    ) -> dict[str, Any]:
        """Get all outputs by type.

        Args:
            installation_id: int
            output_type: int

        Returns:
            Returns a output with type
        """
        output_filter = json.dumps({"type": output_type.upper()})
        return self.by_filter(
            installation_id=installation_id,
            output_filter=output_filter,
        )

    def lights(
        self,
        installation_id: int,
    ) -> dict[str, Any]:
        """Get all outputs by type light.

        Args:
            installation_id: int

        Returns:
            Returns all lights
        """
        return self.by_type(
            installation_id=installation_id,
            output_type="LIGHT",
        )

    def outlets(
        self,
        installation_id: int,
    ) -> dict[str, Any]:
        """Get all outputs by type outlet.

        Args:
            installation_id: int

        Returns:
            Returns all outlets
        """
        return self.by_type(
            installation_id=installation_id,
            output_type="OUTLET",
        )

    def by_usage(
        self,
        installation_id: int,
        output_usage: str,
    ) -> dict[str, Any]:
        """Get all outputs by usage.

        Args:
            installation_id: int
            output_usage: str

        Returns:
            Returns all outlets
        """
        output_filter = json.dumps({"usage": output_usage.upper()})
        return self.by_filter(
            installation_id=installation_id,
            output_filter=output_filter,
        )
