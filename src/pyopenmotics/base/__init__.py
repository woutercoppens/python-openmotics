"""Asynchronous Python client for OpenMotics."""
from __future__ import annotations

from typing import TYPE_CHECKING

from cached_property import cached_property

from .installations import Installations

# import asyncio


if TYPE_CHECKING:
    from ..client import Api  # pylint: disable=R0401


class Base:
    """Docstring."""

    def __init__(self, api_client: Api):
        """Docstring."""

        self.api_client = api_client

    @cached_property
    def installations(self):
        """Docstring."""
        return Installations(api_client=self.api_client)
