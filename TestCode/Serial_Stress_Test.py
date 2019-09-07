# OIF STRESS TEST
import numpy as np
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
import itertools
import random
import sys
from datetime import timedelta

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)

####################################################################################
# See stressTest().  Tunes, VOAs, FTFs, tunes again -over and over.
####################################################################################
class serialTest:

    def __init__(self, itla):
        self.it = itla
        self.currentChannel = 'None'
        self.maxchan = 'None'
        self.maxVoa = 'None'
        self.minVoa = 'None'
        self.currentVoa = 'None'
        self.voaStep =  'None'
        self.voaSetMin = 'None'
        self.voaSetMax = 'None'
        self.maxFtf = 'None'
        self.currentFtf = 'None'
        self.ftfStep = 'None'
        self.ftfSetMin = 'None'
        self.ftfSetMax = 'None'
        self.totalOifTransactions = 0
        self.totalMzTransactions = 0
        self.totalVoas = 0
        self.totalFtfs = 0
        self.totalTimeOuts = 0
        self.pwdSet = 0
    def is_float(self, input):
        try:
            num = float(input)
        except ValueError:
            return False
        return True

####################################################################################
# Read grid spacing, first channel frequency, last frequency supported.  Calculate
#	maximum channel setting this device can be set to.
# Return: The number of OIF reads done during the call.
####################################################################################
    def getMaxChannel(self):
      if self.maxchan == 'None':
          grid = self.it.grid()[1]
          fcf1 = self.it.fcf1()[1]
          fcf2 = self.it.fcf2()[1]
          lfh1 = self.it.lfh()[1]
          lfh2 = self.it.lfl()[1]
          fcf = (fcf1 * 10000) + fcf2  # Convert to 100Mhz
          lfh = (lfh1 * 10000) + lfh2
          frange = lfh - fcf
          lastChannel= int( (frange/grid) + 1 )
          self.maxchan = lastChannel
      if self.currentChannel == 'None':
          self.currentChannel = self.it.channel()[1]      
          return (6)    # assume needed channel    
      return (0)

####################################################################################
# Reads a random register and throws away the response.  
#	supportedOnly==1: Read only MSA specified registers.
#	supportedOnly==0: Read any register 0x0->0x62 (several unsupported)
####################################################################################
    def randomRead(self, supportedOnly=1):
	if(supportedOnly == 1):
		regset = [[i for i in range(0x0B)], [i for i in range(0x0D,0x10)], [i for i in range(0x13,0x15)],  [i for i in range(0x20,0x2A)], [i for i in range(0x30,0x36)], [i for i in range(0x40,0x43)], [i for i in range(0x4F-0x5C)], [i for i in range(0x5F-0x62)]]
		regset = list(itertools.chain(*regset))
	else:
		regset = [i for i in range(0x62)]
		
	regToRead = random.choice(regset)
	self.it.register(ITLA.Register.Register(address=regToRead,data=0x0), write=False)

####################################################################################
# Will run until either all pending bits clear in the NOP or a timeout occurrs.  
#	Will also do random reads (from 0-10) of miscellaneous registers between
#	NOP requests.
#   log99 = interleave 0x99 polling.
#   verbose = output stuff to screen.  (0/1/2 -depending on how much you want)        
####################################################################################
    def waitLockAndRandomReads(self, log99 = 0, timeoutSec=200, verbose = 1):
        if(log99==1 and self.pwdSet==0):
            self.it.setpassword()
            self.pwdSet=1
        oifIterations = 0
        iterations99 = 0
        startT = time.time()
        endT = startT + timeoutSec
        while self.it.nop()[1].fieldPending().value() != 0 and time.time() < endT:
		oifIterations = oifIterations + 1
		for i in range(random.randrange(0,10,1)):
                  self.randomRead(supportedOnly=1)
                  oifIterations = oifIterations + 1
                  if(log99==1):
                    self.it.readx99()
                    iterations99 = iterations99 + 1
                    self.totalMzTransactions = self.totalMzTransactions + 1
        if(verbose>0):
            if(time.time() > endT):
                print ' -Timeout Waiting-'
                self.totalTimeOuts = self.totalTimeOuts + 1
            if(verbose>1):
                print ' -Pending clear wait time: ', time.time()-startT
                print ' -Total OIF commands while waiting: ', oifIterations
                print ' -Total 0x99 reads while waiting: ', iterations99
        return oifIterations
	
