"""Asynchronous Python client for OpenMotics."""
from __future__ import annotations

from typing import TYPE_CHECKING

from cached_property import cached_property

from .installations import Installations

if TYPE_CHECKING:
    from ..client import Api  # pylint: disable=R0401


class Base:
    """Object holding the base class.

    OpenMotics base API for controlling all base functions such as toggle outputs,
    set thermostats, ...
    """

    def __init__(self, api_client: Api):
        """Init the groupactions object.

        Args:
            api_client: Api
        """
        self.api_client = api_client

    @cached_property
    def installations(self):
        """cached_property.

        Returns:
            installations: all functions about installations
        """
        return Installations(api_client=self.api_client)
