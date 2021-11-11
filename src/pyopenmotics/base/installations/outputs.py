"""Asynchronous Python client for OpenMotics."""
from __future__ import annotations

# import asyncio
import json
import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401

logger = logging.getLogger(__name__)


class Outputs:
    """Doc String."""

    # id: Optional[str] = None
    # name: Optional[str] = None
    # version: Optional[str] = None
    # user_role: Optional[list[str]] = None
    # features: Optional[list[str]] = None

    def __init__(self, api_client: Api):
        """Doc String."""
        self.api_client = api_client

    def all(
        self,
        installation_id: str,
    ) -> dict[str, Any]:
        """Doc String."""

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

        path = f"/base/installations/{installation_id}/outputs"
        return self.api_client.get(path)

    def by_filter(
        self,
        installation_id: str,
        output_filter: str,
    ) -> dict[str, Any]:
        """Doc String."""

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

        path = f"/base/installations/{installation_id}/outputs"
        query_params = {"filter": output_filter}
        return self.api_client.get(
            path=path,
            params=query_params,
        )

    def by_id(
        self,
        installation_id: str,
        output_id: str,
    ) -> dict[str, Any]:
        """Doc String."""

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

        path = f"/base/installations/{installation_id}/outputs/{output_id}"
        return self.api_client.get(path)

    def toggle(
        self,
        installation_id: str,
        output_id: str,
    ) -> dict[str, Any]:
        """Doc String."""
        path = f"/base/installations/{installation_id}/outputs/{output_id}/toggle"
        return self.api_client.post(path)

    def turn_on(
        self,
        installation_id: str,
        output_id: str,
        value: int | None = 100,
    ) -> dict[str, Any]:
        """Doc String."""
        path = f"/base/installations/{installation_id}/outputs/{output_id}/turn_on"
        payload = {"value": value}
        return self.api_client.post(path, json=payload)

    def turn_off(
        self,
        installation_id: str,
        output_id: str | None = None,
    ) -> dict[str, Any]:
        """Doc String."""
        if output_id is None:
            # Turn off all lights
            path = f"/base/installations/{installation_id}/outputs/turn_off"
        else:
            # Turn off light with id
            path = f"/base/installations/{installation_id}/outputs/{output_id}/turn_off"
        return self.api_client.post(path)

    def location(
        self,
        installation_id: str,
        output_id: str,
        floor_id: str = None,
        floor_coordinates_x: str = None,
        floor_coordinates_y: str = None,
    ) -> dict[str, Any]:
        """Doc String."""
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
        installation_id: str,
        output_type: str,
    ) -> dict[str, Any]:
        """Doc String."""
        output_filter = json.dumps({"type": output_type.upper()})
        return self.by_filter(
            installation_id=installation_id,
            output_filter=output_filter,
        )

    def lights(
        self,
        installation_id: str,
    ) -> dict[str, Any]:
        """Doc String."""
        return self.by_type(
            installation_id=installation_id,
            output_type="LIGHT",
        )

    def outlets(
        self,
        installation_id: str,
    ) -> dict[str, Any]:
        """Doc String."""
        return self.by_type(
            installation_id=installation_id,
            output_type="OUTLET",
        )

    def by_usage(
        self,
        installation_id: str,
        output_usage: str,
    ) -> dict[str, Any]:
        """Doc String."""
        output_filter = json.dumps({"usage": output_usage.upper()})
        return self.by_filter(
            installation_id=installation_id,
            output_filter=output_filter,
        )