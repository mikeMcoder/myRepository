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
import PyTTXTalk
import Dictionary
from Utility import *
import System

import Mask

MODULE_INDEX = 7

METHOD_INDICES = {'frequency'           : 0,
                  'powerTarget'         : 1,
                  'status'              : 2,
                  'powerVariance'       : 3,
                  'powerError'          : 4,
                  'powerOutput'         : 5,
                  'maskElement'         : 6,
                  'currentTarget'       : 7,
                  'mode'                : 8,
                  'coldStart'           : 9,
                  'retries'             : 10,
                  'frequencyOffset'     : 11,
                  'powerState'          : 12,
                  'tecClock'            : 13
                  }

ELEMENT_DATA = (('TUNER',  ''),
                ('SBS_SUPPRESSION', ''),
                ('TX_TRACE', ''),
                ('AMBIENT_COMPENSATOR', ''))

ELEMENT_PROPERTIES = []

for index in range(len(ELEMENT_DATA)):

    data = ELEMENT_DATA[index]

    ELEMENT_PROPERTIES.append({'index':index,
                               'label':data[0],
                               'units':data[1],
                               'type':''})

PROPERTIES = {'ELEMENT_PROPERTIES':ELEMENT_PROPERTIES}

class TunerManager:
    def __init__(self, ttx_interface, dictionary_manager, Nano=False):
        self.__current_tuner = CurrentTuner(ttx_interface)
        self.__power_tuner = PowerTuner()
        config = System.Configuration()
        if Nano:        # NANO
            status_dictionary = {'11': 'CHANNEL_LOCK', '10': 'STABILIZE', '13': 'MZM_STATE',
                                 '12': 'FINE_TUNE', '1': 'IDLE', '0': 'COLD_START',
                                 '3': 'TEMPERATURE', '2': 'DARK', '5': 'ADJUSTMENT',
                                 '4': 'GAIN_MEDIUM', '7': 'CAVITY_LOCK', '6': 'FIRST_LIGHT',
                                 '9': 'CAVITY_OFFSET_LOCK', '8': 'POWER_LEVEL'}
            state_dictionary = {'1': 'POWER_STATE_LASER_PHOTODIODE', '0': 'POWER_STATE_DISABLE',
                                '3': 'POWER_STATE_LOCK', '2': 'POWER_STATE_MZM_PHOTODIODE'}
            self.__current_tuner.statusDictionary(status_dictionary)
            self.__current_tuner.powerStateDictionary(state_dictionary)
            self.__power_tuner.statusDictionary(status_dictionary)
            self.__power_tuner.powerStateDictionary(state_dictionary)
            return
        status_dictionary = config.restore(ttx_interface.firmwareVersion(), 'TunerStatus')
#        print ttx_interface.firmwareVersion()
        if len(status_dictionary) == 0:
            raise 'TunerStatus undefined!'

        state_dictionary = config.restore(ttx_interface.firmwareVersion(), 'PowerState')
        if len(state_dictionary) == 0:
            raise 'Power States undefined!'

        dm = dictionary_manager
        d = Dictionary.Dictionary()
#        d.memory(dm.dictionary('MODEL_DICTIONARY').memory())
#        d.addEntry('model', dm.dictionary('MODEL_DICTIONARY'))
        ###d.addEntry('ambient_compensator', dm.dictionary('AMBIENT_COMPENSATOR_DICTIONARY'))
        self.__current_tuner.statusDictionary(status_dictionary)
        self.__current_tuner.powerStateDictionary(state_dictionary)
        self.__current_tuner.dictionary(d)

        d1 = Dictionary.Dictionary()
#        d1.memory(dm.dictionary('MODEL_DICTIONARY').memory())
#        d1.addEntry('model', dm.dictionary('MODEL_DICTIONARY'))
        ###d1.addEntry('power', dm.dictionary('POWER_DICTIONARY'))
        ###d1.addEntry('ambient_compensator', dm.dictionary('AMBIENT_COMPENSATOR_DICTIONARY'))
        self.__power_tuner.statusDictionary(status_dictionary)
        self.__power_tuner.powerStateDictionary(state_dictionary)
        self.__power_tuner.dictionary(d1)

    def currentTuner(self):
        return self.__current_tuner

    def powerTuner(self):
        return self.__power_tuner

