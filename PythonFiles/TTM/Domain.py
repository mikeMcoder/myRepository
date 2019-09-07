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
import Frame
import Mask

from Utility import *

MODULE_INDEX = 2

METHOD_INDICES = {'frameElementF32'   : 0,
                  'maskElement'       : 1,
                  'rxPower'           : 2
                 }

ELEMENT_DATA_UITLA = (
                ('FILTER1_TEMPERATURE',             'C'),
                ('FILTER2_TEMPERATURE',             'C'),
                ('SLED_TEMPERATURE',                'C'),
                ('SI_BLOCK_TEMPERATURE',            'C'),
                ('PHOTODIODE_CURRENT',              'uA'),
                ('N5_2_VOLTAGE',                    'V'),
                ('PCB_TEMPERATURE',                 'C'),
                ('DEMODULATION_REAL',               'ABU'),
                ('DEMODULATION_IMAGINARY',          'ABU'),
                ('AVERAGE_FILTER1_TEMPERATURE',     'C'),
                ('AVERAGE_FILTER2_TEMPERATURE',     'C'),
                ('AVERAGE_SLED_TEMPERATURE',        'C'),
                ('AVERAGE_SI_BLOCK_TEMPERATURE',    'C'),
                ('AVERAGE_PHOTODIODE_CURRENT',      'uA'),
                ('AVERAGE_DEMODULATION_REAL',       'ABU'),
                ('AVERAGE_DEMODULATION_IMAGINARY',  'ABU'),
                ('GAIN_MEDIUM_CURRENT',             'mA'),
                ('P3_3_VOLTAGE',                    'V'),
                ('TEC_CURRENT',                     'A'),
                ('TEC_VOLTAGE',                     'V'),
                ('H1_I_MON',                        'A'),
                ('H2_I_MON',                        'A'),
                ('SiB_I_MON',                       'A'),
                ('TECV_MON',                        'V'),
                ('GMI_MON',                         'A'),
                ('GMV_MON',                         'V'),
                ('FILT1_HTR',                       'V'),
                ('FILT2_HTR',                       'V'),
                ('SiB_HTR',                         'V'),
                ('CARRIER_THERM',                   'C'),
               )

ELEMENT_DATA_NANO = (
                ('FILTER1_TEMPERATURE',             'C'),
                ('FILTER2_TEMPERATURE',             'C'),
                ('SLED_TEMPERATURE',                'C'),
                ('SI_BLOCK_TEMPERATURE',            'C'),
                ('PHOTODIODE_CURRENT',              'uA'),
                ('P22_VOLTAGE',                     'V'),
                ('PCB_TEMPERATURE',                 'C'),
                ('DEMODULATION_REAL',               'ABU'),
                ('DEMODULATION_IMAGINARY',          'ABU'),
                ('AVERAGE_FILTER1_TEMPERATURE',     'C'),
                ('AVERAGE_FILTER2_TEMPERATURE',     'C'),
                ('AVERAGE_SLED_TEMPERATURE',        'C'),
                ('AVERAGE_SI_BLOCK_TEMPERATURE',    'C'),
                ('AVERAGE_PHOTODIODE_CURRENT',      'uA'),
                ('AVERAGE_DEMODULATION_REAL',       'ABU'),
                ('AVERAGE_DEMODULATION_IMAGINARY',  'ABU'),
                ('GAIN_MEDIUM_CURRENT',             'mA'),
                ('P3_3_VOLTAGE',                    'V'),
                ('TEC_CURRENT',                     'A'),
                ('TEC_VOLTAGE',                     'V'),
                ('PD_DELTA_HI_H2O',                 'uA'),
                ('AVERAGE_DEMOD_HI_H20',            'ABU'),
                ('AVERAGE_DEMOD_LOW_H20',           'ABU'),
                ('SiB_HEATER',                      'V'),
                ('SiB_SENSE',                       'V'),
               )
PROPERTIES={}

class DomainStage:

    def __init__(self,type=None):
        global PROPERTIES
        ELEMENT_PROPERTIES = []
        PROPERTIES = {'ELEMENT_PROPERTIES':ELEMENT_PROPERTIES}
        if type != None:
            if (type == 0):
                ELEMENT_DATA = ELEMENT_DATA_UITLA
                items = 20                  # uitla entries
            elif (type == 1):
                ELEMENT_DATA = ELEMENT_DATA_UITLA
                items = len(ELEMENT_DATA_UITLA)   # goldbox
            else:
                ELEMENT_DATA = ELEMENT_DATA_NANO
                items = len(ELEMENT_DATA_NANO)   # NANO
            if len(ELEMENT_PROPERTIES):
                ELEMENT_PROPERTIES = []
            for index in range(items):
                data = ELEMENT_DATA[index]
                ELEMENT_PROPERTIES.append({'index' : index,
                                           'label' : data[0],
                                           'units' : data[1],
                                           'type'  : 'F32'})
            PROPERTIES = {'ELEMENT_PROPERTIES':ELEMENT_PROPERTIES}
        self.__frame = DomainFrame()
        self.__mask = DomainMask()
        self.__dictionary = None
               
    def dictionary(self, d = None):

        if (d == None): return(self.__dictionary)

        self.__dictionary = d

    def frame(self):

        'Returns the domain frame.'

        return(self.__frame)

    def mask(self):

        'Returns the domain mask.'

        return(self.__mask)

    def rxPower(self):

        newOperation(MODULE_INDEX,
                     METHOD_INDICES['rxPower'])
        #PyTTXTalk.pushU8(self.__controllerID__()[0])
        sendPacket(1)
        return(PyTTXTalk.popF32())



class DomainFrame(Frame.Frame):

    def __init__(self):

        Frame.Frame.__init__(self,
                             'Domain frame.',
                             PROPERTIES['ELEMENT_PROPERTIES'],
                             MODULE_INDEX,
                             METHOD_INDICES)

class DomainMask(Mask.Mask):

    def __init__(self):

        Mask.Mask.__init__(self,
                           'Domain mask.',
                           PROPERTIES['ELEMENT_PROPERTIES'],
                           MODULE_INDEX,
                           METHOD_INDICES)
