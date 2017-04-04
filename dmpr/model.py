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
from .um.model import UM

def identify_model(path):
    """
    Identify the model under path

    >>> identify_model('test/sample/um').name
    'UM'
    """
    return UM()

def model_from_name(name):
    """
    Return the model object for a given name

    >>> model_from_name('UM').name
    'UM'
    """
    if name == UM.name:
        return UM()
    else:
        raise ArgumentError
