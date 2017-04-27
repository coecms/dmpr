#!/usr/bin/env python
# Copyright 2017 ARC Centre of Excellence for Climate Systems Science
# author: Scott Wales <scott.wales@unimelb.edu.au>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import print_function
import six
from six.moves.urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import re

default_server = 'http://dmp.climate-cms.org:3000'

class DMPOnline(object):
    """
    A connection to DMPonline
    """
    plan_re = re.compile('.*/projects/(?P<project_id>[^/]+)/plans/(?P<plan_id>[^/]+)/edit$')

    def __init__(self, server = default_server):
        self.server = server
        self._projects_cache = None
        self.session = requests.Session()

    def login(self, email, password):
        """
        Log in to DMPOnline
        """
        r = self._get('users/sign_in')
        soup = BeautifulSoup(r.text, 'html.parser')
        token = soup.find('input', attrs={'name':'authenticity_token'})['value']
        r = self._post('users/sign_in', 
                data={'user[email]': email,
                    'user[password]': password,
                    'authenticity_token': token})

    def projects(self):
        """
        Get the available projects
        """
        if self._projects_cache is None:
            r = self._get('projects.json')
            self._projects_cache = [Project(self, p) for p in r.json()]
        return self._projects_cache

    def project(self, id):
        """
        Get a single project given the ID

        :param id: Project ID
        """
        r = self.get('projects/%s.json'%id)
        return Project(self, r.json())

    def requests(self):
        """
        Get the available requests
        """
        if self._requests_cache is None:
            r = self._get('requests.json')
            self._requests_cache = [Request(self, p) for p in r.json()]
        return self._requests_cache

    def request(self, id):
        """
        Get a single request given the ID

        :param id: Request ID
        """
        r = self.get('requests/%s.json'%id)
        return Project(self, r.json())

    def _post(self, url, **kwargs):
        fullurl = urljoin(self.server, url)
        r = self.session.post(fullurl, **kwargs)
        try:
            r.raise_for_status()
        except requests.HTTPError:
            print(r.headers)
            raise

        return r

    def _get(self, url, **kwargs):
        fullurl = urljoin(self.server, url)
        r = self.session.get(fullurl, **kwargs)
        try:
            r.raise_for_status()
        except requests.HTTPError:
            print(r.request.headers)
            print(r.headers)
            raise
        return r

class Project(object):
    """
    A DMPOnline project

    Contains the same attributes as you'll find in DMPOnline's ``/projects.json``
    """

    def __init__(self, server, json):
        self.server = server
        # Set attributes automatically from the Json
        [setattr(self, k, v) for k, v in six.iteritems(json)]
        self.json = json

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<%s>'%self.url

    @property
    def url_path(self):
        return 'projects/%s'%self.slug

    @property
    def url(self):
        return urljoin(self.server.server, self.url_path)

    def plan_urls(self):
        """
        Returns the plans attached to this project as a dictionary
        """
        _plans = {}

        # Get the tab links
        r = self.server._get(self.url_path)
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.find(id='project-tabs').find_all('a')

        # Get the plan URLs
        for link in links:
            match = plan_re.match(link.href)
            if match is not None:
                plan_id = match.groupdict()['plan_id']
                _plans[link.text] = '%s/plans/%s'%(self.url_path, plan_id)
        return _plans

    def export_plans(form):
        """
        Export this project's plans

        :param str form: Output format
        """
        urls = self.plan_urls()
        _plans = {}

        for k, v in six.iteritems(urls):
            if form in ['json', 'xml', 'text', 'csv']:
                _plans[k] = self.server._get('%s/export'%v, data={'format': form}).text
            else:
                _plans[k] = self.server._get('%s/export'%v, data={'format': form}).content
        return _plans

