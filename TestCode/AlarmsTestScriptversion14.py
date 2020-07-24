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
time.sleep(3)

sys.path.append(os.path.abspath('.'))

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



####################################################################################################
#############################   MAIN PROGRAM  ######################################################
####################################################################################################



class TestFatalAlarms:
    """Series of sequences to validate the fatal alarms functionality"""
    def __init__(self):
        self.it = it
        self.t = t
        self.PORT = 3
        self.BAUD = 115200

    def checkFrequencyalarms(self):
        print "===>TEST 1A"
        self.it.connect(self.PORT,self.BAUD)
        self.it.logging(True)#turn on the logging
        self.it.logfile("F1F2Dev1C.txt")
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
        offset = 0
        print "Set the filters to trigger frequency fatal alarm 1C deviation from each other"
        print "Getting the new filter 1 and filter 2 values..."
        for i in range(1):
            offset += 1.5
            t.controlStage().filter1TemperatureController().target(f1_default + offset)
            t.controlStage().filter2TemperatureController().target(f2_default + offset)
            f1 = t.domainStage().frame().filter1Temperature()
            f2 = t.domainStage().frame().filter2Temperature()
            sled = t.domainStage().frame().sledTemperature()
            demodR = t.domainStage().frame().demodulationReal()
            siB = t.domainStage().frame().siBlockTemperature()
            pd = t.domainStage().frame().photodiodeCurrent()
            gmi = t.domainStage().frame().gainMediumCurrent()
            startT = time.time()
            lapseT = time.time()-startT
            for i in range(100):
                print "Time:",lapseT,"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                f1 = t.domainStage().frame().filter1Temperature()
                f2 = t.domainStage().frame().filter2Temperature()
                sled = t.domainStage().frame().sledTemperature()
                demodR = t.domainStage().frame().demodulationReal()
                siB = t.domainStage().frame().siBlockTemperature()
                pd = t.domainStage().frame().photodiodeCurrent()
                gmi = t.domainStage().frame().gainMediumCurrent()
                lapseT = time.time()-startT 
        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)

##
        print "===>TEST 1B"
        self.it.connect(self.PORT,self.BAUD)
        self.it.logging(True)#turn on the logging
        self.it.logfile("F1F2Dev-1C.txt")#set the mcb register
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
        offset = 0
        print "Set the filters to trigger frequency fatal alarm -1C deviation from each other"
        print "Getting the new filter 1 and filter 2 values..."
        for i in range(1):
            offset += 1.5
            t.controlStage().filter1TemperatureController().target(f1_default - offset)
            t.controlStage().filter2TemperatureController().target(f2_default - offset)
            f1 = t.domainStage().frame().filter1Temperature()
            f2 = t.domainStage().frame().filter2Temperature()
            sled = t.domainStage().frame().sledTemperature()
            demodR = t.domainStage().frame().demodulationReal()
            siB = t.domainStage().frame().siBlockTemperature()
            pd = t.domainStage().frame().photodiodeCurrent()
            gmi = t.domainStage().frame().gainMediumCurrent()
            startT = time.time()
            lapseT = time.time()-startT
            for i in range(100):
                print "Time:",lapseT,"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                f1 = t.domainStage().frame().filter1Temperature()
                f2 = t.domainStage().frame().filter2Temperature()
                sled = t.domainStage().frame().sledTemperature()
                demodR = t.domainStage().frame().demodulationReal()
                siB = t.domainStage().frame().siBlockTemperature()
                pd = t.domainStage().frame().photodiodeCurrent()
                gmi = t.domainStage().frame().gainMediumCurrent()
                lapseT = time.time()-startT 
        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
