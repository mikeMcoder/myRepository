
def P3_3ONF():


    #import sys 
    #sys.path.append(r'C:\Documents and Settings\rcanwa-lltltest\Desktop\ITLA2TestCode2')
    #sys.path.append(r'C:\Documents and Settings\rcanwa-lltltest\Desktop\LUX\pCode')
    import InstrumentDrivers_DS as inst
    #import time as tt
    
   
    P3_3ON = inst.HP3631A(0,9)
    #P5_2ON = inst.HP3631A(0,10)
    P3_3ON.connect()
    #P5_2ON.connect()
    

    P3_3ON.setOutputState('ON')
    
    #P5_2ON.setOutputState('ON')
    
    
    
    P3_3ON.disconnect()
    #P5_2ON.disconnect()

def POFF():


    #import sys 
    #sys.path.append(r'C:\Documents and Settings\rcanwa-lltltest\Desktop\ITLA2TestCode2')
    #sys.path.append(r'C:\Documents and Settings\rcanwa-lltltest\Desktop\LUX\pCode')
    import InstrumentDrivers_DS as inst
    import time as tt
    
   
    P3_3ON = inst.HP3631A(0,9)
    #P5_2ON = inst.HP3631A(0,10)
    P3_3ON.connect()
    #P5_2ON.connect()

    #P5_2ON.setOutputState('OFF')    
    P3_3ON.setOutputState('OFF')
        
    P3_3ON.disconnect()
    #P5_2ON.disconnect()

def cycle(BAUDRATE):
    print 'Power On'
    P3_3ONF()
    print 'Sleep for 15 seconds'
    print
    time.sleep(15)
    print
    print it.release()
    print it.release()
    print it.release()
    print
    print 'Change Baudrate: ', BAUDRATE
    it.baudrate(BAUDRATE)
    print 'Gencfg'
    print
    it.genCfg(1)
    time.sleep(1)
    print 'Power Off'
    print
    POFF()
    print 'Sleep for 10 seconds'
    print
    time.sleep(10)
    print 'Power On'
    print    
    P3_3ONF()
    print it.release()
    print it.release()
    print it.release()
    print
    print 'Baudrate after power cycle: ', it.baudrate()
    print    
    print 'Power Off'
    print
    POFF()
    print 'Sleep for 10 seconds'
    print
    time.sleep(10)


#######
## Main
#######
import time
NUM_ITERATIONS = 5000
for i in range(NUM_ITERATIONS):
    print '####################################'
    print 'iteration :',i+1
    print '####################################'
    print 'Number of iterations left:',NUM_ITERATIONS-(i+1)
    print
    cycle(19200)
    cycle(38400)
    cycle(115200)
    cycle(9600)


