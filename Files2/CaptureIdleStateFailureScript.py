import time
import sys

sys.path.sort()


def clearAlarms():
    it.statusF(1,1,1,1,1,1,1,1)
    it.statusW(1,1,1,1,1,1,1,1)
    
def waitfortimeout(timeout=25.0):
    sys.stdout.write('Waiting ' + str(timeout) + ' seconds...')
    starttime = time.time()
    loopcount = 0
    while True:
        loopcount = loopcount + 1
        if not loopcount % 100:
            sys.stdout.write('.')
            sys.stdout.flush()
        it.readx99()
        it.nop()
        if time.time() - starttime > timeout:
            print 'Done'
            return (time.time() - starttime)

it.connect(3,115200)
it.setpassword(3)
it.logging(True)
it.logfile('IDLESTATE_x99.txt')
chnLst = [5,50,100]
failcount = 0
time.sleep(1)
for channel in chnLst:
    it.resena(1)
    it.pwr(1300)
    it.ftf(3000)
    time.sleep(10)
    "START"
    pwr = it.opsh()[1]
    it.pwr(pwr)#back to default
    it.ftf(0)#set to 0ghz offset
    it.resena(0)
    waitfortimeout(timeout=1)
    it.resena(1)
    waitfortimeout(timeout=15)
    pollTime=0
    pollLimit = 10
    it.mcb(adt = 1)
    print '*' * 10,  'LASER TRANSIENT' ,'*' * 10
    it.channel(channel)
    it.resena(0)
    waitfortimeout(timeout=10)
    clearAlarms()
    sledtempCheck = it.readx99().sled_temperature
    if sledtempCheck >=60 or sledtempCheck<=40:
        failcount +=1
        it.logentry('Fail Flag:' + str(failcount))
        print '( -  |  - )( -  |  - )( -  |  - )( -  |  - )Fail Count:',failcount ,'( -  |  - )( -  |  - )( -  |  - )( -  |  - )'                  
    it.resena(1)
    startTime= time.time()
    pollTime =time.time()-startTime
    while pollTime <= pollLimit:
        x99 = it.readx99()
        print 'TIME:', pollTime,'PENDING:',it.nop()[1].fieldPending().toBinaryString(),'STATUSW:',hex(int(it.statusW()[1].data())),'STATUSF:',hex(int(it.statusF()[1].data())),'OOP:',it.oop()[1],'F1:',x99.f1temp,\
              'F2:',x99.f2temp,'SiBlock:',x99.siblocktemp,'DemodR:',x99.demodrealerr,'GMI:',x99.gain_medium_current,'PD:',x99.photodiode_current,'SLED:',x99.sled_temperature,'StateMachine:',x99.tunerstate
        pollTime =time.time()-startTime
        time.sleep(.100)
##        print 'TIME:', pollTime,'PENDING:',it.nop()[1].fieldPending().toBinaryString(),'StateMachine:',it.readx99().tunerstate
##        pollTime =time.time()-startTime
##        time.sleep(.100)
        if it.readx99().tunerstate == 'TUNER_IDLE':
            print 'TIME:', pollTime,'PENDING:',it.nop()[1].fieldPending().toBinaryString(),'STATUSW:',hex(int(it.statusW()[1].data())),'STATUSF:',hex(int(it.statusF()[1].data())),'OOP:',it.oop()[1],'F1:',x99.f1temp,\
            'F2:',x99.f2temp,'SiBlock:',x99.siblocktemp,'DemodR:',x99.demodrealerr,'GMI:',x99.gain_medium_current,'PD:',x99.photodiode_current,'SLED:',x99.sled_temperature,'StateMachine:',x99.tunerstate
            print 'TIME:', pollTime,'PENDING:',it.nop()[1].fieldPending().toBinaryString(),'STATUSW:',hex(int(it.statusW()[1].data())),'STATUSF:',hex(int(it.statusF()[1].data())),'OOP:',it.oop()[1],'F1:',x99.f1temp,\
            'F2:',x99.f2temp,'SiBlock:',x99.siblocktemp,'DemodR:',x99.demodrealerr,'GMI:',x99.gain_medium_current,'PD:',x99.photodiode_current,'SLED:',x99.sled_temperature,'StateMachine:',x99.tunerstate
            print "Failure Found!"
            break
it.disconnect()
print ("Test Done")
            
        