class Tuner:

    '''
Class to tune the laser to specified frequencies.
    '''

    def __init__(self):

        self.__dictionary = None
        self.__module_index = MODULE_INDEX
        self.__method_indices = METHOD_INDICES
        self.__mask = TunerMask()

    def statusDictionary(self, dictionary = None):
        if dictionary != None:
            self.__status_dictionary = dictionary
        return self.__status_dictionary

    def powerStateDictionary(self, dictionary = None):
        if dictionary != None:
            self.__power_state_dictionary = dictionary
        return self.__power_state_dictionary

    def __repr__(self):

        s  = 'Frequency       : %7.3f\n' % self.frequency()
        s += 'Status          : %s\n' % self.status()
        s += 'Mask            : %s\n' % ['Unmasked', 'Masked'][self.mask().tuner()]
        s += 'Retries         : %d' % self.retries()
        try:
            s += '\nFrequency Offset: %d MHz' % self.frequencyOffset()
        except:
            pass
        s += '\nPower State     : %s' % self.powerState()

        return(s)

    def labels(self):
        data = []
        data.append('Frequency')
        data.append('Status')
        data.append('Mask')
        data.append('Retries')
        try:
            self.frequencyOffset()
            data.append('Frequency Offset')
        except:
            pass

        return data

    def elements(self):
        data = []
        data.append(self.frequency())
        data.append(self.status())
        data.append(self.mask().tuner())
        data.append(self.retries())
        try:
            data.append(self.frequencyOffset())
        except:
            pass

        return data

    def dictionary(self, d = None):

        if (d == None): return(self.__dictionary)

        self.__dictionary = d

    def frequency(self, THz = None):
        ' frequency = 0 disable lasers. '

        newOperation(self.__module_index, self.__method_indices['frequency'])

        if (THz != None): PyTTXTalk.pushF32(THz)

        sendPacket(1)

        if (THz == None): return(PyTTXTalk.popF32())

    def status(self):
        newOperation(self.__module_index, self.__method_indices['status'])

        sendPacket(1)
        s = PyTTXTalk.popU8()

        return(self.statusDictionary()[str(s)])

    def powerState(self):
        newOperation(self.__module_index, self.__method_indices['powerState'])

        sendPacket(1)
        s = PyTTXTalk.popU8()

        return(self.powerStateDictionary()[str(s)])

    def retries(self):
        '''
Returns the total number of channel retries to lock the cavity within
the desired temperature range.
        '''
        newOperation(self.__module_index, self.__method_indices['retries'])
        sendPacket(1)
        return(PyTTXTalk.popU8())

    def mask(self):

        'Returns the tuner mask. Use only if TRN disabled laser'

        return(self.__mask)

    def coldStart(self):
        '''
This turns off the tuner putting it in cold start. Note: This this is
equivalent to t.off(). Standard way to disable laser is to set frequency to
0.0
        '''
        newOperation(self.__module_index, self.__method_indices['coldStart'])
        sendPacket(1)

    def frequencyOffset(self, MHz = None):

        newOperation(self.__module_index, self.__method_indices['frequencyOffset'])

        if (MHz != None): PyTTXTalk.pushS16(MHz)

        sendPacket(1)

        if (MHz == None): return(PyTTXTalk.popS16())

    def __moduleIndex(self):
        return self.__module_index

    def __methodIndices(self):
        return self.__method_indices