##
##
##
        print "===>TEST 2A"
        self.it.connect(self.PORT,self.BAUD)
        self.it.logging(True)#turn on the logging
        self.it.logfile("F1F2Dev_0.5C_fromeachother.txt")#set the mcb register
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
        offset = 0
        print "Set the filters to trigger frequency fatal alarm 0.5C deviation from each other"
        print "Getting the new filter 1 and filter 2 values..."
        for i in range(1):
            offset += 0.25
            t.controlStage().filter1TemperatureController().target(f1_default + offset)
            t.controlStage().filter2TemperatureController().target(f2_default - offset)
            f1 = t.domainStage().frame().filter1Temperature()
            f2 = t.domainStage().frame().filter2Temperature()
            sled = t.domainStage().frame().sledTemperature()
            demodR = t.domainStage().frame().demodulationReal()
            siB = t.domainStage().frame().siBlockTemperature()
            pd = t.domainStage().frame().photodiodeCurrent()
            gmi = t.domainStage().frame().gainMediumCurrent()
            startT = time.time()
            lapseT = time.time()-startT
            for i in range(100):
                print "Time:",lapseT,"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                f1 = t.domainStage().frame().filter1Temperature()
                f2 = t.domainStage().frame().filter2Temperature()
                sled = t.domainStage().frame().sledTemperature()
                demodR = t.domainStage().frame().demodulationReal()
                siB = t.domainStage().frame().siBlockTemperature()
                pd = t.domainStage().frame().photodiodeCurrent()
                gmi = t.domainStage().frame().gainMediumCurrent()
                lapseT = time.time()-startT 
        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)




        print "===>TEST 2B"
        self.it.connect(self.PORT,self.BAUD)
        self.it.logging(True)#turn on the logging
        self.it.logfile("F1F2Dev_-0.5C_fromeachother.txt")#set the mcb register
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
        offset = 0
        print "Set the filters to trigger frequency fatal alarm -0.5C deviation from each other"
        print "Getting the new filter 1 and filter 2 values..."
        for i in range(1):
            offset += 0.25
            t.controlStage().filter1TemperatureController().target(f1_default - offset)
            t.controlStage().filter2TemperatureController().target(f2_default + offset)
            f1 = t.domainStage().frame().filter1Temperature()
            f2 = t.domainStage().frame().filter2Temperature()
            sled = t.domainStage().frame().sledTemperature()
            demodR = t.domainStage().frame().demodulationReal()
            siB = t.domainStage().frame().siBlockTemperature()
            pd = t.domainStage().frame().photodiodeCurrent()
            gmi = t.domainStage().frame().gainMediumCurrent()
            startT = time.time()
            lapseT = time.time()-startT
            for i in range(100):
                print "Time:",lapseT,"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                f1 = t.domainStage().frame().filter1Temperature()
                f2 = t.domainStage().frame().filter2Temperature()
                sled = t.domainStage().frame().sledTemperature()
                demodR = t.domainStage().frame().demodulationReal()
                siB = t.domainStage().frame().siBlockTemperature()
                pd = t.domainStage().frame().photodiodeCurrent()
                gmi = t.domainStage().frame().gainMediumCurrent()
                lapseT = time.time()-startT 
        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)


        print "\n"
        print "\n"
        print "\n"
        print "===>TEST 3"
        self.it.connect(self.PORT,self.BAUD)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SiblockSetto81C.txt")#set the mcb register
        print "Turn on laser..."
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        sbtc = t.controlStage().siBlockTemperatureController()
        t.controlStage().siBlockSlot(sbtc)
        siB_default = t.controlStage().siBlockTemperatureController().target()
        print "Getting the default SiB values..."
        print "SIB:",siB_default
        print "\n"
        print"===> Clear Alarms..."
        self.it.statusF(1,1,1,1,1,1,1,1)#clear the alarms fatal
        self.it.statusW(1,1,1,1,1,1,1,1)#clear the alarms warning
        time.sleep(.5)
        print "Alarms after cleared","StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
        print "\n"
        offset = 0
        print "Set the Siblock to 81C to trigger Fatal Alarms"
        print "Getting the SiBlock Value"
        for i in range(1):
            target = 81
            t.controlStage().siBlockTemperatureController().target(target)
            siB_newTarget = t.controlStage().siBlockTemperatureController().target()
            f1 = t.domainStage().frame().filter1Temperature()
            f2 = t.domainStage().frame().filter2Temperature()
            sled = t.domainStage().frame().sledTemperature()
            demodR = t.domainStage().frame().demodulationReal()
            siB = t.domainStage().frame().siBlockTemperature()
            pd = t.domainStage().frame().photodiodeCurrent()
            gmi = t.domainStage().frame().gainMediumCurrent()
            startT = time.time()
            lapseT = time.time()-startT
            for i in range(100):
                print "Time:",lapseT,"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                f1 = t.domainStage().frame().filter1Temperature()
                f2 = t.domainStage().frame().filter2Temperature()
                sled = t.domainStage().frame().sledTemperature()
                demodR = t.domainStage().frame().demodulationReal()
                siB = t.domainStage().frame().siBlockTemperature()
                pd = t.domainStage().frame().photodiodeCurrent()
                gmi = t.domainStage().frame().gainMediumCurrent()
                lapseT = time.time()-startT 

        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"





        print "\n"
        print "\n"
        print "\n"
        print "===>TEST 4"
        self.it.connect(self.PORT,self.BAUD)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SetSledT_+4C.txt")
        print "Turn on laser..."
        self.it.mcb(sdf=0,adt=1) #set the mcb register
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        sledDefault = t.controlStage().sledTemperatureController().target()
        print "Getting the default sled values..."
        print "Sled==>",sledDefault
        print "\n"
        print"===> Clear Alarms..."
        self.it.statusF(1,1,1,1,1,1,1,1)#clear the alarms fatal
        self.it.statusW(1,1,1,1,1,1,1,1)#clear the alarms warning
        time.sleep(1)
        print "Alarms after cleared","StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
        print "\n"
        offset = 0
        print "Increase the sled temperature by +4C to trigger frequency warning alarm"
        for i in range(1):#change the filter1 and filter 2 by .1 increments
            target = 54
            t.controlStage().sledTemperatureController().target(target)
            sled_newTarget = t.controlStage().sledTemperatureController().target()
            print "new target:",sled_newTarget
            f1 = t.domainStage().frame().filter1Temperature()
            f2 = t.domainStage().frame().filter2Temperature()
            sled = t.domainStage().frame().sledTemperature()
            demodR = t.domainStage().frame().demodulationReal()
            siB = t.domainStage().frame().siBlockTemperature()
            pd = t.domainStage().frame().photodiodeCurrent()
            gmi = t.domainStage().frame().gainMediumCurrent()
            startT = time.time()
            lapseT = time.time()-startT
            for i in range(100):
                f1 = t.domainStage().frame().filter1Temperature()
                f2 = t.domainStage().frame().filter2Temperature()
                sled = t.domainStage().frame().sledTemperature()
                demodR = t.domainStage().frame().demodulationReal()
                siB = t.domainStage().frame().siBlockTemperature()
                pd = t.domainStage().frame().photodiodeCurrent()
                gmi = t.domainStage().frame().gainMediumCurrent()
                print "Time:",lapseT,"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                lapseT = time.time()-startT 

        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"




        print "\n"
        print "\n"
        print "\n"
        print "===>TEST 5"
        self.it.connect(self.PORT,self.BAUD)
        self.it.logging(True)#turn on the logging
        self.it.logfile("MonitorDemor0.2WarningAlarm.txt")#set the mcb register
        print "Turn on laser..."
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        print"===> Clear Alarms..."
        self.it.statusF(1,1,1,1,1,1,1,1)#clear the alarms fatal
        self.it.statusW(1,1,1,1,1,1,1,1)#clear the alarms warning
        print "Alarms after cleared","StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
        startT = time.time()
        lapseT = time.time() - startT
        while lapseT <= 20.0:
            f1 = t.domainStage().frame().filter1Temperature()
            f2 = t.domainStage().frame().filter2Temperature()
            sled = t.domainStage().frame().sledTemperature()
            demodR = t.domainStage().frame().demodulationReal()
            siB = t.domainStage().frame().siBlockTemperature()
            pd = t.domainStage().frame().photodiodeCurrent()
            gmi = t.domainStage().frame().gainMediumCurrent()
            print "Time:",lapseT,"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
            lapseT = time.time()-startT 

        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"





        print "\n"
        print "\n"
        print "\n"
        print "===>TEST 6"
        self.it.connect(self.PORT,self.BAUD)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SetSledT_+5C_triggerwarningpweralarm.txt")#set the mcb register
        print "Turn on laser..."
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        sledDefault = t.controlStage().sledTemperatureController().target()
        sbc = t.controlStage().siBlockTemperatureController()
        t.controlStage().siBlockSlot(sbc)
        print "Getting the default sled values..."
        print "Sled==>",sledDefault
        print "\n"
        print"===> Clear Alarms..."
        self.it.statusF(1,1,1,1,1,1,1,1)#clear the alarms fatal
        self.it.statusW(1,1,1,1,1,1,1,1)#clear the alarms warning
        time.sleep(1)
        print "Alarms after cleared","StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
        print "\n"
        offset = 0
        print "Increase the sled temperature by +5C to trigger power warning alarm"
        for i in range(1):#change the filter1 and filter 2 by .1 increments
            target = 56
            t.controlStage().sledTemperatureController().target(target)
            sled_newTarget = t.controlStage().sledTemperatureController().target()
            t.controlStage().siBlockTemperatureController().target(50)
            print "new target:",sled_newTarget
            f1 = t.domainStage().frame().filter1Temperature()
            f2 = t.domainStage().frame().filter2Temperature()
            sled = t.domainStage().frame().sledTemperature()
            demodR = t.domainStage().frame().demodulationReal()
            siB = t.domainStage().frame().siBlockTemperature()
            pd = t.domainStage().frame().photodiodeCurrent()
            gmi = t.domainStage().frame().gainMediumCurrent()
            startT = time.time()
            lapseT = time.time()-startT
            for i in range(100):
                f1 = t.domainStage().frame().filter1Temperature()
                f2 = t.domainStage().frame().filter2Temperature()
                sled = t.domainStage().frame().sledTemperature()
                demodR = t.domainStage().frame().demodulationReal()
                siB = t.domainStage().frame().siBlockTemperature()
                pd = t.domainStage().frame().photodiodeCurrent()
                gmi = t.domainStage().frame().gainMediumCurrent()
                print "Time:",lapseT,"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                lapseT = time.time()-startT 

        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"




        print "\n"
        print "\n"
        print "\n"
        print "===>TEST 7"
        self.it.connect(self.PORT,self.BAUD)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SetSiblock_lowerthan_sledtemp_triggerfatalpoweralarm.txt")#set the mcb register
        print "Turn on laser..."
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        sledDefault = t.controlStage().sledTemperatureController().target()
        sbc = t.controlStage().siBlockTemperatureController()
        t.controlStage().siBlockSlot(sbc)
        print "Getting the default sled values..."
        print "Sled==>",sledDefault
        print "\n"
        print"===> Clear Alarms..."
        self.it.statusF(1,1,1,1,1,1,1,1)#clear the alarms fatal
        self.it.statusW(1,1,1,1,1,1,1,1)#clear the alarms warning
        time.sleep(1)
        print "Alarms after cleared","StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
        print "\n"
        offset = 0
        print "Increase the sled temperature by +5C to trigger power warning alarm"
        for i in range(1):#change the filter1 and filter 2 by .1 increments
            target = 51
            t.controlStage().sledTemperatureController().target(target)
            sled_newTarget = t.controlStage().sledTemperatureController().target()
            t.controlStage().siBlockTemperatureController().target(50)
            print "new target:",sled_newTarget
            f1 = t.domainStage().frame().filter1Temperature()
            f2 = t.domainStage().frame().filter2Temperature()
            sled = t.domainStage().frame().sledTemperature()
            demodR = t.domainStage().frame().demodulationReal()
            siB = t.domainStage().frame().siBlockTemperature()
            pd = t.domainStage().frame().photodiodeCurrent()
            gmi = t.domainStage().frame().gainMediumCurrent()
            startT = time.time()
            lapseT = time.time()-startT
            for i in range(100):
                f1 = t.domainStage().frame().filter1Temperature()
                f2 = t.domainStage().frame().filter2Temperature()
                sled = t.domainStage().frame().sledTemperature()
                demodR = t.domainStage().frame().demodulationReal()
                siB = t.domainStage().frame().siBlockTemperature()
                pd = t.domainStage().frame().photodiodeCurrent()
                gmi = t.domainStage().frame().gainMediumCurrent()
                print "Time:",lapseT,"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                lapseT = time.time()-startT 

        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"




        print "===>TEST8 "
        self.it.connect(self.PORT,self.BAUD)
        self.it.logging(True)#turn on the logging
        self.it.logfile("Setgmito10mAtodroppowerto10dBlessthantarget.txt")#set the mcb register
        print "Turn on laser..."
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        print"===> Clear Alarms..."
        self.it.statusF(1,1,1,1,1,1,1,1)#clear the alarms fatal
        self.it.statusW(1,1,1,1,1,1,1,1)#clear the alarms warning
        time.sleep(1)
        print "Alarms after cleared","StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
        print "\n"
        offset = 0
        print "Set the output power to be < -10db to trigger fatal power alarm"
        #print "Getting the SiBlock Value"
        for i in range(1):#change the filter1 and filter 2 by .1 increments
            target = 10
            t.controlStage().mask().gainMediumCurrent(1)
            t.controlStage().frame().gainMediumCurrent(target)
            t.controlStage().frame().gainMediumCurrent(target)
            t.controlStage().frame().gainMediumCurrent(target)
            f1 = t.domainStage().frame().filter1Temperature()
            f2 = t.domainStage().frame().filter2Temperature()
            sled = t.domainStage().frame().sledTemperature()
            demodR = t.domainStage().frame().demodulationReal()
            siB = t.domainStage().frame().siBlockTemperature()
            pd = t.domainStage().frame().photodiodeCurrent()
            gmi = t.domainStage().frame().gainMediumCurrent()
            startT = time.time()
            lapseT = time.time()-startT
            for i in range(100):
                print "Time:",lapseT,"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                f1 = t.domainStage().frame().filter1Temperature()
                f2 = t.domainStage().frame().filter2Temperature()
                sled = t.domainStage().frame().sledTemperature()
                demodR = t.domainStage().frame().demodulationReal()
                siB = t.domainStage().frame().siBlockTemperature()
                pd = t.domainStage().frame().photodiodeCurrent()
                gmi = t.domainStage().frame().gainMediumCurrent()
                lapseT = time.time()-startT 

        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"


        print "===>TEST 9"
        self.it.connect(self.PORT,self.BAUD)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SiblockSetto81CtotriggerPowerfatalAlarm.txt")#set the mcb register
        print "Turn on laser..."
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        sbtc = t.controlStage().siBlockTemperatureController()
        t.controlStage().siBlockSlot(sbtc)
        siB_default = t.controlStage().siBlockTemperatureController().target()
        print "Getting the default SiB values..."
        print "SIB:",siB_default
        print "\n"
        print"===> Clear Alarms..."
        self.it.statusF(1,1,1,1,1,1,1,1)#clear the alarms fatal
        self.it.statusW(1,1,1,1,1,1,1,1)#clear the alarms warning
        time.sleep(.5)
        print "Alarms after cleared","StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
        print "\n"
        offset = 0
        print "Set the Siblock to 81C to trigger Fatal Power Alarms"
        print "Getting the SiBlock Value"
        for i in range(1):#change the filter1 and filter 2 by .1 increments
            target = 81
            t.controlStage().siBlockTemperatureController().target(target)
            siB_newTarget = t.controlStage().siBlockTemperatureController().target()
            f1 = t.domainStage().frame().filter1Temperature()
            f2 = t.domainStage().frame().filter2Temperature()
            sled = t.domainStage().frame().sledTemperature()
            demodR = t.domainStage().frame().demodulationReal()
            siB = t.domainStage().frame().siBlockTemperature()
            pd = t.domainStage().frame().photodiodeCurrent()
            gmi = t.domainStage().frame().gainMediumCurrent()
            startT = time.time()
            lapseT = time.time()-startT
            for i in range(100):
                print "Time:",lapseT,"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                f1 = t.domainStage().frame().filter1Temperature()
                f2 = t.domainStage().frame().filter2Temperature()
                sled = t.domainStage().frame().sledTemperature()
                demodR = t.domainStage().frame().demodulationReal()
                siB = t.domainStage().frame().siBlockTemperature()
                pd = t.domainStage().frame().photodiodeCurrent()
                gmi = t.domainStage().frame().gainMediumCurrent()
                lapseT = time.time()-startT 

        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"



        print "===>TEST 10"

        for i in range(2):#change the filter1 and filter 2 by .1 increments

            if i == 0:
                self.it.connect(self.PORT,self.BAUD)
                self.it.logging(True)#turn on the logging
                self.it.logfile("SetFilter1Tempto140CToTrigger.txt")#set the mcb register
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
                offset1 = 0
                offset2 = 0
                print "Alarms after cleared","StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                print "\n"
                print "Set the filters to trigger thermal fatal alarm by -50 or 140C"
                print "Getting the new filter 1 and filter 2 values..."
                offset1 += 150
                offset2 += 0
                t.controlStage().filter1TemperatureController().target(f1_default + offset1)
                t.controlStage().filter2TemperatureController().target(f2_default + offset2)
                f1 = t.domainStage().frame().filter1Temperature()
                f2 = t.domainStage().frame().filter2Temperature()
                sled = t.domainStage().frame().sledTemperature()
                demodR = t.domainStage().frame().demodulationReal()
                siB = t.domainStage().frame().siBlockTemperature()
                pd = t.domainStage().frame().photodiodeCurrent()
                gmi = t.domainStage().frame().gainMediumCurrent()
                startT = time.time()
                lapseT = time.time()-startT
                for i in range(100):
                    print "Time:",lapseT,"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                    f1 = t.domainStage().frame().filter1Temperature()
                    f2 = t.domainStage().frame().filter2Temperature()
                    sled = t.domainStage().frame().sledTemperature()
                    demodR = t.domainStage().frame().demodulationReal()
                    siB = t.domainStage().frame().siBlockTemperature()
                    pd = t.domainStage().frame().photodiodeCurrent()
                    gmi = t.domainStage().frame().gainMediumCurrent()
                    lapseT = time.time()-startT 


                print "Test Complete"
                it.resena(mr=1)
                
            elif i == 1:
                time.sleep(3)
                self.it.connect(self.PORT,self.BAUD)
                self.it.logging(True)#turn on the logging
                self.it.logfile("SetFilter2Tempto140CToTrigger.txt")#set the mcb register
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
                offset1 = 0
                offset2 = 0
                print "Alarms after cleared","StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                print "\n"
                print "Set the filters to trigger thermal fatal alarm by -50 or 140C"
                print "Getting the new filter 1 and filter 2 values..."
                offset1 += 0
                offset2 += 150
                t.controlStage().filter1TemperatureController().target(f1_default + offset1)
                t.controlStage().filter2TemperatureController().target(f2_default + offset2)
                f1 = t.domainStage().frame().filter1Temperature()
                f2 = t.domainStage().frame().filter2Temperature()
                sled = t.domainStage().frame().sledTemperature()
                demodR = t.domainStage().frame().demodulationReal()
                siB = t.domainStage().frame().siBlockTemperature()
                pd = t.domainStage().frame().photodiodeCurrent()
                gmi = t.domainStage().frame().gainMediumCurrent()
                startT = time.time()
                lapseT = time.time()-startT
                for i in range(100):
                    print "Time:",lapseT,"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                    f1 = t.domainStage().frame().filter1Temperature()
                    f2 = t.domainStage().frame().filter2Temperature()
                    sled = t.domainStage().frame().sledTemperature()
                    demodR = t.domainStage().frame().demodulationReal()
                    siB = t.domainStage().frame().siBlockTemperature()
                    pd = t.domainStage().frame().photodiodeCurrent()
                    gmi = t.domainStage().frame().gainMediumCurrent()
                    lapseT = time.time()-startT 


                print "Test Complete"
                it.resena(mr=1)
        t.disconnect()
        print "\n"
        print "\n"
        print "\n"



        print "\n"
        print "\n"
        print "\n"
        print "===>TEST11 "
        self.it.connect(self.PORT,self.BAUD)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SetSledT_to100C_triggerThermalFatalAlarm.txt")#set the mcb register
        print "Turn on laser..."
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        sledDefault = t.controlStage().sledTemperatureController().target()
        print "Getting the default sled values..."
        print "Sled==>",sledDefault
        print "\n"
        print"===> Clear Alarms..."
        self.it.statusF(1,1,1,1,1,1,1,1)#clear the alarms fatal
        self.it.statusW(1,1,1,1,1,1,1,1)#clear the alarms warning
        time.sleep(1)
        print "Alarms after cleared","StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
        print "\n"
        offset = 0
        print "Increase the sled temperature by +100C to trigger thermal fatal alarm"
        for i in range(1):#change the filter1 and filter 2 by .1 increments
            target = 100
            t.controlStage().sledTemperatureController().target(target)
            sled_newTarget = t.controlStage().sledTemperatureController().target()
            print "new target:",sled_newTarget
            f1 = t.domainStage().frame().filter1Temperature()
            f2 = t.domainStage().frame().filter2Temperature()
            sled = t.domainStage().frame().sledTemperature()
            demodR = t.domainStage().frame().demodulationReal()
            siB = t.domainStage().frame().siBlockTemperature()
            pd = t.domainStage().frame().photodiodeCurrent()
            gmi = t.domainStage().frame().gainMediumCurrent()
            startT = time.time()
            lapseT = time.time()-startT
            for i in range(100):
                f1 = t.domainStage().frame().filter1Temperature()
                f2 = t.domainStage().frame().filter2Temperature()
                sled = t.domainStage().frame().sledTemperature()
                demodR = t.domainStage().frame().demodulationReal()
                siB = t.domainStage().frame().siBlockTemperature()
                pd = t.domainStage().frame().photodiodeCurrent()
                gmi = t.domainStage().frame().gainMediumCurrent()
                print "Time:",lapseT,"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
                lapseT = time.time()-startT 

        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"            



