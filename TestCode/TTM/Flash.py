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

    $Source: /data/development/cvs/Sundial2/Python/TTX/Flash.py,v $
    $Revision: 1.1 $
    $Date: 2007/04/18 19:45:25 $
    $Name: Sundial2_02_01_04_00 $
    
'''
import PyTTXTalk

PAGE_SIZE = 1024

MODULE_INDEX = 1

METHOD_INDICES = {'erasePage':0,
                  'readBytes':1,
                  'writeBytes':2}

PROPERTIES = {'CHUNK_SIZE':32}

from Utility import *

class Flash:

    def __init__(self):

        self.__module_index = MODULE_INDEX
        self.__method_indices = METHOD_INDICES

    def erasePage(self, page_number):

        newOperation(self.__module_index, self.__method_indices['erasePage'])
        PyTTXTalk.pushU16(page_number);
        sendPacket(1);

    def write(self, address, bytes):

        CHUNK_SIZE = PROPERTIES['CHUNK_SIZE']

        while (len(bytes) != 0):
            
            # Grab up to 'chunk size' worth of bytes.
            chunk = bytes[:CHUNK_SIZE]
            bytes = bytes[CHUNK_SIZE:]
        
            newOperation(self.__module_index,
                         self.__method_indices['writeBytes'])


            # Reverse the string to place on the packet stack.
            chunk = list(chunk)
            chunk.reverse()
            chunk = ''.join(chunk)

            for byte in chunk: PyTTXTalk.pushU8(ord(byte))
            
            PyTTXTalk.pushU32(address)
            sendPacket(1);

            address += len(chunk)

    def read(self, address, count):

        CHUNK_SIZE = PROPERTIES['CHUNK_SIZE']

        data = []

        while (count > 0):

            subcount = CHUNK_SIZE

            if (count < subcount): subcount = count

            newOperation(self.__module_index,
                         self.__method_indices['readBytes'])
            PyTTXTalk.pushU8(subcount)
            PyTTXTalk.pushU32(address)
            sendPacket(1);

            address += subcount
            count -= subcount

            subdata = []
            
            while (subcount > 0):

                subdata.append(chr(PyTTXTalk.popU8()))
                subcount -= 1

            subdata.reverse()

            data.extend(subdata)
            
        return(''.join(data))
