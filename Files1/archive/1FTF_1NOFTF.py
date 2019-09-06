import time
import sys
import os
sys.path.append('C:\Documents and Settings\ttx.user\Desktop\DUAL_ REGRESSION_TEST_SUITE\Python')
import instrumentDrivers as inst
import ConfigParser as parser
import math
import random
import struct

ConfigIni = parser.ConfigParser()
ConfigIni.read(r'C:\Documents and Settings\ttx.user\Desktop\DUAL_ REGRESSION_TEST_SUITE\Python\Regression_1.ini')
#SN = raw_input("Please Enter Serial Number")
SN = 'USCQF6V003'
strSN = str(SN)

laserOne = 1
laserTwo = 2
ChannelLstSize = 2500
channellst1 = []
channellst2 = []
laser1freq = []
laser2freq = []
laser1target = [] 
laser2target = []
FreqError1 = []
FreqError2 = []
ftfRange = [100,200,300,400,500,600,700,800,900,1000,-100,-200,-300,-400,-500,-600,-700,-800,-900,-1000,1000,2000,3000,4000,5000,6000,-1000,-2000,-3000,-4000,-5000,-6000]
testNumber = [1,2]
firstChan = 40


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

##    if Supplies_ON:
##        PS_n52 = (ConfigIni.get('Station','SupplyN5_2'))
##        print 'Supply n52:', PS_n52
##        SupplyN5_2= inst.HP3631A(0,6)
##        SupplyN5_2.connect()
##        
##        PS_33 = (ConfigIni.get('Station','Supply3_3'))
##        print 'Supply 3.3:', PS_33
##        Supply3_3 = inst.HP3631A(0,7)
##        Supply3_3.connect()
##
##        Supply3_3.setOutputState('ON')
##        time.sleep(.2)
##        SupplyN5_2.SetOutputState('ON')
##        time.sleep(.2)        
        

    if record_meters:
        WM_cmd1 = ConfigIni.get('Station','WaveMeter1')
        print 'wavemeter1:',WM_cmd1
        exec ('wavemeter1 = inst.%s'%(WM_cmd1))
        wavemeter1.connect()

        WM_cmd2 = ConfigIni.get('Station','WaveMeter2')
        print 'wavemeter2:',WM_cmd2
        exec ('wavemeter2 = inst.%s'%(WM_cmd2))
        wavemeter2.connect()        
        
        PM_cmd1 = ConfigIni.get('Station','PwrMeter1')
        print 'pwrmeter1:',PM_cmd1
        exec ('pwrmeter1 = inst.%s'%(PM_cmd1))
##        PM_SLOT1 = ConfigIni.get('Station','PM_SLOT1')
##        PM_HEAD1 = ConfigIni.get('Station','PM_HEAD1')
##        pwrmeter1.SetActiveConf('pm1',int(PM_SLOT1),int(PM_HEAD1))
        pwrmeter1.connect()
        print 'meter1 initialized'

        PM_cmd2 = ConfigIni.get('Station','PwrMeter2')
        print 'pwrmeter2:',PM_cmd2
        exec ('pwrmeter2 = inst.%s'%(PM_cmd2))
##        PM_SLOT2 = ConfigIni.get('Station','PM_SLOT2')
##        PM_HEAD2 = ConfigIni.get('Station','PM_HEAD2')
##        pwrmeter2.SetActiveConf('pm2',int(PM_SLOT2),int(PM_HEAD2))
        pwrmeter2.connect()
        print 'meter2 initialized'
    return wavemeter1,wavemeter2,pwrmeter1,pwrmeter2,com_port

def bin(n):
    if n==0:return '0'
    else:
        return bin(n/2) + str(n%2)   

def GenerateChannelLists():
    
    channellst1 = [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49,51,53,55,57,59,61,63,65,67,69,71,73,75,77,79,81,83,85,87,89,91,93,95]
    channellst2 = [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49,51,53,55,57,59,61,63,65,67,69,71,73,75,77,79,81,83,85,87,89,91,93,95]
    return channellst1,channellst2

    print 'Laser 1 list: '
    print channellst1

    print 'Laser 2 list: '
    print channellst2

