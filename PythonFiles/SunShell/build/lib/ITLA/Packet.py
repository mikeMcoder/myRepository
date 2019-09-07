'''
NeoPhotonics CONFIDENTIAL
Copyright 2004, 2005 NeoPhotonics Corporation All Rights Reserved.

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

    $Source: /data/development/cvs/Sundial2/Python/ITLA/Packet.py,v $
    $Revision: 1.1 $
    $Date: 2007/04/18 19:45:18 $
    $Name: Sundial2_01_03_00_01 $
    
'''
import struct
import types

import BitField

class Packet:

    def __init__(self):
        
        self.__buffer = ''

    def buffer(self, buffer = None):
        
        '''
Raw data as string.
        '''
        
        if (buffer == None): return self.__buffer
        
        self.__buffer = buffer
    
    def checksum(self): pass

    def computedChecksum(self):
        bytes = struct.unpack('BBBB', self.buffer())
        bip8 = (bytes[0] & 0x0F) ^ bytes[1] ^ bytes[2] ^ bytes[3]
        
        return ((bip8 & 0xF0) >> 4) ^ (bip8 & 0x0F)

    def data(self): pass

    def register(self): pass

class ModuleBoundPacket(Packet):
    
    '''
Packet structure that conforms to IPC2003.00.x.
    '''

    def __init__(self):
        
        self.__bitfield = BitField.BitField('MODULE_BOUND_PACKET', 32)
        self.__bitfield.addChild(BitField.BitField('CHECKSUM', 4, 28))
        self.__bitfield.addChild(BitField.BitField('LAST_RESPONSE',
                                                   1,
                                                   27,
                                                   {0 : 'FALSE',
                                                    1 : 'TRUE'}))
        self.__bitfield.addChild(BitField.BitField('LASER',
                                                   1,
                                                   26,
                                                   {0 : 'LASER0',
                                                    1 : 'LASER1'}))
        self.__bitfield.addChild(BitField.BitField('MODE',
                                                   1,
                                                   24,
                                                   {0 : 'READ',
                                                    1 : 'WRITE'}))
        self.__bitfield.addChild(BitField.BitField('REGISTER', 8, 16))
        data = BitField.BitField('DATA', 16)
        data.addChild(BitField.BitField('HIGH', 8, 8))
        data.addChild(BitField.BitField('LOW', 8, 0))
        self.__bitfield.addChild(data)

    def __repr__(self):
        
        return(`self.__bitfield`)

    def __str__(self):
        return self.__bitfield.name() + ' 0x%08X' % self.__bitfield.value()

    def checksum(self, value = None):
        
        if (value == None):
            
            return(self.__bitfield['CHECKSUM'].value())
        
        self.__bitfield['CHECKSUM'].value(value)

    def register(self, value = None):
        
        if (value == None):
            
            return(self.__bitfield['REGISTER'].value())
        
        self.__bitfield['REGISTER'].value(value)

    def lastResponse(self, value = None):
        '''
Valid values: 'TRUE', 'FALSE'
        '''
        
        bitfield = self.__bitfield['LAST_RESPONSE']
        
        if (value == None): return(str(bitfield))

        bitfield.value(value)

    def laser(self, value = None):
        
        '''
Valid values: 'LASER0', 'LASER1'
        '''
        
        bitfield = self.__bitfield['LASER']
        
        if (value == None): return(str(bitfield))
        

        bitfield.value(value)

    def mode(self, value = None):
        
        '''
Valid values: 'READ', 'WRITE'
        '''
        
        bitfield = self.__bitfield['MODE']
        
        if (value == None): return(str(bitfield))
        

        bitfield.value(value)

    def data(self, value = None):
        
        '''
Read or writes the 16 bit data value. Use dataLow or dataHigh for 8-bit access.
        '''
        
        if (value == None):
            
            return(self.__bitfield['DATA'].value())
        
        self.__bitfield['DATA'].value(value)

    def dataLow(self, value = None):
        
        '''
Read or write the 8-bit data value of the 16-bit data field.
        '''
        
        if (value == None):
            
            return(self.__bitfield['DATA']['LOW'].value())
        
        self.__bitfield['DATA']['LOW'].value(value)
        
    def dataHigh(self, value = None):
        
        '''
Read or write the 8-bit data value of the 16-bit data.
        '''
        
        if (value == None):
            
            return(self.__bitfield['DATA']['HIGH'].value())
        
        self.__bitfield['DATA']['HIGH'].value(value)

    def buffer(self, value = None):
        
        '''
Imports or exports raw packet data. String values are in big endian format.
        '''
        
        if (value == None):
            
            l = list(self.__bitfield.toString())

            # Convert to bit endian for transmission.
            l.reverse()
            return(''.join(l))

        # Convert from big endian. Bitfields expect little endian.
        value = list(value)
        value.reverse()
        self.__bitfield.fromString(''.join(value))
        