####################################################################################
#   powerCycleProb = % chance the laser will power cycle before starting tune starts
####################################################################################
    def startRandomTune(self, verbose = 1, powerCycleProb = 10):
        oifIterations = 0
        oifIterations = oifIterations + self.getMaxChannel()
        upcomingChannel = self.currentChannel
        sena = self.it.resena()[1].fieldSena()
        oifIterations = oifIterations + 1
        while upcomingChannel == self.currentChannel:
            upcomingChannel = random.randrange(1,self.maxchan,1)
            oifIterations = oifIterations + 1
        if(verbose>0):
            print '**Channel:' + str(upcomingChannel)            

        if(sena.value() == 0):
            self.it.channel(upcomingChannel)
            self.it.resena(sena=1)
            oifIterations = oifIterations + 2
        elif(random.randrange(1,100,1)<=powerCycleProb): # % chance of turning off laser.         
            self.it.resena(sena=0)
            if(verbose>0):
                print '-Laser Power Toggled-'
            self.it.channel(upcomingChannel)
            time.sleep(.020)
            self.it.resena(sena=1)
            oifIterations = oifIterations + 3
        else:
            self.it.channel(upcomingChannel)
            oifIterations = oifIterations + 1
            
        self.currentChannel = upcomingChannel
        return oifIterations
    
####################################################################################
# Sets the unit to an arbitrary channel.  If sena==0 -then sends sena=1. Will then
# poll NOP for pending clear or timeout while doing random reads of other registers.
#   log99 = interleave 0x99 polling.
#   verbose = output stuff to screen.  (0/1/2 -depending on how much you want)        
####################################################################################
    def tuneAndRandomReads(self, log99 = 0, verbose = 1):
        oifIterations = 0
        oifIterations = oifIterations  + self.startRandomTune(verbose)
        oifIterations = oifIterations + self.waitLockAndRandomReads(log99, timeoutSec = 45)
        return oifIterations

####################################################################################
# Gathers VOA capabilities of the unit if needed.  Then sets the upper and lower
#  limits of the next VOA operation.
#   voaStepMag = Percentage of total allowable VOA (from minimum to maximum power)
#     to be used as a maximum voa step size (100=total random between min and max power)
####################################################################################
    def setVoaRange(self, voaStepMag = 100):
        oifIterations = 0
        if self.maxVoa == 'None':
            self.maxVoa = self.it.opsh()[1]
            oifIterations = oifIterations + 1
        if self.minVoa == 'None':
            self.minVoa = self.it.opsl()[1]
            oifIterations = oifIterations + 1
        if(self.currentVoa == 'None'):
            self.currentVoa = self.it.pwr()[1]
            oifIterations = oifIterations + 1
        self.voaStep = int((self.maxVoa - self.minVoa) * (voaStepMag * .01))
        self.voaSetMin = max((self.currentVoa - self.voaStep), self.minVoa)
        self.voaSetMax = min((self.currentVoa + self.voaStep), self.maxVoa)
        return oifIterations
        
####################################################################################
# Sets the unit to an arbitrary power level.  Will then poll NOP for pending clear
# or timeout while doing random reads of other registers.
#   voaStepMag = Percentage of total allowable VOA (from min to max power) to be
#       used as a max VOA step size (100=random between full min and max power)
#   log99 = interleave 0x99 polling.
#   verbose = output stuff to screen.  (0/1/2 -depending on how much you want)        
####################################################################################
    def voaAndRandomReads(self, log99 = 0, voaStepMag = 100, verbose = 1):
        oifIterations = 0
        prevVoa = self.currentVoa
        oifIterations = oifIterations + self.setVoaRange(voaStepMag)
        self.currentVoa = random.randrange(self.voaSetMin, self.voaSetMax, 1)
        self.it.pwr(self.currentVoa)
        if(verbose>0):
            print 'VOA:' + str(self.currentVoa)
            if(verbose>1):
                print 'VOA Power Swing: ', self.currentVoa - prevVoa
        oifIterations = oifIterations + 1
        oifIterations = oifIterations + self.waitLockAndRandomReads(log99, timeoutSec = 150)
        return oifIterations

