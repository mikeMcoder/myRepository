
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
iter = 0
timeInc = .5
sleepTime = 1
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
    for i in range(200):
        #print "------->",i
        #it.statusF(1,1,1,1,1,1,1,1)
        #it.statusW(1,1,1,1,1,1,1,1)
        #crlF = it.statusF()[1].fieldCrl().toBinaryString()
        #srqF = it.statusF()[1].fieldSrq().toBinaryString()
        #crlW = it.statusW()[1].fieldCrl().toBinaryString()
        #srqW = it.statusW()[1].fieldSrq().toBinaryString()
        #statF = hex(int(it.statusF()[1].data()))
        #statW = hex(int(it.statusW()[1].data()))
##        
        #print'Turn on laser after LDIS'
        it.resena(1)
        #print 'Before',it.statusF()
        #print 'Before',it.statusW()
##        if laser == '1':
##            print laser
##            g.MODSEL_N_Disable()
##            g.MODSEL_N_Enable()
##            print 'reset done1'
        #print 'delay for %2fs'%sleepTime
        time.sleep(sleepTime)
        
        #print 'Disable laser'
        g.LDIS_N_Disable()
        time.sleep(.2)
        #print 'Enable laser'
        g.LDIS_N_Enable()
        
        #clearPending()
        #print 'After', it.statusF()
        #print 'After', it.statusW()
        statF = it.statusF()
        crlF1 = statF[1].fieldCrl().toBinaryString()
        srqF1 = statF[1].fieldSrq().toBinaryString()
        #statW = it.statusW()
        #crlW1 = statW[1].fieldCrl().toBinaryString()
        #srqW1 = statW[1].fieldSrq().toBinaryString()
        statF1 = hex(int(statF[1].data()))
        #statW1 = hex(int(statW[1].data()))
        #iter +=1
        if crlF1 == 1:
            raise   "Failure detected, dly:", sleepTime, i
        #print iter + 1
        #duration = time.asctime()
        #data = duration + ' ' + rms + ' ' + crlF + ' ' + srqF + ' ' + crlW + ' ' + srqW + \
        #       ' ' + statF + ' ' + statW + ' ' + crlF1 + ' ' + srqF1 + ' ' + crlW1 + ' ' + srqW1 +\
        #       ' ' + statF1 + ' ' + statW1 +'\n'
        #file.write(data)
        sleepTime = sleepTime + timeInc
        
##        print'Turn off laser'
##        it.resena(0)
##        it.resena(1)
##        clearPending()
    file.close()
    print "PASSED"
except(KeyboardInterrupt):
    file.close()

print 'test complete'
it.disconnect()
totalTime = time.time() - starttime
print "total test time is: %4fs"%totalTime
    








