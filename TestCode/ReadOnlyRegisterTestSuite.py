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

testName = 'Sequential_Frequency_Test'
channelList = []
com_port = 3
iteration = 3


def runCase1():
        
    it.connect(com_port)
    print it.buildstring()
    
    
    for i in range(100):
        print it.devTyp()
    
    
    for i in range(100):
        print it.mfgr()
    
    
    for i in range(100):
        print it.model()
    
    for i in range(100):
        print it.serNo()
    
    for i in range(100):
        print it.mfgDate()
    
    for i in range(100):
        print it.release()
    
    
    for i in range(100):
        print it.buildstring()
    
    
    for i in range(100):
        print it.relBack()
    
    for i in range(100):
        print it.aeaEac()
    
    
    for i in range(100):
        print it.aeaEar()
    
    
    for i in range(100):
        print it.lstResp()
    
    
    for i in range(100):
        print it.dlStatus()
    
    
    for i in range(100):
        print it.lf()
    
    
    for i in range(100):
        print it.oop()
    
    
    for i in range(100):
        print it.ctemp()
    
    
    for i in range(100):
        print it.ftfr()
    
    
    for i in range(100):
        print it.opsh()
    
    
    for i in range(100):
        print it.opsl()
    
    
    for i in range(100):
        print it.lfh()
    
    
    for i in range(100):
        print it.lfl()
    
    for i in range(100):
        print it.lgrid()
    
    
    for i in range(100):
        print it.currents()
    
    
    for i in range(100):
        print it.temps()
    
    
    for i in range(100):
        print it.age()
        
    it.disconnect()
    print "Test Complete"
    
if __name__=='__main__':
    runCase1()
    













    
    






    