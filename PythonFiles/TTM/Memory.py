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
No license under any patent, copyright, trade secret or other Emcorelectual
property right is granted to or conferred upon you by disclosure or delivery
of the Materials, either expressly, by implication, inducement, estoppel or
otherwise. Any license under such Emcorelectual property rights must be express
and approved by NeoPhotonics in writing.

Include any supplier copyright notices as supplier requires NeoPhotonics to use.

Include supplier trademarks or logos as supplier requires NeoPhotonics to use,
preceded by an asterisk. An asterisked footnote can be added as follows:
*Third Party trademarks are the property of their respective owners.

Unless otherwise agreed by NeoPhotonics in writing, you may not remove or alter this
notice or any other notice embedded in Materials by NeoPhotonics or NeoPhotonics's
suppliers or licensors in any way.

    $Source: /data/development/cvs/Lux/Python/TTM/Memory.py,v $
    $Revision: 1.1 $
    $Date: 2009/01/17 01:31:02 $
    $Name: HEAD $
    
'''
from __future__ import generators

import exceptions
import math
import struct
import types
import HEX
import CRC16
import zlib
from datetime import datetime

DEBUG_MEM = 0
def DebugOut(s):
    if DEBUG_MEM:
        print s

class Memory:

    def __init__(self, address, data, description = 'Generic memory.'):
        DebugOut('Memory.__init__(%s, data, %s)' % (address, description))
        
        self.__description = description
        self.__address = address

        if (type(data) != types.StringType):

            raise exceptions.TypeError('Data must be a string.')

        self.__data = list(data)

    def __len__(self):
        DebugOut('Memory.__len__()')
        
        return(len(self.__data))

    def __repr__(self):
        DebugOut('Memory.__repr__()')

        CHUNK_SIZE = 8

        s =  'Description: ' + self.__description + '\n'
        s += 'Size       : %d\n\n' % (len(self))

        address = 0
        
        for chunk in self.dataGenerator(self.__address, CHUNK_SIZE):

            s += '0x%04X: ' % (self.__address + address)
            for byte in chunk: s += '0x%02X ' % (ord(byte))
            s += '\n'

            address += CHUNK_SIZE
            
        return(s[:-1])

    def address(self):
        DebugOut('Memory.address() = %s' % (self.__address))
        return(self.__address)

    def dataGenerator(self, address, chunk_size):
        DebugOut('Memory.dataGenerator(%s, %s)' % (address, chunk_size))
        offset = address - self.__address

        if ((offset >= len(self)) or (offset < 0)):

            raise exceptions.ValueError('Request is not within memory boundary.')

        for index in range(offset, len(self), chunk_size):

            slice = self.__data[index : index + chunk_size]
            #DebugOut('Memory.dataGenerator slice (%s)' % (str(slice)))
            yield(''.join(slice))

    def description(self, d = None):
        DebugOut('Memory.description(%s)' % (d))
        if (d == None): return(self.__description)

        self.__description = d

    def read(self, address, count):
        DebugOut('Memory.read(%s, %s)' % (address, count))
        
        'Returns a string representation of the requested bytes.'

        offset = address - self.__address
        DebugOut('Memory.read: offset = %s' % (offset))
        DebugOut('Memory.read: self.__address = %s' % (self.__address))

        if (((offset + count - 1) >= len(self)) or (offset < 0)):
            print 'len(self):', len(self), ', offset:0x', hex(offset), ',count:', count
            raise exceptions.ValueError('Request is not within memory boundary.')

        return(''.join(self.__data[offset : offset + count]))

    def write(self, address, data):
        DebugOut('Memory.write(%s, data)' % (address))
        
        'Arguments are the address and a string.'

        if (type(data) != types.StringType):

            raise exceptions.TypeError('Data must be a string.')

        offset = address - self.__address

        DebugOut( 'self.__address: %s' % self.__address )
        DebugOut( 'offset: %s' % offset )
        DebugOut( 'len(data): %s' % len(data))
        #DebugOut( 'len(self): %s' % len(self))
        
        if (((offset + len(data) - 1) >= len(self)) or (offset < 0)):
            raise exceptions.ValueError('Request is not within memory boundary.')

        self.__data[offset : offset + len(data)] = list(data)


    def computeAndWriteAppCheckSum(self):
        DebugOut( 'Memory.computeAndWriteAppCheckSum' )        

        #Create code buffer [0 - 0x3FF] and [0xA00 - 0xFFD] 
        codebuff = self.__data[0 : 0x400]
        codebuff += self.__data[0xA00 : 0xFFFE]

        #Compute Checksum [0 - 0x3FF] and [0xA00 - 0xFFD]
        nCRC16val = CRC16.computeCRC(0xFFFF, codebuff, len(codebuff))

        DebugOut( 'Memory.computeAndWriteAppCheckSum: nCRC16val = %s' % (nCRC16val) )   

        #Write checksum back into memory location
        LoCRC = nCRC16val & 0xFF
        HiCRC = (nCRC16val >> 8) & 0xFF
        
        self.__data[0xFFFE] = chr(HiCRC)
        self.__data[0xFFFF] = chr(LoCRC)

    def computeAndWriteAppCheckSumBin(self, version_tuple, destinationfilename = 'Output\code.bin'):
        DebugOut( 'Memory.computeAndWriteAppCheckSum' )
        FW_CRC32_LOCATION = 0x0
        FW_SIZE_LOCATION  = 0x4
        FW_DATE_LOCATION  = 0xC
        FW_VERSION_LOCATION  = 0x8
        FW_CRC16_LOCATION = 0x1C
        FW_CODE_LOCATION  = 0x20
        
        FW_size = len(self.__data)-FW_CODE_LOCATION
        FW_version = filter
        FW_date = int((datetime.now() - datetime(1970,1,1)).total_seconds())

        #Write code size
        self.__data[FW_SIZE_LOCATION+3] = chr((FW_size >> 24) & 0xFF)
        self.__data[FW_SIZE_LOCATION+2] = chr((FW_size >> 16) & 0xFF)
        self.__data[FW_SIZE_LOCATION+1] = chr((FW_size >> 8) & 0xFF)
        self.__data[FW_SIZE_LOCATION]   = chr(FW_size & 0xFF)

        #Write code date
        self.__data[FW_DATE_LOCATION+3] = chr((FW_date >> 24) & 0xFF)
        self.__data[FW_DATE_LOCATION+2] = chr((FW_date  >> 16) & 0xFF)
        self.__data[FW_DATE_LOCATION+1] = chr((FW_date  >> 8) & 0xFF)
        self.__data[FW_DATE_LOCATION]   = chr(FW_date  & 0xFF)

        #Write code version
        print 'ver: ', version_tuple
        self.__data[FW_VERSION_LOCATION+3] = chr(version_tuple[3])
        self.__data[FW_VERSION_LOCATION+2] = chr(version_tuple[2])
        self.__data[FW_VERSION_LOCATION+1] = chr(version_tuple[1])
        self.__data[FW_VERSION_LOCATION]   = chr(version_tuple[0])
        
        # Compute Checksum 
        codebuff = self.__data[FW_CODE_LOCATION : len(self.__data)]
        nCRC16val = CRC16.computeCRC(0xFFFF, codebuff, len(codebuff))
        
        # Write checksum back into memory location little endian
        self.__data[FW_CRC16_LOCATION+1] = chr((nCRC16val >> 8) & 0xFF)
        self.__data[FW_CRC16_LOCATION]   = chr(nCRC16val & 0xFF)

        # calculate CRC32 starting after the CRC32 value to the end of the code
        codebuff = self.__data[FW_SIZE_LOCATION : len(self.__data)]
        codebuffstr = ''.join(codebuff)
        FW_crc32 = zlib.crc32(codebuffstr)
        
        print 'Code sz: ', hex(FW_size), 'crc16: ', hex(nCRC16val)
        print 'date: ', '0x{:08x}'.format(FW_date)
        print 'CRC32: ', '0x{:08x}'.format(FW_crc32 & 0xFFFFFFFF), 'size', FW_size, 'sz2 ',len(codebuff)

        # Write code CRC32
        self.__data[FW_CRC32_LOCATION+3] = chr((FW_crc32 >> 24) & 0xFF)
        self.__data[FW_CRC32_LOCATION+2] = chr((FW_crc32 >> 16) & 0xFF)
        self.__data[FW_CRC32_LOCATION+1] = chr((FW_crc32 >> 8) & 0xFF)
        self.__data[FW_CRC32_LOCATION]   = chr(FW_crc32 & 0xFF)

        codeHeaderstr = ''.join(self.__data)
        file = open(destinationfilename, 'wb')
        file.write(codeHeaderstr)
        file.close()

    def hex(self, text = None):
        DebugOut( 'Memory.hex %s' % text )
        
        record = HEX.Record()

        if (text == None):

            CHUNK_SIZE = 0x10

            record.type('DATA')

            text = ''

            # Export.
            address = self.address() 
            for chunk in self.dataGenerator(self.__address, CHUNK_SIZE):
        
                record.address(address)
                record.data(chunk)

                text += record.text() + '\n'

                address += CHUNK_SIZE

                #DebugOut( 'Memory.hex EXPORT:  address = %s' % str(address) )
                #DebugOut( 'Memory.hex EXPORT:  chunk = %s' % str(chunk) )
                #DebugOut( 'Memory.hex EXPORT:  text = %s' % text )

            record.type('EOF')

            text += record.text() + '\n'

            return(text)

        # Import.

        for line in text.split('\n'):
            #DebugOut('Memory.hex line (%s)' % (line))

            if (line.startswith(':') == False): continue

            record.text(line.strip())

            if (record.type() == 'EOF'): return

            # Raise an exception if not a data record. 
            ['DATA'].index(record.type())

            self.write(record.address(), record.data())

    ## NOT CALLED
    def ray(self, major, minor, bug, type, text = None):
        print 'Memory.ray', major, minor, bug, type, text
        
        TOKEN_START   = 0
        TOKEN_STOP    = 1
        TOKEN_VERSION = 2
        TOKEN_ADDRESS = 3
        TOKEN_DATA    = 4

        assert (text == None), 'Import not yet supported.'

        if (text == None):

            # Export.

            text = ''

            # Start record.

            for i in (TOKEN_START, 0):

                text += chr(i)

            # Version record: Major, Minor, Bug, FirmwareType
            tokens = [TOKEN_VERSION, 4, major, minor, bug, type]
            
            for i in tokens:

                text += chr(i) 

            # Largest 8-bit number.
            CHUNK_SIZE = 255 

            # Export.
            address = self.address() 

            for chunk in self.dataGenerator(self.__address, CHUNK_SIZE):

                # Address record.
                for i in (TOKEN_ADDRESS, 4):

                    text += chr(i)
 
                # Write 4 bytes of 32-bit address in big-endian.
                text += struct.pack('>I', address)

                for i in (TOKEN_DATA, len(chunk)):

                    text += chr(i)

                text += chunk

                address += CHUNK_SIZE

            for i in (TOKEN_STOP, 0):

                text += chr(i) 

            return(text)


# Defined so that objects may initialize memories to something real.
DEFAULT_MEMORY = Memory(0, '', 'Default memory.')

class Object:

    def __hex__(self): raise exceptions.NotImplementedError('Abstract class.')

    def __init__(self):
        DebugOut('Object.__init__()')

        self.__address = 0
        self.__description = ''
        self.__memory = DEFAULT_MEMORY
        self.__size = 0

    def __repr__(self):
        DebugOut('Object.__repr__()')

        s = ''
        s += 'Description: %s\n' % (self.description())
        s += 'Memory     : %s\n' % (self.memory().description())
        s += 'Address    : 0x%08X\n' % (self.address())
        s += 'Size       : %d' % (self.size())
        return(s)

    def __str__(self): raise exceptions.NotImplementedError('Abstract class.')

    def address(self, a = None):
        DebugOut('Object.address(%s)' % (a))
        
        if (a == None): return(self.__address)

        self.__address = a

    def description(self, d = None):
        DebugOut('Object.description(%s)' % (d))
        
        if (d == None): return(self.__description)

        self.__description = d

    def memory(self, m = None):
        DebugOut('Object.memory(%s)' % (m))

        if (m == None): return(self.__memory)

        self.__memory = m

    def size(self, s = None):
        DebugOut('Object.size(%s)' % (s))

        if (s == None): return(self.__size)

        self.__size = s

class ValueObject(Object):
    
    def __init__(self):
        DebugOut('ValueObject.__init__()')
        
        Object.__init__(self)

    def __repr__(self):
        DebugOut('ValueObject.__repr__()')
        
        s = ''
        s += 'Description: %s\n' % (self.description())
        s += 'Memory     : %s\n' % (self.memory().description())
        s += 'Address    : 0x%08X\n' % (self.address())
        s += 'Size       : %d\n' % (self.size())
        s += 'Value      : %s' % str(self)
        return(s)

    def value(self):
        DebugOut('ValueObject.value()')        
        return(0)

class Character(ValueObject):

    def __init__(self):
        DebugOut('Character.__init__()')  
        Object.__init__(self)
        self.size(1)
        self.description('8-bit ASCII Character.')

    def value(self, v = None):
        DebugOut('Character.value(%s)' % (v))
        
        if (v == None):

            return(self.memory().read(self.address(), self.size()))

        self.memory().write(self.address(), v)

    def __str__(self):
        DebugOut('Character.__str__()')
        
        c = self.value()

        if (c.isalnum() == True): return(c)

        return('\\x%02X' % (ord(c)))

class CValueObject(ValueObject):

    def __init__(self):
        DebugOut('CValueObject.__init__()')
        
        ValueObject.__init__(self)

        self.__format_string = ''

    def __str__(self): raise exceptions.NotImplementedError('Abstract class.')

    def formatString(self, s = None):
        DebugOut('CValueObject.formatString(%s)' % (s))

        if (s == None): return(self.__format_string)

        self.__format_string = s

    def value(self, v = None):
        DebugOut('CValueObject.value(%s)' % (v))

        if (v == None):

            return(struct.unpack(self.formatString(),
                                 self.memory().read(self.address(),
                                                    self.size()))[0])

        self.memory().write(self.address(),
                            struct.pack(self.formatString(), v))

class F32(CValueObject):

    def __init__(self):
        DebugOut('F32.__init__()')
        CValueObject.__init__(self)

        self.description('32-bit IEEE floating-point number.')
        #the format '>f' indicate ">" big endian and "f", float, 32 bit (4 bytes)
        self.formatString('>f')
        self.size(4)

    def __str__(self):

        '''
