from __future__ import annotations
from cached_property import cached_property
# import asyncio

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import Api  # pylint: disable=R0401

from .installations import Installations


class Base:
    def __init__(self, api_client: Api = None):
        # if api_client is None:
        #     api_client = Api()
        self.api_client = api_client

    @cached_property
    def installations(self):
        return Installations(api_client=self.api_client)
