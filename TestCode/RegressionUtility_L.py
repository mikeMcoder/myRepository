
#creator: Michael D. Mercado
#Date: December 31, 2015
#RegressionUtility.py is a collection of useful functions that can be applied to regression testing
#in OIF.
 
import os
import sys
import math
import struct
import ConfigParser as parser
#import instrumentDrivers as inst
import time
import random

sys.path.append(os.path.abspath('.'))
ConfigIni = parser.ConfigParser()
ConfigIni.read(r'\\photon\Company\DWDM Engineering\Micro_ITLA\Firmware\Regression_Testing\Regression Test Scripts\RegressionIni\Regression.ini')

def gotoDefault():
    print'Cleanup Before Disconnecting...'
    pwr = it.opsh()[1]
    ftf = 0
    chn = 1
    it.pwr(pwr)
    it.ftf(0)
    it.channel(1)
    monChannellockS()
    
def singleSaveData(startTime,tuneTime=0.0,monTime=0.0,wavemeter1=0.0,powermeter1=0.0):
    ser = str(it.serNo()[1][1])
    duration = str(time.time()-startTime)
    testStamp = timeStamp()
    Channel = str(it.channel()[1])
    FrequencyLF = str(it.lf()[1])
    FrequencyMTR = str(wavemeter1.getFrequency())
    Power_Actual = str(powermeter1.getDisplayedPower())
    FreqError = str(float(FrequencyLF) - float(FrequencyMTR))
    Power_PWR = float(it.pwr()[1])
    Power_PWRStr = str(Power_PWR)
    Power_OOP = str(it.oop()[1])
    PowerError = Power_PWR/100 - float(Power_Actual)
    PowerErrorStr = str(PowerError)
    Ftf = str(it.ftf()[1])
    reg99 = it.readx99()
    StatusF_Hex = str(hex(int(it.statusF()[1].data())))
    reg99 = it.readx99()
    StatusF_Bin = str(bin(int(it.statusF()[1].data())))
    reg99 = it.readx99()
    StatusW_Hex = str(hex(int(it.statusW()[1].data())))
    reg99 = it.readx99()
    StatusW_Bin = str(bin(int(it.statusW()[1].data())))
    reg99 = it.readx99()
    noUse, currents = it.currents()
    Tec = str(int(currents[1][0]))
    reg99 = it.readx99()
    Diode = str(int(currents[1][1]))
    reg99 = it.readx99()
    noUse, Temps = it.temps()
    PcbTemp = str(int(Temps[1][0]))
    convertedPcbTemp = convertPcbTemp(PcbTemp)
    SledTemp = str(int(Temps[1][1]))
    Pending = str(it.nop()[1].fieldPending().value())
    TuneTime = str(tuneTime)
    MonTuneTime = str(monTime)
    channellockTime = str(tuneTime + monTime)
    tunerState = it.readx99().tunerstate
    f1 = it.readx99().f1temp
    f2 = it.readx99().f2temp
    siBlock = it.readx99().siblocktemp
    sled = it.readx99().sled_temperature
    gmi = it.readx99().gain_medium_current
    demodReal = it.readx99().demodrealerr
    photodiode = it.readx99().photodiode_current
    adt = str(it.mcb()[1].fieldAdt().value())
    grid = str(it.grid()[1])
    reg99 = it.readx99()
    age = str(it.age()[1])
    it.logentry(time.asctime())
    reg99 = it.readx99()
    lstData = []
    lstData.append([ser,testStamp,duration,Channel,FrequencyLF,\
                    FrequencyMTR,FreqError,Power_PWR,Power_OOP,\
                    Power_Actual,PowerErrorStr,Ftf,StatusF_Hex,\
                  StatusF_Bin,StatusW_Hex,StatusW_Bin,Tec,Diode,\
                    convertedPcbTemp,SledTemp,Pending,TuneTime,\
                    MonTuneTime,channellockTime,tunerState,\
                    f1,f2,siBlock,sled,gmi,demodReal,photodiode,\
                    adt,grid,age])
    strWrite = ''
    for item in lstData:
        # post conversion';
        strWrite += '%9s,' % ser
        strWrite += '%0.15s,' % testStamp
        strWrite += '%2.15s,' % duration
        strWrite += '%2s,' % Channel
        strWrite += '%s,' % FrequencyLF
        strWrite += '%s,' % FrequencyMTR
        strWrite += '%s,' % FreqError
        strWrite += '%s,' % Power_PWRStr
        strWrite += '%s,' % Power_OOP
        strWrite += '%s,' % Power_Actual
        strWrite += '%s,' % PowerErrorStr
        strWrite += '%s,' % Ftf
        strWrite += '%8s,' % StatusF_Hex
        strWrite += '%8s,' % StatusF_Bin
        strWrite += '%8s,' % StatusW_Hex
        strWrite += '%8s,' % StatusW_Bin
        strWrite += '%s,' % Tec
        strWrite += '%s,' % Diode
        strWrite += '%s,' % PcbTemp
        strWrite += '%s,' % SledTemp
        strWrite += '%s,' % Pending
        strWrite += '%s,' % TuneTime
        strWrite += '%s,' % MonTuneTime
        strWrite += '%s,' % channellockTime
        strWrite += '%s,' % tunerState
        strWrite += '%s,' % f1
        strWrite += '%s,' % f2
        strWrite += '%s,' % siBlock
        strWrite += '%s,' % sled
        strWrite += '%s,' % gmi
        strWrite += '%s,' % demodReal
        strWrite += '%s,' % photodiode
        strWrite += '%s,' % adt
        strWrite += '%s,' % grid
        strWrite += '%s,' % age
        return (strWrite + '\n')

def singleSaveDataS(startTime,tuneTime=0.0,monTime=0.0):
    ser = str(it.serNo()[1][1])
    duration = str(time.time()-startTime)
    testStamp = timeStamp()
    Channel = str(it.channel()[1])
    FrequencyLF = str(it.lf()[1])
    FrequencyMTR = str(wavemeter1.getFrequency())
    Power_Actual = str(powermeter1.getDisplayedPower())
    FreqError = str(float(FrequencyLF) - float(FrequencyMTR))
    Power_PWR = float(it.pwr()[1])
    Power_PWRStr = str(Power_PWR)
    Power_OOP = str(it.oop()[1])
    PowerError = Power_PWR/100 - float(Power_Actual)
    PowerErrorStr = str(PowerError)
    Ftf = str(it.ftf()[1])
    StatusF_Hex = str(hex(int(it.statusF()[1].data())))
    StatusF_Bin = str(bin(int(it.statusF()[1].data())))
    StatusW_Hex = str(hex(int(it.statusW()[1].data())))
    StatusW_Bin = str(bin(int(it.statusW()[1].data())))
    noUse, currents = it.currents()
    Tec = str(int(currents[1][0]))
    Diode = str(int(currents[1][1]))
    noUse, Temps = it.temps()
    PcbTemp = str(int(Temps[1][0]))
    convertedPcbTemp = convertPcbTemp(PcbTemp)
    SledTemp = str(int(Temps[1][1]))
    Pending = str(it.nop()[1].fieldPending().value())
    TuneTime = str(tuneTime)
    MonTuneTime = str(monTime)
    channellockTime = str(tuneTime + monTime)
    tunerState = '0'#it.readx99().tunerstate
    f1 = str(float(it.dbgTemps(0)[1].data())/100)
    f2 = str(float(it.dbgTemps(1)[1].data())/100)
    siBlock = str(float(it.dbgTemps(3)[1].data())/100)
    sled = str(float(it.dbgTemps(2)[1].data())/100)
    gmi = str(float(it.dbgTemps(16)[1].data())/100)
    demodReal = str(float(it.dbgTemps(7)[1].data()))
    photodiode = str(float(it.dbgTemps(4)[1].data())/100)
    adt = str(it.mcb()[1].fieldAdt().value())
    grid = str(it.grid()[1])
    age = str(it.age()[1])
    it.logentry(time.asctime())
    lstData = []
    lstData.append([ser,testStamp,duration,Channel,FrequencyLF,\
                    FrequencyMTR,FreqError,Power_PWR,Power_OOP,\
                    Power_Actual,PowerErrorStr,Ftf,StatusF_Hex,\
                  StatusF_Bin,StatusW_Hex,StatusW_Bin,Tec,Diode,\
                    convertedPcbTemp,SledTemp,Pending,TuneTime,\
                    MonTuneTime,channellockTime,tunerState,\
                    f1,f2,siBlock,sled,gmi,demodReal,photodiode,\
                    adt,grid,age])
    strWrite = ''
    for item in lstData:
        # post conversion';
        strWrite += '%9s,' % ser
        strWrite += '%0.15s,' % testStamp
        strWrite += '%2.15s,' % duration
        strWrite += '%2s,' % Channel
        strWrite += '%s,' % FrequencyLF
        strWrite += '%s,' % FrequencyMTR
        strWrite += '%s,' % FreqError
        strWrite += '%s,' % Power_PWRStr
        strWrite += '%s,' % Power_OOP
        strWrite += '%s,' % Power_Actual
        strWrite += '%s,' % PowerErrorStr
        strWrite += '%s,' % Ftf
        strWrite += '%8s,' % StatusF_Hex
        strWrite += '%8s,' % StatusF_Bin
        strWrite += '%8s,' % StatusW_Hex
        strWrite += '%8s,' % StatusW_Bin
        strWrite += '%s,' % Tec
        strWrite += '%s,' % Diode
        strWrite += '%s,' % PcbTemp
        strWrite += '%s,' % SledTemp
        strWrite += '%s,' % Pending
        strWrite += '%s,' % TuneTime
        strWrite += '%s,' % MonTuneTime
        strWrite += '%s,' % channellockTime
        strWrite += '%s,' % tunerState
        strWrite += '%s,' % f1
        strWrite += '%s,' % f2
        strWrite += '%s,' % siBlock
        strWrite += '%s,' % sled
        strWrite += '%s,' % gmi
        strWrite += '%s,' % demodReal
        strWrite += '%s,' % photodiode
        strWrite += '%s,' % adt
        strWrite += '%s,' % grid
        strWrite += '%s,' % age
        return (strWrite + '\n')
       


