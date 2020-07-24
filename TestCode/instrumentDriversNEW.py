# This is a  set of instrument drivers written for use with Python 2.6
# written by Jeremy Machi
# add some later codes by Stephanie for hardware test
import serial
import visa
import time
import minimalmodbus
import re
#import numpy
printcmd = 1
class GPIB_BOARD:
    def __init__(self, boardNum):
        self.boardNum = boardNum
        self.gpib_board = visa.Gpib(boardNum)
    def send_ifc(self):
        self.gpib_board.send_ifc()

class pmHP8163:
    '''this is an HP/Agilent two slot lightwave multi-meter'''
    def __init__(self, strVisa, desc='PM', slot=1, head=1):
        self.strVisa = strVisa
        self.slot = slot
        self.head = head
        self.desc = desc
        
    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.inst.ask(cmd)
        print 'Connected:', self.name
        print 'Description: %s, Slot: %d, Head: %d' % (self.desc, self.slot, self.head)
        
    def disconnect(self):
        cmd = 'GTL'
        self.inst.write(cmd)
        del self.inst

    def getPower(self):
        cmd = 'READ%d:CHAN%d:POW?' % (self.slot, self.head)
        return float(self.inst.ask(cmd))

    def getDisplayedPower(self):
        cmd = 'FETC%d:CHAN%d:POW?' % (self.slot, self.head)
        reply = self.inst.ask(cmd)
        try:
            ret = float(reply)
        except:
            ret = -80
        return ret

    def setWavelength(self, lambdaNM = 1556.5):
        cmd = 'SENS%d:CHAN%d:POW:WAV %.2fnm' % (self.slot, self.head, lambdaNM)
        self.inst.write(cmd)
        return

    def getWavelength(self):
        cmd = 'SENS%d:CHAN%d:POW:WAV?'%(self.slot, self.head)
        return float(self.inst.ask(cmd)) * 1.00E+9

    def setFrequency(self, freqTHz = 194.0):
        self.setWavelength(299792458.00/(freqTHz * 1.00E+3))
        return

    def getFrequency(self):
        return 299792458.00/(self.getWavelength() * 1.00E+3)

    def setPowerUnit(self, unit = 0):
        cmd = 'SENS%d:CHAN%d:POW:UNIT %d'%(self.slot, self.head, unit)
        self.inst.write(cmd)
        return
    
    def getPowerUnit(self):
        strCmd = 'SENS%d:CHAN%d:POW:UNIT?' % (self.slot, self.head)
        return int( self.inst.ask(strCmd) )

    def setCalibrationConst(self,const=0):
        cmd = 'SENS%d:CHAN%d:CORR %f%s' % (self.slot, self.head, const,'DB')
        self.inst.write(cmd)

    def getCalibrationConst(self):
        cmd = 'SENS%d:CHAN%d:CORR?'%(self.slot, self.head)
        return float(self.inst.ask(cmd))

    def triggerReadPower(self):
        #trigger must be done on the main channel, number 1.  It will also affect subordinate channel.
        #this is why the trigger is hard coded to be channel 1.
        self.inst.write( ':INIT%d:CHAN1:TRIG:IMM' % self.slot)
        strCmd = 'FETC%d:CHAN%d:POW?'%(self.slot, self.head)
        return float(self.inst.ask(strCmd))

    def setAvgTime(self, secs):
        cmd = 'SENS%d:CHAN%d:POW:ATIM %f'%(self.slot, self.head, secs)
        self.inst.write(cmd)
        
class E4407B:
    def __init__(self, strVisa):
        self.strVisa = strVisa
        self.delay = 0.2

    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.inst.ask(cmd)

    def wait(self,delay=0.001):
        n = int(delay)
        for i in range (n):
            time.sleep(1)
        r = delay-n
        time.sleep(r)
        
    def sendCmd(self,cmd):
        #print "send cmd= ", cmd
        self.inst.write(cmd)
 
    def sendQuery(self,cmd, delay=0.01):
        #print "send query cmd= ", cmd
        self.inst.write(cmd)
        self.wait(delay)
        strRet1 = self.inst.read()
        #print 'result=%s'%strRet1
        return strRet1

class DS0604A:
    '''this is an HP/Agilent DS0604A OSCILLOSCOPE'''
    def __init__(self, strVisa):
        self.strVisa = strVisa
        self.delay = 0.2
                   
    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.inst.ask(cmd)
        #print 'Connected:', self.name

    def queryD(self,cmd,delay=1):
        self.inst.write(cmd)
        time.sleep(delay)        
        rd= self.inst.read()
        print rd
        return rd
    
        
    def write(self,cmd):
        self.inst.write(cmd)

    def read(self):
        return self.inst.read()

    def ask(self,cmd):
        return self.inst.ask(cmd)
        

    def searchVpp(self,count=1):
        i = 0
        while i < count:
            cmd =':MEAS:VPP?'
            #self.inst.write(cmd)
            val = float(self.inst.ask(cmd))
            print val
            i = i+1
        return val
    def searchVmax(self,count=1):
        i = 0
        while i < count:
            cmd ='MEAS:VMAX?'
            #self.inst.write(cmd)
            val = float(self.inst.ask(cmd))
            print val
            i = i+1
    def searchVmin(self,count=1):
        i = 0
        while i < count:
            cmd ='MEAS:VMIN?'
            #self.inst.write(cmd)
            val = float(self.inst.ask(cmd))
            print val
            i = i+1
            
    def InitCapture(self):
        #cmd =":AUTOSCALE\n"
        #self.inst.write(cmd)
        
        cmd ="*RST\n"
        self.inst.write(cmd)
        cmd =":CHAN1:PROBE 10\n"
        self.inst.write(cmd)
        cmd =":CHANNEL1:RANGE 2.5\n"
        self.inst.write(cmd)
        cmd =":TIM:RANG 10e-4\n"
        self.inst.write(cmd)
        cmd =":TIMEBASE:REFERENCE CENTER\n"
        self.inst.write(cmd)
