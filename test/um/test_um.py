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

from dmpr.um.model import *

import os
import pytest
import sys
from compliance_checker.suite import CheckSuite

sampledir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'sample')

@pytest.fixture(scope='module')
def archivedir(tmpdir_factory):
    return str(tmpdir_factory.mktemp('um'))

@pytest.fixture(scope='module')
def standardised(archivedir):
    model = UM()

    outfile = os.path.join(archivedir, 'abcdea_da000.nc')

    model.standardise(
            [os.path.join(sampledir, 'abcdea_da000')],
            outfile)

    return outfile

def test_standardise_exists(standardised):
    assert os.path.isfile(standardised)

def test_standardise_cf(standardised):
    suite = CheckSuite()
    suite.load_all_available_checkers()

    ds = suite.load_dataset(standardised)
    results = suite.run(ds, [], 'cf')

    check_failures = 0
    for r in results['cf'][0]:
        if r.value[1] - r.value[0] > 0:
            print(r, file=sys.stderr)
            check_failures += 1

    assert check_failures == 0
