# -*- coding: utf-8 -*-
'''
pelican_github
-------

The github plugin generates a new Jinja variable containing all your github project's information
'''

from __future__ import unicode_literals
from pelican import signals
from pelican.generators import Generator

from operator import itemgetter
import json
import logging

try:
    # Python 2
    from urllib2 import urlopen
    from urllib2 import HTTPError
    from urllib2 import ProxyHandler
    from urllib2 import build_opener
    from urllib2 import install_opener
except ImportError:
    # Python 3
    from urllib.request import urlopen
    from urllib.request import HTTPError
    from urllib.request import ProxyHandler
    from urllib.request import build_opener
    from urllib.request import install_opener

logger = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com/users/{0}/repos"


class GithubProjectsGenerator(Generator):
    def __init__(self, *args, **kwargs):
        super(GithubProjectsGenerator, self).__init__(*args, **kwargs)
        github_url = GITHUB_API_URL.format(self.settings['GITHUB_USER'])
        http_proxy = None
        self.content = None
        if 'GITHUB_HTTP_PROXY' in self.settings :
            http_proxy = self.settings['GITHUB_HTTP_PROXY']
        if http_proxy:
            proxy_support = ProxyHandler({"http":http_proxy, "https":http_proxy})
            opener = build_opener(proxy_support)
            install_opener(opener)
        try:
            request = urlopen(github_url)
            # Python 3 or 2 makes us have to do nasty stuff to get encoding without being specific.
            encoding = request.headers['content-type'].split('charset=')[-1]
            decoded_request = request.read().decode(encoding)
            self.content = json.loads(decoded_request)
        except HTTPError:
            logger.warning("unable to open {0}".format(github_url))
            return

    def generate_context(self):
        logger.info('Adding github project\'s information to context')
        if self.content is None:
            return
        projects = []
        for repo in self.content:
            if repo['private']:
                continue
            r = {
                'name': repo['name'], 'language': repo['language'],
                'description': repo['description'], 'github_url': repo['html_url'],
                'homepage': repo['homepage']
            }
            projects.append(r)
        self.context['github_projects'] = sorted(projects, key=itemgetter('name'))


def get_generators(generators):
    return GithubProjectsGenerator


def register():
    signals.get_generators.connect(get_generators)
