#Author: Michael Mercado
#Date: September 19, 2015
#Description: The objective of this test to tests the firmware's basic functionalities such as testing the read registers and the important
#write registers  OIF
            
########################################################################################################################################################################


import sys
import os
import sys
import time
import math
import aa_gpio.gpio
import instrumentDrivers as inst
import ConfigParser as parser
import pandas
import re
g = aa_gpio.gpio.gpio()
g.InitPin()

ConfigIni = parser.ConfigParser()
ConfigIni.read(r'\\photon\company\DWDM Engineering\Micro_ITLA\Firmware\Regression_Testing\Regression Test Scripts\RegressionIni')
sys.path.append(os.path.abspath('.'))

sys.path.append(os.path.abspath('.'))

if sys.platform == 'cygwin':
    # for cygwin, use the packages installed from the windows installation of python
    sys.path.append('/cygdrive/c/Python27/Lib/site-packages/')

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'

utility = open('RegressionUtility_L.py','r')
exec(utility)
import instrumentDrivers as inst
ps = inst.psAG3631('GPIB0::06')
ps.connect()


loop = 5001
port = input('Enter Port#')
if type(port) != type(3):
    print 'Must be an integer'
else:
    com_port = port
    
laser = 0
baud = 115200
unitType = 'single' #type single or dual depending onthe unit
devType = 1                             #single uitla
channelList = [1,50,96]  #channel list low mid and high channels
powerList = [1350,1200,1000]
ftfList = [-6000,3000,0,3000,6000]
path = 'c:\data'
fw = 'Sundial3_V03.07.09.93'
RMS = [0,1]
baudLst = [115200,57600,38400,19200,9600]

mcbList = [1,0]
debugrs232 = False



####################################################################################################
#############################   MAIN PROGRAM  ######################################################
####################################################################################################



class SanityCheck:
      
    def __init__(self):
        self.it = it
    def loadFirmware(self):
        pass
    
    def waitfortimeout(timeout=25.0):
        sys.stdout.write('Waiting ' + str(timeout) + ' seconds...')
        starttime = time.time()
        loopcount = 0
        while True:
            loopcount = loopcount + 1
            if not loopcount % 100:
                sys.stdout.write('.')
                sys.stdout.flush()
            it.readx99()
            it.nop()
            if time.time() - starttime > timeout:
                print 'Done'
                return (time.time() - starttime)


