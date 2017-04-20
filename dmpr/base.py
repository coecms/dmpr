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

"""
Abstract base classes used by the actual models
"""

from __future__ import print_function
import os
import os.path
import netCDF4
import sys
from datetime import datetime
from .dmp import DMP
from dmpr import __version__

class Model(object):
    """
    Base class of model processors

    .. py:attribute:: run_meta

        Dictionary for extra metadata to be added to the output file.
        ``run_meta['runid']`` is used to determine the output path

    .. py:attribute:: dmp

        :py:class:`~dmpr.dmp.DMP` attached to this model (may be ``None`` if
        not known yet)
    """

    def __init__(self):
        self.user = os.environ.get('USER', 'unknown')
        self.project = os.environ.get('PROJECT', 'unknown')
        self.dmp = None
        self.run_meta = {}
        self.attr_prefix = 'dmpr.'
        self.archivedir = os.path.join('/short',self.project,self.user,'dmp')

    def read_configs(self, rundir):
        """
        Read the run configuration, setting up run-based metadata

        To be overridden by model classes
        """
        raise NotImplementedError('To be overridden by the model class')

    def out_dir(self):
        """
        Returns the output directory for this model run
        """
        return os.path.join(self.archivedir, self.run_meta['runid'])

    def out_filename(self, infile):
        """
        Returns the base output filename

        May be overriden by the model class

        :param str infile: Filename of the input file as passed to ``dmpr post``

        >>> Model().out_filename('/path/to/foo.nc')
        'foo.nc'
        """
        return os.path.basename(infile)

    def post(self, infile):
        """
        Post-process a file and add metadata from the DMP

        Calls :py:meth:`~Model.post_impl()` to do the main processing, which
        gets overridden by model classes.

        :param str infile: Filename of the input file
        :return: Path to the processed output file
        :rtype: str
        """
        outdir = self.out_dir()

        try:
            os.makedirs(outdir)
        except OSError:
            pass

        outfile = os.path.join(outdir, self.out_filename(infile))
        self.post_impl(infile, outfile)

        # Add DMP metadata
        if self.dmp is not None:
            self.dmp.addmeta(outfile)

        # Add file-level metadata
        self.addmeta(infile, outfile)

        return outfile

    def post_impl(self, infile, outfile):
        """
        Post-processing implementation

        Must be overridden by the model class

        :param str infile: Filename of the input file
        :param str outfile: Filename of the output file (created by this function)
        """
        raise NotImplementedError('To be overridden by the model class')

    def set_dmp(self, dmp_name):
        """
        Set the Data Management Plan for this model run

        Creates a :py:class:`~dmpr.dmp.DMP` and attaches it to the model

        :param str dmp_name: Name of the DMP
        """
        self.dmp = DMP(dmp_name)

    def addmeta(self, infile, outfile):
        """
        Add file-level metadata to the processed file, including history and
        anything added to the dictionary :py:attr:`Model.run_meta`.

        :param str infile: Filename of the input file
        :param str outfile: Filename of the output file
        """
        with netCDF4.Dataset(outfile, mode="a") as f:
            f.setncatts(self.run_meta)

            try:
                history = f.getncattr('history')
            except AttributeError:
                history = ""
            history += "%s %s(%s) post %s\n"%(datetime.now().isoformat(),
                    sys.argv[0], __version__,
                    infile)
            f.setncattr('history', history)