#        cmd =":TRIGGER:TV:SOURCE CHANNEL1\n"
        cmd =":TRIGGER:SOURCE CHANNEL1\n"
        self.inst.write(cmd)
        cmd =":TRIGGER:EDGE:SLOPE POSITIVE\n"
        self.inst.write(cmd)
        cmd =":TRIGGER:MODE NORMAL\n"
        self.inst.write(cmd)
        cmd =":TRIGGER:MODE EDGE\n"
        self.inst.write(cmd)
        cmd =":TRIGGER:EDGE:LEVEL 0.5\n"
        self.inst.write(cmd)
        cmd ="*CLS\n"
        self.inst.write(cmd)
        cmd = '*STB?'
        print 'STB= ', self.inst.ask(cmd)

    def getSTB(self):
        cmd = '*STB?'
        return self.inst.ask(cmd)
    
    def Run(self):    
        cmd =":RUN"
        print cmd
        self.inst.write(cmd)

    def Stop(self):    
        cmd =":STOP"
        print cmd
        self.inst.write(cmd)

    def Capture(self):
        cmd =":ACQUIRE:TYPE NORMAL\n"
        self.inst.write(cmd)
        cmd =":ACQUIRE:COMPLETE 100\n"
        self.inst.write(cmd)
        cmd =":DIGITIZE CHAN1\n"
        self.inst.write(cmd)

    def GetImage(self):
        cmd =":DISPLAY:DATA? BMP8bit, SCREEN, COLOR\n"
        #image_data=self.delay_query(cmd)
        self.inst.write(cmd)
        image_data=self.inst.read()
        fp =open("c:\\scope\\data\\screen.bmp", 'wb')
        fp.write(image_data)
        fp.close()
        
    def GetwaveFormData(self,fn='C:\\scope\data\img1.csv'):
        cmd =":WAVEFORM:DATA?"
        self.inst.write(cmd)
        strRet = self.inst.read()
        print strRet
        lstRet = list(strRet)
        lstOut=[]
        n=1
        if fn!=None:
            f=open(fn,'w')
            for t in lstRet:
                num = ord(t)
                n = n+1
                if n > 11:
                    lstOut.append(num)
                    f.writelines('%d,%d\n'%(n-10,num))
            f.close()        
        print lstOut
        
    def DSO6104A_cmd(self,cmd):
        #print "DSO6104A command ", cmd
        self.inst.write(cmd)

    def DSO6104A_query(self,cmd):
        try:
            print "DSO6104A query ", cmd
            self.inst.write(cmd)
            time.sleep(0.1)
            strRet = self.inst.read()
            print 'ans = %s'%strRet
        except:
            print "DSO6104A query ", cmd
            self.inst.write(cmd)
            time.sleep(0.2)
            strRet = self.inst.read()
            print 'ans = %s'%strRet
        return strRet
    
    def Capture_DSO6104A(self):
        print "capturing DSO6104A"
        cmd ="SINGle"
        self.inst.write(cmd)

        cmd =":MEASure:DUTYcycle? MATH"
        self.inst.write(cmd)
        strRet1 = self.inst.read()
        print 'DUTY=%s'%strRet1

        cmd =":MEASure:VAVerage? CHAN4"
        self.inst.write(cmd)
        strRet2 = self.inst.read()
        print 'AV CH4=%s'%strRet2

        cmd =":MEASure:VPP? CHAN4"
        self.inst.write(cmd)
        strRet3 = self.inst.read()
        print 'VPP=%s'%strRet3

        cmd =":MEASure:VAVerage? CHAN1"
        self.inst.write(cmd)
        strRet4 = self.inst.read()
        print 'AV CH1=%s'%strRet4

        cmd =":MEASure:VAVerage? CHAN3"
        self.inst.write(cmd)
        strRet5 = self.inst.read()
        print 'AV CH3=%s'%strRet5
        return [strRet1,strRet2,strRet3,strRet4,strRet5]

    def DSO6104A_shortquery(self,cmd,delay=0.1):
        #print "DSO6104A query ", cmd
        self.inst.write(cmd)
        time.sleep(delay)
        try:
            strRet = self.inst.read()
        except:
            try:
                time.sleep(delay)
                self.inst.write(cmd)
                time.sleep(delay)
                strRet = self.inst.read()
            except:
                try:
                    time.sleep(delay)
                    self.inst.write(cmd)
                    time.sleep(delay)
                    strRet = self.inst.read()
                except:
                    return [-1,'9999']
        return [0,strRet]
    
    def delay_query(self,cmd):
        delay = self.delay
        while delay < 2.0:
            try:
                time.sleep(delay)
                self.inst.write(cmd)
                time.sleep(delay)
                strRet = self.inst.read()
                if strRet == 'ERROR':
                    raise
                return strRet
            except:
                delay += 0.1
                print 'delay increased to %0.1f' % delay
        print 'GPIB FAILURE: QUERY'
        raise
