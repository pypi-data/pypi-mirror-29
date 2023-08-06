``gitflow-wotw``
~~~~~~~~~~~~~~~~

.. image:: https://badge.fury.io/py/gitflow-wotw.svg
    :target: https://badge.fury.io/py/gitflow-wotw

.. image:: https://travis-ci.org/wizardsoftheweb/gitflow-wotw.svg?branch=master
    :target: https://travis-ci.org/wizardsoftheweb/gitflow-wotw

.. image:: https://coveralls.io/repos/github/wizardsoftheweb/gitflow-wotw/badge.svg?branch=master
    :target: https://coveralls.io/github/wizardsoftheweb/gitflow-wotw?branch=master

``gitflow-wotw`` has grand aspirations to be ``gitflow-avh`` in Python using ``pygit2``.

.. contents::

Suggested Reading
=================

* The original `git flow article <http://nvie.com/posts/a-successful-git-branching-model/>`_
* |gitflow|_ (seriously outdated)
* |gitflow_avh|_ (highly recommended)
* |pygit2|_ (very useful)
* `semantic versioning <https://semver.org>`_ (it makes so much sense)

.. |gitflow| replace:: The first ``gitflow`` implementation
.. _gitflow: https://github.com/nvie/gitflow
.. |gitflow_avh| replace:: An updated and active fork, ``gitflow-avh``
.. _gitflow_avh: https://github.com/petervanderdoes/gitflow-avh
.. |pygit2| replace:: ``pygit2``, Python bindings for ``libgit2``
.. _pygit2: https://github.com/libgit2/pygit2

Installation
============

.. code:: shell-session

    $ pip install --user gitflow-wotw

Usage
=====

.. code:: shell-session

    $ export PATH=~/.local/bin:$PATH
    $ which git-wotw
    ~/.local/bin/git-wotw
    $ git wotw
    < should print the main help >

Roadmap
=======

These percentages are pretty arbitrary. Today's 47% could be tomorrow's 90% or vice versa.

Main Features
-------------

Once all of these are finished, I'll release ``v1``. Until then, ``v0`` should be used with caution, because it's not stable.

.. csv-table::
    :header: "Progress", "Feature"

    "0%", "``init`` support"
    "0%", "``feature`` support"
    "0%", "``bugfix`` support"
    "0%", "``release`` support"
    "0%", "``hotfix`` support"
    "0%", "``support`` support"
    "0%", "``version`` support"
    "0%", "``config`` support"
    "0%", "``log`` support"
    "0%", "Negatable options"

Eventual Features
-----------------

These are things I'd like to add, but might not be included in ``v1``. If not, they'll most likely constitute one or more minor version increments.

.. csv-table::
    :header: "Progress", "Feature"

    "0%", "Repo reflection"
    "0%", "``pygit2`` alternatives"
    "0%", "semver bindings"
    "0%", "Replace ``git wotw`` with ``git flow``"
    "0%", "Local hooks connected to ``gitflow`` actions"
    "0%", "User-defined shortcuts"
    "0%", "Create ``arguments`` from config files"
    "0%", "Create ``actions`` from config files"
    "0%", "Create ``subcommands`` from config files"
    "0%", "Create the main ``command`` from config files"
