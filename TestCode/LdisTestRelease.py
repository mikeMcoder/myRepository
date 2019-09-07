#LDIS Testing
#Author:Michael D.Mercado
#Date:6.26.18

import os
import sys
import time
import numpy as np
import pandas as pd
sys.path.append(r'\\photon\company\DWDM Engineering\Micro_ITLA\Firmware\Regression_Testing\Regression Test Scripts\MICROITLA_REGRESSION_TEST_SUITE_10\Python_DEVELOPMENT')
import aa_gpio.gpio
import FileManager as fm
import random
import threading

import TTM.TTM
import ITLA.ITLA
import instrumentDrivers as inst

t = TTM.TTM.TTM()
it = ITLA.ITLA.ITLA(t)
t.save_it_obj(it)
print "Instance Done.."

PORT = 3

class LaserDisableTest:
    def __init__(self):
        self.it = it
        self.g = None
        self.fm = fm.FileManager()
        self.timeStamp = None
        self.x99Logname = None
        self.inst = inst
        self.pm = None
        self.wm = None
        self.chnLst = []
    
        
    def initializeGpio(self):
        try:
            g = aa_gpio.gpio.gpio()    #instance of g object
            g.InitPin()                #initialize the aardvark dongle
            print 'passed here..'
            return g                   #return g object
        except:
            raise

    def activateInstruments(self):
        wm = self.inst.HP86120C('gpib0::21')
        wm.connect()
        pm = self.inst.pmHP8163('gpib0::11')
        pm.connect()
        return wm,pm

    def turnOnpowersupplies(self):
        ps = self.inst.psAG3631('gpib0::06')
        ps.connect()
        ps.setOutputState(state='ON')
        return ps

    def turnOffpowersupplies(self,ps):
        ps.setOutputState(state='OFF')
        

    def clearAlarms(self):
        self.it.statusF(1,1,1,1,1,1,1,1) #clear statusF
        self.it.statusW(1,1,1,1,1,1,1,1) #clear statusW

    def createRandomChannelList(self,start=1,stop=96):
        '''Create a list of random channels for tests'''
        randomChannelList = []
        for i in range(start,stop,1):
            chn = random.randint(start,stop)
            randomChannelList.append(chn)
        print 'RANDOM CHANNEL LIST CREATED'
        return randomChannelList


    def monChannellock(self,dataname,wm,pm):
        
        ''' Function to monitor channel lock condition'''
        print 'Waiting for Channel Lock...'
        datafile = open(dataname + ".txt","a")
        self.it.setpassword()
        timeOut = 60
        starttime = time.time()
        duration = time.time() - starttime
        newBit = 1
        while duration < timeOut:
            stateMachine = self.it.readx99().tunerstate
            self.it.logentry(time.asctime())
            serialNum = it.serNo()[1][1].rstrip('\x00') #serial number
            buildStr = it.buildstring()[19:28]#firmware version
            freq = wm.getFrequency()
            freqError = float(self.it.lf()[1]-freq)
            power = pm.getDisplayedPower()
            powerError = float(it.oop()[1])/100 - power
            statusW = hex(self.it.statusW()[1].data())
            statusF = hex(self.it.statusF()[1].data())
            pending = self.it.nop()[1].fieldPending().toBinaryString()
            pcbT = float(self.it.temps()[1][1][1])/100                  #pcb temp
            gmi = float(self.it.currents()[1][1][1])/10                 #gmi
            age = int(self.it.age()[1])                                 #age
            reg99 = self.it.readx99()
            f1 = reg99.f1temp
            f2 = reg99.f2temp
            siblock = reg99.siblocktemp
            gmi = reg99.gain_medium_current
            demodr = reg99.demodrealerr
            pd = reg99.photodiode_current
            sm = reg99.tunerstate
            sled = reg99.sled_temperature
            if stateMachine == 'TUNER_CHANNEL_LOCK':
                self.it.logentry(time.asctime())
                reg99 = self.it.readx99()
                print "Channel Locked..."
                tuneTime = duration
                #datafile.write(data) #is not needed because it will create to channel lock prints in the file MM 7.9.18
                datafile.close()
                break
            
            data = ','.join((str(duration),serialNum,buildStr,str(freq),str(freqError),str(power),str(powerError),str(statusW),str(statusF)\
                   ,str(pending),str(pcbT),str(gmi),str(age),str(f1),str(f2),str(siblock),str(gmi),str(demodr),str(pd)\
                   ,str(sm),str(sled),'\n')) # concatenate the data
            print data
            datafile.write(data)
        
                   

            duration = time.time() - starttime
            if duration >=timeOut:
                it.logentry(time.asctime())
                reg99 = self.it.readx99()
                print self.it.temps()
                print self.it.currents()
                print self.it.statusF()
                print self.it.statusW()
                print self.it.nopStats()
                datafile.write(data)
                datafile.close()
                print "Cannot Lock to a Channel: Stop the Test"
                raise 'STOP TEST'
        datafile.close()
        return tuneTime

    def snapShot(self,dataname,wm,pm,triggerTime):
        ''' Function to take snapshot of parameters'''
        datafile = open(dataname + ".txt","a") #open the file that needs appending
        self.it.setpassword()                  #enable x99
        timeOut = 30
        starttime = time.time()
        duration = time.time() - starttime
        stateMachine = self.it.readx99().tunerstate
        self.it.logentry(time.asctime())
        serialNum = it.serNo()[1][1].rstrip('\x00') #serial number
        buildStr = it.buildstring()[19:28]#firmware version
        freq = wm.getFrequency()
        freqError = float(self.it.lf()[1]-freq)
        power = pm.getDisplayedPower()
        powerError = float(it.oop()[1])/100 - power
        statusW = hex(self.it.statusW()[1].data())
        statusF = hex(self.it.statusF()[1].data())
        pending = self.it.nop()[1].fieldPending().toBinaryString()
        pcbT = float(self.it.temps()[1][1][1])/100                  #pcb temp
        gmi = float(self.it.currents()[1][1][1])/10                 #gmi
        age = int(self.it.age()[1])                                 #age
        reg99 = self.it.readx99()
        f1 = reg99.f1temp
        f2 = reg99.f2temp
        siblock = reg99.siblocktemp
        gmi = reg99.gain_medium_current
        demodr = reg99.demodrealerr
        pd = reg99.photodiode_current
        sm = reg99.tunerstate
        sled = reg99.sled_temperature
        data = ','.join((str(duration),serialNum,buildStr,str(freq),str(freqError),str(power),str(powerError),str(statusW),str(statusF)\
               ,str(pending),str(pcbT),str(gmi),str(age),str(f1),str(f2),str(siblock),str(gmi),str(demodr),str(pd)\
               ,str(sm),str(sled),str(triggerTime),'\n')) # concatenate the data
        datafile.write(data)
        datafile.close()
               
       

    def runTest(self):
        self.g = self.initializeGpio()              #initialize gpio
        time.sleep(2)
        self.ps = self.turnOnpowersupplies()                  #turn on supply
        time.sleep(3)
        self.it.connect(PORT)
        self.it.baudrate(115200)
        self.it.disconnect()
        self.it.connect(PORT,115200)                #connect
        self.it.setpassword()                       #unlock x99
        self.it.logging(True)                       #enable logging
        self.timeStamp = self.fm.logDate()          #log the time
        self.logFilename = "LaserDisableTest",self.timeStamp
        self.x99Logname = '_'.join(self.logFilename) #concatenate the txt
        self.filename = self.x99Logname + "_" + "x99" + ".txt"
        self.it.logfile(self.filename)              #create file name
        self.wm,self.pm = self.activateInstruments()#initialize intruments
        f,self.filename = self.fm.createFile(self.x99Logname)#open a file
        self.chnLst = self.createRandomChannelList()#create random channels
        for i in range(3):
            for chn in self.chnLst:
                self.pwr = self.it.opsh()[1]                                      #set to highest power
                self.ftf = 0                                                      #set to 0 ftf
                self.it.pwr(self.pwr)                                             #set power
                self.it.ftf(self.ftf)                                             #set ftf
                self.it.channel(chn)
                self.clearAlarms()                                                #clear alarms
                time.sleep(1)
                self.it.resena(1)                                                 #turn on laser
                self.monChannellock(self.filename,self.wm,self.pm)                #wait until unit channel locks




                try:
                    self.startAsserttime = time.time()
                    self.g.LDIS_N_Disable()                                       #disable laser
                    self.disBit = self.it.statusF()[1].fieldDis().toBinaryString()#read LDIS pin
                    if self.disBit == '1':                                        #check if the dis bit asserted
                        self.AssertTime = time.time()-self.startAsserttime
                        print "AssertTime:%f"%self.AssertTime
                    else:
                        print "The ldis bit did not assert"                       #if not stop test
                        raise
                except:
                    raise
                
                self.snapShot(self.filename,self.wm,self.pm,self.AssertTime)                     # take a snapshot of parameters durning ldis

                time.sleep(.5)                                                    #just to see the dis alarm turn on
                try:
                    self.startDeasserttime = time.time()
                    self.g.LDIS_N_Enable()#disable laser
                    cnt = 0
                    while 1:
                        self.disBit = self.it.statusF()[1].fieldDis().toBinaryString()#read LDIS pin
                        if self.disBit == '0':
                            self.DeassertTime = time.time()-self.startDeasserttime
                            print "DeassertTime:%f"%self.DeassertTime
                            break
                        else:
                            cnt+=5
                            #print "The ldis bit did not deassert"
                            if cnt ==1:
                                print "The ldis bit did not deassert"
                                raise
                        self.DeassertTime = time.time()-self.startDeasserttime
                except:
                    raise

                self.snapShot(self.filename,self.wm,self.pm,self.DeassertTime) # take a snapshot of parameters after ldis enabled again

                self.it.resena(1) #turn on the laser
                self.monChannellock(self.filename,self.wm,self.pm)#wait until unit channel locks
       
        self.it.disconnect()
        print "Test Complete"
        self.turnOffpowersupplies(self.ps)#turnoff supply
        

ldt = LaserDisableTest()

if __name__== '__main__':
    
    ldt.runTest()                       #run the main method
        
        





