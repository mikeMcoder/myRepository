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

testName = 'Sequential_Power_Test'
channelList = []
com_port = 3
iteration = 5

def turnOnpowersupplies():
    ps = inst.psAG3631('gpib0::06')
    ps.connect()
    ps.setOutputState(state='ON')
    return ps

def turnOffpowersupplies(ps):
    ps.setOutputState(state='OFF')
    
    

def runCase1():
    ps = turnOnpowersupplies()
    time.sleep(3)
    wavemeter1,powermeter1,com_port1 = connectInstrument()      #initialize intruments
    it.connect(com_port,115200)                                       #open port
    setComslog(testName)   
    instrumentInfo,parameters = showInitialParameters(wavemeter1)                           #get the initial parameters as a dictionary
    folderPath = createNewDirectory(name=testName)              #Createfolder
    test_name1,test_file1 = singlecreateFile(folderPath,testName,parameters,instrumentInfo)#createfile
    test_file1 = open(folderPath + '\\' + test_name1 + '.txt','w')
    huaweiPowerSupplySequence()                                #turn on huawei power supply sequence
    time.sleep(3)
    readMready()                                               #wait for mready bit to be 1
    turnOnLaser()                                              #turnonlaser
    startTime = time.time()
    for i in parameters.values()[2]:
        it.mcb(adt=i)                                          #set the adt bit in the mcb register
        print 'SET ADT:%d'%i, '=', it.mcb()[1].fieldAdt()
        channelList = createChannelList(start=1,stop = 97,step = 10)
        for chn in channelList:                                #loop to select channel
            clearAlarms()                                      #Clear alarms
            setChannel(chn)                                    #Change to a channel
            freq = it.lf()[1]
            powermeter1.setFrequency(freq)                     #change the powermeter wavelength
            pendingClear()                                     #Wait for pending bit to clear via nop
            monChannellock()
            for cycle in range(iteration):
                print 'ITERATION:', cycle + 1
                #powerList = [1550,1500,1400,1300,1200,1100,1000,1100,1200,1300,1400,1500]
                powerList = [1350,1300,1200,1100,1000,900,800,700,700,800,900,1000,1100,1200,1300,1350]
                for pwr in powerList:                          #list of power levels
                    setPower(pwr)                              #set power levels for test
                    tuneTime= pendingClear()                   #Wait for pending bit to clear via nop
                    monTime = monChannellock()
                    waitfortimeout(timeout=15)
                    output = singleSaveData(startTime,tuneTime,monTime,wavemeter1,powermeter1)
                    test_file1.write(output)

    gotoDefault()
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
        test_file1.close()
        raise
        print e

    




#############################################################################################################################################
#############################################################################################################################################




    
