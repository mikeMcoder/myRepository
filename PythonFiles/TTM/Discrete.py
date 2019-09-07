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
import Frame
import Mask

MODULE_INDEX = 4

METHOD_INDICES = {'frameElementU16':0,
                  'maskElement':1}

ELEMENT_DATA = (
                'TEC_COOL_CURRENT_LIMIT',
                'SI_BLOCK',
                'TEC_VOLT_LIMIT',
                'FILTER2',
                'TEC',
                'GAIN_MEDIUM',
                'TEC_HOT_CURRENT_LIMIT',
                'FILTER1',
				'SBSS_GAIN', 
                )
ELEMENT_PROPERTIES = []

for index in range(len(ELEMENT_DATA)):

    label = ELEMENT_DATA[index]
    
    ELEMENT_PROPERTIES.append({'index':index,
                               'label':label,
                               'units':'Counts',
                               'type':'U16'})
    
PROPERTIES = {'ELEMENT_PROPERTIES':ELEMENT_PROPERTIES}

class DiscreteStage:

    def __init__(self):

        self.__frame = DiscreteFrame()
        self.__mask = DiscreteMask()
        self.__dictionary = None

    def dictionary(self, d = None):

        if (d == None): return(self.__dictionary)

        self.__dictionary = d

    def frame(self):

        'Returns the discrete frame.'

        return(self.__frame)

    def mask(self):

        'Returns the discrete mask.'

        return(self.__mask)

class DiscreteFrame(Frame.Frame):

    def __init__(self):

        Frame.Frame.__init__(self,
                             'Discrete frame.',
                             PROPERTIES['ELEMENT_PROPERTIES'],
                             MODULE_INDEX,
                             METHOD_INDICES)

class DiscreteMask(Mask.Mask):

    def __init__(self):

        Mask.Mask.__init__(self,
                           'Discrete mask.',
                           PROPERTIES['ELEMENT_PROPERTIES'],
                           MODULE_INDEX,
                           METHOD_INDICES)
