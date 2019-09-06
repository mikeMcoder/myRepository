
import time
import ConfigParser as parser
import struct
import instrumentDrivers as inst
import os
import sys
import aa_gpio.gpio
g = aa_gpio.gpio.gpio()
g.InitPin()
sys.path.append(os.path.abspath('.'))
    
ConfigIni = parser.ConfigParser()
ConfigIni.read(r'\\photon\Company\DWDM Engineering\Micro_ITLA\Firmware\Regression_Testing\Regression Test Scripts\RegressionIni\Regression1.ini')

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'

reg = open('RegressionUtility_K.py','r')
exec(reg)
PORT = 1



def lognumoftime(itr,timeG,timeL,resetflag,testfile,wavemeter1,powermeter1):
    ini = 0
    Error1 = 0
    Error2 = 0
    duration = (time.time()-timeL)
    while duration <itr:
        if (resetflag != 'NO') and ini==0:
            ini = 1
            outstring,Error1 = itpull(timeG,resetflag,wavemeter1,powermeter1)

        else:
            outstring,Error2 = itpull(timeG,0,wavemeter1,powermeter1)
            
        try:
            testfile.write(outstring+"\n")
            print outstring
        except IOError:
            raise 'Error : file is opened in another program'
        duration = (time.time()-timeL)

 
                         
        
def itpull (time0,resflag,wavemeter1,powermeter1):
    if 1:
        
        read99 = it.readx99
        c1 = time.asctime()
        c2 = str(time.time()-time0)
        (dummy1,lf) = it.lf()
        
        c3 = str(lf)
        (dummy4,c4) = it.channel()
        c4 = str(c4)
        reset = str(resflag)
        strdemodR = str(read99().demodrealerr)
        
        strF1 = str(read99().f1temp)#str(float(it.dbgTemps(0)[1].data())/100)#filter1
        it.readx99()
        strF2 = str(read99().f2temp)#str(float(it.dbgTemps(1)[1].data())/100)#filter2
        it.readx99()
        strSiBlock = str(read99().siblocktemp)#str(float(it.dbgTemps(3)[1].data())/100)#SiBlock
        it.readx99()
        strSled = str(read99().sled_temperature)#str(float(it.dbgTemps(2)[1].data())/100)#Sledtemp
        it.readx99()
        strphoto = str(read99().photodiode_current)#str(float(it.dbgTemps(4)[1].data())/100)#photodiode
        it.readx99()
        strGMI = str(read99().gain_medium_current)#str(float(it.dbgTemps(16)[1].data())/100)#GMI
        it.readx99()
        strSiBlockControl= str(float(it.dbgTemps(258)[1].data())/100)#SiBlock Controller
        it.readx99()
        DAC1 = str(int(it.dbgTemps(1025)[1].data()))#DAC CHANNEL 1
        it.readx99()
        DAC2 = str(int(it.dbgTemps(1026)[1].data()))#DAC CHANNEL 2
        it.readx99()
        DAC3 = str(int(it.dbgTemps(1027)[1].data()))#DAC CHANNEL 3
        it.readx99()
        DAC4 = str(int(it.dbgTemps(1028)[1].data()))#DAC CHANNEL 4
        it.readx99()
        DAC5 = str(int(it.dbgTemps(1029)[1].data()))#DAC CHANNEL 5
        it.readx99()
        DAC6 = str(int(it.dbgTemps(1030)[1].data()))#DAC CHANNEL 6
        it.readx99()
        DAC7 = str(int(it.dbgTemps(1031)[1].data()))#DAC CHANNEL 7
        c,pcbTemp = it.temps()[1][1]
        
        #IF(pcbtemp < 32768,PCBtemp,-(65536-pcbtemp))
        if int(pcbTemp) >= 32768:
            intpcbTemp = int(-(65536-int(pcbTemp)))
            strpcbTemp = str(intpcbTemp)
        else:
            intpcbTemp = int(pcbTemp)
            strpcbTemp = str(intpcbTemp)
        it.readx99()        
        statusF = str(hex(int(it.statusF()[1].data())))
        statusW = str(hex(int(it.statusW()[1].data())))
        exec ('c39 = str(powermeter1.%s)'%(ConfigIni.get('Station','Pwr_Cmd')))
        exec ('c40 = str(wavemeter1.%s)'%(ConfigIni.get('Station','Wave_Cmd')))
        age = str(it.age()[1])
        #c39 = '0'
        #c40 = '0'
        freqError = str(float(lf) - float(c40))
        floatError = float(freqError)
        #freqError = '0'
        #floatError = '0'
        
        output =  "Date: " + "," + c1 + "," +"Duration:"+ "," + c2+ "," + "LF:" + "," +c3 + "," + "Meter:" + "," + c40 + "," + "FreqError" + "," + freqError+ "," +"Channel:" +  "," + c4 + "," + "Power_Meter" + "," + c39 \
               + "," + "Reset:" + "," + reset + "," +  "demodR:" + "," + strdemodR + "," + "Filter1:" + "," + strF1\
               + "," +"Filter2:" + "," + strF2 + "," + "SiBlockTemp:" + "," + strSiBlock + "," + "SledTemp:" + "," + strSled\
               + "," + "photodiode:"+ "," + strphoto + "," + "GMI:" + "," + strGMI + "," + "DAC1-Siblock:"\
               + "," + DAC1 + "," + "DAC3-F2:" + "," + DAC3 + "," + "DAC4-TEC:" + "," +  DAC4\
               + "," + "DAC5-GMI:" + "," + DAC5 + ","+ "DAC7-F1:" + "," + DAC7 + "," + "PCBTEMP:" + ","\
               + strpcbTemp + "," + "StatusF:" + "," + statusF + "," + "statusW:" + "," + statusW + "," + "AGE:" + ","+ age ,floatError 

        return output




