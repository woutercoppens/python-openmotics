"""Exceptions for the OpenMotics API."""


class OpenMoticsError(Exception):
    """Generic OpenMotics API exception."""


class OpenMoticsConnectionError(OpenMoticsError):
    """OpenMotics API connection exception."""


class OpenMoticsConnectionTimeoutError(OpenMoticsConnectionError):
    """OpenMotics API connection timeout exception."""


class OpenMoticsRateLimitError(OpenMoticsConnectionError):
    """OpenMotics API Rate Limit exception."""


class OpenMoticsAuthenticationError(OpenMoticsConnectionError):
    """OpenMotics API Authentication exception."""
