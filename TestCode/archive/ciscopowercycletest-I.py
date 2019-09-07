
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
P3_3 = inst.psAG3631('GPIB0::07')
PN5_2 = inst.psAG3631('GPIB0::06')

loop = 5000
port = 3
counter = 0
passcnt = 0
stuckcnt = 0
defaultCurrent_P6V = 1.50
defaultCurrent = 1.0


   
def initializeSupply():
    
    ps1 = inst.psAG3631('GPIB0::06')
    ps1.connect()
    ps1.setOutputState('ON')
    ps1.setVoltCurr(selOutput = 'P6V', volts = 3.3 ,current = defaultCurrent_P6V)
    ps1.setVoltCurr(selOutput = 'P25V', volts = 3.3 ,current = defaultCurrent)


    ps2 = inst.psAG3631('GPIB0::07')
    ps2.connect()
    ps2.setOutputState('ON')
    ps2.setVoltCurr(selOutput = 'P6V', volts = 3.3 ,current = defaultCurrent_P6V)
    return ps1,ps2

def supplyOn():
    return ps2.setOutputState('ON')

def supplyOff():
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

def pendingClear1():

    starttime = time.time()
    
    alarmdat = 0xFFFF
    #while( CT1.ReadRegAbs(0x0004a000) & 0xFF00 ):
    while(time.time() - starttime < 60 and (alarmdat & 0x7fff )!= 0):
        # clear alarms
        it.register(ITLA.Register.Register(address=ITLA.Register.STATUSW,data=0xFFFF),write=True)
        alarmdat = it.statusW()[1].data()
        tunetime = time.time() - starttime
    print 'ALARM:',alarmdat,'TUNETIME:',tunetime
    return tunetime
    

        
CT1=CT1class()

def readReg():
    temp =  CT1.ReadRegAbs(0x0004a058)
    tempLaser =  CT1.ReadRegAbs(0x0004a00B)
    tempLaserfloat = (struct.unpack('h', struct.pack('H', tempLaser))[0]/100.0) 
    print 'tempLaserfloat: %.02f'%tempLaserfloat
    tempCase =  CT1.ReadRegAbs(0x0004a00B)
    tempCasefloat = (struct.unpack('h', struct.pack('H', tempCase))[0]/100.0)
    print 'tempCasefloat:%.02f'%tempCasefloat 
    tempEtalon =  CT1.ReadRegAbs(0x0004a00B)
    tempEtalonfloat = (struct.unpack('h', struct.pack('H', tempEtalon))[0]/100.0)
    print 'tempEtalonfloat:%.02f'%tempEtalonfloat 
    powerLaser =  CT1.ReadRegAbs(0x0004a042)
    powerLaserfloat = (struct.unpack('h', struct.pack('H', powerLaser))[0]/100.0)
    print 'powerLaserfloat:%.02f'%powerLaserfloat
    temp =  CT1.ReadRegAbs(0x0004a065)
    vcc =  CT1.ReadRegAbs(0x0004a00B)
    vccfloat = (vcc/100.0)
    print 'vccfloat:%.02f'%vccfloat 
    temp =  CT1.ReadRegAbs(0x0004a057)
    LosaTECI =  CT1.ReadRegAbs(0x0004a00B)
    LosaTECIfloat =(struct.unpack('h', struct.pack('H', LosaTECI))[0]/10.0)
    print 'LosaTECIfloat:%.02f'%LosaTECIfloat 
    LaserI =  CT1.ReadRegAbs(0x0004a00B)
    LaserIfloat=(LaserI/10.0)
    print 'LaserIfloat:%.02f'%LaserIfloat
    WosaTECI =  CT1.ReadRegAbs(0x0004a00B)
    WosaTECIfloat=(struct.unpack('h', struct.pack('H', WosaTECI))[0]/10.0)
    print 'WosaTECIfloat:%.02f'%WosaTECIfloat
    soaI =  CT1.ReadRegAbs(0x0004a00B)
    soaIfloat=(soaI/10.0) 
    print 'soaIfloat:%.02f'%soaIfloat
    temp =  CT1.ReadRegAbs(0x0004a0B8)
    memsx = getfloat()
    print 'memsxfloat:%.04f'%memsx
    
    data = str(tempLaserfloat)+','+str(tempCasefloat)+','+str(tempEtalonfloat)+','+str(powerLaserfloat)+','+str(vccfloat) +','+str(LosaTECIfloat)+','+ str(LaserIfloat)+ ','+ str(WosaTECIfloat)+','+str(soaIfloat)+ ',' +str(memsx)
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

   
                  
def setCommslog():
    it.logfile('ERIC_FW_PowerCycle_RST_Test.txt')
    it.logging(True)
    #it.setpassword()
    

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

ps1,ps2 = initializeSupply()  #Initialize power supply of rst and module
it.disconnect()
it.connect(port)    #connect to rs 232
setCommslog()       #Set logging enable
it.debugRS232(0)    #set 1 if need to be in debug mode
time.sleep(.5)
#strSer = str(it.serNo())
#ser = str(strSer[14:24])
#print it.buildstring()
#print ser
it.resena(1)
pendingClear1()
timeStamp = str(time.asctime())
timeStamp = timeStamp.replace(':','')
datafile = open('dataCollection'+'_' + timeStamp + '.csv','w')
header = 'TIMESTAMP'+','+'CHANNEL' +','+'ITERATION'+','+'TEMP_LASER_FLOAT' + ',' + 'TEMP_CASE_FLOAT'+ ',' +' TEMP_ETHALON_FLOAT'+ ',' + 'POWER_LASER_FLOAT' \
+ ',' +'VCC_FLOAT' + ',' + 'LOSA_TECI_FLOAT' + ',' + 'LASER_I_FLOAT'+ ','+'WOSA_TEC_I_FLOAT' + ','+  'SOA_I_FLOAT'\
+ ',' + 'MEMS_X_FLOAT' + ',' + 'TUNETIME'

datafile.write(header)
datafile.write('\n')

if __name__ == '__main__':
    
    try:  

        #Main iteration
        for i in range(loop):
                  
            #Turn on suply sequence
            ####MAIN####
            supplyOn()
            setRST(ps1)
            time.sleep(1)
            waitformrdy( timeout = 30 )
            state = readReg()
            chn = createRandomChannel()
            timeStamp1 = str(time.asctime())
            tunetime = 0
            datafile.write(timeStamp1 + ',' + str(chn)+ ',' + str(i) + ',' + state + ',' + str(tunetime) + '\n')
            print 'PARAMETERS AFTER HARD RESET:',readReg()
            it.channel(chn)
            print 'set to channel:',chn
            it.resena(1)
            print 'send sena =1'
            tunetime = pendingClear1()
            state = readReg()
            timeStamp2 = str(time.asctime())
            datafile.write(timeStamp2 + ',' + str(chn)+ ',' + str(i) + ',' + state + ',' + str(tunetime) + '\n')
            print 'PARAMETERS AFTER PENDING CLEARED:',readReg()
            passcnt += 1
            print "Pending Cleared COUNTER:", passcnt
            time.sleep(10)
            
      
    except Exception,e:
          datafile.close()
          print e
    it.disconnect()
    datafile.close()
