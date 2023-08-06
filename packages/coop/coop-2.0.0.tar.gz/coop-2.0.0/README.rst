Coop - base for all (most) Takeflight sites
===========================================

This is a base to build all Takeflight sites off. This package contains all the
common code shared between sites, with the ideal Takeflight site containing only
model definitions, templates, and front end assets.

Making a release
----------------

Upgrade the version in ``coop/_version.py``.
Coop follows `semver <http://semver.org/>`_ for its versioning scheme.

Update the CHANGELOG. Please.

Tag your release:

.. code-block:: bash

    $ git tag "x.y.z"
    $ git push --tags

Make a virtual environment and activate it. You may already have one from last time:

.. code-block:: bash

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install wheel # Only required once per venv

Then, package up and publish the package:

.. code-block:: bash

    $ ./setup.py sdist bdist_wheel upload

And you are done!