def showInitialParameters(wavemeter1):
    '''get initial registers and instrument names'''
    instruments = {}
    parameters = {}
    supply1,supply2,x,y=setpowerSupply()
    wavemeterName = wavemeter1.name
    
    instruments['POWERSUPPLY1']= supply1
    instruments['POWERSUPPLY2']= supply2
    instruments['WAVEMETER']= wavemeterName

    parameters['ADT'] = [0,1]
    parameters['MODELNUMBER'] = it.model()[1][1]
    parameters['SERIALNUMBER'] = it.serNo()[1][1]
    parameters['BUILD']= it.buildstring()
    parameters['GRIDSPACING'] = str(it.grid()[1])
    parameters['LF'] = str(it.lf()[1])
    parameters['LFH'] = str(it.lfh()[1])
    parameters['LFL'] = str(it.lfl()[1])
    parameters['POWER'] = str(it.pwr()[1])
    parameters['OPSH'] = str(it.opsh()[1])
    parameters['OPSL'] = str(it.opsl()[1])
    parameters['FTF'] = str(it.ftf()[1])
    parameters['BAUDRATE'] = str(it.baudrate()[1])
    parameters['POWERLEVELS'] = [it.opsh()[1],(it.opsh()[1] + it.opsl()[1])/2,it.opsl()[1]]
       
    for x,y in parameters.iteritems():
        print x,':',y

    for a,b in instruments.iteritems():
        print a,':',b
    return instruments,parameters


def singlecreateFile(path, name = 'Test',parameters = None, instrumentName = None):

    if parameters == None:
        parameters = 'xxx'

    if instrumentName == None:
        instrumentName = 'xxxx'
        
    #Createfile    
    daytime = time.asctime()
    daytimestr = daytime.replace(' ','')
    daytimestr = daytimestr.replace(':','')
    test_name = name + '_' + daytimestr
    test_file = open(path + '\\' + '%s.txt'%(test_name),'w')
    
    headerLst = ['SerialNo',
                 'TimeStamp',
                 'Duration',
                 'Channel',
                 'Frequency(LF)',
                 'Frequency(Meter)',
                 'FreqError',
                 'Power(PWR)',
                 'Power(OOP)',
                 'Power(dBm)',
                 'PowerError',
                 'FTF',
                 'StatusF(Hex)',
                 'StatusF(Bin)',
                 'StatusW(Hex)',
                 'StatusW(Bin)',
                 'TecCurrent',
                 'DiodeCurrent',
                 'SledTemp',
                 'PCBTemp',
                 'Pending',
                 'PendingTuneTime',                     
                 'ChannellockTuneTime',
                 'TotalTuneTime',
                 'TunerState',
                 'F1_99',
                 'F2_99',
                 'SiBlock_99',
                 'Sled_99',
                 'Gmi',
                 'DemodReal_99',
                 'Photodiode_99',
                 'ADT',
                 'Grid',
                 'Age',
                  ]
               
    strHeader = ''
    for item in headerLst:
                 strHeader += (item + ',')
    #print strHeader
    test_file.write(strHeader + '\n')

    

    return test_name,test_file

##



def createNewDirectory(name= 'TEST'):
    time = timeStamp()
    currentDirectory= os.getcwd()
    name = name + '_' + time
    newPath = currentDirectory + '\\' + name
    if not os.path.exists(newPath):
        os.mkdir(newPath)
    return newPath
    
def clearAlarms():
    '''Clears the warning and fatal alarm status'''
    it.logentry(time.asctime())
    reg99 = it.readx99()
    return it.statusF(1,1,1,1,1,1,1,1),it.statusW(1,1,1,1,1,1,1,1)

def clearAlarmsS():
    '''Clears the warning and fatal alarm status'''
    it.logentry(time.asctime())
    #reg99 = it.readx99()
    return it.statusF(1,1,1,1,1,1,1,1),it.statusW(1,1,1,1,1,1,1,1)

def checkAlarms():
    '''Checks the warning and fatal alarm status'''
    print '#' * 20, 'WARNING ALARMS', '#' * 20
    print it.statusW()
    print '#' * 20, 'FATAL ALARMS', '#' * 20
    print it.statusF()
    it.logentry(time.asctime())
    reg99 = it.readx99()

    
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

def pendingClearS():
    '''Function to monitor pending operation'''
    print 'Waiting for pending bit to clear...'
    #it.setpassword()
    timeOut = 2000
    starttime = time.time()
    duration = time.time() - starttime
    while duration < timeOut:
        pendingBit = str(int(it.nop()[1].fieldPending().value()))
        it.logentry(time.asctime())
        #reg99 = it.readx99()
        it.logentry(time.asctime())
        if pendingBit == '0':
            #reg99 = it.readx99()
            print "Pending bit Cleared..."
            tuneTime = duration
            break
        duration = time.time() - starttime
        if duration >=timeOut:
            it.logentry(time.asctime())
            #reg99 = it.readx99()
            print it.temps()
            print it.currents()
            print it.statusF()
            print it.statusW()
            #print it.readx99()
            raise "Tunetime more than 60 seconds: Stop Test"
    print 'TUNETIME:',tuneTime
    return tuneTime

def pendingClearRecordParameters():
    '''Function to monitor pending operation'''
    print 'Waiting for pending bit to clear...'
    it.setpassword()
    timeOut = 200
    starttime = time.time()
    duration = time.time() - starttime
    while duration < timeOut:
        pendingBit = str(int(it.nop()[1].fieldPending().value()))
        f1highwatermark, f2highwatermark, hopcount = readRegister85()
        recordParams(starttime,f1highwatermark, f2highwatermark, hopcount,'ADJUSTING')
        it.logentry(time.asctime())
        reg99 = it.readx99()

        if pendingBit == '0':
            
            recordParams(starttime,f1highwatermark, f2highwatermark, hopcount,'PENDING_DROP')
            reg99 = it.readx99()
            print "Pending bit Cleared..."
            tuneTime = duration
            break
        duration = time.time() - starttime
        if duration >=timeOut:
            it.logentry(time.asctime())
            reg99 = it.readx99()
            recordParams(starttime,f1highwatermark, f2highwatermark, hopcount,'PENDING_DROP')
            print it.temps()
            print it.currents()
            print it.statusF()
            print it.statusW()
            print it.readx99()
            raise "Tunetime more than 120 seconds: Stop Test"
    print 'TUNETIME:',tuneTime
    return tuneTime,starttime

def monChannellock():
    
    ''' Function to monitor channel lock condition'''
    print 'Waiting for Channel Lock...'
    it.setpassword()
    timeOut = 900
    starttime = time.time()
    duration = time.time() - starttime
    while duration < timeOut:
        stateMachine = it.readx99().tunerstate
        it.logentry(time.asctime())
        reg99 = it.readx99()
        it.lf()
        it.statusF()
        it.statusW()
        if stateMachine == 'TUNER_CHANNEL_LOCK':
            it.logentry(time.asctime())
            reg99 = it.readx99()
            print "Channel Locked..."
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
            print it.nopStats()
            print "Cannot Lock to a Channel: Stop the Test"
            raise 'STOP TEST'
    return tuneTime


def monChannellockS():
    
    ''' Function to monitor channel lock condition'''
    print 'Waiting for Channel Lock...'
    #it.setpassword()
    timeOut = 15
    starttime = time.time()
    duration = time.time() - starttime
    while duration < timeOut:
        #stateMachine = it.readx99().tunerstate
        it.logentry(time.asctime())
        #reg99 = it.readx99()
##        if stateMachine == 'TUNER_CHANNEL_LOCK':
##            it.logentry(time.asctime())
##            reg99 = it.readx99()
##            print "Channel Locked..."
##            tuneTime = duration
##            break
        duration = time.time() - starttime
        if duration >=timeOut:
            it.logentry(time.asctime())
            #reg99 = it.readx99()
