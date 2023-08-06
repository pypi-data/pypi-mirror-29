Django-GitHub-Revision
======================

Publishes information about the git revision that is running and links
to the GitHub repository.

Getting Started
---------------

Prerequisites
~~~~~~~~~~~~~

Do you need exists project managed by Django to use this project.

Installing
~~~~~~~~~~

To get up application running install it:

.. code:: bash

    pip install django_github_revision

Next to update Django settings:

.. code:: python

    INSTALLED_APPS += ['github_revision', ]
    GITHUB_REVISION_REPO_URL = 'https://github.com/watchdogpolska/django-github-revision'

Finally use template tags:

.. code:: html

    {% load github_revision_tags %}
    {% github_link %}

Alternatively use context processors available at ```github_revision.context_processors.github_revision```.

Raven integration
~~~~~~~~~~~~~~~~~

If you use Sentry you propably want use following settings:

.. code:: python

    from dealer.auto import auto

    RELEASE_ID = auto.revision
    RAVEN_CONFIG = {
        'dsn': env.str('RAVEN_DSN', 'http://example.com'),
        'release': RELEASE_ID,
    }

Running the tests
-----------------

To run tests execute::

    tox

Versioning
----------

We use `SemVer`_ for versioning. For the versions available, see the
`tags on this repository`_.

Authors
-------

-  **Adam Dobrawy** - *Initial work* - `ad-m`_

See also the list of `contributors`_ who participated in this project.

License
-------

This project is licensed under the MIT License - see the `LICENSE`_ file
for details

.. _SemVer: http://semver.org/
.. _tags on this repository: https://github.com/watchdogpolska/django-github-revision/tags
.. _ad-m: https://github.com/ad-m
.. _contributors: https://github.com/watchdogpolska/django-github-revision/contributors
.. _LICENSE: LICENSE