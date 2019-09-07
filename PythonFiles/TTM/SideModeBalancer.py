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

    $Source: /data/development/cvs/Sundial2/Python/TTX/SideModeBalancer.py,v $
    $Revision: 1.4 $
    $Date: 2007/10/15 16:16:56 $
    $Name: Sundial2_01_03_00_01 $
    
'''
import PyTTXTalk
import Dictionary
from Utility import *

import Mask

MODULE_INDEX = 10

METHOD_INDICES = {'error':0,
                  'iteration':1,
                  'gain':2,
                  'heatDither':3,
                  'real': 4,
                  'imaginary': 5,
                  'mask': 6
                 }


class SideModeBalancer:

    def __init__(self):

        self.__module_index = MODULE_INDEX
        self.__method_indices = METHOD_INDICES
        self.__dictionary = None

    def __repr__(self):

        s =  'Description: Side Mode Balancer\n'
        s += 'Iterations : %d \n' % self.iteration()
        s += 'Error      : %f\n' % self.error()
        s += 'Gain       : %f\n' % self.gain()
        s += 'Heat Dither: %f' % self.heatDither()
        s += 'Real       : %f\n' % self.real()
        s += 'Imaginary  : %f\n' % self.imaginary()
        s += 'Mask : %s \n' % ['Unmasked', 'Masked'][self.mask()]
        return(s)
    
    def dictionary(self, d = None):

        if (d == None): return(self.__dictionary)

        self.__dictionary = d

    def error(self):

        '''
Power error.
        '''

        newOperation(self.__module_index,
                     self.__method_indices['error'])

        sendPacket(1)
        return(PyTTXTalk.popF32())
    def real(self):

        '''
real Power error.
        '''

        newOperation(self.__module_index,
                     self.__method_indices['real'])

        sendPacket(1)
        return(PyTTXTalk.popF32())

    def imaginary(self):

        '''
imaginary Power error.
        '''

        newOperation(self.__module_index,
                     self.__method_indices['imaginary'])

        sendPacket(1)
        return(PyTTXTalk.popF32())



    def iteration(self, i = None):

        '''
Number of iterations to run. U32 value.
        '''

        newOperation(self.__module_index,
                     self.__method_indices['iteration'])

        if (i == None):

            sendPacket(1)
            return(PyTTXTalk.popU32())

        PyTTXTalk.pushU32(i)
        sendPacket(1)
        
        
    def mask(self, i = None):


        newOperation(self.__module_index,
                     self.__method_indices['mask'])

        if (i == None):

            sendPacket(1)
            return(PyTTXTalk.popU32())

        PyTTXTalk.pushU32(i)
        sendPacket(1)
        

    def gain(self, i = None):

        '''
F32 gain used in the filter servo.
        '''

        newOperation(self.__module_index,
                     self.__method_indices['gain'])

        if (i == None):

            sendPacket(1)
            return(PyTTXTalk.popF32())

        PyTTXTalk.pushF32(i)
        sendPacket(1)

    def heatDither(self, i = None):

        '''
F32 gain used in the filter servo.
        '''

        newOperation(self.__module_index,
                     self.__method_indices['heatDither'])

        if (i == None):

            sendPacket(1)
            return(PyTTXTalk.popF32())

        PyTTXTalk.pushF32(i)
        sendPacket(1)