##            print it.temps()
##            print it.currents()
##            print it.statusF()
##            print it.statusW()
##            print it.nopStats()
            print "Channel Lock"
            tuneTime = duration
            pass
    return tuneTime



def timeStamp():
    daytime = time.asctime()
    daytimestr = daytime.replace(' ','')
    daytimestr = daytimestr.replace(':','')
    return daytimestr
    

    
  
def connectInstrument():
    
    ConfigIni = parser.ConfigParser()
    ConfigIni.read(r'\\photon\Company\DWDM Engineering\Micro_ITLA\Firmware\Regression_Testing\Regression Test Scripts\RegressionIni\Regression.ini')
    record_meters  = ConfigIni.get('Freq_Seq','Record_Meters')
    com_port  = int(ConfigIni.get('Station','COM_PORT'))
    pwrlevelstr  = ConfigIni.get('Freq_Seq','Pwr_Levels')
    pwrlevelst  = pwrlevelstr.split(',')
    print 'pwrlevels:',pwrlevelst

    adtstr  = ConfigIni.get('Freq_Seq','ADT_Lst')
    adtlst  = adtstr.split(',')
    print 'ADTs:',adtlst
    
    CHstr  = ConfigIni.get('Freq_Seq','CH_Seq')
    CHlst  = CHstr.split(',')
    samplingL = int(ConfigIni.get('Freq_Seq','SamplingL'))
    samplingP = int(ConfigIni.get('Freq_Seq','SamplingP'))
    

    
    if record_meters:
        if it.laser() == 0:           
            WM_cmd1 = ConfigIni.get('Station','WaveMeter1')
            print 'wavemeter1:',WM_cmd1
            exec ('wavemeter1 = inst.%s'%(WM_cmd1))
            wavemeter1.connect()
            print 'WAVEMETER1 ON'

            PM_cmd1 = ConfigIni.get('Station','PwrMeter1')
            print 'pwrmeter1:',PM_cmd1
            exec ('pwrmeter1 = inst.%s'%(PM_cmd1))
            pwrmeter1.connect()
            print 'POWERMETER1 ON'
            return wavemeter1,pwrmeter1,com_port
        
        if it.laser() == 1:           
            WM_cmd1 = ConfigIni.get('Station','WaveMeter1')
            print 'wavemeter1:',WM_cmd1
            exec ('wavemeter1 = inst.%s'%(WM_cmd1))
            wavemeter1.connect()
            print 'WAVEMETER1 ON'

            PM_cmd1 = ConfigIni.get('Station','PwrMeter1')
            print 'pwrmeter1:',PM_cmd1
            exec ('pwrmeter1 = inst.%s'%(PM_cmd1))
            pwrmeter1.connect()
            print 'POWERMETER1 ON'
            return wavemeter1,pwrmeter1,com_port

        if it.laser()== 2:
            WM_cmd2 = ConfigIni.get('Station','WaveMeter2')
            print 'wavemeter2:',WM_cmd2
            exec ('wavemeter2 = inst.%s'%(WM_cmd2))
            wavemeter2.connect()
            print 'WAVEMETER2 ON'

            PM_cmd2 = ConfigIni.get('Station','PwrMeter2')
            print 'pwrmeter2:',PM_cmd2
            exec ('pwrmeter2 = inst.%s'%(PM_cmd2))
            pwrmeter2.connect()
            return wavemeter2,pwrmeter2,com_port
            
            


    

def setPowerMeter1Wavelength(freq):
    print 'Set the powermeter1 wavelength to:',freq
    powermeter1.setFrequency(freq)

def setPowerMeter2Wavelength(freq):
    print 'Set the powermeter2 wavelength to:',freq
    powermeter2.setFrequency(freq)

    
    
##def singlecreateFile():
##    
##    #Createfile    
##    # Assemble file header for laser1 and laser2
##    pwrlevelstr  = ConfigIni.get('Freq_Seq','Pwr_Levels')
##    pwrlevelst  = pwrlevelstr.split(',')
##    adtstr  = ConfigIni.get('Freq_Seq','ADT_Lst')
##    adtlst  = adtstr.split(',')
##    teststr1  = ConfigIni.get('Freq_Seq','Name')+"_UITLA"
##
##    daytime = time.asctime()
##    daytimestr = daytime.replace(' ','')
##    daytimestr = daytimestr.replace(':','')
##    test_name1 = 'TEST'+"_"+teststr1+"_"+daytimestr
##    test_file1 = open("%s.csv"%(test_name1),"w")
##
##    headerLst = ['Iteration',
##                 'Laser#',
##                 'SerialNo',
##                 'TimeStamp',
##                 'Duration',
##                 'Channel',
##                 'Frequency(LF)',
##                 'Frequency(Meter)',
##                 'FreqError',
##                 'Power(PWR)',
##                 'Power(OOP)',
##                 'Power(dBm)',
##                 'PowerError',
##                 'StatusF(Hex)',
##                 'StatusF(Bin)',
##                 'StatusW(Hex)',
##                 'StatusW(Bin)',
##                 'Tec Current',
##                 'Diode Current',
##                 'Sled Temp',
##                 'PCB Temp',
##                 'Pending',
##                 'TuneTime',                     
##                 'nopStats_pending',
##                 'nopStats_ch_lock',
##                 'nopStats_State_Mach',
##                 'AGE',
##                  ]
##               
##    strHeader = ''
##    for item in headerLst:
##                 strHeader += (item + ',')
##                 
##
##
##    test_file1.write(strHeader + '\n')
##
##    return test_name1,test_file1
        
def dualcreateFile():
    
    #Createfile    
    # Assemble file header for laser1 and laser2
    pwrlevelstr  = ConfigIni.get('Freq_Seq','Pwr_Levels')
    pwrlevelst  = pwrlevelstr.split(',')
    adtstr  = ConfigIni.get('Freq_Seq','ADT_Lst')
    adtlst  = adtstr.split(',')
    teststr1  = ConfigIni.get('Freq_Seq','Name')+"_lsr1"
    teststr2  = ConfigIni.get('Freq_Seq','Name')+"_lsr2"
    daytime = time.asctime()
    daytimestr = daytime.replace(' ','')
    daytimestr = daytimestr.replace(':','')
    test_name1 = ConfigIni.get('Station','Serial')+"_"+teststr1+"_"+daytimestr
    test_name2 = ConfigIni.get('Station','Serial')+"_"+teststr2+"_"+daytimestr
    test_file1 = open("%s.csv"%(test_name1),"w")
    test_file2 = open("%s.csv"%(test_name2),"w")

    headerLst = ['Iteration',
                 'Laser#',
                 'SerialNo',
                 'TimeStamp',
                 'Duration',
                 'Channel',
                 'Frequency(LF)',
                 'Frequency(Meter)',
                 'FreqError',
                 'Power(PWR)',
                 'Power(OOP)',
                 'Power(dBm)',
                 'PowerError',
                 'StatusF(Hex)',
                 'StatusF(Bin)',
                 'StatusW(Hex)',
                 'StatusW(Bin)',
                 'Tec Current',
                 'Diode Current',
                 'Sled Temp',
                 'PCB Temp',
                 'Pending',
                 'TuneTime',                     
                 'nopStats_pending',
                 'nopStats_ch_lock',
                 'nopStats_State_Mach',
                 'AGE',
                  ]
               
    strHeader = ''
    for item in headerLst:
                 strHeader += (item + ',')
                 


    test_file1.write(strHeader + '\n')
    test_file2.write(strHeader + '\n')
##    test_file1.close()
##    test_file2.close()
    return test_name1,test_name2,test_file1,test_file2

def convertPcbTemp(pcbT):
    if int(pcbT) >= 32768:
        intpcbTemp = int(-(65536-int(pcbT)))
        strpcbTemp = str(intpcbTemp)
    else:
        intpcbTemp = int(pcbT)
        strpcbTemp = str(intpcbTemp)
    return strpcbTemp



