import math
import struct
import sys
import os
import time
import random
import instrumentDrivers as inst
import ConfigParser as parser
import RegressionUtility
import aa_gpio.gpio
sys.path.append(os.path.abspath('.'))
g = aa_gpio.gpio.gpio()
g.InitPin()

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'


utility = open('RegressionUtility.py','r')
exec(utility)

ConfigIni = parser.ConfigParser()
ConfigIni.read(r'\\photon\Company\DWDM Engineering\Micro_ITLA\Firmware\Regression_Testing\Regression Test Scripts\RegressionIni\Regression.ini')

#SN = raw_input("Please Enter Serial Number")
SN = 'CRTMF5F01T'
strSN = str(SN)

ChannelLstSize = 20
channellst1 = []
laser1freq = []
laser1target = [] 
FreqError1 = []
ftfRange = [100,200,300,400,500,600,700,800,900,1000,-100,-200,-300,-400,-500,-600,-700,-800,-900,-1000,1000,2000,3000,4000,5000,6000,-1000,-2000,-3000,-4000,-5000,-6000]
timeOut = 60
firstChan = 40
adtLst = [1,0]


#functions to turn on supplies
def PS1_ON ():
    return PS1.setOutputState('ON')

def PS2_ON ():
    return PS2.setOutputState('ON')


#functions to turn off supplies
def PS1_OFF():
    return PS1.setOutputState('OFF')

def PS2_OFF():
    return PS2.setOutputState('OFF')

def connectInstr():
    record_meters  = ConfigIni.get('Freq_Seq','Record_Meters')
    Supplies_ON = ConfigIni.get('Station','Supplies')
    com_port  = int(ConfigIni.get('Station','COM_PORT'))

    

    if record_meters:
        WM_cmd1 = ConfigIni.get('Station','WaveMeter1')
        print 'wavemeter1:',WM_cmd1
        exec ('wavemeter1 = inst.%s'%(WM_cmd1))
        wavemeter1.connect()
  
        PM_cmd1 = ConfigIni.get('Station','PwrMeter1')
        print 'pwrmeter1:',PM_cmd1
        exec ('pwrmeter1 = inst.%s'%(PM_cmd1))
        pwrmeter1.connect()
        print 'meter1 initialized'

    return wavemeter1,pwrmeter1,com_port

def bin(n):
    if n==0:return '0'
    else:
        return bin(n/2) + str(n%2)   

def GenerateChannelLists():
    
    #channellst1 = [1,95,51,3,93,53,5,91,55,7,89,57,9,87,45,11,85,47,13,83,49,15,81]
    channellst1 = [1,95,51,3,93,53,5,91,55,7,89]

    

    return channellst1

    print 'Laser 1 list: '
    print channellst1

def CreateDataFile():
    timestamp = time.asctime()
    timestampstr = timestamp.replace(' ','')
    timestampstr = timestampstr.replace(':','')
    file_name1 =strSN + '_' + 'FTF_Test1'+timestampstr+'.txt'
    datafile1 = open(file_name1,'w')
    return datafile1


def pullData1(startTime,status = ''):
    if 1:
        dummy0 = it.serNo()
        c0 = str(dummy0[1][1:])
        c0 = c0.strip("('")
        serial = c0.strip("',)")
        timeStamp = time.asctime()
        duration = str((time.time()-startTime))
        (dummy1,c3) = it.lf()
        lf = str(c3)
        (dummy4,c4) = it.channel()
        channel = str(c4)
        statWbin = bin(int(it.statusW()[1].data()))
        statFbin = bin(int(it.statusF()[1].data()))
        statWhex = hex(int(it.statusW()[1].data()))
        statFhex = hex(int(it.statusF()[1].data()))
        (dummy7,(dummy8, [c29, c30]))=it.temps()
        sledT = str(int(c29))
        pcbT = str(int(c30))
        (dummy9,(dummy10,[c31,c32]))= it.currents()
        tec = str(int(c31))
        diode = str(int(c32))
        dummy12 = it.release()
        c33 = str(dummy12[1][1:])
        c33 = c33.strip("('")
        release = c33.strip("',)")
        (dummy13, c34) = it.pwr()
        pwr = str(int(c34))
        (dummy14, c35) = it.oop()
        oop = str(c35)
        exec ('powerM1 = str(pwrmeter1.%s)'%(ConfigIni.get('Station','Pwr_Cmd')))
        exec ('waveM1 = str(wavemeter1.%s)'%(ConfigIni.get('Station','Wave_Cmd')))
        age = str(it.age()[1])
        floatwaveM1 = float(waveM1)

        if floatwaveM1>= 2990.00001:
            waveM1 = str(0)
            error1 = str(0)
        else:
            error1 = str(float(lf)-floatwaveM1)
        dummy15 = it.nop()
        pending = str(int(dummy15[1].fieldPending().value()))
        
        return serial + "\t" + release+ "\t" + timeStamp + "\t" + duration + "\t" + lf + "\t" + channel + "\t" + waveM1 + "\t" + error1 + "\t" + \
               oop+ "\t" + powerM1 + "\t" + statWbin + "\t" + statFbin + "\t" + statWhex + "\t" + statFhex\
               + "\t" + sledT + "\t" + pcbT + "\t" + tec + "\t" + diode + "\t" + pending + "\t" + age+ "\t" + status


