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

    $Source: /data/development/cvs/Sundial2/Python/TTX/HEX.py,v $
    $Revision: 1.1 $
    $Date: 2007/04/18 19:45:25 $
    $Name: Sundial2_01_03_00_01 $
    
'''
import types

DEBUG_REC = 0
def DebugOut(s):
    if DEBUG_REC:
        print s

class Record:

    HIGHEST_ADDRESS = 0xFFFF
    MAXIMUM_SIZE = 0xFF

    TYPES = {'DATA'                     : 0,
             'EOF'                      : 1,
             'EXTENDED_SEGMENT'         : 2,
             'EXTENDED_LINEAR_ADDRESS'  : 4}

    def __computeChecksum__(self, data):

        '''
Data is expected to be a string where each character is a byte.
        '''

        checksum = 0

        for c in data: checksum = checksum + ord(c)

        nresult = (~checksum + 1) & 0xFF
        DebugOut('Record.__computeChecksum__(%s)' % (nresult))
        return nresult

    def __dataToText__(self, data):

        s = ''

        for byte in data: s += '%02X' % (ord(byte))

        DebugOut('Record.__dataToText__(%s)' % (s))
        return(s)

    def __init__(self):
        DebugOut('Record.__init__()')
    
        self.__type = 'DATA' 
        self.__address = 0
        self.__data = ''

    def __repr__(self):
        DebugOut('Record.__repr__()')
        
        s =  ''
        s += 'Type   : %s\n' % self.type()
        s += 'Size   : %d\n' % self.size()
        s += 'Address: 0x%04X\n' % self.address()
        s += 'Data   : %s' % self.__dataToText__(self.data())

        return(s)

    def __textToData__(self, text):
        DebugOut('Record.__textToData__(%s)' % (text))

        data = ''

        for i in range(0, len(text), 2):

            data += chr(int(text[i : i + 2], 16))

        return(data)

    def address(self, a = None):
        DebugOut('Record.address(%s)' % (a))

        if (a == None): return(self.__address)

        assert a <= Record.HIGHEST_ADDRESS, \
               'Address is greater than sixteen bits.'

        if (self.type() != 'DATA'):

            assert a == 0, 'Address must be zero for this record type.' 

        self.__address = a

    def data(self, d = None):
        #DebugOut('Record.data(%s)' % (d))

        if (d == None): return(self.__data)

        assert type(d) == types.StringType, 'Data must be a string.'

        if (self.type() == 'EOF'):

            assert d == '', 'EOF records may not contain data.'

        assert len(d) <= Record.MAXIMUM_SIZE, \
                         'Records do not support this much data.' 

        self.__data = d

    def size(self):
        DebugOut('Record.size(%s)' % (len(self.__data)))
        return(len(self.__data))

    def text(self, t = None):
        DebugOut('Record.text(%s)' % (t))
        if (t == None):

            # Read value.

            # Create everything except the checksum.
            text = ':%02X%04X%02X%s' % (self.size(),
                                        self.address(),
                                        Record.TYPES[self.type()],
                                        self.__dataToText__(self.data()))

            checksum = self.__computeChecksum__(self.__textToData__(text[1 :])) 

            text += '%02X' % (checksum)
            DebugOut('Record.text = %s' % (text))
            return(text)

        # Writing a string. Parse.
        
        # Test the checksum.
        checksum = int(t[-2 : ], 16)

        if (self.__computeChecksum__(self.__textToData__(t[1 : -2])) != \
            checksum):

            raise 'Checksum error.'

        size = int(t[1 : 3], 16)

        address = int(t[3 : 7], 16)

        ttype = int(t[7 : 9])

        DebugOut('HEX.text: size = %s' % (size))
        DebugOut('HEX.text: address = %s' % (address))
        DebugOut('HEX.text: ttype = %s' % (ttype))
        

        for key, value in Record.TYPES.items():

            if (ttype == value): ttype = key

        # If the type was not found it will still be an integer.
        assert type(ttype) == types.StringType, 'Unknown type.'
        
        data = self.__textToData__(t[9 : -2])

        if (size != len(data)): raise 'Incorrect amount of data.'

        self.type(ttype)
        self.address(address)
        self.data(data)

    def type(self, t = None):
        DebugOut('HEX.type(%s)' % (t))
        
        if (t == None): return(self.__type)

        # Raise an exception if the type does not exist.
        Record.TYPES[t] 

        self.__type = t

        if (t != 'DATA'): self.__address = 0

        if (t == 'EOF'): self.__data = ''

def test():

    r = Record()
    r.type('EOF')
    print r
    print r.text()

    r1 = Record()
    r1.text(r.text())
    print '.' * 10
    print r1
    print r1.text()

    print

    r.type('EXTENDED_SEGMENT')
    r.data('\xF0\x00')
    print r
    print r.text()

    r1 = Record()
    r1.text(r.text())
    print '.' * 10
    print r1
    print r1.text()

    print

    r.type('EXTENDED_LINEAR_ADDRESS')
    r.data('\x00\xFF')
    print r
    print r.text()

    r1 = Record()
    r1.text(r.text())
    print '.' * 10
    print r1
    print r1.text()

    print

    r.type('DATA')
    r.address(0x2462)
    r.data('\x46\x4C\x55\x49\x44\x20\x50\x52\x4F\x46\x49\x4C\x45\x00\x46\x4C')
    print r
    print r.text()

    r1 = Record()
    r1.text(r.text())
    print '.' * 10
    print r1
    print r1.text()

    ROOT = r'c:\Documents and Settings\Ken\Desktop'

    file = open(ROOT + r'\H3.hex')

    r = Record()

    counter  = {'EOF' : 0,
                'DATA' : 0,
                'EXTENDED_SEGMENT' : 0,
                'EXTENDED_LINEAR_ADDRESS' : 0}

    for line in file.readlines():

        if (line.startswith(':')):

            r.text(line.strip())

            counter[r.type()] += 1

    print counter

    file.close()

