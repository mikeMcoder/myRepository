'''
NeoPhotonics CONFIDENTIAL
Copyright 2003-2015 NeoPhotonics Corporation All Rights Reserved.

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

    $Source: /data/development/cvs/Sundial2/Python/TTX/CRC16.py,v $
    $Revision: 1.1 $
    $Date: 2007/04/18 19:45:25 $
    $Name: Sundial2_01_03_00_01 $
    
'''

DEBUG_CRC = 0
def DebugOut(s):
    if DEBUG_CRC:
        print s

#def ROR(x, n):
#    mask = (2L**n) - 1
#    mask_bits = x & mask
#    return (x >> n) | (mask_bits << (16 - n))

def ROL(x, n):
    return (x << n) & 0xFFFF #ROR(x, 16 - n)

def computeCRC(init_crc, arData, nLen):
    DebugOut('computeCRC(%s,arData,%s)' % (init_crc, nLen))
        
    crc = int(init_crc)
    DebugOut('computeCRC 1 [init_crc] : %s' % (crc))
    DebugOut('computeCRC nLen = %s' % (nLen))
    #DebugOut('computeCRC range(nLen) = %s' % range(nLen))
        
    for n in range(nLen):
        DebugOut('%s computeCRC 2.0 [ord(arData[n])] : %s' % (n, ord(arData[n])))
        
        crc = crc ^ ROL(ord(arData[n]), 8)
        DebugOut('computeCRC 2.1 [crc = crc ^ ROL(ord(arData[n]), 8)] : %s' % (crc))
                
        for i in range(8) :
            if( crc & 0x8000 ):
                crc = ROL(crc, 1) ^ 0x1021
                DebugOut('computeCRC 3 [crc = ROL(crc, 1) ^ 0x1021] : %s' % (crc))
            else:
                crc = ROL(crc, 1)
                DebugOut('computeCRC 4 [crc = ROL(crc, 1)] : %s' % (crc))

    
    print('computeCRC: final result = %s' % (crc))
    return crc

SEED = 0xA001

def nextWord(crc, data):
    DebugOut('nextWord(%s,data)' % (crc))
        
    '''
Given a sixteen bit CRC and sixteen bit word compute the next CRC word.
    '''

    for i in range(8, 0, -1):
        if ((data ^ crc) & 0x0001):
            crc = (crc >> 1) ^ SEED
        else:
            crc >>= 1

        data >>= 1

    DebugOut('nextWord: return %s' % (crc))
    return(crc)