def saveData(i,lsrNo ,ser = None,tuneTime = None):
    stri = str(i)
    duration = str(time.clock())
    testStamp = str(time.ctime().replace(' ', '_').replace(':', '').replace('2015',''))
    Channel = str(it.channel()[1])
    reg99 = it.readx99()
    FrequencyLF = str(it.lf()[1])
    reg99 = it.readx99()
    if lsrNo == 1:
        FrequencyMTR = str(wavemeter1.getFrequency())
        Power_Actual = str(pwrmeter1.getDisplayedPower())
    else:
        FrequencyMTR = str(wavemeter2.getFrequency())
        Power_Actual = str(pwrmeter2.getDisplayedPower())
    FreqError = str(float(FrequencyLF) - float(FrequencyMTR))
    Power_PWR = float(it.pwr()[1])
    reg99 = it.readx99()
    Power_PWRStr = str(Power_PWR)
    reg99 = it.readx99()
    Power_OOP = str(it.oop()[1])
    reg99 = it.readx99()
    PowerError = Power_PWR/100 - float(Power_Actual)
    PowerErrorStr = str(PowerError)
    reg99 = it.readx99()
    StatusF_Hex = str(hex(int(it.statusF()[1].data())))
    reg99 = it.readx99()
    StatusF_Bin = str(bin(int(it.statusF()[1].data())))
    reg99 = it.readx99()
    StatusW_Hex = str(hex(int(it.statusW()[1].data())))
    reg99 = it.readx99()
    StatusW_Bin = str(bin(int(it.statusW()[1].data())))
    reg99 = it.readx99()
    noUse, currents = it.currents()
    Tec = str(int(currents[1][0]))
    reg99 = it.readx99()
    Diode = str(int(currents[1][1]))
    reg99 = it.readx99()
    noUse, Temps = it.temps()
    PcbTemp = str(int(Temps[1][0]))
    convertedPcbTemp = convertPcbTemp(PcbTemp)
    SledTemp = str(int(Temps[1][1]))
    reg99 = it.readx99()
    Pending = str(it.nop()[1].fieldPending().value())
    reg99 = it.readx99()
    TuneTime = str(tuneTime)                     
    nopStats_pending = str(it.nopStats()[1].fieldNopPendLock().toBinaryString())
    Channel_Lock = str(it.nopStats()[1].fieldNopPendCh().toBinaryString())
    reg99 = it.readx99()
    State_Machine =str(it.nopStats()[1].fieldStateMach().cipher())
    reg99 = it.readx99()
    age = str(it.age()[1])
    it.logentry(time.asctime())
    reg99 = it.readx99()

    lstData = []
    lstData.append([stri,lsrNo,ser,testStamp,duration,Channel,FrequencyLF,FrequencyMTR,FreqError,Power_PWR,Power_OOP,Power_Actual,StatusF_Hex,\
                  StatusF_Bin,StatusW_Hex,StatusW_Bin,Tec,Diode,convertedPcbTemp,SledTemp,Pending,TuneTime,nopStats_pending,Channel_Lock,State_Machine,\
                  age])
   
    for item in lstData:
        # post conversion
        strWrite = ''
        strWrite += '%s,' % stri
        strWrite += '%s,' % lsrNo
        strWrite += '%9s,' % ser
        strWrite += '%0.15s,' % testStamp
        strWrite += '%2.15s,' % duration
        strWrite += '%2s,' % Channel
        strWrite += '%s,' % FrequencyLF
        strWrite += '%s,' % FrequencyMTR
        strWrite += '%s,' % FreqError
        strWrite += '%s,' % Power_PWRStr
        strWrite += '%s,' % Power_OOP
        strWrite += '%s,' % Power_Actual
        strWrite += '%s,' % PowerErrorStr
        strWrite += '%s,' % StatusF_Hex
        strWrite += '%s,' % StatusF_Bin
        strWrite += '%s,' % StatusW_Hex
        strWrite += '%s,' % StatusW_Bin
        strWrite += '%s,' % Tec
        strWrite += '%s,' % Diode
        strWrite += '%s,' % PcbTemp
        strWrite += '%s,' % SledTemp
        strWrite += '%s,' % Pending
        strWrite += '%s,' % TuneTime
        strWrite += '%s,' % nopStats_pending
        strWrite += '%s,' % Channel_Lock
        strWrite += '%s,' % State_Machine
        strWrite += '%s,' % age
       
        return (strWrite + '\n')


        
def createFile(adt):
    teststr  = ConfigIni.get('Freq_Seq','Name')+"_ADT"+m_adt+ "_"+pwrlevel
    daytimestr = timeStamp()
    test_name = ConfigIni.get('Station','Serial')+"_"+teststr+"_"+daytimestr  
    test_file = open("%s.csv"%(test_name),"w")
    test_file.write("SN,RELEASE,TIMESTAMP,DURATION,LF,CHANNEL,FREQUENCY(METER),ERROR(THZ),OOP,POWER(dBm),POWERERROR,STATUSW(BIN),STATUSF(BIN),STATUSW(HEX),STATUSF(HEX),\
    SLEDT,PCBT,TEC,DIODE,PENDING,TuneTime,Status,AGE\n")
    test_file.close()
    return test_name,test_file

#def pwr_adt():
#    pwrlevelstr  = ConfigIni.get('Freq_Seq','Pwr_Levels')
#    pwrlevelst  = pwrlevelstr.split(',')
#    print 'pwrlevels:',pwrlevelst
#
#    adtstr  = ConfigIni.get('Freq_Seq','ADT_Lst')
#    adtlst  = adtstr.split(',')
#    print 'ADTs:',adtlst
#    return pwrlevelst, adtlst
    


def itpull(time0,pwr_meter,wave_meter):
    it.logentry(time.asctime())
    dummy0 = it.serNo()
    c0 = str(dummy0[1][1:])
    c0 = c0.strip("('")
    serial = c0.strip("',)")
    timeStamp = time.asctime()
    duration = str((time.time()-time0))
    (dummy1,c3) = it.lf()
    lf = str(c3)
    (dummy4,c4) = it.channel()
    it.readx99()
    channel = str(c4)
    statusW = it.statusW()
    statusF = it.statusF()
    statWbin = bin(int(statusW[1].data()))
    statFbin = bin(int(statusF[1].data()))
    it.readx99()
    statWhex = hex(int(statusW[1].data()))
    statFhex = hex(int(statusF[1].data()))
    it.readx99()
    (dummy7,(dummy8, [c29, c30]))=it.temps()
    sledT = str(int(c29))
    pcbT = str(int(c30))
    (dummy9,(dummy10,[c31,c32]))= it.currents()
    it.readx99()
    tec = str(int(c31))
    diode = str(int(c32))
    dummy12 = it.release()
    it.readx99()
    c33 = str(dummy12[1][1:])
    c33 = c33.strip("('")
    release = c33.strip("',)")
    (dummy13, c34) = it.pwr()
    it.readx99()
    pwr = str(int(c34))
    (dummy14, c35) = it.oop()
    it.readx99()
    oop = str(c35)
    exec ('powerM = str(pwr_meter.%s)'%(ConfigIni.get('Station','Pwr_Cmd')))
    exec ('waveM = str(wave_meter.%s)'%(ConfigIni.get('Station','Wave_Cmd')))
    age = str(it.age()[1])
    it.readx99()
    powError = float(c35)/100- float(powerM)
    strpowError = str(powError)
    floatwaveM = float(waveM)

    if floatwaveM>= 2990.00001:
        waveM = str(0)
        error = str(0)
    else:
        error = str(float(lf)-floatwaveM)
   
    dummy15 = it.nop()
    pending = str(int(dummy15[1].fieldPending().value()))
    it.logentry(time.asctime())
    it.readx99()

    
    return  serial+ "," + release+ "," + timeStamp + "," + duration + "," + lf + "," + channel + "," + waveM + "," + error + "," + \
            oop+ "," + powerM + "," + strpowError + "," + statWbin + "," + statFbin + "," + statWhex + "," + statFhex\
            + "," + sledT + "," + pcbT + "," + tec + "," + diode + "," + pending + "," + age

def dualconnectInstrument():
    record_meters  = ConfigIni.get('Freq_Seq','Record_Meters')
    Supplies_ON = ConfigIni.get('Station','Supplies')
    com_port  = int(ConfigIni.get('Station','COM_PORT'))
    #baud = int(ConfigIni.get('Station','BaudRate'))


    if record_meters:
        WM_cmd1 = ConfigIni.get('Station','WaveMeter1')
        print 'wavemeter1:',WM_cmd1
        exec ('wavemeter1 = inst.%s'%(WM_cmd1))
        wavemeter1.connect()

        WM_cmd2 = ConfigIni.get('Station','WaveMeter2')
        print 'wavemeter2:',WM_cmd2
        exec ('wavemeter2 = inst.%s'%(WM_cmd2))
        wavemeter2.connect()        
##        
        PM_cmd1 = ConfigIni.get('Station','PwrMeter1')
        print 'pwrmeter1:',PM_cmd1
        exec ('pwrmeter1 = inst.%s'%(PM_cmd1))
        pwrmeter1.connect()
        print 'meter1 initialized'

        PM_cmd2 = ConfigIni.get('Station','PwrMeter2')
        print 'pwrmeter2:',PM_cmd2
        exec ('pwrmeter2 = inst.%s'%(PM_cmd2))
        pwrmeter2.connect()
        print 'meter2 initialized'
    return wavemeter1,wavemeter2,pwrmeter1,pwrmeter2,com_port    

        
    
    
