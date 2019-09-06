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

class Mask:

    def __init__(self, description, element_properties, module, methods):

        self.__description = description
        self.__element_properties = element_properties
        self.__module_index = module
        self.__method_indices = methods

        self.__maximum_label_length = 0

        # For each element add its accessor method and determine the maximum
        # label length for formatting purposes.
        for element in self.__element_properties:

            exec 'def %s(self, value = None): return(self._Mask__element(%d, value))'\
                 % (Utility.buildFunctionName(element['label']),
                    element['index']) in self.__class__.__dict__

            length = len(element['label'])
            
            if (length > self.__maximum_label_length):

                self.__maximum_label_length = length

    def __repr__(self):

        string = ''
        string += 'Description: %s\n' % (self.__description,)
        string += 'Length     : %d\n\n' % (len(self),)

        state = ['Unmasked', 'Masked']

        for element in self.__element_properties:
            
            string += '%-*s: %s\n' % (self.__maximum_label_length,
                                      element['label'],
                                      state[self.__element(element['index'])])
        return(string[:-1])

    def __len__(self): return(len(self.__element_properties))

    def __element(self, index, value = None):

        type = self.__element_properties[index]['type']
        
        Utility.newOperation(self.__module_index,
                             self.__method_indices['maskElement'])

        if (value != None): PyTTXTalk.pushS8(value)

        PyTTXTalk.pushS8(index)
        
        Utility.sendPacket(1)

        if (value == None): return(PyTTXTalk.popS8())

    def maskAll(self):

        for element in self.__element_properties:

            self.__element(element['index'], 1)

    def unmaskAll(self):

        for element in self.__element_properties:

            self.__element(element['index'], 0)            

    def elements(self):
        data = []

        for element in self.__element_properties:
            data.append(self.__element(element['index']))

        return data

    def labels(self):
        data = []

        for element in self.__element_properties:
            data.append(element['label'])

        return data