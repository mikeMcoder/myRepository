'''
NeoPhotonics CONFIDENTIAL
Copyright 2008 NeoPhotonics Corporation All Rights Reserved.

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
    
'''
import PyTTXTalk
import Utility

MODULE_INDEX = 8

METHOD_INDICES = {'status':0,
                  'warning':1,
                  'alarm':2,
                  'mask':3,
                  }

ELEMENT_DATA = ()

ELEMENT_PROPERTIES = []
    
PROPERTIES = {}

class Health:

    def __init__(self):

        self.__dictionary = None
        self.__method_indices = METHOD_INDICES
        self.__module_index = MODULE_INDEX

    def dictionary(self, d = None):

        if (d == None): return(self.__dictionary)

        self.__dictionary = d

    def __repr__(self):
        
        LABELS = ['SLED_TEMPERATURE_LIMIT_EXCEEDED',
                  'FILTER1_TEMPERATURE_LIMIT_EXCEEDED',
                  'FILTER2_TEMPERATURE_LIMIT_EXCEEDED',
                  'FREQUENCY_SHIFT_RANGE_EXCEEDED',
                  'POWER_WARNING',
                  'TEMPERATURE_WARNING',
                  'FREQUENCY_WARNING',
                  'BIAS_CURRENT_WARNING']
        
        s =  'Description: Health Monitor\n'
        s += 'Masked     : %s\n' % (['Yes', 'No'][self.mask() == 0])
        s += 'Violations : '

        value = self.status()

        if ((value & 0xFF) == 0):

            s += 'None'

        else:
            
            for i in range(len(LABELS)):

                if (value & (1 << i)): s += LABELS[i] + ' '

        s += '\nLast Reset : '

        RESET_SRC = ['/RST pin asserted.',
                     'Power-on or VDD monitor reset',
                     'Missing clock detector timeout',
                     'Watchdog timer asserted',
                     'Software reset',
                     'Comparator0 reset',
                     'CNVSTR0 reset']
        if ((value & 0xFF00) == 0):

            s += 'None'

        else:
            
            for i in range(len(RESET_SRC)):

                if (value & (1 << (i + 8))): s += RESET_SRC[i] + ' '
        
        return(s)

    def mask(self, m = None):
        
        Utility.newOperation(self.__module_index,
                             self.__method_indices['mask'])

        if (m != None): PyTTXTalk.pushU8(m)
        
        Utility.sendPacket(1)

        if (m == None): return(PyTTXTalk.popU8())    

    def status(self):
        '''
    Bit n  | Description:
    15     | N/A
    14     | CNVSTR0 reset (latched)
    13     | Comparator0 reset (latched)
    12     | Software reset (latched)
    11     | Watchdog timer asserted (latched)
    10     | Missing clock detector timeout reset (latched)
    09     | Power-on or VDD monitor reset (latched)
    08     | /RST pin asserted (latched)
    07     | N/A
    06     | Bias current warning
    05     | Frequency warning
    04     | Temperature warning
    03     | Power warning
    02     | Filter 2 temperature limit exceede (latched clear on read)
    01     | Filter 1 temperature limit exceede (latched clear on read)
    00     | Sled temperature limit exceeded (latched clear on read)
        '''
        
        Utility.newOperation(self.__module_index,
                             self.__method_indices['status'])

        Utility.sendPacket(1)

        return(PyTTXTalk.popU16())
    

        