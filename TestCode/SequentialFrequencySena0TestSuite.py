import math
import struct
import sys
import os
import time
import instrumentDrivers as inst
import ConfigParser as parser
sys.path.append(os.path.abspath('.'))

utility = open('RegressionUtility_L.py')
exec(utility)

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'


import aa_gpio.gpio 
g = aa_gpio.gpio.gpio()
g.InitPin()


channelList = []
com_port = 3
iteration = 30

def turnOnpowersupplies():
    ps = inst.psAG3631('gpib0::06')
    ps.connect()
    ps.setOutputState(state='ON')
    return ps

def turnOffpowersupplies(ps):
    ps.setOutputState(state='OFF')


def pendingClearSled():
    '''Function to monitor pending operation'''
    print 'Waiting for pending bit to clear...'
    it.setpassword()
    timeOut = 2000
    starttime = time.time()
    duration = time.time() - starttime
    while duration < timeOut:
        pendingBit = str(int(it.nop()[1].fieldPending().value()))
        it.logentry(time.asctime())
        reg99 = it.readx99()
        if reg99.sled_temperature <49.0 or reg99.sled_temperature > 51.0:
            raise "Failed Sled Temp"
        it.lf()
        it.statusF()
        it.statusW()
        it.logentry(time.asctime())
        if pendingBit == '0':
            reg99 = it.readx99()
            reg99
            print "Pending bit Cleared..."
            tuneTime = duration
            break
        duration = time.time() - starttime
        if duration >=timeOut:
            it.logentry(time.asctime())
            reg99 = it.readx99()
            print it.temps()
            print it.currents()
            print it.statusF()
            print it.statusW()
            print it.readx99()
            raise "Tunetime more than 60 seconds: Stop Test"
    print 'TUNETIME:',tuneTime
    return tuneTime

    

def runCase1():
    testName = 'Nano_Sequential_Frequency_Test_Sena0'
    ps=turnOnpowersupplies()
    time.sleep(3)
    wavemeter1,powermeter1,com_port1 = connectInstrument()      #initialize intruments
    it.connect(com_port,115200)                                       #open port
    setComslog(testName)   
    instrumentInfo,parameters = showInitialParameters(wavemeter1)                           #get the initial parameters as a dictionary
    folderPath = createNewDirectory(name=testName)              #Createfolder
    test_name1,test_file1 = singlecreateFile(folderPath,testName,parameters,instrumentInfo)#createfile
    test_file1 = open(folderPath + '\\' + test_name1 + '.txt','w')
    #huaweiPowerSupplySequence()                                #turn on huawei power supply sequence
    #time.sleep(3)
    #readMready()                                               #wait for mready bit to be 1
    turnOnLaser()                                              #turnonlaser
    startTime = time.time()
    for i in parameters.values()[2]:
        
        it.mcb(adt=i)                                          #set the adt bit in the mcb register
        print 'SET ADT:%d'%i, '=', it.mcb()[1].fieldAdt()
        for pwr in parameters.values()[13]:                    #list of power levels
            setPower(pwr)                                                                  #set power levels for test
            pendingClear()
            waitfortimeout(timeout=15)
            for cycle in range(iteration):
                print 'ITERATION:', cycle + 1
                channelList = createChannelList(start=1, stop=97, step=1) #create sequential sequence
                for chn in channelList:                                    #loop to select channel
                    clearAlarms()
                    it.logentry(time.time() + '=====> Turn on laser here')
                    it.resena(1)#Clear alarms
                    setChannel(chn)                                         #Change to a channel
                    freq = it.lf()[1]
                    powermeter1.setFrequency(freq)                          #change the powermeter wavelength
                    tuneTime= pendingClearSled()                                 #Wait for pending bit to clear via nop
                    monTime = monChannellock()
                    output = singleSaveData(startTime,tuneTime,monTime,wavemeter1,powermeter1)
                    test_file1.write(output)
                    it.logentry(time.time() + '=====> Turn off laser here')
                    it.resena(0)
                    output = singleSaveData(startTime,tuneTime,monTime,wavemeter1,powermeter1)
                    test_file1.write(output)
                    timeout = random.uniform(0,10)
                    it.logentry("===>delay of:",str(timeout))
                    waitfortimeout(timeout=timeout)
                    
    #gotoDefault()
    test_file1.close()
    it.disconnect()
    print "Test Complete"
    turnOffpowersupplies(ps)
###########################################################################################################################################
###########################################################################################################################################

if __name__ == '__main__':

    try:
        runCase1()


    except (KeyboardInterrupt,Exception),e:
        raise
        print e

    
    




#############################################################################################################################################
#############################################################################################################################################




    
