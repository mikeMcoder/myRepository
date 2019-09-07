#Command List
##        -it.dbgTemps(7)- DemodReal
##        -it.dbgTemps(0)- DomainStage Filter1
##        -it.dbgTemps(1)- DomainStage Filter2
##        -it.dbgTemps(3)- SiBlock Temperature
##        -it.dbgTemps(2)- Sled Temperature
##        -it.dbgTemps(4)- Photodiode Current
##        -it.dbgTemps(16)- GMI
##        -it.dbgTemps(512)- ADC channel 0
##        -it.dbgTemps(513)- ADC channel 1
##        -it.dbgTemps(514)- ADC channel 2
##        -it.dbgTemps(515)- ADC channel 3
##        -it.dbgTemps(516)- ADC channel 4
##        -it.dbgTemps(517)- ADC channel 5
##        -it.dbgTemps(518)- ADC channel 6
##        -it.dbgTemps(519)- ADC channel 7
##        -it.dbgTemps(1024)- DAC channel 0
##        -it.dbgTemps(1025)- DAC channel 1
##        -it.dbgTemps(1026)- DAC channel 2
##        -it.dbgTemps(1027)- DAC channel 3
##        -it.dbgTemps(1028)- DAC channel 4
##        -it.dbgTemps(1029)- DAC channel 5
##        -it.dbgTemps(1030)- DAC channel 6
##        -it.dbgTemps(1031)- DAC channel 7
##        -it.dbgTemps(2048)- RTD 1 SAMPLE MSB
##        -it.dbgTemps(2049)- RTD 1 SAMPLE LSB
##        -it.dbgTemps(1050)- RTD 2 SAMPLE MSB
##        -it.dbgTemps(1051)- RTD 2 SAMPLE LSB
##        -it.dbgTemps(1052)- SLED THERMISTOR ADC SAMPLE
##        -it.dbgTemps(1053)- SI BLOCK RTD SAMPLE
##        -it.dbgTemps(1055)- PHOTODIODE MONITOR SAMPLE
##        -it.dbgTemps(1056)- DEMOD SAMPLE


import time
import ConfigParser as parser
import struct
import instrumentDrivers as inst
import os
import sys
import RegressionUtility
sys.path.append(os.path.abspath('.'))

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'

reg = open('RegressionUtility.py','r')
exec(reg)

#PS = inst.HP3631A(0,6)


def PS_ON ():
    return PS.setOutputState('ON')
    
def PS_OFF():
    return PS.setOutputState('OFF')


def lognumoftime(itr,timeG,timeL,resetflag,testfile,wave_meter,power_meter):
    ini = 0
    Error1 = 0
    Error2 = 0
    duration = (time.time()-timeL)
    while duration <itr:
        if (resetflag != 'NO') and ini==0:
            ini = 1
            outstring,Error1 = itpull(timeG,resetflag,wave_meter,power_meter)
##            print Error1
##            if duration > 1:
##                if Error1 > 0.0015 or Error1 < -0.0015:
##                    if 1:
##                        print"Sucks Here"
##                        print Error1
##                        raise "Mode Hop Stop Test"

        else:
            outstring,Error2 = itpull(timeG,0,wave_meter,power_meter)
##            print Error2
##            if duration > 1:
##                if Error2 > 0.0015 or Error2 < -0.0015:
##                    if 1:
##                        print"Bad Here"
##                        print Error2
##                        raise "Mode Hop Stop Test"
        try:
            testfile.write(outstring+"\n")
            print outstring
        except IOError:
            raise 'Error : file is opened in another program'
        duration = (time.time()-timeL)


def demodConv(val):
    if val>=32768: #0x8000
        fval = -(65536-float(val))#0x10000
    else:
        fval = float(val)
    return fval/1000.0        
                         
        
