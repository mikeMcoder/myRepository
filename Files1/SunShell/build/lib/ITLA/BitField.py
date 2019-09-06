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

    $Source: /data/development/cvs/Sundial2/Python/ITLA/BitField.py,v $
    $Revision: 1.1 $
    $Date: 2007/04/18 19:45:18 $
    $Name: Sundial2_01_03_00_01 $
    
'''
import copy
import exceptions
import math
import types

class BitField:

    """
BitField:

b = BitField(name, length, position = 0, cipher = None)

name: A string containing the bitfield name.

length: An integer representing the number of bits.

position: An integer describing the first bit position of the field. This
is meaningful only when a parent bitfield is supplied.

cipher: A dictionary of integer keys and string values. The integers can be
int or long. Used to convert a field's value into a string meaningful to
the application.
    """

    def __init__(self,
                 name,
                 length,
                 position = 0,
                 cipher = None):

        self.__name = name
        self.__length = length
        self.__position = position
        self.__parent = None
        self.__children = {}
        self.__value = 0L
        self.__cipher = cipher

    def __deepcopy__(self, memo):

        c = BitField(self.__name,
                     self.__length,
                     self.__position,
                     copy.deepcopy(self.__cipher, memo))

        c.__value = self.value()

        # Deep copy each child and reassign its parent.
        for k, v in self.__children.iteritems():

            c.addChild(copy.deepcopy(v, memo))

        return(c)

    def __repr__(self):

        # Precompute formatting widths.
        WIDTH = [[len(self.name())],
                  [len(hex(self.value()))],
                  [len(str(self))]]

        for child in self.__children.values():

            WIDTH[0].append(len(child.name()))
            WIDTH[1].append(len(hex(child.value())))
            WIDTH[2].append(len(str(child)))

        WIDTH[0].sort()
        WIDTH[0] = WIDTH[0].pop()
        WIDTH[1].sort()
        WIDTH[1] = WIDTH[1].pop()
        WIDTH[2].sort()
        WIDTH[2] = WIDTH[2].pop()

        s = binaryString(self.value(), self.length())
        s += ' %-*s' % (WIDTH[0], self.name())
        s += ' %+*s' % (WIDTH[1], hex(self.value()))
        s += ' %-*s\n' % (WIDTH[2], str(self))
        
        child_list = self.__children.values()

        child_list.sort(lambda a, b: b.position() - a.position())

        for child in child_list:

            s += '%*s' % (self.length(),
                          '%-*s' %
                          (child.length() + child.position(),
                           child.toBinaryString()))

            s += ' %-*s' % (WIDTH[0], child.name())
            s += ' %+*s' % (WIDTH[1], hex(child.value()))
            s += ' %-*s\n' % (WIDTH[2], str(child))
            
        return(s[:-1])

    def __str__(self):
        if (self.__cipher is not None):

            return(self.__cipher.get(self.value(), 'Undefined'))

        if (self.__length == 1):

            if (self.value() == True): return('True')

            return('False')

        return('')

    def __hex__(self): return(hex(self.value()))

    def __oct__(self): return(oct(self.value()))

    def __getitem__(self, index): return(self.__children[index])

    def __setitem__(self, index, value): self.__children[index].value(value)

    def __delitem__(self, index): del self.__children[index]

    def __getslice__(self, i, j):

        if (j > self.__length): j = self.__length

        position = i
        length = j - i

        v = (self.value() & self.__createMask(length, position)) >> i

        return(BitField('', length, position).value(v))

    def __len__(self): return(self.__length)

    def __createMask(self, length = None, position = None):

        if (position is None): position = self.__position
        if (length is None): length = self.__length
        
        m = ~0L
        m <<= length
        m = ~m
        m <<= position

        return(m)

    def ciphers(self):

        '''
Return a copy of the cipher so that it may not be altered.
        '''

        return(copy.deepcopy(self.__cipher))

    def cipher(self):
        if self.__cipher != None:
            return self.__cipher[self.value()]
    
    def toBinaryString(self): return(binaryString(self.value(), self.length()))

    def toString(self):

        count = self.__length / 8

        if (self.__length % 8): count += 1

        s = ''

        value = self.value()

        while (count):

            s += chr(value & 0xFF)
            value >>= 8
            count -= 1

        return(s)

    def fromString(self, string):

        v = 0L

        for i in range(len(string)): v |= ord(string[i]) << (i * 8)

        self.value(v)

    def length(self, s = None):

        if (s is None): return(self.__length)

        self.__length = s

        return(self)

    def position(self, p = None):

        if (p is None): return(self.__position)

        self.__position = p

        return(self)

    def name(self, n = None):

        if (n is None): return(self.__name)

        self.__name = n

        return(self)

    def value(self, v = None):

        if (self.__parent is None):

            current_value = self.__value

        else:
            
            current_value = self.__parent.value()

        mask = self.__createMask()

        if (v is None): return((current_value & mask) >> self.__position)

        if (type(v) == types.StringType):

            for item in self.__cipher.items():

                if (item[1] == v):

                    v = item[0]
                    break

            if (type(v) == types.StringType):

                raise exceptions.ValueError(v + ' is an unknown symbol.')

        if (v > long(mask)):

            raise exceptions.ValueError('Value exceeds length of this bit field.')
        new_value = (current_value & ~mask) | (v << self.__position)

        if (self.__parent is None):
            
            self.__value = new_value

        else:

            self.__parent.value(new_value)

        return(self)

    def addChild(self, bitfield):

        if (self.__length < (bitfield.position() + len(bitfield))):

            raise(exceptions.ValueError('Bitfield \'%s\' is out of bounds.' % (name)))

        bitfield.__parent = self

        self.__children[bitfield.name()] = bitfield


def test1():
    
    b = BitField('REGISTER', 16)
    b['REGISTER'] = 0x01
    
    print repr(b['REGISTER'])
    
    
def test():

    b = BitField('REGISTER', 16)

    b.addChild(BitField('FRAME', 13, 0))
    b.addChild(BitField('FLAG', 1, 13))
    b.addChild(BitField('STA', 2, 14, {0:'OK', 1:'CP', 2:'XE', 3:'AEA'}))

    for i in range(13):

        b['FRAME'].addChild(BitField('BIT%d' % (i), 1, i))

    return(b)

def binaryString(value, width, cluster_length = None):

    if (cluster_length is None): cluster_length = width

    if (width % cluster_length):

        width += (cluster_length - (width % cluster_length))

    s = ''

    test_bit = 1L << (width - 1)
    counter = 0

    while (test_bit):

        if (value & test_bit):
            
            s += '1'

        else:

            s += '0'

        test_bit >>= 1

        counter += 1
            
        if (counter == cluster_length):

            s += '.'
            counter = 0

    return(s[:-1])

if __name__ == '__main__':
    print repr(test())
    #test1()