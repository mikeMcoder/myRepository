import time
import random
import sys
import os




it.connect(3)
it.resena(1)
time.sleep(30)
for i in range(500):
    for ch in range(1,96,1):
        print it.channel(ch)
        print it.channel()
        print it.temps(),it.oop(),it.currents()
        if it.channel()[0] != 'OK':
            raise 'FAIL'
                        
    

##for i in range(500):
##    a = it.write('\x31\x30\x00\x01') #1
##    a1 = it.read(4)
##    print a,a1
##    b = it.write('\x01\x30\x00\x02') #2
##    b1 = it.read(4)
##    print b,b1
##    c = it.write('\x11\x30\x00\x03') #3
##    c1= it.read(4)
##    print c,c1
##    d = it.write('\x61\x30\x00\x04') #4
##    d1 = it.read(4)
##    print d,d1
##    e = it.write('\x71\x30\x00\x05') #5
##    e1= it.read(4)
##    print e,e1
##    d=it.write('\x41\x30\x00\x06')   #6
##    d1=it.read(4)
##    print d,d1
##    e = it.write('\x51\x30\x00\x07') #7
##    e1= it.read(4)
##    print e,e1
##    f = it.write('\xA1\x30\x00\x08') #8
##    f1 = it.read(4)
##    print f,f1
##    g = it.write('\xB1\x30\x00\x09') #9
##    g1 = it.read(4)
##    print g,g1
##    h =it.write('\x81\x30\x00\x0A') #10
##    h1 =it.read(4)
##    print h,h1

 	