class HostBoundPacket(Packet):

    '''
Packet structure that conforms to IPC2003.00.x.
    '''

    def __init__(self):
        
        self.__bitfield = BitField.BitField('HOST_BOUND_PACKET',32)

        self.__bitfield.addChild(BitField.BitField('CHECKSUM',4,28))

        self.__bitfield.addChild(BitField.BitField('CE',
                                                   1,
                                                   27,
                                                   {0 : 'FALSE',
                                                    1 : 'TRUE'}))

        self.__bitfield.addChild(BitField.BitField('LASER',
                                                   1,
                                                   26,
                                                   {0 : 'LASER0',
                                                    1 : 'LASER1'}))

        self.__bitfield.addChild(BitField.BitField('STATUS',
                                                   2,
                                                   24,
                                                   {0 : 'OK',
                                                    1 : 'XE',
                                                    2 : 'AEA',
                                                    3 : 'CP'}))
        
        self.__bitfield.addChild(BitField.BitField('REGISTER', 8, 16))

        data = BitField.BitField('DATA', 16)

        data.addChild(BitField.BitField('HIGH', 8, 8))

        data.addChild(BitField.BitField('LOW', 8, 0))

        self.__bitfield.addChild(data)

    def __repr__(self):
        
        return(`self.__bitfield`)

    def __str__(self):
        return self.__bitfield.name() + '   0x%08X' % self.__bitfield.value()

    def checksum(self, value = None):

        if (value == None):

            return(self.__bitfield['CHECKSUM'].value())

        self.__bitfield['CHECKSUM'].value(value)

    def status(self, value = None):
        
        bitfield = self.__bitfield['STATUS']
        
        if (value == None): return(str(bitfield))
        
        if (type(value) != types.StringType):

            raise exceptions.TypeError('Must be a string.')

        bitfield.value(value)

    def register(self, value = None):
        
        if (value == None):
            
            return(self.__bitfield['REGISTER'].value())
        
        self.__bitfield['REGISTER'].value(value)

    def communicationError(self, value = None):
        
        bitfield = self.__bitfield['CE']
        
        if (value == None): return(str(bitfield))
        
        if (type(value) != types.StringType):

            raise exceptions.TypeError('Must be a string.')

        bitfield.value(value)

    def data(self, value = None):
        
        '''
Read or writes the 16 bit data value. Use dataLow,dataHigh for 8 bit access.
        '''
        
        if (value == None):
            
            return(self.__bitfield['DATA'].value())
        
        self.__bitfield['DATA'].value(value)

    def dataLow(self, value = None):
        
        '''
Read or writes the 8-bit data value of the 16-bit data.
        '''
        
        if (value == None):
            
            return(self.__bitfield['DATA']['LOW'].value())
        
        self.__bitfield['DATA']['LOW'].value(value)
        
    def dataHigh(self, value = None):
        
        '''
Read or writes the 8-bit data value of the 16-bit data.
        '''
        
        if (value == None):
            
            return(self.__bitfield['DATA']['HIGH'].value())
        
        self.__bitfield['DATA']['HIGH'].value(value)
        
    def buffer(self, value = None):
        
        '''
Imports or exports raw packet data. String values are in big endian format.
        '''
        
        if (value == None):
            
            l = list(self.__bitfield.toString())

            # Convert to bit endian for transmission.
            l.reverse()
            return(''.join(l))

        # Convert from big endian. Bitfields expect little endian.
        value = list(value)
        value.reverse()
        self.__bitfield.fromString(''.join(value))

