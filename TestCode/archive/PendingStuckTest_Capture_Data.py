import sys
import os
import sys
import instrumentDrivers as inst
import time
import math
import aa_gpio.gpio
g = aa_gpio.gpio.gpio()

sys.path.append(os.path.abspath('.'))

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'

P3_3 = inst.psAG3631('GPIB0::06')
PN5_2 = inst.psAG3631('GPIB0::07')

loop = 10
port = 3
counter = 0
passcnt = 0
stuckcnt = 0


def Supply_3_3ON():    
    P3_3.setOutputState('ON')

    
def Supply_3_3OFF():
    P3_3.setOutputState('OFF')


def Supply_5_2ON():    
    PN5_2.setOutputState('ON')

    
def Supply_5_2OFF():
    PN5_2.setOutputState('OFF')


def Supply_3_3Curr():
    Current = P3_3.getCurr()
    return Current

def read(cnt):
    fail = 0
    try:
        temp1 = float(it.dbgTemps(1)[1].data())/100
        temp2 = float(it.dbgTemps(2)[1].data())/100
        if temp1 and temp2 > 300.00:
            status = 1
            
            
        else:
            status = 0
            
    except:
         pass
           
    return status
            
        
        
        
        
    


P3_3.connect()
PN5_2.connect()


# Assemble file header
testTime = time.ctime().replace(' ', '_').replace(':', '')
dataFile = open('HuaweiPSStressTest' + '_' + testTime +  '.txt', 'w')
headerLst = ['serialNo',
             'time',
             'nop',
             'fAge',
             'statusF(hex)',
             'oop',
             'tec',
             'gmi',
             'statusW',
             'sled',
             'pcbTemp',
             'age',
             'pending']
strHeader = ''
for item in headerLst:
             strHeader += (item + '\t')
strHeader.rstrip('\t')
dataFile.write(strHeader + '\n')
    

it.connect(port)
strSer = str(it.serNo())
ser = str(strSer[14:24])
if __name__ == '__main__':
    

    #Main iteration
    while 1:
       
        #Turn on suply sequence
        ####MAIN####
        Supply_5_2OFF()
        time.sleep(.06)
       
        Supply_3_3OFF()
        time.sleep(.6)
        Supply_5_2ON()
        time.sleep(.045)
        Supply_3_3ON()
        g.InitPin()
        time.sleep(.9)
        g.reset(.05)
        duration = time.time()
        time.sleep(1)
        it.resena(sr=1)
        time.sleep(3)
        it.resena(1)
        time.sleep(1)
        failcnt = read(counter)
        if failcnt == 0:
            passcnt += 1
            print "Pending Good Count", passcnt
            raise "Stop Capture Data"
        else:
            stuckcnt +=1
            print "Pending Stuck Count", stuckcnt
            print it.nopStats()
            print it.dbgTemps(1)
            print it.dbgTemps(2)
            print it.temps()
            raise "STOP! Failed here, print failure conditions"

            
            

        time.sleep(1)
            
        
        
it.disconnect()




