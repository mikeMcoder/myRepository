import time
import sys
import os
import pandas
import Tkinter
import tkMessageBox


sys.path.append(os.path.abspath('.'))
sys.path.sort()

if sys.platform == 'cygwin':
    # for cygwin, use the packages installed from the windows installation of python
    sys.path.append('/cygdrive/c/Python27/Lib/site-packages/')

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
t.save_it_obj(it)

print 'Instantiated a TTX interface as t, ITLA as it.'


_PORT = 1
_BAUD = 9600

class PendingBitTest:
    
    def __init__(self):
        self.it = it
        self.logfilename1 = "CheckThePendingBitCase1.txt"
        self.logfilename2 = "CheckThePendingBitCase2.txt"
        self.logfilename3 = "CheckThePendingBitCase3.txt"
        self.logfilename4 = "CheckThePendingBitCase4.txt"
        self.logfilename5 = "CheckThePendingBitCase5.txt"
        self.logfilename6 = "CheckThePendingBitCase6.txt"
        self.logfilename7 = "CheckThePendingBitCase7.txt"
        self.logfilename8 = "CheckThePendingBitCase8.txt"
        self.logfilename9 = "CheckThePendingBitCase9.txt"
        self.logfilename10 = "CheckThePendingBitCase10.txt"
        self.logfilename11 = "CheckThePendingBitCase11.txt"
        self.logfilename12 = "CheckThePendingBitCase12.txt"
        self.logfilename13 = "CheckThePendingBitCase13.txt"
        self.logfilename14 = "CheckThePendingBitCase14.txt"
        self.logfilename15 = "CheckThePendingBitCase15.txt"
        self.logfilename16 = "CheckThePendingBitCase16.txt"
        self.logfilename17 = "CheckThePendingBitCase17.txt"
        self.logfilename18 = "CheckThePendingBitCase18.txt"
        self.channelList = [1 , 52 , 93]
        self.powerList = [1300,1400,1600]
        self.ftfList = [3000,2000,6000]
        self.startTime = 0.0
        self.lapseTime = 0.0
        self.tunerstate = None
        self.tunerstateTarget = 'TUNER_CHANNEL_LOCK'
        self.timeout = 60.0
        self.statusF = None
        self.statusW = None
        self.oop = None
        self.pending = None
        self.ftf = None
        self.stateMachine = None
        self.lf = None
        self.timeout = 180.0

    
        
    def runpendingtestCase1(self):
        ''' change to low mid and high channels, while changing, monitor pending bit, oop, ls, statemachine this is just channel switching\
        measure the pending time'''
        self.it.connect(_PORT,_BAUD)       #connect
        self.it.logging(True)
        self.it.logfile(self.logfilename1)  #enable logging
        self.it.setpassword()              #x99 enabled
        for x in self.channelList:
            try:
                self.it.resena(0)              #laser off 
                time.sleep(1)
                self.it.channel(x)                        #channel
                print "==>Tune to channel:%d"%x  #print channel number
                self.it.pwr()                   #read voa
                self.it.ftf()                   #ftf read
                self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
                self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
                self.it.resena(1)              #turn on laser
                print self.it.resena()         #print reg#32        
                print "==>Turn on the laser"
            except:
                raise "Error"

            #print data until channel locks
            self.startTime = time.time()        #starttime
            self.lapseTime = time.time() -  self.startTime  #lapse time count
            self.tunerstate = self.it.readx99().tunerstate #state machine at the moment
            while self.tunerstate != self.tunerstateTarget:
                self.statusF = bin(int(self.it.statusF()[1].data()))
                self.statusW = bin(int(self.it.statusW()[1].data()))
                self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                self.lf = self.it.lf()[1]
                self.oop = self.it.oop()[1]
                self.ftf = self.it.ftf()[1]
                self.tunerstate = self.it.readx99().tunerstate
                print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                self.lapseTime = time.time() -  self.startTime  #keep counting time
                if self.lapseTime >= self.timeout:
                    print "The unit cannot tune please check the unit"
                    self.it.disconnect()
        print("Test Complete")
        self.it.resena(mr=1)                #reset everything
        self.it.disconnect()                #close communication

    def runpendingtestCase2(self):
        ''' tune to a channel and set power at the same time, wait until channel lock state'''
        self.it.connect(_PORT,_BAUD)       #connect
        self.it.logging(True)
        self.it.logfile(self.logfilename2)  #enable logging
        self.it.setpassword()              #x99 enabled
        for x,y in zip(self.channelList, self.powerList):
            try:
                self.it.resena(0)              #laser off 
                time.sleep(1)
                self.it.channel(x)                        #channel
                time.sleep(0.2)
                print "==>Tune to channel:%d"%x  #print channel number
                print "==>Set Power to :%d"%y    #print power level 
                self.it.pwr(y)                   #set voa
                self.it.ftf()                   #ftf read
                self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
                self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
                self.it.resena(1)              #turn on laser
                print self.it.resena()         #print reg#32        
                print "==>Turn on the laser"
            except:
                raise "Error"

            #print data until channel locks
            self.startTime = time.time()        #starttime
            self.lapseTime = time.time() -  self.startTime  #lapse time count
            self.tunerstate = self.it.readx99().tunerstate #state machine at the moment
            while self.tunerstate != self.tunerstateTarget:
                self.statusF = bin(int(self.it.statusF()[1].data()))
                self.statusW = bin(int(self.it.statusW()[1].data()))
                self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                self.lf = self.it.lf()[1]
                self.oop = self.it.oop()[1]
                self.ftf = self.it.ftf()[1]
                self.tunerstate = self.it.readx99().tunerstate
                print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                self.lapseTime = time.time() -  self.startTime  #keep counting time
                if self.lapseTime >= self.timeout:
                    print "The unit cannot tune please check the unit"
                    self.it.disconnect()
        print("Test Complete")
        self.it.disconnect()                #close communication

    def waitforChannellock(self,timeLimit = 0):
        self.timeLimit = timeLimit
        self.startTime = time.time() #start log of time
        self.lapseTime = time.time() -  self.startTime 
        while 1: #while true
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(0.5)
            self.stateMachine = self.it.readx99().tunerstate
            self.lapseTime = time.time() -  self.startTime 
            if self.stateMachine is "TUNER_CHANNEL_LOCK":
                print("Channel lock reached")
                break;
            elif self.lapseTime >=  self.timeLimit:
                try:
                    print("Cannot Reach Channel Lock")
                    self.it.disconnect()
                    break
                except:
                    raise "Error"
        return self.lapseTime
            

    def runpendingtestCase3(self):
            ''' tune to a channel wait for channel lock and set power wait until the pendingbit clears'''
            self.it.connect(_PORT,_BAUD)       #connect
            self.it.logging(True)
            self.it.logfile(self.logfilename3)  #enable logging
            self.it.setpassword()              #x99 enabled
            for x,y in zip(self.channelList, self.powerList):
                try:
                    self.it.resena(0)              #laser off 
                    time.sleep(1)
                    self.it.channel(x)                        #channel
                    time.sleep(0.2)
                    print "==>Tune to channel:%d"%x  #print channel number
                    self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
                    self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
                    self.it.resena(1)              #turn on laser
                    self.waitforChannellock(60)#wait for channellock
                    print "==>Set Power to :%d"%y    #print power level 
                    self.it.pwr(y)                   #set voa
                    self.it.ftf()                   #ftf read
                    print self.it.resena()         #print reg#32        
                    print "==>Turn on the laser"
                except:
                    raise "Error"

                self.startTime = time.time()        #starttime
                self.lapseTime = time.time() -  self.startTime  #lapse time count
                self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                
                while 1 :
                    try:
                        
                        self.statusF = bin(int(self.it.statusF()[1].data()))
                        self.statusW = bin(int(self.it.statusW()[1].data()))
                        self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                        self.lf = self.it.lf()[1]
                        self.oop = self.it.oop()[1]
                        self.ftf = self.it.ftf()[1]
                        self.tunerstate = self.it.readx99().tunerstate
                        self.lapseTime = time.time() -  self.startTime  #keep counting time
                        print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                        if self.pending =='00000000':
                            print("PendingBit Cleared!")
                            break
                            
                        elif self.lapseTime >= self.timeout:
                            print "The unit cannot tune please check the unit"
                            self.it.disconnect()
                        time.sleep(.5)
                    except:
                        raise "Error"
                
                     
            print("Test Complete")
            self.it.disconnect()                #close communication




    def runpendingtestCase4(self):
        ''' tune to a channel and set ftf at the same time, wait until channel lock state'''
        self.it.connect(_PORT,_BAUD)       #connect
        self.it.logging(True)
        self.it.logfile(self.logfilename4)  #enable logging
        self.it.setpassword()              #x99 enabled
        for x,y in zip(self.channelList, self.ftfList):
            try:
                self.it.resena(0)              #laser off 
                time.sleep(1)
                self.it.channel(x)                        #channel
                time.sleep(2)
                print "==>Tune to channel:%d"%x  #print channel number
                print "==>Set ftf to :%d"%y    #print ftf level 
                self.it.pwr()                   #read voa
                self.it.ftf(y)                   #ftf set
                self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
                self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
                self.it.resena(1)              #turn on laser
                print self.it.resena()         #print reg#32        
                print "==>Turn on the laser"
            except:
                raise "Error"

            #print data until channel locks
            self.startTime = time.time()        #starttime
            self.lapseTime = time.time() -  self.startTime  #lapse time count
            self.tunerstate = self.it.readx99().tunerstate #state machine at the moment
            while self.tunerstate != self.tunerstateTarget:
                self.statusF = bin(int(self.it.statusF()[1].data()))
                self.statusW = bin(int(self.it.statusW()[1].data()))
                self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                self.lf = self.it.lf()[1]
                self.oop = self.it.oop()[1]
                self.ftf = self.it.ftf()[1]
                self.tunerstate = self.it.readx99().tunerstate
                print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                self.lapseTime = time.time() -  self.startTime  #keep counting time
                if self.lapseTime >= self.timeout:
                    print "The unit cannot tune please check the unit"
                    self.it.disconnect()
        print("Test Complete")
        self.it.disconnect()                #close communication




    def runpendingtestCase5(self):
            ''' tune to a channel wait for channel lock and set ftf wait until the pendingbit clears'''
            self.it.connect(_PORT,_BAUD)       #connect
            self.it.logging(True)
            self.it.logfile(self.logfilename5)  #enable logging
            self.it.setpassword()              #x99 enabled
            for x,y in zip(self.channelList, self.ftfList):
                try:
                    self.it.resena(0)              #laser off 
                    time.sleep(1)
                    self.it.channel(x)                        #channel
                    time.sleep(0.2)
                    print "==>Tune to channel:%d"%x  #print channel number
                    self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
                    self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
                    self.it.resena(1)                #turn on laser
                    self.waitforChannellock(60)      #wait for channellock
                    print "==>Set Power to :%d"%y    #print power level 
                    self.it.pwr()                    #read voa
                    self.it.ftf(y)                   #set ftf 
                    print self.it.resena()          #print reg#32        
                    print "==>Turn on the laser"
                except:
                    raise "Error"

                self.startTime = time.time()        #starttime
                self.lapseTime = time.time() -  self.startTime  #lapse time count
                self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                
                while 1 :
                    try:
                        
                        self.statusF = bin(int(self.it.statusF()[1].data()))
                        self.statusW = bin(int(self.it.statusW()[1].data()))
                        self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                        self.lf = self.it.lf()[1]
                        self.oop = self.it.oop()[1]
                        self.ftf = self.it.ftf()[1]
                        self.tunerstate = self.it.readx99().tunerstate
                        self.lapseTime = time.time() -  self.startTime  #keep counting time
                        print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                        if self.pending =='00000000':
                            print("PendingBit Cleared!")
                            break
                            
                        elif self.lapseTime >= self.timeout:
                            print "The unit cannot tune please check the unit"
                            self.it.disconnect()
                        time.sleep(.5)
                        
                    except Exception as e:
                        print e.message
                
                     
            print("Test Complete")
            self.it.disconnect()                #close communication




    def runpendingtestCase6(self):
        ''' tune to a channel and set ftf  and set power at the same time, wait until channel lock state'''
        self.it.connect(_PORT,_BAUD)       #connect
        self.it.logging(True)
        self.it.logfile(self.logfilename6)  #enable logging
        self.it.setpassword()              #x99 enabled
        for x,y,z in zip(self.channelList,self.powerList, self.ftfList):
            try:
                self.it.resena(0)              #laser off 
                time.sleep(1)
                self.it.channel(x)                        #channel
                print self.it.channel()
                time.sleep(1)
                print "==>Tune to channel:%d"%x  #print channel number
                print "==>Set pwr to :%d"%y    #print ftf level
                print "==>Set ftf to :%d"%z    #print ftf level 
                self.it.pwr(y)                   #read voa
                print self.it.pwr()
                self.it.ftf(z)                   #ftf set
                time.sleep(1)
                print self.it.ftf()
                time.sleep(1)
                self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
                self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
                self.it.resena(1)              #turn on laser
                print self.it.resena()         #print reg#32        
                print "==>Turn on the laser"
            except Exception as e:
                print e.message

            #print data until channel locks
            self.startTime = time.time()        #starttime
            self.lapseTime = time.time() -  self.startTime  #lapse time count
            self.tunerstate = self.it.readx99().tunerstate #state machine at the moment
            while self.tunerstate != self.tunerstateTarget:
                self.statusF = bin(int(self.it.statusF()[1].data()))
                self.statusW = bin(int(self.it.statusW()[1].data()))
                self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                self.lf = self.it.lf()[1]
                self.oop = self.it.oop()[1]
                self.ftf = self.it.ftf()[1]
                self.tunerstate = self.it.readx99().tunerstate
                print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                self.lapseTime = time.time() -  self.startTime  #keep counting time
                if self.lapseTime >= self.timeout:
                    print "The unit cannot tune please check the unit"
                    self.it.disconnect()
        print("Test Complete")
        self.it.disconnect()                #close communication



    def runpendingtestCase7(self):
            ''' tune to a channel wait for channel lock and set ftf , set voa, set channel and wait until the pendingbit clears'''
            self.it.connect(_PORT,_BAUD)       #connect
            self.it.logging(True)
            self.it.logfile(self.logfilename7)  #enable logging
            self.it.setpassword()              #x99 enabled
            for x,y,z in zip(self.channelList,self.powerList, self.ftfList):
                try:
                    self.it.resena(0)              #laser off 
                    self.it.channel(50)                        #channel
                    time.sleep(0.2)
                    print "==>Tune to channel:50"  #print channel number
                    self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
                    self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
                    self.it.resena(1)                #turn on laser
                    self.waitforChannellock(60)      #wait for channellock
                    print "==>Tune to channel:%d"%x  #print channel number
                    self.it.channel(x)
                    print "==>Set Power to :%d"%y    #print power level 
                    self.it.pwr(y)                    #set voa
                    print "==>Set ftf to :%d"%z      #print ftf setting 
                    self.it.ftf(y)                   #set ftf 
                    print self.it.resena()          #print reg#32        
                    print "==>Turn on the laser"
                except Exception as e:
                    print e.message
                

                self.startTime = time.time()        #starttime
                self.lapseTime = time.time() -  self.startTime  #lapse time count
                self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                
                while 1 :
                    try:
                        
                        self.statusF = bin(int(self.it.statusF()[1].data()))
                        self.statusW = bin(int(self.it.statusW()[1].data()))
                        self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                        self.lf = self.it.lf()[1]
                        self.oop = self.it.oop()[1]
                        self.ftf = self.it.ftf()[1]
                        self.tunerstate = self.it.readx99().tunerstate
                        self.lapseTime = time.time() -  self.startTime  #keep counting time
                        print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                        if self.pending =='00000000':
                            print("PendingBit Cleared!")
                            break
                            
                        elif self.lapseTime >= self.timeout:
                            print "The unit cannot tune please check the unit"
                            self.it.disconnect()
                        time.sleep(.5)
                        
                    except Exception as e:
                        print e.message
                
                     
            print("Test Complete")
            self.it.disconnect()                #close communication



    def runpendingtestCase8(self):
            ''' tune to a channel wait for channel lock and set ftf , set voa, set channel and after 5 secs turn laser off'''
            self.it.connect(_PORT,_BAUD)       #connect
            self.it.logging(True)
            self.it.logfile(self.logfilename8)  #enable logging
            self.it.setpassword()              #x99 enabled
            for x,y,z in zip(self.channelList,self.powerList, self.ftfList):
                try:
                    self.it.resena(0)              #laser off 
                    self.it.channel(50)                        #channel
                    time.sleep(0.2)
                    print "==>Tune to channel:50"  #print channel number
                    self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
                    self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
                    self.it.resena(1)                #turn on laser
                    self.waitforChannellock(60)      #wait for channellock
                    print "==>Tune to channel:%d"%x  #print channel number
                    self.it.channel(x)
                    print "==>Set Power to :%d"%y    #print power level 
                    self.it.pwr(y)                    #set voa
                    print "==>Set ftf to :%d"%z      #print ftf setting 
                    self.it.ftf(y)                   #set ftf 
                    print self.it.resena()          #print reg#32        
                    print "==>Turn on the laser"
                except Exception as e:
                    print e.message
                

                self.startTime = time.time()        #starttime
                self.lapseTime = time.time() -  self.startTime #lapse time count
                self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                
                while 1 :
                    try:
                        
                        self.statusF = bin(int(self.it.statusF()[1].data()))
                        self.statusW = bin(int(self.it.statusW()[1].data()))
                        self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                        self.lf = self.it.lf()[1]
                        self.oop = self.it.oop()[1]
                        self.ftf = self.it.ftf()[1]
                        self.tunerstate = self.it.readx99().tunerstate
                        self.lapseTime = time.time() -  self.startTime  #keep counting time
                        print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                        
                        if self.lapseTime >= 5.0: #After 5 secs, turn off laser
                            print("==>Turn laser off...")
                            self.it.resena(0)
                            for rep in range(5): #print 5 times
                                self.statusF = bin(int(self.it.statusF()[1].data()))
                                self.statusW = bin(int(self.it.statusW()[1].data()))
                                self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                                self.lf = self.it.lf()[1]
                                self.oop = self.it.oop()[1]
                                self.ftf = self.it.ftf()[1]
                                self.tunerstate = self.it.readx99().tunerstate
                                self.lapseTime = time.time() -  self.startTime #keep counting time
                                print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                            break
                                
                        if self.pending =='00000000':
                            print("PendingBit Cleared!")
                            break
                            
                        elif self.lapseTime >= self.timeout:
                            print "The unit cannot tune please check the unit"
                            self.it.disconnect()
                        time.sleep(.5)
                        
                    except Exception as e:
                        print e.message
                
                     
            print("Test Complete")
            self.it.disconnect()                #close communication


    def runpendingtestCase9(self):
        ''' while laser is off, set channel, check nop'''
        self.it.connect(_PORT,_BAUD)       #connect
        self.it.logging(True)
        self.it.logfile(self.logfilename9)  #enable logging
        self.it.setpassword()              #x99 enabled
    
        try:
           
            self.it.resena(0)              #laser off 
            self.it.channel(50)            #channel
            time.sleep(0.2)
            print "==>Tune to channel:50"  #print channel number
            self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
            self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
            self.statusF = bin(int(self.it.statusF()[1].data()))
            self.statusW = bin(int(self.it.statusW()[1].data()))
            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
            self.lf = self.it.lf()[1]
            self.oop = self.it.oop()[1]
            self.ftf = self.it.ftf()[1]
            self.tunerstate = self.it.readx99().tunerstate
            self.lapseTime = time.time() -  self.startTime  #keep counting time
            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
            self.it.channel(90)            #channel
            time.sleep(0.2)
            print "==>Tune to channel:90"  #print channel number
            self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
            self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
            self.statusF = bin(int(self.it.statusF()[1].data()))
            self.statusW = bin(int(self.it.statusW()[1].data()))
            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
            self.lf = self.it.lf()[1]
            self.oop = self.it.oop()[1]
            self.ftf = self.it.ftf()[1]
            self.tunerstate = self.it.readx99().tunerstate
            self.lapseTime = time.time() -  self.startTime  #keep counting time
            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
            self.it.channel(10)            #channel
            time.sleep(0.2)
            print "==>Tune to channel:10"  #print channel number
            self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
            self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
            self.statusF = bin(int(self.it.statusF()[1].data()))
            self.statusW = bin(int(self.it.statusW()[1].data()))
            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
            self.lf = self.it.lf()[1]
            self.oop = self.it.oop()[1]
            self.ftf = self.it.ftf()[1]
            self.tunerstate = self.it.readx99().tunerstate
            self.lapseTime = time.time() -  self.startTime  #keep counting time
            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters

        
        except Exception as e:
            print e.message

             
        print("Test Complete")
        self.it.disconnect()                #close communication





    def runpendingtestCase10(self):
        ''' while laser is off, set voa, check nop'''
        self.it.connect(_PORT,_BAUD)       #connect
        self.it.logging(True)
        self.it.logfile(self.logfilename10)  #enable logging
        self.it.setpassword()              #x99 enabled
    
        try:
           
            self.it.resena(0)              #laser off 
            self.it.pwr(1550)            #setpower
            time.sleep(0.2)
            print "==>Change Power to 1550"  #print power level
            self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
            self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
            self.statusF = bin(int(self.it.statusF()[1].data()))
            self.statusW = bin(int(self.it.statusW()[1].data()))
            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
            self.lf = self.it.lf()[1]
            self.oop = self.it.oop()[1]
            self.ftf = self.it.ftf()[1]
            self.tunerstate = self.it.readx99().tunerstate
            self.lapseTime = time.time() -  self.startTime  #keep counting time
            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
            self.it.pwr(1050)            #setpower
            time.sleep(0.2)
            print "==>Change Power to 1050"  #print power level
            self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
            self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
            self.statusF = bin(int(self.it.statusF()[1].data()))
            self.statusW = bin(int(self.it.statusW()[1].data()))
            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
            self.lf = self.it.lf()[1]
            self.oop = self.it.oop()[1]
            self.ftf = self.it.ftf()[1]
            self.tunerstate = self.it.readx99().tunerstate
            self.lapseTime = time.time() -  self.startTime  #keep counting time
            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
            self.it.pwr(1450)            #setpower
            time.sleep(0.2)
            print "==>Change Power to 1450"  #print power level
            self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
            self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
            self.statusF = bin(int(self.it.statusF()[1].data()))
            self.statusW = bin(int(self.it.statusW()[1].data()))
            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
            self.lf = self.it.lf()[1]
            self.oop = self.it.oop()[1]
            self.ftf = self.it.ftf()[1]
            self.tunerstate = self.it.readx99().tunerstate
            self.lapseTime = time.time() -  self.startTime  #keep counting time
            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters

        
        except Exception as e:
            print e.message

             
        print("Test Complete")
        self.it.disconnect()                #close communication

        

    def runpendingtestCase11(self):
        ''' while laser is off, set ftf, check nop'''
        self.it.connect(_PORT,_BAUD)       #connect
        self.it.logging(True)
        self.it.logfile(self.logfilename11)  #enable logging
        self.it.setpassword()              #x99 enabled
    
        try:
           
            self.it.resena(0)              #laser off 
            self.it.ftf(5000)              #set ftf
            time.sleep(0.2)
            print "==>Change ftf to 5000"  #print ftf
            self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
            self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
            self.statusF = bin(int(self.it.statusF()[1].data()))
            self.statusW = bin(int(self.it.statusW()[1].data()))
            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
            self.lf = self.it.lf()[1]
            self.oop = self.it.oop()[1]
            self.ftf = self.it.ftf()[1]
            self.tunerstate = self.it.readx99().tunerstate
            self.lapseTime = time.time() -  self.startTime  #keep counting time
            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
            self.it.ftf(-3000)              #set ftf
            time.sleep(0.2)
            print "==>Change ftf to -3000"  #print ftf
            self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
            self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
            self.statusF = bin(int(self.it.statusF()[1].data()))
            self.statusW = bin(int(self.it.statusW()[1].data()))
            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
            self.lf = self.it.lf()[1]
            self.oop = self.it.oop()[1]
            self.ftf = self.it.ftf()[1]
            self.tunerstate = self.it.readx99().tunerstate
            self.lapseTime = time.time() -  self.startTime  #keep counting time
            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
            self.it.ftf(2000)              #set ftf
            time.sleep(0.2)
            print "==>Change ftf to 2000"  #print ftf
            self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
            self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
            self.statusF = bin(int(self.it.statusF()[1].data()))
            self.statusW = bin(int(self.it.statusW()[1].data()))
            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
            self.lf = self.it.lf()[1]
            self.oop = self.it.oop()[1]
            self.ftf = self.it.ftf()[1]
            self.tunerstate = self.it.readx99().tunerstate
            self.lapseTime = time.time() -  self.startTime  #keep counting time
            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters

        
        except Exception as e:
            print e.message

             
        print("Test Complete")
        self.it.disconnect()                #close communication






    def runpendingtestCase12(self):
    
        ''' tune to a channel wait for channel lock and set ftf , set voa, set channel and after 5 secs trigger huawei soft reset'''
        self.it.connect(_PORT,_BAUD)       #connect
        self.it.logging(True)
        self.it.logfile(self.logfilename12)  #enable logging
        self.it.setpassword()              #x99 enabled
        for x,y,z in zip(self.channelList,self.powerList, self.ftfList):
            try:
                self.it.resena(0)              #laser off 
                self.it.channel(50)                        #channel 50 as default
                time.sleep(0.2)
                print "==>Tune to channel:50"  #print channel number
                self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
                self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
                self.it.resena(1)                #turn on laser
                self.waitforChannellock(60)      #wait for channellock
                print "==>Tune to channel:%d"%x  #print channel number
                self.it.channel(x)
                print "==>Set Power to :%d"%y    #print power level 
                self.it.pwr(y)                    #set voa
                print "==>Set ftf to :%d"%z      #print ftf setting 
                self.it.ftf(z)                   #set ftf 
                print self.it.resena()          #print reg#32        
                print "==>Turn on the laser"
            except Exception as e:
                print e.message
            

            self.startTime = time.time()        #starttime
            self.lapseTime = time.time() -  self.startTime #lapse time count
            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
            
            while 1 :
                try:
                    
                    self.statusF = bin(int(self.it.statusF()[1].data()))
                    self.statusW = bin(int(self.it.statusW()[1].data()))
                    self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                    self.lf = self.it.lf()[1]
                    self.oop = self.it.oop()[1]
                    self.ftf = self.it.ftf()[1]
                    self.tunerstate = self.it.readx99().tunerstate
                    self.lapseTime = time.time() -  self.startTime  #keep counting time
                    print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                    
                    if self.lapseTime >= 5.0: #After 5 secs, turn off laser
                        print("==>Trigger Soft Reset...")
                        self.it.resena(sena = 1, sr = 1) # trigger Huawei soft reset
                        for rep in range(5): #print 5 times
                            self.statusF = bin(int(self.it.statusF()[1].data()))
                            self.statusW = bin(int(self.it.statusW()[1].data()))
                            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                            self.lf = self.it.lf()[1]
                            self.oop = self.it.oop()[1]
                            self.ftf = self.it.ftf()[1]
                            self.tunerstate = self.it.readx99().tunerstate
                            self.lapseTime = time.time() -  self.startTime #keep counting time
                            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                        break
                            
                        
                    elif self.lapseTime >= self.timeout:
                        print "The unit cannot tune please check the unit"
                        self.it.disconnect()
                    time.sleep(.5)
                    
                except Exception as e:
                    print e.message
            
                 
        print("Test Complete")
        self.it.disconnect()                #close communication



    def runpendingtestCase13(self):
    
        ''' tune to a channel wait for channel lock and set ftf , set voa, set channel and after 5 secs trigger regular soft reset'''
        self.it.connect(_PORT,_BAUD)       #connect
        self.it.logging(True)
        self.it.logfile(self.logfilename13)  #enable logging
        self.it.setpassword()              #x99 enabled
        for x,y,z in zip(self.channelList,self.powerList, self.ftfList):
            try:
                self.it.setpassword()
                self.it.resena(0)              #laser off 
                self.it.channel(50)                        #channel 50 as default
                time.sleep(0.2)
                print "==>Tune to channel:50"  #print channel number
                self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
                self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
                self.it.resena(1)                #turn on laser
                self.waitforChannellock(60)      #wait for channellock
                print "==>Tune to channel:%d"%x  #print channel number
                self.it.channel(x)
                print "==>Set Power to :%d"%y    #print power level 
                self.it.pwr(y)                    #set voa
                print "==>Set ftf to :%d"%z      #print ftf setting 
                self.it.ftf(z)                   #set ftf 
                print self.it.resena()          #print reg#32        
                print "==>Turn on the laser"
            except Exception as e:
                print e.message
            

            self.startTime = time.time()        #starttime
            self.lapseTime = time.time() -  self.startTime #lapse time count
            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
            
            while 1 :
                try:
                    self.it.setpassword()
                    self.statusF = bin(int(self.it.statusF()[1].data()))
                    self.statusW = bin(int(self.it.statusW()[1].data()))
                    self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                    self.lf = self.it.lf()[1]
                    self.oop = self.it.oop()[1]
                    self.ftf = self.it.ftf()[1]
                    self.tunerstate = self.it.readx99().tunerstate
                    self.lapseTime = time.time() -  self.startTime  #keep counting time
                    print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                    
                    if self.lapseTime >= 5.0: #After 5 secs,trigger soft reset
                        print("==>Trigger Soft Reset...")
                        self.it.resena(sr = 1) # trigger soft reset
                        #time.sleep(3)
                        
                        for rep in range(5): #print 5 times
                          
                            self.statusF = bin(int(self.it.statusF()[1].data()))
                            self.statusW = bin(int(self.it.statusW()[1].data()))
                            self.pending = self.it.nop()[1].fieldPending()
                            a = self.it.nop()
                            self.lf = self.it.lf()[1]
                            self.oop = self.it.oop()[1]
                            self.ftf = self.it.ftf()[1]
                            self.it.setpassword()
                            self.tunerstate = self.it.readx99().tunerstate
                            self.lapseTime = time.time() -  self.startTime #keep counting time
                            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters

                        break
                            
                        
                    elif self.lapseTime >= self.timeout:
                        print "The unit cannot tune please check the unit"
                        self.it.disconnect()
                    time.sleep(.5)
                    
                except Exception as e:
                    print e.message
                    self.it.flushBuffer()
                    pass
            
                 
        print("Test Complete")
        self.it.disconnect()                #close communication



    def runpendingtestCase14(self):
    
        ''' while laser off, set to channel, turn on laser, monitor nop after 5 sec trigger main reset'''
        self.it.connect(_PORT,_BAUD)       #connect
        self.it.logging(True)
        self.it.logfile(self.logfilename14)  #enable logging
        self.it.setpassword()              #x99 enabled
        for x,y,z in zip(self.channelList,self.powerList, self.ftfList):
            try:
                self.it.resena(0)              #laser off 
                self.it.channel(50)                        #channel 50 as default
                time.sleep(1)
                print "==>Tune to channel:50"  #print channel number
                self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
                self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
                self.it.resena(1)                #turn on laser
                self.waitforChannellock(60)      #wait for channellock
                print "==>Tune to channel:%d"%x  #print channel number
                self.it.channel(x)
                print "==>Set Power to :%d"%y    #print power level 
                self.it.pwr(y)                    #set voa
                print "==>Set ftf to :%d"%z      #print ftf setting 
                self.it.ftf(z)                   #set ftf 
                print self.it.resena()          #print reg#32        
                print "==>Turn on the laser"
            except Exception as e:
                print e.message
            

            self.startTime = time.time()        #starttime
            self.lapseTime = time.time() -  self.startTime #lapse time count
            self.pending = self.it.nop()[1].fieldPending()
            
            while 1 :
                try:
                    
                    self.statusF = bin(int(self.it.statusF()[1].data()))
                    self.statusW = bin(int(self.it.statusW()[1].data()))
                    self.pending = self.it.nop()[1].fieldPending()
                    self.lf = self.it.lf()[1]
                    self.oop = self.it.oop()[1]
                    self.ftf = self.it.ftf()[1]
                    self.tunerstate = self.it.readx99().tunerstate
                    self.lapseTime = time.time() -  self.startTime  #keep counting time
                    print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                    
                    if self.lapseTime >= 5.0: #After 5 secs,trigger main reset
                        print("==>Trigger main Reset...")
                        self.it.resena(mr = 1) # trigger main reset
                        #time.sleep(3)
                        for rep in range(5): #print 5 times
                            self.it.setpassword()
                            self.statusF = bin(int(self.it.statusF()[1].data()))
                            self.statusW = bin(int(self.it.statusW()[1].data()))
                            self.pending = self.it.nop()[1].fieldPending()
                            self.lf = self.it.lf()[1]
                            self.oop = self.it.oop()[1]
                            self.ftf = self.it.ftf()[1]
                            self.tunerstate = self.it.readx99().tunerstate
                            self.lapseTime = time.time() -  self.startTime #keep counting time
                            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                        break
                            
                        
                    elif self.lapseTime >= self.timeout:
                        print "The unit cannot tune please check the unit"
                        self.it.disconnect()
                    time.sleep(.5)
                    
                except Exception as e:
                    print e.message
            
                 
        print("Test Complete")
        self.it.disconnect()                #close communication


    def runpendingtestCase15(self):
        ''' while laser off, set to channel, turn on laser, monitor nop after 5 sec trigger laserdisable'''
        import aa_gpio.gpio                #aimport the gpio module
        g = aa_gpio.gpio.gpio()             #intance of gpio the class
        g.InitPin()                         #initialize the gpio
        self.it.connect(_PORT,_BAUD)       #connect
        self.it.logging(True)
        self.it.logfile(self.logfilename15)  #enable logging
        self.it.setpassword()              #x99 enabled
        for x,y,z in zip(self.channelList,self.powerList, self.ftfList):
            try:
                self.it.resena(0)              #laser off 
                self.it.channel(50)                        #channel 50 as default
                time.sleep(0.2)
                print "==>Tune to channel:50"  #print channel number
                self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
                self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
                self.it.resena(1)                #turn on laser
                self.waitforChannellock(60)      #wait for channellock
                print "==>Tune to channel:%d"%x  #print channel number
                self.it.channel(x)
                print "==>Set Power to :%d"%y    #print power level 
                self.it.pwr(y)                    #set voa
                print "==>Set ftf to :%d"%z      #print ftf setting 
                self.it.ftf(z)                   #set ftf 
                print self.it.resena()          #print reg#32        
                print "==>Turn on the laser"
            except Exception as e:
                print e.message
            

            self.startTime = time.time()        #starttime
            self.lapseTime = time.time() -  self.startTime #lapse time count
            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
            
            while 1 :
                try:
                    
                    self.statusF = bin(int(self.it.statusF()[1].data()))
                    self.statusW = bin(int(self.it.statusW()[1].data()))
                    self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                    self.lf = self.it.lf()[1]
                    self.oop = self.it.oop()[1]
                    self.ftf = self.it.ftf()[1]
                    self.tunerstate = self.it.readx99().tunerstate
                    self.lapseTime = time.time() -  self.startTime  #keep counting time
                    print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                    
                    if self.lapseTime >= 5.0: #After 5 secs,trigger laser disable
                        print("==>Trigger Laser Disable Pin...")
                        g.LDIS_N_Disable() # trigger laser disable
                        #time.sleep(3)
                        for rep in range(5): #print 5 times
                            self.it.setpassword()
                            self.statusF = bin(int(self.it.statusF()[1].data()))
                            self.statusW = bin(int(self.it.statusW()[1].data()))
                            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                            self.lf = self.it.lf()[1]
                            self.oop = self.it.oop()[1]
                            self.ftf = self.it.ftf()[1]
                            self.tunerstate = self.it.readx99().tunerstate
                            self.lapseTime = time.time() -  self.startTime #keep counting time
                            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                        print("==>Trigger Laser Enable Pin...")
                        g.LDIS_N_Enable() # trigger laser Enable
                        for rep in range(5): #print 5 times
                            self.it.setpassword()
                            self.statusF = bin(int(self.it.statusF()[1].data()))
                            self.statusW = bin(int(self.it.statusW()[1].data()))
                            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                            self.lf = self.it.lf()[1]
                            self.oop = self.it.oop()[1]
                            self.ftf = self.it.ftf()[1]
                            self.tunerstate = self.it.readx99().tunerstate
                            self.lapseTime = time.time() -  self.startTime #keep counting time
                            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                        
                        break
                            
                        
                    elif self.lapseTime >= self.timeout:
                        print "The unit cannot tune please check the unit"
                        self.it.disconnect()
                    time.sleep(.5)
                    
                except Exception as e:
                    print e.message
            
                 
        print("Test Complete")
        self.it.disconnect()                #close communication



    def runpendingtestCase16(self):
        ''' while laser off, set to channel, turn on laser, monitor nop after 5 sec trigger hard reset pin'''
        import aa_gpio.gpio                #aimport the gpio module
        g = aa_gpio.gpio.gpio()             #intance of gpio the class
        g.InitPin()                         #initialize the gpio
        self.it.connect(_PORT,_BAUD)       #connect
        self.it.logging(True)
        self.it.logfile(self.logfilename16)  #enable logging
        self.it.setpassword()              #x99 enabled
        for x,y,z in zip(self.channelList,self.powerList, self.ftfList):
            try:
                self.it.resena(0)              #laser off 
                self.it.channel(50)                        #channel 50 as default
                time.sleep(1)
                print "==>Tune to channel:50"  #print channel number
                self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
                self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
                self.it.resena(1)                #turn on laser
                self.waitforChannellock(60)      #wait for channellock
                print "==>Tune to channel:%d"%x  #print channel number
                self.it.channel(x)
                print "==>Set Power to :%d"%y    #print power level 
                self.it.pwr(y)                    #set voa
                print "==>Set ftf to :%d"%z      #print ftf setting 
                self.it.ftf(z)                   #set ftf 
                print self.it.resena()          #print reg#32        
                print "==>Turn on the laser"
            except Exception as e:
                print e.message
            

            self.startTime = time.time()        #starttime
            self.lapseTime = time.time() -  self.startTime #lapse time count
            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
            
            while 1 :
                try:
                    
                    self.statusF = bin(int(self.it.statusF()[1].data()))
                    self.statusW = bin(int(self.it.statusW()[1].data()))
                    self.pending = self.it.nop()[1].fieldPending()
                    self.lf = self.it.lf()[1]
                    self.oop = self.it.oop()[1]
                    self.ftf = self.it.ftf()[1]
                    self.tunerstate = self.it.readx99().tunerstate
                    self.lapseTime = time.time() -  self.startTime  #keep counting time
                    print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                    
                    if self.lapseTime >= 5.0: #After 5 secs,trigger Hard Reset
                        print("==>Trigger Hard Reset...")
                        g.reset(3) # trigger Hard Reset
                        #time.sleep(3)
                        for rep in range(5): #print 5 times
                            self.it.setpassword()
                            self.statusF = bin(int(self.it.statusF()[1].data()))
                            self.statusW = bin(int(self.it.statusW()[1].data()))
                            self.pending = self.it.nop()[1].fieldPending()
                            self.lf = self.it.lf()[1]
                            self.oop = self.it.oop()[1]
                            self.ftf = self.it.ftf()[1]
                            self.tunerstate = self.it.readx99().tunerstate
                            self.lapseTime = time.time() -  self.startTime #keep counting time
                            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                        break
                            
                        
                    elif self.lapseTime >= self.timeout:
                        print "The unit cannot tune please check the unit"
                        self.it.disconnect()
                    time.sleep(.5)
                    
                except Exception as e:
                    print e.message
            
                 
        print("Test Complete")
        self.it.disconnect()                #close communication
        
        
        
        
        
    def runpendingtestCase17(self):
        
        ''' while laser off, set to channel, turn on laser, monitor nop after 5 sec trigger power cycle'''
        import  instrumentDrivers as inst   #import instrumentdrivers
        powersupply = inst.psAG3631('GPIB0::06')#intance of the agilent power supply
        powersupply.connect()                   #connect to power supply
        self.it.connect(_PORT,_BAUD)       #connect
        self.it.logging(True)
        self.it.logfile(self.logfilename17)  #enable logging
        self.it.setpassword()              #x99 enabled
        for x,y,z in zip(self.channelList,self.powerList, self.ftfList):
            try:
                self.it.resena(0)              #laser off 
                self.it.channel(50)                        #channel 50 as default
                time.sleep(1)
                print "==>Tune to channel:50"  #print channel number
                self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
                self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
                self.it.resena(1)                #turn on laser
                self.waitforChannellock(60)      #wait for channellock
                print "==>Tune to channel:%d"%x  #print channel number
                self.it.channel(x)
                print "==>Set Power to :%d"%y    #print power level 
                self.it.pwr(y)                    #set voa
                print "==>Set ftf to :%d"%z      #print ftf setting 
                self.it.ftf(z)                   #set ftf 
                print self.it.resena()          #print reg#32        
                print "==>Turn on the laser"
            except Exception as e:
                print e.message
            

            self.startTime = time.time()        #starttime
            self.lapseTime = time.time() -  self.startTime #lapse time count
            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
            
            while 1 :
                try:
                    
                    self.statusF = bin(int(self.it.statusF()[1].data()))
                    self.statusW = bin(int(self.it.statusW()[1].data()))
                    self.pending = self.it.nop()[1].fieldPending()
                    self.lf = self.it.lf()[1]
                    self.oop = self.it.oop()[1]
                    self.ftf = self.it.ftf()[1]
                    self.tunerstate = self.it.readx99().tunerstate
                    self.lapseTime = time.time() -  self.startTime  #keep counting time
                    print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                    
                    if self.lapseTime >= 5.0: #After 5 secs,trigger power cycle
                        print("==>Trigger Power Cycle...")
                        powersupply.setOutputState('OFF') # Turn off the power supply
                        time.sleep(3)                     # Delay for 3 seconds
                        powersupply.setOutputState('ON')  #Turn the power supply back on
                        time.sleep(3)
                        for rep in range(5): #              print 5 times
                            self.it.setpassword()           #enable password for x99
                            self.statusF = bin(int(self.it.statusF()[1].data()))
                            self.statusW = bin(int(self.it.statusW()[1].data()))
                            self.pending = self.it.nop()[1].fieldPending()
                            self.lf = self.it.lf()[1]
                            self.oop = self.it.oop()[1]
                            self.ftf = self.it.ftf()[1]
                            self.tunerstate = self.it.readx99().tunerstate
                            self.lapseTime = time.time() -  self.startTime #keep counting time
                            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                        break
                            
                        
                    elif self.lapseTime >= self.timeout:
                        print "The unit cannot tune please check the unit"
                        self.it.disconnect()
                    time.sleep(.5)
                    
                except Exception as e:
                    print e.message
            
                 
        print("Test Complete")
        self.it.disconnect()                #close communication
            
    def adjustsmallstepPower(self):
        self.min = 900   #minimum power level
        self.max = 1500  #maximum power level
        self.step = 100  #steps
     
        try:
            self.derivedPower = np.arange(self.min,self.max,self.step) #using arange to get the steps
        except Exception as e:
            print e.message
         
        self.derivedPowerList = self.derivedPower.tolist()    #convert to list
        return self.derivedPowerList     #return value
     
    def pendingClear(self):
        
        '''Function to monitor pending operation'''
        print 'Waiting for pending bit to clear...'
        self.it.setpassword()
        self.timeOut = 60.0
        self.starttime = time.time()
        self.duration = time.time() - starttime
        while self.duration <= self.timeOut:
            self.pendingBit = str(int(self.it.nop()[1].fieldPending().value()))
            self.it.logentry(time.asctime())
            self.reg99 = self.it.readx99()
            self.it.lf()
            self.it.statusF()
            self.it.statusW()
            self.it.logentry(time.asctime())
            if self.pendingBit == '0':
                self.reg99 = self.it.readx99()
                print "Pending bit Cleared..."
                self.tuneTime = self.duration
                break
            self.duration = time.time() - self.starttime
            if self.duration >=self.timeOut:
                self.it.logentry(time.asctime())
                self.reg99 = self.it.readx99()
                print self.it.temps()
                print self.it.currents()
                print self.it.statusF()
                print self.it.statusW()
                print self.it.readx99()
                raise "Tunetime more than 60 seconds: Stop Test"
        print 'TUNETIME:',self.tuneTime
        return self.tuneTime

         
          
    def runpendingtestCase18(self):
        ''' tune to a channel, wait for channel lock, set power 0.1dbm steps'''
        import  instrumentDrivers as inst       #import instrumentdrivers
        powersupply = inst.psAG3631('GPIB0::06')#intance of the agilent power supply
        powersupply.connect()                  #connect to power supply
        self.it.connect(_PORT,_BAUD)           #connect
        self.it.logging(True)
        self.it.logfile(self.logfilename18)    #enable logging
        self.it.setpassword()                  #x99 enabled
        self.powerList = adjustsmallstepPower()#call this function to get the steps
        for chan in self.channelList:          #iterate the channels
            try:
                self.it.channel(chan)          #switch channel
                self.it.statusF(1,1,1,1,1,1,1,1)#clear fatal alarm
                self.it.statusW(1,1,1,1,1,1,1,1)#clear warning alarm
                self.it.resena(sena=1)          #turn on the laser
                self.waitforChannellock(60)     #wait till channel lock
            except Exception as e:
                print e.message
                    
            for p in self.powerList:         #list of power
                try:
                    self.it.pwr(p)           #change power
                    self.pendingClear()      #wait until pending bit clears
                    self.it.channel(50)            #channel 50 as default
                    time.sleep(1)
                    print "==>Tune to channel:50"  #print channel number
                    self.it.statusF(1,1,1,1,1,1,1,1) #clear fatal alarms
                    self.it.statusW(1,1,1,1,1,1,1,1) #clear warning alarms
                    self.it.resena(1)                #turn on laser
                    self.waitforChannellock(60)      #wait for channellock
                    print "==>Tune to channel:%d"%x  #print channel number
                    self.it.channel(x)
                    print "==>Set Power to :%d"%y    #print power level 
                    self.it.pwr(y)                    #set voa
                    print "==>Set ftf to :%d"%z      #print ftf setting 
                    self.it.ftf(z)                   #set ftf 
                    print self.it.resena()          #print reg#32        
                    print "==>Turn on the laser"
                except Exception as e:
                    print e.message
                

            self.startTime = time.time()        #starttime
            self.lapseTime = time.time() -  self.startTime #lapse time count
            self.pending = self.it.nop()[1].fieldPending().toBinaryString()
                
            while 1 :
                try:
                        
                    self.statusF = bin(int(self.it.statusF()[1].data()))
                    self.statusW = bin(int(self.it.statusW()[1].data()))
                    self.pending = self.it.nop()[1].fieldPending()
                    self.lf = self.it.lf()[1]
                    self.oop = self.it.oop()[1]
                    self.ftf = self.it.ftf()[1]
                    self.tunerstate = self.it.readx99().tunerstate
                    self.lapseTime = time.time() -  self.startTime  #keep counting time
                    print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                    
                    if self.lapseTime >= 5.0: #After 5 secs,trigger power cycle
                        print("==>Trigger Power Cycle...")
                        powersupply.setOutputState('OFF') # Turn off the power supply
                        time.sleep(3)                     # Delay for 3 seconds
                        powersupply.setOutputState('ON')  #Turn the power supply back on
                        #time.sleep(3)
                        for rep in range(10): #print 5 times
                            
                            self.statusF = bin(int(self.it.statusF()[1].data()))
                            self.statusW = bin(int(self.it.statusW()[1].data()))
                            self.pending = self.it.nop()[1].fieldPending()
                            self.lf = self.it.lf()[1]
                            self.oop = self.it.oop()[1]
                            self.ftf = self.it.ftf()[1]
                            self.tunerstate = self.it.readx99().tunerstate
                            self.lapseTime = time.time() -  self.startTime #keep counting time
                            print(self.lapseTime, self.pending, self.lf, self.oop, self.ftf, self.statusF, self.statusW, self.tunerstate) #print these parameters
                        break
                            
                        
                    elif self.lapseTime >= self.timeout:
                        print "The unit cannot tune please check the unit"
                        self.it.disconnect()
                    time.sleep(.5)
                    
                except Exception as e:
                    print e.message
            
                 
        print("Test Complete")
        self.it.disconnect()                #close communication
