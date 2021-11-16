"""Asynchronous Python client for OpenMotics API."""

from __future__ import annotations

from typing import TYPE_CHECKING

# import websocket
# import async_timeout
# from yarl import URL

# from .const import OM_API_BASE_PATH, OM_API_HOST

# from cached_property import cached_property
# import socket
# from typing import Any, Callable
# from typing import Callable

# import aiohttp


# from .exceptions import (
#     OpenMoticsConnectionError,
#     OpenMoticsConnectionTimeoutError,
#     OpenMoticsError,
#     OpenMoticsRateLimitError,
# )

if TYPE_CHECKING:
    from .client import Api  # pylint: disable=R0401


class WebSocket:
    """Docstring."""

    def __init__(self, api_client: Api):
        """Docstring."""
        self.api_client = api_client

        self.ws = None  # websocket client:
        # # Websocket path is different for cloud and local connections:
        # if api_client.base_url.host == OM_API_HOST:
        #     self.path = f"{OM_API_BASE_PATH}/ws"
        # else:
        #     self.path = "/ws"

        # self.path = f"{OM_API_BASE_PATH}/ws"

        # self.endpoint = URL.build(
        #     scheme="ws",
        #     host=api_client.base_url.host,
        #     port=api_client.base_url.port,
        #     path=self.path,
        # )

        # print(self.endpoint)

    # async def events(
    #     self,
    # ):
    #     path = "/ws/events"
    #     return self.api_client.get(path)

    # @property
    # def connected(self) -> bool:
    #     """Return if we are connect to the WebSocket of OpenMotics.
    #     Returns:
    #         True if we are connected to the WebSocket of OpenMotics,
    #         False otherwise.
    #     """
    #     return self.ws is not None and not self.ws.closed

    # async def connect(self) -> None:
    #     """Connect to the WebSocket of a OpenMotics.
    #     Raises:
    #         OpenMoticsError: The configured OpenMotics does not support WebSocket
    #             communications.
    #         OpenMoticsConnectionError: Error occurred while communicating with
    #             OpenMotics via the WebSocket.
    #     """
    #     if self.connected:
    #         return

    #     try:
    #         self.ws = await self.api_client.client.ws_connect(
    #             url=self.endpoint,
    #             heartbeat=30,
    #         )
    #     except (
    #         aiohttp.WSServerHandshakeError,
    #         aiohttp.ClientConnectionError,
    #         socket.gaierror,
    #     ) as exception:
    #         raise OpenMoticsConnectionError(
    #             "Error occurred while communicating with openmotics"
    #             f" on WebSocket at {self.server}"
    #         ) from exception

    # async def listen(self, callback: Callable[[Device], None]) -> None:
    #     """Listen for events on the WLED WebSocket.
    #     Args:
    #         callback: Method to call when a state update is received from
    #             the WLED device.
    #     Raises:
    #         WLEDError: Not connected to a WebSocket.
    #         WLEDConnectionError: An connection error occurred while connected
    #             to the WLED device.
    #         WLEDConnectionClosed: The WebSocket connection to the remote WLED
    #             has been closed.
    #     """
    #     if not self.ws or not self.connected or not self._device:
    #         raise OpenMoticsError("Not connected to a WLED WebSocket")

    #     while not self.ws.closed:
    #         message = await self.ws.receive()

    #         if message.type == aiohttp.WSMsgType.ERROR:
    #             raise OpenMoticsConnectionError(self.ws.exception())

    #         if message.type == aiohttp.WSMsgType.TEXT:
    #             message_data = message.json()
    #             device = self.ws.update_from_dict(data=message_data)
    #             callback(device)

    #         if message.type in (
    #             aiohttp.WSMsgType.CLOSE,
    #             aiohttp.WSMsgType.CLOSED,
    #             aiohttp.WSMsgType.CLOSING,
    #         ):
    #             raise OpenMoticsConnectionError(
    #                 f"Connection to the WLED WebSocket on {self.host} has been closed"
    #             )

    # async def disconnect(self) -> None:
    #     """Disconnect from the WebSocket of a WLED device."""
    #     if not self.ws or not self.connected:
    #         return
