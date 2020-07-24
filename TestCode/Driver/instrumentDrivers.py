# This is a  set of instrument drivers written for use with Python 2.6
# written by Jeremy Machi

import visa
import time
import minimalmodbus

class NP2832C:
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

class attHP8156:
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

class psAG3631:
    '''This is an Agilent triple output E3631A power supply'''
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

class Agilent6624A:
    '''This is an Agilent quad output E6624A power supply'''
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
    
    def setVoltCurr(self, selOutput = 1 , volts = 0.0, current = 0.1):
        '''Selects which output of the supply with selOutput.
        Sets the voltage output, and current limit'''
        cmd = 'VSET' + ' ' + str(selOutput) + ',' + str(volts) + ';'
        self.inst.write(cmd)
        cmd = 'ISET' + ' ' + str(selOutput) + ',' + str(current) + ';'
        self.inst.write(cmd)
        return

    def getVolts(self, selOutput = 1):
        cmd = 'VOUT?' + str(selOutput)
        Volt = float(self.inst.ask(cmd))
        return Volt

    def getCurr(self,selOutput = 1):
        '''Measure the output current of selected supply'''
        cmd = 'IOUT?' + str(selOutput)
        Curr = float(self.inst.ask(cmd))
        return Curr
    
    def getPowerConsumption(self, selOutput = 1):
        return abs(self.getVolts(selOutput)*self.getCurr(selOutput))
        
    def setOutputState(self, state = 'NONE', output=1):
        'This command enables the voltage output when state = ON, and disables the voltage output when state = OFF'
        state = state.upper()      
        if state == "NONE":
            cmd = 'OUT? %d' % output
        elif state == "ON":
            cmd = 'OUT %d,1' % output
        elif state == "OFF":
            cmd = 'OUT %d,0' % output
        else:
            raise 'Invalid Input'
        self.inst.write(cmd)
        if state == "NONE":
            s = self.inst.read()
            return (int(s))
        else: return state
        
    def setState(self, state = 'NONE'):
        return self.setOutputState(state)

class JDSU_MAP_Switch:
    '''This is an JDSU 1x4 optical switch'''
    def __init__(self, strVisa, intChassis, intSlot, intDevice):
        self.strVisa = strVisa
        self.intSlot = intSlot
        self.intChassis = intChassis
        self.intDevice = intDevice
        
    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.inst.ask(cmd)
        print 'Connected:', self.name
        
    def disconnect(self):
        cmd = 'GTL'
        self.inst.write(cmd)
        del self.inst

    def route(self, input, output=None):
        if output:
            cmd = ':ROUT:CLOS %d,%d,%d,%d,%d' % (self.intChassis, self.intSlot, self.intDevice, input, output)
            self.inst.write(cmd)
        cmd = ':ROUT:CLOS? %d,%d,%d,%d' % (self.intChassis, self.intSlot, self.intDevice, input) 
        return int(self.inst.ask(cmd))

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

class BurleighWA1100:
    'This is a Wavelength meter'
    version = 1.00
    def __init__(self, strVisa):
        self.strVisa = strVisa

##    def __repr__(self):
##        s = 'Description: Burleigh 1100 Wave meter\n'
##        s += __repr__(self)
##        return(s)

    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.inst.ask(cmd)
        print 'Connected:', self.name


    def setTemplate(self,waveln_nm=1000,Avtm=0.2):
        cmd = 'sense1:chan1:pow:atime '+str(Avtm)+';wave '+str(waveln_nm)
        self.write(cmd)


    def get_template(self):
        cmd = 'FETC:SCAL:POW?'
        return (float(self.query(cmd)))


    def turnOffAverage(self):
        cmd = ':SENS:AVER OFF'
        self.write(cmd)


    def setAverage(self, Average):
        cmd = ':SENS:AVER '+str(Average)
        self.write(cmd)

    def getFrequency(self):
        cmd = ':FETC:FREQ?'
