# -*- coding: utf-8 -*-
__author__ = "Konstantin Klementiev"
__date__ = "23 Jul 2021"
# !!! SEE CODERULES.TXT !!!

import numpy as np

import scipy.linalg as spl

import sys; sys.path.append('..')  # analysis:ignore
from parseq.core import transforms as ctr
# from parseq.utils import math as uma
from parseq.third_party import xrt

cpus = 'half'  # can be int, 'all' or 'half'


def _line(xs, ys):
    k = (ys[1] - ys[0]) / (xs[1] - xs[0])
    b = ys[1] - k*xs[1]
    return k, b


class Tr0(ctr.Transform):
    name = 'mask Eiger'
    defaultParams = dict(
        cutoffNeeded=True, cutoff=2000, cutoffMaxBelow=0, cutoffMaxFrame=0,
        autoVMax=True, fracVMax=0.1, use2Droi=False, roi=[])
    nThreads = cpus
    # nProcesses = cpus
    # inArrays and outArrays needed only for multiprocessing/multithreading:
    inArrays = ['elastic3Draw', 'dispersive2Draw']
    outArrays = ['elastic3D', 'dispersive2D']

    @staticmethod
    def run_main(data):
        dtparams = data.transformParams

        data.elastic3D = np.array(data.elastic3Draw)
        data.dispersive2D = np.array(data.dispersive2Draw)
        if dtparams['cutoffNeeded']:
            cutoff = dtparams['cutoff']
            data.elastic3D[data.elastic3D > cutoff] = 0
            data.dispersive2D[data.dispersive2D > cutoff] = 0
            dtparams['cutoffMaxBelow'] = data.elastic3D.max()
            dtparams['cutoffMaxFrame'] = np.unravel_index(
                data.elastic3D.argmax(), data.elastic3D.shape)[0]
        shape2D = data.dispersive2D.shape
        data.elastic3D = np.concatenate(
            (data.elastic3D, data.dispersive2D.reshape(1, *shape2D)), axis=0)

        roi = dtparams['roi']
        if dtparams['use2Droi'] and roi:
            cy, cx, dy, dx = roi
            xslice = slice(max(cx, 0), dx+cx)
            yslice = slice(max(cy, 0), dy+cy)

            tmp = np.zeros_like(data.dispersive2D)
            tmp[xslice, yslice] = data.dispersive2D[xslice, yslice]
            data.dispersive2D = tmp

            tmp = np.zeros_like(data.elastic3D)
            tmp[:, xslice, yslice] = data.elastic3D[:, xslice, yslice]
            data.elastic3D = tmp

        return True


