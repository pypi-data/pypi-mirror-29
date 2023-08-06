``gitflow-easyrelease``
~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://badge.fury.io/py/gitflow-easyrelease.svg
    :target: https://badge.fury.io/py/gitflow-easyrelease

.. image:: https://travis-ci.org/wizardsoftheweb/gitflow-easyrelease.svg?branch=master
    :target: https://travis-ci.org/wizardsoftheweb/gitflow-easyrelease

.. image:: https://coveralls.io/repos/github/wizardsoftheweb/gitflow-easyrelease/badge.svg?branch=master
    :target: https://coveralls.io/github/wizardsoftheweb/gitflow-easyrelease?branch=master

``gitflow-easyrelease`` aims to streamline ``git flow release`` commands. It adds some `semver <https://semver.org/>`__ shortcuts as well.

.. contents::

Installation
============

.. code:: sh-session

    $ pip install --user gitflow-easyrelease

Usage
=====

.. code:: sh-session

    $ export PATH=~/.local/bin:$PATH
    $ which git-easyrelease
    ~/.local/bin/git-easyrelease
    $ git easyrelease
    < should print the main help >
    $ git easyrelease --all-help
    < dumps all the help >

Positionals
===========

``version``
-----------

``version`` can be one of the following:

* ``p``, ``patch``, or ``~`` for a patch bump
* ``m``, ``minor``, or ``^`` for a minor bump
* ``M`` or ``major`` for a major bump
* ``X.Y.Z`` for a new, unconnected semver version
* ``<any string>`` for a not semver version

``base``
--------

``base`` is an optional branch to use as the base for the release. It requires |gitflow_avh|_, but it's totally optional and shouldn't break anything if you both don't have ``gitflow-avh`` and never use ``base``.

.. |gitflow_avh| replace:: the extended ``gitflow-avh``
.. _gitflow_avh: https://github.com/petervanderdoes/gitflow-avh

Commands
========

``init``
--------

``git easyrelease init [base]``

Convenience method to seed the release with ``0.0.0``. It runs

.. code:: sh-session

    $ git flow release start 0.0.0 <base>
    $ git flow release finish


``quick``
---------

``git easyrelease quick version [base]``

Convenience method to start and finish a release branch. It runs

.. code:: sh-session

    $ git flow release start <version> <base>
    $ git flow release finish


``start``
---------

``git easyrelease start version [base]``

Extends ``git flow release start`` with extra semver functionality. It runs

.. code:: sh-session

    $ git flow release start <version> <base>


``finish``
----------

``git easyrelease finish [version]``

Extends ``git flow release finish`` with extra semver functionality. Without ``version``, it attempts to ``finish`` the active branch. It runs

.. code:: sh-session

    $ git flow release finish <version>


``publish``
-----------

``git easyrelease publish [version]``

Extends ``git flow release publish`` with extra semver functionality. Without ``version``, it attempts to ``publish`` the active branch. It runs

.. code:: sh-session

    $ git flow release publish <version>


``delete``
----------

``git easyrelease delete [version]``

Extends ``git flow release delete`` with extra semver functionality. Without ``version``, it attempts to ``delete`` the active branch. It runs

.. code:: sh-session

    $ git flow release delete <version>


Roadmap
=======

These percentages are pretty arbitrary. Today's 47% could be tomorrow's 90% or vice versa.

Main Features
-------------

Once all of these are finished, I'll release `v1`. Until then, `v0` should be used with caution, because it's not stable.

.. csv-table::
    :header: "Progress", "Feature"

    "100%", "Testing ``v0.2.0``"

Eventual Features
-----------------

These are things I'd like to add, but probably won't be included in `v1`. If not, they'll most likely constitute one or more minor version increments.

.. csv-table::
    :header: "Progress", "Feature"

    "10%", "``git config`` integration (or, rather, ``gitflow`` config integration"
    "0%", "Disable ``base`` without ``gitflow-avh``"