class TestSrqTriggers:

    def __init__(self):
        #self.it = it_obj
        #self.t = t
        self.PORT = 3
        self.BAUD = 115200
        #self.g = g_obj

    def monitorParameters(self):
        f1 = t.domainStage().frame().filter1Temperature() #check the staus of alarms
        f2 = t.domainStage().frame().filter2Temperature()
        sled = t.domainStage().frame().sledTemperature()
        demodR = t.domainStage().frame().demodulationReal()
        siB = t.domainStage().frame().siBlockTemperature()
        pd = t.domainStage().frame().photodiodeCurrent()
        gmi = t.domainStage().frame().gainMediumCurrent()
        print "Time:",time.asctime(),"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
        
    def runSrqtTest(self,it,g):
        """"""
        self.it = it
        self.g = g
        #tune to channel
        #set srqT True in DIS and false for everything else
        #triger Dis
        #check statusF and StatusW

        print "\n"
        print "\n"
        print "\n"
        print "===>TEST1 "
        print "===>SRQT_DIS_Bit_Enabled "
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SRQT_DIS_Bit.txt")#set the mcb register
        print "Turn on laser..."
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        self.it.srqT(1,0,0,0,0,0,0,0,0,0,0,0,0) #enable dis turn off everything
        print it.srqT()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #Clear alarms
        self.g.LDIS_N_Disable() #disable the laser
        time.sleep(1)
        f1 = t.domainStage().frame().filter1Temperature() #check the staus of alarms
        f2 = t.domainStage().frame().filter2Temperature()
        sled = t.domainStage().frame().sledTemperature()
        demodR = t.domainStage().frame().demodulationReal()
        siB = t.domainStage().frame().siBlockTemperature()
        pd = t.domainStage().frame().photodiodeCurrent()
        gmi = t.domainStage().frame().gainMediumCurrent()
        print "==>> Show the alarm status after laser disabled"
        print "Time:",time.asctime(),"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
        self.g.LDIS_N_Enable() #deassert the LDIS
        time.sleep(1)
        f1 = t.domainStage().frame().filter1Temperature() #check the staus of alarms
        f2 = t.domainStage().frame().filter2Temperature()
        sled = t.domainStage().frame().sledTemperature()
        demodR = t.domainStage().frame().demodulationReal()
        siB = t.domainStage().frame().siBlockTemperature()
        pd = t.domainStage().frame().photodiodeCurrent()
        gmi = t.domainStage().frame().gainMediumCurrent()
        print "==>> Show the alarm status after laser enabled"
        print "Time:",time.asctime(),"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())


        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.srqT(0,0,0,0,0,0,0,0,0,0,0,0,0) #disble dis bit turn off everything
        print it.srqT()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #Clear alarms
        self.g.LDIS_N_Disable() #disable the laser
        time.sleep(1)
        f1 = t.domainStage().frame().filter1Temperature() #check the staus of alarms
        f2 = t.domainStage().frame().filter2Temperature()
        sled = t.domainStage().frame().sledTemperature()
        demodR = t.domainStage().frame().demodulationReal()
        siB = t.domainStage().frame().siBlockTemperature()
        pd = t.domainStage().frame().photodiodeCurrent()
        gmi = t.domainStage().frame().gainMediumCurrent()
        print "==>> Show the alarm status after laser disabled"
        print "Time:",time.asctime(),"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
        self.g.LDIS_N_Enable() #deassert the LDIS
        time.sleep(1)
        f1 = t.domainStage().frame().filter1Temperature() #check the staus of alarms
        f2 = t.domainStage().frame().filter2Temperature()
        sled = t.domainStage().frame().sledTemperature()
        demodR = t.domainStage().frame().demodulationReal()
        siB = t.domainStage().frame().siBlockTemperature()
        pd = t.domainStage().frame().photodiodeCurrent()
        gmi = t.domainStage().frame().gainMediumCurrent()
        print "==>> Show the alarm status after laser enabled"
        print "Time:",time.asctime(),"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"            





        print "===>TEST2 "
        print "===>SRQT_WFreql_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SRQT_WFreql_Bit_Enabled.txt")#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        self.it.srqT(0,0,1,0,0,0,0,0,0,0,0,0,0) #enable dis turn off everything
        print it.srqT()
        self.it.statusF()
        self.it.statusW() #Do not clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after laser is tuned while the wfreql is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.srqT(0,0,0,0,0,0,0,0,0,0,0,0,0) #enable dis turn off everything
        print it.srqT()
        self.it.statusF()
        self.it.statusW() #Do not clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after laser is tuned while the wfreql is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"



        print "===>TEST3 "
        print "===>SRQT_Wtherml_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SRQT_Wtherml_Bit_Enabled.txt")#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        self.it.srqT(0,0,0,1,0,0,0,0,0,0,0,0,0) #enable dis turn off everything
        print it.srqT()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        t.controlStage().sledTemperatureController().target(80) #ramp sled to 80C
        time.sleep(1)
        print "==>> Show the alarm status after laser is tuned while the wtherml is on"
        self.monitorParameters()
        t.controlStage().sledTemperatureController().target(50) #set sled back to 50C
        time.sleep(2)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.srqT(0,0,0,0,0,0,0,0,0,0,0,0,0) #enable dis turn off everything
        print it.srqT()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        t.controlStage().sledTemperatureController().target(80)#ramp sled to 80C
        time.sleep(1)
        print "==>> Show the alarm status after laser is tuned while the wtherml is on"
        self.monitorParameters()
        t.controlStage().sledTemperatureController().target(50)#set sled back to 50C
        time.sleep(2)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"


        print "===>TEST4 "
        print "===>SRQT_WPowl_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SRQT_WPowl_Bit_Enabled.txt")#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        self.it.srqT(0,0,0,0,1,0,0,0,0,0,0,0,0) #enable dis turn off everything
        print it.srqT()
        self.it.statusF()
        self.it.statusW() #Do not clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after laser is tuned while the wpowl is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.srqT(0,0,0,0,0,0,0,0,0,0,0,0,0) #enable dis turn off everything
        print it.srqT()
        self.it.statusF()
        self.it.statusW() #Do not clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after laser is tuned while the wpowl is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"



        print "===>TEST5 "
        print "===>SRQT_Xel_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SRQT_Xel_Bit_Enabled.txt")#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        self.it.srqT(0,0,0,0,0,1,0,0,0,0,0,0,0) #enable dis turn off everything
        print it.srqT()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        it.channel(-1)#trigger xel
        time.sleep(1)
        print "==>> Show the alarm status after laser is tuned while the xel is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.srqT(0,0,0,0,0,0,0,0,0,0,0,0,0) #enable dis turn off everything
        print it.srqT()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        it.channel(-1)#trigger xel
        time.sleep(1)
        print "==>> Show the alarm status after laser is tuned while the xel is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"



        print "===>TEST6 "
        print "===>SRQT_Mrl_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SRQT_Mrl_Bit_Enabled.txt")#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        self.it.srqT(0,0,0,0,0,0,0,1,0,0,0,0,0) #enable mrl turn off everything
        print it.srqT()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        it.resena(mr=1)#trigger main reset
        time.sleep(3)
        print "==>> Show the alarm status after laser is tuned while the mrl is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.srqT(0,0,0,0,0,0,0,0,0,0,0,0,0) #enable dis turn off everything
        print it.srqT()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        it.resena(mr=1)#trigger main reset
        time.sleep(3)
        print "==>> Show the alarm status after laser is tuned while the mrl is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"




        print "===>TEST7 "
        print "===>SRQT_Crl_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SRQT_Crl_Bit_Enabled.txt")#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        it.resena(mr=1)#trigger main reset
        self.it.srqT(0,0,0,0,0,0,0,0,1,0,0,0,0) #enable crl turn off everything
        print it.srqT()
        time.sleep(3)
        print "==>> Show the alarm status after laser is tuned while the Crl is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        it.resena(mr=1)#trigger main reset
        time.sleep(3)
        self.it.srqT(0,0,0,0,0,0,0,0,0,0,0,0,0) #enable dis turn off everything
        print it.srqT()
        print "==>> Show the alarm status after laser is tuned while the Crl is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"



        print "===>TEST8 "
        print "===>SRQT_FFreql_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SRQT_FFreql_Bit_Enabled.txt")#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock
        self.it.srqT(0,0,0,0,0,0,0,0,0,0,1,0,0) #enable ffreql turn off everything
        print it.srqT()
        freqDefault = t.controlStage().filter1TemperatureController().target() #read the default target f1
        t.controlStage().filter1TemperatureController().target(140) #set the filter1 temp to trigger fatal freq
        time.sleep(.5)
        print "==>> Show the alarm status after laser is tuned while the ffreql is on"
        self.monitorParameters()
        t.controlStage().filter1TemperatureController().target(freqDefault)#set to default
        time.sleep(2)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.srqT(0,0,0,0,0,0,0,0,0,0,0,0,0) #enable dis turn off everything
        print it.srqT()
        freqDefault = t.controlStage().filter1TemperatureController().target() #read the default target f1
        t.controlStage().filter1TemperatureController().target(140) #set the filter1 temp to trigger fatal freq
        time.sleep(.5)
        print "==>> Show the alarm status after laser is tuned while the ffreql is on"
        self.monitorParameters()
        t.controlStage().filter1TemperatureController().target(freqDefault)#set to default
        time.sleep(2)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"





        print "===>TEST9 "
        print "===>SRQT_Ftherml_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SRQT_Ftherml_Bit_Enabled.txt")
        self.it.mcb(sdf=0,adt=1)#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock
        self.it.srqT(0,0,0,0,0,0,0,0,0,0,0,1,0) #enable ftherml turn off everything
        print it.srqT()
        thermDefault = t.controlStage().filter1TemperatureController().target() #read the default target of sled
        t.controlStage().filter1TemperatureController().target(145) #set the sled temp to trigger fatal thermal alarm
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the ftherml is on"
        self.monitorParameters()
        self.it.resena(mr=1) #reset
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.srqT(0,0,0,0,0,0,0,0,0,0,0,0,0) #enable dis turn off everything
        print it.srqT()
        thermDefault = t.controlStage().filter1TemperatureController().target() #read the default target of sled
        t.controlStage().filter1TemperatureController().target(145) #set the sled temp to trigger fatal thermal alarm
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the ftherml is on"
        self.monitorParameters()
        self.it.resena(mr=1)#reset
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"





        print "===>TEST10 "
        print "===>SRQT_Fpowl_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SRQT_Fpowl_Bit_Enabled.txt")
        self.it.mcb(sdf=0,adt=1)#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock
        self.it.srqT(0,0,0,0,0,0,0,0,0,0,0,0,1) #enable fpowl turn off everything
        print it.srqT()
        sbc = t.controlStage().siBlockTemperatureController()
        t.controlStage().siBlockSlot(sbc)
        powDefault = sbc.target()#read the default target of siblock
        sbc.target(85) #kick the siblock to 85C to trigger Fpow alarm
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the fpowl is on"
        self.monitorParameters()
        
        sbc.target(powDefault) #set it back to normal
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.srqT(0,0,0,0,0,0,0,0,0,0,0,0,0) #enable dis turn off everything
        print it.srqT()
        sbc = t.controlStage().siBlockTemperatureController()
        t.controlStage().siBlockSlot(sbc)
        powDefault = sbc.target()#read the default target of siblock
        sbc.target(85) #kick the siblock to 85C to trigger Fpow alarm
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the fpowl is on"
        self.monitorParameters()
        
        sbc.target(powDefault) #set it back to normal
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"


        print "===>TEST11 "
        print "===>SRQT_Fvsfl_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SRQT_Fvsfl_Bit_Enabled.txt")
        self.it.mcb(sdf=0,adt=1)#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock
        self.it.srqT(0,0,0,0,0,0,0,0,0,1,0,0,0) #enable fvsfl turn off everything
        print it.srqT()
        thermDefault = t.controlStage().filter1TemperatureController().target() #read the default target of sled
        t.controlStage().filter1TemperatureController().target(145) #set the sled temp to trigger fatal thermal alarm
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the fvsfl is on"
        self.monitorParameters()
        self.it.resena(mr=1) #reset
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.srqT(0,0,0,0,0,0,0,0,0,0,0,0,0) #enable dis turn off everything
        print it.srqT()
        thermDefault = t.controlStage().filter1TemperatureController().target() #read the default target of sled
        t.controlStage().filter1TemperatureController().target(145) #set the sled temp to trigger fatal thermal alarm
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the fvsfl is on"
        self.monitorParameters()
        self.it.resena(mr=1)#reset
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"




        print "===>TEST12 "
        print "===>SRQT_Wvsfl_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("SRQT_Wvsfl_Bit_Enabled.txt")
        self.it.mcb(sdf=0,adt=1)#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock
        self.it.srqT(0,1,0,0,0,0,0,0,0,0,0,0,0) #enable fvsfl turn off everything
        print it.srqT()
        t.controlStage().frame().gainMediumCurrent(450) #set the gmi to a value that would be 90% of the threshold to trigger wvsfl
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the wvsfl is on"
        self.monitorParameters()
        #self.it.resena(mr=1) #reset
        #time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.srqT(0,0,0,0,0,0,0,0,0,0,0,0,0) #enable dis turn off everything
        print it.srqT()
        t.controlStage().frame().gainMediumCurrent(450) #set the gmi to a value that would be 90% of the threshold to trigger wvsfl
        print "==>> Show the alarm status after laser is tuned while the fvsfl is on"