####
    def laserDisabletest(self,g):
           
        
        try:
            it.connect(com_port,baud)
            it.logging(True)
            print '*' * 10,  'TEST:LDIS TEST', '*' * 10
            #Verify ldis
            for chn in [1,5,15,35,45,55,65,75,85]:
                it.resena(0)
                time.sleep(0.5)
                it.channel(chn)
                print "tune to channel:%d"%chn
                it.resena(1) #turn on laser
                pendingClear()#wait for pending to clear
                monChannellock()#wiat to chanel lock
                clearAlarms()
                print "Trigger LDIS"
                g.LDIS_N_Disable()
                time.sleep(1)
                checkAlarms()
                time.sleep(1)
                print "Set Back to Normal"
                g.LDIS_N_Enable()
                time.sleep(1)
                checkAlarms()
            it.disconnect()
            print "Test Done"
        except(IOError,ValueError):
            raise'FAILED'



    def moduleSelecttest(self,g):
        
        try:
            print '*' * 10,  'TEST:MS TEST', '*' * 10
            it.connect(3,0)

            devType = inputType()                #input if it is single or dual microitla
           
            for r in RMS:
                 for bd in baudLst:
                     print "TEST#1"
                     filename = 'APPLICATION_TEST_MS' + '_' + 'RMS'+ '_'+ str(r) + '_' + str(bd) + '.txt'          #createfile
                     baudTest = bd                        #input baudrate to test
                     it.logfile(filename)                 #enter filename in comslog
                     it.logging(True)                   #enable logging
                     it.disconnect()
                     connectRS232(devType,com_port)           #Connect to Rs232
                     setComslog()                         #set comslog
                     state = r                            #Input RMS True or False
                     setRMS(state,baudTest,devType)       #set the RMS
                     print 'DISABLE MODSELECT PIN'
                     it.logentry('DISABLE MODSEL PIN')
                     modselDisable(devType)
                     time.sleep(2)
                     showBaud(devType)                    #Show the baudrate and release
                     print 'ENABLE MODSELECT PIN'
                     it.logentry('ENABLE MODSEL PIN')
                     modselEnable(devType)
                     it.baudrate(115200)                  #Set baudrate to non default Value(115200)
                     result = checkCombaud(devType)       #check if there is communication
                     time.sleep(1)
                     showBaud(devType)                    #Show the baudrate and release
                     checkPassfail(state,result)          #Check if unit pass/fail
                     cleanUp(devType)
                     time.sleep(1)
            it.disconnect()
            print 'TEST DONE'

               
        except:
            KeyboardInterrupt

    def hardResettest(self,g):
        
        try:
            
            print '*' * 10,  'TEST:RST TEST', '*' * 10
            #Verify RST
        
            it.connect(com_port,baud)
            it.logging(True)
            print '*' * 10,  'TEST: hardResettest', '*' * 10
                #Verify hard reset
            for chn in [1,5,15,35,45,55,65,75,85]:
                it.resena(0)
                time.sleep(0.5)
                it.channel(chn)
                print "tune to channel:%d"%chn
                it.resena(1) #turn on laser
                pendingClear()#wait for pending to clear
                monChannellock()#wiat to chanel lock
                clearAlarms()
                checkAlarms()
                g.reset(1)
                print 'TRIGGER RST PIN'
                time.sleep(2)
                turnOnLaser()
                checkAlarms()
            it.disconnect()
            print ' HardReset Test Done...'
            
        except(IOError,ValueError):
            raise'FAILED'


    def mainResettest(self):
        
        try:
            
            it.connect(com_port,baud)
            it.logging(True)
            print '*' * 10,  'TEST: MainResettest', '*' * 10
                #Verify hard reset
            for chn in [1,5,15,35,45,55,65,75,85]:
                it.resena(0)
                time.sleep(0.5)
                it.channel(chn)
                print "tune to channel:%d"%chn
                it.resena(1) #turn on laser
                pendingClear()#wait for pending to clear
                monChannellock()#wiat to chanel lock
                clearAlarms()
                checkAlarms()
                it.resena(mr=1)
                print 'TRIGGER MASTER RESET COMMAND'
                time.sleep(2)
                turnOnLaser()
                checkAlarms()
            it.disconnect()
            print 'MainReset Test Done...'
            
        except(IOError,ValueError):
            raise'FAILED'

    def softResettest(self):
        
        try:
          
            it.connect(com_port,baud)
            it.setpassword()
            it.logging(True)
            print '*' * 10,  'TEST: SoftResettest', '*' * 10
                #Verify hard reset
            for chn in [1,5,15,35,45,55,65,75,85]:
                it.resena(0)
                time.sleep(0.5)
                it.channel(chn)
                print "tune to channel:%d"%chn
                it.resena(1) #turn on laser
                pendingClear()#wait for pending to clear
                monChannellock()#wiat to chanel lock
                clearAlarms()
                checkAlarms()
                it.resena(sr=1)
                print 'TRIGGER SOFT RESET COMMAND'
                time.sleep(2)
                turnOnLaser()
                checkAlarms()
            it.disconnect()
            print 'SoftReset Test Done...'
            
        except(IOError,ValueError):
            raise'FAILED'

    def adtTest(self):
        
        try:
            it.connect(com_port,baud)
            it.logging(True)
            print '*' * 10,  'TEST:ADT TEST' ,'*' * 10
            for adtValue in mcbList:

                for chn in [1,5,15,35,45,55,65,75,85]:
                    print 'ADT:',adtValue
                    pollTime = 0
                    pollLimit = 15
                    it.mcb(adt = adtValue)
                    it.channel(chn)
                    print "tune to channel:%d"%chn
                    it.resena(0)
                    clearAlarms()
                    it.resena(1)
                    while pollTime <= pollLimit:
                        print 'TIME:', time.asctime(),'PENDING:',it.nop()[1].fieldPending().toBinaryString(),'STATUSW:',hex(int(it.statusW()[1].data())),'STATUSF:',hex(int(it.statusF()[1].data())),'OOP:',it.oop()[1]
                        pollTime += 1
                        time.sleep(1)
            it.disconnect()
            print 'Adt Test done...'
                
        except(IOError,ValueError):
             raise'FAILED'

    def nopTest(self):
        timeLimit = 600
        for i in range(1):
            print 'Start...'
            try:
                it.connect(com_port,baud)
                it.setpassword()
                it.logging(True)
                it.logfile('TransientTesting' + '_' + str(i) + '.txt')
                failcount = 0
                start = time.time()
                lapseTime = time.time() - start
                while lapseTime <=timeLimit:
                    print '*' * 10,  'TEST:NOP-PENDINGBIT TEST' ,'*' * 10
                    for channel in [1,50,90]:
                        print 'Tune to Channel:',channel
                        pollTime=0
                        pollLimit = 30
                        it.mcb(adt = 1)
                        print '*' * 10,  'LASER TRANSIENT' ,'*' * 10
                        it.channel(channel)
                        it.resena(0)
                        waitfortimeout(timeout=10)
                        clearAlarms()
                        sledtempCheck = it.readx99().sled_temperature
                        if sledtempCheck >=60 or sledtempCheck<=40:
                            failcount +=1
                            it.logentry('Fail Flag:' + str(failcount))
                            print '( -  |  - )( -  |  - )( -  |  - )( -  |  - )Fail Count:',failcount ,'( -  |  - )( -  |  - )( -  |  - )( -  |  - )'                  
                        it.resena(1)
                        startTime= time.time()
                        while pollTime <= pollLimit:
                            x99 = it.readx99()
                            print 'TIME:', pollTime,'PENDING:',it.nop()[1].fieldPending().toBinaryString(),'STATUSW:',hex(int(it.statusW()[1].data())),'STATUSF:',hex(int(it.statusF()[1].data())),'OOP:',it.oop()[1],'F1:',x99.f1temp,\
                                  'F2:',x99.f2temp,'SiBlock:',x99.siblocktemp,'DemodR:',x99.demodrealerr,'GMI:',x99.gain_medium_current,'PD:',x99.photodiode_current,'SLED:',x99.sled_temperature,'StateMachine:',x99.tunerstate
                            pollTime =time.time()-startTime
                            time.sleep(.100)
                            
                        lapseTime = time.time() - start
                        if lapseTime >= timeLimit:
                            break
                            
                        pollTime=0
                        pollLimit = 30

                        print '*' * 10,  'LASER TRANSIENT & POWER' ,'*' * 10

                        it.resena(0)
                        waitfortimeout(timeout=10)
                        clearAlarms()
                        sledtempCheck = it.readx99().sled_temperature
                        if sledtempCheck >=60 or sledtempCheck<=40:
                            failcount +=1
                            it.logentry('Fail Flag:' + str(failcount))
                            print '( -  |  - )( -  |  - )( -  |  - )( -  |  - )Fail Count:',failcount ,'( -  |  - )( -  |  - )( -  |  - )( -  |  - )'  
                        it.resena(1)
                        
                        it.pwr(1300)
                        startTime= time.time()
                        while pollTime <= pollLimit:
                            x99 = it.readx99()
                            print 'TIME:', pollTime,'PENDING:',it.nop()[1].fieldPending().toBinaryString(),'STATUSW:',hex(int(it.statusW()[1].data())),'STATUSF:',hex(int(it.statusF()[1].data())),'OOP:',it.oop()[1],'F1:',x99.f1temp,\
                                  'F2:',x99.f2temp,'SiBlock:',x99.siblocktemp,'DemodR:',x99.demodrealerr,'GMI:',x99.gain_medium_current,'PD:',x99.photodiode_current,'SLED:',x99.sled_temperature,'StateMachine:',x99.tunerstate
                            pollTime =time.time()-startTime
                            time.sleep(.100)
                        
                        pwr = it.opsh()[1]
                        it.pwr(pwr)#back to default
                        it.resena(0)
                        waitfortimeout(timeout=1)
                        it.resena(1)
                        waitfortimeout(timeout=15)
                        
                        lapseTime = time.time() - start
                        if lapseTime >= timeLimit:
                            break

                        pollTime=0
                        pollLimit = 30

                        print '*' * 10,  'LASER TRANSIENT & POWER & FTF' ,'*' * 10

                        it.resena(0)
                        waitfortimeout(timeout=10)
                        clearAlarms()
                        sledtempCheck = it.readx99().sled_temperature
                        if sledtempCheck >=60 or sledtempCheck<=40:
                            failcount +=1
                            it.logentry('Fail Flag:' + str(failcount))
                            print '( -  |  - )( -  |  - )( -  |  - )( -  |  - )Fail Count:',failcount ,'( -  |  - )( -  |  - )( -  |  - )( -  |  - )'   
                        it.resena(1)
                        
                        it.pwr(1300)
                        waitfortimeout(timeout=.1)
                        it.ftf(3000)

                        startTime= time.time()
                        while pollTime <= pollLimit:
                            x99 = it.readx99()
                            print 'TIME:', pollTime,'PENDING:',it.nop()[1].fieldPending().toBinaryString(),'STATUSW:',hex(int(it.statusW()[1].data())),'STATUSF:',hex(int(it.statusF()[1].data())),'OOP:',it.oop()[1],'F1:',x99.f1temp,\
                                  'F2:',x99.f2temp,'SiBlock:',x99.siblocktemp,'DemodR:',x99.demodrealerr,'GMI:',x99.gain_medium_current,'PD:',x99.photodiode_current,'SLED:',x99.sled_temperature,'StateMachine:',x99.tunerstate
                            pollTime =time.time()-startTime
                            time.sleep(.100)

                        lapseTime = time.time() - start
                        if lapseTime >= timeLimit:
                            break
                            
                        
                        pwr = it.opsh()[1]
                        it.pwr(pwr)#back to default
                        it.ftf(0)#set to 0ghz offset
                        it.resena(0)
                        waitfortimeout(timeout=1)
                        it.resena(1)
                        waitfortimeout(timeout=15)
                    lapseTime = time.time() - start
                    if lapseTime >= timeLimit:
                        break
                    print "Total Lapse Time:",lapseTime
                it.resena(mr=1)
                time.sleep(5)
                it.disconnect()
                
            except(IOError,ValueError):
                 raise'FAILED'
                
        print 'nop test done...'
    



    def genConfigtest(self):
        
        try:
            it.connect(3)
            it.setpassword()
            DEFAULT_POWER = it.opsh()[1]
            DEFAULT_CHANNEL = it.channel()[1]
            DEFAULT_GRID = it.grid()[1]
            DEFAULT_MCB = 1
            DEFAULT_FCF = it.fcf()[1]
            NEW_POWER = 1000
            NEW_CHANNEL = 40
            NEW_GRID = 1
            NEW_MCB = 0
            NEW_FCF = 193.8

            it.connect(3,0)
            it.setpassword()
            it.logging(True)
            print '*' * 10,  'TEST:GENCONFIG TEST', '*' * 10
            #Verify RST
            it.resena(0)
            print 'CHANNEL BEFORE GENCONFIG:%d'%DEFAULT_CHANNEL
            print 'POWER BEFORE GENCONFIG:%d'%DEFAULT_POWER
            print 'GRID BEFORE GENCONFIG:%d'%DEFAULT_GRID
            print 'FCF BEFORE GENCONFIG:%f'%DEFAULT_FCF
            print 'MCB BEFORE GENCONFIG:%d'%DEFAULT_MCB
            print 'CHANGE THE SETTINGS THE ISSUE GENCONFIG..'
            it.fcf(NEW_FCF)
            print 'FCF:',it.fcf()[1]
            it.pwr(NEW_POWER)
            print 'POWER:',it.pwr()[1]
            it.grid(NEW_GRID)
            print 'GRID:',it.grid()[1]
            it.channel(NEW_CHANNEL)
            print 'CHANNEL:',it.channel()[1]
            it.mcb(NEW_MCB)
            print 'MCB:',it.mcb()[1].fieldAdt()
            print 'ISSUE GENCONFIG...'
            it.genCfg(1)
            print 'Power Cycle.....'
            ps.setOutputState('OFF')
            time.sleep(3)
            ps.setOutputState('ON')
            time.sleep(4)
            if unitType == 'dual':
                it.laser(1) #dual
            else:
                it.laser(0) #single
        
            it.connect(com_port,baud)
            time.sleep(2)

            
            
            print 'CHANNEL AFTER GENCONFIG:',it.channel()[1]
            print 'POWER AFTER GENCONFIG:',it.pwr()[1]
            print 'GRID AFTER GENCONFIG:',it.grid()[1]
            print 'FCF AFTER GENCONFIG:',it.fcf()[1]
            print 'MCB AFTER GENCONFIG:',it.mcb()[1].fieldAdt()

            

            print 'SET BACK TO DEFAULT...'
            it.fcf(DEFAULT_FCF)
            it.pwr(DEFAULT_POWER)
            it.grid(DEFAULT_GRID)
            it.channel(DEFAULT_CHANNEL)
            it.mcb(1)
            it.genCfg(1)
            ps.setOutputState('OFF')
            time.sleep(1)
            ps.setOutputState('ON')
            time.sleep(4)
            if unitType == 'dual':
                it.laser(1) #dual
            else:
                it.laser(0) #single
        
            it.disconnect()
            print' Genconfig Test Done...'


            
        except(IOError,ValueError):
            raise'FAILED'

    def resenaTest(self):
        
        it.connect(3)
        it.logging(True)
        def addMarkers():
            print '##########' * 5
            
        print '*' * 10,  'TEST:RESENA COMBINATION TEST', '*' * 10

        try:
            ##Send Resena (sena = 1)	Laser turns on
            print '*' * 10,'Send Resena (sena = 1)	Laser turns on','*' * 10
            it.resena(0)
            print it.resena(sena = 1)
            addMarkers()
            print 'Clear Alarms...'
            clearAlarms()
            addMarkers()
            print 'Wait until pending bit clears...'
            pendingClear()
            addMarkers()
            print 'Check alarms again...'
            checkAlarms()
            addMarkers()
            print 'Read OOP'
            print it.oop()
            addMarkers()
            print 'Read Reset Source'
            print it.dbgReset()

            addMarkers()
            addMarkers()
            addMarkers()

            
    #While laser on , send resena(sena=1)	returns OK no change
            print '*' * 10,'While laser on , send resena(sena=1)	returns OK no change','*' * 10
            print it.resena(sena = 1)
            addMarkers()
            print 'Clear Alarms...'
            clearAlarms()
            addMarkers()
            print 'Wait until pending bit clears...'
            pendingClear()
            addMarkers()
            print 'Check alarms again...'
            checkAlarms()
            addMarkers()
            print 'Read OOP'
            print it.oop()
            addMarkers()
            print 'Read Reset Source'
            print it.dbgReset()


            addMarkers()
            addMarkers()
            addMarkers()


    #While laser on , send resena(sena=1, sr=1,mr=0)	returns 'XE'
            print '*' * 10,'While laser on , send resena(sena=1, sr=1,mr=0)	returns XE for non- Huawei, OK for Huawei','*' * 10
            print it.resena(sena = 1)
            addMarkers()
            print 'Clear Alarms...'
            clearAlarms()
            addMarkers()
            print 'Wait until pending bit clears...'
            pendingClear()
            time.sleep(10)
            addMarkers()
            print 'Send it.resena(sena=1,sr=1,mr=0)...'
            print it.resena(sena=1,sr=1,mr=0)
            addMarkers()
            print 'Check alarms again...'
            time.sleep(1)
            checkAlarms()
            addMarkers()
            print 'Read OOP'
            print it.oop()
            print 'Read Reset Source'
            print it.dbgReset()


            addMarkers()
            addMarkers()
            addMarkers()



    ##While laser on , send resena(sena=1, sr=0  ,mr=1)	Main Reset Triggered
            print '*' * 10,'While laser on , send resena(sena=1, sr=0  ,mr=1)	Main Reset Triggered','*' * 10
            print it.resena(1)
            addMarkers()
            print 'Clear Alarms...'
            clearAlarms()
            addMarkers()
            print 'Wait until pending bit clears...'
            pendingClear()
            addMarkers()
            print 'Send it.resena(sena=1,sr=0,mr=1)...'
            print it.resena(sena=1,sr=0,mr=1)
            time.sleep(2)
            if unitType == 'dual':
                it.laser(1) #dual
            else:
                it.laser(0) #single
            addMarkers()
            print 'Reconnect...'
            it.connect(com_port,baud)
            it.setpassword()
            time.sleep(2)
            addMarkers()
            print 'Check alarms again...'
            checkAlarms()
            addMarkers()
            print 'Read OOP'
            print it.oop()
            print 'Read Reset Source'
            print it.dbgReset()



            
    ##While laser on , send resena(sr=0  ,mr=1)	Main Reset Triggered
            print '*' * 10,'While laser on , send resena(sr=0  ,mr=1)	Main Reset Triggered','*' * 10
            print it.resena(1)
            clearAlarms()
            pendingClear()
            print it.resena(sr=0, mr=1)
            if unitType == 'dual':
                it.laser(1) #dual
            else:
                it.laser(0) #single
        
            it.connect(com_port,baud)
            it.setpassword()
            time.sleep(2)
            checkAlarms()
            it.oop()
            
    ##While laser on , send resena(sr=1  ,mr=0)	Main Reset Triggered
            print '*' * 10,'While laser on , send resena(sr=1  ,mr=0)	Main Reset Triggered','*' * 10
            print it.resena(1)
            clearAlarms()
            pendingClear()
            print it.resena(sr=1,mr=0)
            if unitType == 'dual':
                it.laser(1) #dual
            else:
                it.laser(0) #single
        
            it.connect(com_port,baud)
            it.setpassword()
            time.sleep(2)
            checkAlarms()
            it.oop()
            
    ##While laser on , send resena(sr=1  ,mr=1)	Main Reset Triggered
            print '*' * 10,'While laser on , send resena(sr=1  ,mr=1)	Main Reset Triggered','*' * 10
            print it.resena(1)
            clearAlarms()
            pendingClear()
            print it.resena(sr=1,mr=1)
            if unitType == 'dual':
                it.laser(1) #dual
            else:
                it.laser(0) #single
        
            it.connect(com_port,baud)
            it.setpassword()
            time.sleep(2)
            checkAlarms()
            it.oop()
            
    ##While laser is off, send resena(sena=1, sr=0, mr = 0)	Laser turns on
            print '*' * 10,'While laser is off, send resena(sena=1, sr=0, mr = 0)	Laser turns on','*' * 10
            print it.resena(0)
            print it.resena(1)
            clearAlarms()
            pendingClear()
            checkAlarms()
            it.oop()

    ##While laser is off, send resena(sena=1, sr=1,  mr = 0)	Returns a 'XE'
            print '*' * 10,'While laser is off, send resena(sena=1, sr=1,  mr = 0)	Returns a XE','*' * 10
            it.resena(0)
            print it.resena(sena=1,sr=1,mr=0)
            if unitType == 'dual':
                it.laser(1) #dual
            else:
                it.laser(0) #single
        
            it.connect(com_port,baud)
            it.setpassword()
            time.sleep(2)
            checkAlarms()
            it.oop()
            
    ##While laser is off, send resena(sena=1, sr=0,  mr = 1)	Main Reset Triggered
            print '*' * 10,'While laser is off, send resena(sena=1, sr=0,  mr = 1)	Main Reset Triggered','*' * 10
            it.resena(0)
            print it.resena(sena=1,sr=0,mr=1)
            if unitType == 'dual':
                it.laser(1) #dual
            else:
                it.laser(0) #single
        
            it.connect(com_port,baud)
            it.setpassword()
            time.sleep(2)
            checkAlarms()
            it.oop()


    ##While laser is off, send resena(sr=0,  mr = 1)	Main Reset Triggered
            print '*' * 10,'While laser is off, send resena(sr=0,  mr = 1)	Main Reset Triggered','*' * 10
            it.resena(0)
            print it.resena(sena=0,sr=0,mr=1)
            if unitType == 'dual':
                it.laser(1) #dual
            else:
                it.laser(0) #single
        
            it.connect(com_port,baud)
            it.setpassword()
            time.sleep(2)
            checkAlarms()
            it.oop()


    ##While laser is off, send resena(sr=1,  mr = 0)	Main Reset Triggered
            print '*' * 10,'While laser is off, send resena(sr=1,  mr = 0)	Main Reset Triggered','*' * 10
            it.resena(0)
            print it.resena(sena=0,sr=1,mr=0)
            if unitType == 'dual':
                it.laser(1) #dual
            else:
                it.laser(0) #single
        
            it.connect(com_port,baud)
            it.setpassword()
            time.sleep(2)
            checkAlarms()
            it.oop()


    ##While laser is off, send resena(sr=1,  mr = 1)	Main Reset Triggered
            print '*' * 10,'While laser is off, send resena(sr=1,  mr = 1)	Main Reset Triggered','*' * 10
            it.resena(0)
            print it.resena(sena=0,sr=1,mr=1)
            if unitType == 'dual':
                it.laser(1) #dual
            else:
                it.laser(0) #single
        
            it.connect(com_port,baud)
            it.setpassword()
            time.sleep(2)
            checkAlarms()
            it.oop()

    ##Send resena(-1)	returns 'XE'
            print '*' * 10,'Send resena(-1)	returns XE','*' * 10
            print it.resena(sena=-1)
        except(IOError,ValueError):
            raise'FAILED'


    def fPowthTest(self):
        

        print '\n\n'    
        print '*' * 10,'FPOWTH TEST','*' * 10

        try:
            it.connect(com_port,baud)
            it.setpassword()
            it.logging(True)
            #put 10db value to the register and check the result
            print 'Put a value of 10dbm to fpowth..'
            response = it.fPowTh(1000)[1]
            print 'Read the fpowth..'
            if it.fPowTh()[0]=='OK':
                print 'fpowth is:',response
                print 'PASS'
            else:
                print 'fpowth is:',response
                print 'FAIL'

            # set the value above the threshold of 1000 and read register           
            
            print 'Put a value above 10dbm to fpowth..'
            response = it.fPowTh(1500)[0]
            print 'Read the fpowth..'
            if response =='XE':
                print 'fpowth is:',response
                print 'PASS'
            else:
                print 'fpowth is:',response
                print 'FAIL'
                
            #set the value to 0 and read register

            print 'Put a value of 0dbm to fpowth..'
            response =  it.fPowTh(0)[0]
            print 'Read the fpowth..'
            if response=='XE':
                print 'fpowth is:',response
                print 'PASS'
            else:
                print 'fpowth is:',response
                print 'FAIL'            
            print 'FpowTh Test Done...'
            it.disconnect()


        except(IOError,ValueError):
            raise'FAILED'



    def wPowThTest(self):
        print '\n\n'    
        print '*' * 10,'WPOWTH TEST','*' * 10

        try:
            #input 3 values to see if it changes
            it.connect(com_port,baud)
            it.setpassword()
            it.logging(True)
            print 'Input 3 values to see if it changes...'
            th_value = [0,1,100,1000]
            for th in th_value:
                print it.wPowTh(th)
                      
            print 'Put a value below 0 or a negative number...'
            neg_value = -1
            print it.wPowTh(neg_value)
            
            print 'put a value above the fpowth...'
            above_value = 1001
            print it.wPowTh(above_value)
            it.disconnect()
            print 'wPowTh Test Done...'
            

        except(IOError,ValueError):
            raise'FAILED'



    def freqandThermalthresholdTest(self):

        try:   
            print '\n\n'    
            print '*' * 10,'FREQ and THERM THRESHOLD TEST','*' * 10
            it.connect(com_port,baud)
            it.setpassword()
            it.logging(True)
            print 'fFreqTh:',it.fFreqTh()#freqfatalth
            print 'wFreqTh:',it.wFreqTh()#warningfreqth
            print 'fThermTh:',it.fThermTh()#fthermth
            print 'wThermTh:',it.wThermTh()#wthermth
            it.disconnect()
            print 'frequencyandThermThresholdTest Done...'
        except:
            raise 'Failed'
    

    def srqTest(self):
        try:
            
            print '\n\n'    
            print '*' * 10,'SRQT TEST','*' * 10
            it.connect(com_port,baud)
            it.setpassword()
            it.logging(True)
            print 'Set the SRQT to trigger if there is a XEL'
            print it.srqT(1,1,1,1,1,1,1,1,1,1,1,1,1)
            print 'Trigger the XEL by sending a command that that is not valid'
            print it.wPowTh(-1)
            print 'Read register'
            print it.statusF()
            
            print 'Set the SRQT to not trigger if there is a XEL'
            print it.srqT(0,0,0,0,0,0,0,0,0,0,0,0,0)
            print 'Trigger the XEL by sending a command that that is not valid'
            print it.wPowTh(-1)
            print 'Read register'
            print it.statusF()
            it.disconnect()
            print 'srqTest Done...'
            it.disconnect()
        except:
            raise 'Failed'

    def fatalTTest(self):
        try:
            
            print '\n\n'    
            print '*' * 10,'FATALT TEST','*' * 10
            #assert fatalT bit
            ##    1.  Do a resena (mr=1) to create MRL then FATAL should trigger
            it.connect(com_port,baud)
            it.setpassword()
            it.logging(True)
            print'Trigger MRL...'
            print it.resena(mr=1)
            time.sleep(3)
            if unitType == 'dual':
                it.laser(1) #dual
            else:
                it.laser(0) #single

            it.connect(com_port,baud)
            it.setpassword()
            print it.fatalT(1,1,1,1,1,1,1,1,1)
            checkAlarms()
            print it.fatalT(0,0,0,0,0,0,0,0,0)
            checkAlarms()
            it.disconnect()
            print 'fatalTTest Done...'
        except:
            raise 'Failed'

    def almTTest(self):

        try:
            print '\n\n'    
            print '*' * 10,'ALMT TEST','*' * 10
            print 'Disable  Wfreq and WPWR of ALMT'
            it.connect(com_port,baud)
            it.setpassword()
            it.logging(True)
            print it.almT(0,0,0,0,0,0,0,0)
            print 'mcb(set adt=1)'
            print it.mcb(adt=1)
            print 'Turn on laser by sending sena=1'
            clearAlarms()
            print it.resena(sena=1)
            for i in range(40):
                print 'ALM Bit:',it.statusF()[1].fieldAlm()
                time.sleep(0.5)

            it.resena(0)
            
            print 'Enable  Wfreq and WPWR of ALMT.'
            print it.almT(1,1,1,1,1,1,1,1)
            print 'Turn on laser by sending sena=1'
            clearAlarms()
            print it.resena(sena=1)
            for i in range(40):
                print 'ALM Bit:',it.statusF()[1].fieldAlm()
                time.sleep(0.5)
            it.disconnect()
            print 'almT Test Done...'
        except:
            raise 'Failed'


    def channelTest(self):

        #try:
            
        print '\n\n'    
        print '*' * 10,'CHANNEL TEST','*' * 10
        print 'Set channel to (0) and read value'
        it.connect(com_port,baud)
        it.setpassword()
        it.logging(True)
        print "Test1:"
        print 'Setting channel to 0'
        it.channel(0)
        print 'Reading channel after setting to 0:', it.channel()
        
        print "Test2:"
        print 'Set channel to channel above the highest channel and read value'
        print it.channel(200)
        print 'The channel after setting to highest channel:',it.channel()[1]

        print "Test3:"
        print 'Turn on laser'
        print it.resena(sena=1)
        #self.waitfortimeout()
        print 'Once pending bit clears. Enable the Dis line'
        g.LDIS_N_Disable()
        time.sleep(1)
        print 'Read status registers'
        checkAlarms()
        print 'Check optical output'
        print 'The Output power is:',it.oop()[1]
        print 'Send resena(1)'
        it.resena(1)
        print 'Read response of alarms after sending sena 1 while laser is disabled'
        checkAlarms()
        print 'Enable the laser by disabling the DIS line'
        g.LDIS_N_Enable()
        print 'Read status registers after the DIS is disabled'
        checkAlarms()

        print "Test4"    
        print 'Set channel to (-1) and read value'
        print it.channel(-1)
        print 'The output after channel is set to -1',it.channel()[1]
        it.disconnect()
        print 'channel Test Done...'
        it.disconnect()
       # except (TypeError):
            #raise 'Failed'
        

    def pwrTest(self):

        try:
            
            print '\n\n'    
            print '*' * 10,'PWR TEST','*' * 10
            it.connect(com_port,baud)
            it.setpassword()
            it.logging(True)
            print 'OPSH:',it.opsh()[1]
            pwr = it.opsh()[1] - 20
            it.pwr(pwr)
            for i in range(30):
                pwr = int(it.pwr()[1]) + 1
                stat=it.pwr(pwr)[0]
                print 'Input power:',pwr
                if stat == 'XE':
                    print stat,'Error at:',it.pwr()[1],'power level'
                    break
     
            print 'OPSL:',it.opsl()[1]
            pwr = it.opsl()[1] + 20
            it.pwr(pwr)
            for i in range(30):
                pwr = int(it.pwr()[1]) - 1
                stat=it.pwr(pwr)[0]
                print 'Input power:',pwr
                if stat == 'XE':
                    print stat,'Error at:',it.pwr()[1],'power level'
                    break
            it.disconnect()
            print 'pwr Test Done...'
        except:
            raise 'Failed...'


    def gridTest(self):
        try:
            
            print '\n\n'    
            print '*' * 10,'GRID TEST','*' * 10
            print 'Set Resena to 0'
            it.connect(3)
            it.setpassword()
            it.logging(True)
            it.resena(0)
            print 'Set Grid to 50Ghz Spacing'
            print it.grid(500)
            print it.grid()
            print 'Set Grid to 1Ghz Spacing'
            print it.grid(1)
            print it.grid()
            print 'Set Grid to Negative Number'
            print it.grid(-50)
            print it.grid()
            print 'Set Resena to 1'
            it.resena(1)
            print 'Set Grid to 50Ghz Spacing'
            print it.grid(500)
            print it.grid()
            print 'Set Grid to 1Ghz Spacing'
            print it.grid(1)
            print it.grid()
            print 'Set Grid to Negative Number'
            print it.grid(-50)
            print it.grid()
            print 'Grid Test Done...'
            it.disconnect()
        except:
            raise 'Failed...'


