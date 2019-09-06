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



def timeStamp():
    daytime = time.asctime()
    daytimestr = daytime.replace(' ','')
    daytimestr = daytimestr.replace(':','')
    return daytimestr



def pendingClear():
    '''Function to monitor pending operation'''
    print 'Waiting for pending bit to clear...'
    it.setpassword()
    timeOut = 2000
    starttime = time.time()
    duration = time.time() - starttime
    while duration < timeOut:
        pendingBit = str(int(it.nop()[1].fieldPending().value()))
        it.logentry(time.asctime())
        reg99 = it.readx99()
        it.lf()
        it.statusF()
        it.statusW()
        it.logentry(time.asctime())
        if pendingBit == '0':
            reg99 = it.readx99()
            print "Pending bit Cleared..."
            tuneTime = duration
            break
        duration = time.time() - starttime
        if duration >=timeOut:
            it.logentry(time.asctime())
            reg99 = it.readx99()
            print it.temps()
            print it.currents()
            print it.statusF()
            print it.statusW()
            print it.readx99()
            raise "Tunetime more than 60 seconds: Stop Test"
    print 'TUNETIME:',tuneTime
    return tuneTime


def turnOnpowersupplies():
    ps = inst.psAG3631('gpib0::06')
    ps.connect()
    ps.setOutputState(state='ON')
    return ps

def turnOffpowersupplies(ps):
    ps.setOutputState(state='OFF')
    
#GENERAL MODULE COMMANDS
   


        

##    
##def MFGR_Test(file):
##    #Register 0x02 R
##    mfgr = it.mfgr()
##    print "READ 0X02 REGISTER"
##    print mfgr
##    if mfgr ==  ('OK', (6L, 'Emcore')):
##        print 'PASS: CORRECT MFGR READING'
##    else:
##        print 'FAILED NOT CORRECT READING'
##    file.write('REGISTER 0X02:' + str(mfgr)+'\n')
    
        
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
    file = open('ReadOnlyRegisterTestResults.txt','w')
    file.write('#####################ReadOnlyRegisterTestResults###########################'+ '\n')
    return file

def createNewDirectory(name= 'TEST'):
    time = timeStamp()
    currentDirectory= os.getcwd()
    name = name + '_' + time
    newPath = currentDirectory + '\\' + name
    if not os.path.exists(newPath):
        os.mkdir(newPath)
    return newPath



