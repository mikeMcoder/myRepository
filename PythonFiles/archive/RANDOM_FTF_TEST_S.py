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
    testName = 'Random_Ftf_Test'
    channelList = []
    com_port = 3
    iteration = 3
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
            for pwr in parameters.values()[13]:                    #list of power levels
                setPowerS(pwr)                                                                  #set power levels for test
                pendingClearS()
                for cycle in range(iteration):
                    print 'ITERATION:', cycle + 1
                    channelList = createChannelList(start=1, stop=97, step=10) #create sequential sequence
                    for chn in channelList:                                    #loop to select channel
                        clearAlarmsS()                                           #Clear alarms
                        setChannelS(chn)                                         #Change to a channel
                        freq = it.lf()[1]
                        setPowerMeter1Wavelength(freq)                          #change the powermeter wavelength
                        monChannellockS()                                        #Wait for pending bit to clear via nop
                        ftfList = createRandomFtfList(start=-6000,stop=6000+10,step=100)
                        for i in range(10):
                            ftf = random.choice(ftfList)
                            clearAlarmsS()
                            setFtfS(ftf)
                            tuneTime = pendingClearS()
                            waitfortimeoutS(timeout=15)
                            output = singleSaveDataS(startTime,tuneTime)
                            test_file1.write(output)
                        setFtfS(0)
                        pendingClearS()
                        waitfortimeoutS(timeout=10)
        gotoDefault()
        test_file1.close()

    except (KeyboardInterrupt,Exception),e:
        test_file1.close()
        print e
    test_file1.close()
    it.disconnect()
    
    




#############################################################################################################################################
#############################################################################################################################################




    
