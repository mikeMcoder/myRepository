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






import aa_gpio.gpio 
g = aa_gpio.gpio.gpio()
g.InitPin()

ConfigIni = parser.ConfigParser()
ConfigIni.read(r'C:\Documents and Settings\ttx.user\Desktop\MICROITLA_REGRESSION_TEST_SUITE\Python\Regression.ini')


#Define parameters of instruments
PS1 = inst.psAG3631('GPIB0::06')
PS2 = inst.psAG3631('GPIB0::07')
WM = inst.HP86120C('GPIB0::21')

#functions to turn on supplies
def PS1_ON ():
    return PS1.setOutputState('ON')

def PS2_ON ():
    return PS2.setOutputState('ON')


#functions to turn off supplies
def PS1_OFF():
    return PS1.setOutputState('OFF')

def PS2_OFF():
    return PS2.setOutputState('OFF')

def connectInstr():
    record_meters  = ConfigIni.get('Freq_Seq','Record_Meters')
    com_port  = int(ConfigIni.get('Station','COM_PORT'))
    
    if record_meters:
        WM_cmd = ConfigIni.get('Station','WaveMeter')
        print 'wavemeter:',WM_cmd
        exec ('wavemeter = inst.%s'%(WM_cmd))
        wavemeter.connect()
        
        PM_cmd = ConfigIni.get('Station','PwrMeter')
        print 'pwrmeter:',PM_cmd
        exec ('pwrmeter = inst.%s'%(PM_cmd))
        pwrmeter.connect()
        print 'meters initialized'
    return wavemeter,pwrmeter,com_port

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
    test_file.write("SN,RELEASE,TIMESTAMP,DURATION,LF,CHANNEL,FREQUENCY(METER),ERROR(THZ),OOP,POWER(dBm),STATUSW(BIN),STATUSF(BIN),STATUSW(HEX),STATUSF(HEX),\
    SLEDT,PCBT,TEC,DIODE,PENDING,AGE\n")
    test_file.close()
    return test_name,test_file



#minimize the parameters to access to speed up test
#convert the garbage freq and freq error values to zero
#change the wavelength of the power meter everytime power is read
    
def itpull(time0,pwr_meter,wave_meter):
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
        floatwaveM = float(waveM)

        if floatwaveM>= 2990.00001:
            waveM = str(0)
            error = str(0)
        else:
            error = str(float(lf)-floatwaveM)
        


        dummy15 = it.nop()
        pending = str(int(dummy15[1].fieldPending().value()))


        return serial+ "," + release+ "," + timeStamp + "," + duration + "," + lf + "," + channel + "," + waveM + "," + error + "," + \
               oop+ "," + powerM + "," + statWbin + "," + statFbin + "," + statWhex + "," + statFhex\
               + "," + sledT + "," + pcbT + "," + tec + "," + diode + "," + pending + "," + age


        
        



###########################################################################################################################################
###########################################################################################################################################

if __name__ == '__main__':
    wavemeter,pwrmeter,port = connectInstr()
    PS1.connect()
    PS2.connect()
    PS1_OFF()
    PS2_OFF()
    time.sleep(.5)
    PS1_ON()
    time.sleep(.5)
    PS2_ON()
    it.connect(port)
    clearbuffer()
    pwrlevelst, adtlst = pwr_adt()
    for pwrlevel in pwrlevelst:
        print'Power level: pwrlevel',pwrlevel
        for m_adt in adtlst:
            print 'ADT:', m_adt
            test_name,test_file = createFile(m_adt)
            CHstr  = ConfigIni.get('Freq_Seq','CH_Seq')
            CHlst  = CHstr.split(',')
            samplingL = int(ConfigIni.get('Freq_Seq','SamplingL'))
            samplingP = int(ConfigIni.get('Freq_Seq','SamplingP'))

            print 'channelseq : %s\npwrlevel : %s\nsamplingL(s) : %d\nsamplingP(s) : %d'%(CHlst,pwrlevel,samplingL,samplingP)
            exec ('it.mcb(adt=%s)'%(m_adt))
            globleST = time.time()
            expectduration = len(CHlst)*samplingL
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
                        # clear statusF and statusW registers
                        it.statusF(1,1,1,1,1,1,1,1)
                        it.statusW(1,1,1,1,1,1,1,1)  
                        localTL= 0.0
                        while(localTL<(samplingL-samplingP)):
                            samplingST = time.time()
                            outstring = ""
                            if 1:
                            #try:
                                outstring += itpull(globleST,pwrmeter,wavemeter)
                                try:
                                    test_file = open("%s.csv"%(test_name),"a+")
                                    test_file.write(outstring+"\n")
                                    test_file.close()
                                    print 'output : %s'%(outstring)
                                    
                                except IOError:
                                    raise 'Error : file is opened in another program'
                            else:
                            #except:
                                test_file = open("%s.csv"%(test_name),"a+")
                                test_file.write("Error")
                                test_file.close()
                                print ' Error : itpull'

                            curtime     = time.time()                
                            samplingTL  = curtime-samplingST
                            localTL     = curtime-localST
                            globleTL    = curtime-globleST
                            countdown   = (expectduration - globleTL)/3600
                            restP = max(samplingP-samplingTL,0)
                            print 'samplingTL : %s \nlocalTL : %s \nglobleTL : %s \ncountdown in hrs: %s \nsleep: %s \n'%(samplingTL,localTL,globleTL,countdown, restP)
                            sys.stdout.flush()
                            time.sleep(restP)
                            sys.stdout.flush()
        print 'Test Complete!\n'
it.disconnect()
##PS1_OFF()
##PS1.disconnect()
##PS2_OFF()
##PS2.disconnect()

########################################################################################################################################################################
########################################################################################################################################################################




    