def itpull (time0,resflag,wave_meter,power_meter):
    if 1:
        c1 = time.asctime()
        c2 = str(time.time()-time0)
        (dummy1,lf) = it.lf()
        
        c3 = str(lf)
        (dummy4,c4) = it.channel()
        c4 = str(c4)
        reset = str(resflag)
        strdemodR = float(it.dbgTemps(7)[1].data()) #demodR
        demodR = demodConv(strdemodR)
        strdemodR = str(demodR)
        strF1 = str(float(it.dbgTemps(0)[1].data())/100)#filter1
        strF2 = str(float(it.dbgTemps(1)[1].data())/100)#filter2
        strSiBlock = str(float(it.dbgTemps(3)[1].data())/100)#SiBlock
        strSled = str(float(it.dbgTemps(2)[1].data())/100)#Sledtemp
        strphoto = str(float(it.dbgTemps(4)[1].data())/100)#photodiode
        strGMI = str(float(it.dbgTemps(16)[1].data())/100)#GMI
        strSiBlockControl= str(float(it.dbgTemps(258)[1].data())/100)#SiBlock Controller
        DAC1 = str(int(it.dbgTemps(1025)[1].data()))#DAC CHANNEL 1
        DAC2 = str(int(it.dbgTemps(1026)[1].data()))#DAC CHANNEL 2
        DAC3 = str(int(it.dbgTemps(1027)[1].data()))#DAC CHANNEL 3
        DAC4 = str(int(it.dbgTemps(1028)[1].data()))#DAC CHANNEL 4
        DAC5 = str(int(it.dbgTemps(1029)[1].data()))#DAC CHANNEL 5
        DAC6 = str(int(it.dbgTemps(1030)[1].data()))#DAC CHANNEL 6
        DAC7 = str(int(it.dbgTemps(1031)[1].data()))#DAC CHANNEL 7
        c,pcbTemp = it.temps()[1][1]
        
        #IF(pcbtemp < 32768,PCBtemp,-(65536-pcbtemp))
        if int(pcbTemp) >= 32768:
            intpcbTemp = int(-(65536-int(pcbTemp)))
            strpcbTemp = str(intpcbTemp)
        else:
            intpcbTemp = int(pcbTemp)
            strpcbTemp = str(intpcbTemp)
                
        statusF = str(hex(int(it.statusF()[1].data())))
        statusW = str(hex(int(it.statusW()[1].data())))
        exec ('c39 = str(power_meter.%s)'%(ConfigIni.get('Station','Pwr_Cmd')))
        exec ('c40 = str(wave_meter.%s)'%(ConfigIni.get('Station','Wave_Cmd')))
        age = str(it.age()[1])
        #c39 = '0'
        #c40 = '0'
        freqError = str(float(lf) - float(c40))
        floatError = float(freqError)
        #freqError = '0'
        #floatError = '0'
        
        return "Date: " + "," + c1 + "," +"Duration:"+ "," + c2+ "," + "LF:" + "," +c3 + "," + "Meter:" + "," + c40 + "," + "FreqError" + "," + freqError+ "," +"Channel:" +  "," + c4 + "," + "Power_Meter" + "," + c39 \
               + "," + "Reset:" + "," + reset + "," +  "demodR:" + "," + strdemodR + "," + "Filter1:" + "," + strF1\
               + "," +"Filter2:" + "," + strF2 + "," + "SiBlockTemp:" + "," + strSiBlock + "," + "SledTemp:" + "," + strSled\
               + "," + "photodiode:"+ "," + strphoto + "," + "GMI:" + "," + strGMI + "," + "DAC1-Siblock:"\
               + "," + DAC1 + "," + "DAC3-F2:" + "," + DAC3 + "," + "DAC4-TEC:" + "," +  DAC4\
               + "," + "DAC5-GMI:" + "," + DAC5 + ","+ "DAC7-F1:" + "," + DAC7 + "," + "PCBTEMP:" + ","\
               + strpcbTemp + "," + "StatusF:" + "," + statusF + "," + "statusW:" + "," + statusW + "," + "AGE:" + ","+ age ,floatError 

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

if __name__ == '__main__':
    ConfigIni = parser.ConfigParser()
    ConfigIni.read('Regression.ini')
    record_meters  = ConfigIni.get('Freq_Seq','Record_Meters')

    if record_meters:
        WM_cmd = ConfigIni.get('Station','WaveMeter')
        print 'wavemeter:',WM_cmd
        exec ('wave_meter = inst.%s'%(WM_cmd))
        wave_meter.connect()
        
        PM_cmd = ConfigIni.get('Station','PwrMeter')
        print 'pwrmeter:',PM_cmd
        exec ('power_meter = inst.%s'%(PM_cmd))
        power_meter.connect()
