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

@pytest.fixture
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