##        ##cmd = ':FETC:SCAL:FREQ?'
##        string = self.query(cmd)
##        if (string.find('LO') != -1) :
##            return (-1.0)
##        s=float(string)
##        s/=1000
        result = float(self.inst.ask(cmd))/1000
        return result



    #getFrequency = getFrequency    

    def getDisplayPower(self):
        cmd = ':FETC:POW?'
        return (float(self.query(cmd)))

    def reset_measurement(self):
        cmd=':CALC:RES'
        self.write(cmd)    
    
   

class CSA8200:
    'This a Tektronix CSA8200 Communications Signal Analyzer'
    def __init__(self, strVisa):
        self.strVisa = strVisa

        # Instrument specific
        self.__measMaxIndex = 8 # Maximum number of measuremnet
        self.currentChannel = 1 # default channel 1
        #self.queryDelay = 0.2 #[sec] delay for query

        # Measurement list
        self.__extinctionRatioList = (1, 'EXTINCTDB')
        self.__CrossingList = (2, 'PCTCROss')
        self.__Pk2PkJitterList = (3, 'PKPKJitter')
        self.__RMSJitterList = (4, 'RMSJitter')
        self.__QualityFactorList = (5, 'QFACtor')
        self.__RiseList = (6, 'RISe')
        self.__FallList = (7, 'FALL')
        self.__AOPList = (8, 'AOPTPWRDBM')
        self.__fltGarbageThreshold = 1.0e6

    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.inst.ask(cmd)
        print 'Connected:', self.name

    def lockFrontPanel(self):
        self.inst.write('LOCK ALL')
    def unlockFrontPanel(self):
        self.inst.write('UNLOCK ALL')

    def PrintScreen(self,filename):
        self.inst.write('HARDCopy:filename "%s"' % filename)
        print 'HARDCopy:filename "%s"' % filename
        time.sleep(3)
        self.inst.write('HARDCopy')
        time.sleep(.5)
        self.inst.write('*WAI')

    def AcquireWaveForm(self, waveFormNumb, filename = ''):
        '''Optionally save screen under filename'''
        self.inst.write('ACQuire:STATE OFF')
        time.sleep(.5)
        self.inst.write('ACQuire:STOPAFTER:MODE CONDITION')
        time.sleep(.5)
        self.inst.write('ACQuire:STOPAFTER:COUNT %d' % waveFormNumb)
        time.sleep(.5)
        self.inst.write('ACQuire:STOPAfter:CONDition ACQWfms')
        if filename <> '':
            #self.write('ACQuire:SAVEFile:SAVEScreen '+ '"%s"' % filename )
            #self.write('ACQuire:STOPAfter:ACTion SAVEScreen')
            time.sleep(.5)
            self.inst.write('ACQuire:STOPAfter:ACTion NONE')
        else:
            time.sleep(.5)
            self.inst.write('ACQuire:STOPAfter:ACTion NONE')

        time.sleep(.5)
        self.inst.write('ACQuire:DATA:CLEAR')
        # run acquisition
        self.inst.write('ACQuire:STATE ON')
        time.sleep(1.0)
        self.WaitForOperationComplete()
        float(self.__GetResultString('MEASUrement:MEAS%d:VALue?' % self.__extinctionRatioList[0]))
        time.sleep(.5)
        if filename <> '':
            self.inst.write('HARDCopy:filename "%s"' % filename)
            time.sleep(3)
            self.inst.write('HARDCopy')
            time.sleep(.5)
            self.inst.write('*WAI')

    def RecallSetup(self, filename):
        self.inst.write('REC:SETU "%s"' % filename)

    # Setup scope to read following measurements
    # 1: Amplitude (NZR) -> ER (Extinction ratio [dB])
    # 2: Crossing (%)
    # 3: Pk-Pk Jitter
    # 4: RMS Jitter
    # 5: Quality Factor
    def SetupScopeMeasurement(self):
        '''Setup scope Measurements'''
        self.inst.write('*CLS')
        self.inst.write('AUTOSET:TYPE EYE')
        time.sleep(0.1)
        self.inst.write('SELECT:CH%d ON' % (self.currentChannel))
        time.sleep(0.1)
        # // set the wfmdb source and enable and display the wfmdb
        self.inst.write('WFMDB:WFMDB1:SOURCE CH%d,MAIN' % (self.currentChannel))
        time.sleep(0.1)
        self.inst.write('WFMDB:WFMDB1:ENABLE ON')
        time.sleep(0.1)
        self.inst.write('WFMDB:WFMDB1:DISPLAY ON')

        # Mask settings
        self.inst.write('MASK:DISPLAY ON') # turn off mask
        time.sleep(0.1)
        self.inst.write('MASK:AUTOSET:MODE MANUAL')
        time.sleep(0.1)
        #self.write('MASK:STANDARD OC192')
        self.inst.write('MASK:STANDARD FEC10709')
        time.sleep(0.1)
        self.inst.write('MASK:SOURCE CH%d' % (self.currentChannel))
        time.sleep(0.1)
        #self.write('MASK:AUTOSET:MODE AUTO')
        #self.write('MASK:WFMDB:STATE ON') # FIX: is it really what we want?
        #self.write('MASK:MARgin:PERCENT 10.0') # FIX: what is the percentage?
        #self.write('MASK:MARgin:STATE ON')

        #self.write('CH%d:EXTAtten:MODE DB' % (self.currentChannel))
        #self.write('CH%d:EXTAtten:VALue 0' % (self.currentChannel))
        time.sleep(0.1)
        self.inst.write('HARDCopy:FORMat JPEG')
        time.sleep(0.1)
        # Set measurements
        for meas in (self.__extinctionRatioList,
                     self.__CrossingList,
                     self.__Pk2PkJitterList,
                     self.__RMSJitterList,
                     self.__QualityFactorList,
                     self.__RiseList,
                     self.__FallList,
                     self.__AOPList):
            self.inst.write('MEASUrement:MEAS%d:TYPE %s' % (meas[0],meas[1]))
            time.sleep(0.1)
            self.inst.write('MEASUrement:MEAS%d:SOURCE1:WFM CH%d' % (meas[0], self.currentChannel))
            time.sleep(0.1)
            self.inst.write('MEASUrement:MEAS%d:SOURCE1:WFMDB:SIGType EYE' % (meas[0]))
            time.sleep(0.1)
            self.inst.write('MEASUrement:MEAS%d:STATE ON' % (meas[0]))
            time.sleep(0.1)

        # Rise and fall measurements
        self.inst.write('MEASUrement:MEAS%d:REFLevel:METHod RELative' % self.__RiseList[0])
        time.sleep(0.1)
        self.inst.write('MEASUrement:MEAS%d:REFLevel:RELative:HIGH 80' % self.__RiseList[0])
        time.sleep(0.1)
        self.inst.write('MEASUrement:MEAS%d:REFLevel:RELative:LOW 20' % self.__RiseList[0])
        time.sleep(0.1)

        self.inst.write('MEASUrement:MEAS%d:REFLevel:METHod RELative' % self.__FallList[0])
        time.sleep(0.1)
        self.inst.write('MEASUrement:MEAS%d:REFLevel:RELative:HIGH 80' % self.__FallList[0])
        time.sleep(0.1)
        self.inst.write('MEASUrement:MEAS%d:REFLevel:RELative:LOW 20' % self.__FallList[0])
        time.sleep(0.1)

        # Recall setup and overwrite these files
        #self.RecallSetup('C:\\Config\Setup.stp')

    def __GetResultString(self, queryString):
        '''Extract result from query. Example: MEASU:MEAS1:VAL?
        v1.5.2.2 returns: 51.1\n
        v1.3.3.1 returns: MEASU:MEAS1:VAL? 51.1\n'''
        result = self.inst.ask(queryString)
        if result.find(' ')>=0:
            return result.split(' ')[1]
        else:
            return result

    def GetExtinctionRatio(self):
        fltReturn = float(self.__GetResultString('MEASUrement:MEAS%d:VALue?' % self.__extinctionRatioList[0]))
        if abs(fltReturn) > self.__fltGarbageThreshold:
            print 'Exitinction Ratio Exception. Scope is returning garbage value for ER.  Check scope for bad eye or no eye.'
            #raise InstrumentException('Scope is returning garbage value for ER.  Check scope for bad eye or no eye.')
        return fltReturn

    def GetCrossing(self):
        fltReturn = float(self.__GetResultString('MEASUrement:MEAS%d:VALue?' % self.__CrossingList[0]))
        if abs(fltReturn) > self.__fltGarbageThreshold:
            print 'Crossing Exception. Scope is returning garbage value for Xing.  Check scope for bad eye or no eye.'
            #raise InstrumentException('Scope is returning garbage value for crossing.  Check scope for bad eye or no eye.')
        return fltReturn
    
    def GetPk2PkJitter(self):
        return float(self.__GetResultString('MEASUrement:MEAS%d:VALue?' % self.__Pk2PkJitterList[0]))

    def GetRMSJitter(self):
        return float(self.__GetResultString('MEASUrement:MEAS%d:VALue?' % self.__RMSJitterList[0]))

    def GetQualityFactor(self):
        return float(self.__GetResultString('MEASUrement:MEAS%d:VALue?' % self.__QualityFactorList[0]))

    def GetRise(self):
        return float(self.__GetResultString('MEASUrement:MEAS%d:VALue?' % self.__RiseList[0]))

    def GetFall(self):
        return float(self.__GetResultString('MEASUrement:MEAS%d:VALue?' % self.__FallList[0]))
    def GetAverageOpticalPower(self):
        return float(self.__GetResultString('MEASUrement:MEAS%d:VALue?' % self.__AOPList[0]))
    def GetScopeMeasurementList(self):
        measTypeList = []
        for i in range(1, self.__measMaxIndex+1):
            measTypeList.append(self.query('MEASUrement:MEAS%d:TYPE?' % (i)))
        return measTypeList

    def EnableMaskCount(self, onFlag):
        '''Turn on/off mask count. onFlag 1:on, 0:off'''
        if onFlag:
            self.write('MASK:DISPLAY ON')
            time.sleep(.5)
            self.write('MASK:COUNT:STATE ON')
        else:
            self.write('MASK:DISPLAY OFF') # turn off mask
            time.sleep(.5)
            self.write('MASK:COUNT:STATE OFF')

    def GetMaskHits(self):
        # Returns number of hits on the mask
        return int(self.__GetResultString('MASK:COUNt:TOTal?'))

    def SetFilter(self, filterType, blnReadBack = 1):
        '''filterType: 0:off, 1:OC192, 2:FEC 10.71'''
        if filterType == 1:
            self.inst.write('CH%d:FILTer:VALue OC192' % self.currentChannel)
        elif filterType == 2:
            self.inst.write('CH%d:FILTer:VALue FEC10709' % self.currentChannel)
        else:
            self.inst.write('CH%d:FILTer:VALue NONe' % self.currentChannel)

        if blnReadBack:
            nRead = self.GetFilter()
            if filterType != nRead:
                raise InstrumentException('Eye scope tried to set filter to %d but read back %d' % \
                                          (filterType, nRead))

    #<DS>
    def GetFilter(self):
        strCmd = 'CH%d:FILTer:VALue?' % self.currentChannel
        strResp = self.inst.ask(strCmd)
        if strResp.find('NONE') != -1:
            return 0
        elif strResp.find('OC192') != -1:
            return 1
        elif strResp.find('FEC10709') != -1:
            return 2
        else:
            #raise InstrumentException('TDS8000B.GetFilter() returned unrecognized filter type:' + strResp)
            return -1
    #</DS>
    
    def ExecuteDarkCal(self):
        '''Dark level compensation'''
        self.inst.write('COMPensate:DARKLev:CH%d' % (self.currentChannel))
        time.sleep(15)
        # FIX: wait until completed!
        self.inst.write('*WAI')

    def ExecuteAutoset(self):
        self.inst.write('ACQuire:STOPAFTER:MODE RUNSTOP')
        time.sleep(0.1)
        self.inst.write('ACQuire:STATE ON')
        time.sleep(0.1)
        #self.write('ACQuire:STATE OFF')
        self.inst.write('AUTOSet EXECute')
        time.sleep(0.1)
        self.WaitForOperationComplete()
        #self.write('ACQuire:STATE ON')
        #self.write('ACQuire:STATE OFF')

    def GetID(self):
        return self.inst.ask('*IDN?')

    def WaitForOperationComplete(self):
        time.sleep(5.0)
        busy = self.__GetResultString('BUSY?')
        #print 'busy:', busy
        while busy[0] == '1': # query actually returns '1\n'
            time.sleep(1.0) # poll every 500ms
            busy = self.__GetResultString('BUSY?')
            #print 'Busy:', busy

    def SetMask(self, maskID, marginPercent):
        if maskID == 1:
            self.inst.write('MASK:STANDARD OC192')
        else:
            self.inst.write('MASK:STANDARD FEC10709')
        self.WaitForOperationComplete()
        self.inst.write('MASK:MARGIN:PERCENT %d' % int(marginPercent))


