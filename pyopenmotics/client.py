"""Asynchronous Python client for OpenMotics API."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
import asyncio
import json
import socket
import time
from time import sleep

from requests.models import Response
from cached_property import cached_property

from typing import Any, Awaitable, Callable, Dict, List, Optional
# import requests
from aiohttp import ClientError, ClientResponse, ClientSession
from requests_oauthlib import TokenUpdated
from oauthlib.oauth2 import TokenExpiredError
import async_timeout
import backoff
from yarl import URL


from .__version__ import __version__
from .const import (
    OM_API_BASE_PATH,
    OM_API_HOST,
    OM_API_PORT,
    OM_API_SSL,
)
from .exceptions import (
    OpenMoticsConnectionError,
    OpenMoticsConnectionTimeoutError,
    OpenMoticsError,
    OpenMoticsRateLimitError,
)
from .base import Base
from .ws import WebSocket

logger = logging.getLogger(__name__)


class Api(object):
    """Main class for handling connections with the OpenMotics API."""

    # installation_id: Optional[str] = None
    # _installations: Optional[List[Installation]] = None
    # _status: Optional[Status] = None
    _close_session: bool = False

    # _webhook_refresh_timer_task: Optional[asyncio.TimerHandle] = None
    # _webhook_url: Optional[str] = None

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        server: Optional[str] = OM_API_HOST,
        port: Optional[int] = OM_API_PORT,
        ssl: Optional[bool] = OM_API_SSL,
        request_timeout: Optional[int] = 8,
        user_agent: Optional[str] = None,
    ) -> None:
        self.token = None
        self.client  = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.port = port
        self.server = server

        self.request_timeout = request_timeout
        self.user_agent = user_agent

        if user_agent is None:
            self.user_agent = f"PythonOpenMoticsAPI/{__version__}"

        if ssl is False:
            self.scheme = "http"
        else:
            self.scheme = "https"

        self.base_url = URL.build(
            scheme=self.scheme,
            host=server,
            port=port,
            path=OM_API_BASE_PATH,
        )
        self.token_url = self.join_url(self.base_url, "authentication/oauth2/token")

    @cached_property
    def base(self):
        return Base(api_client=self)

    @cached_property
    def ws(self):
        return WebSocket(api_client=self)

    async def get_token(self):
        token_url = str(self.token_url)
        self.token = self.client.fetch_token(
            token_url=self.token_url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            )


    def token_saver(self, token):
        self.token = token

    def join_url(
        self,
        base: URL = None,
        path: str = None,
    ) -> URL:
        if path.startswith("/"):
            # Remove trailing /
            path = path[1:]
        self.url = base / path
        return self.url

    # pylint: disable=too-many-arguments
    @backoff.on_exception(
        backoff.expo, OpenMoticsConnectionError, max_tries=3, logger=None
    )
    @backoff.on_exception(
        backoff.expo, OpenMoticsRateLimitError, base=60, max_tries=6, logger=None
    )
    async def __request(
        self,
        method: str = "GET",
        url: str = "",
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        **kwargs,
    ) -> dict[str, Any]:
        """Handle a request to the Quby ToonAPI."""

        self.url = str(self.join_url(self.base_url, url))

        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json",
        }

        logger.debug(
            f"Request: method = {method}, \
                url = {self.url},\
                params = {params},\
                json = {json},\
                t = {int(time.time()*1000)}"
        )

        try:
            with async_timeout.timeout(self.request_timeout):
                resp = self.client.request(
                    method,
                    url=self.url,
                    headers=headers,
                    json=json,
                    params=params,
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    **kwargs,
                )
            
                # async with self.client.request(
                #     method,
                #     url=self.url,
                #     headers=headers,
                #     # data=data,
                #     json=json,
                #     params=params,
                #     client_id=self.client_id,
                #     client_secret=self.client_secret,
                #     **kwargs,
                # ) as r:
                #     resp = await r 
        except asyncio.TimeoutError as exception:
            raise OpenMoticsConnectionTimeoutError(
                f"Timeout occurred while connecting to the api"
            ) from exception
        except (TokenUpdated, TokenExpiredError):
            # Refresh token and call again
            await self.get_token()
            return await self.__request(method, url, json, params, **kwargs) 
        except (
            # aiohttp.ClientError,
            # aiohttp.ClientResponseError,
            socket.gaierror,
        ) as exception:
            raise OpenMoticsError(
                "Error occurred while communicating with the OpenMotics API"
            ) from exception

        content_type = resp.headers.get("Content-Type", "")

        # Error handling
        if (resp.status_code // 100) in [4, 5]:
            contents = await resp.content
            print(contents)
            resp.close()

            if resp.status_code == 429:
                raise OpenMoticsRateLimitError(
                    "Rate limit error has occurred with the OpenMotics API"
                )

            if content_type == "application/json":
                raise OpenMoticsError(
                    resp.status_code, json.loads(contents.decode("utf8"))
                )
            raise OpenMoticsError(
                resp.status_code, {"message": contents.decode("utf8")}
            )

        # Handle empty response
        if resp.status_code == 204:
            return

        if "application/json" in content_type:
            response_data = resp.json().get("data")
            return response_data

        return resp.text()

    async def get(
        self, path: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Http Get.
        Requests the server to return specified resources.
        Args:
            path (str): api path
            params (map): request parameter
        Returns:
            response: response body
        """
        return await self.__request("GET", path, params, None)

    async def post(
        self, path: str, body: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Http Post.
        Requests the server to update specified resources.
        Args:
            path (str): api path
            body (map): request body
        Returns:
            response: response body
        """
        return await self.__request("POST", path, None, body)

    async def put(
        self, path: str, body: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Http Put.
        Requires the server to perform specified operations.
        Args:
            path (str): api path
            body (map): request body
        Returns:
            response: response body
        """
        return await self.__request("PUT", path, None, body)

    async def delete(
        self, path: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Http Delete.
        Requires the server to delete specified resources.
        Args:
            path (str): api path
            params (map): request param
        Returns:
            response: response body
        """
        return await self.__request("DELETE", path, params, None)
   
    async def root(self):
        # The current v1 implementation returns the current logged in user's information and his (paid) features.
        path = f"/"
        return await self.get(path)

    async def closed(self) -> bool:
        return self.client.closed()

    async def close(self) -> None:
        """Close open client session."""
        # if self.client is not None and self._close_session:
        #     await self.client.close()
        # if self.ws:
        #     self.ws.close()
        # if self.client:
        #     self.client.delete(
        #         f'{self.AUTHENTICATION_HOST}/v1/token/{self.token["refresh_token"]}',
        #         headers={"X-Api-Key": self.client_id},
        #     )
        #     self.client.delete(
        #         f'{self.AUTHENTICATION_HOST}/v1/token/{self.token["access_token"]}',
        #         headers={"X-Api-Key": self.client_id},
        #     )
        pass

    async def __aenter__(self) -> Api:
        """Async enter.
        Returns:
            The Api object.
        """
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit.
        Args:
            _exc_info: Exec type.
        """
        print("Disconnecting nicely....")
        await self.close()