##viSetAttribute(vi, VI_ATTR_TMO_VALUE, 30000);
##img_size = IMG_SIZE;
##viQueryf(vi, ":DISPLAY:DATA? BMP8bit, SCREEN, COLOR\n", "%#b\n",
##&img_size, image_data);
##/* Write image data to file. */
##fp = fopen ("c:\\scope\\data\\screen.bmp", "wb");
##img_size = fwrite(image_data, sizeof(unsigned char), img_size, fp);
##fclose (fp);
##printf("Wrote image data (%d bytes) to file.\n", img_size);
##viSetAttribute(vi, VI_ATTR_TMO_VALUE, 5000);

##/* IMAGE_TRANSFER - In this example we will query for the image
##* data with ":DISPLAY:DATA?" to read the data and save the data
##* to the file "image.dat" which you can then send to a printer.
##*/
##viSetAttribute(vi, VI_ATTR_TMO_VALUE, 30000);
##printf("Transferring image to c:\\scope\\data\\screen.bmp\n");
##img_size = IMG_SIZE;
##viQueryf(vi, ":DISPLAY:DATA? BMP8bit, SCREEN, COLOR\n", "%#b\n",
##&img_size, image_data);
##printf("Read display data query (%d bytes).\n", img_size);
##/* Write image data to file. */
##fp = fopen ("c:\\scope\\data\\screen.bmp", "wb");
##img_size = fwrite(image_data, sizeof(unsigned char), img_size, fp);
##fclose (fp);
##printf("Wrote image data (%d bytes) to file.\n", img_size);
##viSetAttribute(vi, VI_ATTR_TMO_VALUE, 5000);
        

class attenHP81613:
    '''this is an HP/Agilent 8156A stand alone optical attenuator'''
    def __init__(self, strVisa):
        self.strVisa = strVisa
                   
    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.inst.ask(cmd)
        print 'Connected:', self.name
        
    def disconnect(self):
        cmd = 'GTL'
        self.inst.write(cmd)
        del self.inst

    def setOutputState(self, state = 'NONE'):
        state = state.upper()
        if state == "NONE":
            cmd = 'OUTP:STAT?'
        elif state == "ON":
            cmd = 'OUTP:STAT ON'
        elif state == "OFF":
            cmd = 'OUTP:STAT OFF'
        else:
            raise 'Invalid Input'
        self.inst.write(cmd)
        if state == "NONE":
            s = self.inst.read()
            return int(s)
        else:
            return state
        
    def setAttenuationMode(self):
        'Sets the instrument to attenuation mode.'
        cmd = 'OUTP:APM:OFF'
        self.inst.write(cmd)

    def setFrequency(self, freqTHz = 193.5):
        'Sets the optical frequency of the attenuator with the argument freqTHz in TeraHertz '
        nm = ((299792458.00)/(freqTHz * 1.00E+12))*1.00E+9
        cmd = 'INP:WAV'+ ' '+ str(nm) + 'nm'
        self.inst.write(cmd)
        return
        
    def setAttenuation(self, attdB = 25.0):
        'Sets the optical attenuation value with the attdB argument in Decibels '
        cmd = 'INP:ATT %.3f'%attdB
        self.inst.write(cmd)
        return

    def getAttenuation(self):
        return float(self.inst.ask(":INP:ATT?"))                
        
    def setAttenuationOffset(self, fltOffset):
        cmd = ':INP:OFFS %0.2f' % fltOffset
        self.inst.write(cmd)
        
    def getAttenuationOffset(self):
        return float( self.inst.ask(':INP:OFFS?'))
        
