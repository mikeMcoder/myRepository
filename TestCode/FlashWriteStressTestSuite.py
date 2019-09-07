# -*- coding: utf-8 -*-
"""
Created on Fri May 05 09:08:41 2017

@author: Michael Mercado

Requirement
Writeflashwrites at a very fast rate sequence is:
power(9)
check watchdog
cnt1
channe(1)
check watchdog
cnt1
power(10)
check watchdog
cnt1
channel(96)
check watchdog
cnt1

version3: add a counter to count 20x before printing to avoid the runtime error
"""




import sys
import os
sys.path.append(os.path.abspath('.'))
import instrumentDrivers as inst
#import instrumentDrivers as inst
#import TDS3054B_E_revA as instScope

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'


import time

TCP_IP = '192.168.1.1'
PORT=3 #int(raw_input('Enter Port:'))
PowerList = [1000,990,980,970,960,950,940,930,920,910,900,890,880,870,860,850,840,830,820,810,800,790,780,770,760,750,740,730,720,710,700]             
ChannelList = [96]
Limit = 500000
count = 0
sleeptime=0.000


def activateWavemeter(inst):
    wm = inst.HP86120C('GPIB::21')
    wm.connect()
    return wm
    
def activatePowermeter(inst):
    pm = inst.pmHP8163('GPIB::11')
    pm.connect()
    return pm
    
def createFileForVoltageTest(SN,dt,tempS='25C'):
    fname='C:\data\%s_HiSilicon_SledLockingIssue_bombardFlashwrites_%s_%s'%(SN[1][0:10],tempS,dt)
    f=open(fname,'w')
    
    s='%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %('CurrentTime','run_time', 'Tec','gmi','power','Tsled','Tpcb','statusF','statusW','Freq',\
    'nop','SetPwr','Frequency(Meter)','Power(Meter)','Filter1 Temp','Filter2 Temp','Siblock','DemodR','Sled','Gmi','PD','State_Machine')#,\
                                                             #'Filter1 Temp','Filter2 Temp','SiBlock Htr DAC', 'Filter1 Htr DAC','Filter2 Htr DAC',\
                                                              #     'PD current ADC','DemodR','StateMachine')
    
    f.writelines(s+'\n')
    f.close()
    print fname
    return fname
    
def turnOnpowersupplies():
        ps = inst.psAG3631('gpib0::06')
        ps.connect()
        ps.setOutputState(state='ON')
        return ps

def turnOffpowersupplies(ps):
        ps.setOutputState(state='OFF')

    

def waitSeconds(seconds):
    s = int(seconds)
    for i in range (s):
        time.sleep(1)
    time.sleep(seconds-s)
    
def timeStamp():
    daytime = time.asctime()
    daytimestr = daytime.replace(' ','')
    daytimestr = daytimestr.replace(':','')
    return daytimestr


def checkSled(sled=0):
    if sled < 48.00:
        print 'sled',sled
        raise ' Sled not in spec stop'
        return 1
    else:
        return 0
    
def checkWatchdog(resetStatus = '',dogCount= None,flashCount=  None):
    if resetStatus == 'WATCHDOG_RESET':
        dogCount +=1
        flashCount +=1
        it.resena(mr=1)
        time.sleep(5)
        it.pwr(900)
        it.channel(1)
        it.statusF(1,1,1,1,1,1,1,1)
        it.statusW(1,1,1,1,1,1,1,1)
        it.resena(1)
        time.sleep(30)
        print 'Watchdog Triggered, reset laser then continue....'
        return flashCount,dogCount
    else:
        flashCount +=1
        return flashCount,dogCount

   
        
        
    
    
