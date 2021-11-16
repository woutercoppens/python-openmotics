"""Asynchronous Python client for OpenMotics."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ...client import Api  # pylint: disable=R0401


class Sensors:
    """A Sensor object represents a sensor device.

    It might yield multiple values depending on installed components.
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
        sensors_filter: str | None = None,
    ) -> dict[str, Any]:
        """Get a list of all Sensor objects.

        Args:
            installation_id: int
            sensors_filter: Optional filter

        Returns:
            Dict with all sensors

        Optional filter:
            location: Only returns Sensors at this location
                room_id: Only returns Sensors in this room
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
        path = f"/base/installations/{installation_id}/sensors"
        if sensors_filter:
            query_params = {"filter": sensors_filter}
            return self.api_client.get(path, params=query_params)

        return self.api_client.get(path)

    def by_id(
        self,
        installation_id: int,
        sensor_id: int,
    ) -> dict[str, Any]:
        """Get sensor by id.

        Args:
            installation_id: int
            sensor_id: int

        Returns:
            Returns a sensor with id
        """
        path = f"/base/installations/{installation_id}/sensors/{sensor_id}"
        return self.api_client.get(path)

    def historical(
        self,
        installation_id: int,
        sensor_id: int | None = None,
        start: str | None = None,
        end: str | None = None,
        resolution: str | None = "5m",
        group_function: str | None = "last",
        use_active_hours: bool | None = False,
        time_format: str | None = "iso",
    ) -> dict[str, Any]:
        """Get historical data of a sensor.

        Args:
            installation_id: int
            sensor_id: int
            start:  1620804462
                start point to query from in unix timestamp
            end: 1623400787
                end point to query from in unix timestamp
            resolution: M
                resolution of the data: {1m, 5m, 15m, h, D, M}: aggregate
                the data to a certain resolution, default is 5m
            group_function: mean
                the group function: {last, mean, max, min} : What to do
                when changing the resolution of the data. default is last.
            use_active_hours: True
                {True, False}: boolean to indicate if active hours time
                overlay needs to be used for this installation. Default is False
            time_format: iso
                {unix, iso}: format to use for timestamps in the response

        Returns:
            Dict

        # noqa: E800
        # {
        #   "data": {
        #     "time": "1970-01-01T00:10:00",
        #     "tags": {
        #         "sensor_id": "6",
        #         "sensor_name": "Sensor 0",
        #         "gateway_id": 1
        #     },
        # "values": {
        #   "temperature": 22.1
        #     }
        # },
        # "_acl": null,
        # "_error": null
        # }
        """

        # E501 line too long
        path = (
            f"/base/installations/{installation_id}/sensors/{sensor_id}"
            f"/historical?start={start}&end={end}&resolution={resolution}"
            f"&group_function={group_function}&use_active_hours={use_active_hours}"
            f"&time_format={time_format}"
        )
        return self.api_client.get(path)