##
##    while time.time() - duration < 6: #sec:
##       #nop_data = str(hex(int(it.nop()[1].data())))
##        it.write('\x00\x00\x00\x00')
##        it.read(4)
##       #it.temps()
##        it.write('\xD0\x58\x00\x00')
##        it.read(4)
##        it.write('\xA0\x0A\x00\x00')
##        it.read(4)
##        it.write('\x90\x09\x00\x00')
##        it.read(4)
##        it.write('\xB0\x0B\x00\x00')
##        it.read(4)
##        it.write('\xB0\x0B\x00\x00')
##        it.read(4)
####      it.resena(sr=1)
##    it.write('\x21\x32\x00\x02')
##    it.read(4)
##    ##it.resena(1)
##    it.write('\x81\x32\x00\x08')
##    it.read(4)
##
##    
####      it.ioCap(9600)
##    it.write('\xD1\x0D\x10\x00')
##    it.read(4)
####      it.srqT(0,0,0,0,0,0,0,0,0,0,0,0,0)
##    it.write('\xA0\x28\x00\x00')
##    it.read(4)
##    it.write('\xB1\x28\x00\x00')
##    it.read(4)
####        it.grid(50)
##    it.write('\x71\x34\x00\x32')
##    it.read(4)
####        it.pwr(1000)
##    it.write('\x61\x31\x03\xE8')
##    it.read(4)
####        it.wPowTh(200)
##    it.write('\x41\x23\x00\xC8')
##    it.read(4)
####        it.fPowTh(300)
##    it.write('\xE1\x22\x01\x2C')
##    it.read(4)
####        it.ditherE(0) #0x59 dither disabled
##    it.write('\xD1\x59\x00\x00')
##    it.read(4)
####        it.ditherE(1) #0x59 dither Ensabled
##    it.write('\xC1\x59\x00\x10')
##    it.read(4)
####        it.fcf1(191) #0x35 first channel frequency can be defined here Thz
##    it.write('\x31\x35\x00\xBF')
##    it.read(4)
####        it.fcf2(5000) #0x36 first channel frequency can be defined here Ghz * 10
##    it.write('\x61\x36\x13\x88')
##    it.read(4)
####        it.mcb(sdf=0, adt=0) #0x33 module configuration behavior settings
##    it.write('\x00\x33\x00\x00')
##    it.read(4)
##    it.write('\x11\x33\x00\x00')
##    it.read(4)
####        it.statusF(1,1,1,1,1,1,1,1) # fatal status
##    it.write('\x31\x20\x00\xFF')
##    it.read(4)
####        it.statusW(1,1,1,1,1,1,1,1) # warning status
##    it.write('\x21\x21\x00\xFF')
##    it.read(4)
##
##    
## #turn on laser
##    pending = it.nop()[1].fieldPending().toBinaryString()
##    flag = str(pending[7])
##    Startime = time.time()
##    duration = 1
##    iter=0
##    lstData = []
##    while duration < 40:
##        nop  = it.nop()
##        nop_data = str(hex(int(it.nop()[1].data())))
####            if nop[0] != 'OK':
####                file = open('it.nop()_failed.txt','w')
####                file.write('failure:'+'\n')
####                failed_nop = str(nop)
####                file.write(failed_nop)
####                file.close()
####                raise "nop Failed"
####            
##        fAge = it.fAgeTh()
##        fAge_data = str(it.fAgeTh()[1])
####            if fAge[0] != 'OK':
####                file = open('it.fAge()_failed.txt','w')
####                file.write('failure:'+'\n')
####                failed_fAge = str(fAge)
####                file.write(failed_fAge)
####                file.close()
####                raise "fAge failed"
####            
##        statusF = it.statusF()
##        statusF_data = str(hex(int(it.statusF()[1].data())))
####            if statusF[0] != 'OK':
####                file = open('it.statusF()_failed.txt','w')
####                file.write('failure:'+'\n')
####                failed_statusF = str(statusF)
####                file.write(failed_statusF)
####                file.close()
####                raise "StatusF failed"
##        
##        oop =it.oop()
##        oop_data = str(it.oop()[1])
####            if oop[0] != 'OK':
####                file = open('it.oop()_failed.txt','w')
####                file.write('failure:'+'\n')
####                failed_oop = str(oop)
####                file.write(failed_oop)
####                file.close()
####                raise "oop failed"
##        
##        currents =it.currents()
##        garbage , currents_data = it.currents()
##        tec = currents_data[1][0]
##        gmi = currents_data[1][1]
##        currents =it.currents()
####            if currents[0] != 'OK':
####                file = open('it.currents()_failed.txt','w')
####                file.write('failure:'+'\n')
####                failed_currents = str(currents)
####                file.write(failed_currents)
####                file.close()
####                raise "currents failed"
####            
##        statusW = it.statusW()
##        statusW_data = str(hex(int(it.statusW()[1].data())))
####            if statusW[0] != 'OK':
####                file = open('it.statusW()_failed.txt','w')
####                file.write('failure:'+'\n')
####                failed_statusW = str(statusW)
####                file.write(failed_statusW)
####                file.close()
####                raise "statusW failed"
##        
##        temps = it.temps()
##        garbage, temps_data = it.temps()
##        sledTemp = temps_data[1][0]
##        pcbTemp = temps_data[1][1]
####            if temps[0] != 'OK':
####                file = open('it.temps()_failed.txt','w')
####                file.write('failure:'+'\n')
####                failed_temps = str(temps)
####                file.write(failed_temps)
####                file.close()
####                raise "temps failed"
##        age = it.age()
##        age_data = it.age()[1]
####            if age[0] != 'OK':
######                file = open('it.age()_failed.txt','w')
######                file.write('failure:'+'\n')
######                failed_age = str(age)
######                file.write(failed_age)
######                file.close()
######                raise "age failed"
##        lf = it.lf()
####            if lf[0] != 'OK':
####                file = open('it.lf()_failed.txt','w')
####                file.write('failure:'+'\n')
####                failed_lf = str(lf)
####                file.write(failed_lf)
####                file.close()
####                raise "lf failed"
##        lfh = it.lfh()
####            if lfh[0] != 'OK':
####                file = open('it.lfh()_failed.txt','w')
####                file.write('failure:'+'\n')
####                failed_lfh = str(lfh)
####                file.write(failed_lfh)
####                file.close()
####                raise "lfh failed"       
##        lfl = it.lfl()
####            if lfl[0] != 'OK':
####                file = open('it.lfl()_failed.txt','w')
####                file.write('failure:'+'\n')
####                failed_lfl = str(lfl)
####                file.write(failed_lfl)
####                file.close()
####                raise "lfl failed"
##        duration = time.time() - Startime
##        iter += 1
##        testTime = time.ctime().replace(' ', '_').replace(':', '')
##        Pend = it.nop()[1].fieldPending().toBinaryString()
##        pending= str(Pend[7])
##        lstData.append([testTime,nop_data,fAge_data,statusF_data,\
##                       oop_data,tec,gmi,statusW_data,sledTemp,\
##                       pcbTemp,age_data,pending])
##
##        for item in lstData:
##            # post conversion
##            strWrite = ''
##            strWrite += '%s\t' % ser
##            strWrite += '%0.2d\t' % duration
##            strWrite += '%s\t' % nop_data 
##            strWrite += '%s\t' % fAge_data
##            strWrite += '%s\t' % statusF_data
##            strWrite += '%s\t' % oop_data
##            strWrite += '%s\t' % tec
##            strWrite += '%s\t' % gmi
##            strWrite += '%s\t' % statusW_data
##            strWrite += '%s\t' % sledTemp
##            strWrite += '%s\t' % pcbTemp
##            strWrite += '%s\t' % age_data
##            #strWrite += '%s\t' % pending
##            strWrite += '%s\t' % pending
##            strWrite += '\n'
##            dataFile.write(strWrite)
##            time.sleep(.1)
##  
##
##        if iter == 1:
##            print "*",
##            sys.stdout.flush()
##            time.sleep(.01)
##            iter = 0
##        if duration >= 20 and pending ==1:
##            print "Pending bit is stuck"
##            dataFile.write(strWrite)
##            raise "This unit failed"
##    
##    
##    counter += 1
##    print "Counter:",counter
##     
##    Supply_5_2OFF()
##    Supply_3_3OFF()
##
##print "Test Complete"
##it.disconnect()
##Supply_5_2OFF()
##Supply_3_3OFF()
##   