def CreateDataFile():
    timestamp = time.asctime()
    timestampstr = timestamp.replace(' ','')
    timestampstr = timestampstr.replace(':','')
    file_name1 =strSN + '_' + 'Dual_FTF_Test1'+timestampstr+'.txt'
    file_name2 =strSN + '_' + 'Dual_FTF_Test2'+timestampstr+'.txt'
    datafile1 = open(file_name1,'w')
    datafile2 = open(file_name2,'w')
    return datafile1,datafile2


def pullData1(startTime):
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
        statFbin = bin(int(it.statusW()[1].data()))
        statWhex = hex(int(it.statusW()[1].data()))
        statFhex = hex(int(it.statusW()[1].data()))
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

        floatwaveM1 = float(waveM1)

        if floatwaveM1>= 2990.00001:
            waveM1 = str(0)
            error1 = str(0)
        else:
            error1 = str(float(lf)-floatwaveM1)
        dummy15 = it.nop()
        pending = str(int(dummy15[1].fieldPending().value()))
        it.statusW(1,1,1,1,1,1,1,1)
        it.statusF(1,1,1,1,1,1,1,1)
        
        return serial + "\t" + release+ "\t" + timeStamp + "\t" + duration + "\t" + lf + "\t" + channel + "\t" + waveM1 + "\t" + error1 + "\t" + \
               oop+ "\t" + powerM1 + "\t" + statWbin + "\t" + statFbin + "\t" + statWhex + "\t" + statFhex\
               + "\t" + sledT + "\t" + pcbT + "\t" + tec + "\t" + diode + "\t" + pending

def pullData2(startTime):
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
        statFbin = bin(int(it.statusW()[1].data()))
        statWhex = hex(int(it.statusW()[1].data()))
        statFhex = hex(int(it.statusW()[1].data()))
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
        exec ('powerM2 = str(pwrmeter2.%s)'%(ConfigIni.get('Station','Pwr_Cmd')))
        exec ('waveM2 = str(wavemeter2.%s)'%(ConfigIni.get('Station','Wave_Cmd')))
        floatwaveM2 = float(waveM2)

        if floatwaveM2>= 2990.00001:
            waveM2 = str(0)
            error2 = str(0)
        else:
            error2 = str(float(lf)-floatwaveM2)
        dummy15 = it.nop()
        pending = str(int(dummy15[1].fieldPending().value()))
        
        it.statusW(1,1,1,1,1,1,1,1)
        it.statusF(1,1,1,1,1,1,1,1)
        
        return serial+ "\t" + release+ "\t" + timeStamp + "\t" + duration +"\t" + lf + "\t" + channel + "\t" + waveM2 + "\t" + error2 + "\t" + \
               oop+ "\t" + powerM2 + "\t" + statWbin + "\t" + statFbin + "\t" + statWhex + "\t" + statFhex\
               + "\t" + sledT + "\t" + pcbT + "\t" + tec + "\t" + diode + "\t" + pending

def setInitFreq(firstChan):
    complete = 'False'
    done1 = 0
    done2 = 0
    #set laser 1
    it.laser(1)
    it.channel(firstChan)
    LF = it.lf()
    pwrmeter1.setFrequency(LF[1])
    it.resena(1)


    #set laser 2
    it.laser(2)
    it.channel(firstChan)
    LF = it.lf()
    pwrmeter2.setFrequency(LF[1])
    it.resena(1)
    while 1:
        it.laser(1)
        pendingFlag1 = str(int(it.nop()[1].fieldPending().value()))
        if pendingFlag1 == '0':
            #clear alarms
            it.statusF(1,1,1,1,1,1,1,1)
            it.statusW(1,1,1,1,1,1,1,1)
            done1 = 1
            
        
        it.laser(2)
        pendingFlag2 = str(int(it.nop()[1].fieldPending().value()))
        if  pendingFlag2 == '0':
            done2 = 1
            #clear alarms
            it.statusF(1,1,1,1,1,1,1,1)
            it.statusW(1,1,1,1,1,1,1,1)
                
        if done1==1 & done2 == 1:
            print "Laser 1 Channel Lock"
            print "Laser 2 Channel Lock"
            print complete
            break
            