class pmHP8156:
    '''this is an HP/Agilent two slot lightwave multi-meter'''
    def __init__(self, strVisa, desc='PM', slot=1, head=1):
        self.strVisa = strVisa
        self.slot = slot
        self.head = head
        self.desc = desc
        
    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.inst.ask(cmd)
        print 'Connected:', self.name
        print 'Description: %s, Slot: %d, Head: %d' % (self.desc, self.slot, self.head)
        
    def disconnect(self):
        cmd = 'GTL'
        self.inst.write(cmd)
        del self.inst

    def getPower(self):
        cmd = 'READ%d:CHAN%d:POW?' % (self.slot, self.head)
        return float(self.inst.ask(cmd))

    def getDisplayedPower(self):
        cmd = 'FETC%d:CHAN%d:POW?' % (self.slot, self.head)
        reply = self.inst.ask(cmd)
        try:
            ret = float(reply)
        except:
            ret = -80
        return ret

    def setWavelength(self, lambdaNM = 1556.5):
        cmd = 'SENS%d:CHAN%d:POW:WAV %.2fnm' % (self.slot, self.head, lambdaNM)
        self.inst.write(cmd)
        return

    def getWavelength(self):
        cmd = 'SENS%d:CHAN%d:POW:WAV?'%(self.slot, self.head)
        return float(self.inst.ask(cmd)) * 1.00E+9

    def setFrequency(self, freqTHz = 194.0):
        self.setWavelength(299792458.00/(freqTHz * 1.00E+3))
        return

    def getFrequency(self):
        return 299792458.00/(self.getWavelength() * 1.00E+3)

    def setPowerUnit(self, unit = 0):
        cmd = 'SENS%d:CHAN%d:POW:UNIT %d'%(self.slot, self.head, unit)
        self.inst.write(cmd)
        return
    
    def getPowerUnit(self):
        strCmd = 'SENS%d:CHAN%d:POW:UNIT?' % (self.slot, self.head)
        return int( self.inst.ask(strCmd) )

    def setCalibrationConst(self,const=0):
        cmd = 'SENS%d:CHAN%d:CORR %f%s' % (self.slot, self.head, const,'DB')
        self.inst.write(cmd)

    def getCalibrationConst(self):
        cmd = 'SENS%d:CHAN%d:CORR?'%(self.slot, self.head)
        return float(self.inst.ask(cmd))

    def triggerReadPower(self):
        #trigger must be done on the main channel, number 1.  It will also affect subordinate channel.
        #this is why the trigger is hard coded to be channel 1.
        self.inst.write( ':INIT%d:CHAN1:TRIG:IMM' % self.slot)
        strCmd = 'FETC%d:CHAN%d:POW?'%(self.slot, self.head)
        return float(self.inst.ask(strCmd))

    def setAvgTime(self, secs):
        cmd = 'SENS%d:CHAN%d:POW:ATIM %f'%(self.slot, self.head, secs)
        self.inst.write(cmd)

class psAG3631:
    '''This is an Agilent triple output E3631A power supply'''
    def __init__(self, strVisa):
        self.strVisa = strVisa
        
    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.inst.ask(cmd)
        #print 'Connected:', self.name
        
    def disconnect(self):
        cmd = 'GTL'
        self.inst.write(cmd)
        del self.inst

    def beep(self):
        self.inst.write('SYST:BEEP')
        
    def setText(self, strText = None):
        if strText:
            self.inst.write('DISP:TEXT "%s"' % strText)
        else:
            self.inst.write('DISP:TEXT:CLEAR')
            
    def clearText(self):
        self.setText()
    
    def setVoltCurr(self, selOutput = 'P6V' , volts = 0.0, current = 0.1):
        '''Selects which output of the supply with selOutput.
        Sets the voltage output, and current limit'''
        cmd = 'APPL' + ' ' + selOutput.upper() + ',' + str(volts) + ',' + str(current)
        #print 'set voltage command=',cmd
        self.inst.write(cmd)
        return

    def getVolts(self, selOutput = 'P6V'):
        cmd = 'MEAS:VOLT? '+selOutput
        self.inst.ask(cmd)
        self.Volt = float(self.inst.ask(cmd))
        return self.Volt

    def getCurr(self,selOutput = 'P6V'):
        '''Measure the output current of selected supply'''
        cmd = 'MEAS:CURR? '+selOutput
        self.Curr = float(self.inst.ask(cmd))
        return self.Curr
    
    def getPowerConsumption(self, strOutput = 'P6V'):
        return abs(self.getVolts(strOutput)*self.getCurr(strOutput))
        
    def setOutputState(self, state = 'NONE'):
        'This command enables the voltage output when state = ON, and disables the voltage output when state = OFF'
        state = state.upper()
        #print state
        if state == "NONE":
            cmd = 'OUTP:STAT?'
        elif state == "ON":
            cmd = 'OUTP:STAT ON'
        elif state == "OFF":
            cmd = 'OUTP:STAT OFF'
        else:
            raise 'Invalid Input'
        self.inst.write(cmd)
        if state == "NONE":
            s = self.inst.read()
            return (int(s))
        else: return state
        
    def setState(self, state = 'NONE'):
        return self.setOutputState(state)