##        self.monitorParameters()
##        self.it.resena(mr=1)#reset
##        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"


##         DIS         0x1 True 
##         WVSFL       0x0 False
##         WFREQL      0x0 False
##         WTHERML     0x0 False
##         WPWRL       0x0 False
##         XEL         0x0 False
##         CEL         0x0 False
##         MRL         0x1 True 
##         CRL         0x1 True 
##         FVSFL       0x1 True 
##         FFREQL      0x1 True 
##         FTHERML     0x1 True 
##         FPWRL       0x1 True         

    
##
class TestFatalTriggers:
    
    def __init__(self):
        #self.it = it_obj
        #self.t = t
        self.PORT = 3
        self.BAUD = 115200
        #self.g = g_obj

    def monitorParameters(self):
        f1 = t.domainStage().frame().filter1Temperature() #check the staus of alarms
        f2 = t.domainStage().frame().filter2Temperature()
        sled = t.domainStage().frame().sledTemperature()
        demodR = t.domainStage().frame().demodulationReal()
        siB = t.domainStage().frame().siBlockTemperature()
        pd = t.domainStage().frame().photodiodeCurrent()
        gmi = t.domainStage().frame().gainMediumCurrent()
        print "Time:",time.asctime(),"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", bin(self.it.statusF()[1].data()),"StatusW:", bin(self.it.statusW()[1].data())
        
    def runFatalTtest(self,it,g):
        """"""
        self.it = it
        self.g = g
 
        print "===>TEST1"
        print "===>FatalT_Wvsfl_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("FatalT_Wvsfl_Bit_Enabled.txt")
        self.it.mcb(sdf=0,adt=1)#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock
        self.it.fatalT(1,0,0,0,0,0,0,0,0) #enable wvsfl turn off everything
        print it.fatalT()
        t.controlStage().frame().gainMediumCurrent(450) #set the gmi to a value that would be 90% of the threshold to trigger wvsfl
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the wvsfl is on"
        self.monitorParameters()
        #self.it.resena(mr=1) #reset
        #time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.fatalT(0,0,0,0,0,0,0,0,0) #enable wvsfl turn off everything
        print it.fatalT()
        t.controlStage().frame().gainMediumCurrent(450) #set the gmi to a value that would be 90% of the threshold to trigger wvsfl
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the wvsfl is on"
        self.monitorParameters()
