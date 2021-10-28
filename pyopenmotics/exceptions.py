"""Exceptions for the OpenMotics API."""
from requests import Response


class OpenMoticsError(Exception):
    """Generic OpenMotics API exception."""

    def __init__(self, response: Response):
        try:
            # assume Response json
            response_json = response.json()
            super().__init__(response_json)
            self.status_code = response_json["status_code"]
            self.error = response_json["error"]
            self.message = response_json["message"]
        except (Exception,):
            super().__init__(response)
            self.status_code = response.status_code
            self.error = None
            self.message = None


class OpenMoticsConnectionError(OpenMoticsError):
    """OpenMotics API connection exception."""


class OpenMoticsConnectionTimeoutError(OpenMoticsConnectionError):
    """OpenMotics API connection timeout exception."""


class OpenMoticsRateLimitError(OpenMoticsConnectionError):
    """OpenMotics API Rate Limit exception."""
