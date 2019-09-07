import sys
import os
import sys
import instrumentDrivers as inst
import time
import math
import aa_gpio.gpio
g = aa_gpio.gpio.gpio()

sys.path.append(os.path.abspath('.'))

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'

P3_3 = inst.psAG3631('GPIB0::06')
PN5_2 = inst.psAG3631('GPIB0::07')

loop = 500
port = 3
counter = 0
passcnt = 0
stuckcnt = 0


def Supply_3_3ON():    
    P3_3.setOutputState('ON')

    
def Supply_3_3OFF():
    P3_3.setOutputState('OFF')


def Supply_5_2ON():    
    PN5_2.setOutputState('ON')

    
def Supply_5_2OFF():
    PN5_2.setOutputState('OFF')


def Supply_3_3Curr():
    Current = P3_3.getCurr()
    return Current

def read(ser):
    fail = 0
    try:
        temp1 = float(it.dbgTemps(1)[1].data())/100
        temp2 = float(it.dbgTemps(2)[1].data())/100
        if temp1 and temp2 > 300.00:
            status = 1
            lstData = []
            testTime = time.ctime().replace(' ', '_').replace(':', '').replace('2015','')
            nop_data = str(hex(int(it.nop()[1].data())))
            Pending = it.nopStats()[1].fieldNopPendLock().toBinaryString()
            Channel_Lock = it.nopStats()[1].fieldNopPendCh().toBinaryString()
            State_Machine =it.nopStats()[1].fieldStateMach().cipher()
            statusF_data = str(hex(int(it.statusF()[1].data())))
            oop_data = str(it.oop()[1])
            garbage , currents_data = it.currents()
            tec = currents_data[1][0]
            gmi = currents_data[1][1]
            statusW_data = str(hex(int(it.statusW()[1].data())))
            garbage, temps_data = it.temps()
            sledTemp = temps_data[1][0]
            pcbTemp = temps_data[1][1]
            temp1 = float(it.dbgTemps(1)[1].data())/100
            temp2 = float(it.dbgTemps(2)[1].data())/100
            lstData.append([ser,testTime,nop_data,Pending,Channel_Lock,State_Machine,statusF_data,\
                           oop_data,tec,gmi,statusW_data,sledTemp,\
                           pcbTemp,temp1,temp2])

            for item in lstData:
                # post conversion
                strWrite = ''
                strWrite += '%s\t' % ser
                strWrite += '%0.25s\t' % testTime
                strWrite += '%s\t' % nop_data 
                strWrite += '%s\t\t' % Pending
                strWrite += '%s\t\t' % Channel_Lock
                strWrite += '%s\t' % State_Machine
                strWrite += '%s\t' % statusF_data
                strWrite += '%s\t' % oop_data
                strWrite += '%s\t' % tec
                strWrite += '%s\t\t' % gmi
                strWrite += '%s\t\t' % statusW_data
                strWrite += '%s\t\t' % sledTemp
                strWrite += '%s\t\t' % pcbTemp
                strWrite += '%s\t\t' % temp1
                strWrite += '%s\t' % temp2
                strWrite += '\n'
                dataFile.write(strWrite)
                time.sleep(.1)
                
            
        else:
            status = 0
            
    except:
             KeyError


    return status

def saveData(ser,status):
    lstData = []
    testTime = time.ctime().replace(' ', '_').replace(':', '').replace('2015','')
    nop_data = str(hex(int(it.nop()[1].data())))
    Pending = it.nopStats()[1].fieldNopPendLock().toBinaryString()
    Channel_Lock = it.nopStats()[1].fieldNopPendCh().toBinaryString()
    State_Machine =it.nopStats()[1].fieldStateMach().cipher()
    statusF_data = str(hex(int(it.statusF()[1].data())))
    oop_data = str(it.oop()[1])
    garbage , currents_data = it.currents()
    tec = currents_data[1][0]
    gmi = currents_data[1][1]
    statusW_data = str(hex(int(it.statusW()[1].data())))
    garbage, temps_data = it.temps()
    sledTemp = temps_data[1][0]
    pcbTemp = temps_data[1][1]
    temp1 = float(it.dbgTemps(1)[1].data())/100
    temp2 = float(it.dbgTemps(2)[1].data())/100
    lstData.append([ser,testTime,nop_data,Pending,Channel_Lock,State_Machine,statusF_data,\
                   oop_data,tec,gmi,statusW_data,sledTemp,\
                   pcbTemp,temp1,temp2])

    for item in lstData:
        # post conversion
        strWrite = ''
        strWrite += '%s\t' % ser
        strWrite += '%0.25s\t' % testTime
        strWrite += '%s\t' % nop_data 
        strWrite += '%s\t\t' % Pending
        strWrite += '%s\t\t' % Channel_Lock
        strWrite += '%s\t' % State_Machine
        strWrite += '%s\t' % statusF_data
        strWrite += '%s\t' % oop_data
        strWrite += '%s\t' % tec
        strWrite += '%s\t\t' % gmi
        strWrite += '%s\t\t' % statusW_data
        strWrite += '%s\t\t' % sledTemp
        strWrite += '%s\t\t' % pcbTemp
        strWrite += '%s\t\t' % temp1
        strWrite += '%s\t' % temp2
        strWrite += '%s\t' % status
        strWrite += '\n'
        dataFile.write(strWrite)
        
        time.sleep(.1)
                    
           
    
            
 

