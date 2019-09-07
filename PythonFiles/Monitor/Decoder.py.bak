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

    $Source: /data/development/cvs/Sundial2/Python/Monitor/Decoder.py,v $
    $Revision: 1.1 $
    $Date: 2007/04/18 19:45:18 $
    $Name: Sundial2_02_01_04_00 $
    
'''
import sys

TOKENS = {'START'  : 0,
          'STOP'   : 1,
          'VERSION': 2,
          'ADDRESS': 3,
          'DATA'   : 4,
          'CRC'    : 5 } # Monitor:

class Decoder:

    def __init__(self, filename = None):

        self.__state = self.stateToken 
        self.__token = None; 
        self.__count = 0;
        self.__address = 0;
        self.__version = 0;
        # Monitor:
        self.__crc = 0;
        
        if (filename == None):

            self.__output = sys.stdout

        else:

            self.__output = open(filename, 'wb')


    def transfer(self, byte):

        self.__state(byte)

        self.__output.flush()

    def stateComplete(self, byte):

        self.__state = self.stateError

    def stateToken(self, byte):

        if (byte < len(TOKENS)):

            self.__state = self.stateCount

        else:

            self.__state = self.stateError
            
        if ((self.__token == None) and (byte != TOKENS['START'])): 
        
            self.__state = self.stateError

        self.__token = 'INVALID'

        for key, value in TOKENS.items():

            if (byte == value): self.__token = key

        self.__output.write('Token: %s Byte: 0x%02X\n' % (self.__token, byte))

    def stateCount(self, byte):

        if ((self.__token == 'VERSION') or (self.__token == 'ADDRESS')):

            if (byte == 4):

                self.__state = self.stateProcess

            else:

                self.__state = self.stateError

            self.__address = 0

        elif (self.__token == 'STOP'):

            if (byte == 0):

                self.__state = self.stateComplete

            else:

                self.__state = self.stateError

        elif (self.__token == 'START'):

            if (byte == 0):

                self.__state = self.stateToken

            else:

                self.__state = self.stateError

        elif (self.__token == 'DATA'):

            self.__state = self.stateProcess

        # Monitor: Add entire elif block.

        elif (self.__token == 'CRC'):

            if (byte == 2):

                self.__state = self.stateProcess

            else:

                self.__state = self.stateError

            self.__crc = 0

        else:

            self.__state = self.stateError

                    
        self.__count = byte

        self.__output.write('Count: %d\n' % (self.__count))

    def stateProcess(self, byte):

        self.__count -= 1

        if (self.__count == 0): self.__state = self.stateToken

        if (self.__token == 'VERSION'):

            self.__version |= byte << ((3 - self.__count) << 3);

            self.__output.write('Version Byte: 0x%02X\n' % (byte))

            if (self.__count == 0):
                
                self.__output.write('Version: 0x%08X\n' % (self.__version))

        elif (self.__token == 'ADDRESS'):

            # The bytes come in little endian so as count goes
            # through 3, 2, 1, 0 the byte is shifted 0, 8, 16, 24.
            # The left shift is the multiply by eight.
            self.__address |= byte << (self.__count << 3);

            self.__output.write('Address Byte: 0x%02X\n' % (byte))

            if (self.__count == 0):
                
                self.__output.write('Address: 0x%08X\n' % (self.__address))

        # Monitor: Add the elif block.

        elif (self.__token == 'CRC'):

            # The bytes come in big endian so as count goes through 1 and 0
            # the byte is shifted 8 and 0.
            self.__crc |= byte << (self.__count * 8);

            self.__output.write('CRC Byte: 0x%02X\n' % (byte))

            if (self.__count == 0):
                
                self.__output.write('CRC: 0x%04X\n' % (self.__crc))

        elif (self.__token == 'DATA'):

            self.__output.write('Write: 0x%02X Count: %03d\n' \
                                % (byte, self.__count))

        else:

            self.__output.write('Process: %s\n' % (self.__token))

    def stateError(self, byte):

        # Errors latch.
        self.__output.write('Latched error.\n')
