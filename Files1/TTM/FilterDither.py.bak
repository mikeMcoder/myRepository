'''
NeoPhotonics CONFIDENTIAL
Copyright 2003, 2004 NeoPhotonics Corporation All Rights Reserved.

The source code contained or described herein and all documents related to
the source code ("Material") are owned by NeoPhotonics Corporation or its
suppliers or licensors. Title to the Material remains with NeoPhotonics Corporation
or its suppliers and licensors. The Material may contain trade secrets and
proprietary and confidential information of NeoPhotonics Corporation and its
suppliers and licensors, and is protected by worldwide copyright and trade
secret laws and treaty provisions. No part of the Material may be used, copied,
reproduced, modified, published, uploaded, posted, transmitted, distributed,
or disclosed in any way without NeoPhotonics's prior express written permission.
No license under any patent, copyright, trade secret or other intellectual
property right is granted to or conferred upon you by disclosure or delivery
of the Materials, either expressly, by implication, inducement, estoppel or
otherwise. Any license under such intellectual property rights must be express
and approved by NeoPhotonics in writing.

Include any supplier copyright notices as supplier requires NeoPhotonics to use.

Include supplier trademarks or logos as supplier requires NeoPhotonics to use,
preceded by an asterisk. An asterisked footnote can be added as follows:
*Third Party trademarks are the property of their respective owners.

Unless otherwise agreed by NeoPhotonics in writing, you may not remove or alter this
notice or any other notice embedded in Materials by NeoPhotonics or NeoPhotonics's
suppliers or licensors in any way.

    $Source: /data/development/cvs/Lux/Python/TTM/FilterDither.py,v $
    $Revision: 1.5 $
    $Date: 2009/11/02 22:02:29 $
    $Name: HEAD $

'''
import PyTTXTalk
import Dictionary
from Utility import *

import Mask

MODULE_INDEX = 6

METHOD_INDICES = {'mask':0,
                  'cavity_locker_mask':1,
                  'cavity_locker_error':2,
                  'smb_mask':3,
                  'smb_error':4,
                  'cavity_variance':5,
                  'cavity_is_locked':6
                 }

class FilterDither:

    def __init__(self):

        self.__module_index = MODULE_INDEX
        self.__method_indices = METHOD_INDICES
        self.__dictionary = None
        self.__cavity_locker = CavityLocker()
        self.__side_mode_balancer = SideModeBalancer()

    def __repr__(self):

        s =  'Description: Filter Dither\n'
        s += 'Mask : %s \n' % ['Unmasked', 'Masked'][self.mask()]
        return(s)

    def dictionary(self, d = None):

        if (d == None): return(self.__dictionary)

        self.__dictionary = d

    def mask(self, m = None):
        ' Filter Dither. Master enable/disable switch.'

        newOperation(self.__module_index,
                     self.__method_indices['mask'])

        if (m == None):
            sendPacket(1)
            return(PyTTXTalk.popU8())
        else:
            PyTTXTalk.pushU8(m)
            sendPacket(1)

    def cavityLocker(self):
        'Returns the cavity locker object'
        return (self.__cavity_locker)

    def sideModeBalancer(self):
        'Returns the side mode balancer object'
        return (self.__side_mode_balancer)


class SideModeBalancer:
    def __init__(self):

        self.__module_index = MODULE_INDEX
        self.__method_indices = METHOD_INDICES

    def error(self):

        newOperation(self.__module_index,
                     self.__method_indices['smb_error'])

        sendPacket(1)
        return(PyTTXTalk.popF32())

    def mask(self, i = None):
        'Enable/disable SMB separately from filter dither.'

        newOperation(self.__module_index,
                     self.__method_indices['smb_mask'])

        if (i == None):

            sendPacket(1)
            return(PyTTXTalk.popU8())

        PyTTXTalk.pushU8(i)
        sendPacket(1)

    '''def gain(self, i = None):
        'F32 gain used in the filter servo.        '

        newOperation(self.__module_index,
                     self.__method_indices['smb_gain'])

        if (i == None):

            sendPacket(1)
            return(PyTTXTalk.popF32())

        PyTTXTalk.pushF32(i)
        sendPacket(1)'''

class CavityLocker:
    def __init__(self):

        self.__module_index = MODULE_INDEX
        self.__method_indices = METHOD_INDICES

    def error(self):

        newOperation(self.__module_index,
                     self.__method_indices['cavity_locker_error'])

        sendPacket(1)
        return(PyTTXTalk.popF32())

    def mask(self, i = None):
        'Enable/disable Cavity Locker'

        newOperation(self.__module_index,
                     self.__method_indices['cavity_locker_mask'])

        if (i == None):

            sendPacket(1)
            return(PyTTXTalk.popU8())

        PyTTXTalk.pushU8(i)
        sendPacket(1)


    def variance(self):
        'Cavity variance'

        newOperation(self.__module_index,
                     self.__method_indices['cavity_variance'])

        sendPacket(1)
        return(PyTTXTalk.popF32())


    def isLocked(self):
        'Cavity locked status'

        newOperation(self.__module_index,
                     self.__method_indices['cavity_is_locked'])

        sendPacket(1)
        return(PyTTXTalk.popU8())


    '''def heatDitherAmplitude(self, i = None):
        'F32 gain used in the filter servo.'

        newOperation(self.__module_index,
                     self.__method_indices['heat_dither_amplitude'])

        if (i == None):

            sendPacket(1)
            return(PyTTXTalk.popF32())

        PyTTXTalk.pushF32(i)
        sendPacket(1)

    def heatDitherScale(self, i = None):
        'F32 gain used in the filter servo.'

        newOperation(self.__module_index,
                     self.__method_indices['heat_dither_scale'])

        if (i == None):

            sendPacket(1)
            return(PyTTXTalk.popF32())

        PyTTXTalk.pushF32(i)
        sendPacket(1)

    def gain(self, i = None):
        'F32 gain used in the filter servo.        '

        newOperation(self.__module_index,
                     self.__method_indices['cavity_gain'])

        if (i == None):

            sendPacket(1)
            return(PyTTXTalk.popF32())

        PyTTXTalk.pushF32(i)
        sendPacket(1)'''