class TE_Oven_F4:
    '''This is a Test Equity oven with an F4 controller (Serial ModBus)'''

    def __init__(self, strCommPort):
        self.port = strCommPort
        self.delay = 0.2

    def connect(self):
        self.inst = minimalmodbus.Instrument(self.port, 1)
        
    def disconnect(self):
        pass

    def getTemp(self):
        temperature = self.inst.read_register(100, signed=True)/10.0
        return temperature

    def setTemp(self, temp=None):
        if temp:
            # Seems to be a bug in the minimalmodbus module so that it cannot accept a zero (code hangs)
            if temp == 0.0:
                temp == 0.1
            self.inst.write_register(300, temp*10.0, signed=True)
        temperature = self.inst.read_register(300, signed=True)/10.0
        return temperature

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
        self.delay = 0.2

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
        self.delay_write('DATa:SOUrce CH%s' % strSource)
        self.delay_write('DATa:ENCdg ASCIi')
        self.osc.delay_write('DATa:WIDth 2')
        self.delay_write('DATa:STARt 1')
        self.delay_write('DATa:STOP 10000')
        preamble = delay_query('WFMPRe?')

class HP_DAQ:
    '''This is an HP/Agilent Data Aqcisition Unit'''

    def __init__(self, strVisa, intChannel):
        self.strVisa = strVisa
        self.channel = intChannel
        self.delay = 0.2

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

    def getTemp(self):
        temp = float(self.delay_query('MEAS:TEMP? TC , K , (@%d)' % self.channel))
        return temp
        
    def actuatorState(self, state=None):
        if state:
            self.delay_write('ROUTE:%s (@%d)' % (state, self.channel))
        ##state = self.delay_query()
        return state

