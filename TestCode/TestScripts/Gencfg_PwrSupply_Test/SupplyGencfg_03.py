
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
    sys.stdout.flush()
    time.sleep(1)
    sys.stdout.flush()
    print 'Change Baudrate: ', BAUDRATE
    it.baudrate(BAUDRATE)
    print
    pull(BAUDRATE)
    print
    print 'Gencfg'
    print
    it.genCfg(1)
    time.sleep(15)
    print 'Power Off'
    print
    POFF()
    print 'Sleep for 10 seconds'
    print
    sys.stdout.flush()
    time.sleep(10)
    sys.stdout.flush()
    print 'Power On'
    print    
    P3_3ONF()
    print
    pull(BAUDRATE)
    print
    print 'Baudrate after power cycle: ', it.baudrate()
    print    
    print 'Power Off'
    print
    POFF()
    print 'Sleep for 10 seconds'
    print
    sys.stdout.flush()
    time.sleep(10)
    sys.stdout.flush()

def pull(BAUDRATE):
    c0 = time.asctime()
    c1 = str(it.release())
    c2 = str(it.release())
    c3 = it.release()

    c4 = str(c3)
    c1 = c1.replace(',','')
    c2 = c2.replace(',','')
    c4 = c4.replace(',','')
    test_file = open("%s.csv"%(test_name),"a+")
    test_file.write(c0+","+str(BAUDRATE)+","+c1+","+c2+","+c4+"\n")
    test_file.close()
    if (c3[0]!='OK'):
        raise 'Error ',c3
    else:
        print 'release1:',c1
        print 'release2:',c2
        print 'release3:',c4
#clear buffer, calling it.release() max 3 times 

#######
## Main
#######
import time
import sys
c3 = ''
NUM_ITERATIONS = 5000
test_name = input('filename')
test_file = open("%s.csv"%(test_name),"w")
test_file.write("time,baudrate,release1, release2, release3\n")
test_file.close()
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