class TestFatalAlarms:
    """Series of sequences to validate the fatal alarms functionality"""
    def __init__(self):
        self.it = it
        self.t = t
        self.PORT = 1
        self.BAUD = 115200

    def checkFatalalarm(self):
##        print "===>TEST 1"
##        self.it.connect(self.PORT,self.BAUD)
##        self.it.logging(True)#turn on the logging
##        self.it.logfile("TestFatalAlarm1.txt")#set the mcb register
##        print "Turn on laser..."
##        self.it.mcb(sdf=0,adt=1)
##        self.it.resena(sena=1)#turn on the laser
##        monChannellock()#wiat to chanel lock#monitor until channel lock
##        f1_default = t.controlStage().filter1TemperatureController().target()
##        f2_default = t.controlStage().filter2TemperatureController().target()
##        print "Getting the default filter 1 and filter 2 values..."
##        print "F1:",f1_default,"======","F2:",f2_default
##        print "\n"
##        print"===> Clear Alarms..."
##        self.it.statusF(1,1,1,1,1,1,1,1)#clear the alarms fatal
##        self.it.statusW(1,1,1,1,1,1,1,1)#clear the alarms warning
##        time.sleep(.5)
##        print "Alarms after cleared","StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
##        print "\n"
##        offset = 0
##        print "Set the filters to trigger frequency fatal alarm 0.4 deviation from each other"
##        print "Getting the new filter 1 and filter 2 values..."
##        for i in range(1):#change the filter1 and filter 2 by .1 increments
##            offset += 0.5
##            t.controlStage().filter1TemperatureController().target(f1_default + offset)
##            t.controlStage().filter2TemperatureController().target(f2_default - offset)
##            f1 = t.controlStage().filter1TemperatureController().target()
##            f2 = t.controlStage().filter2TemperatureController().target()
##            sled = t.domainStage().frame().sledTemperature()
##            demodR = t.domainStage().frame().demodulationReal()
##            siB = t.domainStage().frame().siBlockTemperature()
##            pd = t.domainStage().frame().photodiodeCurrent()
##            gmi = t.domainStage().frame().gainMediumCurrent()
##            for i in range(100):
##                print "F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
##                if self.it.statusF() != '0L':
##                    "Fatal Alarms triggered"
##                else:
##                    "No Alarms..."
##
##        print "Test Complete"
##        it.resena(mr=1)
##        time.sleep(3)
##        
##        print "\n"
##        print "\n"
##        print "\n"
##        print "===>TEST 2"
##        self.it.connect(self.PORT,self.BAUD)
##        self.it.logging(True)#turn on the logging
##        self.it.logfile("TestFatalAlarm2.txt")#set the mcb register
##        print "Turn on laser..."
##        self.it.mcb(sdf=0,adt=1)
##        self.it.resena(sena=1)#turn on the laser
##        monChannellock()#wiat to chanel lock#monitor until channel lock
##        f1_default = t.controlStage().filter1TemperatureController().target()
##        f2_default = t.controlStage().filter2TemperatureController().target()
##        print "Getting the default filter 1 and filter 2 values..."
##        print "F1:",f1_default,"======","F2:",f2_default
##        print "\n"
##        print"===> Clear Alarms..."
##        self.it.statusF(1,1,1,1,1,1,1,1)#clear the alarms fatal
##        self.it.statusW(1,1,1,1,1,1,1,1)#clear the alarms warning
##        time.sleep(.5)
##        print "Alarms after cleared","StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
##        print "\n"
##        offset = 0
##        print "Set the filters to trigger frequency fatal alarm 1C deviation from each other"
##        print "Getting the new filter 1 and filter 2 values..."
##        for i in range(1):#change the filter1 and filter 2 by .1 increments
##            offset += 1.5
##            t.controlStage().filter1TemperatureController().target(f1_default + offset)
##            t.controlStage().filter2TemperatureController().target(f2_default + offset)
##            f1 = t.controlStage().filter1TemperatureController().target()
##            f2 = t.controlStage().filter2TemperatureController().target()
##            sled = t.domainStage().frame().sledTemperature()
##            demodR = t.domainStage().frame().demodulationReal()
##            siB = t.domainStage().frame().siBlockTemperature()
##            pd = t.domainStage().frame().photodiodeCurrent()
##            gmi = t.domainStage().frame().gainMediumCurrent()
##            for i in range(100):
##                print "F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
##                if self.it.statusF() != '0L':
##                    "Fatal Alarms triggered"
##                else:
##                    "No Alarms..."
##
##        print "Test Complete"
##        it.resena(mr=1)
##        time.sleep(3)
##        print "\n"
##        print "\n"
##        print "\n"
##        print "===>TEST 3"
##        self.it.connect(self.PORT,self.BAUD)
##        self.it.logging(True)#turn on the logging
##        self.it.logfile("TestFatalAlarm3.txt")#set the mcb register
##        print "Turn on laser..."
##        self.it.mcb(sdf=0,adt=1)
##        self.it.resena(sena=1)#turn on the laser
##        monChannellock()#wiat to chanel lock#monitor until channel lock
##        sbtc = t.controlStage().siBlockTemperatureController()
##        t.controlStage().siBlockSlot(sbtc)
##        siB_default = t.controlStage().siBlockTemperatureController().target()
##        print "Getting the default SiB values..."
##        print "SIB:",siB_default
##        print "\n"
##        print"===> Clear Alarms..."
##        self.it.statusF(1,1,1,1,1,1,1,1)#clear the alarms fatal
##        self.it.statusW(1,1,1,1,1,1,1,1)#clear the alarms warning
##        time.sleep(.5)
##        print "Alarms after cleared","StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
##        print "\n"
##        offset = 0
##        print "Set the Siblock to 90C to trigger Fatal Alarms"
##        print "Getting the SiBlock Value"
##        for i in range(1):#change the filter1 and filter 2 by .1 increments
##            target = 90
##            t.controlStage().siBlockTemperatureController().target(target)
##            siB_newTarget = t.controlStage().siBlockTemperatureController().target()
##            f1 = t.domainStage().frame().filter1Temperature()
##            f2 = t.domainStage().frame().filter2Temperature()
##            sled = t.domainStage().frame().sledTemperature()
##            demodR = t.domainStage().frame().demodulationReal()
##            siB = t.domainStage().frame().siBlockTemperature()
##            pd = t.domainStage().frame().photodiodeCurrent()
##            gmi = t.domainStage().frame().gainMediumCurrent()
##            for i in range(100):
##                print "F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
##                if self.it.statusF() != '0L':
##                    "Fatal Alarms triggered"
##                else:
##                    "No Alarms..."
##
##        print "Test Complete"
##        it.resena(mr=1)
##        time.sleep(3)
##        print "\n"
##        print "\n"
##        print "\n"
##        print "===>TEST 4"
##        self.it.connect(self.PORT,self.BAUD)
##        self.it.logging(True)#turn on the logging
##        self.it.logfile("TestFatalAlarm4.txt")#set the mcb register
##        print "Turn on laser..."
##        self.it.mcb(sdf=0,adt=1)
##        self.it.resena(sena=1)#turn on the laser
##        monChannellock()#wiat to chanel lock#monitor until channel lock
##        print"===> Clear Alarms..."
##        self.it.statusF(1,1,1,1,1,1,1,1)#clear the alarms fatal
##        self.it.statusW(1,1,1,1,1,1,1,1)#clear the alarms warning
##        time.sleep(1)
##        print "Alarms after cleared","StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
##        print "\n"
##        offset = 0
##        print "Set the output power to be < -10db to trigger fatal power alarm"
##        #print "Getting the SiBlock Value"
##        for i in range(1):#change the filter1 and filter 2 by .1 increments
##            target = 10
##            t.controlStage().mask().gainMediumCurrent(1)
##            t.controlStage().frame().gainMediumCurrent(target)
##            t.controlStage().frame().gainMediumCurrent(target)
##            t.controlStage().frame().gainMediumCurrent(target)
##            f1 = t.domainStage().frame().filter1Temperature()
##            f2 = t.domainStage().frame().filter2Temperature()
##            sled = t.domainStage().frame().sledTemperature()
##            demodR = t.domainStage().frame().demodulationReal()
##            siB = t.domainStage().frame().siBlockTemperature()
##            pd = t.domainStage().frame().photodiodeCurrent()
##            gmi = t.domainStage().frame().gainMediumCurrent()
##            for i in range(100):
##                print "F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
##                if self.it.statusF() != '0L':
##                    "Fatal Alarms triggered"
##                else:
##                    "No Alarms..."
##
##        print "Test Complete"
##        it.resena(mr=1)
##        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"
        print "===>TEST 5"
        self.it.connect(self.PORT,self.BAUD)
        self.it.logging(True)#turn on the logging
        self.it.logfile("TestFatalAlarm5.txt")#set the mcb register
        print "Turn on laser..."
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        f1_default = t.controlStage().filter1TemperatureController().target()
        f2_default = t.controlStage().filter2TemperatureController().target()
        print "Getting the default filter 1 and filter 2 values..."
        print "F1:",f1_default,"======","F2:",f2_default
        print "\n"
        print"===> Clear Alarms..."
        self.it.statusF(1,1,1,1,1,1,1,1)#clear the alarms fatal
        self.it.statusW(1,1,1,1,1,1,1,1)#clear the alarms warning
        time.sleep(.5)
        print "Alarms after cleared","StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
        print "\n"
        offset1 = 0
        offset2 = 0
        print "Set the filters to trigger thermal fatal alarm by -50 or 140C"
        print "Getting the new filter 1 and filter 2 values..."
        for i in range(1):#change the filter1 and filter 2 by .1 increments
            if i == 0:
                offset1 += 150
                offset2 += 0
                t.controlStage().filter1TemperatureController().target(f1_default + offset1)
                t.controlStage().filter2TemperatureController().target(f2_default + offset2)
                f1 = t.controlStage().filter1TemperatureController().target()
                f2 = t.controlStage().filter2TemperatureController().target()
                sled = t.domainStage().frame().sledTemperature()
                demodR = t.domainStage().frame().demodulationReal()
                siB = t.domainStage().frame().siBlockTemperature()
                pd = t.domainStage().frame().photodiodeCurrent()
                gmi = t.domainStage().frame().gainMediumCurrent()
                for i in range(100):
                    print "F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                    if self.it.statusF() != '0L':
                        "Fatal Alarms triggered"
                    else:
                        "No Alarms..."

                print "Test Complete"
                it.resena(mr=1)
            else:
                offset1 += 0
                offset2 += 150
                t.controlStage().filter1TemperatureController().target(f1_default + offset1)
                t.controlStage().filter2TemperatureController().target(f2_default + offset2)
                f1 = t.controlStage().filter1TemperatureController().target()
                f2 = t.controlStage().filter2TemperatureController().target()
                sled = t.domainStage().frame().sledTemperature()
                demodR = t.domainStage().frame().demodulationReal()
                siB = t.domainStage().frame().siBlockTemperature()
                pd = t.domainStage().frame().photodiodeCurrent()
                gmi = t.domainStage().frame().gainMediumCurrent()
                for i in range(100):
                    print "F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                    if self.it.statusF() != '0L':
                        "Fatal Alarms triggered"
                    else:
                        "No Alarms..."

            print "Test Complete"
            it.resena(mr=1)
        t.disconnect()




        print "\n"
        print "\n"
        print "\n"
        print "===>TEST 6"
        self.it.connect(self.PORT,self.BAUD)
        self.it.logging(True)#turn on the logging
        self.it.logfile("TestWarningAlarm_TriggerSled.txt")#set the mcb register
        print "Turn on laser..."
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        f1_default = t.controlStage().filter1TemperatureController().target()
        f2_default = t.controlStage().filter2TemperatureController().target()
        print "Getting the default filter 1 and filter 2 values..."
        print "F1:",f1_default,"======","F2:",f2_default
        print "\n"
        print"===> Clear Alarms..."
        self.it.statusF(1,1,1,1,1,1,1,1)#clear the alarms fatal
        self.it.statusW(1,1,1,1,1,1,1,1)#clear the alarms warning
        time.sleep(.5)
        print "Alarms after cleared","StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
        print "\n"
        offset1 = 0
        offset2 = 0
        print "Set the filters to trigger thermal fatal alarm by -50 or 140C"
        print "Getting the new filter 1 and filter 2 values..."
        for i in range(1):#change the filter1 and filter 2 by .1 increments
            if i == 0:
                offset1 += 150
                offset2 += 0
                t.controlStage().filter1TemperatureController().target(f1_default + offset1)
                t.controlStage().filter2TemperatureController().target(f2_default + offset2)
                f1 = t.controlStage().filter1TemperatureController().target()
                f2 = t.controlStage().filter2TemperatureController().target()
                sled = t.domainStage().frame().sledTemperature()
                demodR = t.domainStage().frame().demodulationReal()
                siB = t.domainStage().frame().siBlockTemperature()
                pd = t.domainStage().frame().photodiodeCurrent()
                gmi = t.domainStage().frame().gainMediumCurrent()
                for i in range(100):
                    print "F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                    if self.it.statusF() != '0L':
                        "Fatal Alarms triggered"
                    else:
                        "No Alarms..."

                print "Test Complete"
                it.resena(mr=1)
            
            
            
    



    
