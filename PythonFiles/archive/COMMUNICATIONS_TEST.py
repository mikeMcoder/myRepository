import sys
import os
import sys
import instrumentDrivers as inst
import time
import math
import aa_gpio.gpio
g = aa_gpio.gpio.gpio()
sys.path.append(os.path.abspath('.'))

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'

P3_3 = inst.psAG3631('GPIB0::06')
PN5_2 = inst.psAG3631('GPIB0::07')

port = 3
error = 0
error1 = 0

def Supply_3_3ON():    
    P3_3.setOutputState('ON')

    
def Supply_3_3OFF():
    P3_3.setOutputState('OFF')


def Supply_5_2ON():    
    PN5_2.setOutputState('ON')

    
def Supply_5_2OFF():
    PN5_2.setOutputState('OFF')



P3_3.connect()
PN5_2.connect()


it.connect(port)
starttime = time.time()
it.debugRS232(1)
print 'Serial NUmber:',it.serNo
print 'Time:',time.asctime
if __name__ == '__main__':
    
    #Turn on suply sequence
        ####MAIN####
        Supply_5_2OFF()
        time.sleep(.06)
        Supply_3_3OFF()
        time.sleep(.6)
        Supply_5_2ON()
        time.sleep(.045)
        Supply_3_3ON()
        time.sleep(1)
        it.resena(1)
        
        
        while 1:
            nop = it.nop()
            statusF = it.statusF()[1].data()
            statusW = it.statusW()[1].data()
            #print nop
            if nop[0]=='' or statusF =='' or statusW  =='':
                print 'error'
                print nop[0]
                print statusF
                print statusW
                error += 1
                if error == 1:
                    duration = time.time()- starttime
                    print "Duration:%d" %duration
                    raise"Stop Communication Issue"
                
            elif nop[0]=='No response' or statusF=='No response'or statusW  == 'No response':
                print 'error1'
                print nop[0]
                print statusF
                print statusW
                error1 += 1
                if error1 == 1:
                    duration1 = time.time()- starttime
                    print "Duration:%d"%duration1
                    raise"Stop Communication Issue"
                
                

        



        
     
it.disconnect()
