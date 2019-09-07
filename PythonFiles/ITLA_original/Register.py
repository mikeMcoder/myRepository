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

    $Source: /data/development/cvs/Sundial2/Python/ITLA/Register.py,v $
    $Revision: 1.8 $
    $Date: 2008/04/09 22:01:32 $
    $Name: Sundial2_01_03_00_01 $
    
'''
from BitField import BitField
import copy
import struct
import types

class Register:

    def __init__(self, address = 0, data = 0):
        self.__buffer = ''
        self.__bitfield = BitField('Register', 24)
        self.__bitfield.addChild(BitField('Address', 8, 16))
        self._data = BitField('Data', 16, 0)
        self.__bitfield.addChild(self._data)

        self.__initialize(address)
        self.data(data)
        
    def __repr__(self):
        message = repr(self.__bitfield) + '\n'
        data = repr(self._data).split('\n')
        # All children of data
        for i in data[1:]:
            message += ' ' * 8 + i + '\n'
        return message

    def __str__(self):
        return self.__repr__()
    
    def __initialize(self, value):
        self.__bitfield['Address'].value(value)
        self.__header = []
        try:
            self.__bitfield['Address'].name(nameDictionary()[value][0])

            fields = nameDictionary()[value]
            if type(fields) == types.ListType and len(fields) > 1:
                for field in fields[1]:
                    # print 'field', field
                    if len(field) == 3:
                        b = BitField(field[0], field[1], field[2])
                    else:
                        b = BitField(field[0], field[1], field[2], field[3])
                    self._data.addChild(b)
                    self.__header.append(field[0])
                    name = field[0].split('_')

                    function_name = 'field'
                    for i in name:
                        function_name += i.lower().title()

                    function = 'def %s(self, value = None): \n' % (function_name)
                    function += '    if value == None:\n'
                    function += '        return self._data[\'%s\']\n' % (field[0])
                    function += '    self._data[\'%s\'] = value\n' % (field[0])
                    exec function in self.__class__.__dict__
        except:
            self.__bitfield['Address'].name(hex(value))

    def buffer(self):
        l = list(self.__bitfield.toString())

        # Convert to big endian for transmission.
        l.reverse()
        return(''.join(l))


    def name(self): return self.__bitfield['Address'].name()

    def address(self):
        return self.__bitfield['Address'].value()
        
    def data(self, value = None):
        if value == None:
            return self._data.value()
        else:
            if value < 0:
                value = value & 0xffff
            self._data.value(value)

    def header(self):
        return self.__header

''' The following register definition is based on the document OIF-ITLA-MSA-01.0 '''
def nameDictionary():
    return {0x00 : ['NOP',
                    [
                        ['PENDING', 8, 8],
                        ['LOCKED', 2, 6],
                        ['MRDY', 1, 4],
                        ['ERROR_FIELD', 4, 0,
                            {0x00 : 'OK',
                             0x01 : 'RNI',
                             0x02 : 'RNW',
                             0x03 : 'RVE',
                             0x04 : 'CIP',
                             0x05 : 'CII',
                             0x06 : 'ERE',
                             0x07 : 'ERO',
                             0x08 : 'EXF',
                             0x09 : 'CIE',
                             0x0A : 'IVC',
                             0x0F : 'VSE'}] ] ],
            0x01 : ['DEVTYP'],
            0x02 : ['MFGR'],
            0x03 : ['MODEL'],
            0x04 : ['SERNO'],
            0x05 : ['MFGDATE'],
            0x06 : ['RELEASE'],
            0x07 : ['RELBACK'],
            0x08 : ['GENCFG',
                    [
                        ['SDC', 1, 15],
                        ['RCS', 1, 0] ] ],
            0x09 : ['AEA_EAC',
                    [
                        ['RAI', 2, 14,
                            {
                                0x0 : 'No address change',
                                0x1 : 'Address auto post increment by INCR',
                                0x2 : 'Address auto post decrement by INCR',
                                0x3 : 'Undefined' }],
                        ['WAI', 2, 12,
                            {
                                0x0 : 'No address change',
                                0x1 : 'Address auto post increment by INCR',
                                0x2 : 'Address auto post decrement by INCR',
                                0x3 : 'Undefined' }],
                        ['EAM', 3, 9],
                        ['INCR', 2, 7],
                        ['HIGH_ORDER_ADDRESS', 6, 0] ] ],
            0x0A : ['AEA_EA'],
            0x0B : ['AEA_EAR'],
            0x0D : ['IOCAP',
                    [
                        ['RMS', 1, 12],
                        ['CURRENT_BAUD_RATE', 4, 4,
                            {
                                0x0 : '9600',
                                0x1 : '19200',
                                0x2 : '38400',
                                0x3 : '57600',
                                0x4 : '115200',
                                0x7 : '230400'
                            } ],
                        ['SUPPORTED_BAUD_RATE', 4, 0,
                            {
                                0x0 : '9600',
                                0x1 : '19200',
                                0x2 : '38400',
                                0x3 : '57600',
                                0x4 : '115200'
                            } ] ] ],
            0x0E : ['EAC',
                    [
                        ['RAI', 2, 14],
                        ['WAI', 2, 12],
                        ['EAM', 3, 9],
                        ['INCR', 2, 7],
                        ['HIGH_ORDER_ADDRESS', 6, 0] ] ],
            0x0F : ['EA'],
            0x10 : ['EAR'],
            0x11 : ['WCRC'],
            0x12 : ['RCRC'],
            0x13 : ['LSTRESP'],
            0x14 : ['DLCONFIG',
                    [
                        ['TYPE', 4, 12,
                            {
                                0x00 : 'NO CHANGE',
                                0x01 : 'Non-Service Interrupting 1',
                                0x02 : 'Non-Service Interrupting 2',
                                0x03 : 'Service Interrupting A',
                                0x04 : 'Service Interrupting B'} ],
                        ['RUNV', 4, 8,
                            {
                                0x00 : 'NO CHANGE',
                                0x01 : 'Non-Service Interrupting 1',
                                0x02 : 'Non-Service Interrupting 2',
                                0x03 : 'Service Interrupting A',
                                0x04 : 'Service Interrupting B'} ],
                        ['INIT_RUN', 1, 5],
                        ['INIT_CHECK', 1, 4],
                        ['INIT_READ', 1, 3],
                        ['DONE', 1, 2],
                        ['ABRT', 1, 1],
                        ['INIT_WRITE', 1, 0] ] ],
            0x15 : ['DLSTATUS',
                    [
                        ['IN_USE', 1, 1],
                        ['VALID', 1, 0] ] ],
            0x16 : ['LOCK'],
            0x20 : ['STATUSF',
                    [
                        ['SRQ', 1, 15],
                        ['ALM', 1, 14],
                        ['FATAL', 1, 13],
                        ['DIS', 1, 12],
                        ['FVSF', 1, 11],
                        ['FFREQ', 1, 10],
                        ['FTHERM', 1, 9],
                        ['FPWR', 1, 8],
                        ['XEL', 1, 7],
                        ['CEL', 1, 6],
                        ['MRL', 1, 5],
                        ['CRL', 1, 4],
                        ['FVSFL', 1, 3],
                        ['FFREQL', 1, 2],
                        ['FTHERML', 1, 1],
                        ['FPWRL', 1, 0] ] ],
            0x21 : ['STATUSW',
                    [
                        ['SRQ', 1, 15],
                        ['ALM', 1, 14],
                        ['FATAL', 1, 13],
                        ['DIS', 1, 12],
                        ['WVSF', 1, 11],
                        ['WFREQ', 1, 10],
                        ['WTHERM', 1, 9],
                        ['WPWR', 1, 8],
                        ['XEL', 1, 7],
                        ['CEL', 1, 6],
                        ['MRL', 1, 5],
                        ['CRL', 1, 4],
                        ['WVSFL', 1, 3],
                        ['WFREQL', 1, 2],
                        ['WTHERML', 1, 1],
                        ['WPWRL', 1, 0] ] ],
            0x22 : ['FPOWTH'],
            0x23 : ['WPOWTH'],
            0x24 : ['FFREQTH'],
            0x25 : ['WFREQTH'],
            0x26 : ['FTHERMTH'],
            0x27 : ['WTHERMTH'],
            0x28 : ['SRQT',
                    [
                        ['DIS', 1, 12],
                        ['WVSFL', 1, 11],
                        ['WFREQL', 1, 10],
                        ['WTHERML', 1, 9],
                        ['WPWRL', 1, 8],
                        ['XEL', 1, 7],
                        ['CEL', 1, 6],
                        ['MRL', 1, 5],
                        ['CRL', 1, 4],
                        ['FVSFL', 1, 3],
                        ['FFREQL', 1, 2],
                        ['FTHERML', 1, 1],
                        ['FPWRL', 1, 0] ] ],
            0x29 : ['FATALT',
                    [
                        ['WVSFL', 1, 11],
                        ['WFREQL', 1, 10],
                        ['WTHERML', 1, 9],
                        ['WPWRL', 1, 8],
                        ['MRL', 1, 5],
                        ['FVSFL', 1, 3],
                        ['FFREQL', 1, 2],
                        ['FTHERML', 1, 1],
                        ['FPWRL', 1, 0] ] ],
            0x2A : ['ALMT',
                    [
                        ['WVSF', 1, 11],
                        ['WFREQ', 1, 10],
                        ['WTHERM', 1, 9],
                        ['WPWR', 1, 8],
                        ['FVSF', 1, 3],
                        ['FFREQ', 1, 2],
                        ['FTHERM', 1, 1],
                        ['FPWR', 1, 0] ] ],
            0x30 : ['CHANNEL'],
            0xEA : ['GMISLOPE'],
            0x31 : ['PWR'],
            0x32 : ['RESENA',
                    [
                        ['SENA', 1, 3],
                        ['SR', 1, 1],
                        ['MR', 1, 0] ] ],
            0x33 : ['MCB',
                    [
                        ['SDF', 1, 2],
                        ['ADT', 1, 1],
                        ['ADO', 1, 3] ] ],
            0x34 : ['GRID'],
            0x35 : ['FCF1'],
            0x36 : ['FCF2'],
            0x40 : ['LF1'],
            0x41 : ['LF2'],
            0x42 : ['OOP'],
            0x43 : ['CTEMP'],
            0x4F : ['FTFR'],
            0x50 : ['OPSL'],
            0x51 : ['OPSH'],
            0x52 : ['LFL1'],
            0x53 : ['LFL2'],
            0x54 : ['LFH1'],
            0x55 : ['LFH2'],
            0x56 : ['LGRID'],
            0x57 : ['CURRENTS'],
            0x58 : ['TEMPS'],
            0x59 : ['DITHERE',
                    [
                        ['WF', 2, 4],
                        ['DE', 2, 0] ] ],
            0x5A : ['DITHERR'],
            0x5B : ['DITHERF'],
            0x5C : ['DITHERA'],
            0x5D : ['TBTFL'],
            0x5E : ['TBTFH'],
            0x5F : ['FAGETH'],
            0x60 : ['WAGETH'],
            0x61 : ['AGE'],
            0x62 : ['FTF'],
            0x88 : ['DEBUG',
                    [
                        ['WORD_INDEX', 1, 15,
                            {
                                0x00 : 'Low',
                                0x01 : 'High' } ],
                        ['ADDRESS', 15, 0] ] ],
            0x89 : ['HEALTH',
                    [
                        ['SLED_TEMPERATURE_RANGE_EXCEEDED', 1, 0],
                        ['FILTER1_TEMPERATURE_RANGE_EXCEEDED', 1, 1],
                        ['FILTER2_TEMPERATURE_RANGE_EXCEEDED', 1, 2],
                        ['FREQUENCY_SHIFT_RANGE_EXCEEDED', 1, 3],
                        ['POWER_WARNING', 1, 4],
                        ['TEMPERATURE_WARNING', 1, 5],
                        ['FREQUENCY_WARNING', 1, 6],
                        ['BIAS_CURRENT_WARNING', 1, 7],
                        ['RST_PIN_ASSERTED', 1, 8],
                        ['PON_OR_VDD_MON_RST', 1, 9],
                        ['MISSING_CLOCK_DET_TMO', 1, 10],
                        ['WD_TIMER_ASSERTED', 1, 11],
                        ['SW_RESET', 1, 12],
                        ['CMP0_RESET', 1, 13],
                        ['CNVSTR0_RESET', 1, 14],
                        ['N/A', 1, 15], ]],
            0x92 : ['DBG_RESET',
                     [
                        ['SOURCE', 9, 0,
                            {   
                                0x01 : 'RST_PIN_RESET',
                                0x02 : 'PWR_ON_RESET',
                                0x04 : 'MISSING_CLK_RESET',
                                0x08 : 'WATCHDOG_RESET',
                                0x10 : 'SOFT_RESET',
                                0x20 : 'COMP0_RESET',
                                0x40 : 'FLASH_ERR_RESET',
                                0x80 : 'HITLESS_SW_RESET',
                                0x100 : 'HITLESS_WD_RESET',                               
                            } ]]],
            0xA0 : ['DBG_ACR'],
            0xF2 : ['NOP_STATS',
                    [
                        ['STATE_MACH', 4, 0,
                            {   
                                0x00 : 'COLD_START',
                                0x01 : 'IDLE',
                                0x02 : 'DARK',
                                0x03 : 'TEMPERATURE',
                                0x04 : 'GAIN_MEDIUM',
                                0x05 : 'ADJUSTMENT',
                                0x06 : 'FIRST_LIGHT',
                                0x07 : 'CAVITY_LOCK',
                                0x08 : 'POWER_LEVEL',
                                0x09 : 'CAVITY_OFFS_LOCK',
                                0x0A : 'STABILIZE',
                                0x0B : 'CHANNEL_LOCK',
                                0x0C : 'FINE_TUNE',
                                0x0D : 'MZM_STATE',
                                0x0E : 'ERROR_xE',
                                0x0F : 'ERROR_xF'} ],
                        ['HEALTH_SERVICE', 4, 4],
                        ['TUNER_MASK', 1, 8],
                        ['TUNER_PENDING', 1, 9],
                        ['PWR_WARNING', 1, 10],
                        ['PWR_TUNING', 1, 11],
                        ['FREQ_TUNING', 1, 12],
                        ['FTF_STARTED', 1, 13],
                        ['NOP_PEND_CH', 1, 14],
                        ['NOP_PEND_LOCK', 1, 15] ] ],
            0xF3 : ['DBG_TEMPS'],
            0xFF : ['MONITOR'],
        }

# Create constants for register addresses
for __i in nameDictionary():
    __v =  nameDictionary()[__i][0]
    exec '%s = %i' % (__v, __i)


if __name__ == '__main__':
    r = Register(NOP)
    print r
    r.data(0xffff)
    print r
    r.fieldErrorField('RVE')
    r.fieldLocked(1)
    r.fieldMrdy(0)
    r.fieldPending(0xe)
    print r
    raise 'stop'
    print Register(NOP, 0xffff)
    print Register(DEVTYP)
    print Register(MFGR)
    print Register(MODEL)
    print Register(SERNO)
    print Register(MFGDATE)
    print Register(RELEASE)
    print Register(RELBACK)
    print Register(GENCFG)
    print Register(GENCFG, 0xffff)
    print Register(AEA_EAC)
    print Register(AEA_EAC, 0xffff)
    print Register(AEA_EA)
    print Register(AEA_EA, 0xffff)
    print Register(AEA_EAR)
    print Register(AEA_EAR, 0xffff)
    print Register(IOCAP)
    print Register(IOCAP, 0xffff)
    print Register(EAC)
    print Register(EAC, 0xffff)
    print Register(EA)
    print Register(EA, 0xffff)
    print Register(EAR)
    print Register(EAR, 0xffff)
    print Register(WCRC)
    print Register(WCRC, 0xffff)
    print Register(RCRC)
    print Register(LSTRESP)
    print Register(DLCONFIG)
    print Register(DLCONFIG, 0xffff)
    print Register(DLSTATUS)
    print Register(LOCK)
    print Register(LOCK, 0xffff)
    print Register(STATUSF)
    print Register(STATUSF, 0xffff)
    print Register(STATUSW)
    print Register(STATUSW, 0xffff)
    print Register(FPOWTH)
    print Register(FPOWTH, 0xFEED)
    print Register(WPOWTH)
    print Register(WPOWTH, 0xFEED)
    print Register(FFREQTH)
    print Register(FFREQTH, 0xFEED)
    print Register(WFREQTH)
    print Register(WFREQTH, 0xFEED)
    print Register(FTHERMTH)
    print Register(FTHERMTH, 0xFEED)
    print Register(WTHERMTH)
    print Register(WTHERMTH, 0xFEED)
    print Register(SRQT)
    print Register(SRQT, 0xffff)
    print Register(FATALT)
    print Register(FATALT, 0xffff)
    print Register(ALMT)
    print Register(ALMT, 0xffff)
    print Register(CHANNEL)
    print Register(CHANNEL, 0xFEED)
    print Register(PWR)
    print Register(PWR, 0xFEED)
    print Register(RESENA)
    print Register(RESENA, 0xffff)
    print Register(MCB)
    print Register(MCB, 1)
    print Register(GRID)
    print Register(GRID, 0xFEED)
    print Register(FCF1)
    print Register(FCF1, 0xFEED)
    print Register(FCF2)
    print Register(FCF2, 0xFEED)
    print Register(LF1)
    print Register(LF1, 0xFEED)
    print Register(LF2)
    print Register(LF2, 0xFEED)
    print Register(OOP)
    print Register(CTEMP)
    print Register(FTFR)
    print Register(OPSL)
    print Register(OPSH)
    print Register(LFL1)
    print Register(LFL2)
    print Register(LFH1)
    print Register(LFH2)
    print Register(LGRID)
    print Register(CURRENTS)
    print Register(TEMPS)
    print Register(DITHERE)
    print Register(DITHERE, 1)
    print Register(DITHERR)
    print Register(DITHERR, 1)
    print Register(DITHERF)
    print Register(DITHERF, 1)
    print Register(DITHERA)
    print Register(DITHERA, 1)
    print Register(TBTFL)
    print Register(TBTFL, 0xFEED)
    print Register(TBTFH)
    print Register(TBTFH, 0xFEED)
    print Register(FAGETH)
    print Register(FAGETH, 0xBEEF)
    print Register(WAGETH)
    print Register(WAGETH, 0xBEEF)
    print Register(AGE)
    print Register(USER1)
    print Register(USER1, 0xBEEF)
    
