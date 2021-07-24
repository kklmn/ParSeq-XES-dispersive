# -*- coding: utf-8 -*-
__author__ = "Konstantin Klementiev"
__date__ = "23 Jul 2021"
# !!! SEE CODERULES.TXT !!!

# import numpy as np
from silx.gui import qt
from silx.gui.plot.tools.roi import RegionOfInterestManager
from silx.gui.plot.items import roi as roi_items

import sys; sys.path.append('..')  # analysis:ignore
from parseq.core import singletons as csi
from parseq.third_party import xrt

# from parseq.core import commons as cco
from parseq.gui.propWidget import PropWidget


class Tr0Widget(PropWidget):
    u"""
    Help page under construction

    .. image:: _images/mickey-rtfm.gif
       :width: 309

    test link: `MAX IV Laboratory <https://www.maxiv.lu.se/>`_

    """

    def __init__(self, parent=None, node=None, transform=None):
        super(Tr0Widget, self).__init__(parent, node, transform)

        self.roi = None

        layout = qt.QVBoxLayout()

        label2D = qt.QLabel(
            '`dispersive2D` image is the last image\nin the 3D stack')
        label2D.setStyleSheet("QLabel {font: bold;}")
        layout.addWidget(label2D)

        cutoffPanel = qt.QGroupBox(self)
        cutoffPanel.setFlat(False)
        cutoffPanel.setTitle('pixel value cutoff')
        cutoffPanel.setCheckable(True)
        self.registerPropWidget(cutoffPanel, cutoffPanel.title(),
                                'cutoffNeeded')
        layoutC = qt.QVBoxLayout()

        layoutL = qt.QHBoxLayout()
        cutoffLabel = qt.QLabel('cutoff')
        layoutL.addWidget(cutoffLabel)
        cutoff = qt.QSpinBox()
        cutoff.setToolTip(u'0 ≤ cutoff ≤ 1e8')
        cutoff.setMinimum(0)
        cutoff.setMaximum(1e8)
        cutoff.setSingleStep(100)
        self.registerPropWidget([cutoff, cutoffLabel], cutoffLabel.text(),
                                'cutoff')
        layoutL.addWidget(cutoff)
        layoutC.addLayout(layoutL)

        layoutL = qt.QHBoxLayout()
        maxLabel = qt.QLabel('max under cutoff = ')
        layoutL.addWidget(maxLabel)
        maxValue = qt.QLabel()
        self.registerStatusLabel(maxValue, 'cutoffMaxBelow')
        layoutL.addWidget(maxValue)
        maxLabelFrame = qt.QLabel('in frame ')
        layoutL.addWidget(maxLabelFrame)
        # maxValueFrame = qt.QLabel()
        maxValueFrame = qt.QPushButton()
        maxValueFrame.setMinimumWidth(28)
        maxValueFrame.setFixedHeight(17)
        self.registerStatusLabel(maxValueFrame, 'cutoffMaxFrame')
        maxValueFrame.clicked.connect(self.gotoFrame)
        layoutL.addWidget(maxValueFrame)
        layoutC.addLayout(layoutL)

        vmaxPanel = qt.QGroupBox(self)
        vmaxPanel.setFlat(False)
        vmaxPanel.setTitle('auto colormap.vmax as')
        vmaxPanel.setCheckable(True)
        self.registerPropWidget(vmaxPanel, vmaxPanel.title(), 'autoVMax')
        layoutV = qt.QHBoxLayout()
        fracVMaxEdit = qt.QLineEdit()
        fracVMaxEdit.setMinimumWidth(32)
        fracVMaxEdit.setSizePolicy(
            qt.QSizePolicy.Expanding, qt.QSizePolicy.Fixed)
        layoutV.addWidget(fracVMaxEdit)
        fracVMaxLabel = qt.QLabel('× (max under cutoff)')
        self.registerPropWidget(
            (fracVMaxEdit, fracVMaxLabel), 'vmax fraction', 'fracVMax',
            convertType=float)
        layoutV.addWidget(fracVMaxLabel)
        vmaxPanel.setLayout(layoutV)
        layoutC.addWidget(vmaxPanel)

        cutoffPanel.setLayout(layoutC)
        self.registerPropGroup(
            cutoffPanel, [cutoff, cutoffPanel], 'cutoff properties')
        layout.addWidget(cutoffPanel)

        self.roiPanel = qt.QGroupBox(self)
        self.roiPanel.setTitle('use rectangle ROI')
        self.roiPanel.setCheckable(True)
        layoutR = qt.QVBoxLayout()
        # layoutR.setContentsMargins(0, 0, 0, 0)
        self.roiGeom = qt.QLabel('not defined')
        layoutR.addWidget(self.roiGeom)
        self.registerPropWidget(self.roiGeom, 'roi geometry', 'roi')
        self.roiApplyDynamically = qt.QCheckBox('apply ROI dynamically')
        self.roiApplyDynamically.setChecked(True)
        layoutR.addWidget(self.roiApplyDynamically)
        self.roiApply = qt.QPushButton('apply ROI')
        self.roiApply.clicked.connect(self.updateROI)
        layoutR.addWidget(self.roiApply)
        self.roiPanel.setLayout(layoutR)
        self.roiPanel.toggled.connect(self.use2Droi)
        self.registerPropWidget(self.roiPanel, 'use2Droi', 'use2Droi')
        layout.addWidget(self.roiPanel)

        layout.addStretch()
        self.setLayout(layout)

    def setROI(self):
        data = csi.selectedItems[0]
        dtparams = data.transformParams
        geom = dtparams['roi']
        if not geom:
            dy, dx = data.dispersive2D.shape
            geom = [int(dy*0.25), 0, int(dx*0.5), dy-1]
            for data in csi.selectedItems:
                data.transformParams['roi'] = geom
        self.roiGeom.setText('origin={0}; size={1}'.format(geom[:2], geom[2:]))

        if self.roi is None:
            self.roi = roi_items.RectangleROI()
            self.roi.setName('Rectangle ROI')
            self.roi.setEditable(True)
            # self.roi.setLineWidth(3)
            # self.roi.setLineStyle('-')
            self.roi.setGeometry(origin=geom[:2], size=geom[2:])
            self.roi.sigRegionChanged.connect(self.updateROIauto)

            self.roiManager = RegionOfInterestManager(
                self.node.widget.plot._plot)
            self.roiManager.setColor('#f7941e')
            self.roiManager.addRoi(self.roi)
        else:
            self.roi.setGeometry(origin=geom[:2], size=geom[2:])

    def gotoFrame(self):
        if len(csi.selectedItems) == 0:
            return
        data = csi.selectedItems[0]
        frame = data.transformParams['cutoffMaxFrame']
        self.node.widget.plot._browser.setValue(frame)

    def setColormapMax(self):
        if len(csi.selectedItems) == 0:
            return
        data = csi.selectedItems[0]
        dtparams = data.transformParams
        colormap = self.node.widget.plot.getColormap()
        if dtparams['autoVMax']:
            cmapMax = dtparams['cutoffMaxBelow'] * dtparams['fracVMax']
            colormap.setVRange(vmin=0, vmax=cmapMax)
        else:
            colormap.setVRange(vmin=0, vmax=None)

    def extraSetUIFromData(self):
        if len(csi.selectedItems) == 0:
            return
        self.gotoFrame()

        data = csi.selectedItems[0]
        dtparams = data.transformParams
        if dtparams['use2Droi']:
            self.setROI()
        if self.roi is not None:
            self.roi.setVisible(dtparams['use2Droi'])
            geom = data.transformParams['roi']
            lims = geom[0] - 10, geom[0] + geom[2] + 10
            self.node.widget.plot._plot.getXAxis().setLimits(*lims)

    def extraPlot(self):
        self.setColormapMax()
        if self.node.widget.wasNeverPlotted:
            data = csi.selectedItems[0]
            dtparams = data.transformParams
            if dtparams['use2Droi']:
                geom = data.transformParams['roi']
                lims = geom[0] - 10, geom[0] + geom[2] + 10
                self.node.widget.plot._plot.getXAxis().setLimits(*lims)

    def updateROIauto(self):
        if self.roiApplyDynamically.isChecked():
            self.updateROI()

    def updateROI(self):
        geom = [int(v) for v in self.roi.getOrigin()] +\
            [int(v) for v in self.roi.getSize()]
        self.roiGeom.setText('origin={0}; size={1}'.format(geom[:2], geom[2:]))
        self.updateProp('transformParams.roi', geom)

    def use2Droi(self, on):
        checkBox = self.sender()
        if not checkBox.hasFocus():
            return
        if len(csi.selectedItems) == 0:
            return
        if on:
            self.setROI()
        if self.roi is not None:
            self.roi.setVisible(on)