def setpowerSupply():
    defaultVoltage = 3.55
    defaultCurrent = 2.5
    
    ps1 = inst.psAG3631('GPIB0::06')
    ps1.connect()
    ps1.setOutputState('ON')
    ps1.setVoltCurr(selOutput = 'P6V', volts = defaultVoltage ,current = defaultCurrent)
    psName1 = ps1.name

    ps2 = inst.psAG3631('GPIB0::07')
    ps2.connect()
    ps2.setOutputState('ON')
    ps2.setVoltCurr(selOutput = 'P6V', volts = defaultVoltage ,current = defaultCurrent)
    psName2 = ps2.name
    return psName1,psName2,ps1,ps2

def demodConv(val):
    if val>=32768: #0x8000
        fval = -(65536-float(val))#0x10000
    else:
        fval = float(val)
    return fval/1000.0
##
##def pendingClear():
##    timeOut = 100
##    starttime = time.time()
##    duration = time.time() - starttime
##    while duration < timeOut:
##        pendingFlag = str(int(it.nop()[1].fieldPending().value()))
##        if pendingFlag == '0':
##            print "Pending bit Cleared"
##            tuneTime = float(duration)
##            break
##        
##        duration = time.time() - starttime
##        if duration >=timeOut:
####            outstring1 = saveData(lsr1,ser,Freq1,Pwr1,tuneTime1)
####            outstring2 = saveData(lsr2,ser,Freq2,Pwr2,tuneTime2)
##            print it.nop()
##            print it.nopStats()
##            print it.oop()
##            print it.lf()
##            print it.temps()
##            print it.currents()
##            print it.statusF()
##            print it.statusW()
##            return duration
##            break
##            
##    
##    return tuneTime

def readMready():
    startTime = time.time()
    duration = time.time() - startTime
    while 1:
        rdy = it.nop()[1].fieldMrdy().toBinaryString()
        #print rdy
        duration = time.time() - startTime
        if rdy == '1':
            print "MREADY in %0.6fs:"%duration
            break
    return duration


def bin(n):
    if n==0:return '0'
    else:
        return bin(n/2) + str(n%2)


def supplyOn(ps2):
    return ps2.setOutputState('ON')

def supplyOff(ps2):
    return ps2.setOutputState('OFF')

def readReg92():
    for i in range(5):
        command = Register.Register(Register.DBG_RESET)
        reg92 = it.register(command)
        reg92Out = reg92[1].fieldSource()
    print reg92Out
    return reg92Out

def setRST(ps1):
    ON = 3.3
    OFF = 0
    rise,fall = randDelay()
    amplitude = 'AMPLITUDE 0V'
    it.logentry('FALLING EDGE')
    ps1.setVoltCurr(selOutput = 'P25V', volts = OFF ,current = defaultCurrent)
    time.sleep(fall)
    supplyOff()
    time.sleep(.850)
    supplyOn()
    time.sleep(.2)
    it.logentry(amplitude)
    it.logentry('RISING EDGE')
    ps1.setVoltCurr(selOutput = 'P25V', volts = ON ,current = defaultCurrent)
    rise,fall = randDelay()
    time.sleep(fall)
    it.logentry('FALLING EDGE')
    ps1.setVoltCurr(selOutput = 'P25V', volts = OFF ,current = defaultCurrent)
    time.sleep(.05)
    ps1.setVoltCurr(selOutput = 'P25V', volts = ON ,current = defaultCurrent)
    it.logentry('RISING EDGE')
    



def setRST(ps1):
    ON = 3.3
    OFF = 0
    rise,fall = randDelay()
    amplitude = 'AMPLITUDE 0V'
    it.logentry('FALLING EDGE')
    ps1.setVoltCurr(selOutput = 'P25V', volts = OFF ,current = defaultCurrent)
    time.sleep(fall)
    supplyOff()
    time.sleep(.850)
    supplyOn()
    time.sleep(.2)
    it.logentry(amplitude)
    it.logentry('RISING EDGE')
    ps1.setVoltCurr(selOutput = 'P25V', volts = ON ,current = defaultCurrent)
    rise,fall = randDelay()
    time.sleep(fall)
    it.logentry('FALLING EDGE')
    ps1.setVoltCurr(selOutput = 'P25V', volts = OFF ,current = defaultCurrent)
    time.sleep(.05)
    ps1.setVoltCurr(selOutput = 'P25V', volts = ON ,current = defaultCurrent)
    it.logentry('RISING EDGE')
    
    
    
    
    
def randDelay():
    delayRise = random.randint(250,275)/1000.0
    delayFall = random.randint(0,299)/1000.0
    return delayRise,delayFall


def tx(cmd):
    it.write(cmd)
    rep = it.read(4)
    return rep

def readReg92():
    for i in range(5):
        command = Register.Register(Register.DBG_RESET)
        reg92 = it.register(command)
        reg92Out = reg92[1].fieldSource()
    print reg92Out
    return reg92Out

def readReg():
    reg92 = readReg92()
    state = str(it.nopStats()[1].fieldStateMach())
    print 'Time:',time.asctime(),'\t','NOP:',it.nop()[1].fieldPending().toBinaryString(),\
    '\t','CHANNEL:',it.channel()[1],'\t','NOPSTAT:',int(it.nopStats()[1].data()),'\t','STATEMACHINE:',state,'\t','CTEMP:',it.ctemp()[1],'\t','OOP:',it.oop()[1]#,'92:',reg92
    return state
    

##def pendingClear():
##    it.debugRS232(0)
##    it.setpassword()
##    timeOut = 60
##    starttime = time.time()
##    duration = time.time() - starttime
##    while duration < timeOut:
##        pendingFlag = str(int(it.nop()[1].fieldPending().value()))
##        it.readx99()
##        if pendingFlag == '0':
##            print "Pending bit Cleared"
##            tuneTime = duration
##            it.debugRS232(0)
##            break
##        
##        duration = time.time() - starttime
##        if duration >=timeOut:
##            
##            print it.temps()
##            print it.currents()
##            print it.statusF()
##            print it.statusW()
##            print it.channel()
##            print it.nop()
##            print it.readx99()
##            raise "Tunetime more than 60 seconds: Stop Test"
##        #print "TIME:",time.asctime(),"Pending Bit:",pendingFlag
##    return tuneTime

def setComslog(testName = None):
    stamp = time.asctime()
    stamp = stamp.replace(':','')
    if testName == None:
        it.logfile('TEST' + '_' + stamp + '.txt')
        it.logging(True)
        it.logentry(time.asctime())
        it.setpassword()
        print it.serNo()
        print it.buildstring()
        print it.release()
        print it.monitor()
    else:
        it.logfile(testName + '_' + stamp + '.txt')
        it.logging(True)
        it.logentry(time.asctime())
        it.setpassword()
        print it.serNo()
        print it.buildstring()
        print it.release()
        print it.monitor()


def setComslogS(testName = None):
    stamp = time.asctime()
    stamp = stamp.replace(':','')
    if testName == None:
        it.logfile('TEST' + '_' + stamp + '.txt')
        it.logging(True)
        it.logentry(time.asctime())
        #it.setpassword()
        print it.serNo()
        print it.buildstring()
        print it.release()
        print it.monitor()
    else:
        it.logfile(testName + '_' + stamp + '.txt')
        it.logging(True)
        it.logentry(time.asctime())
        #it.setpassword()
        print it.serNo()
        print it.buildstring()
        print it.release()
        print it.monitor()
        


def waitformrdy( timeout = 30 ):
    it.setpassword()
    print 'Waiting for mrdy clear...'
    starttime = time.time()
    while True:
        sys.stdout.write('.')
        time.sleep(.010)
        nopdat = it.nop()[1].data()
        it.readx99()
        if ( nopdat & 0xFF == 0x10):
            print'MREADY SET'
            break
        if (time.time() - starttime > timeout):
            print 'Timed out'
            break
        


def setalarmTriggers():
    it.srqT(1,1,1,1,1,1,1,1,1,1,1,1)
    print it.srqT()
    it.almT(1,1,1,1,1,1,1,1)
    print it.almT()
    it.fatalT(1,1,1,1,1,1,1,1)
    print it.fatalT()

    

     
def turnOnBothLasers(startChan=50):
    it.laser(1)
    it.channel(startChan)
    it.resena(sena = 1)
    print 'TURN ON LASER 1'
    pendingClear()
    monChannellock()
    
    it.laser(2)
    it.channel(startChan)
    it.resena(sena = 1)
    print 'TURN ON LASER 2'
    pendingClear()
    monChannellock()
    
def turnOnLaser1():
    it.laser(1)
    it.resena(sena = 1)
    print 'TURN ON LASER 1'
    tuneTime1 = pendingClear()
    return tuneTime1
    

def turnOnLaser2():
    it.laser(2)
    it.resena(sena = 1)
    print 'TURN ON LASER 2'
    tuneTime2 = pendingClear()
    return tuneTime2

def turnOnLaser():
    print 'TURN ON LASER'
    chn = setFrequency(193.8)
    it.channel(chn)
    it.resena(1)
    tuneTime = pendingClear()
    monChannellock()
    return tuneTime

def turnOnLaserS():
    print 'TURN ON LASER'
    chn = setFrequency(193.8)
    it.channel(chn)
    it.resena(1)
    tuneTime = pendingClearS()
    monChannellockS()
    return tuneTime
    

