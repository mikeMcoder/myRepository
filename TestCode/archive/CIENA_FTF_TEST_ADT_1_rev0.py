
import sys
import os
sys.path.append(os.path.abspath('.'))
import time
import random
import struct
import instrumentDrivers as inst
import ConfigParser as parser




import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'


port = 3

    
    


#Define parameters of instruments
PS = inst.psAG3631('GPIB0::06')
wm = inst.BurleighWA1100('GPIB0::21')
pm = inst.pmHP8163('GPIB0::11')
wm.connect()
pm.connect()


#Declare variables
resultData = []
iter = 0
endTime = 300 #86400 #43200
almCnt = 0
#fwPath = 'C:\data\Sundial3S_V03.06.07.01.ray'
fwPath = 'C:\data\ECL_uITLA_V3.6.6-27-[333fd50]-branch_03.06.06_(Sundial3S_V03.06.06.07_Product_2_SINGLE_UITLA).ray'



def PS_ON ():
    return PS.setOutputState('ON')
    
def PS_OFF():
    return PS.setOutputState('OFF')

def checkStatus():
    w= 0
    f= 0
    #read warning status and Fatal status
    statW = it.statusW()
    statF = it.statusF()
##    statW =  '1'
##    statF =  '0'
##    statWl = '0'
##    statFl = '0'
    

    #Stop if alarm triggered
    if statW[1].fieldWfreq().toBinaryString() == '1' or statW[1].fieldWfreql().toBinaryString() == '1':
    #if statW == '1' or  statWl== '1':
        print it.statusW()
        w += 1
        

    
    if statF[1].fieldFfreq().toBinaryString() == '1' or statF[1].fieldFfreql().toBinaryString() == '1':
    #if statF == '1' or  statFl== '1':
        print it.statusF()
        f += 1
        
    return statW, statF ,w ,f
    #return w ,f

def converttoString(statusW,statusF):
    return str(statusW),str(statusF)


def clearAlarms():
    return it.statusF(1,1,1,1,1,1,1,1),it.statusW(1,1,1,1,1,1,1,1)


def pendingClear():
    timeOut = 60
    starttime = time.time()
    duration = time.time() - starttime
    while duration < timeOut:
        pendingFlag = str(int(it.nop()[1].fieldPending().value()))
        if pendingFlag == '0':
            print "Pending bit Cleared"
            tuneTime = duration
            break
        
        duration = time.time() - starttime
        if duration >=timeOut:
            print it.temps()
            print it.currents()
            print it.statusF()
            print it.statusW()
            raise "Tunetime more than 60 seconds: Stop Test"
    return tuneTime


def snapshotunitstate():
    snapshotdat = it.readx99()
##    snapshotdat.time = time.time()
##    snapshotdat.nopdat = it.nop()[1].data()
##    snapshotdat.statF = it.statusF()[1].data()
##    snapshotdat.statW = it.statusW()[1].data()
##    it.register(ITLA.Register.Register(address=0x21,data=0x00FF),write=True)
##    it.register(ITLA.Register.Register(address=0x20,data=0x00FF),write=True) 
##    snapshotdat.casetemp = it.temps()[1][1][1]/100.0
##    snapshotdat.laserage = it.age()[1]
    glitchinfo = it.readAEAfloatarray(ITLA.Register.Register(address=0x85,data=0x0000))
    it.register(ITLA.Register.Register(address=0x85,data=0x0002),write=True)
    snapshotdat.f1highwatermark=glitchinfo[0]
    snapshotdat.f2highwatermark=glitchinfo[2]
##    snapshotdat.oop = it.oop()[1]/100.0 # technically not needed since we have the MPD, but probably good to log
    snapshotdat.hopcount = round(it.readAEAfloatarray(ITLA.Register.Register(address=0x85,data=0x0002))[0])
    return(snapshotdat)


#Connect to power supply
PS.connect()
PS_OFF()
time.sleep(2)
PS_ON()
time.sleep(1)
####upgrade Firmware
it.connect(port)
time.sleep(1)
#change baudrate:
it.baudrate(115200)
print 'START UPGRADE'
#Send the upgrade command
it.upgrade('APPLICATION',fwPath)
#set the baudrate back to 9600
time.sleep(2)
it.baudrate(9600)
           
print' Finish Upgrade'

#initialize power meter

#Turn on the supply

PS_OFF()
time.sleep(10)
PS_ON()

#Connect to unit 
it.connect(port)
time.sleep(1)
dut = it.serNo()[1][1]
testTime = time.ctime().replace(' ', '_').replace(':', '')


#CreateFile
dataFile = open(dut + '_' + 'FTF_Ciena_Test' + testTime + '.txt', 'w')
headerLst = ['TimeStamp',
             'statW0',
             'statF0',
             'statW1',
             'statF1',
             'statW2',
             'statF2',
             'OOP',
             'SLED',
             'PCBT',
             'CURRENTS',
             'AGE',
             'Freq(Meter)',
             'Power(Meter)',
             'FTF',
             'LF',
             'F1',
             'F2',
             'HOPCNT',
             ]
strHeader = ''
for h in headerLst:
    strHeader += (h + '\t')
strHeader.rstrip('\t')
dataFile.write(strHeader + '\n')

it.disconnect()


it.connect(3)
#enable logging
it.logfile()
it.logging('True')
#enable register 99/85
it.setpassword()

#reset modhop counter
it.register(ITLA.Register.Register(address=0x85,data=0x0003),write=True)


