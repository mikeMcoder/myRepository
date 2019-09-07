import struct
import sys
import os
import time
sys.path.append(os.path.abspath('.'))
import instrumentDrivers as inst
import ConfigParser as parser

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'

#Turn on GPIO
import aa_gpio.gpio
g = aa_gpio.gpio.gpio()


#Define parameters of instruments
PS1 = inst.psAG3631('GPIB0::06')
PS2 = inst.psAG3631('GPIB0::07')
WM = inst.HP86120C('GPIB0::21')


def PS1_ON ():
    return PS1.setOutputState('ON')

def PS2_ON ():
    return PS2.setOutputState('ON')
    
def PS1_OFF():
    return PS1.setOutputState('OFF')

def PS2_OFF():
    return PS2.setOutputState('OFF')

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
    
def pendingClear():
    timeOut = 60
    starttime = time.time()
    duration = time.time() - starttime
    while duration < timeOut:
        pendingFlag = str(int(it.nop()[1].fieldPending().value()))
        if pendingFlag == '0':
            print "Pending bit Cleared"
            print "Pending drop at %2fs:"%duration
            break
        
        duration = time.time() - starttime
        if duration >=timeOut:
            print it.temps()
            print it.currents()
            print it.statusF()
            print it.statusW()
            raise "Tunetime more than 60 seconds: Stop Test"
    return duration
     
def clearAlarms():
    return it.statusF(1,1,1,1,1,1,1,1),it.statusW(1,1,1,1,1,1,1,1)

def itpull(time0,pwr_meter,wave_meter,status =''):
    if 1:
        dummy0 = it.serNo()
        c0 = str(dummy0[1][1:])
        c0 = c0.strip("('")
        c0 = c0.strip("',)")
        c1 = time.asctime()
        c2 = str((time.time()-time0))
        (dummy1,c3) = it.lf()
        c3 = str(c3)
        (dummy4,c4) = it.channel()
        c4 = str(c4)
        dummy5 = it.statusW()
        c5 = str(int(dummy5[1].fieldSrq().value()))
        c6 = str(int(dummy5[1].fieldAlm().value()))
        c7 = str(int(dummy5[1].fieldFatal().value()))
        c8 = str(int(dummy5[1].fieldDis().value()))
        c9 = str(int(dummy5[1].fieldWvsf().value()))
        c10 = str(int(dummy5[1].fieldWfreq().value()))
        c11 = str(int(dummy5[1].fieldWtherm().value()))
        c12 = str(int(dummy5[1].fieldWpwr().value()))
        c13 = str(int(dummy5[1].fieldXel().value()))
        c14 = str(int(dummy5[1].fieldCel().value()))
        c15 = str(int(dummy5[1].fieldMrl().value()))
        c16 = str(int(dummy5[1].fieldCrl().value()))

##        it.statusW(xel=1) Do not need to clear latches MM 10.31.15
##        it.statusW(cel=1)       
##        it.statusW(mrl=1)
##        it.statusW(crl=1)  
        
        c17 = str(int(dummy5[1].fieldWvsf().value()))
        c18 = str(int(dummy5[1].fieldWfreql().value()))
        c19 = str(int(dummy5[1].fieldWtherml().value()))
        c20 = str(int(dummy5[1].fieldWpwrl().value()))

##        it.statusW(wvsfl=1) Do not need to clear latches MM 10.31.15
##        it.statusW(wfreql=1)       
##        it.statusW(wtherml=1)
##        it.statusW(wpwrl=1)  

        dummy6 = it.statusF()
        c21 = str(int(dummy6[1].fieldFvsf().value()))
        c22 = str(int(dummy6[1].fieldFfreq().value()))
        c23 = str(int(dummy6[1].fieldFtherm().value()))
        c24 = str(int(dummy6[1].fieldFpwr().value()))
        c25 = str(int(dummy6[1].fieldFvsf().value()))
        c26 = str(int(dummy6[1].fieldFfreql().value()))
        c27 = str(int(dummy6[1].fieldFtherml().value()))
        c28 = str(int(dummy6[1].fieldFpwrl().value()))
