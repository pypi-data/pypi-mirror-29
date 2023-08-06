"""This file provides the cli function"""

from __future__ import print_function

from collections import OrderedDict

from gitflow_easyrelease import Application, ColorOutput, Subcommand


def cli():
    """Runs module from the CLI"""
    color_output = ColorOutput()
    subcommands = OrderedDict()
    subcommands['init'] = Subcommand(
        'init',
        help_string=(
            "Equivalent to %s"
            % (
                color_output('git autorelease quick 0.0.0', style='bold')
            )
        ),
        release_commands=['start', 'finish'],
        has_version=False,
        has_base=True
    )
    subcommands['quick'] = Subcommand(
        'quick',
        help_string=(
            "Starts and finishes a release (%s; %s)"
            % (
                color_output(
                    'git flow release start <version> <base>',
                    style='bold'
                ),
                color_output(
                    'git flow release finish <version>',
                    style='bold'
                ),
            )
        ),
        release_commands=['start', 'finish'],
        has_version=True,
        version_optional=False,
        has_base=True
    )
    subcommands['start'] = Subcommand(
        'start',
        help_string=(
            "Starts a release (%s)"
            % (
                color_output(
                    'git flow release start <version> <base>',
                    style='bold'
                )
            )
        ),
        release_commands=['start'],
        has_version=True,
        version_optional=False,
        has_base=True
    )
    subcommands['finish'] = Subcommand(
        'finish',
        help_string=(
            "Finishes a release (%s)"
            % (
                color_output(
                    'git flow release finish <version>',
                    style='bold'
                ),
            )
        ),
        release_commands=['finish'],
        has_version=True,
        version_optional=True,
        has_base=False
    )
    subcommands['publish'] = Subcommand(
        'publish',
        help_string=(
            "Publishes a release branch (%s)"
            % (
                color_output(
                    'git flow release publish <version>',
                    style='bold'
                )
            )
        ),
        release_commands=['publish'],
        has_version=True,
        version_optional=True,
        has_base=False
    )
    subcommands['delete'] = Subcommand(
        'delete',
        help_string=(
            "Deletes a release branch (%s)"
            % (
                color_output(
                    'git flow release delete <version>',
                    style='bold'
                )
            )
        ),
        release_commands=['delete'],
        has_version=True,
        version_optional=True,
        has_base=False
    )
    app = Application(subcommands)
    app.bootstrap()