##
##        PM_cfg = ConfigIni.get('Station','PM_Cfg')
##        exec("power_meter.SetActiveConf('POW',%s)"%(PM_cfg))
        
    rststr  = ConfigIni.get('Reset','RSTlst')
    rstlst  = rststr.split(',')
    for rst in rstlst:
        com_port  = int(ConfigIni.get('Station','COM_PORT'))
        preresetX = int(ConfigIni.get('Reset','Pre_ResetX'))
        postresetX = int(ConfigIni.get('Reset','Post_ResetX'))
        repeatX = int(ConfigIni.get('Reset','RepeatX'))
        repeatY = int(ConfigIni.get('Reset','RepeatY'))
        channelstr = ConfigIni.get('Reset','Channelst')
        channelst = channelstr.split(',')
       



    
        print 'preresetX:',preresetX
        print 'postresetX:',postresetX
        print 'channel lst:',channelst
        print 'reset:',rst
        if rst == 'SR':
            repeat = repeatY
        else:
            repeat = repeatX
        
        print 'repeat:',repeat
        

        #PS.connect()
        #PS_OFF()
        time.sleep(.5)
        #PS_ON()
        it.disconnect()
        time.sleep(.5)        
        it.connect(com_port)
        print 'it connected to COM_PORT %d '%(com_port)
        print it.baudrate()
        it.mcb(adt=1)    
        it.resena(1)
        time.sleep(30)
        print 'sena = 1'
        globleST = time.time()
        for chnl in channelst:
            #create a file to save data
            daytime = time.asctime()
            daytimestr = daytime.replace(' ','')
            daytimestr = daytimestr.replace(':','')
            test_name = ConfigIni.get('Station','Serial')+ "_" + chnl + "_"+rst+"_"+daytimestr
            test_file = open("%s.csv"%(test_name),"w")
            test_file.close()
            test_file = open("%s.csv"%(test_name),"a+")
            print 'test_name:',test_name
            
            #set default
            chnl = int(chnl)
            it.channel(int(chnl))
            #it.pwr(1600)
            pwr = it.pwr()
            baud = it.baudrate()
            print chnl, pwr , baud
            ##laser on
            it.resena(1)
            if rst == 'SR':
                time.sleep(45)
            else:
                time.sleep(45)
                
            print "reset is %4s repeat %d times"%(rst,repeat)
            for i in range(repeat):
                set = 0
                if rst=='SR':
                    clearAlarms()
                    set = 1
                    it.resena(sena=1,sr=1)
                    time.sleep(.1)
                    print 'Issued Soft Reset'
                    #localST = time.time()
                    #lognumoftime(postresetX,globleST,localST,set,test_file,wave_meter,power_meter)
                    outstring,Error = itpull(globleST,1,wave_meter,power_meter)
                    test_file.write(outstring+"\n")
                    
                elif rst=='ECHO':
                    clearAlarms()
                    set = 1
                    it.write('\x91\x90\x00\x45')
                    it.read(4)
                    it.write('\xF1\x90\x00\x43')
                    it.read(4)
                    it.write('\x41\x90\x00\x48')
                    it.read(4)
                    it.write('\x31\x90\x00\x4F')
                    it.read(4)
                    time.sleep(.5)
                    outstring,Error = itpull(globleST,1,wave_meter,power_meter)
                    test_file.write(outstring+"\n")
                    print 'Issued ECHO Command'
                    
                elif rst=='TINA':
                    clearAlarms()
                    set = 1
                    it.write('\xa1\x93\x00\x54')
                    it.read(4)
                    it.write('\x61\x93\x00\x49')
                    it.read(4)
                    it.write('\x11\x93\x00\x4e')
                    it.read(4)
                    it.write('\xe1\x93\x00\x41')
                    it.read(4)
                    print 'Issued TINA Command'
                    
                elif rst=='MR':
                    
                    print 'Issued MR Command'
                    it.resena(mr=1)
                    time.sleep(4)
                    clearAlarms()
                    it.resena(1)
                    pendingClear()
                    outstring,Error = itpull(globleST,1,wave_meter,power_meter)
                    test_file.write(outstring+"\n")

          
                print '%s Command Count = %d'%(rst,i)
                #for i in range(10):
##                    it.write('\x00\x00\x00\x00')
##                    a1 = it.read(4)
##                    if len(a1)== 0:
##                        break
                
                localST = time.time()
                print 'log %d samples'%(postresetX)
                print "Take Data"
                lognumoftime(postresetX,globleST,localST,set,test_file,wave_meter,power_meter)
        
        #it.resena(0)                    
        test_file.close()
        it.disconnect()
        #PS_OFF()
        #PS.disconnect()
        print 'finished'
        
