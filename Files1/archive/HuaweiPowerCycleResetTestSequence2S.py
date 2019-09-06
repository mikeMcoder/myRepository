'''Author: Michael Mercado
   Date: June 15 2017

Requirements: To write a script that will copy the sequence

'''
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
import pandas

#import RegressionUtility_K

Utility = open('RegressionUtility_K.py','r')
exec(Utility)

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
P3_3 = inst.psAG3631('GPIB0::07')
PN5_2 = inst.psAG3631('GPIB0::06')

loop = 1500
PORT = 3
counter = 0
passcnt = 0
stuckcnt = 0
defaultCurrent_P6V = 1.50
defaultCurrent_n25V=1.0
defaultCurrent = 1.0
timeOut = 30.0

#Initialize and turn on 3.3V power supply

    
def initializeSupply():
    
    ps1 = inst.psAG3631('GPIB0::06')
    ps1.connect()
    ps1.setOutputState('ON')
    ps1.setVoltCurr(selOutput = 'P6V', volts = 3.3 ,current = defaultCurrent_P6V)
    ps1.setVoltCurr(selOutput = 'P25V', volts = 3.3 ,current = defaultCurrent)


    ps2 = inst.psAG3631('GPIB0::07')
    ps2.connect()
    ps2.setOutputState('ON')
    ps2.setVoltCurr(selOutput = 'N25V', volts = -5.2 ,current = defaultCurrent_n25V)
    return ps1,ps2

def supply1On():
    return ps1.setOutputState('ON')

def supply1Off():
    return ps1.setOutputState('OFF')

def supply2On():
    return ps2.setOutputState('ON')

def supply2Off():
    return ps2.setOutputState('OFF')

def readReg92():
    for i in range(5):
        it.readx99()
        command = Register.Register(Register.DBG_RESET)
        reg92 = it.register(command)
        reg92Out = reg92[1].fieldSource()
    return reg92Out

def cycleSupply(ps1,ps2,g):
##    supply2Off()
##    time.sleep(0.08)
##    g.reset_toggleOn()
##    time.sleep(.095)
##    supply2On()
##    time.sleep(.01)
##    supply1Off()
##    time.sleep(.02)
##    g.reset_toggleOff()
##    time.sleep(0.250)
##    supply1On()
    supply2Off()
    time.sleep(0.055)
    g.reset_toggleOn()
    #time.sleep(.060)
    time.sleep(0.102)
    supply1Off()
    time.sleep(2)
    supply2On()
    time.sleep(0.170)
    supply1On()
    time.sleep(.050)
    g.reset_toggleOff()
    time.sleep(0.500)
    g.reset_toggleOn()
    time.sleep(0.050)
    g.reset_toggleOff()
   
    


    
    
    
def randDelay():
    delayRise = random.randint(250,275)/1000.0
    delayFall = random.randint(0,299)/1000.0
    return delayRise,delayFall


def tx(cmd):
    it.write(cmd)
    rep = it.read(4)
    return rep   

def readReg():
    a = it.readx99()
    reg92 = readReg92()
    state = str(it.readx99())
    sled,pcb = it.temps()[1][1]
    tec,gmi = it.currents()[1][1]
    
    print 'Time:',time.asctime(),'NOP:',it.nop()[1].fieldPending().toBinaryString(),\
          'CHANNEL:',it.channel()[1],'NOPSTAT:',int(it.nopStats()[1].data()),'sled:',int(sled),'pcb:',int(pcb)\
    ,'tec:',int(tec),'gmi:',int(gmi),'OOP:',it.oop()[1],'92:',reg92 #### deleted'85:',readRegister85
    return state
    

def pendingClear():
    it.debugRS232(0)
    it.setpassword()
    timeOut = 60
    starttime = time.time()
    duration = time.time() - starttime
    while duration < timeOut:
        pendingFlag = str(int(it.nop()[1].fieldPending().value()))
        it.readx99()
        if pendingFlag == '0':
            it.readx99()
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
            print it.readx99()
            raise "Tunetime more than 60 seconds: Stop Test"
        #print "TIME:",time.asctime(),"Pending Bit:",pendingFlag
    return tuneTime

def setCommslog():
    it.logfile('HiSilicon_PowerCycle_RST_Test.txt')
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
        #it.readx99()
        if ( nopdat & 0xFF == 0x10):
            #it.readx99()
            break
        if (time.time() - starttime > timeout):
            #it.readx99()
            print 'Timed out'
            break

def createFileForVoltageTest(SN,dt,tempS='25C'):
    fname='C:\data\%s_HiSilicon_PowerCycle_RST_Test_%s_%s'%(SN,tempS,dt)
    f=open(fname,'w')
    
    s='%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %('CurrentTime','run_time', 'Tec','gmi','power','Tsled','Tpcb','statusF','statusW','Freq',\
    'nop','SetPwr','Frequency(Meter)','Filter1 Temp','Filter2 Temp','Siblock','DemodR','Sled','Gmi','PD','State_Machine')#,\
                                                             #'Filter1 Temp','Filter2 Temp','SiBlock Htr DAC', 'Filter1 Htr DAC','Filter2 Htr DAC',\
                                                              #     'PD current ADC','DemodR','StateMachine')
    f.writelines(s+'\n')
    f.close()
    print fname
    return fname