##        self.it.resena(mr=1)#reset
##        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"

        print "===>TEST2 "
        print "===>FatalT_WFreql_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("FatalT_WFreql_Bit_Enabled.txt")
        self.it.mcb(sdf=0,adt=1)#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        self.it.fatalT(0,1,0,0,0,0,0,0,0) #enable wvsfl turn off everything
        print it.fatalT()
        self.it.statusF()
        self.it.statusW() #Do not clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after laser is tuned while the wfreql is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.fatalT(0,0,0,0,0,0,0,0,0) #enable wvsfl turn off everything
        print it.fatalT()
        self.it.statusF()
        self.it.statusW() #Do not clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after laser is tuned while the wfreql is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"





        print "===>TEST3 "
        print "===>FatalT_Wtherml_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("FatalT_Wtherml_Bit_Enabled.txt")#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        self.it.fatalT(0,0,1,0,0,0,0,0,0) #enable wtherml turn off everything
        print it.fatalT()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        t.controlStage().sledTemperatureController().target(80) #ramp sled to 80C
        time.sleep(1)
        print "==>> Show the alarm status after laser is tuned while the wtherml is on"
        self.monitorParameters()
        t.controlStage().sledTemperatureController().target(50) #set sled back to 50C
        time.sleep(2)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.fatalT(0,0,0,0,0,0,0,0,0) #enable wtherml turn off everything
        print it.fatalT()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        t.controlStage().sledTemperatureController().target(80)#ramp sled to 80C
        time.sleep(1)
        print "==>> Show the alarm status after laser is tuned while the wtherml is on"
        self.monitorParameters()
        t.controlStage().sledTemperatureController().target(50)#set sled back to 50C
        time.sleep(2)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"



        print "===>TEST4 "
        print "===>FatalT_WPowl_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("FatalT_WPowl_Bit_Enabled.txt")#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        self.it.fatalT(0,0,0,1,0,0,0,0,0) #enable wtherml turn off everything
        print it.fatalT()
        self.it.statusF()
        self.it.statusW() #Do not clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after laser is tuned while the wpowl is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.fatalT(0,0,0,0,0,0,0,0,0) #enable wtherml turn off everything
        print it.fatalT()
        self.it.statusF()
        self.it.statusW() #Do not clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after laser is tuned while the wpowl is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"


        print "===>TEST5 "
        print "===>FatalT_Mrl_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("FatalT_Mrl_Bit_Enabled.txt")#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        it.resena(mr=1)#trigger main reset
        time.sleep(3)
        self.it.fatalT(0,0,0,0,1,0,0,0,0) #enable wtherml turn off everything
        print it.fatalT()
        print "==>> Show the alarm status after laser is tuned while the mrl is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        it.resena(mr=1)#trigger main reset
        time.sleep(3)
        self.it.fatalT(0,0,0,0,0,0,0,0,0) #enable wtherml turn off everything
        print it.fatalT()
        print "==>> Show the alarm status after laser is tuned while the mrl is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        time.sleep(1)
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"



        print "===>TEST6 "
        print "===>FatalT_Fvsfl_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("FatalT_Fvsfl_Bit_Enabled.txt")
        self.it.mcb(sdf=0,adt=1)#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock
        self.it.fatalT(0,0,0,0,0,1,0,0,0) #enable Fvsfl turn off everything
        print it.fatalT()
        thermDefault = t.controlStage().filter1TemperatureController().target() #read the default target of sled
        t.controlStage().filter1TemperatureController().target(145) #set the sled temp to trigger fatal thermal alarm
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the fvsfl is on"
        self.monitorParameters()
        self.it.resena(mr=1) #reset
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.fatalT(0,0,0,0,0,0,0,0,0) #enable Fvsfl turn off everything
        print it.fatalT()
        thermDefault = t.controlStage().filter1TemperatureController().target() #read the default target of sled
        t.controlStage().filter1TemperatureController().target(145) #set the sled temp to trigger fatal thermal alarm
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the fvsfl is on"
        self.monitorParameters()
        self.it.resena(mr=1)#reset
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"


        print "===>TEST7 "
        print "===>FatalT_FFreql_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("FatalT_FFreql_Bit_Enabled.txt")#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock
        self.it.fatalT(0,0,0,0,0,0,1,0,0) #enable FFreql turn off everything
        print it.fatalT()
        freqDefault = t.controlStage().filter1TemperatureController().target() #read the default target f1
        t.controlStage().filter1TemperatureController().target(140) #set the filter1 temp to trigger fatal freq
        time.sleep(.5)
        print "==>> Show the alarm status after laser is tuned while the ffreql is on"
        self.monitorParameters()
        t.controlStage().filter1TemperatureController().target(freqDefault)#set to default
        time.sleep(2)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.fatalT(0,0,0,0,0,0,0,0,0) #enable FFreql turn off everything
        print it.fatalT()
        freqDefault = t.controlStage().filter1TemperatureController().target() #read the default target f1
        t.controlStage().filter1TemperatureController().target(140) #set the filter1 temp to trigger fatal freq
        time.sleep(.5)
        print "==>> Show the alarm status after laser is tuned while the ffreql is on"
        self.monitorParameters()
        t.controlStage().filter1TemperatureController().target(freqDefault)#set to default
        time.sleep(2)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"



        print "===>TEST8 "
        print "===>FatalT_Ftherml_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("FatalT_Ftherml_Bit_Enabled.txt")
        self.it.mcb(sdf=0,adt=1)#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock
        self.it.fatalT(0,0,0,0,0,0,0,1,0) #enable Ftherml turn off everything
        print it.fatalT()
        thermDefault = t.controlStage().filter1TemperatureController().target() #read the default target of sled
        t.controlStage().filter1TemperatureController().target(145) #set the sled temp to trigger fatal thermal alarm
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the ftherml is on"
        self.monitorParameters()
        self.it.resena(mr=1) #reset
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.fatalT(0,0,0,0,0,0,0,0,0) #enable Ftherml turn off everything
        print it.fatalT()
        thermDefault = t.controlStage().filter1TemperatureController().target() #read the default target of sled
        t.controlStage().filter1TemperatureController().target(145) #set the sled temp to trigger fatal thermal alarm
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the ftherml is on"
        self.monitorParameters()
        self.it.resena(mr=1)#reset
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"



        print "===>TEST9 "
        print "===>FatalT_Fpowl_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("FatalT_Fpowl_Bit_Enabled.txt")
        self.it.mcb(sdf=0,adt=1)#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock
        self.it.fatalT(0,0,0,0,0,0,0,0,1) #enable Fpowl turn off everything
        print it.fatalT()
        sbc = t.controlStage().siBlockTemperatureController()
        t.controlStage().siBlockSlot(sbc)
        powDefault = sbc.target()#read the default target of siblock
        sbc.target(85) #kick the siblock to 85C to trigger Fpow alarm
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the fpowl is on"
        self.monitorParameters()
        
        sbc.target(powDefault) #set it back to normal
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.fatalT(0,0,0,0,0,0,0,0,0) #enable Fpowl turn off everything
        print it.fatalT()
        sbc = t.controlStage().siBlockTemperatureController()
        t.controlStage().siBlockSlot(sbc)
        powDefault = sbc.target()#read the default target of siblock
        sbc.target(85) #kick the siblock to 85C to trigger Fpow alarm
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the fpowl is on"
        self.monitorParameters()
        
        sbc.target(powDefault) #set it back to normal
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"