TestFatalAlarms = TestFatalAlarms()      


if __name__== '__main__':
    
##    try:
##        SanityCheck().channelTest()
##    except:
##        raise
##        
##    try:
##        SanityCheck().pwrTest()
##    except:
##        raise
##        
##    try:
##        SanityCheck().nopTest()
##    except:
##        raise
##        
##    try:
##        SanityCheck().laserDisabletest(g)
##    except:
##        raise
##    
##    try:
##        SanityCheck().moduleSelecttest(g)
##    except:
##        raise
##        
##    try:
##        SanityCheck().hardResettest(g)
##    except:
##        raise
##        
##    try:
##        SanityCheck().mainResettest()
##    except:
##        raise
##        
##    try:
##        SanityCheck().softResettest()
##    except:
##        raise
##        
##    try:
##        SanityCheck().adtTest()
##    except:
##        SanityCheck().genConfigtest()
##    
##    try:
##        SanityCheck().resenaTest()
##    except:
##        raise
##        
##    try:
##        SanityCheck().fPowthTest()
##    except:
##        raise
##        
##    try:
##        SanityCheck().wPowThTest()
##    except:
##        raise
##        
##    try:
##        SanityCheck().freqandThermalthresholdTest()
##    except:
##        raise
##        
##    try:
##        SanityCheck().srqTest()
##    except:
##        raise
##        
##    try:
##        SanityCheck().fatalTTest()
##    except:
##        raise
##        
##    try:
##        SanityCheck().almTTest()
##        
##    except:
##        raise
##        
##    try:
##        SanityCheck().gridTest()
##    except:
##        raise

    try:
        TestFatalAlarms.checkFatalalarm()

    except:
        raise








     



    






    