if __name__ == '__main__':

    ps1,ps2 = initializeSupply()  #Initialize power supply of rst and module
    it.disconnect()
    print 'wait for terminate the COM port, this is used for debug only'
    it.connect(PORT,0)
    time.sleep(3)
    it.logging('True')
    timestamp = timeStamp()
    it.logfile('HiSilicon_PowerCycle_RST_Test' + '_' + timestamp + '.txt')
    #it.setpassword(3)
    print 'ttm_laser1 connected!'
    cm=time.localtime()
    dateTime= '%d%02d%02d%02d%02d%02d.csv'%(cm[0],cm[1],cm[2],cm[3],cm[4],cm[5])
    (status,SN) = it.serNo()
    fn = createFileForVoltageTest(SN[1][0:10],dateTime)
    print fn
    alarmCounter = 0
    print 'Start collecting data...'
    #Main iteration
    for i in range(loop):
        #Turn on suply sequence
        ####MAIN####
        chn = random.randint(1,96)
        cycleSupply(ps1,ps2,g)
        time.sleep(5)
        waitformrdy( timeout = 30 )
        it.connect(PORT,0)
        it.resena(sr=1)
        time.sleep(5)
        waitformrdy( timeout = 30 )
        it.baudrate(9600)
        it.srqT(0,0,0,0,0,0,0,0,0)
        it.grid(500)
        it.pwr(1000)
        it.wPowTh(100)
        it.fPowTh(200)
        it.ditherE(0)
        it.fcf1(191)
        it.fcf2(1000)
        it.mcb(0,0,0)
        it.statusF(1,1,1,1,1,1,1,1)
        it.statusW(1,1,1,1,1,1,1,1)
        it.channel(79)
        waitformrdy( timeout = 30 )
        it.resena(1)
        dummy = it.nop()
        starttime = time.time()
        runT = time.time()-starttime 
        while(runT<= timeOut):
            f1=open(fn,'a')
            (status,(DataLength,Currents))=it.currents()
            (status,Power)=it.oop()
            (status,(DataLength,Temps))=it.temps()
            StatusF = it.statusF()
            StatusW = it.statusW()
            Freq = 0.0 #wm.getFrequency()
            (Status,ChanelFreq) = it.lf()
            PowerIdx= 0.0
            it.logentry(str(time.asctime()))
            internal = '0'#it.readx99()
            f1_temp = str(float(it.dbgTemps(0)[1].data())/100)
            f2_temp = str(float(it.dbgTemps(1)[1].data())/100)
            siBlock = str(float(it.dbgTemps(3)[1].data())/100)
            demodR = '0'#internal.demodrealerr
            sled = str(float(it.dbgTemps(2)[1].data())/100)
            gmi = str(float(it.dbgTemps(16)[1].data())/100)
            pd = str(float(it.dbgTemps(4)[1].data())/100)
            state = '0'#internal.tunerstate
            currentTime = timeStamp()
            runT = time.time()-starttime         	         	
            s = '%s,%8.3f,%4d,%4d,%4d,%4d,%4d,0x%04x,0x%04x,%8.4f,0x%04x,%d,%s,,%s,,%s,,%s,,%s,,%s,,%s,,%s,%s'\
            %(currentTime,runT,Currents[0],Currents[1],Power,Temps[0],Temps[1],StatusF[1].data(),StatusW[1].data(),ChanelFreq,dummy[1].data(),PowerIdx,Freq,f1_temp,\
            f2_temp,siBlock,demodR,sled,gmi,pd,state)
            #print s
            f1.writelines(s+'\n')
            f1.close()
            time.sleep(1)
            dummy = it.nop()
        if it.nop()[1].fieldPending().toBinaryString()=='00000000':
            print time.asctime(),'Power Cycle Successful:',i
        else:
            for i in range(10):
                f1=open(fn,'a')
                (status,(DataLength,Currents))=it.currents()
                (status,Power)=it.oop()
                (status,(DataLength,Temps))=it.temps()
                StatusF = it.statusF()
                StatusW = it.statusW()
                Freq = 0.0 #wm.getFrequency()
                (Status,ChanelFreq) = it.lf()
                PowerIdx= 0.0
                #it.readx99()
                it.logentry(str(time.asctime()))
                internal = '0'#it.readx99()
                f1_temp = str(float(it.dbgTemps(0)[1].data())/100)
                f2_temp = str(float(it.dbgTemps(1)[1].data())/100)
                siBlock = str(float(it.dbgTemps(3)[1].data())/100)
                demodR = '0'#internal.demodrealerr
                sled = str(float(it.dbgTemps(2)[1].data())/100)
                gmi = str(float(it.dbgTemps(16)[1].data())/100)
                pd = str(float(it.dbgTemps(4)[1].data())/100)
                state = '0'#internal.tunerstate
                currentTime = timeStamp()
                runT = time.time()-starttime         	         	
                s = '%s,%8.3f,%4d,%4d,%4d,%4d,%4d,0x%04x,0x%04x,%8.4f,0x%04x,%d,,%s,,%s,,%s,,%s,,%s,,%s,,%s,,%s,%s'\
                %(currentTime,runT,Currents[0],Currents[1],Power,Temps[0],Temps[1],StatusF[1].data(),StatusW[1].data(),ChanelFreq,dummy[1].data(),PowerIdx,Freq,f1_temp,\
                f2_temp,siBlock,demodR,sled,gmi,pd,state)
                #print s
                f1.writelines(s+'\n')
                f1.close()
                time.sleep(1)
                dummy = it.nop()
            
            raise 'Pending Stuck!!!!'

    it.disconnect()
    print 'test comlete'
