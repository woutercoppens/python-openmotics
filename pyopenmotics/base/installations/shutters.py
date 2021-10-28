"""Asynchronous Python client for OpenMotics."""
from __future__ import annotations

# import asyncio
import json
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401


class Shutters:

    def __init__(self, api_client: Api = None):
        self.api_client = api_client

    def all(
        self,
        installation_id: str = None,
        shutter_filter: Optional[str] = None,
    ) -> Any:
        path = f"/base/installations/{installation_id}/shutters"
        if shutter_filter:
            query_params = {"filter": shutter_filter}
            return self.api_client.get(path, params=query_params)

        return self.api_client.get(path)

    def by_id(
        self,
        installation_id: str = None,
        shutter_id: str = None,
    ):
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}"
        return self.api_client.get(path)

    def up(
        self,
        installation_id: str = None,
        shutter_id: str = None,
    ):
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/up"
        return self.api_client.post(path)

    def down(
        self,
        installation_id: str = None,
        shutter_id: str = None,
    ):
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/down"
        return self.api_client.post(path)

    def stop(
        self,
        installation_id: str = None,
        shutter_id: str = None,
    ):
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/stop"
        return self.api_client.post(path)

    # def change_direction()
    # Deprecated in favor of .../shutters/:id/up and .../shutters/:id/down.

    def change_position(
        self,
        installation_id: str = None,
        shutter_id: str = None,
        position: str = None,
    ):
        # E501 line too long
        path = (
            f"/base/installations/{installation_id}"
            f"/shutters/{shutter_id}/change_position"
        )
        payload = json.dumps(
            {
                "position": position,
            }
        )
        return self.api_client.post(path, data=payload)

    def change_relative_position(
        self,
        installation_id: str = None,
        shutter_id: str = None,
        offset: str = None,
    ):
        # E501 line too long
        path = (
            f"/base/installations/{installation_id}"
            f"/shutters/{shutter_id}/change_relative_position"
        )
        payload = json.dumps(
            {
                "offset": offset,
            }
        )
        return self.api_client.post(path, data=payload)

    def lock(
        self,
        installation_id: str = None,
        shutter_id: str = None,
    ):
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/lock"
        return self.api_client.post(path)

    def unlock(
        self,
        installation_id: str = None,
        shutter_id: str = None,
    ):
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/unlock"
        return self.api_client.post(path)

    def preset(
        self,
        installation_id: str = None,
        shutter_id: str = None,
        position: str = None,
    ):
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/preset"
        payload = json.dumps(
            {
                "position": position,
            }
        )
        return self.api_client.post(path, body=payload)

    def move_to_preset(
        self,
        installation_id: str = None,
        shutter_id: str = None,
    ):
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/move"
        return self.api_client.post(path)