class fujiVIPA:
    '''This is an Fujisu VIPA chromatic dispersion emulator'''
    def __init__(self, strVisa):
        self.strVisa = strVisa
        self.delay = 0.2

    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.vipa_query(cmd)
        print 'Connected:', self.name
        
    def disconnect(self):
        cmd = 'GTL'
        self.vipa_write(cmd)
        del self.inst

    def setWavelength(self, fltWL='NONE'):
        if fltWL != 'NONE':
            cmd = 'WVLN%.2f' % fltWL
            self.vipa_write(cmd)
        cmd = 'TWVLN?'
        strRet = self.vipa_query(cmd)
        strRet = strRet.rstrip('[nm]')
        return float(strRet)

    def setFrequency(self, fltFreq='NONE'):
        if fltFreq != 'NONE':
            cmd = 'WVFQ%.3f' % fltFreq
            self.vipa_write(cmd)
        cmd = 'TWVFQ?'
        strRet = self.vipa_query(cmd)
        strRet = strRet.rstrip('[THz]')
        return float(strRet)

    def setDispersion(self, fltDisp='NONE'):
        if fltDisp != 'NONE':
            cmd = 'DPSN%.0f' % fltDisp
            self.vipa_write(cmd)
        cmd = 'TDPSN?' 
        strRet = self.vipa_query(cmd)
        strRet = strRet.rstrip('[ps/nm]')
        return float(strRet)

    def nowWavelength(self):
        cmd = 'NWVLN?'
        strRet = self.vipa_query(cmd)
        strRet = strRet.rstrip('[nm]')
        return float(strRet)

    def nowFrequency(self):
        cmd = 'NWVFQ?'
        strRet = self.vipa_query(cmd)
        strRet = strRet.rstrip('[THz]')
        return float(strRet)

    def nowDispersion(self):
        cmd = 'NDPSN?'
        strRet = self.vipa_query(cmd)
        strRet = strRet.rstrip('[ps/nm]')
        return float(strRet)

    def getStatus(self):
        cmd = 'ALLGRN?'
        strRet = self.vipa_query(cmd)
        if strRet == 'YES':
            status = 'ALL GREEN'
        else:
            status = 'STILL TUNING'
        return status

    def setAndSettle(self, fltDisp='NONE', fltFreq='NONE', fltWL='NONE'):
        if fltDisp != 'NONE':
            self.setDispersion(fltDisp)
        if fltFreq != 'NONE':
            self.setFrequency(fltFreq)
        if fltWL != 'NONE':
            self.setWavelength(fltWL)
        currStatus = ''
        while currStatus != 'ALL GREEN':
            currWL = self.nowWavelength()
            currFreq = self.nowFrequency()
            currDisp = self.nowDispersion()
            currStatus = self.getStatus()
            setFreq = self.setFrequency()
            setWL = self.setWavelength()
            setDisp = self.setDispersion()
            print 'SetDisp=%.0f, NowDisp=%.0f, SetFreq=%.2f, NowFreq=%.2f, SetWL=%.2f, NowWL=%.2f, Status=%s' % (setDisp, currDisp, setFreq,currFreq,setWL,currWL,currStatus)

    def vipa_write(self,cmd):
        delay = self.delay
        while delay < 2.0:          
            try:
                time.sleep(delay)
                self.inst.write(cmd)
                return
            except:
                delay += 0.1
                print 'delay increased to %0.1f' % delay
        print 'GPIB FAILURE: WRITE'
        raise

    def vipa_query(self,cmd):
        delay = self.delay
        while delay < 2.0:
            try:
                time.sleep(delay)
                self.inst.write(cmd)
                time.sleep(delay)
                strRet = self.inst.read()
                if strRet == 'ERROR':
                    raise
                return strRet
            except:
                delay += 0.1
                print 'delay increased to %0.1f' % delay
        print 'GPIB FAILURE: QUERY'
        raise

class tds_3054B:
    '''This is a Tektronix TDS 3054B Oscilloscope'''
    def __init__(self, strVisa):
        self.strVisa = strVisa
        self.delay = 0.0

    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.delay_query(cmd)
        print 'Connected:', self.name
        
    def disconnect(self):
        cmd = 'GTL'
        self.delay_write(cmd)
        del self.inst

    def delay_write(self,cmd):
        delay = self.delay
        while delay < 2.0:          
            try:
                time.sleep(delay)
                self.inst.write(cmd)
                return
            except:
                delay += 0.1
                print 'delay increased to %0.1f' % delay
        print 'GPIB FAILURE: WRITE'
        raise

    def delay_query(self,cmd):
        delay = self.delay
        while delay < 2.0:
            try:
                time.sleep(delay)
                self.inst.write(cmd)
                time.sleep(delay)
                strRet = self.inst.read()
                if strRet == 'ERROR':
                    raise
                return strRet
            except:
                delay += 0.1
                print 'delay increased to %0.1f' % delay
        print 'GPIB FAILURE: QUERY'
        raise

    def capture(self, strSource):
        #valid waveform source strings are CH1, CH2, CH3, CH4, MATH, MATH1 (same as MATH), REF1, REF2, REF3, and REF4
        self.delay_write('DATa:SOUrce %s' % strSource)
        self.delay_write('DATa:ENCdg ASCIi')
        self.delay_write('DATa:WIDth 2')
        self.delay_write('DATa:STARt 1')
        self.delay_write('DATa:STOP 10000')
        ##preamble = self.delay_query('WFMPRe?')
        x_inc = float(self.delay_query('WFMPre:XINcr?'))
        x_zero = float(self.delay_query('WFMPre:XZEro?'))
        y_mult = float(self.delay_query('WFMPre:YMUlt?'))
        y_offset = float(self.delay_query('WFMPre:YOFf?'))
        y_zero = float(self.delay_query('WFMPre:YZEro?'))
        ##lstX_values = numpy.arange(x_zero, x_zero + x_inc*10000.0, x_inc)
        lstX_values = numpy.arange(0.0, x_inc*10000.0, x_inc)
        # value_in_units = ((curve_in_dl -- YOFF_in_dl) * YMULT) + YZERO_in_units
        lstWaveform = self.delay_query('CURVE?').split(',')
        lstY_values = []
        for i in lstWaveform:
            lstY_values.append((float(i) - y_offset)*y_mult + y_zero)
        return (lstX_values, lstY_values)

    def trig_force(self):
        self.inst.write('TRIGger:FORCe')

    def set_single_seq(self):
        self.delay_write('ACQuire:STOPAfter SEQuence')

    def run(self):
        self.delay_write('ACQUIRE:STATE RUN')
    
