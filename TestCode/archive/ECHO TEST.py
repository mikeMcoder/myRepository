import struct
import sys
import os
import time
sys.path.append('C:\\Users\\michael.mercado\\Desktop\\uITLA_ &_uITLA2 Scripts\\Python')
sys.path.append(os.path.abspath('.'))
import instrumentDrivers as inst
import ConfigParser as parser
#import aa_gpio.gpio
#g = aa_gpio.gpio.gpio()


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


def lognumoftime(itr,timeG,timeL,resetflag,testfile,wave_meter,power_meter):
    ini = 0
    while (time.time()-timeL)<itr:
        if (resetflag != 'NO') and ini==0:
            ini = 1
            outstring = itpull(timeG,resetflag,wave_meter,power_meter)
        else:
            outstring = itpull(timeG,0,wave_meter,power_meter)
        try:
            testfile.write(outstring+"\n")
            print outstring
        except IOError:
            raise 'Error : file is opened in another program'
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
        (dummy1,c3) = it.lf()
        c3 = str(c3)
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
        DAC0= str(int(it.dbgTemps(1024)[1].data()))#DAC CHANNEL 0
        DAC1 = str(int(it.dbgTemps(1025)[1].data()))#DAC CHANNEL 1
        DAC2 = str(int(it.dbgTemps(1026)[1].data()))#DAC CHANNEL 2
        DAC3 = str(int(it.dbgTemps(1027)[1].data()))#DAC CHANNEL 3
        DAC4 = str(int(it.dbgTemps(1028)[1].data()))#DAC CHANNEL 4
        DAC5 = str(int(it.dbgTemps(1029)[1].data()))#DAC CHANNEL 5
        DAC6 = str(int(it.dbgTemps(1030)[1].data()))#DAC CHANNEL 6
        DAC7 = str(int(it.dbgTemps(1031)[1].data()))#DAC CHANNEL 7
##        strRTD1_MSB = str(int(it.dbgTemps(2048)[1].data()))#Sample RTD1 MSB
##        strRTD1_LSB = str(int(it.dbgTemps(2049)[1].data()))#Sample RTD1 LSB
##        strRTD2_MSB = str(int(it.dbgTemps(2050)[1].data()))#Sample RTD2 MSB
##        strRTD2_LSB = str(int(it.dbgTemps(2051)[1].data()))#Sample RTD2 LSB
##        strSled_sam = str(int(it.dbgTemps(2052)[1].data()))#Sample Sled
##        strSiBlock_sam= str(int(it.dbgTemps(2053)[1].data()))#Sample SiBlock
##        strPhoto_sam= str(int(it.dbgTemps(2055)[1].data()))#Sample Photo
##        strDemod_sam= str(int(it.dbgTemps(2056)[1].data()))#Sample demod
        c,pcbTemp = it.currents()
        strpcbTemp = str(float(pcbTemp[1][0]/100))
        exec ('c39 = str(power_meter.%s)'%(ConfigIni.get('Station','Pwr_Cmd')))
        exec ('c40 = str(wave_meter.%s)'%(ConfigIni.get('Station','Wave_Cmd')))
        return str(c1)+","+str(c2)+","+str(c3)+","+ str(c40) + "," + str(c4) + "," + str(c39)+ ","\
               + str(resflag) + "," +  "demodR:" + "," + str(strdemodR) + "," +"Filter1:" + "," + str(strF1) + ","\
               + "Filter2:" + "," + str(strF2) + "," + "SiBlockTemp:" + "," + str(strSiBlock) + "," + "SledTemp:" + "," + str(strSled) + ","\
               + "photodiode:"+ ","+ str(strphoto) + "," + "GMI:" + "," + str(strGMI) + "," + "DAC0:" + "," + str(DAC0) + "," + "DAC1:" + ","\
               + str(DAC1) + "," + "DAC2:" + "," + str(DAC2) + "," + "DAC3:" + "," + str(DAC3) + "," + "DAC4:" + "," +  str(DAC4)\
               + "," + "DAC5:" + "," + str(DAC5) + "," + "DAC6:" + "," + str(DAC6) + "," +"DAC7:" + "," + str(DAC7) + "," + "PCBTEMP:"+\
               "," + str(strpcbTemp)


       

