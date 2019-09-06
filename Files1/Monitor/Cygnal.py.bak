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

    $Source: /data/development/cvs/Sundial2/Python/Monitor/Cygnal.py,v $
    $Revision: 1.1 $
    $Date: 2007/04/18 19:45:18 $
    $Name: Sundial2_02_01_04_00 $
    
'''
class CodeLocation:

    '''
Map any 17-bit code location to a bank and a 16-bit address.
    '''

    def __init__(self, location):

        # Ensure the address is 17-bits.
        assert (location & ~0x1FFFF) == 0, 'Location must be 17-bit.'

        # Bank is represented by bits 15 & 16.
        self.__bank = location >> 15;

        if (self.__bank == 0):

            self.__address = location;

        else:

            self.__address = (location & 0x7FFF) | (1 << 15)

        self.__page = location >> 10;

        self.__location = location

    def __repr__(self):

        s = ''
        s += 'Location: 0x%05X\n' % (self.location())
        s += 'Address : 0x%04X\n' % (self.address())
        s += 'Bank    : %d\n' % (self.bank())
        s += 'Page    : %d' % (self.page())

        return(s)

    def address(self): return(self.__address)

    def bank(self): return(self.__bank)

    def location(self): return(self.__location)

    def page(self): return(self.__page)
