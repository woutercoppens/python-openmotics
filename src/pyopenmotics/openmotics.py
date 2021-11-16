"""Asynchronous Python client for OpenMotics API."""
from __future__ import annotations

import logging

from authlib.integrations.httpx_client import OAuth2Client, OAuthError
from oauthlib.oauth2 import (
    BackendApplicationClient,
    LegacyApplicationClient,
    ServiceApplicationClient,
)

from .client import Api
from .exceptions import OpenMoticsAuthenticationError, OpenMoticsError

logger = logging.getLogger(__name__)


# authlib.integrations.httpx_client import OAuth2Client
class BackendClient(Api):
    """Docstring."""

    def __init__(self, client_id, client_secret, **kwargs):
        """Init the BackendClient object.

        Args:
            client_id: str
            client_secret: str
            **kwargs: other arguments
        """
        super().__init__(client_id, client_secret, **kwargs)

        self.scope = "control view"
        self.client = BackendApplicationClient(client_id=self.client_id)
        self.session = OAuth2Client(  # noqa: S106
            client_id=self.client_id,
            client_secret=self.client_secret,
            token_endpoint_auth_method="client_secret_post",  # nosec
            scope=self.scope,
            token_endpoint=str(self.token_url),
            grant_type="client_credentials",
            update_token=self.token_saver,
        )

    def token_saver(self, token, refresh_token=None, access_token=None):
        """Save the token to self.token.

        Args:
            token: str
            refresh_token: str
            access_token: str
        """
        self.token = token

    def get_token(self):
        """Get a new token.

        Raises:
            OpenMoticsAuthenticationError: blabla
            OpenMoticsError: blabla
        """
        try:
            self.token = self.session.fetch_token(
                url=str(self.token_url),
                grant_type="client_credentials",
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

        return


class ServiceClient(Api):
    """Docstring."""

    # NOT TESTED
    def __init__(self, registration_key, private_key, **kwargs):
        """Init the ServiceClient object.

        Args:
            registration_key: str
            private_key: str
            **kwargs: other arguments
        """
        super().__init__(None, None, **kwargs)

        self.scope = "control view"
        extra = {}
        self.registration_key = registration_key
        client = ServiceApplicationClient(
            None,
            private_key,
            issuer="OM",
            subject="gateway",
            audience=self.url,
            scope=self.scope,
        )
        self.client = OAuth2Client(
            client=client,
            token_updater=self.token_saver,
            auto_refresh_url=str(self.token_url),
            auto_refresh_kwargs=extra,
        )
        self.client.headers.update({"X-Bearer-Token-Type": "JWT"})

    def get_token(self):
        """Get a new token."""
        token_data = self.client.fetch_token(
            token_url=str(self.token_url),
            extra_claims={"registration_key": self.registration_key},
            scope=self.scope,
        )
        self.token = token_data["access_token"]

    def token_saver(self, token, refresh_token=None, access_token=None):
        """Save the token to self.token.

        Args:
            token: str
            refresh_token: str
            access_token: str
        """
        self.token = token


class LegacyClient(Api):
    """Doc String."""

    # NOT TESTED
    # def __init__(self, username, password, client_id, client_secret, **kwargs):
    def __init__(self, client_id, client_secret, **kwargs):
        """Init the LegacyClient object.

        Args:
            client_id: str
            client_secret: str
            **kwargs: other arguments
        """
        super().__init__(client_id, client_secret, **kwargs)

        self.scope = "control view"
        self.client = LegacyApplicationClient(
            client_id=self.client_id, client_secret=self.client_secret
        )
        self.session = OAuth2Client(  # noqa: S106
            client_id=self.client_id,
            client_secret=self.client_secret,
            token_endpoint_auth_method="client_secret_post",  # nosec
            scope=self.scope,
            token_endpoint=str(self.token_url),
            grant_type="client_credentials",
            update_token=self.token_saver,
        )

    def token_saver(self, token, refresh_token=None, access_token=None):
        """Save the token to self.token.

        Args:
            token: str
            refresh_token: str
            access_token: str
        """
        self.token = token

    def get_token(self):
        """Get a new token."""
        self.token = self.session.fetch_token(
            url=str(self.token_url),
            grant_type="client_credentials",
        )
