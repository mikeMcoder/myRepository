
#creator: Michael D. Mercado
#Date: December 31, 2015
#RegressionUtility.py is a collection of useful functions that can be applied to regression testing
#in OIF.
 
import os
import sys
import math
import struct
sys.path.append(os.path.abspath('.'))


def setComslog():
    '''Functions to enable the comslog during test'''
    it.setpassword()
    
def clearAlarms():
    '''Clears the warning and fatal alarm status'''
    return it.statusF(1,1,1,1,1,1,1,1),it.statusW(1,1,1,1,1,1,1,1)

def checkAlarms():
    '''Checks the warning and fatal alarm status'''
    print '#' * 20, 'WARNING ALARMS', '#' * 20
    print it.statusW()
    print '#' * 20, 'FATAL ALARMS', '#' * 20
    print it.statusF()
    
    
def pendingClear():
    '''Function to monitor pending operation'''
    print 'Waiting for pending bit to clear...'
    it.setpassword()
    timeOut = 60
    starttime = time.time()
    duration = time.time() - starttime
    while duration < timeOut:
        pendingFlag = str(int(it.nop()[1].fieldPending().value()))
        reg99 = it.readx99()
        if pendingFlag == '0':
            reg99 = it.readx99()
            print "Pending bit Cleared..."
            tuneTime = duration
            break
        duration = time.time() - starttime
        if duration >=timeOut:
            reg99 = it.readx99()
            print it.temps()
            print it.currents()
            print it.statusF()
            print it.statusW()
            raise "Tunetime more than 60 seconds: Stop Test"
    return tuneTime

def monChannellock( ):
    
    ''' Function to monitor channel lock condition'''
    print 'Waiting for Channel Lock...'
    it.setpassword()
    timeOut = 30 
    starttime = time.time()
    duration = time.time() - starttime
    while duration < timeOut:
        stateMachine = it.nopStats()[1].fieldStateMach().cipher()
        reg99 = it.readx99()
        if stateMachine == 'CHANNEL_LOCK':
            reg99 = it.readx99()
            print "Channel Locked..."
            tuneTime = duration
            break
        duration = time.time() - starttime
        if duration >=timeOut:
            reg99 = it.readx99()
            print it.temps()
            print it.currents()
            print it.statusF()
            print it.statusW()
            print it.nopStats()
            raise "Cannot Lock to a Channel: Stop the Test"
    return tuneTime


def timeStamp():
    daytime = time.asctime()
    daytimestr = daytime.replace(' ','')
    daytimestr = daytimestr.replace(':','')
    return daytimestr
  
def connectInstr():
    
    ConfigIni = parser.ConfigParser()
    #ConfigIni.read(r'C:\Documents and Settings\ttx.user\Desktop\MICROITLA_REGRESSION_TEST_SUITE\Python\Regression.ini')
    ConfigIni.read(r'\\photon\company\DWDM Engineering\Micro_ITLA\Firmware\Regression_Testing\Regression Test Scripts\MICROITLA_REGRESSION_TEST_SUITE_9\Python\Regression.ini')

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
        WM_cmd = ConfigIni.get('Station','WaveMeter1')
        print 'wavemeter1:',WM_cmd
        exec ('wavemeter1 = inst.%s'%(WM_cmd))
        wavemeter1.connect()
        
        PM_cmd = ConfigIni.get('Station','PwrMeter1')
        print 'pwrmeter1:',PM_cmd
        exec ('pwrmeter1 = inst.%s'%(PM_cmd))
        pwrmeter1.connect()
        print 'meters initialized'

    return wavemeter1,pwrmeter1,com_port,pwrlevelst, adtlst,samplingL,samplingP

def createHeader():
    header = ['SN',\
              'BUILD',\
              'TIMESTAMP',\
              'DURATION',\
              'CHANNEL',\
              'LF',\
              'FREQUENCY(METER)',\
              'FREQUENCY_ERROR(THZ)',\
              'PWR',\
              'OOP',\
              'POWERMETER(dBm)',\
              'POWER_ERROR',\
              'STATUSW(BIN)',\
              'STATUSW(HEX)',\
              'STATUSF(BIN)',\
              'STATUSF(HEX)',\
              'PENDING_BIT',\
              'STATUS',\
              'PCBT',\
              'GMI',\
              'TEC',\
              'SLED',\
              'F1',\
              'F2',\
              'SIBLOCK',\
              'DEMODR_ERROR',\
              'GMI',\
              'TEC',\
              'PHOTODIODE',\
              'N5_2V',\
              'DF1',\
              'DF2',\
              'SLED_CURRENT',\
              'PHOTODIODE_CURRENT',\
              'AGE']
    testfile = open('test_file.txt','w')
    for i in range(len(header)):
        pass
        
        


        
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
    
def dualconnectInstr():
    pass

def itpull(time0,pwr_meter,wave_meter,strtuneTime,status = ''):
    if 1:
        dummy0 = it.serNo()
        c0 = str(dummy0[1][1:])
        c0 = c0.strip("('")
        serial = c0.strip("',)")
        timeStamp = time.asctime()
        duration = str((time.time()-time0))
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
        exec ('powerM = str(pwr_meter.%s)'%(ConfigIni.get('Station','Pwr_Cmd')))
        exec ('waveM = str(wave_meter.%s)'%(ConfigIni.get('Station','Wave_Cmd')))
        age = str(it.age()[1])
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
        
        return serial+ "," + release+ "," + timeStamp + "," + duration + "," + lf + "," + channel + "," + waveM + "," + error + "," + \
               oop+ "," + powerM + "," + strpowError + "," + statWbin + "," + statFbin + "," + statWhex + "," + statFhex\
               + "," + sledT + "," + pcbT + "," + tec + "," + diode + "," + pending + "," + strtuneTime + "," + status + "," + age +"\n"



        
    
    
def setpowerSupply():
    ps1 = inst.psAG3631('GPIB0::06')
    ps1.connect()
    ps1.setOutputState('ON')
    ps1.setVoltCurr(selOutput = 'P6V', volts = mcuV ,current = defaultC)

    ps2 = inst.psAG3631('GPIB0::07')
    ps2.connect()
    ps2.setOutputState('ON')
    ps2.setVoltCurr(selOutput = 'P6V', volts = Supply_3_3 ,current = defaultC)