#check serial number
print it.serNo()
#check release
print it.release()
#set adt = 1
it.mcb(adt=1)
print it.mcb()
#check PWR
print it.pwr()
#check LF
print 'LF:',it.lf()
#Check FTF
print 'FTF:', it.ftf()
#check almT
print 'almT'
print it.almT()
#check srqT
print 'srqT'
print it.srqT()
#check fatalT
print 'fatalT'
print it.fatalT()
print 'switch to channel 50'
it.channel(50)
print it.channel()
#turn on the laser
print 'Turn on Laser'
time.sleep(2)
it.resena(1)
#wait for pending bit to de assert
pending = it.nop()[1].fieldPending().toBinaryString()
while pending[7]!= '0':
    pending = it.nop()[1].fieldPending().toBinaryString()
    #print pending[7]
print 'pending deasserted'
print 'clear statusF and status W registers'
time.sleep(5)

#clear statusF 0x20
#clear statusW 0x21
clearAlarms()
#Run for 24 Hours:
start = time.time()
duration = time.time()-start
while duration <= endTime:
    
    try:
        #set new random ftf value
        ftf = random.randint(0,100)
        it.ftf(ftf)
        pendingClear()
        #Check if there is an alarm
        dataW0, dataF0,statW_bit0,statF_bit0 = checkStatus()
        strdataW0 = str(hex(int(dataW0[1].data())))
        strdataF0 = str(hex(int(dataF0[1].data())))
        #clear status registers
        clearAlarms()
   

        #set new random ftf value
        ftf = random.randint(0,100)
        it.ftf(ftf)
        pendingClear()
        #Check if there is an alarm
        dataW1, dataF1,statW_bit1,statF_bit1 = checkStatus()
        strdataW1 = str(hex(int(dataW0[1].data())))
        strdataF1 = str(hex(int(dataF0[1].data())))
        #clear status registers
        clearAlarms()
        
        #set new random ftf value
        ftf = random.randint(0,100)
        it.ftf(ftf)
        pendingClear()
        #Check if there is an alarm
        dataW2, dataF2,statW_bit2,statF_bit2 = checkStatus()
        strdataW2 = str(hex(int(dataW2[1].data())))
        strdataF2 = str(hex(int(dataF2[1].data())))
        #clear status registers
        clearAlarms()
        
        #read oop
        oop = it.oop()
        stroop =str(oop[1])
        #set new random ftf value
        ftf = random.randint(0,200)
        it.ftf(ftf)
        pendingClear()
        clearAlarms()
        
        #read temps
        garbage,temps = it.temps()
        strSled =str(int(temps[1][0]))
        strPcbT =str(int(temps[1][1]))
        #set new random ftf value
        ftf = random.randint(0,200)
        it.ftf(ftf)
        pendingClear()
        clearAlarms()

        #read currents
        currents = it.currents()
        strcurrents = str(currents)
        #set new random ftf value
        ftf = random.randint(0,200)
        it.ftf(ftf)
        pendingClear()
        clearAlarms()
        #read age
        age = it.age()
        strage = str(age[1])
        freq = str(wm.getFrequency())
        pwr = str(pm.getDisplayedPower())
        ftf = str(it.ftf()[1])
        lf = str(it.lf()[1])
        snap = snapshotunitstate()
        f1 = str(snap.f1highwatermark)
        f2 = str(snap.f2highwatermark)
        hop = str(snap.hopcount)
        read = it.readx99()
        
        

        if statW_bit0 == 1 or statF_bit0 == 1 or statW_bit1 == 1 or statF_bit1 == 1 or statW_bit2 == 1 or statF_bit2 == 1:
            timeStamp = time.asctime().replace(' ', '_').replace(':', '')
            resultData =''
            resultData = timeStamp + '\t'+ strdataW0 + '\t' + strdataF0 + \
                         '\t'+ strdataW1 + '\t' + strdataF1 + \
                         '\t'+ strdataW2 + '\t' + strdataF2 + \
                         '\t'+ stroop + '\t' + strSled + '\t' + strPcbT + '\t' + strcurrents +  \
                         '\t' + strage + '\t' + freq + '\t' + pwr + '\t' + ftf + '\t' + lf + '\t' + f1 + '\t' + f2 + '\t' + hop +'\n'
            #resultData = timeStamp + '\t'+ 'fail' 
            dataFile.write(resultData)
            almCnt += 1
            #raise "STOP ALARMS HAD TRIGGERED"
        
        else:    
        
            timeStamp = time.asctime().replace(' ', '_').replace(':', '')
            resultData =''
            resultData = timeStamp + '\t'+ strdataW0 + '\t' + strdataF0 + \
                         '\t'+ strdataW1 + '\t' + strdataF1 + \
                         '\t'+ strdataW2 + '\t' + strdataF2 + \
                         '\t'+ stroop + '\t' + strSled + '\t' + strPcbT + '\t' + strcurrents +  \
                         '\t' + strage + '\t' + freq + '\t' + pwr + '\t' + ftf + '\t' + lf + '\t' + f1 + '\t' + f2 +  '\t' + hop +'\n'
                        
            
            dataFile.write(resultData)
        iter += 1
        print 'END OF LOOP'
        print 'LOOP COUNT NO ALARMS:',iter
        duration = time.time() - start
        print 'TIME RAN IN SEC:', duration
        print almCnt
    except ValueError,KeyboardInterrupt:
        raise"Value Error"
        
it.disconnect()
dataFile.close()
print 'TEST DONE IN:%fs:'%duration
print 'TOTAL ALARMS TRIGGERED:', almCnt
PS_OFF()