def DevTyp_Test(file1, path):

    try:
        

        print "==> Device Type Case: 1 Read the Register"
        file1.write('==> Device Type Case: 1 Read the Register"\n')
        devTyp = it.devTyp()
        print '==> REGISTER 0X01:' + str(devTyp)
        file1.write('==> REGISTER 0X01:' + str(devTyp) + '\n')
        file1.write('\n')
        file1.write('\n')

    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'


    try:
            
        print "==> Device Type Case: 2 Read the Register 100x"
        file1.write('==> Device Type Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            devTyp = it.devTyp()
            print ('==> ITERATION: %d REGISTER 0X01:'%i + str(devTyp) + '\n')
            file1.write('==> ITERATION: %d REGISTER 0X01:'%i + str(devTyp) + '\n')
        file1.write('\n')
        file1.write('\n')


    except Exception as e:
         print e.message
         raise "Stop"
    
   
    try:

        print '\n'
        print "==> Device Type Case: 3 Write to Register"
        try:
            result = it.devTyp(-1)
        except:
            pass
        
        file1.write('==> REGISTER 0X01: Cannot Write to Register \n')
        print '\n'
        file1.close()

    except Exception as e:
         print e.message
         raise "Stop"




def MFGR_Test(file2, path):

    
    try:
        
        print "==> MFGR Case: 1 Read the Register"
        file2.write('==> MFGR Case: 1 Read the Register"\n')
        mfgr = it.mfgr()
        print '==> REGISTER 0X02:' + str(mfgr)
        file2.write('==> REGISTER 0X02:' + str(mfgr) + '\n')
        file2.write('\n')
        file2.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> MFGR Case: 2 Read the Register 100x"
        file2.write('==> MFGR Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            mfgr = it.mfgr()
            print ('==> ITERATION: %d REGISTER 0X02:'%i + str(mfgr) + '\n')
            file2.write('==> ITERATION: %d REGISTER 0X02:'%i + str(mfgr) + '\n')
        file2.write('\n')
        file2.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> MFGR Case: 3 Write to Register"
        try:
            result = it.mfgr(-1)
        except:
            pass
        
        file2.write('==> REGISTER 0X02: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"





def Model_Test(file3, path):

    
    try:
        
        print "==> Model Case: 1 Read the Register"
        file3.write('==> Model Case: 1 Read the Register"\n')
        model = it.model()
        print '==> REGISTER 0X03:' + str(model)
        file3.write('==> REGISTER 0X03:' + str(model) + '\n')
        file3.write('\n')
        file3.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> Model Case: 2 Read the Register 100x"
        file3.write('==> Model Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            model = it.model()
            print ('==> ITERATION: %d REGISTER 0X03:'%i + str(model) + '\n')
            file3.write('==> ITERATION: %d REGISTER 0X03:'%i + str(model) + '\n')
        file3.write('\n')
        file3.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> Model Case: 3 Write to Register"
        try:
            result = it.model(-1)
        except:
            pass
        
        file3.write('==> REGISTER 0X03: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"






def SerNo_Test(file4, path):

    
    try:
        
        print "==> Model Case: 1 Read the Register"
        file4.write('==> Model Case: 1 Read the Register"\n')
        serNo = it.serNo()
        print '==> REGISTER 0X04:' + str(serNo)
        file4.write('==> REGISTER 0X04:' + str(serNo) + '\n')
        file4.write('\n')
        file4.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> Model Case: 2 Read the Register 100x"
        file4.write('==> Model Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            serNo = it.serNo()
            print ('==> ITERATION: %d REGISTER 0X04:'%i + str(serNo) + '\n')
            file4.write('==> ITERATION: %d REGISTER 0X04:'%i + str(serNo) + '\n')
        file4.write('\n')
        file4.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> Model Case: 3 Write to Register"
        try:
            result = it.serNo(-1)
        except:
            pass
        
        file4.write('==> REGISTER 0X04: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"






def MFGDate_Test(file5, path):

    
    try:
        
        print "==> MFGDate Case: 1 Read the Register"
        file5.write('==> MFGDate Case: 1 Read the Register"\n')
        mfgdate = it.mfgDate()
        print '==> REGISTER 0X05:' + str(mfgdate)
        file5.write('==> REGISTER 0X05:' + str(mfgdate) + '\n')
        file5.write('\n')
        file5.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> MFGDate Case: 2 Read the Register 100x"
        file5.write('==> MFGDate Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            mfgdate = it.mfgDate()
            print ('==> ITERATION: %d REGISTER 0X05:'%i + str(mfgdate) + '\n')
            file5.write('==> ITERATION: %d REGISTER 0X05:'%i + str(mfgdate) + '\n')
        file5.write('\n')
        file5.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> MFGDate Case: 3 Write to Register"
        try:
            result = it.mfgDate(-1)
        except:
            pass
        
        file5.write('==> REGISTER 0X05: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"





def Release_Test(file6, path):

    
    try:
        
        print "==> Release Case: 1 Read the Register"
        file6.write('==> Release Case: 1 Read the Register"\n')
        release = it.release()
        print '==> REGISTER 0X06:' + str(release)
        file6.write('==> REGISTER 0X06:' + str(release) + '\n')
        file6.write('\n')
        file6.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> Release Case: 2 Read the Register 100x"
        file6.write('==> Release Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            release = it.release()
            print ('==> ITERATION: %d REGISTER 0X06:'%i + str(release) + '\n')
            file6.write('==> ITERATION: %d REGISTER 0X06:'%i + str(release) + '\n')
        file6.write('\n')
        file6.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> Release Case: 3 Write to Register"
        try:
            result = it.release(-1)
        except:
            pass
        
        file6.write('==> REGISTER 0X03: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"




def Relback_Test(file7, path):

    
    try:
        
        print "==> Relback Case: 1 Read the Register"
        file7.write('==> Relback Case: 1 Read the Register"\n')
        relback = it.relBack()
        print '==> REGISTER 0X07:' + str(relback )
        file7.write('==> REGISTER 0X07:' + str(relback) + '\n')
        file7.write('\n')
        file7.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> Relback Case: 2 Read the Register 100x"
        file7.write('==> Relback Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            relback = it.relBack()
            print ('==> ITERATION: %d REGISTER 0X07:'%i + str(relback) + '\n')
            file7.write('==> ITERATION: %d REGISTER 0X07:'%i + str(relback) + '\n')
        file7.write('\n')
        file7.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> Relback Case: 3 Write to Register"
        try:
            relback= it.relBack(-1)
        except:
            pass
        
        file7.write('==> REGISTER 0X07: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"


def AEA_EAC_Test(file9, path):

    
    try:
        
        print "==> AEA_EAC Case: 1 Read the Register"
        file9.write('==> AEA_EAC Case: 1 Read the Register"\n')
        AEA_EAC =  it.aeaEac()
        print '==> REGISTER 0X09:' + str(AEA_EAC)
        file9.write('==> REGISTER 0X09:' + str(AEA_EAC) + '\n')
        file9.write('\n')
        file9.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> AEA_EAC Case: 2 Read the Register 100x"
        file9.write('==> AEA_EAC Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            AEA_EAC =  it.aeaEac()
            print ('==> ITERATION: %d REGISTER 0X09:'%i + str(AEA_EAC) + '\n')
            file9.write('==> ITERATION: %d REGISTER 0X09:'%i + str(AEA_EAC) + '\n')
        file9.write('\n')
        file9.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> AEA_EAC Case: 3 Write to Register"
        try:
            result = it.aeaEac(-1)
        except:
            pass
        
        file9.write('==> REGISTER 0X09: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"



def AEA_EA_Test(file10, path):

    
    try:
        
        print "==> AEA_EA Case: 1 Read the Register"
        file10.write('==> AEA_EA Case: 1 Read the Register"\n')
        AEA_EA = it.aeaEa()
        print '==> REGISTER 0X0A:' + str(AEA_EA)
        file10.write('==> REGISTER 0X0A:' + str(AEA_EA) + '\n')
        file10.write('\n')
        file10.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> AEA_EA Case: 2 Read the Register 100x"
        file10.write('==> AEA_EA Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            AEA_EA = it.aeaEa()
            print ('==> ITERATION: %d REGISTER 0X0A:'%i + str(AEA_EA) + '\n')
            file10.write('==> ITERATION: %d REGISTER 0X0A:'%i + str(AEA_EA) + '\n')
        file10.write('\n')
        file10.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> AEA_EA Case: 3 Write to Register"
        try:
            result = it.aeaEa(-1)
        except:
            pass
        
        file10.write('==> REGISTER 0X0A: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"






def LstResp_Test(file13, path):

    
    try:
        
        print "==>  LstResp Case: 1 Read the Register"
        file13.write('==>  LstResp Case: 1 Read the Register"\n')
        LstResp = it.lstResp()
        print '==> REGISTER 0X13:' + str(LstResp)
        file13.write('==> REGISTER 0X13:' + str(LstResp) + '\n')
        file13.write('\n')
        file13.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> LstResp Case: 2 Read the Register 100x"
        file13.write('==> LstResp Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            LstResp = it.lstResp()
            print ('==> ITERATION: %d REGISTER 0X13:'%i + str(LstResp) + '\n')
            file13.write('==> ITERATION: %d REGISTER 0X13:'%i + str(LstResp) + '\n')
        file13.write('\n')
        file13.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> LstResp Case: 3 Write to Register"
        try:
            result = it.lstResp(-1)
        except:
            pass
        
        file13.write('==> REGISTER 0X13: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"








def DLSatus_Test(file15, path):

    
    try:
        
        print "==> DLSatus Case: 1 Read the Register"
        file15.write('==> DLSatus Case: 1 Read the Register"\n')
        DLSatus = it.dlStatus()
        print '==> REGISTER 0X15:' + str(DLSatus)
        file15.write('==> REGISTER 0X15:' + str(DLSatus) + '\n')
        file15.write('\n')
        file15.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> DLSatus Case: 2 Read the Register 100x"
        file15.write('==> DLSatus Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            DLSatus = it.dlStatus()
            print ('==> ITERATION: %d REGISTER 0X15:'%i + str(DLSatus) + '\n')
            file15.write('==> ITERATION: %d REGISTER 0X15:'%i + str(DLSatus) + '\n')
        file15.write('\n')
        file15.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> DLSatus Case: 3 Write to Register"
        try:
            result = it.dlSatus(-1)
        except:
            pass
        
        file15.write('==> REGISTER 0X15: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"



def  LF1_Test(file16, path):

    
    try:
        
        print "==>  LF1 Case: 1 Read the Register"
        file16.write('==>  LF1 Case: 1 Read the Register"\n')
        lf = it.lf()
        print '==> REGISTER 0X40:' + str(lf)
        file16.write('==> REGISTER 0X40:' + str(lf) + '\n')
        file16.write('\n')
        file16.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> LF1 Case: 2 Read the Register 100x"
        file16.write('==> LF1 Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            lf = it.lf()
            print ('==> ITERATION: %d REGISTER 0X40:'%i + str(lf) + '\n')
            file16.write('==> ITERATION: %d REGISTER 0X40:'%i + str(lf) + '\n')
        file16.write('\n')
        file16.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> LF1 Case: 3 Write to Register"
        try:
            result = it.lf(-1)
        except:
            pass
        
        file16.write('==> REGISTER 0X40: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"






def OOP_Test(file17, path):

    
    try:
        
        print "==> OOP Case: 1 Read the Register"
        file17.write('==> OOP Case: 1 Read the Register"\n')
        oop = it.oop()
        print '==> REGISTER 0X42:' + str(oop)
        file17.write('==> REGISTER 0X42:' + str(oop) + '\n')
        file17.write('\n')
        file17.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> OOP Case: 2 Read the Register 100x"
        file17.write('==> OOP Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            oop = it.oop()
            print ('==> ITERATION: %d REGISTER 0X42:'%i + str(oop) + '\n')
            file17.write('==> ITERATION: %d REGISTER 0X42:'%i + str(oop) + '\n')
        file17.write('\n')
        file17.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> OOP Case: 3 Write to Register"
        try:
            result = it.oop(-1)
        except:
            pass
        
        file17.write('==> REGISTER 0X42: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"





def Ctemp_Test(file18, path):

    
    try:
        
        print "==> Ctemp Case: 1 Read the Register"
        file18.write('==> Ctemp Case: 1 Read the Register"\n')
        ctemp = it.ctemp()
        print '==> REGISTER 0X43:' + str(ctemp)
        file18.write('==> REGISTER 0X43:' + str(ctemp) + '\n')
        file18.write('\n')
        file18.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> Ctemp Case: 2 Read the Register 100x"
        file18.write('==> Ctemp Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            ctemp = it.ctemp()
            print ('==> ITERATION: %d REGISTER 0X43:'%i + str(ctemp) + '\n')
            file18.write('==> ITERATION: %d REGISTER 0X43:'%i + str(ctemp) + '\n')
        file18.write('\n')
        file18.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==>  Ctemp Case: 3 Write to Register"
        try:
            result = it.ctemp(-1)
        except:
            pass
        
        file18.write('==> REGISTER 0X43: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"







def FTFR_Test(file19, path):

    
    try:
        
        print "==> FTFR Case: 1 Read the Register"
        file19.write('==> FTFR Case: 1 Read the Register"\n')
        ftfr = it.ftfr()
        print '==> REGISTER 0X4F:' + str(ftfr)
        file19.write('==> REGISTER 0X4F:' + str(ftfr) + '\n')
        file19.write('\n')
        file19.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> FTFR Case: 2 Read the Register 100x"
        file19.write('==> FTFR Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            ftfr = it.ftfr()
            print ('==> ITERATION: %d REGISTER 0X4F:'%i + str(ftfr) + '\n')
            file19.write('==> ITERATION: %d REGISTER 0X4F:'%i + str(ftfr) + '\n')
        file19.write('\n')
        file19.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> FTFR Case: 3 Write to Register"
        try:
            result = it.ftfr(-1)
        except:
            pass
        
        file19.write('==> REGISTER 0X4F: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"






def OPSL_Test(file20, path):

    
    try:
        
        print "==> OPSL Case: 1 Read the Register"
        file20.write('==> OPSL Case: 1 Read the Register"\n')
        opsl = it.opsl()
        print '==> REGISTER 0X50:' + str(opsl)
        file20.write('==> REGISTER 0X50:' + str(opsl) + '\n')
        file20.write('\n')
        file20.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> OPSL Case: 2 Read the Register 100x"
        file20.write('==> OPSL Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            opsl = it.opsl()
            print ('==> ITERATION: %d REGISTER 0X50:'%i + str(opsl) + '\n')
            file20.write('==> ITERATION: %d REGISTER 0X50:'%i + str(opsl) + '\n')
        file20.write('\n')
        file20.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> OPSL Case: 3 Write to Register"
        try:
            result = it.opsl(-1)
        except:
            pass
        
        file20.write('==> REGISTER 0X50: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"





def OPSH_Test(file21, path):

    
    try:
        
        print "==> OPSH Case: 1 Read the Register"
        file21.write('==> OPSH Case: 1 Read the Register"\n')
        opsh = it.opsh()
        print '==> REGISTER 0X51:' + str(opsh)
        file21.write('==> REGISTER 0X51:' + str(opsh) + '\n')
        file21.write('\n')
        file21.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> OPSH Case: 2 Read the Register 100x"
        file21.write('==> OPSH Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            opsh = it.opsh()
            print ('==> ITERATION: %d REGISTER 0X51:'%i + str(opsh) + '\n')
            file21.write('==> ITERATION: %d REGISTER 0X51:'%i + str(opsh) + '\n')
        file21.write('\n')
        file21.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> OPSH Case: 3 Write to Register"
        try:
            result = it.opsh(-1)
        except:
            pass
        
        file21.write('==> REGISTER 0X51: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"







def LFL1_Test(file22, path):

    
    try:
        
        print "==> LFL1 Case: 1 Read the Register"
        file22.write('==> LFL1 Case: 1 Read the Register"\n')
        lfl1= it.lfl()
        print '==> REGISTER 0X52:' + str(lfl1)
        file22.write('==> REGISTER 0X52:' + str(lfl1) + '\n')
        file22.write('\n')
        file22.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> LFL1 Case: 2 Read the Register 100x"
        file22.write('==> LFL1 Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            lfl1= it.lfl()
            print ('==> ITERATION: %d REGISTER 0X52:'%i + str(lfl1) + '\n')
            file22.write('==> ITERATION: %d REGISTER 0X52:'%i + str(lfl1) + '\n')
        file22.write('\n')
        file22.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> LFL1 Case: 3 Write to Register"
        try:
            result = it.lfl(-1)
        except:
            pass
        
        file22.write('==> REGISTER 0X52: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"







def LFH1_Test(file23, path):

    
    try:
        
        print "==> LFH1 Case: 1 Read the Register"
        file23.write('==> LFH1 Case: 1 Read the Register"\n')
        lfh1 = it.lfh()
        print '==> REGISTER 0X53:' + str(lfh1)
        file23.write('==> REGISTER 0X53:' + str(lfh1) + '\n')
        file23.write('\n')
        file23.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> LFH1 Case: 2 Read the Register 100x"
        file23.write('==> LFH1 Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            lfh1 = it.lfh()
            print ('==> ITERATION: %d REGISTER 0X53:'%i + str(lfh1) + '\n')
            file23.write('==> ITERATION: %d REGISTER 0X53:'%i + str(lfh1) + '\n')
        file23.write('\n')
        file23.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> LFH1 Case: 3 Write to Register"
        try:
            result = it.lfh(-1)
        except:
            pass
        
        file23.write('==> REGISTER 0X53: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"






def  LGrid_Test(file24, path):

    
    try:
        
        print "==> LGrid Case: 1 Read the Register"
        file24.write('==> LGrid Case: 1 Read the Register"\n')
        lgrid = it.lgrid()
        print '==> REGISTER 0X56:' + str(lgrid )
        file24.write('==> REGISTER 0X56:' + str(lgrid ) + '\n')
        file24.write('\n')
        file24.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> LGrid Case: 2 Read the Register 100x"
        file24.write('==> LGrid Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            lgrid = it.lgrid()
            print ('==> ITERATION: %d REGISTER 0X56:'%i + str(lgrid ) + '\n')
            file24.write('==> ITERATION: %d REGISTER 0X56:'%i + str(lgrid) + '\n')
        file24.write('\n')
        file24.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> LGrid  Case: 3 Write to Register"
        try:
            result = it.lgrid(-1)
        except:
            pass
        
        file24.write('==> REGISTER 0X56: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"






def Currents_Test(file25, path):

    
    try:
        print "==> Currents Case: 1 Read the Register"
        file25.write('==> Currents Case: 1 Read the Register"\n')
        currents = it.currents()
        print '==> REGISTER 0X57:' + str(currents)
        file25.write('==> REGISTER 0X57:' + str(currents) + '\n')
        file25.write('\n')
        file25.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> Currents Case: 2 Read the Register 100x"
        file25.write('==> Currents  Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            currents = it.currents()
            print ('==> ITERATION: %d REGISTER 0X57:'%i + str(currents) + '\n')
            file25.write('==> ITERATION: %d REGISTER 0X57:'%i + str(currents) + '\n')
        file25.write('\n')
        file25.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> Currents Case: 3 Write to Register"
        try:
            result = it.currents(-1)
        except:
            pass
        
        file25.write('==> REGISTER 0X57: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"



def Temps_Test(file26, path):

    
    try:
        print "==> Temps Case: 1 Read the Register"
        file26.write('==> Temps  Case: 1 Read the Register"\n')
        temps = it.temps()
        print '==> REGISTER 0X58:' + str(temps)
        file26.write('==> REGISTER 0X58:' + str(temps) + '\n')
        file26.write('\n')
        file26.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> Temps Case: 2 Read the Register 100x"
        file26.write('==> Temps Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            temps = it.temps()
            print ('==> ITERATION: %d REGISTER 0X58:'%i + str(temps) + '\n')
            file26.write('==> ITERATION: %d REGISTER 0X58:'%i + str(temps) + '\n')
        file26.write('\n')
        file26.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> Temps Case: 3 Write to Register"
        try:
            result = it.temps(-1)
        except:
            pass
        
        file26.write('==> REGISTER 0X58: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"


def Age_Test(file27, path):

    
    try:
        print "==> Age Case: 1 Read the Register"
        file27.write('==> Age Case: 1 Read the Register"\n')
        age = it.age()
        print '==> REGISTER 0X61:' + str(age)
        file27.write('==> REGISTER 0X61:' + str(age) + '\n')
        file27.write('\n')
        file27.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
    print '\n'

    try:
        
        print "==> Age Case: 2 Read the Register 100x"
        file27.write('==> Age Case: 2 Read the Register 100x \n')
        for i in range(100): #print 100x
            age = it.age()
            print ('==> ITERATION: %d REGISTER 0X57:'%i + str(age) + '\n')
            file27.write('==> ITERATION: %d REGISTER 0X57:'%i + str(age) + '\n')
        file27.write('\n')
        file27.write('\n')
        
    except Exception as e:
         print e.message
         raise "Stop"
        
   
    try:
        
        print '\n'
        print "==> Age Case: 3 Write to Register"
        try:
            result = it.age(-1)
        except:
            pass
        
        file27.write('==> REGISTER 0X61: Cannot Write to Register \n')
        print '\n'
        
    except Exception as e:
         print e.message
         raise "Stop"


    
    
def runTest():
    ps = turnOnpowersupplies()
    time.sleep(2)
    ###MAIN###
    #it.laser(laser)
    it.connect(port,baud)
    it.logging(True)         #enable logging
    it.debugRS232(0)
    time.sleep(1)

    
    #NOP_Test()
    it.resena(1) # turn on the laser
    pendingClear() #wait for pending to clear
    

    try:    
        print 'Register 0x01 DevTyp'
        path = createNewDirectory(name= 'DeviceTypeTest')
        file1 = open(path + '\\' +  "DeviceType.txt","w")
        DevTyp_Test(file1, path)
        
    except Exception as e:
         print e.message
         raise "Stop"

        

    try:
        print 'Register 0x02 MFGR'
        path = createNewDirectory(name= 'MFGRTest')
        file2 = open(path + '\\' +  "MFGR.txt","w")
        MFGR_Test(file2,path)
        
    except Exception as e:
         print e.message
         raise "Stop"



    try:
        print 'Register 0x03 Model'
        path = createNewDirectory(name= 'ModelTest')
        file3 = open(path + '\\' +  "Model.txt","w")
        Model_Test(file3,path)
        
    except Exception as e:
         print e.message
         raise "Stop"



    try:
        print 'Register 0x04 SerNo'
        path = createNewDirectory(name= 'SerNoTest')
        file4 = open(path + '\\' +  "SerNo.txt","w")
        SerNo_Test(file4,path)
        
    except Exception as e:
         print e.message
         raise "Stop"



    #print 'Register 0x05 MFGDate'
    #MFGDate_Test(file)

    try:
        print 'Register 0x05 MFGDate'
        path = createNewDirectory(name= 'MFGDateTest')
        file5 = open(path + '\\' +  "MFGDate.txt","w")
        MFGDate_Test(file5,path)
        
    except Exception as e:
         print e.message
         raise "Stop"



##    print 'Register 0x06 Release'
##    Release_Test(file)

    try:
        print 'Register 0x06 Release'
        path = createNewDirectory(name= 'ReleaseTest')
        file6 = open(path + '\\' +  "Release.txt","w")
        Release_Test(file6,path)
        
    except Exception as e:
         print e.message
         raise "Stop"


##    print 'Register 0x07 RelBack'
##    RelBack_Test(file)

    try:
        print 'Register 0x07 RelBack'
        path = createNewDirectory(name= 'RelBackTest')
        file7 = open(path + '\\' +  "RelBack.txt","w")
        Relback_Test(file7,path)
        
    except Exception as e:
         print e.message
         raise "Stop"


##    print 'Register 0x09 AEA_EAC'
##    AEA_EAC_Test(file)

    try:
        print 'Register 0x09 AEA_EAC'
        path = createNewDirectory(name= 'AEA_EACTest')
        file9 = open(path + '\\' +  "AEA_EAC.txt","w")
        AEA_EAC_Test(file9,path)
        
    except Exception as e:
         print e.message
         raise "Stop"
        
##    print 'Register 0x0A AEA_EA'
##    AEA_EA_Test(file)

    try:
        print 'Register 0x0A AEA_EA'
        path = createNewDirectory(name= 'AEA_EATest')
        file10 = open(path + '\\' +  "AEA_EA.txt","w")
        AEA_EA_Test(file10,path)
        
    except Exception as e:
         print e.message
         raise "Stop"


##    print 'Register 0x13 LstResp'
##    LstResp_Test(file)

    try:
        print 'Register 0x13 LstResp'
        path = createNewDirectory(name= 'LstRespTest')
        file13 = open(path + '\\' +  "LstResp.txt","w")
        LstResp_Test(file13,path)
        
    except Exception as e:
         print e.message
         raise "Stop"


##    print 'Register 0x15 DLSatus'
##    DLSatus_Test(file)

    try:
        print 'Register 0x15 DLSatus'
        path = createNewDirectory(name= 'DLSatusTest')
        file15 = open(path + '\\' +  "DLSatus.txt","w")
        DLSatus_Test(file15,path)
        
    except Exception as e:
         print e.message
         raise "Stop"


##    print 'Register 0x40 LF1'
##    LF1_Test(file)

    try:
        print 'Register 0x40 LF1'
        path = createNewDirectory(name= 'LF1Test')
        file16 = open(path + '\\' +  "LF1.txt","w")
        LF1_Test(file16,path)
        
    except Exception as e:
         print e.message
         raise "Stop"


##    print 'Register 0x42 OOP'
##    OOP_test(file)

    try:
        print 'Register 0x42 OOP'
        path = createNewDirectory(name= 'OOPTest')
        file17 = open(path + '\\' +  "OOP.txt","w")
        OOP_Test(file17,path)
        
    except Exception as e:
         print e.message
         raise "Stop"


##    print 'Register 0x43 Ctemp'
##    CTemp_Test(file)

    try:
        print 'Register 0x43 Ctemp'
        path = createNewDirectory(name= 'CtempTest')
        file18 = open(path + '\\' +  "Ctemp.txt","w")
        Ctemp_Test(file18,path)
        
    except Exception as e:
         print e.message
         raise "Stop"


##    print 'Register 0x4F FTFR'
##    FTFR_Test(file)

    try:
        print 'Register 0x4F FTFR'
        path = createNewDirectory(name= 'FTFRTest')
        file19 = open(path + '\\' +  "FTFR.txt","w")
        FTFR_Test(file19,path)
        
    except Exception as e:
         print e.message
         raise "Stop"


##    print 'Register 0x50 OPSL'
##    OPSL_Test(file)

    try:
        print 'Register 0x50 OPSL'
        path = createNewDirectory(name= 'OPSLTest')
        file20 = open(path + '\\' +  "OPSL.txt","w")
        OPSL_Test(file20,path)
        
    except Exception as e:
         print e.message
         raise "Stop"


##    print 'Register 0x51 OPSH'
##    OPSH_Test(file)

    try:
        print 'Register 0x51 OPSH'
        path = createNewDirectory(name= 'OPSHTest')
        file21 = open(path + '\\' +  "OPSH.txt","w")
        OPSH_Test(file21,path)
        
    except Exception as e:
         print e.message
         raise "Stop"


##    print 'Register 0x52 LFL1'
##    LFL1_Test(file)

    try:
        print 'Register 0x52 LFL1'
        path = createNewDirectory(name= 'LFL1Test')
        file22 = open(path + '\\' +  "LFL1.txt","w")
        LFL1_Test(file22,path)
        
    except Exception as e:
         print e.message
         raise "Stop"


##    print 'Register 0x53 LFH1'
##    LFH1_Test(file)

    try:
        print 'Register 0x53 LFH1'
        path = createNewDirectory(name= 'LFH1Test')
        file23 = open(path + '\\' +  "LFH1.txt","w")
        LFH1_Test(file23,path)
        
    except Exception as e:
         print e.message
         raise "Stop"
        
##    print 'Register 0x56 LGrid'
##    LGrid_Test(file)

    try:
        print 'Register 0x56 LGrid'
        path = createNewDirectory(name= 'LGridTest')
        file24 = open(path + '\\' +  "LGrid.txt","w")
        LGrid_Test(file24,path)
        
    except Exception as e:
         print e.message
         raise "Stop"


##    print 'Register 0x57 Currents'
##    Currents_Test(file)

    try:
        print 'Register 0x57 Currents'
        path = createNewDirectory(name= 'CurrentsTest')
        file25 = open(path + '\\' +  "Currents.txt","w")
        Currents_Test(file25,path)
        
    except Exception as e:
         print e.message
         raise "Stop"
##    print 'Register 0x58 Temps'
##    Temps_Test(file)

    try:
        print 'Register 0x58 Temps'
        path = createNewDirectory(name= 'TempsTest')
        file26 = open(path + '\\' +  "Temps.txt","w")
        Temps_Test(file26,path)
        
    except Exception as e:
         print e.message
         raise "Stop"
        
##    print 'Register 0x61 Age'
##    Age_Test(file)

    try:
        print 'Register 0x61 Age'
        path = createNewDirectory(name= 'AgeTest')
        file27 = open(path + '\\' +  "Age.txt","w")
        Age_Test(file27,path)
        
    except Exception as e:
         print e.message
         raise "Stop"
##    file.close()
        
    it.disconnect()
    print "TEST COMPLETE"
    turnOffpowersupplies(ps)

if __name__== '__main__':
    runTest()
    








    