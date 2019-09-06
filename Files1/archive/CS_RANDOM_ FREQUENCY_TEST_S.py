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


###########################################################################################################################################
###########################################################################################################################################

if __name__ == '__main__':
    testName = 'Cold_Start_Random_Frequency_Test'
    channelList = []
    com_port = 3
    iteration = 3
    dwellT = 120
    try:
        
        wavemeter1,powermeter1,com_port = connectInstrument()      #initialize intruments
        x1,x2,ps1,ps2 = setpowerSupply()
        it.connect(com_port)                                       #open port
        setComslogS(testName)   
        instrumentInfo,parameters = showInitialParameters(wavemeter1)                           #get the initial parameters as a dictionary
        folderPath = createNewDirectory(name=testName)              #Createfolder
        test_name1,test_file1 = singlecreateFile(folderPath,testName,parameters,instrumentInfo)#createfile
        #test_file1 = open(folderPath + '\\' + test_name1 + '.txt','w')
        huaweiPowerSupplySequence()                                #turn on huawei power supply sequence
        readMready()                                               #wait for mready bit to be 1
        turnOnLaserS()
        startTime = time.time()
        for i in parameters.values()[2]:
            print 'SET ADT:%d'%i, '=', it.mcb()[1].fieldAdt()
            for pwr in parameters.values()[13]:                    #list of power levels
                for cycle in range(iteration):
                    print 'ITERATION:', cycle + 1
                    channelList = createRandomChannelList(start=1,stop=97) #create sequential sequence
                    for chn in channelList:
                        supplyOff(ps2)
                        print("Hold for 2 min") #loop to select channel
                        time.sleep(dwellT)
                        huaweiPowerSupplySequence()                                #turn on huawei power supply sequence
                        readMready()                                               #wait for mready bit to be 1
                        #it.setpassword()
                        waitfortimeoutS(timeout=30)
                        clearAlarmsS()                                           #Clear alarms
                        it.mcb(adt=i)                                           #set the adt bit in the mcb register
                        setPowerS(pwr)                                           #set power levels for test
                        setChannelS(chn)                                         #Change to a channel
                        it.resena(1)                                            #turn on the laser                    
                        freq = it.lf()[1]
                        setPowerMeter1Wavelength(freq)                          #change the powermeter wavelength
                        tuneTime= pendingClearS()                                 #Wait for pending bit to clear via nop
                        monTime = monChannellockS()
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




    
