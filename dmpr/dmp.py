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
from bs4 import BeautifulSoup
import click
from tabulate import tabulate

from .dmponline import DMPOnline, default_server

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
    s = DMPOnline(server)
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

    s = DMPOnline(server)
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

