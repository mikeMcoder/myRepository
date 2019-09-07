import random
import math
import struct
import sys
import os
import time
import ConfigParser as parser
sys.path.append(os.path.abspath('.'))
import ITLA.Register as Register
import RegressionUtility_I


class CT1class(object):
    def __init__(self):
        self.it = it
        self.register = None
        self.retdat = None
        self. byte1and2 = None
        self.byte3and4 = None
        self.temp = None
        self.tempLaser = None
        self.tempLaserfloat = None
        
    def ReadRegAbs(self,writedata):
        #register = (writedata & 0x00FF0000 )/ 0x00010000
        self.register = writedata & 0xFF
        #data = writedata & 0x0000FFFF
        self.retdat=self.it.register(ITLA.Register.Register(address=register,data=0),write=False)
        #print retdat
        return (self.retdat[1].data())

    def WriteRegAbs(self,writedata,Value):
        #register = (writedata & 0x00FF0000 )/ 0x00010000
        self.register = writedata & 0xFF
        #data = writedata & 0x0000FFFF
        self.retdat=it.register(ITLA.Register.Register(address=register,data=Value),write=True)
        #print retdat
        return (self.retdat[1].data())
        
    def getfloat(self):
        self.byte1and2 =  ReadRegAbs(0x0004a00B)
        self.byte3and4 =  ReadRegAbs(0x0004a00B)
        return(struct.unpack('<f',struct.pack('>H',self.byte1and2) +  struct.pack('>H',self.byte3and4 ))[0])

    def tempLaserfloat(self):
        self.temp =  ReadRegAbs(0x0004a058)
        self.tempLaser =  ReadRegAbs(0x0004a00B)
        self.tempLaserfloat = (struct.unpack('h', struct.pack('H', tempLaser))[0]/100.0) 
        print 'tempLaserfloat: %.02f'%self.tempLaserfloat
        return self.tempLaserfloat
##        tempCase =  CT1.ReadRegAbs(0x0004a00B)
##        tempCasefloat = (struct.unpack('h', struct.pack('H', tempCase))[0]/100.0)
##        print 'tempCasefloat:%.02f'%tempCasefloat 
##        tempEtalon =  CT1.ReadRegAbs(0x0004a00B)
##        tempEtalonfloat = (struct.unpack('h', struct.pack('H', tempEtalon))[0]/100.0)
##        print 'tempEtalonfloat:%.02f'%tempEtalonfloat 
##        powerLaser =  CT1.ReadRegAbs(0x0004a042)
##        powerLaserfloat = (struct.unpack('h', struct.pack('H', powerLaser))[0]/100.0)
##        print 'powerLaserfloat:%.02f'%powerLaserfloat
##        temp =  CT1.ReadRegAbs(0x0004a065)
##        vcc =  CT1.ReadRegAbs(0x0004a00B)
##        vccfloat = (vcc/100.0)
##        print 'vccfloat:%.02f'%vccfloat 
##        temp =  CT1.ReadRegAbs(0x0004a057)
##        LosaTECI =  CT1.ReadRegAbs(0x0004a00B)
##        LosaTECIfloat =(struct.unpack('h', struct.pack('H', LosaTECI))[0]/10.0)
##        print 'LosaTECIfloat:%.02f'%LosaTECIfloat 
##        LaserI =  CT1.ReadRegAbs(0x0004a00B)
##        LaserIfloat=(LaserI/10.0)
##        print 'LaserIfloat:%.02f'%LaserIfloat
##        WosaTECI =  CT1.ReadRegAbs(0x0004a00B)
##        WosaTECIfloat=(struct.unpack('h', struct.pack('H', WosaTECI))[0]/10.0)
##        print 'WosaTECIfloat:%.02f'%WosaTECIfloat
##        soaI =  CT1.ReadRegAbs(0x0004a00B)
##        soaIfloat=(soaI/10.0) 
##        print 'soaIfloat:%.02f'%soaIfloat
##        temp =  CT1.ReadRegAbs(0x0004a0B8)
##        memsx = getfloat()
##        print 'memsxfloat:%.04f'%memsx
##        
##        data = str(tempLaserfloat)+','+str(tempCasefloat)+','+str(tempEtalonfloat)+','+str(powerLaserfloat)+','+str(vccfloat) +','+str(LosaTECIfloat)+','+ str(LaserIfloat)+ ','+ str(WosaTECIfloat)+','+str(soaIfloat)+ ',' +str(memsx)
##        return data
        print data