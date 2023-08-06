"""This file provides the SemVer class"""

from __future__ import print_function

from gitflow_easyrelease import is_semver, RepoInfo


class SemVer(object):
    """This class encapsulates semantic versioning logic."""

    PATCH_KEYS = ['p', 'patch', '~']
    MINOR_KEYS = ['m', 'minor', '^']
    MAJOR_KEYS = ['M', 'major']
    ALL_KEYS = PATCH_KEYS + MINOR_KEYS + MAJOR_KEYS

    def __init__(self, major=0, minor=0, patch=0):
        self.major = int(major)
        self.minor = int(minor)
        self.patch = int(patch)

    def compare(self, version=None):
        """Compares its own semver against version"""
        if not isinstance(version, SemVer):
            version = SemVer.from_version(version)
        if version:
            for component in ['major', 'minor', 'patch']:
                comparison = SemVer.compare_component(
                    getattr(self, component),
                    getattr(version, component)
                )
                if 0 != comparison:
                    return comparison
            return 0
        return -1

    def greater(self, version=None):
        """Checks if self is greater than version"""
        return -1 == self.compare(version)

    def lesser(self, version=None):
        """Checks if self is less than version"""
        return 1 == self.compare(version)

    def equal(self, version=None):
        """Checks if self is equal to version"""
        return 0 == self.compare(version)

    def bump(self, component=None):
        """Increases the semver using the specified component"""
        if component in SemVer.ALL_KEYS:
            if component in SemVer.PATCH_KEYS:
                self.patch = self.patch + 1
            else:
                self.patch = 0
                if component in SemVer.MINOR_KEYS:
                    self.minor = self.minor + 1
                else:
                    self.minor = 0
                    self.major = self.major + 1
        return self

    def __repr__(self):
        return "%d.%d.%d" % (self.major, self.minor, self.patch)

    @staticmethod
    def compare_component(first, second):
        """Compares two semver components"""
        if first < second:
            return 1
        elif first > second:
            return -1
        return 0

    @staticmethod
    def from_version(version):
        """Creates a SemVer object from a version string"""
        if is_semver(version):
            return SemVer(*version.replace('v', '').split('.'))
        return SemVer()

    @staticmethod
    def is_component(version):
        """Checks if a version string is a semver component"""
        return version in SemVer.ALL_KEYS

    @staticmethod
    def get_active_branch():
        """Determines the active branch"""
        args = RepoInfo().to_semver_args()
        if args:
            return SemVer(*args)
        return args

    @staticmethod
    def get_current_version():
        """Gets either the active semver or the topmost semver"""
        active = SemVer.get_active_branch()
        if active:
            return active
        versions = RepoInfo.get_semver_tags()
        if versions:
            max_version = SemVer.from_version(versions.pop())
            for version in versions:
                semver = SemVer.from_version(version)
                if semver.greater(max_version):
                    max_version = semver
            return max_version
        return SemVer()

    @staticmethod
    def process_version(version=None):
        """Creates a new SemVer from the version input"""
        if version:
            if is_semver(version):
                return SemVer.from_version(version)
            elif SemVer.is_component(version):
                return SemVer.get_current_version().bump(version)
            return version
        return SemVer.get_active_branch()
