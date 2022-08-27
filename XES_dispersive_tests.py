# -*- coding: utf-8 -*-
__author__ = "Konstantin Klementiev"
__date__ = "23 Jul 2021"
# !!! SEE CODERULES.TXT !!!

import os.path as osp
from os.path import dirname as up

import sys; sys.path.append('..')  # analysis:ignore
import parseq.core.singletons as csi


def load_test_data():
    dirname = up(osp.abspath(__file__))

    scanName = (
        "silx:" + osp.join(dirname, 'data', '20201112_b.h5') + "::/entry10198")
    dataNameElastic3D = (
        "silx:" + osp.join(
            dirname, 'data',
            'NbO2_Kb13-inCircle-elastic-scan_96_data_000001.h5') +
        "::/entry/data/data")

    dataNameDispersive2D = (
        "silx:" + osp.join(
            dirname, 'data', 'NbO2_Kb13-inCircle_94_data_000001.h5') +
        "::/entry/data/data")
    dispersive2Dcut = '22, :, :'

    # # to check with an image from the basis set:
    # dataNameDispersive2D = (
    #     "silx:" + osp.join(
    #         dirname, 'data',
    #         'NbO2_Kb13-inCircle-elastic-scan_96_data_000001.h5') +
    #     "::/entry/data/data")
    # dispersive2Dcut = '30, :, :'

    elastic3Dcut = ''
    h5Format = [
        'measurement/mono1_energy',
        'd["measurement/albaem01_ch1"] + d["measurement/albaem01_ch2"]']

    rootItem = csi.dataRootItem
    rootItem.kwargs['runDownstream'] = True

    slices = ['', '', elastic3Dcut, dispersive2Dcut]
    dataFormat0 = dict(
        dataSource=h5Format+[dataNameElastic3D, dataNameDispersive2D],
        slices=slices)
    transformParams0 = dict(use2Droi=True, roi=[400, 0, 82, 1064])
    spectrum0 = rootItem.insert_data(
        scanName, dataFormat=dataFormat0, copyTransformParams=False,
        transformParams=transformParams0, runDownstream=True)[0]
