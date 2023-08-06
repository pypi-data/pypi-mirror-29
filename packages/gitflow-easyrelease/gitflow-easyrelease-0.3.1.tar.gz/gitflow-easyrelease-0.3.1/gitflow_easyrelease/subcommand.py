"""This file provides the Subcommand class"""

from __future__ import print_function

from subprocess import check_output

from argparse_color_formatter import ColorHelpFormatter

from gitflow_easyrelease import ColorOutput, RepoInfo, SemVer


class Subcommand(object):
    """This class defines a subcommand to be run against the main app."""

    def __init__(  # pylint: disable=too-many-arguments
            self,
            subcommand='',
            help_string='',
            release_commands=None,
            has_version=True,
            version_optional=True,
            has_base=True
    ):
        self.subcommand = subcommand
        self.help_string = help_string
        self.release_commands = (
            release_commands
            if release_commands
            else []
        )
        self.has_version = has_version
        self.version_optional = version_optional
        self.has_base = has_base

    def attach_subparser(self, subparsers):
        """Adds its subparser to the parent parser"""
        parser = subparsers.add_parser(
            self.subcommand,
            description=self.help_string,
            formatter_class=ColorHelpFormatter,
            help=self.help_string
        )
        if self.has_version:
            Subcommand.attach_version_argument(parser, self.version_optional)
        if self.has_base:
            Subcommand.attach_base_argument(parser)

    def execute(self, parsed_args):
        """Executes its action"""
        version = (
            SemVer.process_version(parsed_args.version)
            if self.has_version and hasattr(parsed_args, 'version')
            else SemVer()
        )
        if version is None:
            raise ValueError(
                'Version was not passed in and the repo is not on a release branch'
            )
        base = (
            parsed_args.base
            if self.has_base and hasattr(parsed_args, 'base')
            else None
        )
        options = (
            parsed_args.options
            if hasattr(parsed_args, 'options')
            else None
        )
        for command in self.release_commands:
            Subcommand.execute_release_command(command, version, base, options)

    @staticmethod
    def attach_version_argument(parser, version_optional=True):
        """Adds a version input argument"""
        color_output = ColorOutput()
        options = {
            'help': (
                "The version to use."
                " %s, %s, and %s increment semver;"
                " anything else is used as the version string"
                % (
                    color_output('major', style='bold'),
                    color_output('minor', style='bold'),
                    color_output('patch', style='bold')
                )
            ),
            'type': str
        }
        if version_optional:
            options['nargs'] = '?'
        parser.add_argument('version', **options)

    @staticmethod
    def attach_base_argument(parser):
        """Adds a base branch argument"""
        parser.add_argument(
            "base",
            nargs="?",
            default=None,
            help="Optional base branch",
            choices=RepoInfo.get_branches(),
            type=str
        )

    @staticmethod
    def execute_release_command(command, version, base=None, options=None):
        """Executes a specific git flow release subcommand"""
        command = ['git', 'flow', 'release', command, "%s" % version]
        if base:
            command.append(base)
        if options:
            command = command + options
        check_output(command)
