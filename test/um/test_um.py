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
from dmpr.model import identify_model

import os
sample = os.path.join(os.path.dirname(os.path.realpath(__file__)),'sample')

def test_identify_model():
    assert isinstance(identify_model(sample), UM)
    
def test_read_config():
    model = UM()
    model.read_configs(sample)
    assert model.runid == 'abcde'

def test_cfcheck(tmpdir, cfchecker):
    model = UM()
    model.read_configs(sample)
    model.archivedir = str(tmpdir)

    infile = '/short/w35/saw562/UM_ROUTDIR/saw562/vatad/vatada_pa000'
    outfile = model.post(infile)

    cfchecker.checker(outfile)