##
##        it.statusF(fvsfl=1)Do not need to clear latches MM 10.31.15
##        it.statusF(ffreql=1)       
##        it.statusF(ftherml=1)
##        it.statusF(fpwrl=1)  
        
        (dummy7,(dummy8, [c29, c30]))=it.temps()
        c29 = str(int(c29))
        c30 = str(int(c30))
        (dummy9,(dummy10,[c31,c32]))= it.currents()
        c31 = str(int(c31))
        c32 = str(int(c32))
        dummy12 = it.release()
        c33 = str(dummy12[1][1:])
        c33 = c33.strip("('")
        c33 = c33.strip("',)")
        (dummy13, c34) = it.pwr()
        c34 = str(int(c34))
        (dummy14, c35) = it.oop()
        c35 = str(c35)
        exec ('c36 = str(pwr_meter.%s)'%(ConfigIni.get('Station','Pwr_Cmd')))
        exec ('c37 = str(wave_meter.%s)'%(ConfigIni.get('Station','Wave_Cmd')))
        dummy15 = it.nop()
        c38 = str(int(dummy15[1].fieldPending().value()))
        
        it.write('\x80\x91\x00\x00')
        dummy16 = it.read(4)
        it.write('\x80\x91\x00\x00')
        dummy16 = it.read(4)
        dummy16 = struct.unpack('BBBB',dummy16)
        c39 = str((dummy16[2]*256)+dummy16[3])
        it.write('\xd0\x94\x00\x00')
        dummy17 = it.read(4)
        it.write('\xd0\x94\x00\x00')
        dummy17 = it.read(4)
        dummy17 = struct.unpack('BBBB',dummy17)
        c40 = str((dummy17[2]*256)+dummy17[3])
        c41 = status
        age = str(it.age()[1])

        return c0+","+c33+","+c1+","+c2+","+c3+","+c37+","+c4 + "," + c34+","+c35+ ","+c36+"," + c29 + ","\
               + c30 + "," + c31 + "," + c32+","+ c5 + ","\
               + c6 + "," + c7 + "," + c8 + "," + c9 + ","\
               + c10 + "," + c11 + "," + c12 + "," + c13 + ","\
               + c14 + "," + c15 + "," + c16 + "," + c17 + ","\
               + c18 + "," + c19 + "," + c20 + "," + c21 + ","\
               + c22 + "," + c23 + "," + c24 + "," + c25 + ","\
               + c26 + "," + c27 + "," + c28 + "," + c38 + "," + c39 + "," + c40+ "," + c41 + "," + age +"\n"  


if __name__ == '__main__':
    ConfigIni = parser.ConfigParser()
    ConfigIni.read(r'C:\Documents and Settings\ttx.user\Desktop\MICROITLA_REGRESSION_TEST_SUITE\Python\Regression.ini')
    record_meters  = ConfigIni.get('Pwr_Seq','Record_Meters')

    com_port  = int(ConfigIni.get('Station','COM_PORT'))
    #record_meters == 0 not implemented
    if record_meters:
        WM_cmd = ConfigIni.get('Station','WaveMeter')
        print 'wavemeter:',WM_cmd
        exec ('wavemeter = inst.%s'%(WM_cmd))
        wavemeter.connect()
        
        PM_cmd = ConfigIni.get('Station','PwrMeter')
        print 'pwrmeter:',PM_cmd
        exec ('pwrmeter = inst.%s'%(PM_cmd))
        pwrmeter.connect()

