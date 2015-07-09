=======================
Pelican Github Projects
=======================

Embed a list of your public GitHub projects in your pages.

Installation
============

To install pelican-github-projects, simply install it from PyPI:

.. code-block:: bash

    $ pip install pelican-github-projects

Configuration
=============

Enable the plugin in your pelicanconf.py

.. code-block:: python

    PLUGINS = [
        # ...
        'pelican-github-projects',
        # ...
    ]

Add a setting with your GitHub username.

.. code-block:: python

    GITHUB_USER = 'kyah'

Available data
==============

:name:
    The name of your project.
:language:
    The language your project is written in, information on how GitHub detects
    languages is `available here
    <https://help.github.com/articles/my-repository-is-marked-as-the-wrong-language>`_.
    It is GitHub that detects the language, not this plugin. So please, no
    issues about that.
:description:
    The description of your project (as set on GitHub.)
:homepage:
    The homepage of your project (as set on GitHub.)
:github_url:
    The web page URL of your project on GitHub (not the GIT or API URL.)

Usage
=====

In your templates you will be able to iterate over the `github_projects`
variable, as below.

.. code-block:: html

    {% if GITHUB_USER %}
        {% for project in github_projects %}
          <h2>{{ project.name }} {% if project.language %}<sup>({{ project.language }})</sup>{% endif %}</h2>
          <p>{{ project.description }}</p>
          <p>
            {% if project.homepage %}
                <a href="{{ project.homepage }}">Homepage</a>
            {% endif %}
            <a href="{{ project.github_url }}">GitHub</a>
          </p>
        {% endfor %}
    {% endif %}

License
=======

`GPLv2`_ license.

.. _GPLv2: http://opensource.org/licenses/GPL-2.0
