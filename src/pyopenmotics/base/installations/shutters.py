"""Asynchronous Python client for OpenMotics."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401


class Shutters:
    """Object holding functions about shutters.

    A Shutter is a special type of Output and consists out of two Output alike devices.
    One controls the up direction motor, the other one the down direction motor.
    The firmware makes sure up and down cannot be active at the same time.
    """

    def __init__(self, api_client: Api):
        """Init the shutter object.

        Args:
            api_client: Api
        """
        self.api_client = api_client

    def all(  # noqa: A003
        self,
        installation_id: int,
        shutter_filter: str | None = None,
    ) -> dict[str, Any]:
        """List all Shutter objects.

        Args:
            installation_id: int
            shutter_filter: Optional filter

        Returns:
            Dict with all shutters

        usage: The usage filter allows the Shutters to be filtered for their
            intended usage.
            CONTROL: These Shutters can be controlled directly and are not
                managed by an internal process.
        """
        path = f"/base/installations/{installation_id}/shutters"
        if shutter_filter:
            query_params = {"filter": shutter_filter}
            return self.api_client.get(path, params=query_params)

        return self.api_client.get(path)

    def by_id(
        self,
        installation_id: int,
        shutter_id: int,
    ) -> dict[str, Any]:
        """Get a specified Shutter object.

        Args:
            installation_id: int
            shutter_id: int

        Returns:
            Returns a shutter with id
        """
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}"
        return self.api_client.get(path)

    def up(  # noqa: C0103
        self,
        installation_id: int,
        shutter_id: int,
    ) -> dict[str, Any]:
        """Move the specified Shutter into the upwards position.

        Args:
            installation_id: int
            shutter_id: int

        Returns:
            Returns a shutter with id
        """
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/up"
        return self.api_client.post(path)

    def down(
        self,
        installation_id: int,
        shutter_id: int,
    ) -> dict[str, Any]:
        """Move the specified Shutter into the downwards position.

        Args:
            installation_id: int
            shutter_id: int

        Returns:
            Returns a shutter with id
        """
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/down"
        return self.api_client.post(path)

    def stop(
        self,
        installation_id: int,
        shutter_id: int,
    ) -> dict[str, Any]:
        """Stop any movement of the specified Shutter.

        Args:
            installation_id: int
            shutter_id: int

        Returns:
            Returns a shutter with id
        """
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/stop"
        return self.api_client.post(path)

    # def change_direction()
    # Deprecated in favor of .../shutters/:id/up and .../shutters/:id/down.

    def change_position(
        self,
        installation_id: int,
        shutter_id: int,
        position: int,
    ) -> dict[str, Any]:
        """Change the position of the specified Shutter.

        The position can be set from 0 to steps (excluded). The steps value can be
        found in the configuration field of a Shutter.
        Not all gateways or shutters support this feature.

        Args:
            installation_id: int
            shutter_id: int
            position: int  (in body)

        Returns:
            Returns a shutter with id
        """
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
        return self.api_client.post(path, json=payload)

    def change_relative_position(
        self,
        installation_id: int,
        shutter_id: int,
        offset: int,
    ) -> dict[str, Any]:
        """Change the relative position of the specified Shutter.

        The offset can be set from -steps (excluded) to steps (excluded).
        The steps value can be found in the configuration field of a Shutter.
        Not all gateways or shutters support this feature.

        Args:
            installation_id: int
            shutter_id: int
            offset: int (in body)

        Returns:
            Returns a shutter with id
        """
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
        return self.api_client.post(path, json=payload)

    def lock(
        self,
        installation_id: int,
        shutter_id: int,
    ) -> dict[str, Any]:
        """Lock the specified Shutter to prevent future movements.

        The behavior is depending of the capabilities of the Shutter:
            LOCAL_LOCK capability: this lock is a hardware lock, without manual
            override through a local interface.
            CLOUD_LOCK capability: this lock is a software lock in the cloud,
            thus you can still move the shutter through a local interface.


        Args:
            installation_id: int
            shutter_id: int

        Returns:
            Returns the lock_type as response.
        """
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/lock"
        return self.api_client.post(path)

    def unlock(
        self,
        installation_id: int,
        shutter_id: int,
    ) -> dict[str, Any]:
        """Undo the lock action of the specified Shutter.

        Args:
            installation_id: int
            shutter_id: int

        Returns:
            Returns a shutter with id
        """
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/unlock"
        return self.api_client.post(path)

    def preset(
        self,
        installation_id: int,
        shutter_id: int,
        position: int,
    ) -> dict[str, Any]:
        """Change the preset position of the specified Shutter.

        The position can be set from 0 to steps (excluded). The steps value can be
        found in the configuration field of a Shutter.
        Not all gateways or shutters support this feature.

        Args:
            installation_id: int
            shutter_id: int
            position: int (in body)

        Returns:
            Returns a shutter with id
        """
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/preset"
        payload = json.dumps(
            {
                "position": position,
            }
        )
        return self.api_client.post(path, json=payload)

    def move_to_preset(
        self,
        installation_id: int,
        shutter_id: int,
    ) -> dict[str, Any]:
        """Move the specified Shutter to its preset position (defined in POST .../preset).

        Not all gateways or shutters support this feature.

        Args:
            installation_id: int
            shutter_id: int

        Returns:
            Returns a shutter with id
        """
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/move"
        return self.api_client.post(path)
