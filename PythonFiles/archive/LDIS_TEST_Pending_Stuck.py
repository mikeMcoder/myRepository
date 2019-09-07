import sys
import os
import time
import aa_gpio.gpio

g = aa_gpio.gpio.gpio()
g.InitPin()

wait = 6

it.connect(3)
print it.release()
############Test1##########
it.resena(1)
print "EnableLaser"
for i in range(40):
    print "PendingStat:",hex(int(it.nop()[1].data()))
    time.sleep(.2)
    if i == 39:
        g.LDIS_N_Disable()
        print "Monitor while LDIS is disabled"
        for i in range(75):
            print "PendingStat:",hex(int(it.nop()[1].data()))
            time.sleep(.2)
        print "Monitor while LDIS is enabled"
        g.LDIS_N_Enable()
        for i in range(25):
            print "PendingStat:",hex(int(it.nop()[1].data()))
            time.sleep(.2)



############Test2##########
##it.resena(1)
##time.sleep(1)
##it.resena(0)
##time.sleep(5)
##it.resena(1)
##print "Disable Laser"
##g.LDIS_N_Disable()
##for i in range(50):
##    print "PendingStat:",hex(int(it.nop()[1].data())) #The bug reads x810 then x910 then x810
##    time.sleep(.5)
###it.resena(1)
##it.write('\x81\x32\x00\x08')
##it.read(4)
##print "Enable Laser"
##for i in range(50):
##    print "PendingStat:",hex(int(it.nop()[1].data()))
##    time.sleep(.5)
    
    





            
            


    