class JDSUAttn:
    '''This is a Optical Attenuator in the JDSU MAP Chassis'''
    def __init__(self, strVisa, intChassis, intSlot, intHead):
        self.strVisa = strVisa
        self.delay = 0.2
        self.Chassis = intChassis
        self.Slot = intSlot
        self.Head = intHead
        self.Name = ''
        self._conf = {}
        self._ActiveConf = None

    def connect(self):
        self.inst = visa.instrument(self.strVisa)
        cmd = '*IDN?'
        self.name = self.inst.ask(cmd)
        print 'Connected:', self.name
        self.SetActiveConf(chassis=self.Chassis, slot=self.Slot, head=self.Head)
        
    def disconnect(self):
        cmd = 'GTL'
        self.inst.write(cmd)
        del self.inst

    def SetActiveConf(self, Name = None,chassis = 1, slot = None, head = None  ):
        if Name == None:
            Name = "%d:%d:%d"%(chassis,slot,head)
        if not self._conf.has_key(Name):
            if chassis == None or slot == None or head == None:
                raise InstrumentException,'The Slot,chassis, head parameters cannot be empty'
            self._conf[Name] = "%d,%d,%d"%(chassis,slot,head)
        self._ActiveConf = Name

    def setWavelength(self,wavl):
        self.inst.write(":OUTP:WAV %s,%d"%(self._conf[self._ActiveConf],int(wavl)))

    def getWavelength(self,wavl):
        return int(self.inst.ask(":OUTP:WAV? %s"%(self._conf[self._ActiveConf])))


    def setAttenuation(self,Attn):
        self.inst.write(":OUTP:ATT %s,%f"%(self._conf[self._ActiveConf],float(Attn)))

    def getAttenuation(self):
        return float(self.inst.ask(":OUTP:ATT? %s"%(self._conf[self._ActiveConf])) )

    def getPower(self):
        return float(self.inst.ask(":OUTP:POW? %s"%(self._conf[self._ActiveConf])) )

    def setOutputState(self,state = 0):
        ''' [ Beam Block, Beam Enabled] '''
        self.inst.write(":OUTP:BBL %s,%d"%(self._conf[self._ActiveConf],state))

    def getOutputState(self):
        return int(self.inst.ask(":OUTP:BBL %s?"%(self._conf[self._ActiveConf])))

    def GetDiagnostics(self, retHeader = 0):
        if retHeader:
            self._attenuators = copy.deepcopy(self._conf)
            Header = ['Wavelength','Attenuation','STATE','Power Mon1'] * len(self._attenuators)
            return Header
        row = []
        for a in self._attenuators:
            row.append(float ( self.inst.ask(  ":OUTP:WAV? %s"%(self._conf[a])   ) ) )
            row.append(float ( self.inst.ask(  ":OUTP:ATT? %s"%(self._conf[a])   ) ) )
            row.append(float ( self.inst.ask(  ":OUTP:BBL? %s"%(self._conf[a])   ) ) )
            row.append(float ( self.inst.ask(  ":OUTP:POW? %s"%(self._conf[a])   ) ) )
            #row.append(float ( self.query('READ:POW? 1,1,1')))
        return row

