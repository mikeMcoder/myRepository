###This script monitors the internal parameters of the state machine###
###Author: Michael Mercado                                          ###
#######################################################################import struct
import sys
import struct
import math
import os
import time
sys.path.append('C:\\Users\\michael.mercado\\Desktop\\uITLA_ &_uITLA2 Scripts\\Python')
sys.path.append(os.path.abspath('.'))
import instrumentDrivers as inst
import ConfigParser as parser
#import aa_gpio.gpio
#g = aa_gpio.gpio.gpio()
offset = .0015

#Define parameters of instruments
PS1 = inst.psAG3631('GPIB0::06')
PS2 = inst.psAG3631('GPIB0::07')
WM = inst.HP86120C('GPIB0::20')


def PS1_ON ():
    return PS1.setOutputState('ON')

def PS2_ON ():
    return PS2.setOutputState('ON')
    
def PS1_OFF():
    return PS1.setOutputState('OFF')

def PS2_OFF():
    return PS2.setOutputState('OFF')

def Wavemeter():
    return WM.getFrequency()

def modehop(meter):
    freq = float(meter)
    if freq> freq + offset or freq< freq - offset:
        modehop = 1
        print "There is a modehop"
        return modehop
    else:
        modehop = 0
        return modehop

def tpull (time0):
    c0 = time.time()-time0
    c1 = Wavemeter()
    c2 = o.demodulationReal()
    c3 = o.siBlockTemperature()
    c4 = o.filter1Temperature()
    c5 = o.filter2Temperature()
    c6 = o.gainMediumCurrent()
    c7 = o.photodiodeCurrent()
    c8 = o.sledTemperature()
    c9 = d.filter1()
    c10 =d.filter2()
    c11 = d.gainMedium()
    c12 = d.siBlock()
    c13 = d.tec()
    c14 = s.demodSignal()
    c15 = o.pcbTemperature()
    c16 = t.tuner().powerTuner().status()
    outS = ''
    for i in range(17):
        exec 'try:\n\tif type(c%d)!=str:c%d = str(c%d)\nexcept:\n\tpass\n'%(i,i,i)
        exec 'try:\n\toutS += c%d +\',\'\nexcept:\n\tpass\n'%(i)
    print outS
    return  outS

if __name__ == '__main__':
    ConfigIni = parser.ConfigParser()
    ConfigIni.read(r'C:\Documents and Settings\ttx.user\Desktop\uITLA_ &_uITLA2 Scripts\Regression.ini')
    Port=int(ConfigIni.get('Station','COM_PORT'))
    Freqlst=(ConfigIni.get('DomainStage','Freqlst'))
    Freqlst=Freqlst.split(',')
    Iteration=int(ConfigIni.get('DomainStage','Iteration'))
    SerialNumber = ConfigIni.get('Station','Serial')
    # Open a file

#Connect
    PS1.connect()
    PS2.connect()
    WM.connect()
    PS1_OFF()
    time.sleep(.5)
    PS2_OFF()
    time.sleep(.5)
    PS1_ON()
    time.sleep(.5)
    PS2_ON()
    time.sleep(.5)
    t.connect(Port)
    time.sleep(1)
    t.tuner().powerTuner().mask().tuner(0)
   

    for freq in Freqlst:
        timeStamp = time.asctime()
        strtimeStamp = str(timeStamp)
        strtimeStamp = strtimeStamp.replace(' ','')
        strtimeStamp = strtimeStamp.replace(':','')
        testfile = open(SerialNumber + '_' + 'domainStage' + '_' + freq + '_' + strtimeStamp + '.csv','w')
        testfile.write("testtime,Frequency,demodR,siBlock,filter1,filter2,gainMediumCurrent,photodiode,sledTemp,filter1(discrete),filter2(discrete),gmi(discrete),siblock(discrete),tec(discrete),demod(sample),pcb_temp,status\n")    
        freq=float(freq)
        print 'Tuning to:',freq
        t.tuner().powerTuner().frequency(freq)
        starttime=time.time()
        pt = t.tuner().powerTuner()

        print "Start Monitoring DomainStage Parameters"
        for i in range (Iteration):
            file = tpull(starttime)                 
            testfile.write(file + "\n")
            status = t.tuner().powerTuner().status()
            if status == 'CHANNEL_LOCK': 
                arrayS = file.split(',')
                meter = arrayS[1]
                r = modehop(meter)
                if r==1:
                    file = tpull(starttime)                 
                    testfile.write(file + "\n")
                    print "Unit Failed: Modehop Found at %i iteration!" % (Iteration)
                    raise "Stop , Need to debug this unit"
                    
        testfile.close()        
t.disconnect()
PS1_OFF()
PS1.disconnect()
PS2_OFF()
PS2.disconnect()
WM.disconnect()
print "Test is complete"        
        






                                         
    
    
    
