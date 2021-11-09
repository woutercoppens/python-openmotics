"""Asynchronous Python client for OpenMotics."""
from __future__ import annotations

# from typing import TYPE_CHECKING, Any, Optional
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401


class Inputs:
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
        installation_id: str = None,
    ) -> dict[str, Any]:
        """Doc String."""
        path = f"/base/installations/{installation_id}/inputs"
        return self.api_client.get(path)

    def by_id(
        self,
        installation_id: str = None,
        input_id: str = None,
    ) -> dict[str, Any]:
        """Doc String."""
        path = f"/base/installations/{installation_id}/inputs/{input_id}"
        return self.api_client.get(path)