if __name__ == '__main__':
    ConfigIni = parser.ConfigParser()
    ConfigIni.read(r'C:\Documents and Settings\ttx.user\Desktop\uITLA_ &_uITLA2 Scripts\Python\Regression.ini')
    record_meters  = ConfigIni.get('Freq_Seq','Record_Meters')

    if record_meters:
        WM_cmd = ConfigIni.get('Station','WaveMeter')
        print 'wavemeter:',WM_cmd
        exec ('wave_meter = inst.%s'%WM_cmd)
        wave_meter.connect()
        
        PM_cmd = ConfigIni.get('Station','PwrMeter')
        print 'pwrmeter:',PM_cmd
        exec ('power_meter = inst.%s'%PM_cmd)
        power_meter.connect()

        #PM_cfg = ConfigIni.get('Station','PM_Cfg')  --NOT NEEDED FOR 2.7 DRIVER MM 6.5.15
        #exec("power_meter.SetActiveConf('POW',%s)"%(PM_cfg))
        
    rststr  = ConfigIni.get('Reset','RSTlst')
    rstlst  = rststr.split(',')
    for rst in rstlst:
        daytime = time.asctime()
        daytimestr = daytime.replace(' ','')
        daytimestr = daytimestr.replace(':','')
        test_name = ConfigIni.get('Station','Serial')+"_"+rst+"_"+daytimestr
    
        com_port  = int(ConfigIni.get('Station','COM_PORT'))
        preresetX = int(ConfigIni.get('Reset','Pre_ResetX'))
        postresetX = int(ConfigIni.get('Reset','Post_ResetX'))
        repeatX = int(ConfigIni.get('Reset','RepeatX'))
        channelstr = ConfigIni.get('Reset','Channelst')
        channelst = channelstr.split(',')
        print 'test_name:',test_name
        test_file = open("%s.csv"%(test_name),"w")
        test_file.write("datetime,timelapse,lf,Freq_meter,channel,powermeter,\
        CommandFlag, demodR,Filter1,Filter2,SiBlock,SledTemp,Photodiode, GMI, RTD1_MSB, RTD1_LSB, RTD2_MSB, RTD2_LSB,SLED_SAMPLE,\
        SIBLOCK_SAMPLE,PHOTODIODE_SAMPLE,DEMOD_SAMPLE,PCBTEMP\n")
        test_file.close()
        test_file = open("%s.csv"%(test_name),"a+")
    
        print 'preresetX:',preresetX
        print 'postresetX:',postresetX
        print 'channel lst:',channelst
        print 'reset:',rst
        print 'repeatX:',repeatX
        

        PS1.connect()
        PS2.connect()
        PS1_OFF()
        PS2_OFF()
        time.sleep(.5)
        PS1_ON()
        time.sleep(.5)
        PS2_ON()
        it.connect(com_port)
        print 'it connected to COM_PORT %d '%(com_port)

        ##clear buffer, calling it.release() max 5 times
        ################################################
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

        it.mcb(adt=1)    
        it.resena(1)
        print 'sena = 1'

        globleST = time.time()
        #start iteration
        print 'log %d samples'%(preresetX)
        lognumoftime(preresetX,globleST,globleST,'NO',test_file,wave_meter,power_meter)                                              

        for chnl in channelst:
            it.resena(0)
            print"Laser off for 10 sec"
            time.sleep(10)
            ##set default
            chnl = int(chnl)
            it.channel(int(chnl))
            it.pwr(1350)
            pwr = it.pwr()
            baud = it.baudrate()
            print chnl, pwr , baud
            ##laser on
            it.resena(1)
            time.sleep(240)
            
            for i in range(repeatX):
                if rst=='SR':
                    it.resena(sena=1,sr=1)
                    print 'Issued Soft Reset'
                elif rst=='ECHO':
                    it.write('\x91\x90\x00\x45')
                    it.read(4)
                    it.write('\xF1\x90\x00\x43')
                    it.read(4)
                    it.write('\x41\x90\x00\x48')
                    it.read(4)
                    it.write('\x31\x90\x00\x4F')
                    it.read(4)
                    print 'Issued ECHO Command'
                elif rst=='TINA':
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
                    it.resena(mr=1)
                    print 'Issued Module Reset'
                print '%s Command Count = %d'%(rst,i)
                time.sleep(1)
                localST = time.time()
                print 'log %d samples'%(postresetX)
                #print "Take Data"
                lognumoftime(postresetX,globleST,localST,rst,test_file,wave_meter,power_meter)
        
        #it.resena(0)                    
        test_file.close()
        it.disconnect()
        #PS_OFF()
        #PS.disconnect()
        print 'finished'
        