##            



                
PendingBitTest = PendingBitTest()


if __name__== '__main__':

    try:
        print "==>Running Pending Test Case1"
        PendingBitTest.runpendingtestCase1() #run test case 1
    except Exception as ex:
        print(ex.message)

    try:
        print "==>Running Pending Test Case2"
        PendingBitTest.runpendingtestCase2() #run test case 2
    except Exception as ex:
        print(ex.message)
    try:
        print "==>Running Pending Test Case3"
        PendingBitTest.runpendingtestCase3() #run test case 3
    except Exception as ex:
        print(ex.message)
    try:
        print "==>Running Pending Test Case4"
        PendingBitTest.runpendingtestCase4() #run test case 4
    except Exception as ex:
        print(ex.message)

    try:
        print "==>Running Pending Test Case5"
        PendingBitTest.runpendingtestCase5() #run test case 5
    except Exception as ex:
        print(ex.message)
    try:
        print "==>Running Pending Test Case6"
        PendingBitTest.runpendingtestCase6() #run test case 6
    except Exception as ex:
        print(ex.message)
    try:
        print "==>Running Pending Test Case7"
        PendingBitTest.runpendingtestCase7() #run test case 7
    except Exception as ex:
        print(ex.message)

    try:
        print "==>Running Pending Test Case8"
        PendingBitTest.runpendingtestCase8() #run test case 8
    except Exception as ex:
        print(ex.message)

    try:
        print "==>Running Pending Test Case9"
        PendingBitTest.runpendingtestCase9() #run test case 9
    except Exception as ex:
        print(ex.message)

    try:
        print "==>Running Pending Test Case10"
        PendingBitTest.runpendingtestCase10() #run test case 10
    except Exception as ex:
        print(ex.message)


    try:
        print "==>Running Pending Test Case11"
        PendingBitTest.runpendingtestCase11() #run test case 11
    except Exception as ex:
        print(ex.message)

    try:
        print "==>Running Pending Test Case12"
        PendingBitTest.runpendingtestCase12() #run test case 12
    except Exception as ex:
        print(ex.message)

    try:
        print "==>Running Pending Test Case13"
        PendingBitTest.runpendingtestCase13() #run test case 13
    except Exception as ex:
        print(ex.message)

    try:
        print "==>Running Pending Test Case14"
        PendingBitTest.runpendingtestCase14() #run test case 14
    except Exception as ex:
        print(ex.message)


        # An information box
    tkMessageBox.showinfo("Information","Please Unplug and Plug the AARDVARK Dongle")

    try:
        print "==>Running Pending Test Case15"
        PendingBitTest.runpendingtestCase15() #run test case 15
    except Exception as ex:
        print(ex.message)

    tkMessageBox.showinfo("Information","Please Unplug and Plug the AARDVARK Dongle")
    
    try:
        print "==>Running Pending Test Case16"
        PendingBitTest.runpendingtestCase16() #run test case 16
    except Exception as ex:
        print(ex.message)
        
    tkMessageBox.showinfo("Information","Please Unplug and Plug the AARDVARK Dongle")    
        
    try:
        print "==>Running Pending Test Case17"
        PendingBitTest.runpendingtestCase17() #run test case 17
    except Exception as ex:
        print(ex.message)        
        
        