if __name__ == '__main__':

    rststr  = ConfigIni.get('Reset','RSTlst')
    rstlst  = ['MR','ECHO','SR']
    #rstlst  = rststr.split(',')
    
    for rst in rstlst:
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
        
        #create a file to save data
        daytime = time.asctime()
        daytimestr = daytime.replace(' ','')
        daytimestr = daytimestr.replace(':','')
        test_name = "Huawei_Test" + "_" + rst +"_"+daytimestr
        test_file = open("%s.csv"%(test_name),"w")
        test_file.close()
        test_file = open("%s.csv"%(test_name),"a+")
        print 'test_name:',test_name            

        wavemeter1,powermeter1,com_port = connectInstrument()
        print 'it connected to COM_PORT %d '%(com_port)
        huaweiPowerSupplySequence()
        it.connect(PORT)
        checkCom()
        #readMready()
        setComslog('HuaweiTest')
#        showInitialParameters()
        it.mcb(adt=1)
        time.sleep(1)
        it.resena(1)
        pendingClear()
        monChannellock()
        
        globleST = time.time()
        for chnl in channelst:
            setChannel(int(chnl))
            pendingClear()
            monChannellock()
            pwr = it.pwr()
            baud = it.baudrate()
            print chnl, pwr , baud
            #clearRegister85()
             
            print "reset is %4s repeat %d times"%(rst,repeat)
            for i in range(repeat):
                set = 0
                if rst=='SR':
                    clearAlarms()
                    set = 1
                    triggerSoftReset()
                    time.sleep(.1)
                    outstring,Error = itpull(globleST,1,wavemeter1,powermeter1)
                    test_file.write(outstring+"\n")
                    
                elif rst=='ECHO':
                    clearAlarms()
                    set = 1
                    triggerEcho()
                    it.read(4)
                    time.sleep(.5)
                    it.setpassword()
                    outstring,Error = itpull(globleST,1,wavemeter1,powermeter1)
                    test_file.write(outstring+"\n")
                    
                elif rst=='TINA':
                    clearAlarms()
                    set = 1
                    triggerTina()
                    pendingClear()
                    monChannellock()
                    
                elif rst=='MR':
                    triggerMasterReset()
                    time.sleep(4)
                    it.setpassword()
                    clearAlarms()
                    it.resena(1)
                    pendingClear()
                    monChannellock()
                    outstring,Error = itpull(globleST,1,wavemeter1,powermeter1)
                    test_file.write(outstring+"\n")

                #elif rst == 'LDIS'
                #elif rst == 'HARDRST'

          
                print '%s Command Count = %d'%(rst,i)

                
                localST = time.time()
                print 'log %d samples'%(postresetX)
                print "Take Data"
                lognumoftime(postresetX,globleST,localST,set,test_file,wavemeter1,powermeter1)
                
        
            #readRegister85()             
        test_file.close()
        it.disconnect()
        print 'finished'
        
