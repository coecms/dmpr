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
import requests
import six
from six.moves.urllib.parse import urljoin


default_server = 'http://dmp.climate-cms.org:3000'

class DMPServer(object):
    """
    A connection to DMPonline
    """
    def __init__(self, server = default_server):
        self.server = server
        self.cookies = requests.cookies.RequestsCookieJar()
        self._projects_cache = None

    def login(self, email, password):
        """
        Log in to DMPOnline
        """
        self._post(data={'email': email, 'password': password})
        self.cookies.update(r.cookies)

    def projects(self):
        """
        Get the available projects
        """
        if self._projects_cache is None:
            r = self._get('projects.json')
            self._projects_cache = [Project(self, p) for p in r.json()]
        return self._projects_cache

    def _post(self, url, **kwargs):
        fullurl = urljoin(self.server, url)
        r = requests.post(fullurl, cookies=self.cookies, **kwargs)
        r.raise_for_status()
        return r

    def _get(self, url, **kwargs):
        fullurl = urljoin(self.server, url)
        r = requests.get(fullurl, cookies=self.cookies, **kwargs)
        r.raise_for_status()
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

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<%s>'%self.url

    @property
    def url(self):
        return urljoin(self.server.server, 'projects/%s'%self.slug)

class DMP(object):
    """
    DMP related metadata
    """

    def __init__(self, project):
        """
        Initialise the DMP

        :param dmpr.dmp.Project project: The project to initialise from
        """
        self.project = project

    def file_metadata(self):
        """
        Returns metadata that should be added to the file, as a dict
        """
        meta = {}
        meta['data_management_plan'] = self.project.url
        meta['data_contact'] = self.project.data_contact
        meta['principal_investigator'] = self.project.principal_investigator
        meta['principal_investigator_identifier'] = self.project.principal_investigator_identifier

        if self.project.grant_number:
            meta['funder_name'] = self.project.funder
            meta['grant_number'] = self.project.grant_number

        return meta


