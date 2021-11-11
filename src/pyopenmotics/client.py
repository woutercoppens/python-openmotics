"""Asynchronous Python client for OpenMotics API."""
from __future__ import annotations

import json

# import asyncio
import logging
import socket
import time

# from abc import ABC, abstractmethod
# from time import sleep
# from typing import Any, Awaitable, Callable, Dict, List, Optional
from typing import Any

import backoff  # type: ignore

# import requests
# from aiohttp import ClientError, ClientResponse, ClientSession
# from authlib.integrations.requests_client import OAuth2Session
from authlib.integrations.httpx_client import OAuth2Client, OAuthError
from cached_property import cached_property
# from oauthlib.oauth2 import TokenExpiredError

# from requests.models import Response
# from requests_oauthlib import TokenUpdated
from yarl import URL

from .__version__ import __version__
from .base import Base
from .const import OM_API_BASE_PATH, OM_API_HOST, OM_API_PORT, OM_API_SSL
from .exceptions import (  # OpenMoticsConnectionTimeoutError,
    OpenMoticsAuthenticationError,
    OpenMoticsConnectionError,
    OpenMoticsError,
    OpenMoticsRateLimitError,
)
from .ws import WebSocket

logger = logging.getLogger(__name__)


# class Api(object):
class Api:
    """Main class for handling connections with the OpenMotics API."""

    _close_session: bool = False

    def __init__(
        self,
        client_id: str = None,
        client_secret: str = None,
        server: str = OM_API_HOST,
        port: int = OM_API_PORT,
        ssl: bool | None = OM_API_SSL,
        request_timeout: int | None = 8,
        user_agent: str | None = None,
    ) -> None:
        """Initialize connection with the OpenMotics API."""
        self.token = None
        self.client = None
        # self.session: OAuth2Session = None
        self.session: OAuth2Client = None

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
        """Object holding the base class."""
        return Base(api_client=self)

    @cached_property
    def ws(self):
        """Object holding the base class."""
        return WebSocket(api_client=self)

    def join_url(self, base: URL, path: str) -> URL:
        """Docstring."""
        if path.startswith("/"):
            # Remove trailing /
            path = path[1:]
        self.url = base / path
        return self.url

    def get_token(self):
        """Get Token."""

        # Subclasses should implement this!
        raise NotImplementedError()

    def token_saver(self, token, refresh_token=None, access_token=None):
        """Save Token."""

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
        params: Any | None = None,
        json: Any | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        """Handle a request to the OpenMotics API."""
        self.url = self.join_url(self.base_url, url)

        if self.token is None:
            self.get_token()

        # headers = {
        #     "User-Agent": self.user_agent,
        #     "Accept": "application/json",
        # }

        logger.debug(
            "Request: method = %s, url = %s, params = %s, json = %s, t = %s",
            method,
            str(self.url),
            params,
            json,
            int(time.time() * 1000),
        )

        try:
            resp = self.session.request(
                method,
                url=str(self.url),
                # headers=headers,
                params=params,
                json=json,
                **kwargs,
            )

        # except asyncio.TimeoutError as exception:
        #     raise OpenMoticsConnectionTimeoutError(
        #         "Timeout occurred while connecting to the api"
        #     ) from exception
        # except (TokenUpdated, TokenExpiredError):
        #     # Refresh token and call again
        #     self.get_token()
        #     return self.__request(method, url, params, json, **kwargs)
        except (
            # aiohttp.ClientError,
            # aiohttp.ClientResponseError,
            OAuthError,
            socket.gaierror,
        ) as exception:
            raise OpenMoticsError(
                "Error occurred while communicating with the OpenMotics API"
            ) from exception

        if resp.status_code in {401, 403}:
            raise OpenMoticsAuthenticationError(
                "The provided OpenMotics API key is not valid"
            )

        content_type = resp.headers.get("Content-Type", "")
        # Error handling
        if (resp.status_code // 100) in [4, 5]:
            contents = resp.content
            resp.close()

            if resp.status_code == 429:
                logger.error("Rate limit error has occurred with the OpenMotics API")
                raise OpenMoticsRateLimitError()

            if content_type == "application/json":
                raise OpenMoticsError(
                    resp.status_code, json.loads(contents.decode("utf8"))
                )
            raise OpenMoticsError(
                resp.status_code, {"message": contents.decode("utf8")}
            )

        # Handle empty response
        if resp.status_code == 204:
            return {"": ""}

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

    def post(
        self, path: str, json: str | dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Http Post.

        Requests the server to update specified resources.
        Args:
            path (str): api path
            data (map): request body
        Returns:
            response: response body
        """
        return self.__request("POST", path, None, json)

    # def put(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
    #     """Http Put.

    #     Requires the server to perform specified operations.
    #     Args:
    #         path (str): api path
    #         data (map): request body
    #     Returns:
    #         response: response body
    #     """
    #     return self.__request("PUT", path, None, json)

    # def delete(self, path: str, params: dict[str, Any] | None = None)
    # -> dict[str, Any]:
    #     """Http Delete.

    #     Requires the server to delete specified resources.
    #     Args:
    #         path (str): api path
    #         params (map): request param
    #     Returns:
    #         response: response body
    #     """
    #     return self.__request("DELETE", path, params, None)

    def root(self):
        """Return user information."""

        # The current v1 implementation returns the current logged in user's information
        # and his (paid) features.
        path = "/"
        return self.get(path)
