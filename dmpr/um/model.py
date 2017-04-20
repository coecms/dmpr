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
from ..base import Model
import iris
import iris.fileformats.netcdf
import os
import re
import netCDF4

class UM(Model):
    """
    A Unified Model run
    """
    name = 'UM'

    def __init__(self):
        super(UM,self).__init__()

    def read_configs(self, rundir):
        """
        Read the UM namelists and set up metadata
        """
        runid_re = re.compile('^\s*RUNID=(.*)$')

        with open(os.path.join(rundir, 'SUBMIT')) as f:
            for line in f:
                m = runid_re.match(line)
                if m is not None:
                    self.run_meta['runid'] = m.group(1)


    def outfile(self, infile):
        """
        TODO: Decode UM file name
        """
        return os.path.basename(infile) + '.nc'

    def post_impl(self, infile, outfile):
        """
        Convert file using Iris
        """
        cubes = iris.load(infile)
        iris.fileformats.netcdf.save(cubes, outfile)

        # Cleanup CF compliance
        with netCDF4.Dataset(outfile, mode="a") as d:
            if 'level_height' in d.variables:
                v = d.variables['level_height']
                v.delncattr('axis')
