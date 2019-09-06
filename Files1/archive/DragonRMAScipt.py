import os
import sys
sys.path.append(os.path.abspath('.'))
import instrumentDrivers as inst
exec(open('RegressionUtility_K.py','r'))
from Tkinter import *
import math
          
import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'

repeatSeq = 10
pollTimeLimit = 300.0
pwrTarget = 25.0
Dragon = False
HiSilicon = True


class Dragon:
    def __init__(self):
        self.t = t
        self.it = it
        self.port = 3
        wavemeter1,powermeter1,com_port = connectInstrument()
        self.wavemeter1 = wavemeter1
        self.powermeter1 = powermeter1
        self.fList = [191.3,193.9,196.05]
        self.pwrList = [22.3, 28.18]
        self.itpwrList=[500,1350]
        self.header = 'Time' + ','\
                      + 'Frequency' + ',' \
                      +'ActualPower' + ','\
                      +'InternalPower' + ','\
                      +'PowerError' + ','\
                      +'F1' + ','\
                      +'F2' + ','\
                      +'SiBlock' + ','\
                      +'DemodR' + ','\
                      +'PD' + ','\
                      +'GMI' + ','\
                      +'SLED' + ','\
                      +'TEC' + ','\
                      +'PCBT' + '\n' 
        self.file = None
        self.f = 191.3
        self.chn = 0
        
        
    def data(self):
        stamp = time.asctime()
        rstamp = stamp.replace(':','')
        rstamp = rstamp.replace(' ' , '_')
        self.file = open('DragonRMAPowerIssue' + str(rstamp) + '.csv','w')
        self.file.write(self.header)
        return self.file
                
        
    def monitorIt(self,obj1,obj2):
        data = ''
        freq = self.wavemeter1.getFrequency()
        power = self.powermeter1.getDisplayedPower()
        pwrOutput = float(self.it.oop()[1])/100
        pwrError = power - pwrOutput
        f1 = self.it.readx99().f1temp
        f2 = self.it.readx99().f2temp
        siB = self.it.readx99().siblocktemp
        demodR = self.it.readx99().demodrealerr
        pd = self.it.readx99().photodiode_current
        gmi = self.it.readx99().gain_medium_current
        sled = self.it.readx99().sled_temperature
        tec = int(self.it.currents()[1][1][0])
        pcbT = float(self.it.temps()[1][1][1])/100
        data = str(freq) + ','\
               +str(power) + ','\
               +str(pwrOutput) + ','\
               +str(pwrError) + ','\
               +str(f1) + ','\
               +str(f2) + ','\
               +str(siB) + ','\
               +str(demodR) +','\
               +str(pd) + ','\
               +str(gmi) + ','\
               +str(sled) + ','\
               +str(tec) + ','\
               +str(pcbT) + '\n'
        print data
        return data


    def monitor(self,obj1,obj2):
        data = ''
        freq = self.wavemeter1.getFrequency()
        power = self.powermeter1.getDisplayedPower()
        pwrOutput = float(self.it.oop()[1])/100
        pwrError = power - pwrOutput
        f1 = self.t.domainStage().frame().filter1Temperature()
        f2 = self.t.domainStage().frame().filter2Temperature()
        siB =self.t.domainStage().frame().siBlockTemperature()
        demodR = self.t.domainStage().frame().demodulationReal()
        pd = self.t.domainStage().frame().photodiodeCurrent()
        gmi = self.t.domainStage().frame().gainMediumCurrent()
        sled = self.t.domainStage().frame().sledTemperature()
        tec = self.t.domainStage().frame().tecCurrent()
        pcbT = self.t.domainStage().frame().pcbTemperature()
        data = str(freq) + ','\
               +str(power) + ','\
               +str(pwrOutput) + ','\
               +str(pwrError) + ','\
               +str(f1) + ','\
               +str(f2) + ','\
               +str(siB) + ','\
               +str(demodR) +','\
               +str(pd) + ','\
               +str(gmi) + ','\
               +str(sled) + ','\
               +str(tec) + ','\
               +str(pcbT) + '\n'
        print data
        return data    
            
    def waitChannelLock(self):
        limit = 60.0
        start = time.time()
        duration = time.time() - start
        while 1:
            stat = self.t.tuner().powerTuner().status()
            if stat =='CHANNEL_LOCK':
                print 'Channel Locked in %2fs'%duration
                break
            if duration >= limit:
                print 'Time out'
                break
            duration = time.time() - start
        return duration

    
            
               
            

    def RunHiSilicon(self):
        try:
            self.file = self.data()
            self.it.connect(self.port)
            setComslog('HiSiliconRMA')
            #tune to a crhnnel
            self.it.resena(1)
            #list of frequencies to tune
            while self.chn < 96:
                self.chn += 1
                self.it.channel(self.chn)
                print 'Tune to channel',self.it.lf()[1]
                #make sure it is locked
                pendingClear()
                pwr = self.it.opsh()[1]
                currPow =self.it.oop()[1]
                #make sure the starting power is the higest power
                if currPow < pwr:
                    self.it.pwr(pwr)
                    print 'Adjusting power to highest power'
                    pendingClear()
                #iteration of power switches in the sequences
                for r in range(repeatSeq):
                    print 'Iteration:',r
                    #switch power levels
                    for p in self.itpwrList:
                        startTime = time.time()
                        dur = time.time() - startTime
                        self.it.pwr(p)
                        #check the time duration for x sec
                        while dur < pollTimeLimit:
                            data = self.monitorIt(self.wavemeter1,self.powermeter1)
                            self.file.write(str(time.asctime()) + ',' + data)
                            if dur >= pollTimeLimit:
                                print '%fsec polltime complete'%pollTimeLimit
                                break
                            dur = time.time() - startTime
                        print 'Change to next power...'
            self.it.disconnect()
            self.file.close()
            print 'test done...'

        except(ValueError):
            self.file.close()
            raise 'Error'



    def RunDragon(self):
        try:
            self.file = self.data()
            self.t.connect(self.port)
            #tune to a crhnnel
            self.t.tuner().powerTuner().mask().tuner(0)
            #list of frequencies to tune
            while self.f < 196.5:
                self.f +=0.050
                self.t.tuner().powerTuner().frequency(self.f)
                print 'Tune to channel',self.f
                #make sure it is locked
                self.waitChannelLock()
                currPow = self.t.tuner().powerTuner().powerOutput()
                #make sure the starting power is the higest power
                if currPow < 25:
                    self.t.tuner().powerTuner().powerTarget(pwrTarget)
                    print 'Adjusting power to highest power'
                    time.sleep(10)
                #iteration of power swiches in the sequences
                for r in range(repeatSeq):
                    print 'Iteration:',r
                    #switch power levels
                    for p in self.pwrList:
                        startTime = time.time()
                        dur = time.time() - startTime
                        self.t.tuner().powerTuner().powerTarget(p)
                        #check the time duration for x sec
                        while dur < pollTimeLimit:
                            data = self.monitor(self.wavemeter1,self.powermeter1)
                            self.file.write(str(time.asctime()) + ',' + data)
                            if dur >= pollTimeLimit:
                                print '%fsec polltime complete'%pollTimeLimit
                                break
                            dur = time.time() - startTime
                        print 'Change to next power...'
            self.t.disconnect()
            self.file.close()
            print 'test done...'

        except(ValueError):
            self.file.close()
            raise 'Error'        
        


r = Dragon()


if __name__=='__main__':

##    if Dragon:
##        
##        r.RunDragon()

    if HiSilicon:
        
        r.RunHiSilicon()
        
    else:
        print 'Nothing Selected..'
   




#connect
#tune to channel x
#wait for channel lock
#set power to 1450 to 1350, monitor parameters while adjusting, actual power, internal power, domainstage parameters