class Tr1Widget(PropWidget):
    u"""
    Help page under construction

    .. image:: _images/mickey-rtfm.gif
        :width: 309

    test link: `MAX IV Laboratory <https://www.maxiv.lu.se/>`_

    """

    def __init__(self, parent=None, node=None, transform=None):
        super(Tr1Widget, self).__init__(parent, node, transform)

        layout = qt.QVBoxLayout()

        # layoutL = qt.QHBoxLayout()
        # condValueLabel = qt.QLabel('condition number = ')
        # layoutL.addWidget(condValueLabel)
        # condValueValue = qt.QLabel()
        # self.registerStatusLabel(condValueValue, 'condValue', textFormat='.5g')
        # layoutL.addWidget(condValueValue)
        # layout.addLayout(layoutL)

        self.dcmPanel = qt.QGroupBox(self)
        self.dcmPanel.setTitle('convolve with primary energy band')
        self.dcmPanel.setCheckable(True)
        layoutB1 = qt.QVBoxLayout()
        layoutB2 = qt.QHBoxLayout()
        dcmLabel = qt.QLabel('DCM crystals')
        layoutB2.addWidget(dcmLabel)
        self.dcmCombo = qt.QComboBox()
        self.dcmCombo.addItems(xrt.crystals.keys())
        layoutB2.addWidget(self.dcmCombo, 1)
        self.dcmCombo.currentTextChanged.connect(self.dcmTextChanged)
        layoutB1.addLayout(layoutB2)
        dcmShow = qt.QCheckBox('show it')
        self.registerPropWidget(dcmShow, 'show DCM band', 'convolveShow')
        layoutB1.addWidget(dcmShow)
        self.dcmPanel.setLayout(layoutB1)
        self.dcmPanel.toggled.connect(self.dcmConvolve)
        self.registerPropWidget(self.dcmPanel, 'convolve', 'convolve')
        self.registerPropWidget((self.dcmCombo, dcmLabel),
                                'convolve with dcm band', 'convolveWith')
        layout.addWidget(self.dcmPanel)

        layout.addStretch()
        self.setLayout(layout)

    def dcmConvolve(self, on):
        checkBox = self.sender()
        if not checkBox.hasFocus():
            return
        self.updateProp('transformParams.convolve', on)

    def dcmTextChanged(self, txt):
        comboBox = self.sender()
        if not comboBox.hasFocus():
            return
        if len(csi.selectedItems) == 0:
            return
        prop = 'transformParams.convolveWith'
        self.updateProp(prop, txt)

    def extraPlot(self):
        if len(csi.selectedItems) == 0:
            return
        data = csi.selectedItems[0]
        dtparams = data.transformParams
        if dtparams['convolve'] and dtparams['convolveShow']:
            xtal = dtparams['convolveWith']
            if xrt.rc[xtal] is not None:
                plot = self.node.widget.plot
                legend = 'rc({0})'.format(xtal)
                plot.addCurve(
                    data.energy, xrt.rc[xtal]*data.xes.max(), linestyle='-',
                    symbol='.', color='gray', legend=legend, resetzoom=False)
                curve = plot.getCurve(legend)
                curve.setSymbolSize(3)