def setInitFreq(firstChan):
    done1 = 0
    it.channel(firstChan)
    LF = it.lf()
    pwrmeter1.setFrequency(LF[1])
    opsh = int(it.opsh()[1])
    it.pwr(opsh)
    it.resena(1)

    starttime = time.time()
    duration = time.time() - starttime
    while duration <timeOut:
        pendingFlag = str(int(it.nop()[1].fieldPending().value()))
        if pendingFlag == '0':
            #clear alarms
            it.statusF(1,1,1,1,1,1,1,1)
            it.statusW(1,1,1,1,1,1,1,1)
            done1 = 1
            print "Pending bit Cleared"
            break
        
        duration = time.time() - starttime
        if duration >= timeOut:
            print"tuning time too long"
            raise "Stop Test"
        
        

        if done1==1:
            print "Laser Channel Lock"
            break
                    
  
                

def pendingClear(timeOut):
    starttime = time.time()
    duration = time.time() - starttime
    while duration <timeOut:
        pendingFlag = str(int(it.nop()[1].fieldPending().value()))
        #print it.nop()[1].fieldPending().toBinaryString()
        if pendingFlag == '0':
            print 'Binary Data:',it.nop()[1].fieldPending().toBinaryString()
            print "Pending bit Cleared"
            break
        if duration >= timeOut:
            print"tuning time too long"
            raise "Stop Test"
        
        duration = time.time() - starttime

def recordParams(status =''):
    print 'Taking wavelength measurement, Laser 1'
    #record data
    alarmStr1 = pullData1(startTime,status)
    datafile1.write('Laser1''\t'+ alarmStr1 + '\n')


def createHeader():
    datafile1.write('Laser# \tSN\tRELEASE\tTIMESTAMP\tDURATION\tLF\tCHANNEL\tMETER\tERROR\tOOP\tPOWER(dBm)\tSTATUSW(BIN)\tSTATUSF(BIN)\t \
    STATUSW(HEX)\tSTATUSF(HEX)\tSLEDTEMP\tPCBTEMP\tTEC\tDIODE\tPENDING\tAGE\tSTATUS\n')


     
    
     
if __name__ == '__main__':

         
    print "Initializing Instruments...."
    wavemeter1,pwrmeter1,com_port = connectInstr()
# Call function to generate random number
    it.disconnect()
    channellst1 = GenerateChannelLists()
    print channellst1
    it.connect(com_port)
    for set in adtLst:
        it.mcb(adt=set)
    #Call function to create file    
        datafile1 = CreateDataFile()
        createHeader()
         
        laser1done = 0
        startTime = time.time()
        it.resena(0)
        time.sleep(.5)
        chn = firstChan
        print "Perform Test"
        setInitFreq(chn)
        print "Start Testing"
        for freq1 in channellst1:
            print "Set to Channel:", freq1
            it.channel(freq1)
            pendingClear(timeOut)
            for ftf1 in ftfRange:
                print 'setting ftf to:',ftf1
                it.statusF(1,1,1,1,1,1,1,1)
                it.statusW(1,1,1,1,1,1,1,1)
                it.ftf(ftf1)
                pendingClear(timeOut)
                recordParams('afterpendingdrop') 
                time.sleep(10)
                recordParams('10secafter')                    
            print"Set ftf back to 0"
            it.ftf(0) #Setback to default target
            pendingClear(timeOut)
            time.sleep(10)
                

        it.ftf(0)
        opsh = int(it.opsh()[1])
        it.pwr(opsh)
        time.sleep(10)
        datafile1.close()
    TotalTestTime = time.time() - startTime
    print 'Total Test time: %0.2f' % TotalTestTime
    it.disconnect()
    print' All Devices Disconnected'
    