class PowerTuner(Tuner):
    ' Tunes to channels allowing user to specify constant power. '

    __POWER_MODE = 0

    def __init__(self):
        self.__description = 'PowerTuner'
        self.__module_index = MODULE_INDEX
        self.__method_indices = METHOD_INDICES

        Tuner.__init__(self)

    def __repr__(self):
        s =  'Description     : %s\n' % self.__description
        s += Tuner.__repr__(self) + '\n'
        s += 'Power Target    : %f mW\n' % self.powerTarget()
        s += 'Power Output    : %f mW\n' % self.powerOutput()
        s += 'Power Variance  : %f uA\n' % self.powerVariance()
        s += 'Power Error     : %f uA^2' % self.powerError()
        return(s)

    def powerTarget(self, mW = None):
        'Desired optical output power'

        newOperation(self.__module_index, self.__method_indices['powerTarget'])

        if (mW != None): PyTTXTalk.pushF32(mW)

        sendPacket(1)

        if (mW == None): return(PyTTXTalk.popF32())
        self.__setMode()

    def powerVariance(self):
        'Variance of the photodiode current error (powerError())'
        newOperation(self.__module_index, self.__method_indices['powerVariance'])

        sendPacket(1)

        return(PyTTXTalk.popF32())

    def powerError(self):
        'Photodiode error from target photodiode current'
        newOperation(self.__module_index, self.__method_indices['powerError'])

        sendPacket(1)

        return(PyTTXTalk.popF32())

    def powerOutput(self):
        'Measured optical output.'
        newOperation(self.__module_index, self.__method_indices['powerOutput'])

        sendPacket(1)

        return(PyTTXTalk.popF32())

    def frequency(self, THz = None):
        ' Frequency = 0 disable lasers. '
        if (THz != None): self.__setMode()
        return(Tuner.frequency(self, THz))

    def __setMode(self):
        newOperation(self.__module_index, self.__method_indices['mode'])
        PyTTXTalk.pushS8(PowerTuner.__POWER_MODE)
        sendPacket(1)

    def setTEC_Clock(self, TEC_clock_state = None):
        '0:enable TEC Clock, 1:disable for 30 sec (repeat before to keep it disabled)'
        newOperation(self.__module_index, self.__method_indices['tecClock'])

        if(TEC_clock_state == None):
            sendPacket(1)
            return(PyTTXTalk.popS8())

        PyTTXTalk.pushS8(TEC_clock_state)
        sendPacket(1)

class CurrentTuner(Tuner):
    ' Tunes to channels allowing user to specify constant current. '
    __CURRENT_MODE = 1

    def __init__(self, ttx_interface):
        self.__description = 'CurrentTuner'
        self.__module_index = MODULE_INDEX
        self.__method_indices = METHOD_INDICES
        self.__ttx_interface = ttx_interface

        Tuner.__init__(self)

    def __repr__(self):
        s =  'Description     : %s\n' % self.__description
        s += Tuner.__repr__(self) + '\n'
        s += 'Current Target  : %f mA\n' % self.currentTarget()
        s += 'Current Output  : %f mA\n' % self.currentOutput()
        return(s)

    def frequency(self, THz = None):
        ' Frequency = 0 disable lasers. '
        if (THz != None): self.__setMode()
        return(Tuner.frequency(self, THz))

    def currentTarget(self, mA = None):
        'Desired optical output current'

        newOperation(self.__module_index, self.__method_indices['currentTarget'])

        if (mA!= None): PyTTXTalk.pushF32(mA)

        sendPacket(1)

        if (mA == None): return(PyTTXTalk.popF32())
        self.__setMode()


    def currentOutput(self):
        'Measured current output.'
        '''return(self.__ttx_interface.domainStage().frame().gainMediumCurrent())
        '''
        return(self.__ttx_interface.controlStage().frame().gainMediumCurrent())


    def __setMode(self):
        newOperation(self.__module_index, self.__method_indices['mode'])
        PyTTXTalk.pushS8(CurrentTuner.__CURRENT_MODE)
        sendPacket(1)


class TunerMask(Mask.Mask):

    def __init__(self):

        Mask.Mask.__init__(self,
                           'Tuner mask.',
                           PROPERTIES['ELEMENT_PROPERTIES'],
                           MODULE_INDEX,
                           METHOD_INDICES)