class Keithley_2230_30_1:
    '''This is a Keithley 2230-30-1 Triple Channel DC Power Supply'''
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
    
    def setVoltCurr(self, selOutput = 1 , volts = 0.0, current = 0.1):
        '''Selects which output of the supply with selOutput.
        Sets the voltage output, and current limit'''
        cmd = 'INST:SEL CH%d' % selOutput
        self.inst.write(cmd)
        cmd = 'VOLT:LEV %f' % volts
        self.inst.write(cmd)
        cmd = 'CURR:LEV %f' % current
        self.inst.write(cmd)
        return

    def getVolts(self, selOutput = 1):
        cmd = 'INST:SEL CH%d' % selOutput
        self.inst.write(cmd)
        cmd = 'MEAS:VOLT?'
        Volt = float(self.inst.ask(cmd))
        return Volt

    def getCurr(self,selOutput = 1):
        cmd = 'INST:SEL CH%d' % selOutput
        self.inst.write(cmd)
        cmd = 'MEAS:CURR?'
        Curr = float(self.inst.ask(cmd))
        return Curr
    
    def getPowerConsumption(self, selOutput = 1):
        return abs(self.getVolts(selOutput)*self.getCurr(selOutput))
        
    def setOutputState(self, state = 'NONE', selOutput=1):
        'This command enables the voltage output when state = ON, and disables the voltage output when state = OFF'
        state = state.upper()
        cmd = 'INST:SEL CH%d' % selOutput
        self.inst.write(cmd)
        if state == "NONE":
            cmd = 'OUTP?'
        elif state == "ON":
            cmd = 'OUTP ON'
        elif state == "OFF":
            cmd = 'OUTP OFF'
        else:
            raise 'Invalid Input'
        self.inst.write(cmd)
        if state == "NONE":
            s = self.inst.read()
            return (int(s))
        else: return state
        
    def setState(self, state = 'NONE'):
        return self.setOutputState(state)

class TE_Oven_F4_GPIB:
    '''This is a Test Equity oven with an F4 controller (GPIB)'''

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

    def getTemp(self):
##        cmd = 'R? 100,1'
##        reply = self.inst.ask(cmd)
##        return float(reply)/10.0
        return 0.0

    def setTemp(self, temp):
        cmd = "W 300," + str(temp*10)
        self.inst.write(cmd)