P3_3.connect()
PN5_2.connect()


# Assemble file header
testTime = time.ctime().replace(' ', '_').replace(':', '')
dataFile = open('ColdStart_TINA_Test' + '_' + testTime +  '.txt', 'w')
headerLst = ['serialNo',
             'timeStamp',
             'nop',
             'nopStats_pending',
             'nopStats_ch_lock',
             'nopStats_State_Mach',
             'statusF(hex)',
             'oop',
             'tec',
             'gmi',
             'statusW',
             'sled',
             'pcbTemp',
             'F1',
             'F2',
             'status']
strHeader = ''
for item in headerLst:
             strHeader += (item + '\t')


dataFile.write(strHeader + '\n')
    

it.connect(port)

if __name__ == '__main__':
    

    #Main iteration
    for i in range(loop):
        #pseudocode
        #Turn on suply sequence
        #Initialize GPIO
        #Hard reset
        #SoftReset
        #Initialize read power, frequency, ftf, threshold, iocap
        #Turn on Laser
        #Wait when its channel lock, poll nop()
        #At Channel Lock RSave/Read parameters        #Issue TINA Command
        #Issue a hard reset via gpio
        #Turn on laser
        #Wait until channel lock , poll nop()
        #Save parameters
        #Criteria-Must be able to turn on after TINA commands and values must be same
        
        ####MAIN####
        #Turn on suply sequence
        Supply_5_2OFF()
        time.sleep(.06)
        Supply_3_3OFF()
        time.sleep(.6)
        Supply_5_2ON()
        time.sleep(.045)
        Supply_3_3ON()
        print "Turn on Supply"
        #Initialize GPIO
        g.InitPin()
        time.sleep(.9)
        #Hard reset
        g.reset(.05)
        print "Hard reset"
        duration = time.time()
        time.sleep(1)
        #SoftReset
        it.resena(sr=1)
        time.sleep(3)
        print "Soft reset"
        #Turn on Laser
        it.resena(1)
        time.sleep(1)
        print "Laser ON"
        status = it.nopStats()[1].fieldStateMach().cipher()
        strSer = str(it.serNo())
        ser = str(strSer[14:24])
        while status != 'CHANNEL_LOCK':
            failcnt = read(ser) #Function to read temps and save data
            if failcnt == 0:
                pass   
            else:
                stuckcnt +=1
                print "Pending Stuck"
                print it.nopStats()
                print it.dbgTemps(1)
                print it.dbgTemps(2)
                print it.temps()
                raise "STOP! Failed here, print failure conditions"
            status = it.nopStats()[1].fieldStateMach().cipher()
        passcnt += 1
        #Save parameters
        status = 'before'
        data = saveData(ser,status)
        print "Save data before TINA"
        
        #Issue TINA Command
        it.write('\xa1\x93\x00\x54')
        it.read(4)
        it.write('\x61\x93\x00\x49')
        it.read(4)
        it.write('\x11\x93\x00\x4e')
        it.read(4)
        it.write('\xe1\x93\x00\x41')
        it.read(4)
        print 'Issued TINA Command'
        time.sleep(3)
         #Issue a hard reset via gpio
        g.reset(.05)
        it.connect(3)
        time.sleep(4)
        print "Hard Reset After TINA"
        #Turn on laser
        it.resena(1)
        time.sleep(1)
        print "Turn on Laser After TINA"
        #Wait until channel lock , poll nop()
        status = it.nopStats()[1].fieldStateMach().cipher()
        strSer = str(it.serNo())
        ser = str(strSer[14:24])
        while status != 'CHANNEL_LOCK':
            failcnt = read(ser) #Function to read temps and save data
            if failcnt == 0:
                pass   
            else:
                stuckcnt +=1
                print "Pending Stuck"
                print it.nopStats()
                print it.dbgTemps(1)
                print it.dbgTemps(2)
                print it.temps()
                raise "STOP! Failed here, print failure conditions"
            status = it.nopStats()[1].fieldStateMach().cipher()
        passcnt += 1
        #Save parameters
        status = 'after'
        data = saveData(ser,status)
        print "Save Data afer TINA"
    
    dataFile.close()   
          
     
it.disconnect()
