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

MODULE_INDEX = 1

METHOD_INDICES = {
                    'frameElementU16':0,
                    'frameElementU32':1,
                    'maskElement':2,
                 }

ELEMENT_DATA_NANO_ALPHA = (
                'RTD1',
                'RTD2',           
                'SLED_THERMISTOR',
                'P3_3V',
                'PHOTODIODE',
                'PCB_TEMPERATURE',
                'VTEC_N1',
                'VTEC_N2',
                'VTEC_P',
                'P22V',
                'SAMPLE1',
                'SAMPLE2',
                'SAMPLE3',
                'SAMPLE4',
                'SAMPLE5',
                'SAMPLE6',
                'SAMPLE7',
                'SAMPLE8',
                'SAMPLE9',
                'SAMPLE10',
                )
ELEMENT_DATA_NANO_BETA = (
                'RTD1',
                'RTD2',           
                'SLED_THERMISTOR',
                'P3_3V',
                'PHOTODIODE',
                'PCB_TEMPERATURE',
                'TEC_I',
                'VTEC_N',
                'VTEC_P',
                'P22V',
                'SAMPLE1',
                'SAMPLE2',
                'SAMPLE3',
                'SAMPLE4',
                'SAMPLE5',
                'SAMPLE6',
                'SAMPLE7',
                'SAMPLE8',
                'SAMPLE9',
                'SAMPLE10',
                'SiB_HEATER',
                'SiB_SENSE',
                )
ELEMENT_DATA_UITLA = (
                'RTD1',
                'RTD2',           
                'SLED_THERMISTOR',
                'SiB_RTD',
                'P3_3V',
                'PHOTODIODE',
                'DEMOD_SIGNAL',
                'PCB_TEMPERATURE',
                'TEC_CURRENT',
                'TEC_VOLTAGE',
                'N5_2V',
                'SAMPLE1',
                'SAMPLE2',
                'SAMPLE3',
                'SAMPLE4',
                'SAMPLE5',
                'SAMPLE6',
                'SAMPLE7',
                'SAMPLE8',
                'SAMPLE9',
                'SAMPLE10',
                )

GB_MODULE_INDEX = 1
GB_ELEMENT_DATA = (
                'H1_I_MON',
                'H2_I_MON',
                'SiB_I_MON',
                'TEC_VOLTAGE',
                'GMI_MON',
                'GMV_MON',
                'S1P_MON',
                'S2P_MON',
                'Carrier_Version',
                'Carrier_Therm',
                'P3_3_VOLTAGE',
                'N5VOLT_MONITOR',
                'CH4',
                'CH5',
                'CH6',
                'CH7',
               )
PROPERTIES={}

class SampleStage:

    def __init__(self, nano = False):
        
        global PROPERTIES
        ELEMENT_PROPERTIES = []
        
        if nano:
            ELEMENT_DATA = ELEMENT_DATA_NANO_ALPHA
            #ELEMENT_DATA = ELEMENT_DATA_NANO_BETA
        else:
            ELEMENT_DATA = ELEMENT_DATA_UITLA
        
        
        for index in range(len(ELEMENT_DATA)):
        
            label = ELEMENT_DATA[index]
        
            ELEMENT_PROPERTIES.append({'index':index,
                                       'label':label,
                                       'units':'Counts',
                                       'type':['U16', 'U32'][index < 2]})
        
        PROPERTIES = {'ELEMENT_PROPERTIES':ELEMENT_PROPERTIES}
        self.__frame = SampleFrame()
        self.__mask = SampleMask()

    def frame(self):

        'Returns the sample frame.'

        return(self.__frame)

    def mask(self):

        'Returns the sample mask.'

        return(self.__mask)

class SampleFrame(Frame.Frame):

    def __init__(self):

        Frame.Frame.__init__(self,
                             'Sample frame.',
                             PROPERTIES['ELEMENT_PROPERTIES'],
                             MODULE_INDEX,
                             METHOD_INDICES)

class SampleMask(Mask.Mask):

    def __init__(self):

        Mask.Mask.__init__(self,
                           'Sample mask.',
                           PROPERTIES['ELEMENT_PROPERTIES'],
                           MODULE_INDEX,
                           METHOD_INDICES)