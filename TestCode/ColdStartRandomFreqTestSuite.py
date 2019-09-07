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
g.InitPin()def huaweiPowerSupplySequence():
    x1,x2,ps1,ps2 = setpowerSupply()                                                                   #Initialize power supplies
    resetLow(g)                                                                                  #set the reset line low
    time.sleep(.04)                                                                              #delay 40ms
    supplyOff(ps1)                                                                               #turn supply off
    time.sleep(.850)                                                                             #delay 850ms
    supplyOn(ps1)                                                                                # turn supply on
    time.sleep(.3)                                                                               #delay 260ms
    resetHigh(g)                                                                                 #set reset line high
    time.sleep(.260)                                                                             #delay of 260ms before another reset
    reset(.02,g)                                                                                 #reset with 20 ms pulsewidth
    time.sleep(.5)

def runCase1():

    testName = 'Cold_Start_Random_Frequency_Test'
    channelList = []
    com_port = 3
    iteration = 1
    dwellT = 2
    try:
        
        wavemeter1,powermeter1,com_port1 = connectInstrument()      #initialize intruments
        x1,x2,ps1,ps2 = setpowerSupply()
        it.connect(com_port,115200)                                       #open port
        setComslog(testName)   
        instrumentInfo,parameters = showInitialParameters(wavemeter1)                           #get the initial parameters as a dictionary
        folderPath = createNewDirectory(name=testName)              #Createfolder
        test_name1,test_file1 = singlecreateFile(folderPath,testName,parameters,instrumentInfo)#createfile
        #test_file1 = open(folderPath + '\\' + test_name1 + '.txt','w')
        huaweiPowerSupplySequence()                                #turn on huawei power supply sequence
        readMready()                                               #wait for mready bit to be 1
        turnOnLaser()
        startTime = time.time()
        for i in parameters.values()[2]:
            print 'SET ADT:%d'%i, '=', it.mcb()[1].fieldAdt()
            for pwr in parameters.values()[13]:                    #list of power levels
                for cycle in range(iteration):
                    print 'ITERATION:', cycle + 1
                    channelList = createRandomChannelList(start=1,stop=97) #create sequential sequence
                    for chn in channelList:
                        supplyOff(ps1)
                        print("Hold for 2 min") #loop to select channel
                        time.sleep(dwellT)
                        huaweiPowerSupplySequence()                                #turn on huawei power supply sequence
                        readMready()                                               #wait for mready bit to be 1
                        it.setpassword()
                        waitfortimeout(timeout=30)
                        clearAlarms()                                           #Clear alarms
                        it.mcb(adt=i)                                           #set the adt bit in the mcb register
                        setPower(pwr)                                           #set power levels for test
                        setChannel(chn)                                         #Change to a channel
                        it.resena(1)                                            #turn on the laser                    
                        freq = it.lf()[1]
                        powermeter1.setFrequency(freq)                          #change the powermeter wavelength
                        tuneTime= pendingClear()                                 #Wait for pending bit to clear via nop
                        monTime = monChannellock()
                        output = singleSaveData(startTime,tuneTime,monTime,wavemeter1,powermeter1)
                        test_file1.write(output)
                    
        gotoDefault()
        test_file1.close()

    except (KeyboardInterrupt,Exception),e:
        test_file1.close()
        raise
        print e
    test_file1.close()
    it.disconnect()
    

###########################################################################################################################################
###########################################################################################################################################

if __name__ == '__main__':
    
    try:
        runCase1()
    except:
        print "Test Fails"

    

    
    




#############################################################################################################################################
#############################################################################################################################################




    
