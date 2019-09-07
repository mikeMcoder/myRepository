import InstrumentDrivers_DS as inst
import time
import sys

def P3_3ONF():
    
    
    P3_3ON.connect()
    P3_3ON.setOutputState('ON')
    P3_3ON.disconnect()

def Pcur():
    #P3_3ON = inst.HP3631A(0,9)
    P3_3ON.connect()
    cur = P3_3ON.getCurr()
    print 'current',cur
    if cur<0.050:
        raise 'current drop'
    P3_3ON.disconnect()
    
def POFF():
    #P3_3ON = inst.HP3631A(0,9)
    P3_3ON.connect()  
    P3_3ON.setOutputState('OFF')
    P3_3ON.disconnect()

def cycle(BAUDRATE):
    print 'Power On'
    P3_3ONF()
    print 'Sleep for 5 seconds'
    sys.stdout.flush()
    time.sleep(5)
    sys.stdout.flush()
    Pcur()
    print 'read release()'
    pull(it.baudrate())
    print 'Change Baudrate: ', BAUDRATE
    it.baudrate(BAUDRATE)
    print 'read release()'
    pull(BAUDRATE)
    print 'Gencfg'
    it.genCfg(1)
    print 'Sleep for 1 seconds'
    time.sleep(1)
    print 'Power Off'
    POFF()
    print 'Sleep for 10 seconds'
    sys.stdout.flush()
    time.sleep(10)
    sys.stdout.flush()
    print 'Power On'
    P3_3ONF()
    print 'Sleep for 5 seconds'
    sys.stdout.flush()
    time.sleep(5)
    sys.stdout.flush()
    Pcur()
    print 'read release()'
    pull(BAUDRATE)
    print 'Baudrate after power cycle: ', it.baudrate()
    print 'Power Off'
    POFF()
    print 'Sleep for 10 seconds'
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
        print 'current',P3_3ON.getCurr()
        raise 'Error ',c3
    else:
        print 'release1:',c1
        print 'release2:',c2
        print 'release3:',c4
#clear buffer, calling it.release() max 3 times 

#######
## Main
#######
GPIB_address = input('GPIB address')
P3_3ON = inst.HP3631A(0,GPIB_address)
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
    cycle(57600)
    cycle(115200)
    cycle(9600)


