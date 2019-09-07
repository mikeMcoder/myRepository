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

    $Source: /data/development/cvs/Lux/Python/TTM/AmbientCompensator.py,v $
    $Revision: 1.1 $
    $Date: 2009/08/05 23:57:04 $
    $Name: HEAD $

'''
import PyTTXTalk
import Dictionary
from Utility import *

import Mask

MODULE_INDEX = 9

METHOD_INDICES = {'mask':0,
                  'alpha_f1':1,
                  'alpha_f2':2,
                  'alpha_sled':3
                 }


class AmbientCompensator:

    def __init__(self):

        self.__module_index = MODULE_INDEX
        self.__method_indices = METHOD_INDICES
        self.__dictionary = None
        #self.__cavity_locker = CavityLocker()
        #self.__side_mode_balancer = SideModeBalancer()

    def __repr__(self):

        s =  'Description: Ambient Compensator\n'
        s += 'Mask : %s \n' % ['Unmasked', 'Masked'][self.mask()]
        return(s)

    def dictionary(self, d = None):

        if (d == None): return(self.__dictionary)

        self.__dictionary = d

    def mask(self, m = None):
        ' Ambient Compensator. Master enable/disable switch.'

        newOperation(self.__module_index,
                     self.__method_indices['mask'])

        if (m == None):
            sendPacket(1)
            return(PyTTXTalk.popU8())
        else:
            PyTTXTalk.pushU8(m)
            sendPacket(1)

    def alpha_f1(self, m = None):
        ' Ambient Compensator alpha F1.'

        newOperation(self.__module_index,
                     self.__method_indices['alpha_f1'])

        if (m == None):
            sendPacket(1)
            return(PyTTXTalk.popF32())
        else:
            PyTTXTalk.pushF32(m)
            sendPacket(1)

    def alpha_f2(self, m = None):
        ' Ambient Compensator alpha F2.'

        newOperation(self.__module_index,
                     self.__method_indices['alpha_f2'])

        if (m == None):
            sendPacket(1)
            return(PyTTXTalk.popF32())
        else:
            PyTTXTalk.pushF32(m)
            sendPacket(1)

    def alpha_sled(self, m = None):
        ' Ambient Compensator alpha F2.'

        newOperation(self.__module_index,
                     self.__method_indices['alpha_sled'])

        if (m == None):
            sendPacket(1)
            return(PyTTXTalk.popF32())
        else:
            PyTTXTalk.pushF32(m)
            sendPacket(1)

