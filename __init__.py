# -*- coding: utf-8 -*-
"""
A pipeline for data processing of XES spectra measured in energy dispersive
geometry. The energy dispersive image is projected onto the base set of images
given by the scanned elastically scattered band.

This pipeline also serves as an example for creating analysis nodes, transforms
that connect these nodes and widgets that set options and parameters of the
transforms.
"""
__author__ = "Konstantin Klementiev"
__date__ = "23 Jul 2021"

import os.path as osp

import sys; sys.path.append('..')  # analysis:ignore
from parseq.core import singletons as csi
from .XES_dispersive_pipeline import make_pipeline
from .XES_dispersive_tests import load_test_data

from .version import __versioninfo__, __version__, __date__

__author__ = "Konstantin Klementiev (MAX IV Laboratory)"
__email__ = "first dot last at gmail dot com"
__license__ = "MIT license"
__synopsis__ = "A pipeline for data processing of energy dispersive XES"

csi.pipelineName = 'XES dispersive'
csi.appPath = osp.dirname(osp.abspath(__file__))
csi.appIconPath = osp.join(
    csi.appPath, 'doc', '_images', 'XES_dispersive_icon.ico')
csi.appSynopsis = __synopsis__
csi.appDescription = __doc__
csi.appAuthor = __author__
csi.appLicense = __license__
