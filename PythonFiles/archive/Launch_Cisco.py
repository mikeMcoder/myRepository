'''
NeoPhotonics CONFIDENTIAL
Copyright 2005-2015 NeoPhotonics Corporation All Rights Reserved.

The source code contained or described herein and all documents related to
the source code ("Material") are owned by NeoPhotonics Corporation or its
suppliers or licensors. Title to the Material remains with NeoPhotonics Corporation
or its suppliers and licensors. The Material may contain trade secrets and
proprietary and confidential information of NeoPhotonics Corporation and its
suppliers and licensors, and is protected by worldwide copyright and trade
secret laws and treaty provisions. No part of the Material may be used, copied,
reproduced, modified, published, uploaded, posted, transmitted, distributed,
or disclosed in any way without Intels prior express written permission. 
No license under any patent, copyright, trade secret or other intellectual
property right is granted to or conferred upon you by disclosure or delivery
of the Materials, either expressly, by implication, inducement, estoppel or
otherwise. Any license under such intellectual property rights must be express
and approved by NeoPhotonics in writing.

Include any supplier copyright notices as supplier requires NeoPhotonics to use.

Include supplier trademarks or logos as supplier requires NeoPhotonics to use,
preceded by an asterisk. An asterisked footnote can be added as follows:
*Third Party trademarks are the property of their respective owners.

Unless otherwise agreed by NeoPhotonics in writing, you may not remove or alter this
notice or any other notice embedded in Materials by NeoPhotonics or NeoPhotonics's
suppliers or licensors in any way.

    $Source: /data/development/cvs/Sundial2/Python/Launch.py,v $
    $Revision: 1.1 $
    $Date: 2007/04/18 19:45:16 $
    $Name: Sundial2_01_03_00_01 $
    
'''
import os
import sys
sys.path.append(os.path.abspath('.'))
import struct
import CT1
c = CT1.CT1class()
print 'DUITLA Internals instance as c'

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)



import ITLA.ITLA
class newITLAITLAITLA(ITLA.ITLA.ITLA,object):
    def register(self, register = None, write = 0):
        if register.name() == ITLA.Register.Register(ITLA.Register.AEA_EA).name():
            # create dummy return data
            register = ITLA.Register.Register(ITLA.Register.AEA_EA,2)
            return( ('OK',register) )
        if register.name() == ITLA.Register.Register(ITLA.Register.AEA_EAC).name():
            # create dummy return data
            register = ITLA.Register.Register(ITLA.Register.AEA_EAC)
            register.fieldIncr().value(2)
            register.fieldRai().value(1)
            return( ('OK',register) )
        return ( super(newITLAITLAITLA, self).register( register,  write ) )
    def setpassword(self,passwordlevel=None):
        self.register(ITLA.Register.Register(address=0x80,data=0x1428),write=True)
        self.register(ITLA.Register.Register(address=0x81,data=0x5700),write=True)

it = newITLAITLAITLA(t)
import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'


class CT1class:
    def ReadRegAbs(self,writedata):
        #register = (writedata & 0x00FF0000 )/ 0x00010000
        register = writedata & 0xFF
        #data = writedata & 0x0000FFFF
        retdat=it.register(ITLA.Register.Register(address=register,data=0),write=False)
        #print retdat
        return (retdat[1].data())

    def WriteRegAbs(self,writedata,Value):
        #register = (writedata & 0x00FF0000 )/ 0x00010000
        register = writedata & 0xFF
        #data = writedata & 0x0000FFFF
        retdat=it.register(ITLA.Register.Register(address=register,data=Value),write=True)
        #print retdat
        return (retdat[1].data())
        
def getfloat():
    byte1and2 =  CT1.ReadRegAbs(0x0004a00B)
    byte3and4 =  CT1.ReadRegAbs(0x0004a00B)
    return(struct.unpack('<f',struct.pack('>H',byte1and2) +  struct.pack('>H',byte3and4 ))[0])

def pendingClear1(datafile):

    starttime = time.time()
    alarmdat = 0xFFFF
    #while( CT1.ReadRegAbs(0x0004a000) & 0xFF00 ):
    tunetime = time.time() - starttime
    while(time.time() - starttime < 60 and (alarmdat & 0x7fff )!= 0):
        # clear alarms
        dataSet = readReg(tunetime)
        chn = it.lf()[1]
        timestamp = str(time.asctime())
        it.register(ITLA.Register.Register(address=ITLA.Register.STATUSW,data=0xFFFF),write=True)
        alarmdat = it.statusW()[1].data()
        datafile.write(timestamp + ',' + str(chn)  + ','+  dataSet + ',' + str(alarmdat) +'\n')
        tunetime = time.time() - starttime
        
    print 'ALARM:',alarmdat,'TUNETIME:',tunetime
    return tunetime
    

        
CT1=CT1class()

