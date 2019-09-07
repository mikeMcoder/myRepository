import matplotlib as plt
import random
import math
import struct
import sys
import os
import time
import instrumentDrivers as inst
import ConfigParser as parser
sys.path.append(os.path.abspath('.'))
import ITLA.Register as Register
import RegressionUtility_I
import serial

s = serial.Serial(port = 'COM5',baudrate = 9600)
s.write(chr(0x01) + chr(0x65)) # open
s.write(chr(0x01) + chr(0x6F)) # close

Utility = open('RegressionUtility_I.py','r')
exec(Utility)





import TTM.TTM
t = TTM.TTM.TTM()

newITLA=True

if newITLA:
    # override ITLA module function to ignore AEA_EA and AEA_EAC which are not implemented on the older FW
    import ITLA.ITLA
    class newITLAITLAITLA(ITLA.ITLA.ITLA,object):
        def register(self, register = None, write = 0):
            if register.name() == ITLA.Register.Register(ITLA.Register.AEA_EA).name():
                # create dummy return data
                register = ITLA.Register.Register(ITLA.Register.AEA_EA,2)
                return( ('OK',register) )
            if register.name() == ITLA.Register.Register(ITLA.Register.AEA_EAC).name():
                # create dummy return data
                register = ITLA.Register.Register(ITLA.Register.AEA_EAC)
                register.fieldIncr().value(2)
                register.fieldRai().value(1)
                return( ('OK',register) )
            return ( super(newITLAITLAITLA, self).register( register,  write ) )
        def setpassword(self,passwordlevel=None):
            self.register(ITLA.Register.Register(address=0x80,data=0x1428),write=True)
            self.register(ITLA.Register.Register(address=0x81,data=0x5700),write=True)
    
    it = newITLAITLAITLA(t)
else:
    import ITLA.ITLA
    it = ITLA.ITLA.ITLA(t)

#import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'


import aa_gpio.gpio
g = aa_gpio.gpio.gpio()
g.InitPin()
P3_3 = inst.psAG3631('GPIB0::06')
PN5_2 = inst.psAG3631('GPIB0::07')


loop = 5000
port = 3
counter = 0
passcnt = 0
stuckcnt = 0
defaultCurrent_P6V = 1.50
defaultCurrent = 1.0
testName = 'CiscoRMATest'
channels=[195.35,191.45,193,192.95,192.9]
repeat = 200
   
def initializeSupply():
    
    ps1 = inst.psAG3631('GPIB0::07')
    ps1.connect()
    ps1.setOutputState('ON')
    ps1.setVoltCurr(selOutput = 'P6V', volts = 3.3 ,current = defaultCurrent_P6V)
    ps1.setVoltCurr(selOutput = 'P25V', volts = 3.3 ,current = defaultCurrent)


    ps2 = inst.psAG3631('GPIB0::06')
    ps2.connect()
    ps2.setOutputState('ON')
    ps2.setVoltCurr(selOutput = 'P6V', volts = 3.3 ,current = defaultCurrent_P6V)
    return ps1,ps2

def supplyOn(ps2):
    return ps2.setOutputState('ON')

def supplyOff(ps2):
    return ps2.setOutputState('OFF')

def setRST(ps1):
    ON = 3.3
    OFF = 0
    #rise,fall = randDelay()
    amplitude = 'AMPLITUDE 0V'
    it.logentry('FALLING EDGE')
    ps1.setVoltCurr(selOutput = 'P25V', volts = OFF ,current = defaultCurrent) #PULL RESET LOW
    #time.sleep(fall)
    supplyOff()             #TURN OFF 3.3 SUPPLY
    time.sleep(1.5)         #DELAY OF > 1S
    supplyOn()              #TURN SUPPLY ON
    time.sleep(10)          #WAIT 10 SEC TO KEEP THE RST PULLED LOW
    it.logentry(amplitude)
    it.logentry('RISING EDGE')
    ps1.setVoltCurr(selOutput = 'P25V', volts = ON ,current = defaultCurrent) #PULL RESET HIGH
    
        
    
def randDelay():
    delayRise = random.randint(250,275)/1000.0
    delayFall = random.randint(0,299)/1000.0
    return delayRise,delayFall


def tx(cmd):
    it.write(cmd)
    rep = it.read(4)
    return rep   

