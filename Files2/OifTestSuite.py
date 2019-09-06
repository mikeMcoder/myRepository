import math
import struct
import sys
import os
import time
import instrumentDrivers as inst
import ConfigParser as parser
sys.path.append(os.path.abspath('.'))

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'

import aa_gpio.gpio
g = aa_gpio.gpio.gpio()
g.InitPin()

laser = 0
baud = 115200

sys.path.append(os.path.abspath('.'))
port = 3#int(input('Please Enter Port:'))


def turnOnpowersupplies():
    ps = inst.psAG3631('gpib0::06')
    ps.connect()
    ps.setOutputState(state='ON')
    return ps

def turnOffpowersupplies(ps):
    ps.setOutputState(state='OFF')
    
#GENERAL MODULE COMMANDS
def NOP_Test():
    #Register 0x00 R/W
    #pesudocode
    #Turn on laser
    it.resena(0)
    time.sleep(1)
    it.resena(1)
    pending = hex(it.nop()[1].data())
    #Poll it.nop() until 0x10
    while pending != '0x10L':
        pending = hex(it.nop()[1].data())
        print pending
        time.sleep(1)
    #if successfuly tune and readi 0x10 then pass
        if pending == '0x10L':
            print 'PASS 0x00 FUNCTIONAL'
            break
    

def DevTyp_Test(file):
    #Register 0x01 R
    #pseudocode
    #connect to unit
    #call it.DevTyp
    #validate must read 'OK' and type is correct
    #PASS if good
    
    #call it.DevTyp
    devTyp = it.devTyp()
    print devTyp
    #validate must read 'OK' and type is correct
    file.write('REGISTER 0X01:' + str(devTyp) + '\n')

    
def MFGR_Test(file):
    #Register 0x02 R
    mfgr = it.mfgr()
    print "READ 0X02 REGISTER"
    print mfgr
    if mfgr ==  ('OK', (6L, 'Emcore')):
        print 'PASS: CORRECT MFGR READING'
    else:
        print 'FAILED NOT CORRECT READING'
    file.write('REGISTER 0X02:' + str(mfgr)+'\n')
    
        
def Model_Test(file):
    #Register 0x03 R
    model = it.model()
    print "READ 0X03 REGISTER"
    print model
    if model ==  ('OK', (16L, 'TTX199575900N00\x00')):
        print 'PASS: CORRECT MODEL READING'
    else:
        print 'FAILED NOT CORRECT READING'
    file.write('REGISTER 0X03:' +str(model) + '\n')
def SerNo_Test(file):
    #Register 0x04 R
    serNo = it.serNo()
    print serNo
    file.write('REGISTER 0X04:' +str(serNo) + '\n')
def MFGDate_Test(file):
    #Register 0x05 R
    MFGDate= it.mfgDate()
    print MFGDate
    file.write('REGISTER 0X05:' +str(MFGDate) + '\n')
def Release_Test(file):
    #Register 0x06 R
    release = it.release()
    print it.release()
    #print it.release(1)
    file.write('REGISTER 0X06:' +str(release) + '\n')
def RelBack_Test(file):
    #Register 0x07 R
    relBack = it.relBack()
    print it.relBack()
    file.write('REGISTER 0X07:' +str(relBack) + '\n')
def GenCfg_Test():
    #Register 0x08 R/W
    pass
def AEA_EAC_Test(file):
    #Register 0x09 R
    aeaEac = it.aeaEac()
    print it.aeaEac()
    file.write('REGISTER 0X09:' +str(aeaEac) + '\n')
def AEA_EA_Test(file):
    #Register 0x0A R
    aeaEa = it.aeaEa()
    print it.aeaEa()
    file.write('REGISTER 0X0A:' +str(aeaEa) + '\n')
def AEA_EAR_Test(file):
    #Register 0x0B R/W
    pass
def IOCap_Test(file):
    #Register 0x0D R/W
    pass
def EAC_Test(file):
    #Register 0x0E R/W
    pass
def EA_Test(file):
    #Register 0x0F R/W
    pass
def EAR_Test(file):
    #Register 0x10 R/W
    pass
def LstResp_Test(file):
    #Register 0x13 R
    lstResp = it.lstResp()
    print it.lstResp()
    file.write('REGISTER 0X13:' +str(lstResp) + '\n')
def DLConfig_Test(file):
    #Register 0x14 R/W
    pass
def DLSatus_Test(file):
    #Register 0x15 R
    dlStatus = it.dlStatus()
    print it.dlStatus()
    file.write('REGISTER 0X15:' +str(dlStatus) + '\n')


#MODULE STATUS COMMANDS
def StatusF_Test():
    #Register 0x20 R/W
    pass
def StatusW_Test():
    #Register 0x21 R/W
    pass
def FPowTh_Test():
    #Register 0x22 R/W
    pass
def WPowTh_Test():
    #Register 0x23 R/W
    pass
def FFreqTh_Test():
    #Register 0x24 R/W
    pass
def WFreqTh_Test():
    #Register 0x25 R/W
    pass
def FThermTh_Test():
    #Register 0x26 R/W
    pass
def WThermTh_Test():
    #Register 0x27 R/W
    pass
def SRQT_Test():
    #Register 0x28 R/W
    pass
def FatalT_Test():
    #Register 0x29 R/W
    pass
def ALMT_Test():
    #Register 0x2A R/W
    pass



#MODULE OPTICAL COMMANDS
def Channel_Test():
    #Register 0x30 R/W
    pass
def PWR_Test():
    #Register 0x31 R/W
    pass
def ResEna_Test():
    #Register 0x32 R/W
    pass
