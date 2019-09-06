import instrumentDrivers as inst
import time

finishT = 10800
ps = inst.psAG3631('GPIB0::06')
ps.connect()


it.connect(3,115200)
it.setpassword()
it.logging(True)
it.logfile('nanoTestRunnawayIssue.txt')

it.resena(1)
it.channel(50)
time.sleep(20)
startT = time.time()
lapseT = time.time() - startT
while lapseT<= finishT:
    print lapseT,ps.getCurr(), it.readx99().f1temp, it.readx99().f2temp,it.readx99().siblocktemp, it.readx99().sled_temperature, it.readx99().demodrealerr,\
          it.readx99().gain_medium_current, it.readx99().photodiode_current,float(it.temps()[1][1][1])/100
    time.sleep(.5)

    lapseT = time.time() - startT

print "Test Done"
it.disconnect()

    
