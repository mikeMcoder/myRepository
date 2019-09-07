import os
import sys
import time
sys.path.append('.')
import aa_gpio.gpio
g = aa_gpio.gpio.gpio()




#Initialize Aardvark
g.InitPin()

#Connect to unit
it.connect(3)
it.resena(1)
print "Tune to Channel"
time.sleep(15)
g.LDIS_N_Disable()
print "Disable Laser"
it.resena(1)
for i in range(5):
    print it.resena()
time.sleep(1)
print "1 sec delay done enable laser and read again"
g.LDIS_N_Enable()
print it.resena()
print "Turn on laser"
it.resena(1)
print it.resena()
it.disconnect()
