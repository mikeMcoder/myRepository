import os
import sys


ftf = raw_input('Enter FTF:')

it.connect(3)
time.sleep(1)
it.setpassword()
print 'set to channel'
it.channel(90)
it.resena(1)
time.sleep(30)
print 'channel locked'
print 'Set ftf Xghz'
it.ftf(int(ftf))
timestart = time.time()
lapse = time.time()-timestart
while it.nop()[1].fieldPending().toBinaryString() != '00000000':
    lapse = time.time()-timestart
    print 'LapseTime:', lapse, 'NOP:',it.nop()[1].fieldPending().toBinaryString(), 'FTF:',it.ftf(),'CHAN:', it.lf()[1],'OOP:',it.oop()[1]
'TotalTime:',lapse
it.ftf(0)
it.disconnect()