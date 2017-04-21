#!/usr/bin/env python
"""
Copyright 2017 ARC Centre of Excellence for Climate Systems Science

author: Scott Wales <scott.wales@unimelb.edu.au>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import pytest

@pytest.fixture(scope='session')
def cfchecker():
    """
    Makes the CEDA CF Checker available for tests

    Will skip the entire test if cfchecker is not available
    """
    cfchecks = pytest.importorskip('cfchecker.cfchecks')
    checker = cfchecks.CFChecker(
            cfStandardNamesXML=cfchecks.STANDARDNAME,
            cfAreaTypesXML=cfchecks.AREATYPES,
            version=None,
            )
    yield checker

@pytest.fixture(scope='session')
def dmp():
    """
    A sample DMP for testing post-processing
    """
    import dmpr.dmp
    import json
    server = dmpr.dmp.DMPServer()
    p = '{"created_at":"2015-03-23T00:49:13Z","data_contact":"","description":"I will be running a ACCESS AMIP simulation over 100 years to look at how ocean temperature correlates with atmospheric temperatures in Melbourne","dmptemplate_id":4,"funder_name":"","grant_number":"","id":39,"identifier":"","locked":null,"note":null,"organisation_id":9,"principal_investigator":"Scott Wales","principal_investigator_identifier":"","slug":"test-plan-9000","title":"Test Plan 9000","updated_at":"2015-03-23T00:51:06Z"}'
    project = dmpr.dmp.Project(server, json.loads(p))
    return dmpr.dmp.DMP(project)
