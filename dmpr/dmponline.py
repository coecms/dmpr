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
from six.moves.urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

default_server = 'http://dmp.climate-cms.org:3000'

class DMPServer(object):
    """
    A connection to DMPonline
    """
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