##         WVSFL    0x0 False
##         WFREQL   0x0 False
##         WTHERML  0x0 False
##         WPWRL    0x0 False
##         MRL      0x0 False
##         FVSFL    0x1 True 
##         FFREQL   0x1 True 
##         FTHERML  0x1 True 
##         FPWRL    0x1 True



class TestAlmTriggers:
    
    def __init__(self):
        #self.it = it_obj
        #self.t = t
        self.PORT = 3
        self.BAUD = 115200
        #self.g = g_obj

    def monitorParameters(self):
        statF = bin(self.it.statusF()[1].data())
        statW = bin(self.it.statusW()[1].data())
        f1 = t.domainStage().frame().filter1Temperature() #check the staus of alarms
        f2 = t.domainStage().frame().filter2Temperature()
        sled = t.domainStage().frame().sledTemperature()
        demodR = t.domainStage().frame().demodulationReal()
        siB = t.domainStage().frame().siBlockTemperature()
        pd = t.domainStage().frame().photodiodeCurrent()
        gmi = t.domainStage().frame().gainMediumCurrent()
        print "Time:",time.asctime(),"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", statF,"StatusW:", statW
        
    def runAlmTtest(self,it,g):
        """"""
        self.it = it
        self.g = g


        print "===>TEST1 "
        print "===>AlmT_Wvsf_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("AlmT_Wvsfl_Bit_Enabled.txt")
        self.it.mcb(sdf=0,adt=1)#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock
        self.it.almT(1,0,0,0,0,0,0,0) #enable Wvsf turn off everything
        print it.almT()
        t.controlStage().frame().gainMediumCurrent(450) #set the gmi to a value that would be 90% of the threshold to trigger wvsf
        #time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the wvsf is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.almT(0,0,0,0,0,0,0,0) #enable Wvsf turn off everything
        print it.almT()
        t.controlStage().frame().gainMediumCurrent(450) #set the gmi to a value that would be 90% of the threshold to trigger wvsf
        print "==>> Show the alarm status after laser is tuned while the wvsf  is on"
        self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"


        print "===>TEST2 "
        print "===>AlmT_Wfreq_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("AlmT_Wfreq_Bit_Enabled.txt")
        self.it.mcb(sdf=0,adt=1)#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        #monChannellock()#wait to chanel lock
        self.it.almT(0,1,0,0,0,0,0,0) #enable Wfreq turn off everything
        print it.almT()
        #t.controlStage().frame().gainMediumCurrent(450) #set the gmi to a value that would be 90% of the threshold to trigger Wfreq
        #time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the Wfreq is on"
        for i in range(5):
            self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        #monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.almT(0,0,0,0,0,0,0,0) #enable Wfreq turn off everything
        print it.almT()
        #t.controlStage().frame().gainMediumCurrent(450) #set the gmi to a value that would be 90% of the threshold to trigger Wfreq
        print "==>> Show the alarm status after laser is tuned while the fvsfl is on"
        for i in range(5):
            self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"


        print "===>TEST3 "
        print "===>AlmT_Wtherm_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("AlmT_Wtherm_Bit_Enabled.txt")#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wiat to chanel lock#monitor until channel lock
        self.it.almT(0,0,1,0,0,0,0,0) #enable Wtherm turn off everything
        print it.almT()
        #self.it.statusF(1,1,1,1,1,1,1,1)
        #self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        t.controlStage().sledTemperatureController().target(80) #ramp sled to 80C
        time.sleep(1)
        print "==>> Show the alarm status after laser is tuned while the wtherm is on"
        for i in range(10):
            self.monitorParameters()
        t.controlStage().sledTemperatureController().target(50) #set sled back to 50C
        time.sleep(2)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.almT(0,0,0,0,0,0,0,0) #enable Wtherm turn off everything
        print it.almT()
        #self.it.statusF(1,1,1,1,1,1,1,1)
        #self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        t.controlStage().sledTemperatureController().target(80)#ramp sled to 80C
        time.sleep(1)
        print "==>> Show the alarm status after laser is tuned while the wtherml is on"
        for i in range(10):
            self.monitorParameters()
        t.controlStage().sledTemperatureController().target(50)#set sled back to 50C
        time.sleep(2)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"



        print "===>TEST4 "
        print "===>AlmT_Wpow_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("AlmT_Wpow_Bit_Enabled.txt")
        self.it.mcb(sdf=0,adt=1)#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        self.it.almT(0,0,0,1,0,0,0,0) #enable Wpow turn off everything
        print it.almT()
        print "==>> Show the alarm status after laser is tuned while the Wpow is on"
        for i in range(5):
            self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser
        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        self.it.almT(0,0,0,0,0,0,0,0) #enable Wpow turn off everything
        print it.almT()
        print "==>> Show the alarm status after laser is tuned while the Wpow is on"
        for i in range(5):
            self.monitorParameters()
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"



        print "===>TEST5 "
        print "===>AlmT_Fvsf_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("AlmT_Fvsf_Bit_Enabled.txt")
        self.it.mcb(sdf=0,adt=1)#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock
        self.it.almT(0,0,0,0,1,0,0,0) #enable Fvsf turn off everything
        print it.almT()
        #hermDefault = t.controlStage().filter1TemperatureController().target() #read the default target of sled
        t.controlStage().frame().gainMediumCurrent(500) #set the gmi very high to trigger laser age to 100% and therefore fvsf
        #time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the Fvsf is on"
        for i in range(20):
            self.monitorParameters()
        self.it.resena(mr=1) #reset
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.almT(0,0,0,0,0,0,0,0) #enable Fvsf turn off everything
        print it.almT()
        #thermDefault = t.controlStage().filter1TemperatureController().target() #read the default target of sled
        t.controlStage().frame().gainMediumCurrent(500) #set the gmi very high to trigger laser age to 100% and therefore fvsf
        #time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the Fvsf is on"
        for i in range(20):
            self.monitorParameters()
        self.it.resena(mr=1)#reset
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"



        print "===>TEST6 "
        print "===>AlmT_FFreq_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("AlmT_FFreq_Bit_Enabled.txt")#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock
        self.it.almT(0,0,0,0,0,1,0,0) #enable FFreq turn off everything
        print it.almT()
        freqDefault = t.controlStage().filter1TemperatureController().target() #read the default target f1
        t.controlStage().filter1TemperatureController().target(140) #set the filter1 temp to trigger fatal freq
        time.sleep(.5)
        print "==>> Show the alarm status after laser is tuned while the FFreq is on"
        self.monitorParameters()
        t.controlStage().filter1TemperatureController().target(freqDefault)#set to default
        time.sleep(2)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.almT(0,0,0,0,0,0,0,0) #enable FFreq turn off everything
        print it.almT()
        freqDefault = t.controlStage().filter1TemperatureController().target() #read the default target f1
        t.controlStage().filter1TemperatureController().target(140) #set the filter1 temp to trigger fatal freq
        time.sleep(.5)
        print "==>> Show the alarm status after laser is tuned while the FFreq is on"
        self.monitorParameters()
        t.controlStage().filter1TemperatureController().target(freqDefault)#set to default
        time.sleep(2)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"



        print "===>TEST7 "
        print "===>AlmT_Ftherm_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("AlmT_Ftherm_Bit_Enabled.txt")
        self.it.mcb(sdf=0,adt=1)#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock
        self.it.almT(0,0,0,0,0,0,1,0) #enable FTherm turn off everything
        print it.almT()
        thermDefault = t.controlStage().filter1TemperatureController().target() #read the default target of sled
        t.controlStage().filter1TemperatureController().target(145) #set the sled temp to trigger fatal thermal alarm
        #time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the FTherm is on"
        for i in range(20):
            self.monitorParameters()
        self.it.resena(mr=1) #reset
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.almT(0,0,0,0,0,0,0,0) #enable FTherm turn off everything
        print it.almT()
        thermDefault = t.controlStage().filter1TemperatureController().target() #read the default target of sled
        t.controlStage().filter1TemperatureController().target(145) #set the sled temp to trigger fatal thermal alarm
        #time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the ftherm is on"
        for i in range(20):
            self.monitorParameters()
        self.it.resena(mr=1)#reset
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"




        print "===>TEST8 "
        print "===>AlmT_Fpow_Bit_Enabled"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("AlmT_Fpow_Bit_Enabled.txt")
        self.it.mcb(sdf=0,adt=1)#set the mcb register
        print "Turn on laser..."
        self.it.resena(0)
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms        
        self.it.mcb(sdf=0,adt=1)
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock
        self.it.almT(0,0,0,0,0,0,0,1) #enable FTherm turn off everything
        print it.almT()
        sbc = t.controlStage().siBlockTemperatureController()
        t.controlStage().siBlockSlot(sbc)
        powDefault = sbc.target()#read the default target of siblock
        sbc.target(85) #kick the siblock to 85C to trigger Fpow alarm
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the fpow is on"
        self.monitorParameters()
        
        sbc.target(powDefault) #set it back to normal
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()
        it.resena(0)#need to turn off laser

        print "Turn on laser"
        self.it.resena(sena=1)#turn on the laser
        monChannellock()#wait to chanel lock#monitor until channel lock
        self.it.almT(0,0,0,0,0,0,0,0) #enable FTherm turn off everything
        print it.almT()
        sbc = t.controlStage().siBlockTemperatureController()
        t.controlStage().siBlockSlot(sbc)
        powDefault = sbc.target()#read the default target of siblock
        sbc.target(85) #kick the siblock to 85C to trigger Fpow alarm
        time.sleep(2)
        print "==>> Show the alarm status after laser is tuned while the fpow is on"
        self.monitorParameters()
        
        sbc.target(powDefault) #set it back to normal
        time.sleep(3) #wait until stabilize
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1) #clear alarms
        print "==>> Show the alarm status after the alarms are cleared"
        self.monitorParameters()


        print "Test Complete"
        it.resena(mr=1)
        time.sleep(3)
        print "\n"
        print "\n"
        print "\n"



