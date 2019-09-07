##Generate a test to calidate the CRL and SRQ bits by toggling the MS line##
##Psudocode
##Tune to a channel
##set RMS bit of register 0x0D to 1(Clear the input buffers but do not reset the baudrate)
##Repeat(5000)
##a.clear register 0x20 and 0x21 by writing 0x00FF
##b.Toggle MS line(to clear the communication input buffer)
##c.Check registers 0x20 and 0x21
## - Only CRL and SRQ bits should be set

import os
import sys
import time
import aa_gpio.gpio
g = aa_gpio.gpio.gpio()
g.InitPin()
#laser = raw_input('enter laser:')
wait = 0
timeInc = .01
sleepTime = 10
loopCount = 2000
file = open('CRL_VALIDATION.txt','w')
header = ('time'+ ' ' + 'RMS_STATUS'+ ' ' + 'CRL_BEFORE_F' + ' ' + 'SRQ_BEFORE_F' + ' ' + 'CRL_BEFORE_W' + ' ' + 'SRQ_BEFORE_W' + ' ' \
          + 'statFData_Before' + ' ' + 'statWData_Before' + ' ' + 'CRL_AFTER_F' + ' ' + 'SRQ_AFTER_F'+ ' ' + 'CRL_AFTER_W' + ' ' + 'SRQ_AFTER_W'+ ' ' \
          + 'StatFData_After'+ ' ' + ' StatusWData_After' + '\n')
file.write(header)
def clearPending():
    while 1:
        pending = int(it.nop()[1].fieldPending().value())
        if pending == 0:
            print 'Pending Cleared'
            break
        
try:
    starttime = time.time()
    #it.laser(laser)
    print "Test laser:", it.laser()
    it.connect(3)
    time.sleep(1)
    print 'Tune to Channel'
    it.resena(sena = 1)
    clearPending()
    print it.ioCap()
    it.ioCap(9600)
    rms = it.ioCap()[1].fieldRms().toBinaryString()
    print it.ioCap()
    it.statusF(1,1,1,1,1,1,1,1)
    it.statusW(1,1,1,1,1,1,1,1)
    for i in range(10000):
        print "------->",i
        print "wait",wait
        print it.temps()
        print it.oop()
        print it.age()
        print it.ftf()
        print it.fcf()
        print it.ioCap()
        #print'Turn on laser'
        it.resena(1)
        time.sleep(1)
        print 'Before',it.statusF()
        print 'Before',it.statusW()
        #print 'delay for %2fs'%sleepTime
        time.sleep(sleepTime)
        
        #print 'Disable laser'
        g.LDIS_N_Disable()
        time.sleep(wait)
        #clear all registers
        it.statusF(1,1,1,1,1,1,1,1)
        it.statusW(1,1,1,1,1,1,1,1)
        #print 'Enable laser'
        g.LDIS_N_Enable()

        #Read CLR bit
        statF = it.statusF()
        crlF1 = str(int(statF[1].fieldCrl().value()))
        print crlF1
        if crlF1 == '1':
            raise   "Failure detected, dly:", wait, i
        wait = wait + timeInc

        duration = time.asctime()
        data = duration + ' ' + rms + ' ' + crlF + ' ' + srqF + ' ' + crlW + ' ' + srqW + \
               ' ' + statF + ' ' + statW + ' ' + crlF1 + ' ' + srqF1 + ' ' + crlW1 + ' ' + srqW1 +\
               ' ' + statF1 + ' ' + statW1 +'\n'
        file.write(data)
                

    file.close()
    print "PASS"
except(KeyboardInterrupt):
    file.close()

print 'test complete'
it.disconnect()
totalTime = time.time() - starttime
print "total test time is: %4fs"%totalTime
