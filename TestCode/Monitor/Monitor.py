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
import shelve
import struct

import MemoryMap
import TTM.Dictionary
import TTM.System

DICTIONARY_SIZE             = MemoryMap.DICTIONARY_SIZE
DICTIONARY_ADDRESS          = MemoryMap.MONITOR_DICTIONARY_LOCATION.address()
DICTIONARY_FLASH_ADDRESS    = MemoryMap.MONITOR_DICTIONARY_LOCATION.location()
DICTIONARY_PAGE_NUMBER      = MemoryMap.MONITOR_DICTIONARY_LOCATION.page()

CODE_ADDRESS                = MemoryMap.MONITOR_CODE_LOCATION.address()

class Monitor:
    VERSION_FLASH_ADDRESS = 0x18800
    VERSION_LENGTH = 3 # bytes
    
    # Monitor can not exist alone
    # Must co-exist with TTX, thus requiring a initialization parameter
    def __init__(self):
        self.__flash = TTM.Flash.Flash()
        self.__bridge_path = TTM.System.bridgePath(self.version())
        shelf = shelve.open(self.__bridge_path + '\\Monitor.shelf', 'r')
        self.__dictionary = shelf[TTM.Dictionary.DictionaryManager.ROOT_DICTIONARY_KEY]
        shelf.close()
        self.restore()

    def __repr__(self):
        text  = 'Description: Firmware Upgrade Monitor\n\n'
        text += 'Version    : %s\n' % str(self.version())
        return text
    
    def version(self):
        'Return version object'
        text = self.__flash.read(Monitor.VERSION_FLASH_ADDRESS, Monitor.VERSION_LENGTH)
        major, minor, patch = struct.unpack('BBB', text)
        version = TTM.System.Version()
        version.name('Monitor')
        version.major(major)
        version.minor(minor)
        version.patch(patch)
        version.build(0)
        return version

    def dictionary(self):
        'Return dictionary object'
        return self.__dictionary
    
    def restore(self, kv = None):
        'Restore from laser or kv file to memory'
        if kv == None:
            text = self.__flash.read(DICTIONARY_FLASH_ADDRESS, DICTIONARY_SIZE)
            memory = TTM.Memory.Memory(DICTIONARY_ADDRESS, text)
            self.__dictionary.memory(memory)
        else:
            self.__dictionary.restore(kv)

    def save(self, kv = None):
        'Save from memory to laser to kv file'
        if kv == None:
            self.__flash.erasePage(DICTIONARY_PAGE_NUMBER)
            text = self.__dictionary.memory().read(DICTIONARY_ADDRESS, DICTIONARY_SIZE)
            self.__flash.write(DICTIONARY_FLASH_ADDRESS, text)
        else:
            self.__dictionary.save(kv)
    