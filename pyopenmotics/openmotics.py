"""Asynchronous Python client for OpenMotics API."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
import asyncio
import json
import socket
import jwt
from time import sleep
from typing import Any, Awaitable, Callable, Dict, List, Optional

import aiohttp
import async_timeout
import backoff
from yarl import URL

import requests
from aiohttp import ClientError, ClientResponse, ClientSession

from oauthlib.oauth2 import (
    BackendApplicationClient,
    LegacyApplicationClient,
    ServiceApplicationClient,
)
from requests_oauthlib import OAuth2Session

# from async_oauthlib import OAuth2Session
# from authlib.integrations.requests_client import OAuth2Session

from .client import Api

# from .__version__ import __version__
logger = logging.getLogger(__name__)


# class BackendClient(Api):
#     def __init__(self, client_id, client_secret, **kwargs):
#         super(BackendClient, self).__init__(client_id, client_secret, **kwargs)

#         self.scope = "control view"
#         extra = {"client_id": self.client_id, "client_secret": self.client_secret}
#         client = BackendApplicationClient(client_id=self.client_id)
#         if self.client is None:
#             self.client  = OAuth2Session(
#                 client=client,
#                 token_updater=self.token_saver,
#                 auto_refresh_url=self.token_url,
#                 auto_refresh_kwargs=extra,
#             )
#             self._close_session = True

class BackendClient(Api):
    def __init__(self, client_id, client_secret, **kwargs):
        super(BackendClient, self).__init__(client_id, client_secret, **kwargs)

        self.scope = "control view"
        extra = {"client_id": self.client_id, "client_secret": self.client_secret}
        client = BackendApplicationClient(client_id=self.client_id)
        if self.client is None:
            self.client  = OAuth2Session(
                client=client,
                token_updater=self.token_saver,
                auto_refresh_url=self.token_url,
                auto_refresh_kwargs=extra,
            )
            self._close_session = True

class ServiceClient(Api):
    def __init__(self, registration_key, private_key, **kwargs):
        super(ServiceClient, self).__init__(None, None, **kwargs)

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
        self.client  = OAuth2Session(
            client=client,
            token_updater=self.token_saver,
            auto_refresh_url=self.token_url,
            auto_refresh_kwargs=extra,
        )
        self.client.headers.update({"X-Bearer-Token-Type": "JWT"})

    def get_token(self):
        token_data = self.client.fetch_token(
            token_url=self.token_url,
            extra_claims={"registration_key": self.registration_key},
            scope=self.scope,
        )
        """{'token_type': 'Bearer',
            'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNsb3VkIn0.eyJpc3MiOiJodHRwczovL3N0YWdpbmcub3B
            lbm1vdGljcy5jb20iLCJzdWIiOiJnYXRld2F5IiwiZXhwIjoxNjE3MjkwNDY3LCJzY29wZSI6bnVsbCwiZ2F0ZXdheV9pZCI6MTl9.reTXkM
            qCKwS8UOj-WnEf_tdDaIEGFN1Z5lr0yOkxYtE',
            'expires_in': 3600,
            'expires_at': 1617290467.734431}
        """
        self.token = token_data["access_token"]


class LegacyClient(Api):
    def __init__(self, username, password, client_id, client_secret, **kwargs):
        super(LegacyClient, self).__init__(client_id, client_secret, **kwargs)
        self.scope = "control view"
        extra = {"client_id": self.client_id, "client_secret": self.client_secret}
        client = LegacyApplicationClient(client_id=self.client_id)
        self.client  = OAuth2Session(
            client=client,
            token_updater=self.token_saver,
            auto_refresh_url=self.token_url,
            auto_refresh_kwargs=extra,
        )
