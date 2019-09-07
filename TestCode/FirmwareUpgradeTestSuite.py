import math
import struct
import sys
import os
import time
import instrumentDrivers as inst
import ConfigParser as parser
sys.path.append(os.path.abspath('.'))

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'



ConfigIni = parser.ConfigParser()
ConfigIni.read(ConfigIni.read(r'C:\\Documents and Settings\\ttx.user\\Desktop\\nanoRT\\Regression.ini'))

daytime = time.asctime()
daytimestr = daytime.replace(' ','')
daytimestr = daytimestr.replace(':','')
test_name = 'FirmwareUpgrade' + ConfigIni.get('DownLoad','Name')+"_"+daytimestr

com_port  = int(ConfigIni.get('Station','COM_PORT'))
#BRlst     = int(ConfigIni.get('DownLoad','BaudRate_Lst'))
repeatX   = ConfigIni.get('DownLoad','RepeatX')
RayNew    = ConfigIni.get('DownLoad','RayNew')
RayOld    = ConfigIni.get('DownLoad','RayOld')
Raylst    = [RayOld, RayNew]

intrepeatX = int(repeatX)
BRlst = 9600,19200,38400,57600,115200
test_file = open("%s.csv"%(test_name),"w")
test_file.write("datetime,iteration,baudrate,release,upgradeT\n")
test_file.close()
test_file = open("%s.csv"%(test_name),"a+")


#Define parameters of instruments
PS1 = inst.psAG3631('GPIB0::06')
PS2 = inst.psAG3631('GPIB0::07')
WM = inst.HP86120C('GPIB0::20')


def PS1_ON ():
    return PS1.setOutputState('ON')

def PS2_ON ():
    return PS2.setOutputState('ON')
    
def PS1_OFF():
    return PS1.setOutputState('OFF')

def PS2_OFF():
    return PS2.setOutputState('OFF')

##clear buffer, calling it.release() max 5 times
################################################

def clearbuffer():
    for i in range(5):
        try:itR =it.release()
        except:raise'Error : cannot call it.release'
        try:
            if itR[0] == 'OK':
                print 'buffer cleared in %d calls: %s'%(i,itR)
                break
        except:
            raise 'Error : itR[0]'
    if (i==4)&(itR[0]!='OK'):
        raise 'Error : ',itR

def pullrelease(BRpairs,globalST):
    outstring = ''
    for ptr in range(len(BRpairs)):
        it.baudrate(BRpairs[ptr])
        clearbuffer()
        [dummy,preB] = it.baudrate()
        print 'BR:%d,Ray:%s'%(int(preB),Raylst[ptr])
        localST = time.time()
        exec ('it.upgrade(\'application\',r\'c:\data\%s.ray\')'%Raylst[ptr])
        time.sleep(3)
        if BRpairs[ptr] != 115200:
            it.baudrate(115200)
            time.sleep(2)
            it.baudrate(BRpairs[ptr])
        clearbuffer()
        [dummy,c0]=it.baudrate()
        c0 = str(c0)
        dummy = it.release()
        c1 = str(dummy[1][1:])
        c1 = c1.strip("('")
        c1 = c1.strip("',)")
        c2 = str(time.time()-localST)
        outstring += c0+","+c1+","+c2+","
    return outstring

##main
################################################

def runTest():



        
    #Turn on the Supplies
    PS1.connect()
    PS2.connect()
    PS1_OFF()
    PS2_OFF()
    time.sleep(.5)
    PS1_ON()
    time.sleep(.5)
    PS2_ON()
    
    time.sleep(2)
    
    it.connect(3,115200)
    clearbuffer()
    print it.serNo()
    
    globalST = time.time()
    for itr in range(intrepeatX):
        for BR in BRlst:
            BRpairs = [115200,BR]
            outstring = pullrelease(BRpairs,globalST)
            outstring = time.asctime()+','+str(itr+1)+','+outstring + '\n'
            print 'data:',outstring
            test_file = open("%s.csv"%(test_name),"a+")
            test_file.write(outstring)
            test_file.close()        
    
    it.baudrate(9600)
    it.disconnect()
    time.sleep(2)
    
    
if __name__== '__main__':
    runTest()
