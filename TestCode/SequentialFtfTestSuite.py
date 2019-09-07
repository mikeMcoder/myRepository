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

testName = 'Sequential_Ftf_Test'
channelList = []
com_port = 3
iteration = 3
baud = 115200

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
    it.connect(com_port,baud)                                       #open port
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
        for pwr in parameters.values()[13]:                    #list of power levels
            setPower(pwr)                                                                  #set power levels for test
            pendingClear()
            for cycle in range(iteration):
                print 'ITERATION:', cycle + 1
                channelList = createChannelList(start=1, stop=97, step=5) #create sequential sequence
                for chn in channelList:                                    #loop to select channel
                    clearAlarms()                                           #Clear alarms
                    setChannel(chn)                                         #Change to a channel
                    freq = it.lf()[1]
                    powermeter1.setFrequency(freq)                          #change the powermeter wavelength
                    monChannellock()                                        #Wait for pending bit to clear via nop
                    ftfList = createFtfList(start=-6000, stop = 7000, step = 1000)
                    for ftf in ftfList:
                        clearAlarms()
                        setFtf(ftf)
                        tuneTime = pendingClear()
                        waitfortimeout(timeout=15)
                        monTime = 0.0
                        output = singleSaveData(startTime,tuneTime,monTime,wavemeter1,powermeter1)
                        test_file1.write(output)
                    setFtf(0)
                    pendingClear()
                    time.sleep(10)
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
        raise
        test_file1.close()
        print e
        

    
    




#############################################################################################################################################
#############################################################################################################################################




    