## ALMT          0x2a 
## Data         0xd0d 
##         WVSF      0x1 True 
##         WFREQ     0x1 True 
##         WTHERM    0x0 False
##         WPWR      0x1 True 
##         FVSF      0x1 True 
##         FFREQ     0x1 True 
##         FTHERM    0x0 False
##         FPWR      0x1 True 

class TestPowerThreshold:

    def __init__(self):
        #self.it = it_obj
        #self.t = t
        self.PORT = 3
        self.BAUD = 115200
        #self.g = g_obj

    def monitorParameters(self):
        statF = bin(self.it.statusF()[1].data())
        statW = bin(self.it.statusW()[1].data())
        f1 = t.domainStage().frame().filter1Temperature() #check the staus of alarms
        f2 = t.domainStage().frame().filter2Temperature()
        sled = t.domainStage().frame().sledTemperature()
        demodR = t.domainStage().frame().demodulationReal()
        siB = t.domainStage().frame().siBlockTemperature()
        pd = t.domainStage().frame().photodiodeCurrent()
        gmi = t.domainStage().frame().gainMediumCurrent()
        print "Time:",time.asctime(),"F1:",f1,"F2:",f2,"SLED:",sled,"DEMODR:",demodR,"SIB:",siB,"PD:",pd,"GMI:",gmi,"StatusF:", statF,"StatusW:", statW
        
    def runPowerThresholdtest(self,it,g):
        """"""
        self.it = it
        self.g = g