####################################################################################
# Gathers FTF capabilities and sets the upper/lower limits of the upcoming random FTF.
#   ftfStepMag =  Percentage of the total allowable FTF (from minimum to maximum allowed)
#   to be used as a maximum FTF step size (100=total random between min and max)
####################################################################################
    def setFtfRange(self, ftfStepMag = 100):
        oifIterations = 0
        if self.maxFtf == 'None':
		self.maxFtf = self.it.ftfr()[1]
		oifIterations = oifIterations + 1
        if (self.currentFtf == 'None'):
		self.currentFtf = self.it.ftf()[1]
		oifIterations = oifIterations + 1
        self.ftfStep = int((self.maxFtf * 2) * (.01*ftfStepMag))
        self.ftfSetMin = max((self.currentFtf - self.ftfStep), -1*self.maxFtf)
        self.ftfSetMax = min((self.currentFtf + self.ftfStep), self.maxFtf)
        return oifIterations
####################################################################################
# Sets the unit to a new FTF frequency.  Will then poll NOP for pending clear
# or timeout while doing random reads of other registers.
#   ftfStepMag = Percentage of the allowable FTF (from minimum to maximum allowable)
#       to be used as a maximum FTF step size (100=total random between min and max)
#   log99 = interleave 0x99 polling.
#   verbose = output stuff to screen.  (0/1/2 -depending on how much you want)        
####################################################################################
    def ftfAndRandomReads(self, log99 = 0, ftfStepMag = 100, verbose = 1):
        oifIterations = 0
        prevFtf = self.currentFtf
        oifIterations = oifIterations + self.setFtfRange(ftfStepMag)
        self.currentFtf = random.randrange(self.ftfSetMin, self.ftfSetMax, 1)
        self.it.ftf(self.currentFtf)
        if(verbose>0):
            print 'FTF:' + str(self.currentFtf)
            if(verbose>1):
                print 'FTF Frequency Swing: ', self.currentFtf - prevFtf
        oifIterations = oifIterations + 1
        oifIterations = oifIterations + self.waitLockAndRandomReads(log99, timeoutSec = 150)
        return oifIterations

####################################################################################
# Will tune the unit the number of times specified by the switchCount argument.
# When the tune is finished, will do 0-5 power/VOA operations.
# When the VOAs are finished, will do 0-10 FTF operations per VOA operation.
# While tuning/VOA/FTF is in progress -random register reads will happen.
#  oifTransactions -setting this a number will cause the switchCount argument to 
#    be ignored, and will stop the test when a switch sequence is finished and 
#    at least a count of "oifTransactions" has occurred.
#  testRange -Percentage of the max allowable swing for VOA/FTF actions during test.
#   (see ftfStepMag and voaStepMag)
#  log99 = interleave 0x99 polling.
#  verbose = output stuff to screen.  (0/1/2 -depending on how much you want)        
####################################################################################
    def stressTest(self, switchCount = 1, poll99 = 0, oifTransactions = 'None', testRange = 100, verbose = 1):
        self._initTest()
        if(oifTransactions != 'None'):
            switchCount = 1000
        count = switchCount
            
        print 'Starting OIF test'
        while(count != 0):
            voaIterations = random.randrange(0, 5, 1)
            self.totalVoas = self.totalVoas + voaIterations
            if(verbose>0):
                print 'Switch #' + str(switchCount - count + 1)
            self.totalOifTransactions = self.totalOifTransactions + self.tuneAndRandomReads(log99 = poll99, verbose = verbose)
            if(voaIterations):
                while(voaIterations):
                    self.totalOifTransactions  = self.totalOifTransactions + self.voaAndRandomReads(log99 = poll99, voaStepMag = testRange, verbose = verbose)
                    ftfIterations = random.randrange(0, 10, 1)
                    self.totalFtfs = self.totalFtfs + ftfIterations
                    voaIterations = voaIterations - 1
                    while(ftfIterations):
                        self.totalOifTransactions = self.totalOifTransactions + self.ftfAndRandomReads(log99 = poll99, ftfStepMag = testRange, verbose = verbose)
                        ftfIterations = ftfIterations - 1
            else:
                ftfIterations = random.randrange(0, 10, 1)
                while(ftfIterations):
                    self.totalOifTransactions = self.totalOifTransactions + self.ftfAndRandomReads(log99 = poll99, ftfStepMag = testRange, verbose = verbose)
                    ftfIterations = ftfIterations - 1
            if(oifTransactions != 'None'):
                if(self.totalOifTransactions >= oifTransactions):
                    count = 0
            else:
                count = count - 1
                        
        self.showTest(switchCount)
        self.parseGraphLog()
        
