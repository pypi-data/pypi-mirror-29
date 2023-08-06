"""
This file provides a utility function to check if a version is proper semver
"""

from re import compile as re_compile, match

SEMVER_PATTERN = re_compile(r'\s*v?\d+\.\d+\.\d+\s*')


def is_semver(version):
    """Checks if a version string is semver"""
    return not match(SEMVER_PATTERN, version) is None
