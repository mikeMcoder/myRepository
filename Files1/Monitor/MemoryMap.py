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

    $Source: /data/development/cvs/Sundial2/Python/Monitor/MemoryMap.py,v $
    $Revision: 1.1 $
    $Date: 2007/04/18 19:45:18 $
    $Name: Sundial2_02_01_04_00 $
    
'''
import Cygnal

NEW_MAP_LOCATION             = Cygnal.CodeLocation(0x17400)
CURRENT_DICTIONARY_LOCATION  = Cygnal.CodeLocation(0x17800)
CURRENT_MAP_LOCATION         = Cygnal.CodeLocation(0x17C00)
NEUTRAL_ZONE_LOCATION        = Cygnal.CodeLocation(0x17800)
DICTIONARY_LOCATION          = Cygnal.CodeLocation(0x0400)
MONITOR_DICTIONARY_LOCATION  = Cygnal.CodeLocation(0x18400)
MONITOR_CODE_LOCATION        = Cygnal.CodeLocation(0x18000)

DICTIONARY_SIZE = 1024
MAP_SIZE = 1024
NEUTRAL_ZONE_SIZE = MAP_SIZE + DICTIONARY_SIZE

CODE_SPACE_SIZE = 64 * 1024

MONITOR_DICTIONARY_KEY = 'MonitorDictionary'