####################################################################################
# Initialize counts and times at beginning of test (used in showTest())
####################################################################################
    def _initTest(self):
        self.startTime = datetime.datetime.now()
        self.pwdSet = 0
        self.totalOifTransactions = 0
        self.totalMzTransactions = 0
        self.totalVoas = 0
        self.totalFtfs = 0
        self.it.logging(True)

####################################################################################
# Print to screen main test statistics.
####################################################################################
    def showTest(self, tuneCount):
        endTime = datetime.datetime.now()
        print '*** Done *** '
        print 'Start: ', self.startTime.strftime("%a %b %d %H:%M:%S %Y")
        print 'End: ', endTime.strftime("%a %b %d %H:%M:%S %Y")
        print 'Test Time: ', (endTime-self.startTime)
        print 'Total Switches: ', tuneCount
        print 'Total VOAs: ', self.totalVoas
        print 'Total FTFs: ', self.totalFtfs
        print 'Total Timeouts: ', self.totalTimeOuts
        print 'Total OIF Transactions: ', self.totalOifTransactions
        print 'Total MZ Transactions: ', self.totalMzTransactions
        print 'Total Msg Count: ', self.totalOifTransactions + self.totalMzTransactions

####################################################################################
# Use OIF log.  Parse into simple table to be used in creating a boxplot of timing
####################################################################################
    def parseGraphLog(self):
        print 'Parsing OIF Log'
        startTime = datetime.datetime.now()
        self.parseOifLog()
        endParseTime = datetime.datetime.now()
        print 'End Parse: ', endParseTime.strftime("%a %b %d %H:%M:%S %Y")
        print 'Parse Time: ', (endParseTime-startTime)
        self.graphOifData()
        print 'Test Finished'
        
####################################################################################
# Open the loggile for the current test.  Read a line from the file -Figure out 
# if it's a keeper or a throw away entry...
# Create new entry with register/response-time/intercommand-time before/intercommand-time after
# Write entry to formatted timing log file.
####################################################################################
    def parseOifLog(self):
        print 'Preparing log data'
        previousTime = None
        previousOifCmd = None
        print 'OIF Log Filename: ', self.it.getlogfilename()
        
        with open(self.it.getlogfilename(), 'r') as oiflogfile:
            with open(self.it.getlogfilename().split('.')[0] + '_stats.' + self.it.getlogfilename().split('.')[1], 'w+') as oifTimingfile:
                entry = oiflogfile.readline()
                while entry:
                    list = entry.split(" ")
                    if self.is_float(list[0].split("s")[0]) and list[6] == 'Rx:' and self.is_float(list[11].split("ms")[0]):
                        time = float(list[0].split("s")[0])
                        register = list[3]
                        if previousTime != None and previousOifCmd != None:     #
                            oifIntermessageTime = time - previousTime
                            respTime = float(list[11].translate(None,'ms'))
                            # Register, Response Time, inter-command Time, relative time, OIF command prior to this one.
                            line = str(register) + ',' + str(respTime) + ',' + str(oifIntermessageTime) + ',' + str(time) + ',' + str(previousOifCmd) + '\n'
                            oifTimingfile.write(line)
                        previousTime = time
                        previousOifCmd = register
                    entry = oiflogfile.readline()
        oiflogfile.close()
        oifTimingfile.close()
                    
#######################################################
# Read the CSV file prepared by parseOifLog().  Make boxplot.
# FILE FORMAT FROM parseOifLog:
# Reg, respT, InterMsgT, deltaT, PrevReg
# 33,4.0,0.01,59.702,35
#######################################################
    def graphOifData(self):
        print 'Preparing graph of OIF timing data'
        df = pd.read_csv(self.it.getlogfilename().split('.')[0] + '_stats.' + self.it.getlogfilename().split('.')[1], sep=',', names=['Register', 'Response_Time','InterMsg_Time', 'Total_Time', 'Prev_Reg'])
        slice = df.iloc[:,[0, 1]]
#        print 'Response Time Stats:', slice.Response_Time.describe()

        # Need max/min/mean/average/stddev/distribution graph/...

        slice.boxplot(by='Register', column=['Response_Time'], grid=False)

