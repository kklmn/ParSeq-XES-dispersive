# -*- coding: utf-8 -*-
__author__ = "Konstantin Klementiev"
__date__ = "13 Jun 2021"
# !!! SEE CODERULES.TXT !!!

import sys; sys.path.append('..')  # analysis:ignore
from parseq.core import nodes as cno
from collections import OrderedDict
import hdf5plugin  # needed to prevent h5py's "OSError: Can't read data"


class Node1(cno.Node):
    name = '3D elastic energy scan'
    arrays = OrderedDict()
    arrays['energy'] = dict(qUnit='eV', role='1D')
    arrays['i0'] = dict(
        qLabel='I0', qUnit='counts', role='1D', plotLabel=r'$I_0$')
    arrays['elastic3D'] = dict(
        raw='elastic3Draw', qUnit='counts', role='3D',
        plotLabel=['scan axis', 'horizontal pixel', 'tangential pixel'])
    arrays['dispersive2D'] = dict(
        raw='dispersive2Draw', qUnit='counts', role='2D')


class Node2(cno.Node):
    name = '1D energy XES'
    arrays = OrderedDict()
    arrays['energy'] = dict(qUnit='eV', role='x')
    arrays['xes'] = dict(qLabel='XES', qUnit='counts', role='yleft')
