import math
import struct
import sys
import os
import time
import instrumentDrivers as inst
import RegressionUtility
import aa_gpio.gpio
import ConfigParser as parser
g = aa_gpio.gpio.gpio()
g.InitPin()
sys.path.append(os.path.abspath('.'))
utility = open('RegressionUtility.py','r')
exec(utility)


import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'



ConfigIni = parser.ConfigParser()
ConfigIni.read(r'C:\Documents and Settings\ttx.user\Desktop\MICROITLA_REGRESSION_TEST_SUITE\Python\Regression.ini')




def clearbuffer():
    g.MODSEL_N_Disable()
    time.sleep(.5)
    g.MODSEL_N_Enable()
    print 'buffer cleared'

def pwr_adt():
    pwrlevelstr  = ConfigIni.get('Freq_Seq','Pwr_Levels')
    pwrlevelst  = pwrlevelstr.split(',')
    print 'pwrlevels:',pwrlevelst

    adtstr  = ConfigIni.get('Freq_Seq','ADT_Lst')
    adtlst  = adtstr.split(',')
    print 'ADTs:',adtlst
    return pwrlevelst, adtlst

def createFile(adt):
    teststr  = ConfigIni.get('Freq_Seq','Name')+"_ADT"+m_adt+ "_"+pwrlevel
    daytime = time.asctime()
    daytimestr = daytime.replace(' ','')
    daytimestr = daytimestr.replace(':','')
    test_name = ConfigIni.get('Station','Serial')+"_"+teststr+"_"+daytimestr
    test_file = open("%s.csv"%(test_name),"w")
    test_file.write("SN,RELEASE,TIMESTAMP,DURATION,LF,CHANNEL,FREQUENCY(METER),ERROR(THZ),OOP,POWER(dBm),POWERERROR,STATUSW(BIN),STATUSF(BIN),STATUSW(HEX),STATUSF(HEX),\
    SLEDT,PCBT,TEC,DIODE,PENDING,TuneTime,Status,AGE\n")
    test_file.close()
    return test_name,test_file

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


#minimize the parameters to access to speed up test
#convert the garbage freq and freq error values to zero
#change the wavelength of the power meter everytime power is read
    
def itpull(time0,pwr_meter,wave_meter,strtuneTime,status = ''):
    if 1:
        dummy0 = it.serNo()
        c0 = str(dummy0[1][1:])
        c0 = c0.strip("('")
        serial = c0.strip("',)")
        timeStamp = time.asctime()
        duration = str((time.time()-time0))
        (dummy1,c3) = it.lf()
        lf = str(c3)
        (dummy4,c4) = it.channel()
        channel = str(c4)
        statWbin = bin(int(it.statusW()[1].data()))
        statFbin = bin(int(it.statusF()[1].data()))
        statWhex = hex(int(it.statusW()[1].data()))
        statFhex = hex(int(it.statusF()[1].data()))
        (dummy7,(dummy8, [c29, c30]))=it.temps()
        sledT = str(int(c29))
        pcbT = str(int(c30))
        (dummy9,(dummy10,[c31,c32]))= it.currents()
        tec = str(int(c31))
        diode = str(int(c32))
        dummy12 = it.release()
        c33 = str(dummy12[1][1:])
        c33 = c33.strip("('")
        release = c33.strip("',)")
        (dummy13, c34) = it.pwr()
        pwr = str(int(c34))
        (dummy14, c35) = it.oop()
        oop = str(c35)
        exec ('powerM = str(pwr_meter.%s)'%(ConfigIni.get('Station','Pwr_Cmd')))
        exec ('waveM = str(wave_meter.%s)'%(ConfigIni.get('Station','Wave_Cmd')))
        age = str(it.age()[1])
        powError = float(c35)/100- float(powerM)
        strpowError = str(powError)
        floatwaveM = float(waveM)

        if floatwaveM>= 2990.00001:
            waveM = str(0)
            error = str(0)
        else:
            error = str(float(lf)-floatwaveM)
       
        dummy15 = it.nop()
        pending = str(int(dummy15[1].fieldPending().value()))
        
        return serial+ "," + release+ "," + timeStamp + "," + duration + "," + lf + "," + channel + "," + waveM + "," + error + "," + \
               oop+ "," + powerM + "," + strpowError + "," + statWbin + "," + statFbin + "," + statWhex + "," + statFhex\
               + "," + sledT + "," + pcbT + "," + tec + "," + diode + "," + pending + "," + strtuneTime + "," + status + "," + age +"\n"



        
        



###########################################################################################################################################
###########################################################################################################################################
rounds = 2
pwrlevelst, adtlst = pwr_adt()

if __name__ == '__main__':
    wavemeter1,powermeter1,port = connectInstrument()
    huaweiPowerSupplySequence()
    it.connect(port)
    checkCom()
    showInitialParameters()
    setComslog()
    for pwrlevel in pwrlevelst:
        print 'Power Level is:',pwrlevel
        for m_adt in adtlst:
            print 'ADT:',m_adt
            test_name,test_file = createFile(m_adt)
            CHstr  = ConfigIni.get('Freq_Seq','CH_Seq')
            CHlst  = CHstr.split(',')
            samplingL = int(ConfigIni.get('Freq_Seq','SamplingL'))
            samplingP = int(ConfigIni.get('Freq_Seq','SamplingP'))

            print 'channelseq : %s\npwrlevel : %s\nsamplingL(s) : %d\nsamplingP(s) : %d'%(CHlst,pwrlevel,samplingL,samplingP)
            exec ('it.mcb(adt=%s)'%(m_adt))
            globleST = time.time()
            expectduration = len(CHlst)*samplingL
            for itr in range(1):
                print '*' * 30,'THIS IS ROUND:',itr +1,'*' * 35
                for curchannel in CHlst:
                    if 1:
                        if 1:
                            localST = time.time()
                            it.resena(0)
                            freq=it.lf()[1]
                            pwrmeter.setFrequency(freq)
                            it.pwr(int(pwrlevel))
                            time.sleep(5)
                            it.channel(int(curchannel))
                            it.resena(1)
                            #Wait until pending clears
                            tuneTime = pendingClear()
                            strtuneTime = str(tuneTime)
                            print 'tune time is:',strtuneTime
                            # clear statusF and statusW registers
                            it.statusF(1,1,1,1,1,1,1,1)
                            it.statusW(1,1,1,1,1,1,1,1)  
                            localTL= 0.0
                            #while(localTL<(samplingL-samplingP)):
                            samplingST = time.time()
                            outstring = ""
                            if 1:
                            #Sample data after the pending bit drops
                                print 'Take data after pending bit drops'
                                outstring += itpull(globleST,pwrmeter,wavemeter,strtuneTime,'after_pending')
                                try:
                                    test_file = open("%s.csv"%(test_name),"a+")
                                   
                                except IOError:
                                    raise 'Error : file is opened in another program'
                            print 'Wait for 20sec'
                                    
                            time.sleep(20)
                            if 1:
                             #Sample data after 20sec
                                print 'Take data after 20sec'
                                tuneTime_20 = str(tuneTime + 20)
                                print 'Tune time after 20s is:',tuneTime_20
                                outstring += itpull(globleST,pwrmeter,wavemeter,tuneTime_20,'after_20sec')
                                try:
                                    test_file.write(outstring)
                                    test_file.close()
                                    print 'output : %s'%(outstring)
                                    
                                except IOError:
                                    raise 'Error : file is opened in another program'

                            sys.stdout.flush()
            print 'Test Complete!\n'
it.disconnect()

########################################################################################################################################################################
########################################################################################################################################################################




    
