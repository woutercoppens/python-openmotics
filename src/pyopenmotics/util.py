"""Collection of small utility functions for OpenMotics API."""
from __future__ import annotations


def feature_used(
    features: dict,
    feat_to_check: str,
) -> bool | None:
    """Check if a feature is available and used.

    Args:
        features: a dictionary with featueres
            'features':
             {'outputs': {'available': True, 'used': True, 'metadata': None},
              'thermostats': {'available': True, 'used': False, 'metadata': None},
              'energy': {'available': True, 'used': True, 'metadata': None},
        feat_to_check: feature to check if it is in features

    Returns:
        True is feat_to_check is in features

    """
    feat_available = False
    feat_used = False
    try:
        feature = features[feat_to_check]
    except KeyError:
        return False
    for key, value in feature.items():
        if key in ["available"]:
            feat_available = value
        if key in ["used"]:
            feat_used = value
    return feat_available and feat_used
