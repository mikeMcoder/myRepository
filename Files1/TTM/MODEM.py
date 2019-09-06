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

    $Source: /data/development/cvs/Sundial2/Python/TTX/MODEM.py,v $
    $Revision: 1.2 $
    $Date: 2007/11/17 01:07:54 $
    $Name: Sundial2_01_03_00_01 $

'''
import math

class MODEM:

    def __init__(self):

        self.__dictionary = None

    def dictionary(self, d = None):

        if (d == None): return(self.__dictionary)

        self.__dictionary = d
    #def waveform(self, phase = None, amplitude = None, offsetVolts = 0.1):
    def waveform(self, phase = None, amplitude = None, offsetVolts = 0.0):
        '''
Phase in degrees. Amplitude 0 - 1.0 (maps to 0- 4095). Places data in dictionary.
'modulation_table'.
        '''
        resolution = 10.0 # samples per cycle
        maxDAC = 4095  #
        maxVolts = 2.5 # just at the DAC output.
        if (phase == None and amplitude == None):
            ' Read.'
            wave_data = []
            for i in range(0, int(resolution)):
                wave_data.append(self.dictionary()['modulation_table'][i])

            if (len(wave_data) == 0):
                return None
            w = 2.0 * math.pi/resolution
            s = 0 + 0j
            mean = 0.0
            for n in range(0, int(resolution)):
                s += wave_data[n] * (math.sin(w * n) + math.cos(w * n)*1j)
                mean += wave_data[n]
            mean /= resolution

            phase = math.atan2(s.imag, s.real) * 180.0/math.pi
            amplitudeDACcounts = abs(s) * 2.0 / resolution #< sin(n), sin(n)> = 0.5* n
            amplitude = amplitudeDACcounts * 2.0 / maxDAC
            offsetDACcounts = mean - amplitudeDACcounts # minima in DAC counts
            offsetVolts = offsetDACcounts * maxVolts/maxDAC
            return((phase, amplitude, offsetVolts))

        elif (phase != None and amplitude != None):
            wave_data = []
            phase = phase * math.pi/180.0
            A = maxDAC * amplitude / 2.0
            SineCenter = A + offsetVolts * maxDAC/maxVolts

            for i in range(0, int(resolution)):
                angle = 2.0 * math.pi * i/resolution
                wave_data.append(round(math.sin(angle + phase) * A + SineCenter))
            for i in range(0, int(resolution)):
                self.dictionary()['modulation_table'][i] = int(wave_data[i])
        else:
            print 'Invalid phase/amplitude'

