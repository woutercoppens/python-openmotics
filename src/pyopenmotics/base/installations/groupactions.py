"""Asynchronous Python client for OpenMotics."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

# import asyncio

# import json

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401


class Groupactions:
    """Doc String."""

    def __init__(self, api_client: Api):
        """Doc String."""
        self.api_client = api_client

    def all(
        self,
        installation_id: str,
        groupactions_filter: str | None = None,
    ) -> dict[str, Any]:
        """Doc String."""

        # [{
        #     "_version": <version>,
        #     "actions": [
        #         <action type>, <action number>,
        #         <action type>, <action number>,
        #         ...
        #     ],
        # "id": <id>,
        # "location": {
        #     "installation_id": <installation id>
        # },
        # "name": "<name>"
        # }

        path = f"/base/installations/{installation_id}/groupactions"
        if groupactions_filter:
            query_params = {"filter": groupactions_filter}
            return self.api_client.get(path, params=query_params)

        return self.api_client.get(path)

    def by_id(
        self,
        installation_id: str,
        groupaction_id: str,
    ) -> dict[str, Any]:
        """Doc String."""
        path = f"/base/installations/{installation_id}/groupactions/{groupaction_id}"
        return self.api_client.get(path)

    def trigger(
        self,
        installation_id: str,
        groupaction_id: str,
    ) -> dict[str, Any]:
        """Doc String."""
        # E501 line too long
        path = (
            f"/base/installations/{installation_id}"
            f"/groupactions/{groupaction_id}/trigger"
        )
        return self.api_client.post(path)

    def by_usage(
        self,
        installation_id: str,
        groupaction_usage: str,
    ) -> dict[str, Any]:
        """Doc String."""
        path = f"/base/installations/{installation_id}/groupactions"
        query_params = {"usage": groupaction_usage.upper()}
        return self.api_client.get(path, params=query_params)

    def scenes(self, installation_id) -> dict[str, Any]:
        """Doc String."""
        return self.by_usage(installation_id, "SCENE")
