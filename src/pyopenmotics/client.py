"""Asynchronous Python client for OpenMotics API."""
from __future__ import annotations

import logging
import time
from typing import Any

import backoff  # type: ignore
from authlib.integrations.httpx_client import OAuth2Client, OAuthError
from cached_property import cached_property
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
from .websocket import WebSocket

logger = logging.getLogger(__name__)


# class Api(object):
class Api:
    """Main class for handling connections with the OpenMotics API."""

    _close_session: bool = False

    # pylint: disable=too-many-arguments
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
        """Initialize connection with the OpenMotics API.

        Args:
            client_id: str
            client_secret: str
            server: str
            port: int
            ssl: bool
            request_timeout: int
            user_agent: str
        """
        self.token = None
        self.client = None
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
        """cached_property.

        Returns:
            installations: all functions about the base class
        """
        return Base(api_client=self)

    @cached_property
    def websocket(self):
        """cached_property.

        Returns:
            installations: all functions about websockets
        """
        return WebSocket(api_client=self)

    def join_url(self, base: URL, path: str) -> URL:
        """Join URL and path together.

        Args:
            base: URL object
            path: path

        Returns:
            URL object
        """
        if path.startswith("/"):
            # Remove trailing /
            path = path[1:]
        self.url = base / path
        return self.url

    def get_token(self):
        """Get Token.

        Subclasses should implement this!

        Raises:
            NotImplementedError: blabla
        """
        raise NotImplementedError()

    def token_saver(self, token, refresh_token=None, access_token=None):
        """Save Token.

        Subclasses should implement this!

        Args:
            token: str
            refresh_token: str
            access_token: str

        Raises:
            NotImplementedError: blabla
        """
        raise NotImplementedError()  # noqa: DAR401

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
        """Handle a request to an OpenMotics installation.

        A generic method for sending/handling HTTP requests done against
        the OpenMotics installation.

        Args:
            url: Request URI, for example `/json/si`.
            method: HTTP method to use for the request.E.g., "GET" or "POST".
            params: parameters to query
            json: Dictionary of data to send to the installation.
            **kwargs: other arguments

        Returns:
            A Python dictionary (JSON decoded) with the response from the
            OpenMotics installation.

        Raises:
            OpenMoticsAuthenticationError: blabla
            OpenMoticsError: blabla
            OpenMoticsRateLimitError: blabla
        """
        uri = self.join_url(self.base_url, url)

        if self.token is None:
            self.get_token()

        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json",
        }

        logger.debug(
            "Request: method = %s, url = %s, params = %s, json = %s, t = %s",
            method,
            str(uri),
            params,
            json,
            int(time.time() * 1000),
        )

        try:
            resp = self.session.request(
                method,
                url=str(uri),
                headers=headers,
                params=params,
                json=json,
                **kwargs,
            )

        except OAuthError as exc:
            raise OpenMoticsAuthenticationError(
                f"Error occurred while communicating with the OpenMotics " f"API: {exc}"
            ) from exc
        except Exception as exc:  # pylint: disable=broad-except
            raise OpenMoticsError(
                f"Unknown error occurred while communicating with the OpenMotics "
                f"API: {exc}"
            ) from exc

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
            path: api path
            params: request parameter

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
            path: api path
            json: request body

        Returns:
            response: response body
        """
        return self.__request("POST", path, None, json)

    def root(self):
        """Return user information.

        Returns:
            The current v1 implementation returns the current logged in user's
            information and his (paid) features.
        """
        path = "/"
        return self.get(path)