class HP_DAQ:
    '''This is an HP/Agilent Data Aqcisition Unit'''

    def __init__(self, strVisa):
        self.strVisa = strVisa
        self.delay = 0.2

    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.delay_query(cmd)
        #print 'Connected:', self.name
        
    def disconnect(self):
        cmd = 'GTL'
        self.delay_write(cmd)
        del self.inst

    def delay_write(self,cmd):
        delay = self.delay
        while delay < 0.5:          
            try:
                time.sleep(delay)
                self.inst.write(cmd)
                return
            except:
                delay += 0.1
                ##print 'delay increased to %0.1f' % delay
        print 'GPIB FAILURE: WRITE'
        raise

    def delay_query(self,cmd):
        delay = self.delay
        while delay < 0.5:
            try:
                time.sleep(delay)
                self.inst.write(cmd)
                time.sleep(delay)
                strRet = self.inst.read()
                if strRet == 'ERROR':
                    raise
                return strRet
            except:
                delay += 0.1
                ##print 'delay increased to %0.1f' % delay
        print 'GPIB FAILURE: QUERY'
        raise

    def getTemp(self, intChannel):
        temp = float(self.delay_query('MEAS:TEMP? TC , K , (@%d)' % intChannel))
        return temp
        
    def actuatorState(self, intChannel, state=None):
        if state:
            self.delay_write('ROUTE:%s (@%d)' % (state, intChannel))
        ##state = self.delay_query()
        return state

class TE_Oven_F4:
    '''This is a Test Equity oven with an F4 controller (Serial ModBus)'''

    def __init__(self, strCommPort):
        self.port = strCommPort
        self.delay = 0.2

    def connect(self):
        print 'self.port=',self.port
        self.inst = minimalmodbus.Instrument(self.port, 1)
        #print 'Connected to F4 oven controller modbus'
        
    def disconnect(self):
        pass

    def getTemp(self,factor=10.0):
        temperature = self.inst.read_register(100, signed=True)/factor
        return temperature

#    def setTemp(self, temp=None):
    def setTemp(self, temp,factor=10.0):
#        if temp:
#            self.inst.write_register(300, temp*10.0, signed=True)
        self.inst.write_register(300, temp*factor, signed=True)
        temperature = self.inst.read_register(300, signed=True)/factor
        return float(temperature)


class pAgilent33250A:
    def __init__(self, strVisa):
        self.strVisa = strVisa
        
    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.inst.ask(cmd)
        #print 'Connected:', self.name
        
    def disconnect(self):
        cmd = 'GTL'
        self.inst.write(cmd)
        del self.inst

    def write(self,cmd):
        self.inst.write(cmd)

    def read(self,cmd):
        return self.inst.ask(cmd)        
    def SetPatternFreqAmpOffset(self, pattern = 'SINusoid', freq=4000000.0, amp=3.3, offset=1.65):
        cmd = 'APPLy:' + pattern + ' ' + str(freq) + ',' + str(amp) + ',' + str(offset)
        #print cmd
        #self.inst.write('APPLy:SINusoid 50,0.1,1.25')
        self.inst.write(cmd)
    def sendCmd(self,cmd):
        self.inst.write(cmd)
        
# this driver was originated in Michael M's "instrumentDrivers.py"
# for use with HP's 86120B wavelength meter
class HP86120C:
    def __init__(self, strVisa):
        self.strVisa = strVisa
    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.inst.ask(cmd)
        print 'Connected:', self.name
    def getFrequency(self):
        cmd = 'fetc:SCAL:POW:FREQ?'
        result = float(self.inst.ask(cmd))/1E12
        return result
    def getPower(self):
        strCmd = 'FETC:SCAL:POW?'
        return float(self.inst.ask(strCmd))

class HP86122A:
    def __init__(self, strVisa):
        self.strVisa = strVisa
        self.delay = 0.2
    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.inst.ask(cmd)
        #print 'Connected:', self.name
        self.setFreeze()
    def disconnect(self):
        cmd = 'GTL'
        self.inst.write(cmd)
        del self.inst
    def turnOffAverage(self):
        'Turns off averaging'
        #self.device = ibdev(self.board, self.pad, 0, T1s, 1, 0)
        cmd = ':CALCulate2:PWAVerage OFF'
        #self.inst.write(cmd)
        self.inst.write(cmd)
       # s = str(ibrd(self.device, 200))
       # return (s)
    def setAverage(self, Average):
        '''Note: This will turn on Weighted averaging. It doesnt do
        anything with the 'Average' Variable. Its just there for
        compatability with Burleigh'''
        cmd = ':CALCulate2:PWAVerage ON'
        #self.inst.write(cmd)
        self.inst.write(cmd)
        #s = str(ibrd(self.device, 200))
        #return (s)
    def setFreeze(self):
        '''set non continuous mode'''
        cmd = ':INITiate:CONTinuous OFF'
        #self.inst.write(cmd)
        self.inst.write(cmd)
        #s = str(ibrd(self.device, 200))
        #return (s)
    def getFrequency(self,RES = None):
        '''returns frequency in Thz.
        Choose from one of the following Resolutions
        1) MINimum      = 0.001
        2) EXTended1    = 0.0001
        3) DEFault      = Current
        4) MAXimum      = 0.01'''
        #self.SetTimeout(17)
        cmd = ':FETC:SCAL:POW:FREQ?'
