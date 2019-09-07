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

#serialnumber
#producttype
#testname
#

###########################################################################################################################################
###########################################################################################################################################

if __name__ == '__main__':
    testName = 'Sequential_Power_Test'
    channelList = []
    com_port = 3
    iteration = 6
    try:
        
        wavemeter1,powermeter1,com_port = connectInstrument()      #initialize intruments
        it.connect(com_port)                                       #open port
        setComslog(testName)   
        instrumentInfo,parameters = showInitialParameters(wavemeter1)                           #get the initial parameters as a dictionary
        folderPath = createNewDirectory(name=testName)              #Createfolder
        test_name1,test_file1 = singlecreateFile(folderPath,testName,parameters,instrumentInfo)#createfile
        #test_file1 = open(folderPath + '\\' + test_name1 + '.txt','w')
        huaweiPowerSupplySequence()                                #turn on huawei power supply sequence
        readMready()                                               #wait for mready bit to be 1
        turnOnLaserS()                                              #turnonlaser
        startTime = time.time()
        for i in parameters.values()[2]:
            it.mcb(adt=i)                                          #set the adt bit in the mcb register
            print 'SET ADT:%d'%i, '=', it.mcb()[1].fieldAdt()
            channelList = createChannelList(start=1,stop = 97,step = 10)
            for chn in channelList:                                #loop to select channel
                clearAlarmsS()                                      #Clear alarms
                setChannelS(chn)                                    #Change to a channel
                freq = it.lf()[1]
                setPowerMeter1Wavelength(freq)                     #change the powermeter wavelength
                pendingClearS()                                     #Wait for pending bit to clear via nop
                monChannellockS()
                for cycle in range(iteration):
                    print 'ITERATION:', cycle + 1
                    powerList = [1550,1500,1400,1300,1200,1100,1000,1100,1200,1300,1400,1500]
                    for pwr in powerList:                          #list of power levels
                        setPowerS(pwr)                              #set power levels for test
                        tuneTime= pendingClearS()                   #Wait for pending bit to clear via nop
                        monTime = monChannellockS()
                        waitfortimeoutS(timeout=15)
                        output = singleSaveDataS(startTime,tuneTime,monTime)
                        test_file1.write(output)

        gotoDefault()
        test_file1.close()

    except (KeyboardInterrupt,Exception),e:
        test_file1.close()
        print e
    test_file1.close()
    it.disconnect()
    
    




#############################################################################################################################################
#############################################################################################################################################




    