def MCB_Test():
    #Register 0x33 R/W
    pass
def GRID_Test():
    #Register 0x34 R/W
    pass
def FCF1_Test():
    #Register 0x35 R/W
    pass
def FCF2_Test():
    #Register 0x36 R/W
    pass
def LF1_Test(file):
    #Register 0x40 R
    lf = it.lf()
    print it.lf()
    file.write('REGISTER 0X40:' +str(lf) + '\n')
def LF2_Test():
    #Register 0x41 R
    pass
def OOP_test(file):
    oop = it.oop()
    print it.oop()
    #Register 0x42 R
    file.write('REGISTER 0X42:' +str(oop) + '\n')
def CTemp_Test(file):
    #Register 0x43 R
    CTemp = it.ctemp()
    print it.ctemp()
    file.write('REGISTER 0X43:' +str(CTemp) + '\n')


#MODULE CAPABILITIES
def FTFR_Test(file):
    #Register 0x4F R
    ftfr = it.ftfr()
    print it.ftfr()
    file.write('REGISTER 0X4F:' +str(ftfr) + '\n')
def OPSL_Test(file):
    #Register 0x50 R
    opsl = it.opsl()
    print it.opsl()
    file.write('REGISTER 0X50:' +str(opsl) + '\n')
def OPSH_Test(file):
    #Register 0x51 R
    opsh = it.opsh()
    print it.opsh()
    file.write('REGISTER 0X51:' +str(opsh) + '\n')
def LFL1_Test(file):
    #Register 0x52 R
    lfl=it.lfl()
    print it.lfl()
    file.write('REGISTER 0X52:' +str(lfl) + '\n')
def LFL2_Test():
    #Register 0x53 R
    pass
def LFH1_Test(file):
    #Register 0x54 R
    lfh = it.lfh()
    print it.lfh()
    file.write('REGISTER 0X54:' +str(lfh) + '\n')
def LFH2_Test():
    #Register 0x55 R
    pass
def LGrid_Test(file):
    #Register 0x56 R
    grid = it.lgrid()
    print it.lgrid()
    file.write('REGISTER 0X56:' +str(grid) + '\n')

def Buildstring_Test(file):
    #Register 0x56 R
    bs = it.buildstring()
    print bs
    file.write('REGISTER buildstring:' +str(bs) + '\n')    


#MSA COMMANDS
def Currents_Test(file):
    #Register 0x57 R
    currents = it.currents()
    print it.currents()
    file.write('REGISTER 0X57:' +str(currents) + '\n')
def Temps_Test(file):
    #Register 0x58 R
    temps = it.temps()
    print it.temps()
    file.write('REGISTER 0X58:' +str(temps) + '\n')
def DitherE_Test():
    #Register 0x59 R/W
    pass
def DitherR_Test():
     #Register 0x5A R/W
    pass
def DitherF_Test():
    #Register 0x5B R/W
    pass
def DitherA_Test():
    #Register 0x5C R/W
    pass

def TBTFL_Test():
    #Register 0x5D R/W
    pass
def TBTFH_Test():
    #Register 0x5E R/W
    pass
def FAgeTh_Test():
    #Register 0x5F R/W
    pass
def WAgeTh_Test():
    #Register 0x60 R/W
    pass
def Age_Test(file):
    #Register 0x61 R
    age = it.age()
    print it.age()
    file.write('REGISTER 0X61:' +str(age) + '\n')
def FTF_Test():
    #Register 0x62 R/W
    pass
def createFile():
    file = open('Results.txt','w')
    file.write('TestResults'+ '\n')
    return file
                               
    
def runCase1():
    ps = turnOnpowersupplies()
    time.sleep(2)
    ###MAIN###
    #it.laser(laser)
    it.connect(port,baud)
    it.debugRS232(0)
    time.sleep(1)

    file = createFile()
    #NOP_Test()
    print 'Register 0x01 DevTyp'
    DevTyp_Test(file)
    print 'Register 0x02 MFGR'
    MFGR_Test(file)
    print 'Register 0x03 Model'
    Model_Test(file)
    print 'Register 0x04 SerNo'
    SerNo_Test(file)
    print 'Register 0x05 MFGDate'
    MFGDate_Test(file)
    print 'Register 0x06 Release'
    Release_Test(file)
    print 'Register 0x07 RelBack'
    RelBack_Test(file)
    print 'Register 0x09 AEA_EAC'
    AEA_EAC_Test(file)
    print 'Register 0x0A AEA_EA'
    AEA_EA_Test(file)
    print 'Register 0x13 LstResp'
    LstResp_Test(file)
    print 'Register 0x15 DLSatus'
    DLSatus_Test(file)
    print 'Register 0x40 LF1'
    LF1_Test(file)
    print 'Register 0x42 OOP'
    OOP_test(file)
    print 'Register 0x43 Ctemp'
    CTemp_Test(file)
    print 'Register 0x4F FTFR'
    FTFR_Test(file)
    print 'Register 0x50 OPSL'
    OPSL_Test(file)
    print 'Register 0x51 OPSH'
    OPSH_Test(file)
    print 'Register 0x52 LFL1'
    LFL1_Test(file)
    print 'Register 0x53 LFH1'
    LFH1_Test(file)
    print 'Register 0x56 LGrid'
    LGrid_Test(file)
    print 'Register 0x57 Currents'
    Currents_Test(file)
    print 'Register 0x58 Temps'
    Temps_Test(file)
    print 'Register 0x61 Age'
    Age_Test(file)
    file.close()
    it.disconnect()
    print "TEST COMPLETE"
    turnOffpowersupplies(ps)

if __name__== '__main__':
    runCase1()
    








    