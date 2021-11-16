"""Asynchronous Python client for OpenMotics.

An Output is connected to an appliance (e.g. a light, valve, socket, ...)
and can be used to control that appliance.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401


class Inputs:
    """A Input object represents a input device."""

    def __init__(self, api_client: Api):
        """Init the input object.

        Args:
            api_client: Api
        """
        self.api_client = api_client

    def all(  # noqa: A003
        self,
        installation_id: int,
    ) -> dict[str, Any]:
        """Get a list of all input objects.

        Args:
            installation_id: int

        Returns:
            Dict with all inputs
        """
        path = f"/base/installations/{installation_id}/inputs"
        return self.api_client.get(path)

    def by_id(
        self,
        installation_id: int,
        input_id: int,
    ) -> dict[str, Any]:
        """Get input by id.

        Args:
            installation_id: int
            input_id: int

        Returns:
            Returns a input with id
        """
        path = f"/base/installations/{installation_id}/inputs/{input_id}"
        return self.api_client.get(path)