def pendingClear():
    while 1:     
        pendingFlag = str(int(it.nop()[1].fieldPending().value()))
        if pendingFlag == '0':
            print "Pending bit Cleared"
            break

def recordParams():
    print 'Taking wavelength measurement, Laser 1'
    #record data
    it.laser(laserOne)
    alarmStr1 = pullData1(startTime)
    datafile1.write('Laser1''\t'+ alarmStr1 + '\n')
    
    it.laser(laserTwo)
    print 'Taking wavelength measurement, Laser 2'
    #record data
    alarmStr2 = pullData2(startTime)
    datafile2.write('Laser2''\t'+ alarmStr2 + '\n')

def createHeader():
    datafile1.write('Laser# \tSN\tRELEASE\tTIMESTAMP\tDURATION\tLF\tCHANNEL\tMETER\tERROR\tOOP\tPOWER(dBm)\tSTATUSW(BIN)\tSTATUSF(BIN)\t \
    STATUSW(HEX)\tSTATUSF(HEX)\tSLEDTEMP\tPCBTEMP\tTEC\tDIODE\tPENDING\n')

    datafile2.write('Laser# \tSN\tRELEASE\tTIMESTAMP\tDURATION\tLF\tCHANNEL\tMETER\tERROR\tOOP\tPOWER(dBm)\tSTATUSW(BIN)\tSTATUSF(BIN)\t \
    STATUSW(HEX)\tSTATUSF(HEX)\tSLEDTEMP\tPCBTEMP\tTEC\tDIODE\tPENDING\n')
    
     
    
     
if __name__ == '__main__':

         
    print "Initializing Instruments...."
    wavemeter1,wavemeter2,pwrmeter1,pwrmeter2,com_port = connectInstr()

     
    
# Call function to generate random number
    channellst1,channellst2 = GenerateChannelLists()
    it.laser(2)
    it.connect(com_port)
    it.mcb(adt=0)
    it.laser(1)
    it.mcb(adt=0)


    i=0
    j=0




    print 'Laser1: %d, Laser2: %d' % (laserOne, laserTwo)
    if laserOne == 2:
        LaserWM1 = wavemeter1
        LaserWM2 = wavemeter2
    else:
        LaserWM1 = wavemeter2
        LaserWM2 = wavemeter1

#Call function to create file    
    datafile1,datafile2 = CreateDataFile()
    createHeader()
                
    laser1done = 0
    laser2done = 0
    startTime = time.time()
    it.laser(1)
    it.resena(0)
    time.sleep(.5)
    it.laser(2)
    it.resena(0)
    chn = firstChan
    for item in testNumber:
        print "Perform Test#%d"%item
        if item == 1:
            setInitFreq(chn)
            it.laser(2)
            print "Start Testing laser",it.laser()
            for freq1 in channellst2:
                print "Set to Channel:", freq1
                it.channel(freq1)
                pendingClear()
                for ftf1 in ftfRange:
                    print 'setting ftf to:',ftf1
                    it.ftf(ftf1)
                    pendingClear()
                    time.sleep(10)
                    recordParams()                    
                print"Set ftf back to 0"
                it.ftf(0) #Setback to default target
                pendingClear()
                time.sleep(10)
            
        else:
            setInitFreq(chn)
            it.laser(1)
            print "Start Testing laser",it.laser()
            for freq2 in channellst1:
                print "Set to Channel:", freq2
                it.channel(freq2)
                #pendingClear()
                for ftf2 in ftfRange:
                    print "ftf of laser",it.laser()
                    print 'setting ftf to:',ftf2
                    it.ftf(ftf2)
                    pendingClear()
                    time.sleep(10)
                    recordParams()
                    it.laser(1)
                it.ftf(0) #Setback to default target
                pendingClear()
                time.sleep(10)
            
    datafile1.close()
    datafile2.close()


    TotalTestTime = time.time() - startTime
    print 'Total Test time: %0.2f' % TotalTestTime

    wavemeter1.disconnect()
    wavemeter2.disconnect()
    pwrmeter1.disconnect()
    pwrmeter2.disconnect()
    it.disconnect()
    print' All Devices Disconnected'
    