#######################################################
# Interleave it reads with 0x99 requests.
#######################################################
    def itAnd99Read(self, iterations = 1):
        i = 0        
        self._initTest()
        self.it.setpassword()
        while (iterations > 0):
            self.randomRead(supportedOnly=1)
            self.totalOifTransactions = self.totalOifTransactions + 1
            self.it.readx99()
            self.totalMzTransactions = self.totalMzTransactions + 1
            iterations = iterations - 1
            i = i + 1            
            if (i%500 == 0):
                sys.stdout.write('.')
            if (i%(500*100) == 0):
                print ' ', i            # Every 100 dots (50,000 iterations)-print count and newline.
        self.showTest(0)

#######################################################
# Rapid succession of laser on/off.
#######################################################
    def laserEnabDisab(self, iterations = 1, poll99 = 0,):
        self._initTest()
        self.it.setpassword()
        self.getMaxChannel()
        self.it.resena(1)
        senaRead = self.it.resena()[1].fieldSena()
        cycles = 0
        state = 'None'
        time.sleep(1.00)
        self.it.resena(1)

        while (iterations > 0 and state != 'TUNER_IDLE' and senaRead.value() == 1):
            self.it.channel(random.randrange(1,self.maxchan,1))
            self.it.resena(0)
            self.it.resena(1)
            senaRead = self.it.resena()[1].fieldSena()

            if(poll99>1):
                endT = time.time() + .03
                while  time.time() < endT:
                    self.it.readx99()
            else:
                time.sleep(.03)
                
            state = self.it.readx99().tunerstate
            cycles = cycles + 1        
            iterations = iterations - 1
        
        self.showTest(cycles)
        if (state == 'TUNER_IDLE'):
            print '=======Tuner stuck in IDLE========'
        
    def clearStatusAlarmLatches(self):
        self.it.statusF(1,1,1,1,1,1,1,1)
        self.it.statusW(1,1,1,1,1,1,1,1)
        return(2)

    def anyAlarmsPresent(self):
        Fat = self.it.statusF()[1]
        War = self.it.statusW()[1]
        retVal = (Fat.data()+War.data()) != 0 
        return (retVal)
        
#######################################################
# Normal tunes -looking for alarms.
#######################################################
    def tuneAndSpuriousAlarms(self, iterations = 1, poll99 = 0, verbose = 0):
        self._initTest()
        alarm = False
        self.it.mcb(adt=0)
        if(poll99 != 0):
            self.it.setpassword()
        self.totalOifTransactions = self.totalOifTransactions + self.clearStatusAlarmLatches()
        
        while (iterations > 0):
            waitReads = 0
            self.totalOifTransactions = self.totalOifTransactions + self.tuneAndRandomReads(log99 = poll99, verbose = 0)
            if (verbose > 1):
                print 'Tune Finished'
            self.totalOifTransactions = self.totalOifTransactions + self.clearStatusAlarmLatches()
            endTime = datetime.datetime.now() + timedelta(seconds = 5)
            while (datetime.datetime.now() < endTime):
                self.randomRead(supportedOnly=1)
                waitReads = waitReads + 1
            self.totalOifTransactions = self.totalOifTransactions + waitReads
            if (verbose >1):
                print 'Alarm Montior period done'
            if(self.anyAlarmsPresent() == True):
                alarm = True
                iterations = 0
            else:
                iterations = iterations - 1
            if(verbose>0):
                print'*',                     
        if(alarm == True):
            print('Unexpected Alarm')
        else:
            print ('Test completed -No Alarms')
        self.showTest(0)

#######################################################
# Rostam tune and spurious alarms after pending clear.
#######################################################
    def rostamSpecial(self, iterations = 1, poll99 = 0, verbose = 0):
        self._initTest()
        self.it.mcb(adt=1)
        if(poll99 != 0):
            self.it.setpassword()
        while (iterations > 0):
            self.totalOifTransactions = self.totalOifTransactions + self.tuneAndRandomReads(log99 = poll99, verbose = verbose)
            time.sleep(random.uniform(3.0,5.0))   # Sleep 3-5 seconds.
            self.totalOifTransactions = self.totalOifTransactions + self.clearStatusAlarmLatches()
            if(self.anyAlarmsPresent() == True):
                print ('Alarm not cleared! Run: ', iterations)
                iterations = 0
        self.showTest(0)

