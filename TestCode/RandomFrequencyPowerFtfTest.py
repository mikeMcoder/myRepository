import math
import struct
import sys
import os
import time
import instrumentDrivers as inst
import ConfigParser as parser
sys.path.append(os.path.abspath('.'))

utility = open('RegressionUtility_K.py')
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

def turnOnpowersupplies():
    ps = inst.psAG3631('gpib0::06')
    ps.connect()
    ps.setOutputState(state='ON')
    return ps

def turnOffpowersupplies(ps):
    ps.setOutputState(state='OFF')


###########################################################################################################################################
###########################################################################################################################################

if __name__ == '__main__':
    testName = 'RandomFreqChanFTFTest'
    channelList = []
    com_port = 3
    iteration = 100
    try:
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
        readMready()                                               #wait for mready bit to be 1
        turnOnLaser()                                              #turnonlaser
        channelList = createRandomChannelList(start=1,stop=105)     #create random channels
        print channelList
        powerList = createRandomPowerList()              #create random power
        print powerList
        ftfList =  createRandomFtfList()                  #create random ftf
        print ftfList
        startTime = time.time()
        count = 0
        for i in parameters.values()[2]:
            it.mcb(adt=i) 
            print 'SET ADT:%d'%i, '=', it.mcb()[1].fieldAdt()
            for repeat in range(1):
                for chan,pwr,ftf in map(None,channelList,powerList,ftfList): 
                    count+=1
                    if count == 1000:
                        break
                    clearAlarms()
                    setPower(pwr)
                    it.ftf(ftf)
                    print "set ftf to:",ftf
                    setChannel(chan)
                    freq = it.lf()[1]
                    setPowerMeter1Wavelength(freq)                           #change the powermeter wavelength
                    tuneTime= pendingClear()                                 #Wait for pending bit to clear via nop
                    monTime = monChannellock()
                    output = singleSaveData(startTime,tuneTime,monTime)
                    test_file1.write(output)
                    
        gotoDefault()
        test_file1.close()
    
    
        test_file1.close()
        it.disconnect()
        print "Test Complete"
        turnOffpowersupplies(ps)
    
    except (KeyboardInterrupt,Exception),e:
        test_file1.close()
        print e
    
    




#############################################################################################################################################
#############################################################################################################################################




    