Yeilds a %f like format but guarantees 8 significant digits.
        '''

        f = self.value()

        if not (-1e1000000 < f < 1e1000000):
            return("float('nan')")

        if (f == 0.0): return('+0.0')
        
        x = int(math.log10(math.fabs(f))) + 1

        if (x > 0): return('%+10.*f' % (8 - x, f))

        return('%+0.*f' % (8 - x, f))

class S8(CValueObject):

    def __hex__(self):
        DebugOut('S8.__hex__()')
        return('0x%02X' % (self.value(),))

    def __init__(self):
        DebugOut('S8.__init__()')
        CValueObject.__init__(self)

        self.description('Signed 8-bit value.')
        self.formatString('b')
        self.size(1)

    def __str__(self):
        DebugOut('S8.__str__()')
        return('%+d' % (self.value(),))

class U8(CValueObject):

    def __hex__(self):
        DebugOut('U8.__hex__()')
        return('0x%02X' % (self.value(),))

    def __init__(self):
        DebugOut('U8.__init__()')
        CValueObject.__init__(self)

        self.description('Unsigned 8-bit value.')
        self.formatString('B')
        self.size(1)

    def __str__(self): return('%+d' % (self.value(),))

class S16(CValueObject):

    def __hex__(self):
        DebugOut('S16.__hex__()')
        return('0x%04X' % (self.value(),))

    def __init__(self):
        DebugOut('S16.__init__()')
        CValueObject.__init__(self)

        self.description('Signed 16-bit value.')
        self.formatString('>h')
        self.size(2)

    def __str__(self):
        DebugOut('S16.__str__()')
        return('%+d' % (self.value(),))

class U16(CValueObject):

    def __hex__(self):
        DebugOut('U16.__hex__()')
        return('0x%04X' % (self.value(),))

    def __init__(self):
        DebugOut('U16.__init__()')
        CValueObject.__init__(self)

        self.description('Unsigned 16-bit value.')
        self.formatString('>H')
        self.size(2)

    def __str__(self):
        DebugOut('U16.__str__()')
        return('%+d' % (self.value(),))

class S32(CValueObject):

    def __hex__(self):
        DebugOut('S32.__hex__()')
        return('0x%08X' % (self.value(),))

    def __init__(self):
        DebugOut('S32.__init__()')
        CValueObject.__init__(self)

        self.description('Signed 32-bit value.')
        self.formatString('>i')
        self.size(4)

    def __str__(self):
        DebugOut('S32.__str__()')
        return('%+d' % (self.value(),))

class U32(CValueObject):

    def __hex__(self):

        return('0x%08X' % (self.value(),))

    def __init__(self):

        CValueObject.__init__(self)

        self.description('Unsigned 32-bit value.')
        self.formatString('>I')
        self.size(4)

    def __str__(self): return('%+d' % (self.value(),))

class String(Object):

    '''
Fixed length string. String can be up to MAXIMUM_SIZE in length including the
terminating null character.

Strings will be truncated if they exceed the MAXIMUM_SIZE.
    '''

    MAXIMUM_SIZE = 32

    def __init__(self):

        Object.__init__(self)

        self.description('ANSI null-terminated string.')

    def __str__(self): return('\'' + self.value() + '\'')

    def size(self): return(len(self.value()) + 1)

    def value(self, v = None):

        memory = self.memory()
        address = self.address()

        if (v == None):

            # Read.
            data = []
            
            for c in memory.dataGenerator(address, 1):

                if (c == '\x00'): break

                data.append(c)

            return(''.join(data))

        # Write.
        v = v[0:String.MAXIMUM_SIZE - 1]
        
        memory.write(address, v)
        memory.write(address + len(v), '\x00')
