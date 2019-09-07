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

    $Source: /data/development/cvs/Lux/Python/TTM/Frame.py,v $
    $Revision: 1.1 $
    $Date: 2009/01/13 23:59:00 $
    $Name: HEAD $
    
'''
import PyTTXTalk

import Utility

TYPE_FORMATS = {'S8':'%+04d',
                'U8':'%+04d',
                'S16':'%+06d',
                'U16':'%+06d',
                #'U16':'%04X',
                'S32':'%+011d',
                'U32':'%+011d',
                'F32':'%+9.4f'}

class Frame:

    def __init__(self, description, element_properties, module, methods):

        'Base frame class.'

        self.__module_index = module
        self.__method_indices = methods
        self.__description = description
        self.__element_properties = element_properties
        
        # Find longest name and store length.
        self.__maximum_label_length = 0

        for element in self.__element_properties:

            exec 'def %s(self, value = None): return(self._Frame__element(%d, value))'\
                 % (Utility.buildFunctionName(element['label']),
                    element['index']) in self.__class__.__dict__

            length = len(element['label'])
            
            if (length > self.__maximum_label_length):

                self.__maximum_label_length = length

    def __repr__(self):

        string = ''
        string += 'Description: %s\n' % (self.__description,)
        string += 'Length     : %d\n\n' % (len(self),)

        for element in self.__element_properties:

            format_string = '%-*s: ' + TYPE_FORMATS[element['type']] + ' %s\n'
            
            string +=  format_string % (self.__maximum_label_length,
                                        element['label'],
                                        self.__element(element['index']),
                                        element['units'])
        return(string[:-1])

    def __len__(self): return(len(self.__element_properties))

    def __element(self, index, value = None):

        type = self.__element_properties[index]['type']
        
        Utility.newOperation(self.__module_index,
                             self.__method_indices['frameElement' + type])

        if (value != None): exec('PyTTXTalk.push%s(value)' % (type))

        PyTTXTalk.pushS8(index)
        
        Utility.sendPacket(1)

        if (value == None):

            # Reuse 'value'.
            exec('value = PyTTXTalk.pop%s()' % (type))
            return(value)

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