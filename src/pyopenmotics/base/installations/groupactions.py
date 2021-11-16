"""Asynchronous Python client for OpenMotics."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401


class Groupactions:
    """Object holding functions about Groupactions (scenes).

    A GroupAction can be considered a list of actions that will be executed
    sequentially.
    They can contain limited logic such as if-statements.
    They do not hold state so it"s a fire-and-forget approach.
    """

    def __init__(self, api_client: Api):
        """Init the groupactions object.

        Args:
            api_client: Api
        """
        self.api_client = api_client

    def all(  # noqa: A003
        self,
        installation_id: int,
        groupactions_filter: str | None = None,
    ) -> dict[str, Any]:
        """Call lists all GroupAction objects.

        Args:
            installation_id: int
            groupactions_filter: Optional filter

        Returns:
            Dict with all groupactions

        usage: The usage filter allows the GroupActions to be filtered for
            their intended usage.
            SCENE: These GroupActions can be considered a scene,
                e.g. watching tv or romantic dinner.
        # noqa: E800
        # [{
        #      "_version": <version>,
        #      "actions": [
        #          <action type>, <action number>,
        #          <action type>, <action number>,
        #          ...
        #      ],
        #  "id": <id>,
        #  "location": {
        #      "installation_id": <installation id>
        #  },
        #  "name": "<name>"
        #  }
        """
        path = f"/base/installations/{installation_id}/groupactions"
        if groupactions_filter:
            query_params = {"filter": groupactions_filter}
            return self.api_client.get(path, params=query_params)

        return self.api_client.get(path)

    def by_id(
        self,
        installation_id: int,
        groupaction_id: int,
    ) -> dict[str, Any]:
        """Get a specified groupaction object.

        Args:
            installation_id: int
            groupaction_id: int

        Returns:
            Returns a groupaction with id
        """
        path = f"/base/installations/{installation_id}/groupactions/{groupaction_id}"
        return self.api_client.get(path)

    def trigger(
        self,
        installation_id: int,
        groupaction_id: int,
    ) -> dict[str, Any]:
        """Trigger a specified groupaction object.

        Args:
            installation_id: int
            groupaction_id: int

        Returns:
            Returns a groupaction with id
        """
        # E501 line too long
        path = (
            f"/base/installations/{installation_id}"
            f"/groupactions/{groupaction_id}/trigger"
        )
        return self.api_client.post(path)

    def by_usage(
        self,
        installation_id: int,
        groupaction_usage: str,
    ) -> dict[str, Any]:
        """Return a specified groupaction object.

        The usage filter allows the GroupActions to be filtered for their
        intended usage.

        Args:
            installation_id: int
            groupaction_usage: str

        Returns:
            Returns a groupaction with id
        """
        path = f"/base/installations/{installation_id}/groupactions"
        query_params = {"usage": groupaction_usage.upper()}
        return self.api_client.get(path, params=query_params)

    def scenes(self, installation_id: int) -> dict[str, Any]:
        """Return all scenes object.

        SCENE: These GroupActions can be considered a scene,
            e.g. watching tv or romantic dinner.

        Args:
            installation_id: int

        Returns:
            Returns all scenes
        """
        return self.by_usage(installation_id, "SCENE")
