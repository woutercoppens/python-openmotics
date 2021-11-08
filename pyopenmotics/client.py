"""Asynchronous Python client for OpenMotics API."""
from __future__ import annotations

import asyncio
import logging
import socket
import time

# from abc import ABC, abstractmethod
# from time import sleep
# from typing import Any, Awaitable, Callable, Dict, List, Optional
from typing import Any, Optional


import backoff

# import requests
# from aiohttp import ClientError, ClientResponse, ClientSession
from cached_property import cached_property
from oauthlib.oauth2 import TokenExpiredError

# from requests.models import Response
from requests_oauthlib import TokenUpdated
from yarl import URL

from .__version__ import __version__
from .base import Base
from .const import OM_API_BASE_PATH, OM_API_HOST, OM_API_PORT, OM_API_SSL
from .exceptions import (
    OpenMoticsConnectionError,
    OpenMoticsConnectionTimeoutError,
    OpenMoticsError,
    OpenMoticsRateLimitError,
)
from .ws import WebSocket

logger = logging.getLogger(__name__)


# class Api(object):
class Api:

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
        self.client = None
        self.session = None

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

    def get_token(self):
        # Subclasses should implement this!
        raise NotImplementedError()

    def token_saver(self, token, refresh_token=None, access_token=None): 
        # Subclasses should implement this!
        raise NotImplementedError()

    # pylint: disable=too-many-arguments
    @backoff.on_exception(
        backoff.expo, OpenMoticsConnectionError, max_tries=3, logger=None
    )
    @backoff.on_exception(
        backoff.expo, OpenMoticsRateLimitError, base=60, max_tries=6, logger=None
    )
    def __request(
        self,
        method: str = "GET",
        url: str = "",
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        **kwargs,
    ) -> Any:
        """Handle a request to the Quby ToonAPI."""

        self.url = str(self.join_url(self.base_url, url))

        if self.token is None:
            self.get_token()

        # headers = {
        #     "User-Agent": self.user_agent,
        #     "Accept": "application/json",
        # }

        logger.debug(
            f"Request: method = {method}, \
                url = {self.url},\
                params = {params},\
                json = {json},\
                t = {int(time.time()*1000)}"
        )

        # if self.session is None:
        #     self.session = self.get_session()
        #     self._close_session = True

        try:
            resp = self.session.request(
                method,
                url=self.url,
                # headers=headers,
                json=json,
                params=params,
                # client_id=self.client_id,
                # client_secret=self.client_secret,
                **kwargs,
            )

            # async with self.session.request(
            #     method,
            #     url=self.url,
            #     headers=headers,
            #     # data=data,
            #     json=json,
            #     params=params,
            #     client_id=self.client_id,
            #     client_secret=self.client_secret,
            #     **kwargs,
            # ) as resp:
            #     logger.debug(resp.status)
        except asyncio.TimeoutError as exception:
            raise OpenMoticsConnectionTimeoutError(
                "Timeout occurred while connecting to the api"
            ) from exception
        except (TokenUpdated, TokenExpiredError):
            # Refresh token and call again
            self.get_token()
            return self.__request(method, url, json, params, **kwargs)
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
            contents = resp.content
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

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Http Get.
        Requests the server to return specified resources.
        Args:
            path (str): api path
            params (map): request parameter
        Returns:
            response: response body
        """
        return self.__request("GET", path, params, None)

    def post(self, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Http Post.
        Requests the server to update specified resources.
        Args:
            path (str): api path
            body (map): request body
        Returns:
            response: response body
        """
        return self.__request("POST", path, None, body)

    def put(self, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Http Put.
        Requires the server to perform specified operations.
        Args:
            path (str): api path
            body (map): request body
        Returns:
            response: response body
        """
        return self.__request("PUT", path, None, body)

    def delete(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Http Delete.
        Requires the server to delete specified resources.
        Args:
            path (str): api path
            params (map): request param
        Returns:
            response: response body
        """
        return self.__request("DELETE", path, params, None)

    def root(self):
        # The current v1 implementation returns the current logged in user's information
        # and his (paid) features.
        path = "/"
        return self.get(path)
