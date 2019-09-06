import os
import sys
import time



#pseudocode
#connect to unit
it.connect(3)
time = str(time.asctime())
#issue resena 1
it.resena(1)
#Clear all status registers
it.statusW
#poll oop, ststusW register, pending nop register. Time stamp transient
pending = it.nop()[1].fieldPending().toBinaryString()
wpwr = it.statusW()[1].fieldWpwr()
wpwrl = it.statusW()[1].fieldWpwrl()

while pending[7] != '0':
    print time, 'Pending:',pending,'wpwr',wpwr,'wpwrl',wpwrl
    pending = it.nop()[1].fieldPending().toBinaryString()
    wpwr = it.statusW()[1].fieldWpwr()
    wpwrl = it.statusW()[1].fieldWpwrl()
    time = str(time.asctime())
print time, 'Pending:',pending,'wpwr',wpwr,'wpwrl',wpwrl
print "stop test"
    
     
    