##        PM_cfg = ConfigIni.get('Station','PM_Cfg')
##        exec("pwrmeter.SetActiveConf('POW',%s)"%(PM_cfg))

        print 'meters initialized'
        
    #Turn on the power supplies    
    PS1.connect()
    PS2.connect()
    PS1_OFF()
    PS2_OFF()
    time.sleep(.5)
    PS1_ON()
    time.sleep(.5)
    PS2_ON()
    time.sleep(.5)
    
    #Connect to serial port
    it.connect(com_port)
    
    #Check if it communicates
    clearbuffer()
    
    #Get parameters from ini file power levels, channels, alarm during tuning
    pwrlevelstr  = ConfigIni.get('Pwr_Seq','Pwr_Levels')
    pwrlevelst  = pwrlevelstr.split(',')
    print 'pwrlevels:',pwrlevelst
    
    CHstr  = ConfigIni.get('Pwr_Seq','CH_Seq')
    CHlst  = CHstr.split(',')
    print 'CH_Lst:',CHlst

    adtstr  = ConfigIni.get('Pwr_Seq','ADT_Lst')
    adtlst  = adtstr.split(',')
    print 'ADTs:',adtlst
    
    #loop through the list
    for curchannel in CHlst:
        print 'Testing Channel:',curchannel
        for m_adt in adtlst:
            print 'ADT:', m_adt
            daytime = time.asctime()
            daytimestr = daytime.replace(' ','')
            daytimestr = daytimestr.replace(':','')
            test_name = ConfigIni.get('Station','Serial')+"_"+ConfigIni.get('Pwr_Seq','Name')+"_ADT"+m_adt+"_"+daytimestr
            
            #Create file to save data
            test_file = open("%s.csv"%(test_name),"w")
            test_file.write("serNo,release,datetime,timelapse,lf,meterf,\
            channel,PWR,OOP,meterpwr,sledT,pcbT,teccurrent,\
            diodcurrent,SRQ,ALM,FATAL,DIS,WVSF,WFREQ,\
            WTHERM,WPWR,XEL,CEL,MRL,CRL,WVSFL,WFREQL,\
            WTHERML,WPWRL,FVSF,FFREQ,FTHERM,FPWR,FVSFL,\
            FFREQL,FTHERML,FPWRL,PENDING,UPTIME_M,UPTIME_S,TuneTime,Age\n")
            test_file.close()

            #Specify how many samples for data collection                
            samplingL = int(ConfigIni.get('Pwr_Seq','SamplingL'))
            samplingP = int(ConfigIni.get('Pwr_Seq','SamplingP'))

            print 'channelseq : %s\npwrlevel : %s\nsamplingL(s) : %d\nsamplingP(s) : %d'%(CHlst,pwrlevelstr,samplingL,samplingP)
            it.resena(0)
            clearAlarms()
            freq=it.lf()[1]
            pwrmeter.setFrequency(freq)
            OPSH = int(it.opsh()[1])
            it.pwr(OPSH)
            it.channel(int(curchannel))
            exec ('it.mcb(adt=%s)'%(m_adt))
            time.sleep(3)
            it.resena(1)
                      
            globleST = time.time()
            expectduration = len(CHlst)*samplingL
            
            for pwrlevel in pwrlevelst:
                if 1:
                    localST = time.time()
                    localTL= 0.0
                    it.pwr(int(pwrlevel))
                    tuneTime1 = pendingClear()
                    clearAlarms()
                    outstring = ""
                    test_file = open("%s.csv"%(test_name),"a+")
                    try:
                        dataPoint = 0
                        dataPoint1 = 0
                        while dataPoint <= 20-1:
                            outstring += itpull(globleST,pwrmeter,wavemeter,'before')
                            dataPoint+= 1
                              
                        
                        #print 'output : %s'%(outstring)
                        while dataPoint1 <= 20-1:
                            outstring += itpull(globleST,pwrmeter,wavemeter,'after_5s')
                            dataPoint1 += 1
                        print 'output : %s'%(outstring)
                        test_file.write(outstring)
                    except IOError:
                        raise 'Error : file is opened in another program'
                    time.sleep(5)
                        
    test_file.close

    it.disconnect()
    print 'Test Complete\n'

    