#        if RES:
#            if type(RES) == types.StringType:
#                cmd += str(RES)
#            else:
#                raise exceptions.TypeError, "Expecting Sting type. Use Module doc for more help"
        #print cmd
        #strResp = self.query(cmd)
        strResp = self.delay_query(cmd)
        if (strResp.find('LO') != -1) :
            return (-1.0)
        s=float(strResp)
        s/=1000000000000.00
        return s
    def getPower(self, RES = None):
        '''returns Power in dBm.
        Choose from one of the following Resolutions
        1) MINimum      = 0.001
        2) EXTended1    = 0.0001
        3) DEFault      = Current
        4) MAXimum      = 0.01'''
        cmd = ':MEAS:SCAL:POW?'
#        if RES:
#            if type(RES) == types.StringType:
#                cmd += str(RES)
#            else:
#                raise exceptions.TypeError, "Expecting Sting type. Use Module doc for more help"
        #strResp = self.query(cmd)
        strResp = self.delay_query(cmd)
        if (strResp.find('LO') != -1) :
            return (-1.0)
        return float(strResp)
    def delay_query(self,cmd):
        delay = self.delay
        while delay < 2.0:
            try:
                time.sleep(delay)
                self.inst.write(cmd)
                time.sleep(delay)
                strRet = self.inst.read()
                if strRet == 'ERROR':
                    raise
                return strRet
            except:
                delay += 0.1
                print 'delay increased to %0.1f' % delay
        print 'GPIB FAILURE: QUERY'
        raise

class HP34401A:
    'This is a Multimeter'
    version = 1.0
    def __init__(self, strVisa):
        self.strVisa = strVisa
        self.delay = 0.2
        
    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.inst.ask(cmd)
        #print 'Connected:', self.name
        
    def disconnect(self):
        cmd = 'GTL'
        self.inst.write(cmd)
        del self.inst

    def getVoltage(self,samples=10):
        #print "getvoltage in ttxop"
        cmd="CONF:VOLT:DC"
        self.inst.write(cmd)
        cmd = 'VOLT:DC:NPLC 0.1'
        self.inst.write(cmd)
        cmd = 'samp:coun %d'%(samples)
        self.inst.write(cmd)
        cmd = 'init'
        self.inst.write(cmd)
        cmd = 'READ?'
        #s = (self.query(cmd))
        s = self.delay_query(cmd)
        #    s = (self.query(cmd,1000,.5))
        lst=s.split(',')
        if len(lst)==1:
            return float(lst[0])
        else:
            a = map(float, lst)
            #print a
            sum=0
            for i in range (samples):
                sum=sum+a[i]
            ave=sum/samples
            #print ave
            return ave
            
        return (a)

    def measureDCCurrent(self):
        print 'Measure DC Current'
        cmd = 'MEASure:CURRent:DC?'
        #s = self.query(cmd)
        s = self.delay_query(cmd)
        return (float(s))
        
    def delay_query(self,cmd):
        delay = self.delay
        while delay < 2.0:
            try:
                time.sleep(delay)
                self.inst.write(cmd)
                time.sleep(delay)
                strRet = self.inst.read()
                if strRet == 'ERROR':
                    raise
                return strRet
            except:
                delay += 0.1
                print 'delay increased to %0.1f' % delay
        print 'GPIB FAILURE: QUERY'
        raise

class Agilent34970A:
    'Data Aquisition/Switch Unit'
    version = 1.0
    def __init__(self, strVisa):
        self.strVisa = strVisa
        self.delay = 0.2
        
    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.inst.ask(cmd)
        #print 'Connected:', self.name
        
    def getVoltage(self, slot = 102):
        'Measure voltage on the channel number specified by the string channel, and int slot'
        cmd = 'MEAS:VOLT:DC?'+ ' ' + '(' + '@' + str(slot) + ')'
#        print cmd
        #self.Volts = float(self.delay_query(cmd))
        self.inst.write(cmd)
        time.sleep(1)
        strRet= self.inst.read()
#        print strRet
        self.Volts = float(strRet)
#        print self.Volts
        return self.Volts

    def getTemperature(self, slot = 102):
        'Measure temp on the channel number specified by the string channel, and int slot'
        cmd = 'MEAS:TEMP?'+ ' ' + '(' + '@' + str(slot) + ')'
