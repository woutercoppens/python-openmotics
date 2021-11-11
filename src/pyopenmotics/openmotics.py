"""Asynchronous Python client for OpenMotics API."""
from __future__ import annotations

# import asyncio
import logging

from authlib.integrations.httpx_client import OAuth2Client

# from authlib.integrations.requests_client import OAuth2Session
from oauthlib.oauth2 import (
    BackendApplicationClient,
    LegacyApplicationClient,
    ServiceApplicationClient,
)

from .client import Api

logger = logging.getLogger(__name__)


# authlib.integrations.httpx_client import OAuth2Client
class BackendClient(Api):
    """Docstring."""

    def __init__(self, client_id, client_secret, **kwargs):
        """Docstring."""
        super().__init__(client_id, client_secret, **kwargs)

        self.scope = "control view"
        self.client = BackendApplicationClient(client_id=self.client_id)
        self.session = OAuth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            token_endpoint_auth_method="client_secret_post",
            scope=self.scope,
            token_endpoint=str(self.token_url),
            grant_type="client_credentials",
            update_token=self.token_saver,
        )

    def token_saver(self, token, refresh_token=None, access_token=None):
        """Docstring."""
        self.token = token
        # self.get_token()

    def get_token(self):
        """Docstring."""
        self.token = self.session.fetch_token(
            url=str(self.token_url),
            grant_type="client_credentials",
        )


# authlib.integrations.requests_client
# class BackendClient(Api):
#     """Docstring."""

#     def __init__(self, client_id, client_secret, **kwargs):
#         """Doc String."""
#         super().__init__(client_id, client_secret, **kwargs)
#         # def __init__(self, *args, **kwargs):
#         #     # POP CLIENT_ID BEFORE calling super BackendClient
#         #     client_id = kwargs.pop("client_id", None)
#         #     client_secret = kwargs.pop("client_secret", None)
#         #     # call super
#         #     super(BackendClient, self).__init__(*args, **kwargs)

#         self.scope = "control view"
#         self.client = BackendApplicationClient(client_id=self.client_id)
#         self.session = OAuth2Session(
#             client_id=self.client_id,
#             client_secret=self.client_secret,
#             token_endpoint_auth_method="client_secret_post",
#             scope=self.scope,
#             token_endpoint=str(self.token_url),
#             grant_type="client_credentials",
#             # token={"access_token": None, "expires_in": -100},
#             update_token=self.token_saver,
#         )

#     def token_saver(self, token, refresh_token=None, access_token=None):
#         """Docstring."""
#         self.token = token
#         # self.get_token()

#     def get_token(self):
#         """Docstring."""
#         self.token = self.session.fetch_token(
#             url=str(self.token_url),
#             grant_type="client_credentials",
#         )


# class BackendClient(Api):
#     def __init__(self, client_id, client_secret, **kwargs):
#         super(BackendClient, self).__init__(client_id, client_secret, **kwargs)

#         self.scope = 'control view'
#         extra = {'client_id': self.client_id,
#                  'client_secret': self.client_secret}
#         client = BackendApplicationClient(client_id=self.client_id)
#         self.session = OAuth2Session(client=client,
#                                     token_updater=self.token_saver,
#                                     auto_refresh_url=str(self.token_url),
#                                     auto_refresh_kwargs=extra,
#                                     )

#     def token_saver(self, token):
#         self.token = token


class ServiceClient(Api):
    """Docstring."""

    # NOT TESTED
    def __init__(self, registration_key, private_key, **kwargs):
        """Doc String."""
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
        """Docstring."""
        token_data = self.client.fetch_token(
            token_url=str(self.token_url),
            extra_claims={"registration_key": self.registration_key},
            scope=self.scope,
        )
        # {'token_type': 'Bearer',
        #     'access_token': 'eyJhbGc...xYtE',
        #     'expires_in': 3600,
        #     'expires_at': 1617290467.734431}
        self.token = token_data["access_token"]

    def token_saver(self, token, refresh_token=None, access_token=None):
        """Docstring."""
        # token_var = self.get_token()
        self.token = token


class LegacyApplicationClient(Api):
    """Doc String."""

    # NOT TESTED
    # def __init__(self, username, password, client_id, client_secret, **kwargs):
    def __init__(self, client_id, client_secret, **kwargs):
        """Docstring."""
        super().__init__(client_id, client_secret, **kwargs)

        self.scope = "control view"
        self.client = LegacyApplicationClient(client_id=self.client_id, client_secret=self.client_secret)
        self.session = OAuth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            token_endpoint_auth_method="client_secret_post",
            scope=self.scope,
            token_endpoint=str(self.token_url),
            grant_type="client_credentials",
            update_token=self.token_saver,
        )

    def token_saver(self, token, refresh_token=None, access_token=None):
        """Docstring."""
        self.token = token
        # self.get_token()

    def get_token(self):
        """Docstring."""
        self.token = self.session.fetch_token(
            url=str(self.token_url),
            grant_type="client_credentials",
        )