def cleanUp():
    pass

def dualClearAlarms(lsr):
    it.laser(lsr)
    it.statusF(1,1,1,1,1,1,1,1)
    it.statusW(1,1,1,1,1,1,1,1)
    it.logentry(time.asctime())
    reg99 = it.readx99()
    
    'LASER:%d ALARMS CLEARED',lsr
    
def createChannelList(start=1, stop=97, step=1):
    '''Create a list of channels for tests'''
    channelList = []
    for chn in range(start,stop,step):
        channelList.append(chn)
    print 'CHANNEL LIST CREATED'
    return channelList
    
def createRandomChannelList(start=1,stop=96):
    '''Create a list of random channels for tests'''
    randomChannelList = []
    for i in range(start,stop,1):
        chn = random.randint(start,stop)
        randomChannelList.append(chn)
    print 'RANDOM CHANNEL LIST CREATED'
    return randomChannelList

def createRandomFtfList(start=-6000,stop=6000+10,step=100):
    randomFtfList=[]
    for i in range(start,stop,step):
        randomFtfList.append(i)
    print 'Random FTF LIST CREATED'
    return randomFtfList

def createFtfList(start=-6000, stop = 7000, step = 1000):
    '''Create a list of FTF range for tests'''
    ftfList = []
    for ftf in range(start, stop,step):
        ftfList.append(ftf)
    print 'FTF LIST CREATED'
    return ftfList

def createRandomPowerList():
    '''create random list of power range'''
    stop  = it.opsh()[1]
    start = it.opsl()[1]
    step = 10
    randomPowerList = []
    sequentialList = []
    for i in range(start,stop,step):
        sequentialList.append(i)
        #print sequentialList
    for s in range(len(sequentialList)):
        seq = random.choice(sequentialList)
        randomPowerList.append(seq)
        #print randomPowerList
    print 'RANDOM POWER LIST CREATED'
    return randomPowerList
    
    
        
def createPowerList(highestPower = 1600, lowestPower = 1000, steps = 50):
    '''create a list of power ranges for test'''
    powerListLowtoHigh = []
    powerListHightoLow = []
    negSteps = -(steps)
    for pwr in range(lowestPower,highestPower,steps):
       powerListLowtoHigh.append(pwr)
       print 'powerListLowtoHigh',powerListLowtoHigh

    for pwr1 in range(highestPower,lowestPower,negSteps):
       powerListHightoLow.append(pwr1)
       print 'powerListHightoLow', powerListHightoLow
        
    print 'POWER LIST CREATED'
    return powerListLowtoHigh,powerListHightoLow
    
def setChannel(chn):
    ''' set the channel to a frequency'''
    x = it.channel(chn)
    it.logentry(time.asctime())
    reg99 = it.readx99()
    if x[0]== 'XE':
        print 'RETURNED AN EXECUTION ERROR: MUST BE AN INVALID CHANNEL'
    else:
        print 'SET TO CHANNEL:',chn


def setChannelS(chn):
    ''' set the channel to a frequency'''
    x = it.channel(chn)
    it.logentry(time.asctime())
    #reg99 = it.readx99()
    if x[0]== 'XE':
        print 'RETURNED AN EXECUTION ERROR: MUST BE AN INVALID CHANNEL'
    else:
        print 'SET TO CHANNEL:',chn
    

def setFtf(ftf):
    '''Set the Fine Tune Frequency'''
    y = it.ftf(ftf)
    it.logentry(time.asctime())
    reg99 = it.readx99()
    if y[0] == 'XE':
        print 'RETURNED AN EXECUTION ERROR: MUST BE AN INVALID FTF'
    else:
        print 'SET TO FTF TO:',ftf


def setFtfS(ftf):
    '''Set the Fine Tune Frequency'''
    y = it.ftf(ftf)
    it.logentry(time.asctime())
    #reg99 = it.readx99()
    if y[0] == 'XE':
        print 'RETURNED AN EXECUTION ERROR: MUST BE AN INVALID FTF'
    else:
        print 'SET TO FTF TO:',ftf
        
        

def setPower(pwr):
    '''Set the Power Target'''
    p = it.pwr(pwr)
    it.logentry(time.asctime())
    reg99 = it.readx99()
    if p[0] == 'XE':
        print 'RETURNED AN EXECUTION ERROR: MUST BE AN INVALID POWER TARGET'
    else:
        print 'SET TO TARGET POWER TO:',pwr

def setPowerS(pwr):
    '''Set the Power Target'''
    p = it.pwr(pwr)
    it.logentry(time.asctime())
    #reg99 = it.readx99()
    if p[0] == 'XE':
        print 'RETURNED AN EXECUTION ERROR: MUST BE AN INVALID POWER TARGET'
    else:
        print 'SET TO TARGET POWER TO:',pwr
        
        
def findPowerHighAndLowLimits():
    '''Find the OPSH and OPSL '''
    h = it.opsh()
    l = it.opsl()
    return h[1],l[1]
    
def findWarningThresholds():
    '''Print all the Warning Threshold Values'''
    f = it.wFreqTh()
    p = it.wPowTh()
    a = it.wAgeTh()
    t = it.wThermTh()
    print 'WARNING FREQUENCY THRESHOLD:',f
    print 'WARNING POWER THRESHOLD:',p
    print 'WARNING AGE THRESHOLD:',a
    print 'WARNING THERMAL THRESHOLD:',t
    
def findFatalThresholds():
    f = it.fFreqTh()
    p = it.fPowTh()
    a = it.fAgeTh()
    t = it.fThermTh()
    print 'FATAL FREQUENCY THRESHOLD:',f
    print 'FATAL POWER THRESHOLD:',p
    print 'FATAL AGE THRESHOLD:',a
    print 'FATAL THERMAL THRESHOLD:',t
    

#####################EVAL BOARD/GPIO RELATED FUNCTIONS#######################################    
def setLdisLow():
    pass

def setLdisHigh():
    pass
    
def modselDisable(devType):
    if devType==1:
        g.MODSEL_N_Disable()                 #Disable modsel pins
    else:
        g.MODSEL_N_Disable()                 #Disable modsel pins
        g.MODSEL1_N_Disable()                #Disable modsel pins

def modselEnable(devType):
    if devType==1:
        g.MODSEL_N_Enable()                  #Enable modsel pins
    else:
        g.MODSEL_N_Enable()                  #Enable modsel pins
        g.MODSEL1_N_Enable()                 #Enable modsel pins

def reset(delay,g):
    g.setOutputState(5,0)
    print 'Setting RESET Line %0.2f PulseWidth'%delay
    it.logentry('Setting RESET Line %d PulseWidth'%delay)
    time.sleep(delay)
    g.setOutputState(5,1)


def resetLow(g):
    print 'Setting RESET Line Low'
    it.logentry('Setting RESET Line Low')
    g.setOutputState(5,0)

def resetHigh(g):
    print 'Setting RESET Line High'
    it.logentry('Setting RESET Line High')
    g.setOutputState(5,1)  
    
#####################HUAWEI RELATED FUNCTIONS#######################################
def triggerEcho():
    set = 1
    it.logentry(time.asctime())
    reg99 = it.readx99()
    it.write('\x91\x90\x00\x45')
    it.read(4)
    it.write('\xF1\x90\x00\x43')
    it.read(4)
    it.write('\x41\x90\x00\x48')
    it.read(4)
    it.write('\x31\x90\x00\x4F')
    it.read(4)
    time.sleep(.5)
    it.setpassword()
    reg99 = it.readx99()
    print 'ECHO COMMAND TRIGGERED'
    return set

def triggerEchoS():
    set = 1
    #it.logentry(time.asctime())
    #reg99 = it.readx99()
    it.write('\x91\x90\x00\x45')
    it.read(4)
    it.write('\xF1\x90\x00\x43')
    it.read(4)
    it.write('\x41\x90\x00\x48')
    it.read(4)
    it.write('\x31\x90\x00\x4F')
    it.read(4)
    time.sleep(.5)
    #it.setpassword()
    #reg99 = it.readx99()
    print 'ECHO COMMAND TRIGGERED'
    return set

def triggerTina():
    set = 1
    it.logentry(time.asctime())
    reg99 = it.readx99()
    it.write('\xa1\x93\x00\x54')
    it.read(4)
    it.write('\x61\x93\x00\x49')
    it.read(4)
    it.write('\x11\x93\x00\x4e')
    it.read(4)
    it.write('\xe1\x93\x00\x41')
    it.read(4)
    time.sleep(.5)
    it.setpassword()
    reg99 = it.readx99()
    print 'TINA COMMAND TRIGGERED'
    return set

def triggerTinaS():
    set = 1
    it.logentry(time.asctime())
    #reg99 = it.readx99()
    it.write('\xa1\x93\x00\x54')
    it.read(4)
    it.write('\x61\x93\x00\x49')
    it.read(4)
    it.write('\x11\x93\x00\x4e')
    it.read(4)
    it.write('\xe1\x93\x00\x41')
    it.read(4)
    time.sleep(.5)
    #it.setpassword()
    #reg99 = it.readx99()
    print 'TINA COMMAND TRIGGERED'
    return set
    
