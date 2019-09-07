'''
NeoPhotonics CONFIDENTIAL
Copyright 2005-2015 NeoPhotonics Corporation All Rights Reserved.

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

    $Source: /data/development/cvs/Sundial2/Python/Monitor/Verifier.py,v $
    $Revision: 1.1 $
    $Date: 2007/04/18 19:45:18 $
    $Name: Sundial2_02_01_04_00 $
    
'''
import sys

import TTX.Memory

from Monitor.MemoryMap import *

VERIFICATION_COUNT = 10
MAP_SIZE_MASK = 0x3F
MAP_TERMINATOR = 0x0000

# For simulation we will update directly to flash (rather than RAM).
NEW_DICTIONARY_LOCATION = DICTIONARY_LOCATION

class Verifier:

    def __init__(self):

        self.__current_map = None
        self.__new_map = None
        self.__new_element = TTX.Memory.U16()
        self.__current_element = TTX.Memory.U16()

        self.__hex_filenames = ()
        self.__output_filename = None
        self.__counter = 0
        self.__flash = None
        self.__output = None

    def __repr__(self):

        s = ''

        for i in range(len(self.__hex_filenames)):

            s += 'HEX File %d: %s\n' % (i, self.__hex_filenames[i])

        return(s)

    def hexFilenames(self, names = None):

        '''
A tuple of HEX filenames.
        '''

        if (names == None): return(self.__hex_filenames)

        self.__hex_filenames = names

    def outputFilename(self, name = None):

        if (name == None): return(self.__output_filename)

        self.__output_filename = name

    def initialize(self):

        if (self.__output_filename == None):

            self.__output = sys.stdout

        else:

            self.__output = open(self.__output_filename, 'wb')

        output = self.__output

        output.write('Initializing.\n')

        self.__flash = TTX.Memory.Memory(0x0000, '\xFF' * CODE_SPACE_SIZE)

        for filename in self.__hex_filenames:

            file = open(filename, 'rb')

            text = file.read()

            file.close()

            self.__flash.text('HEX', text)

        self.__new_element.memory(self.__flash)
        self.__current_element.memory(self.__flash)

        self.__current_map = CURRENT_MAP_LOCATION.address()
        self.__new_map = NEW_MAP_LOCATION.address()

        # Read the first element of the new map and increment the pointer.
        #flashRead(_new_map, &_new_element, sizeof(_new_element)); 
        self.__new_element.address(self.__new_map)
        self.__new_map += self.__new_element.size()

        output.write('First new element: %s\n' % (hex(self.__new_element)))

        # Initialize dictionary pointers.
        self.__current_dictionary = CURRENT_DICTIONARY_LOCATION.address()
        #_new_dictionary = (U8 xdata *)NEW_DICTIONARY_ADDRESS;
        # Replace dictionary in 'flash' rather than in RAM.
        self.__new_dictionary = NEW_DICTIONARY_LOCATION.address()

        self.__state = self.verifyState;

        self.__counter = VERIFICATION_COUNT;

    def service(self):

        '''
Return True if complete, False otherwise.
        '''

        return(self.__state())

    def verifyState(self):

        output = self.__output

        while (self.__counter):

            self.__counter -= 1

            # Read the next element from the current map.
            self.__current_element.address(self.__current_map)
            self.__current_map += self.__current_element.size()

            current_size = self.__current_element.value() & MAP_SIZE_MASK

            output.write('Current element: %s size: %d\n' % \
                         (hex(self.__current_element), current_size))

            if ((self.__new_element.value() == self.__current_element.value()) or (self.__current_element == MAP_TERMINATOR)):

                # A match was found or the search for a match in current map is
                # exhausted for this element of the new dictionary map. These
                # conditions are handled in exactly the same way except that
                # data is copied to the new dictionary when a match is found.

                if (self.__new_element.value() == \
                    self.__current_element.value()):

                    output.write('Updating new dictionary.\n')
                    # Overwrite the newly uploaded dictionary value with its
                    # match from the current dictionary. 
                    text = self.__flash.read(self.__current_dictionary,
                                             current_size)

                    self.__flash.write(self.__new_dictionary, text)

                # Reset the current pointers.
                self.__current_dictionary = \
                                CURRENT_DICTIONARY_LOCATION.address()

                self.__current_map = CURRENT_MAP_LOCATION.address()

                # Increment the new dictionary pointer and read the next map
                # element. 
                # FIX: Reuse current_size as they match.
                self.__new_dictionary += current_size 
                self.__new_element.address(self.__new_map)
                self.__new_map += self.__new_element.size()

                break

            # Continue stepping through the current dictionary searching for a
            # replace of the new dictionary element. 

            self.__current_dictionary += current_size;

        # Reload counter.
        self.__counter = VERIFICATION_COUNT;

        if (self.__new_element.value() == MAP_TERMINATOR):

            return(True)

            self.__state = self.copyState;

        return(False)