class Tr1(ctr.Transform):
    """Unpublished and therefore obfuscated"""

    name = 'project onto basis'
    defaultParams = dict(
        cutoffMin=None, cutoffMax=None,
        # condValue=0,
        convolve=True, convolveWith='Si111')
    nThreads = cpus
    # nProcesses = cpus
    # inArrays and outArrays needed only for multiprocessing/multithreading:
    inArrays = ['energy', 'i0', 'elastic3D', 'dispersive2D']
    outArrays = ['xes']

    @staticmethod
    def run_main (O00OOO000O000OO00 ):
        O0O0O00O00O0000OO =O00OOO000O000OO00 .transformParams
        O0OOO0O0O0O00OOOO =O0O0O00O00O0000OO ['roi']
        if O0O0O00O00O0000OO ['use2Droi']and O0OOO0O0O0O00OOOO :
            OO00OOO0O00OO0O0O ,O0OOOO000O0O0OO00 ,O00OOOO00OO00OO00 ,OO000O0OO0OOO0OOO =O0OOO0O0O0O00OOOO
            OO0OO0O0O0OO0000O =slice (max (O0OOOO000O0O0OO00 ,0 ),OO000O0OO0OOO0OOO +O0OOOO000O0O0OO00 +1 )
            O0O00OOOO0OO0O00O =slice (max (OO00OOO0O00OO0O0O ,0 ),O00OOOO00OO00OO00 +OO00OOO0O00OO0O0O +1 )
            OOOOO0OO0O00OO000 =O00OOO000O000OO00 .elastic3D [:-1 ,OO0OO0O0O0OO0000O ,O0O00OOOO0OO0O00O ]
        else :
            OOOOO0OO0O00OO000 =O00OOO000O000OO00 .elastic3D [:-1 ,:,:]
        O0O0OO0O0O0OO0000 =OOOOO0OO0O00OO000 .shape [1 ]*OOOOO0OO0O00OO000 .shape [2 ]
        O0OO0O0OO0000OO0O =np .array (OOOOO0OO0O00OO000 ,dtype =np .float64 ).reshape ((-1 ,O0O0OO0O0O0OO0000 ),order ='F').T
        try :
            O0OO0O0OO0000OO0O *=O00OOO000O000OO00 .i0 .max ()/O00OOO000O000OO00 .i0 [np .newaxis ,:]
        except ValueError as OO00000O0OOOOOO00 :
            print (OO00000O0OOOOOO00 )
            return
        if O0O0O00O00O0000OO ['use2Droi']and O0OOO0O0O0O00OOOO :
            O00OOO0OOO0OOOO0O =O00OOO000O000OO00 .dispersive2D [OO0OO0O0O0OO0000O ,O0O00OOOO0OO0O00O ].reshape ((-1 ,O0O0OO0O0O0OO0000 ),order ='F').T
        else :
            O00OOO0OOO0OOOO0O =O00OOO000O000OO00 .dispersive2D .reshape ((-1 ,O0O0OO0O0O0OO0000 ),order ='F').T
        OO0OOOOO0O0O0O00O =np .dot (O0OO0O0OO0000OO0O .T ,O00OOO0OOO0OOOO0O )
        O00O0O0O0OOO0OOOO =np .dot (OO0OOOOO0O0O0O00O .T ,OO0OOOOO0O0O0O00O )
        O0O000O00000OO00O =dict ()
        OO0OO00O00000O0O0 ,OO0OOO0OOO00OOOO0 =spl .eigh (O00O0O0O0OOO0OOOO ,**O0O000O00000OO00O )
        O0O00000O000OOOOO =np .dot (np .dot (OO0OOO0OOO00OOOO0 ,np .diag (1. /OO0OO00O00000O0O0 )),OO0OOO0OOO00OOOO0 .T )
        OO0O0O0O0O0OOOOOO =np .dot (O0OO0O0OO0000OO0O .T *O0O00000O000OOOOO ,O0OO0O0OO0000OO0O *OO0OO00O00000O0O0 )
        O0O000O00000OO00O =dict ()
        OOOO0OOO0OO0OOO00 ,OO0OOOOO0OO00OO0O =spl .eigh (OO0O0O0O0O0OOOOOO ,**O0O000O00000OO00O )
        O0O0O000O000O000O =O0O0O00O00O0000OO ['cutoffMin']
        OOO0O0OOOOOOO0OO0 =O0O0O00O00O0000OO ['cutoffMax']
        OO0OO0OOOOO00OO0O =OO0OOOOO0OO00OO0O [:,O0O0O000O000O000O :OOO0O0OOOOOOO0OO0 ]
        O000OOOOO0000O000 =np .dot (np .dot (OO0OO0OOOOO00OO0O ,np .diag (1. /OOOO0OOO0OO0OOO00 [O0O0O000O000O000O :OOO0O0OOOOOOO0OO0 ])),OO0OO0OOOOO00OO0O .T )
        OOO0OOO0000OO0OO0 =np .dot (O000OOOOO0000O000 ,OO0OOOOO0O0O0O00O ).ravel ()
        OOO00O000O000OO00 =np .argwhere (OOO0OOO0000OO0OO0 <=0 ).ravel ()
        if len (OOO00O000O000OO00 )>1 :
            OOO0OOO0000OO0OO0 [:OOO00O000O000OO00 [0 ]]=0
            OOO0OOO0000OO0OO0 [OOO00O000O000OO00 [-1 ]:]=0
        OOO0OOO0000OO0OO0 [OOO0OOO0000OO0OO0 <0 ]=0
        OOO0OOO0000OO0OO0 *=O00OOO0OOO0OOOO0O .sum ()/OOO0OOO0000OO0OO0 .sum ()
        O00OOO000O000OO00 .xes =OOO0OOO0000OO0OO0
        if O0O0O00O00O0000OO ['convolve']:
            OO0O00OOOOO0O0OO0 =O00OOO000O000OO00 .energy [1 ]-O00OOO000O000OO00 .energy [0 ]
            OO0O0OO000O0O0OOO =O0O0O00O00O0000OO ['convolveWith']
            if xrt .rc [OO0O0OO000O0O0OOO ]is None :
                O0OOOO0O00O0O0O0O =xrt .crystals [OO0O0OO000O0O0OOO ]
                O0OOOO0O00O00OOO0 =O00OOO000O000OO00 .energy [len (O00OOO000O000OO00 .energy )//2 ]
                O00OOO00OO0OO0O00 =O0OOOO0O00O0O0O0O .get_dtheta_symmetric_Bragg (O0OOOO0O00O00OOO0 )
                OO00000OO00OO0OOO =O0OOOO0O00O0O0O0O .get_Bragg_angle (O0OOOO0O00O00OOO0 )-O00OOO00OO0OO0O00
                OOOO000O00OO0O000 =np .abs (O0OOOO0O00O0O0O0O .get_amplitude (O00OOO000O000OO00 .energy ,np .sin (OO00000OO00OO0OOO ))[0 ])**2
                xrt .refl [OO0O0OO000O0O0OOO ]=OOOO000O00OO0O000
                xrt .rc [OO0O0OO000O0O0OOO ]=np .convolve (OOOO000O00OO0O000 ,OOOO000O00OO0O000 ,'same')/(OOOO000O00OO0O000 .sum ()*OO0O00OOOOO0O0OO0 )*OO0O00OOOOO0O0OO0
            O00OOO000O000OO00 .xes =np .convolve (O00OOO000O000OO00 .xes ,xrt .rc [OO0O0OO000O0O0OOO ],'same')/(xrt .rc [OO0O0OO000O0O0OOO ].sum ()*OO0O00OOOOO0O0OO0 )*OO0O00OOOOO0O0OO0
        return True 