class CT1class:
    def ReadRegAbs(self,writedata):
        #register = (writedata & 0x00FF0000 )/ 0x00010000
        register = writedata & 0xFF
        #data = writedata & 0x0000FFFF
        retdat=it.register(ITLA.Register.Register(address=register,data=0),write=False)
        #print retdat
        return (retdat[1].data())

    def WriteRegAbs(self,writedata,Value):
        #register = (writedata & 0x00FF0000 )/ 0x00010000
        register = writedata & 0xFF
        #data = writedata & 0x0000FFFF
        retdat=it.register(ITLA.Register.Register(address=register,data=Value),write=True)
        #print retdat
        return (retdat[1].data())
        
def getfloat():
    byte1and2 =  CT1.ReadRegAbs(0x0004a00B)
    byte3and4 =  CT1.ReadRegAbs(0x0004a00B)
    return(struct.unpack('<f',struct.pack('>H',byte1and2) +  struct.pack('>H',byte3and4 ))[0])

def pendingClear1(datafile):

    starttime = time.time()
    alarmdat = 0xFFFF
    #while( CT1.ReadRegAbs(0x0004a000) & 0xFF00 ):
    tunetime = time.time() - starttime
    while(time.time() - starttime < 60 and (alarmdat & 0x7fff )!= 0):
        # clear alarms
        dataSet = readReg(tunetime)
        chn = it.lf()[1]
        timestamp = str(time.asctime())
        it.register(ITLA.Register.Register(address=ITLA.Register.STATUSW,data=0xFFFF),write=True)
        alarmdat = it.statusW()[1].data()
        datafile.write(timestamp + ',' + str(chn)  + ','+  dataSet + ',' + str(alarmdat) +'\n')
        tunetime = time.time() - starttime
        
    print 'ALARM:',alarmdat,'TUNETIME:',tunetime
    return tunetime
    

        
CT1=CT1class()

def readReg(tunetime):
    temp =  CT1.ReadRegAbs(0x0004a058)
    tempLaser =  CT1.ReadRegAbs(0x0004a00B)
    tempLaserfloat = (struct.unpack('h', struct.pack('H', tempLaser))[0]/100.0) 
    #print 'tempLaserfloat: %.02f'%tempLaserfloat
    tempCase =  CT1.ReadRegAbs(0x0004a00B)
    tempCasefloat = (struct.unpack('h', struct.pack('H', tempCase))[0]/100.0)
    #print 'tempCasefloat:%.02f'%tempCasefloat 
    tempEtalon =  CT1.ReadRegAbs(0x0004a00B)
    tempEtalonfloat = (struct.unpack('h', struct.pack('H', tempEtalon))[0]/100.0)
    #print 'tempEtalonfloat:%.02f'%tempEtalonfloat 
    powerLaser =  CT1.ReadRegAbs(0x0004a042)
    powerLaserfloat = (struct.unpack('h', struct.pack('H', powerLaser))[0]/100.0)
    #print 'powerLaserfloat:%.02f'%powerLaserfloat
    temp =  CT1.ReadRegAbs(0x0004a065)
    vcc =  CT1.ReadRegAbs(0x0004a00B)
    vccfloat = (vcc/100.0)
    #print 'vccfloat:%.02f'%vccfloat 
    temp =  CT1.ReadRegAbs(0x0004a057)
    LosaTECI =  CT1.ReadRegAbs(0x0004a00B)
    LosaTECIfloat =(struct.unpack('h', struct.pack('H', LosaTECI))[0]/10.0)
    #print 'LosaTECIfloat:%.02f'%LosaTECIfloat 
    LaserI =  CT1.ReadRegAbs(0x0004a00B)
    LaserIfloat=(LaserI/10.0)
    #print 'LaserIfloat:%.02f'%LaserIfloat
    WosaTECI =  CT1.ReadRegAbs(0x0004a00B)
    WosaTECIfloat=(struct.unpack('h', struct.pack('H', WosaTECI))[0]/10.0)
    #print 'WosaTECIfloat:%.02f'%WosaTECIfloat
    soaI =  CT1.ReadRegAbs(0x0004a00B)
    soaIfloat=(soaI/10.0) 
    #print 'soaIfloat:%.02f'%soaIfloat
    temp =  CT1.ReadRegAbs(0x0004a0B8)
    memsx = getfloat()
    temp =  CT1.ReadRegAbs(0x0004a0B8)
    memsy = getfloat()    
    #print 'memsxfloat:%.04f'%memsx
    print 'tunetime:',tunetime,'tempLaserfloat: %.02f'%tempLaserfloat,'tempCasefloat:%.02f'%tempCasefloat,'tempEtalonfloat:%.02f'%tempEtalonfloat,'powerLaserfloat:%.02f'%powerLaserfloat,'vccfloat:%.02f'%vccfloat\
          ,'LosaTECIfloat:%.02f'%LosaTECIfloat,'LaserIfloat:%.02f'%LaserIfloat,'WosaTECIfloat:%.02f'%WosaTECIfloat,'soaIfloat:%.02f'%soaIfloat,'memsxfloat:%.04f'%memsx,'memsyfloat:%.04f'%memsy
    data = str(tunetime) + ',' + str(tempLaserfloat)+','+str(tempCasefloat)+','+str(tempEtalonfloat)+','+str(powerLaserfloat)+','+str(vccfloat) +','+str(LosaTECIfloat)+\
           ','+ str(LaserIfloat)+ ','+ str(WosaTECIfloat)+','+str(soaIfloat)+ ',' +str(memsx)+','+ str(memsy)
    return data