def readReg(tunetime=1):
    temp =  CT1.ReadRegAbs(0x0004a058)
    tempLaser =  CT1.ReadRegAbs(0x0004a00B)
    tempLaserfloat = (struct.unpack('h', struct.pack('H', tempLaser))[0]/100.0) 
    #print 'tempLaserfloat: %.02f'%tempLaserfloat
    tempCase =  CT1.ReadRegAbs(0x0004a00B)
    tempCasefloat = (struct.unpack('h', struct.pack('H', tempCase))[0]/100.0)
    #print 'tempCasefloat:%.02f'%tempCasefloat 
    tempEtalon =  CT1.ReadRegAbs(0x0004a00B)
    tempEtalonfloat = (struct.unpack('h', struct.pack('H', tempEtalon))[0]/100.0)
    #print 'tempEtalonfloat:%.02f'%tempEtalonfloat 
    powerLaser =  CT1.ReadRegAbs(0x0004a042)
    powerLaserfloat = (struct.unpack('h', struct.pack('H', powerLaser))[0]/100.0)
    #print 'powerLaserfloat:%.02f'%powerLaserfloat
    temp =  CT1.ReadRegAbs(0x0004a065)
    vcc =  CT1.ReadRegAbs(0x0004a00B)
    vccfloat = (vcc/100.0)
    #print 'vccfloat:%.02f'%vccfloat 
    temp =  CT1.ReadRegAbs(0x0004a057)
    LosaTECI =  CT1.ReadRegAbs(0x0004a00B)
    LosaTECIfloat =(struct.unpack('h', struct.pack('H', LosaTECI))[0]/10.0)
    #print 'LosaTECIfloat:%.02f'%LosaTECIfloat 
    LaserI =  CT1.ReadRegAbs(0x0004a00B)
    LaserIfloat=(LaserI/10.0)
    #print 'LaserIfloat:%.02f'%LaserIfloat
    WosaTECI =  CT1.ReadRegAbs(0x0004a00B)
    WosaTECIfloat=(struct.unpack('h', struct.pack('H', WosaTECI))[0]/10.0)
    #print 'WosaTECIfloat:%.02f'%WosaTECIfloat
    soaI =  CT1.ReadRegAbs(0x0004a00B)
    soaIfloat=(soaI/10.0) 
    #print 'soaIfloat:%.02f'%soaIfloat
    temp =  CT1.ReadRegAbs(0x0004a0B8)
    memsx = getfloat()
    temp =  CT1.ReadRegAbs(0x0004a0B8)
    memsy = getfloat()    
    #print 'memsxfloat:%.04f'%memsx
    print 'tempLaserfloat: %.02f'%tempLaserfloat,'tempCasefloat:%.02f'%tempCasefloat,'tempEtalonfloat:%.02f'%tempEtalonfloat,'powerLaserfloat:%.02f'%powerLaserfloat,'vccfloat:%.02f'%vccfloat\
          ,'LosaTECIfloat:%.02f'%LosaTECIfloat,'LaserIfloat:%.02f'%LaserIfloat,'WosaTECIfloat:%.02f'%WosaTECIfloat,'soaIfloat:%.02f'%soaIfloat,'memsxfloat:%.04f'%memsx,'memsyfloat:%.04f'%memsy

def pendingClear():
    it.debugRS232(0)
    #it.setpassword()
    timeOut = 60
    starttime = time.time()
    duration = time.time() - starttime
    while duration < timeOut:
        pendingFlag = str(int(it.nop()[1].fieldPending().value()))
        #it.readx99()
        if pendingFlag == '0':
            #it.readx99()
            print "Pending bit Cleared"
            tuneTime = duration
            it.debugRS232(0)
            break
        
        duration = time.time() - starttime
        if duration >=timeOut:
            
            print it.temps()
            print it.currents()
            print it.statusF()
            print it.statusW()
            print it.channel()
            print it.nop()
            raise "Tunetime more than 60 seconds: Stop Test"
        #print "TIME:",time.asctime(),"Pending Bit:",pendingFlag
    return tuneTime

   
                  
def setCommslog(name):
    it.logfile(name + '.txt')
    it.logging(True)
    it.setpassword()
    

def waitformrdy( timeout = 30 ):
    #it.setpassword()
    print 'Waiting for mrdy clear...'
    starttime = time.time()
    while True:
        sys.stdout.write('.')
        time.sleep(.010)
        nopdat = it.nop()[1].data()
        if ( nopdat & 0xFF == 0x10):
            print '\n'
            break
        if (time.time() - starttime > timeout):
            print 'Timed out'
            print '\n'
            break
def createRandomChannel():
    chn = random.randint(1,96)
    return chn


def setFrequency(x):
    '''Setting Frequency For 100Mhz Gridspacing'''
    fcf = float(it.fcf()[1])
    ftf = float(it.ftf()[1])/1000000
    grid = float(it.grid()[1])
    grid = float(grid/10)
    highLimit = it.lfh()[1]
    lowLimit = it.lfl()[1]
    if x > highLimit or x < lowLimit:
        print 'THIS IS BEYOND THE LIMITS'
    else:
        chan = (float(x) - fcf-ftf)/(grid/1000)
        Channel = chan + 1.0
        it.channel(int(Channel))
        print 'FREQUENCY:',x, 'CHANNEL:',Channel
    