#set the warning to a value a, adjust the fpowerth until it reads XE

        print "===>TEST1 "
        print "===>FindHighLowFpowThLimits.txt"
        self.it.connect(self.PORT,self.BAUD) #connect
        time.sleep(2)
        self.it.logging(True)#turn on the logging
        self.it.logfile("FindHighLowFpowThLimits.txt")
        default = 1000
        self.it.fPowTh(default)
        #what is the lowest value the fpowth and wpowth can reach?
        self.fpowDefault = int(self.it.fPowTh()[1])
        self.wpowDefault = int(self.it.wPowTh()[1])
        self.newfpowDefault = self.it.fPowTh(int(self.fpowDefault) - 1)
        while 1:
            self.newfpowDefault = self.it.fPowTh(int(self.newfpowDefault[1]) - 1)#reduce the power threshold by 1dB
            print "==>> Warning Power Threshold:%d"%int(self.wpowDefault), "  " , "==>> Fatal Power Threshold:%d"%int(self.newfpowDefault[1])
            
            if not it.fPowTh(self.newfpowDefault[1])[0] == 'OK':
                print "==>> Reached Low Threshold of %d:"%int(self.newfpowDefault[1])
                break
            
        self.newfpowDefault = self.it.fPowTh(int(self.fpowDefault) + 1)
        while 1:
            self.newfpowDefault = self.it.fPowTh(int(self.newfpowDefault[1])+ 1)#add the power threshold by 1dB
            print "==>> Warning Power Threshold:%d"%int(self.wpowDefault), "  " , "==>> Fatal Power Threshold:%d"%int(self.newfpowDefault[1])
            if not it.fPowTh(self.newfpowDefault[1])[0] == 'OK':
                print "==>> Reached High Threshold of %d:"%int(self.newfpowDefault[1])
                break

        it.disconnect()
            
        #Can Fpow go below Wpow?
        #Can Wpoer go above fpow? or vise versa

 
        

class TestFrequencyThreshold:
    pass

class TestThermalThreshold:
    pass

class TestModuleConfigurationBehavior:
    pass





            
    



    
TestFatalAlarms = TestFatalAlarms()
TestSrqTriggers = TestSrqTriggers()
TestFatalTriggers = TestFatalTriggers()
TestAlmTriggers = TestAlmTriggers()
TestPowerThreshold = TestPowerThreshold()

if __name__== '__main__':
    

##    try:
##        TestFatalAlarms.checkFrequencyalarms()
##
##    except:
##        raise


##    try:
##        TestSrqTriggers.runSrqtTest(it,g)
##
##    except:
##        raise


##    try:
##        TestFatalTriggers.runFatalTtest(it,g)
##    except:
##        raise
##
##
    try:
        TestAlmTriggers.runAlmTtest(it,g)
    except:
        raise
##
##
##    try:
##        TestPowerThreshold.runPowerThresholdtest(it,g)
##    except:
##        raise









     



    






    