def triggerSoftReset():
    set = 1
    it.resena(sena=1,sr=1,mr=0)
    time.sleep(.5)
    it.setpassword()
    it.logentry(time.asctime())
    reg99 = it.readx99()
    print 'SOFT RESET TRIGGERED'
    return set

def triggerSoftResetS():
    set = 1
    it.resena(sena=1,sr=1,mr=0)
    time.sleep(.5)
    #it.setpassword()
    it.logentry(time.asctime())
    #reg99 = it.readx99()
    print 'SOFT RESET TRIGGERED'
    return set

def triggerMasterReset():
    set = 1
    it.resena(sena=1,sr=0,mr=1)
    time.sleep(.5)
    it.setpassword()
    it.logentry(time.asctime())
    reg99 = it.readx99()
    print 'MASTER RESET TRIGGERED'
    return set

def triggerMasterResetS():
    set = 1
    it.resena(sena=1,sr=0,mr=1)
    time.sleep(.5)
    #it.setpassword()
    it.logentry(time.asctime())
    #reg99 = it.readx99()
    print 'MASTER RESET TRIGGERED'
    return set

def huaweiPowerSupplySequence():
    x1,x2,ps1,ps2 = setpowerSupply()                                                                   #Initialize power supplies
    resetLow(g)                                                                                  #set the reset line low
    time.sleep(.04)                                                                              #delay 40ms
    supplyOff(ps2)                                                                               #turn supply off
    time.sleep(.850)                                                                             #delay 850ms
    supplyOn(ps2)                                                                                # turn supply on
    time.sleep(.3)                                                                               #delay 260ms
    resetHigh(g)                                                                                 #set reset line high
    time.sleep(.260)                                                                             #delay of 260ms before another reset
    reset(.02,g)                                                                                 #reset with 20 ms pulsewidth
    time.sleep(.5)



    
         
        
#####################IOCAP,RMS,FWDOWNLOAD RELATED FUNCTIONS#########################
        
##def setComslog():
##    it.setpassword()
##    a =   str(it.buildstring())
##    print a
##    ser = str(it.serNo())
##    rel=  str(it.release())
##    mon = str(it.monitor())    
    

def checkCom():
    tries = 3
    try:
        for i in range(tries):
            it.write('\x00\x00\x00\x00')
            reg = it.read(4)
            reg = str(len(reg))
            if reg != '4':
                print 'NO RS232 COMMUNICATION'
                a = open('blah')

        print'RS232 COMMUNICATION EXCELLENT'
    except(IOError):
        print 'STOP TEST'

def checkCombaud(devType):
    tries = 3
    try:
        for i in range(tries):
            it.write('\x00\x00\x00\x00')
            reg = it.read(4)
            reg = str(len(reg))
            if reg != '4':
                print 'NO RS232 COMMUNICATION'
                print 'SET TO DEFAULT'
                if devType == 1:
                    time.sleep(1)
                    it.baudrate(9600)
                    time.sleep(3)
                else:
                    time.sleep(1)
                    it.baudrate(57600)
                    time.sleep(3)
                return 0
            else:
                print 'RS232 COMMUNICATION GOOD'
                return 1
       
    except(IOError):
        print 'STOP TEST'
    
   
    

def inputRMS():
    '''input RMA TRUE OR FALSE'''
    state = 'NOT VALID'
    state = raw_input('Set RMS True or False:')
    state = state.capitalize()
    if state == 'True':
        state = bool(state)
        return state
    elif state == 'False':
        state = bool(not state)
        return state
    else:
        "INPUT True or False"
    

def inputType():
    '''input if it's single or dual uITLA'''
    maxTry = 2
    trials = 0
    
    while trials < maxTry:
        t = raw_input('Please Enter 1 for Single or 2 for Dual:')
        a = ''

        if int(t) == 1:
            print 'SINGLE MICROITLA'
            return 1
            break
        elif int(t) == 2:
            print 'DUAL MICROITLA'
            return 2
            break

            
        else:
            print "NOT VALID NUMBER ENTER 1 OR 2"
            trials += 1
        if trials == maxTry:
            print 'TOO MANY TRIES'
            break
            
def connectRS232(t,port):
    '''connect to rs232 depending on device type'''
    baudS = 9600
    baudD =57600
    if t == 1:                       #Connect if single
        it.laser(0)
        it.connect(port,baudS)
        checkCom()
    else:                            #Connect if dual
        it.laser(1)
        it.connect(port,baudD)
        checkCom()
    
def setRMS(state,baudTest,devType):
        if state == None:
            raise 'N0 VALUE STOP TEST'
        else:
            print 'Change baudarate to Test Baudrate'    #Set baudrate to Test baudrate
            it.baudrate(baudTest)
            #set  iocap
            print 'Change RMS to:',state          #change the RMS
            it.ioCap(baudTest,state)

            if devType == 1:
                rmsStat = it.ioCap()[1]               #validate change
                print 'CURRENT BAUD:',rmsStat.fieldCurrentBaudRate().cipher(),'CURRENT RMS:',int(rmsStat.fieldRms().value())

            else:
                rmsStat = it.ioCap()[1]               #validate change
                it.laser(1)
                print 'LASER1:','CURRENT BAUD:',rmsStat.fieldCurrentBaudRate().cipher(),'CURRENT RMS:',int(rmsStat.fieldRms().value())
                it.laser(2)
                print 'LASER2:','CURRENT BAUD:',rmsStat.fieldCurrentBaudRate().cipher(),'CURRENT RMS:',int(rmsStat.fieldRms().value())

def readRMS(devType):
    
        if devType == 1:
            rmsStat = it.ioCap()[1]               #validate change
            print 'CURRENT BAUD:',rmsStat.fieldCurrentBaudRate().cipher(),'CURRENT RMS:',int(rmsStat.fieldRms().value())

        else:
            rmsStat = it.ioCap()[1]               #validate change
            it.laser(1)
            print 'LASER1:','CURRENT BAUD:',rmsStat.fieldCurrentBaudRate().cipher(),'CURRENT RMS:',int(rmsStat.fieldRms().value())
            it.laser(2)
            print 'LASER2:','CURRENT BAUD:',rmsStat.fieldCurrentBaudRate().cipher(),'CURRENT RMS:',int(rmsStat.fieldRms().value())
    
                

def showBaud(devType):
    try:
        if devType == 1:
            print ' CHECK BAUDRATE'
            baud = it.baudrate()
            release = it.release()
            print 'BAUDRATE:', baud,
            print 'RELEASE:', release
        elif devType== 2:
            it.laser(1)
            baudAfter = it.baudrate()
            releaseAfter = it.release()
            print 'BAUDRATE LASER1:',baudAfter
            print 'RELEASE LASER1:', releaseAfter
            
            it.laser(2)
            baudAfter = it.baudrate()
            releaseAfter = it.release()
            print 'BAUDRATE LASER2:',baudAfter
            print 'RELEASE LASER2:', releaseAfter
        else:
             print'NOTHIN WILL HAPPEN BECAUSE THERE IS NOT DEVTYPE'
            
    except(IOError,ValueError,KeyboardError):
        print 'THERE IS ERROR'
        
def checkPassfail(state,result):
    if state == True and result == 1:
        print 'RMS 1 PASS TEST'
    elif state == True and result == 0:
        print 'RMS 1 FAIL TEST'
    elif state == False and result == 0:
        print 'RMS 0 PASS TEST'
    elif state == False and result ==1:
        print 'RMS 0 FAIL TEST'
    else:
        print 'NOTHING HAPPENED'


def inputFilename():
    file = raw_input('Enter File Name:')
    if file != None:
        newFile = str(file) + '.txt'
    else:
        newFile = 'IOCAP_TEST_APPLICATION.txt'
    return newFile
        
def inputBaud():
    MAXTRIES = 3
    Trial = 0
    while Trial < MAXTRIES:
        baud = raw_input('Enter Baudrate 9600, 19200,38400, 57600, 115200')
        baud = str(baud)
        print baud
        if baud == '9600':
            return int(baud)

        elif baud == '19200':
            return int(baud)

        elif baud == '38400':
            return int(baud)

        elif baud == '57600':
            return int(baud)

        elif baud == '115200':
            return int(baud)

        else:
            print 'NOT RECOGNIZED BAUDRATE'
            Trial +=1
            if Trial == 3:
                print 'TOO MANY TRIES'
                break
    
    
def ask():
    decide = raw_input('Test a different Baud? Enter 1 for Yes 0 for NO:')
    return int(decide)

def readReg():
    for i in range(5):
        reg = it.register(Register.Register(Register.DBG_RESET))
        reg92Out = reg[1].fieldSource().cipher()
    print reg92Out
    return reg92Out    

