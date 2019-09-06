import os
import sys
import time



it.connect(3)
print 'Set wPowTh to 0'
it.wPowTh(0)
wPowTh = it.wPowTh()
print 'wPowTh:', wPowTh[1]
it.resena(1)
while 1:
    pending = int(it.nop()[1].fieldPending().value())
    print time.asctime(),'NOP:',it.nop()[1].fieldPending().value()
    time.sleep(1)
    

    if pending == 0:
        'print pending cleared'
        break
for i in range(1000):
    print time.asctime(),'NOP:',it.nop()[1].fieldPending().value()
    