#        print cmd
        #self.Volts = float(self.delay_query(cmd))
        self.inst.write(cmd)
        time.sleep(1)
        strRet= self.inst.read()
#        print strRet
        self.Volts = float(strRet)
#        print self.Volts
        return self.Volts

    def setCloseSwitch(self, chanList = '201'):
        '''Closes the specified switch postion in slot 2 or 3 '''
        slotLimit = 200
        chanList = str(chanList)
        #if slot < slotLimit:
         #   raise Exception,'Channel: %d does not have this function ' %slot
        cmd = 'ROUTE:CLOSE' + ' ' + '(@' + chanList.upper() + ')'
#        print cmd
        self.inst.write(cmd)
        return

    def setOpenSwitch(self, chanList = '201'):
        '''Closes the specified switch postion in slot 2 or 3 '''
        slotLimit = 200
        chanList = str(chanList)
        #if slot < slotLimit:
          #  raise Exception,'Channel: %d does not have this function ' %slot
        cmd = 'ROUTE:OPEN' + ' ' + '(@' + chanList.upper() + ')'
        self.inst.write(cmd)
        return
    def setSwitchState(self, chanList = '201', blnState = 0):
        if blnState:
            self.setCloseSwitch(chanList)
        else:
            self.setOpenSwitch(chanList)
            
    def getSwitchState(self, nChannel):
        strCmd = 'ROUTE:CLOSE? (@' + str(nChannel) + ')'
        strResp = self.delay_query(strCmd)
        # replies '0\n' for open, '1\n' for closed 
        strResp = strResp.strip()
        return int(strResp)

    def getSwitchStates(self, chanList):
        chanList = str(chanList)
        strCmd = 'ROUTE:CLOSE? (@' + chanList.upper() + ')'
        strResp = self.delay_query(strCmd)
        # replies '0\n' for open, '1\n' for closed 
        strResp = strResp.strip()
#        print '---------------------'
#        print strResp
    
    def open(self, channel):
        #ibclr(self.__class__.devicedict[self.key])
        cmd = ""
        for x in channel: cmd += str(x)+', '
        # strip the last two string chars
        #ROUT:CLOS (@  2,  3)
        cmd = cmd[:len(cmd)-2]
        cmd = 'ROUT:OPEN (@ '+ cmd + ')'
#        if printcmd : print(cmd)
        self.inst.write(cmd)

    def close(self,channel):
        #ibclr(self.__class__.devicedict[self.key])
        cmd = ""
        for x in channel: cmd += str(x)+', '
        # strip the last two string chars
        #ROUT:CLOS (@  2,  3)
        cmd = cmd[:len(cmd)-2]
        cmd = 'ROUT:CLOS (@ '+ cmd + ')'
        #if printcmd : print(cmd)
        self.inst.write(cmd)

    def configureForVolt(self,channel):
        if types.ListType != type(channel):
            channel = [channel]
        #ibclr(self.__class__.devicedict[self.key])
        cmd = ""
        for x in channel: cmd += str(x)+', '
        # strip the last two string chars
        #ROUT:CLOS (@  2,  3)
        cmd = cmd[:len(cmd)-2]
        cmd = 'CONF:VOLT:DC AUTO, (@ '+ cmd + ')'
        #if printcmd : print(cmd)
        self.inst.write(cmd)

    def ClearReset(self):
        cmd ='*CLS'
        self.inst.write(cmd)
        cmd ='*RST'
        self.inst.write(cmd)
        
    def delay_query(self,cmd):
        delay = self.delay
        while delay < 2.0:
            try:
                time.sleep(delay)
                self.inst.write(cmd)
                time.sleep(delay)
                strRet = self.inst.read()
                if strRet == 'ERROR':
                    raise
                return strRet
            except:
                delay += 0.1
                print 'delay increased to %0.1f' % delay
        print 'GPIB FAILURE: QUERY'
        raise
class AndoAQ8291:
    '''Ando Mainframe with Switches AQ8101A'''
    version = 1.0
    def __init__(self, strVisa):
        self.strVisa = strVisa
        self.delay = 0.2

    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.inst.ask(cmd)
        print 'Connected:', self.name

    def disconnect(self):
        #cmd = 'GTL'
        #self.inst.write(cmd)
        del self.inst

    def setRoute(self,slot,device,input,output):
        'set optical switch path'
        #cmd = ':ROUT:CLOS '+"%d,%d,%d,%d,%d" %(chassis,slot,device,input,output)
        cmd = 'C%02d,D%02d,SA%dSB%d' %(slot,device,input,output)
        #print cmd
        self.inst.write(cmd)
        return

    def getRoute(self,chassis,slot,device,input):
        'get optical switch path'
        cmd = 'SASB?'
        resp = self.delay_query(cmd)
        return resp
    
    def delay_query(self,cmd):
        delay = self.delay
        while delay < 0.5:
            try:
                time.sleep(delay)
                self.inst.write(cmd)
                time.sleep(delay)
                strRet = self.inst.read()
                if strRet == 'ERROR':
                    raise
                return strRet
            except:
                delay += 0.1
                print 'delay increased to %0.1f' % delay
        print 'GPIB FAILURE: QUERY'
        raise
