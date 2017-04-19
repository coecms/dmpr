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

import os
import os.path
from .dmp import DMP

class Model(object):
    """
    Base class of model processors
    """

    def __init__(self):
        self.user = os.environ.get('USER')
        self.project = os.environ.get('PROJECT')
        self.dmp = None
        self.file_meta = {}
        self.archivedir = os.path.join('/short',self.project,self.user,'dmp')

    def read_configs(self, rundir):
        """
        Read the run configuration, setting up run-based metadata
        """
        raise NotImplementedError('To be overridden by the model class')

    def outdir(self):
        return os.path.join(self.archivedir, self.runid)

    def outfile(self, infile):
        """
        Returns the base output filename

        >>> Model().outfile('/path/to/foo.nc')
        'foo.nc'
        """
        return os.path.basename(infile)

    def post(self, infile):
        """
        Post-process a file and add metadata from the DMP, returning the processed file name
        """
        outdir = self.outdir()

        try:
            os.makedirs(outdir)
        except OSError:
            pass

        outfile = os.path.join(outdir, self.outfile(infile))
        self.post_impl(infile, outfile)

        # Add DMP metadata
        if self.dmp is not None:
            self.dmp.addmeta(outfile)

        return outfile

    def post_impl(self, infile, outfile):
        """
        Post-processing implementation, overrided
        """
        raise NotImplementedError('To be overridden by the model class')

    def set_dmp(self, dmp_name):
        """
        Set the current DMP
        """
        self.dmp = DMP(dmp_name)

    def file_meta(self, path, infile):
        """
        Add file-level metadata
        """
        with netcdf4.Dataset(path, mode="a") as f:
            f.setncatts(self.run_meta)

            history = f.getncattr('history')
            history += "%s %s(%s) %s\n"%(datetime.now().isoformat(),
                    __project_name__, __version__,
                    infile)

