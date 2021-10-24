""""Expose submodules."""
import logging

# For relative imports to work in Python 3.6
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from .openmotics import BackendClient, ServiceClient, LegacyApplicationClient

__all__ = {
    "BackendClient",
    "ServiceClient",
    "LegacyApplicationClient",
}

logging.getLogger(__name__).addHandler(logging.NullHandler())
