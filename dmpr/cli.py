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
import click
from .model import identify_model, model_from_name
from .dmp import dmpcli
from .dmponline import default_server

@click.group()
def main():
    """
    ARCCSS Data Publication Tools
    """
    pass

@main.command()
@click.option('-r','--rundir', prompt=True)
@click.option('-m','--model')
@click.option('--dmp')
@click.option('--server', default = default_server)
@click.argument('file', nargs=-1)
def post(dmp, model, rundir, server, file):
    """
    Post-process climate data files

    If model is not specified it will be determined from the run directory
    """
    
    # Identify the model type
    if model is not None:
        m = model_from_name(model)
    else:
        m = identify_model(rundir)
    m.read_configs(rundir)

    # Set the DMP if present
    if dmp is not None:
        m.run_meta['data-management-plan'] = '%s/projects/%s'%(server, dmp)

    # Process the files
    for f in file:
        newfile = m.post(f)
        print(newfile)

@main.command()
def stage():
    """
    Stage a run for publication, checking metadata and moving to ua8
    """
    pass

main.add_command(dmpcli)
