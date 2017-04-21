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
from bs4 import BeautifulSoup
import re
import click
from tabulate import tabulate

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

plan_re = re.compile('.*/projects/(?P<project_id>[^/]+)/plans/(?P<plan_id>[^/]+)/edit$')

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

@click.group(name='dmp')
def dmpcli():
    """
    Commands for working with Data Management Plans
    """
    pass

@dmpcli.command()
@click.option('--server', default = default_server)
@click.option('--email', prompt=True)
@click.password_option(confirmation_prompt=False)
def list(server, email, password):
    """
    List available DMPs::

        click list
    """
    s = DMPServer(server)
    s.login(email, password)
    table = [[project.id, project.title, project.url] for project in s.projects()]
    print(tabulate(table, headers=['ID', 'Title', 'URL']))

@dmpcli.command()
@click.option('--server', default = default_server)
@click.option('--email', prompt=True)
@click.password_option(confirmation_prompt=False)
@click.option('-o','--output', type=click.Path(file_okay=False))
@click.option('--format', type=click.Choice(['json', 'xml', 'text', 'csv', 'pdf', 'docx']))
@click.argument('id', nargs=-1)
def export(server, email, password, output, format, id):
    """
    Export a DMP to a directory, either by ID number or URL slug::

        click export --output my-dmp 51
        click export --output my-dmp test-plan-9000
    """
    try:
        os.mkdir(output)
    except OSError:
        pass

    s = DMPServer(server)
    s.login(email, password)

    for i in id:
        p = s.project(i)

        # Export the project
        with open('project.json', 'w') as f:
            json.dump(f.json, f, indent=4)

        # Export plans
        plans = p.export_plans(form=format)
        for k, v in six.iteritems(plans):
            out = k.replace(' ','_') + '.' + format
            if format in ['pdf', 'docx']:
                mode = 'wb'
            else:
                mode = 'w'
            with open(out, mode) as f:
                f.write(v)