def main():
    try:

        flashCount= 0
        dogCount = 0
        flashCnt = 0
        dogCnt = 0
        flashcountTotal = 0
        dogcountTotal = 0
        printCnt = 0
        ps = turnOnpowersupplies() # turn on power supply
        time.sleep(3)
        it.disconnect()
        print 'wait for terminate the COM port, this is used for debug only'
        it.connect(PORT,115200)
        it.logging('True')
        timestamp = timeStamp()
        it.logfile('HiSilicon_SledLockingIssue_bombardFlashwrites' + '_' + timestamp + '.txt')
        it.setpassword(3)
        print 'ttm_laser1 connected!'
        cm=time.localtime()
        dateTime= '%d%02d%02d%02d%02d%02d.csv'%(cm[0],cm[1],cm[2],cm[3],cm[4],cm[5])
        (status,SN) = it.serNo()
        build = it.buildstring()
        it.logentry(SN[1])
        it.logentry(build)
        fn = createFileForVoltageTest(SN[1],dateTime)
        count = 0
        sledNotspec = 0
        stat = 0
        #turn on laser to stable condition first
        it.channel(96)
        it.statusF(1,1,1,1,1,1,1,1)
        it.statusW(1,1,1,1,1,1,1,1)
        it.resena(1)
        #stat = pendingClear(fn,it)
        time.sleep(30)
        print time.asctime(),'Start Reset_Source:',it.dbgReset()
        
        print 'Testing...'
        while flashcountTotal <= Limit:
               
            
            it.pwr(900)
            resetStatus = it.dbgReset()[1].fieldSource().cipher()
            resetStatus = it.dbgReset()[1].fieldSource().cipher()
            resetStatus = it.dbgReset()[1].fieldSource().cipher()
            flashCnt,dogCnt = checkWatchdog(resetStatus,dogCount,flashCount) # function to detect watchdog and count also flashwrites
            if flashCnt:
                flashcountTotal +=1
                printCnt+=1
            if dogCnt:
                dogcountTotal +=1
            #print time.asctime(),'FlashWrite:',flashcountTotal,'Watchdog:',dogcountTotal,'Channel:',it.channel(),'Power:',it.pwr(),'Reset_Source:',it.dbgReset()
            it.channel(1)
            resetStatus = it.dbgReset()[1].fieldSource().cipher()
            resetStatus = it.dbgReset()[1].fieldSource().cipher()
            resetStatus = it.dbgReset()[1].fieldSource().cipher()
            flashCnt,dogCnt = checkWatchdog(resetStatus,dogCount,flashCount) # function to detect watchdog and count also flashwrites
            if flashCnt:
                flashcountTotal +=1
                printCnt+=1
            if dogCnt:
                dogcountTotal +=1
            #print time.asctime(),'FlashWrite:',flashcountTotal,'Watchdog:',dogcountTotal,'Channel:',it.channel(),'Power:',it.pwr(),'Reset_Source:',it.dbgReset()
            it.pwr(1000)
            resetStatus = it.dbgReset()[1].fieldSource().cipher()
            resetStatus = it.dbgReset()[1].fieldSource().cipher()
            resetStatus = it.dbgReset()[1].fieldSource().cipher()
            flashCnt,dogCnt = checkWatchdog(resetStatus,dogCount,flashCount) # function to detect watchdog and count also flashwrites
            if flashCnt:
                flashcountTotal +=1
                printCnt+=1
            if dogCnt:
                dogcountTotal +=1
            #print time.asctime(),'FlashWrite:',flashcountTotal,'Watchdog:',dogcountTotal,'Channel:',it.channel(),'Power:',it.pwr(),'Reset_Source:',it.dbgReset()
            it.channel(96)
            #resetStatus = 'WATCHDOG_RESET'#it.dbgReset()[1].fieldSource().cipher() 
            resetStatus = it.dbgReset()[1].fieldSource().cipher()
            resetStatus = it.dbgReset()[1].fieldSource().cipher()
            resetStatus = it.dbgReset()[1].fieldSource().cipher()
            flashCnt,dogCnt = checkWatchdog(resetStatus,dogCount,flashCount) # function to detect watchdog and count also flashwrites
            if flashCnt:
                flashcountTotal +=1
                printCnt+=1
            if dogCnt:
                dogcountTotal +=1
            #print time.asctime(),'FlashWrite:',flashcountTotal,'Watchdog:',dogcountTotal,'Channel:',it.channel(),'Power:',it.pwr(),'Reset_Source:',it.dbgReset()
            if printCnt ==1000:
                print time.asctime(),'FlashWrite:',flashcountTotal,'Watchdog:',dogcountTotal,'Channel:',it.channel(),'Power:',it.pwr(),'Reset_Source:',it.dbgReset()
                print 'SerialNumber:',SN[1],'Build:',build
                printCnt = 0
        print 'Total Flashwrites:',flashcountTotal,'Total Watchdog Triggers:',dogcountTotal
        print it.serNo()
        print it.buildstring()
        print "Test Complete"
        it.disconnect()
        turnOffpowersupplies(ps)
        
    except Exception,e:
        print e
        print 'Total Flashwrites:',flashcountTotal,'Total Watchdog Triggers:',dogcountTotal
        print 'There is an error..'
        #pass
        

if __name__ == '__main__':
    main()