def pendingClear():
    it.debugRS232(0)
    #it.setpassword()
    timeOut = 60
    starttime = time.time()
    duration = time.time() - starttime
    while duration < timeOut:
        pendingFlag = str(int(it.nop()[1].fieldPending().value()))
        #it.readx99()
        if pendingFlag == '0':
            #it.readx99()
            print "Pending bit Cleared"
            tuneTime = duration
            it.debugRS232(0)
            break
        
        duration = time.time() - starttime
        if duration >=timeOut:
            
            print it.temps()
            print it.currents()
            print it.statusF()
            print it.statusW()
            print it.channel()
            print it.nop()
            raise "Tunetime more than 60 seconds: Stop Test"
        #print "TIME:",time.asctime(),"Pending Bit:",pendingFlag
    return tuneTime

   
                  
def setCommslog(name):
    it.logfile(name + '.txt')
    it.logging(True)
    it.setpassword()
    

def waitformrdy( timeout = 30 ):
    #it.setpassword()
    print 'Waiting for mrdy clear...'
    starttime = time.time()
    while True:
        sys.stdout.write('.')
        time.sleep(.010)
        nopdat = it.nop()[1].data()
        if ( nopdat & 0xFF == 0x10):
            print '\n'
            break
        if (time.time() - starttime > timeout):
            print 'Timed out'
            print '\n'
            break
def createRandomChannel():
    chn = random.randint(1,96)
    return chn


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
    
#power on sequence
#write channel
#write 0x62 ftf
#delay 100ms
#set resena(1)
#timout 65seconds
#delay 100ms
#read statusW
#check power and wavelength warning
#if warning is yes timeout,log timeout, repeat 10x
#if warning is no clear retry counter,log stability time


def runScript():
    #create logfile in csv
    timeStamp = str(time.asctime())
    timeStamp = timeStamp.replace(':','')
    datafile = open('dataCollection'+'_' + timeStamp + '.csv','w')
    header = 'TIMESTAMP'+','+'CHANNEL' + ',' + 'TUNETIME'+','+'TEMP_LASER_FLOAT' + ',' + 'TEMP_CASE_FLOAT'+ ',' +' TEMP_ETHALON_FLOAT'+ ',' + 'POWER_LASER_FLOAT' \
    + ',' +'VCC_FLOAT' + ',' + 'LOSA_TECI_FLOAT' + ',' + 'LASER_I_FLOAT'+ ','+'WOSA_TEC_I_FLOAT' + ','+  'SOA_I_FLOAT'\
    + ',' + 'MEMS_X_FLOAT' + ',' + 'MEMS_Y_FLOAT' +',' + 'STATUSW'

    datafile.write(header)
    datafile.write('\n')

    for rep in range(repeat):
        print '*' * 10 ,'Iteration:',rep,'*' * 10
        #iterate different channels[195.35,191.45,193,192.95,192.9]
        for c in channels:
            #power on sequence
            s.write(chr(0x01) + chr(0x65))
            time.sleep(60)
            s.write(chr(0x01) + chr(0x6F))
            #ps1,ps2= initializeSupply()
           # ps2.setOutputState('OFF')  #Initialize power supply of rst and module
            #time.sleep(20)
           # ps2.setOutputState('ON')
            it.disconnect()
            it.connect(port)              #connect to rs 232
            setCommslog(testName)         #Set logging enable
            it.debugRS232(0)              #set 1 if need to be in debug mode
            time.sleep(.5)
            #write channel
            setFrequency(c)
            #write 0x62 ftf
            it.ftf(100)
            time.sleep(.1)
            it.resena(1)
            pendingClear1(datafile)

    it.disconnect()
    datafile.close()
    print 'Test Complete...'


