import time
import sys
import os
import pandas


sys.path.append(os.path.abspath('.'))

if sys.platform == 'cygwin':
    # for cygwin, use the packages installed from the windows installation of python
    sys.path.append('/cygdrive/c/Python27/Lib/site-packages/')

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
t.save_it_obj(it)

print 'Shit Instantiated a TTX interface as t, ITLA as it.'


_PORT = 20
_BAUD = 115200

class PendingBitTest:
    
    def __init__(self):
        self.it = it
        self.logfilename1 = "CheckThePendingBitCase1.txt"
        self.logfilename2 = "CheckThePendingBitCase2.txt"
        self.channelList = [1 , 52 , 93]
        self.powerList = [1300,1400,1600]
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
            self.lapseTime = self.startTime - time.time() #lapse time count
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
                self.lapseTime = self.startTime - time.time() #keep counting time
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
            self.lapseTime = self.startTime - time.time() #lapse time count
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
                self.lapseTime = self.startTime - time.time() #keep counting time
                if self.lapseTime >= self.timeout:
                    print "The unit cannot tune please check the unit"
                    self.it.disconnect()
        print("Test Complete")
        self.it.disconnect()                #close communication


                
PendingBitTest = PendingBitTest()


if __name__== '__main__':

##    try:
##        print "==>Running Pending Test Case1"
##        PendingBitTest.runpendingtestCase1() #run test case 1
##        
##    except:
##        raise "Error"

    try:
        print "==>Running Pending Test Case2"
        PendingBitTest.runpendingtestCase2() #run test case 2
    except:
        raise "Error"
    

##print "==> Change VOA"
##it.pwr(1300)
##for i in range(30):
##    print(it.nop()[1].fieldPending().toBinaryString(),it.lf(),it.oop(),it.ftf(),it.readx99().tunerstate)
##    time.sleep(1)
##
##
##print "==> Change FTF"
##it.ftf(4000)
##for i in range(40):
##    print(it.nop()[1].fieldPending().toBinaryString(),it.lf(),it.oop(),it.ftf(),it.readx99().tunerstate)
##    time.sleep(1)
##
##print "==> Change FTF and VOA"
##it.ftf(0)
##it.pwr(1550)
##for i in range(15):
##    print(it.nop()[1].fieldPending().toBinaryString(),it.lf(),it.oop(),it.ftf(),it.readx99().tunerstate)
##    time.sleep(1)

##print it.buildstring()
##it.resena(mr=1)
##it.disconnect()