def upgradeFw(devType):
    print "DOWNLOADING FIRMWARE..."
    if devType == 1:
        it.upgrade('APPLICATION',r'C:\data\Sundial3_3740.ray')                 #Download New FW
        time.sleep(1)
    else:
        it.upgrade('APPLICATION',r'C:\data\hex_88\Sundial3D\Sundial3D.ray')                 #Download New FW
        time.sleep(1)
    

def upgradeFw_RST():
    print "DOWNLOADING FIRMWARE...PRESS HARD RESET WHILE DOWNLOADING"
    it.upgrade('APPLICATION',r'C:\data\hex_88\Sundial3D\Sundial3D.ray')                 #Download New FW
    time.sleep(1)
    checkRelease()



    
def checkRelease():
    try:
        itr = it.release()[1][1]
        if itr[21:24]== '2.1':
            print 'THIS IS THE MONITOR VERSION PASS'
            print itr
            return itr
        else:
            raise ValueError
            
    except:(ValueError)

def cleanUp(devType):


     if devType == 1:
##         it.baudrate(115200)
##         it.upgrade('APPLICATION',r'C:\data\hex_88\Sundial3\Sundial3.ray')
##         time.sleep(1)
         it.baudrate(9600)
     else:
##         it.baudrate(115200)
##         it.upgrade('APPLICATION',r'C:\data\hex_88\Sundial3D\Sundial3D.ray')
##         time.sleep(1)
         it.baudrate(57600)

def cleanUp_default(devType):
    
     if devType == 1:
         it.baudrate(115200)
         it.upgrade('APPLICATION',r'C:\data\hex_87\Sundial3\Sundial3.ray')
         time.sleep(1)
         it.baudrate(9600)
     else:
         it.baudrate(115200)
         it.upgrade('APPLICATION',r'C:\data\hex_87\Sundial3D\Sundial3D.ray')
         time.sleep(1)
         it.baudrate(57600)
    


def triggerMonitor():
    it.dlConfig(abrt = 1)
    it.dlConfig(init_write = 1, type = 3)
    print it.release()

###############################MODEHOP COUNTER RELATED FUNCTIONS#######################################

def clearRegister85():
    #Reset modehop counter to 0
    it.register(ITLA.Register.Register(address=0x85,data=0x0003),write=True)
    #Clear high watermark
    it.register(ITLA.Register.Register(address=0x85,data=0x0002),write=True)
    print 'REGISTER 0x85 CLEARED'

def readRegister85():
    glitchinfo = it.readAEAfloatarray(ITLA.Register.Register(address=0x85,data=0x0000))
    #it.register(ITLA.Register.Register(address=0x85,data=0x0002),write=True)
    f1highwatermark=glitchinfo[0]
    f2highwatermark=glitchinfo[2]
    #Count modehop
    hopcount = round(it.readAEAfloatarray(ITLA.Register.Register(address=0x85,data=0x0002))[0])
   # print 'F1:',f1highwatermark
   # print 'F2:',f2highwatermark
   # print 'TIME:',time.asctime(),'MODEHOP COUNT:',hopcount
    it.logentry('F1:'+ str(f1highwatermark))
    it.logentry('F2:'+ str(f2highwatermark))
    it.logentry('MODEHOPCOUNTER:'+ str(hopcount))
    return f1highwatermark,f2highwatermark, hopcount


def demodConv(val):
    if val>=32768: #0x8000
        fval = -(65536-float(val))#0x10000
    else:
        fval = float(val)
    return fval/1000.0       
    
    
    
def setFrequency(x):
    '''Setting Frequency For 100Mhz Gridspacing'''
    fcf = float(it.fcf()[1])
    ftf = float(it.ftf()[1])/1000000
    grid = float(it.grid()[1])
    grid = float(grid/10)
    highLimit = it.lfh()[1]
    lowLimit = it.lfl()[1]
    if x > highLimit or x < lowLimit:
        print 'THIS IS BEYOND THE LIMITS'
    else:
        chan = (float(x) - fcf-ftf)/(grid/1000)
        Channel = chan + 1.0
        it.channel(int(Channel))
        print 'FREQUENCY:',x, 'CHANNEL:',Channel
    
    
def randomStateMachine():
    
    statemachine = {}
##    statemachine['1']=['COLD_START'] 
##    statemachine['2']=['IDLE'] 
    statemachine['1']=['DARK'] 
    statemachine['2']=['TEMPERATURE'] 
    statemachine['3']=['GAIN_MEDIUM'] 
##    statemachine['3']=['ADJUSTMENT'] 
##    statemachine['4']=['FIRST_LIGHT'] 
    statemachine['4']=['CAVITY_LOCK'] 
    statemachine['5']=['POWER_LEVEL'] 
##    statemachine['4']=['CAVITY_OFFSET_LOCK'] 
    statemachine['6']=['STABILIZE'] 
    statemachine['7']=['CHANNEL_LOCK'] 
##    statemachine['13']=['FINE_TUNE'] 
##    statemachine['8']=['MZM_STATE'] 
    key = random.randint(1,6)
    status = statemachine.items()[key][1]
    for i in status:
        return i
        print str(status)


def stateClear(globleST,state,test_file):
    '''Function to monitor state operation'''
    print 'Waiting for pending bit to clear...'
    outstring = ''
    it.setpassword()
    timeOut = 40
    starttime = time.time()
    duration = time.time() - starttime
    while duration < timeOut:
        #pendingBit = str(int(it.nop()[1].fieldPending().value()))
        tunerState = it.readx99().tunerstate
        tunerState = tunerState.replace('TUNER_','')
        print tunerState
        it.logentry(time.asctime())
        reg99 = it.readx99()
        it.logentry(time.asctime())
        outstring = itpull(globleST,powermeter1,wavemeter1)
        test_file.write(outstring + '\n')
        if tunerState == state:
            reg99 = it.readx99()
            print tunerState
            print "TUNERSTATE HAS BEEN REACHED..."
            tuneTime = duration
            outstring = itpull(globleST,powermeter1,wavemeter1)
            test_file.write(outstring + '\n')
            break
        duration = time.time() - starttime
        if tunerState == 'CHANNEL_LOCK':
            reg99 = it.readx99()
            print tunerState
            print "TUNERSTATE HAS BEEN REACHED..."
            tuneTime = duration
            outstring = itpull(globleST,powermeter1,wavemeter1)
            test_file.write(outstring + '\n')
            break
        duration = time.time() - starttime
        if duration >=timeOut:
            outstring = itpull(globleST,powermeter1,wavemeter1)
            test_file.write(outstring + '\n')
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
    
    
def waitfortimeout(timeout=2):
    sys.stdout.write('Waiting ' + str(timeout) + ' seconds...')
    starttime = time.time()
    loopcount = 0
    while True:
        loopcount = loopcount + 1
        if not loopcount % 100:
            sys.stdout.write('.')
            sys.stdout.flush()
        it.nop()[1].data()
        it.readx99()
        if time.time() - starttime > timeout:
            print 'Done'
            break


def waitfortimeoutS(timeout=2):
    sys.stdout.write('Waiting ' + str(timeout) + ' seconds...')
    starttime = time.time()
    loopcount = 0
    while True:
        loopcount = loopcount + 1
        if not loopcount % 100:
            sys.stdout.write('.')
            sys.stdout.flush()
        it.nop()[1].data()
        #it.readx99()
        if time.time() - starttime > timeout:
            print 'Done'
            break


######################################################################FUNCTIONS FOR POWER TEST ENGINE#####################################################


def pendingClearMonPower(test_file1):
    '''Function to monitor pending operation'''
    print 'Waiting for pending bit to clear...'
    it.setpassword()
    timeOut = 90
    starttime = time.time()
    duration = time.time() - starttime
    while duration < timeOut:
        pendingBit = str(int(it.nop()[1].fieldPending().value()))
        f1highwatermark, f2highwatermark, hopcount = readRegister85()
        output = singleSaveData()
        test_file1.write(output)
        it.logentry(time.asctime())
        reg99 = it.readx99()
        if pendingBit == '0':
            output = singleSaveData()
            test_file1.write(output)
            reg99 = it.readx99()
            print "Pending bit Cleared..."
            tuneTime = duration
            break
        duration = time.time() - starttime
        if duration >=timeOut:
            it.logentry(time.asctime())
            reg99 = it.readx99()
            output = singleSaveData()
            test_file1.write(output)
            print it.temps()
            print it.currents()
            print it.statusF()
            print it.statusW()
            print it.readx99()
            raise "Tunetime more than 120 seconds: Stop Test"
    print 'TUNETIME:',tuneTime
    return tuneTime

def pollData(tuneTime,limit = 30):
    pollLimit = limit
    startTime = time.time()
    pollDataTime = time.time()-startTime
    while pollDataTime < pollLimit:
        output = singleSaveData(tuneTime)
        test_file1.write(output)
        pollDataTime = time.time()-startTime

    
        

    
    
    
    
    
        
        
    
    
    
    