#######################################################
# Rostam status register missing OIF latch clear request.
#######################################################
    def rostamNoClearStatusW(self, iterations = 1, verbose = 1):
        self.totalOifTransactions = 0
        TO_count = 0 
        timeoutSec = 45
        timeouts = []
        self._initTest()
        self.it.setpassword()
        self.it.mcb(adt=1)
        while (iterations > 0):
            iterations = iterations - 1
            self.totalOifTransactions = self.totalOifTransactions + self.startRandomTune(verbose)
            startT = time.time()
            endT = startT + timeoutSec
            while self.it.nop()[1].fieldPending().value() != 0 and time.time() < endT:
                self.totalOifTransactions = self.totalOifTransactions + 1
            sleepyTime = random.uniform(2.6,3.0)
            time.sleep(sleepyTime)   
            self.it.statusW(1,1,1,1,1,1,1,1)
            self.totalOifTransactions = self.totalOifTransactions + 1
            time.sleep(.25)   
            if(self.it.statusW()[1].data() != 0):
                print 'Status not cleared!'
                print 'Pause Time: ', sleepyTime
                TO_count = TO_count + 1
                timeouts.append(sleepyTime)
                print self.it.statusW()
                print self.it.readAlarmTriggerLog()
            
        self.showTest(0)
        print 'Number of Timeouts: ', TO_count
        print 'Time List', timeouts
        
#######################################################
# Mike -stack tune/ftf/VOA.  Look for pending bit never clear.
#######################################################
    def stackedPwrVoaFtf(self, iterations =1, verbose = 1):
        self.it.resena(0)
        time.sleep(.25)   
        self.totalOifTransactions = self.totalOifTransactions + self.setVoaRange(100)
        self.totalOifTransactions = self.totalOifTransactions + self.setFtfRange(100)
        while (iterations > 0):
            iterations = iterations - 1
            self.currentFtf = random.randrange(self.ftfSetMin, self.ftfSetMax, 1)
            self.currentVoa = random.randrange(self.voaSetMin, self.voaSetMax, 1)
            self.totalOifTransactions = self.totalOifTransactions + self.startRandomTune(verbose,powerCycleProb = 100)
            self.it.ftf(self.currentFtf)
            self.it.pwr(self.currentVoa)
            self.totalOifTransactions = self.totalOifTransactions + 2
            self.totalOifTransactions = self.totalOifTransactions + self.waitLockAndRandomReads(log99=1, timeoutSec = 150)
            if(self.it.nop()[1].fieldPending().value() != 0):
                iterations = 0
                print('Pending not de-asserting')
                print self.it.nop()
                print self.it.readx99()

    def mikePending(self, iterations = 1, verbose = 1):
        self._initTest()
        self.totalOifTransactions = 0
        self.stackedPwrVoaFtf(iterations, verbose)
        self.showTest(0)
        
    def mikePendingExtended(self,iterations = 1, verbose = 1):
        self._initTest()
        self.totalOifTransactions = 0
        runCount = 0
        self.it.resena(0)
        time.sleep(.25)   
        self.totalOifTransactions = self.totalOifTransactions + self.setVoaRange(100)
        self.totalOifTransactions = self.totalOifTransactions + self.setFtfRange(100)
        self.totalOifTransactions = self.totalOifTransactions + self.getMaxChannel()
        pwr = self.it.pwr()[1]
        while (iterations > 0):
            iterations = iterations - 1
            runCount = runCount + 1
            self.currentFtf = random.randrange(self.ftfSetMin, self.ftfSetMax, 1)
            self.currentVoa = random.randrange(self.voaSetMin, self.voaSetMax, 1)
            self.totalOifTransactions = self.totalOifTransactions + self.startRandomTune(verbose,powerCycleProb = 100)
            self.it.ftf(self.currentFtf)
            self.it.pwr(self.currentVoa)
        
            time.sleep(10)
            
            self.it.ftf(0)
            self.it.pwr(pwr)
            self.it.resena(0)
            
            time.sleep(1)   # ?????????
            
            self.it.resena(1)
            time.sleep(15)
            self.it.mcb(adt=1)
            self.it.channel(random.randrange(1,self.maxchan,1))
            self.it.resena(0)
            if(verbose>=1):
                print 'Next channel + laser off'
                
            time.sleep(10)
            
            self.clearStatusAlarmLatches()
            self.it.resena(1)
            self.totalOifTransactions = self.totalOifTransactions + 11
            self.totalOifTransactions = self.totalOifTransactions + self.waitLockAndRandomReads(log99=1, timeoutSec = 45)
            if(self.it.nop()[1].fieldPending().value() != 0):
                iterations = 0
                print('Pending not de-asserting')
                print self.it.nop()
                self.it.setpassword()
                print self.it.readx99()
        print 'Total Tests Run:', runCount
        self.showTest(0)
