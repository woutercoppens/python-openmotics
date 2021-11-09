""""Expose submodules."""
import logging

# For relative imports to work in Python 3.6
# import os
# import sys
# flake8: noqa
from .openmotics import BackendClient, LegacyApplicationClient, ServiceClient

# sys.path.append(os.path.dirname(os.path.realpath(__file__)))


__all__ = [
    "BackendClient",
    "ServiceClient",
    "LegacyApplicationClient",
]

logging.getLogger(__name__).addHandler(logging.NullHandler())
