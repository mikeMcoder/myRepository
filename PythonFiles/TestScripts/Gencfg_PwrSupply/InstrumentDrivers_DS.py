#-----------------------------------------------------------------------------
# Name:        InstrumentDrivers.py
# Purpose:
#
# Author:      <Anand S Ramalingam>
#
# Created:     2003/28/04
# RCS-ID:      $Id: InstrumentDrivers_DS.py,v 1.1 2005/05/10 21:52:56 ddstarkx Exp $
# Copyright:   (c) 2002
# Licence:     <your licence>
#-----------------------------------------------------------------------------

''' This Module provides python interface to the following GPIB instrumnets.
            1)  ANDO            'OSA'
            2)  BurleighWA1100  'Wavemeter'
            3)  Agilent3499C    'MUX'
            4)  HP34401A        '6.5 digit Multimeter'
            5)  HP3631A         'Triple Output Powersupply'
            6)  HP81619         'Powermeter'
            7)  HP3458          '8.5 digit Multimeter'
            8)  HP3499AB        'MUX'
            9)  HP3499C         'MUX'
            10) MM              'Simulated MUX-Multimeter that behaves like inidividual multimeter'
            11) HP86120         'HP86210 Wavemeter'
            12) HP86122         'HP86122 High resolution Wavemeter'
            12) ILX             'ILX TEC controller'
            13) NewPort         'NewPort TEC controller'
            14) HP86122         'High resolution HP wavemeter'
            15) HP8156A         'Optical Attenuator'
            16) AgilentE4400B          'RF Signal Generator'
            17) Agilent34970A   'Data aquisition/Switch unit'
            18) Agilent8163A/B  'Lightwave Multimeter
            19) TDS8000B        'Tektronix Digital Sampling Oscilloscope'
            20) Therm8800       'Thermotron Environmental Oven'
            21) HP83732         'RF Signal Generator, Hi Freq'

REQUIRED FILES: gpib.py, base.py in same directory as this file along with gpib.pyd
'''


from gpib import *
from base import Base,InstrumentException
import array
import time
import sys
import struct
import types
import exceptions
import math
import win32process
import win32api
import copy
printcmd = 0
verbose = 0
dbg = 0
DUMMY = -1000000000
LIGHT_SPEED = 299792458.00
mean  = lambda x: reduce(lambda a,b: a+b , x) / len (x)




def help(Class = None):
    if Class:
        if type(Class) == types.ClassType or type(Class) == types.MethodType:
            Class = str(Class)[str(Class).find('.')+1:]
        inst = eval(Class+'.__doc__')

        try:
            x = eval(Class)
        except:
            x = None
        if type(x) == types.ClassType:
            print x," has the following methods:\n"
            count = 0
            for i in dir(x):
                if type(eval(Class+'.'+i)) == types.MethodType:
                    if i[:1] != '_':
                        count +=1
                        print "%3d"%count, ') ',i
            print "Example instantiation: \n\tfrom %s import *\n\tinst = %s(0,22)\n\tinst.connect()" %(__name__,Class)
        if type(x) == types.MethodType:
            print inst
            List = Class.split('.')
            print "Example instantiation: \n\tfrom %s import *\n\tinst = %s(0,22)\n\tinst.connect()\n\tinst.%s(yet to find how to get full syntax)" %(__name__,List[0],List[1])
            args = x.func_code.co_varnames[1:x.func_code.co_argcount]
            args = list(args)
            args.reverse()
            defaults = x.func_defaults
            for i in range(len(defaults)):
                args[i] = args[i]+ ' = %s'%defaults[i]
            args.reverse()
            args = tuple(args)
            print "\tinst.%s"%List[1],args
    else:
        count = 0
        for i in DIR:
            OBJ = eval(i)
            if type(OBJ) == types.ClassType:
                count +=1
                print "%3d"%count, ") ", i ,"\t\t\t",OBJ.__doc__






class ANDO(Base):
    '''This is a Optical Spectrum Analyzer'''

    version = 01.01
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)
        self.PeakFreq=-1
        self.Peak_Ht=-1
        self.SecPeakFreq=-1
        self.SecPeakHt=-1
        self.SMSR=-1
        self.SideMode=-1
        self.TMO=0
        self.Name = ""
    def __repr__(self):
        s = 'Description: ANDO Optical Spect Analyzer\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)
        #self.device = self.Device
        #self.TMO = ibask(self.device,IbcTMO)
        self.SetTimeout(14)
        #print ("Device", self.device)
        cmd = '*IDN?'
        self.Name = self.query(cmd)
        return

    def GetSMSR(self,freq=194.00):
        cmd = 'CTRF' + str(freq);
        self.write(cmd)

        cmd = 'SGL'
        self.write(cmd)
        count=1;
        self.poll()
        cmd = 'CTR=P,SGL'
        self.write(cmd)
        count=1;
        self.poll()

        cmd='SMSR1'
        self.write(cmd)
        cmd = 'ANA?'
        s = self.query((cmd))
        f = float(s[-9:-2])
        return(f)
    measure = GetSMSR

    def getSMSRFromData(self,SMSR_Mask=0.00):
        print 'GetSMSRFromData\n'
        cmd = 'ACTV0,SMSR1,SSMSK'+ str(SMSR_Mask)
        self.write(cmd)
        cmd = 'ANA?'
        ANS = self.query(cmd)
        if len(ANS) == 0:
            raise 'Empty String'
        indexbeg=0
        indexend=0
        #ANS="22,33,44,55,66,77,88"
        indexend=ANS.find(',',indexbeg)
        peak_freq = float(ANS[indexbeg:indexend])
        self.PeakFreq=peak_freq
        #print('PeakFreq',peak_freq)
        indexbeg=indexend+1
        indexend=ANS.find(',',indexbeg)
        peak_height = float(ANS[indexbeg:indexend])
        self.Peak_Ht=peak_height
        #print('Peak Ht',peak_height)
        indexbeg=indexend+1
        indexend=ANS.find(',',indexbeg)
        secpeak_freq = float(ANS[indexbeg:indexend])
        self.SecPeakFreq=secpeak_freq
        #print('Sec Peak Freq',secpeak_freq)
        indexbeg=indexend+1
        indexend=ANS.find(',',indexbeg)
        secpeak_height = float(ANS[indexbeg:indexend])
        self.SecPeakHt=secpeak_height
        #print('Sec Peak Ht',secpeak_height)
        indexbeg=indexend+1
        indexend=ANS.find(',',indexbeg)
        side_mode = float(ANS[indexbeg:indexend])
        self.SideMode=side_mode
        #print('SMSR', SMSR)
        indexbeg=indexend+1
        indexend=ANS.find(',',indexbeg)
        SMSR = float(ANS[indexbeg:indexend])
        self.SMSR=SMSR
        #print('SMSR', SMSR)
        return (SMSR)

    def measure(self,freq=194.00):
        cmd = 'CTRF' + str(freq);
        self.write(cmd)
        cmd = 'SGL'
        self.write(cmd)
        count=1;
        while not ibrsp(self.device):
            time.sleep(1)
            if (count > 10): raise 'Timeout'
            count += 1
        cmd = 'CTR=P,SGL'
        self.write(cmd)
        count=1;
        while not ibrsp(self.device):
            time.sleep(1)
            if (count > 10): raise 'Timeout'
            count += 1
        cmd='SMSR1'
        self.write(cmd)
        cmd = 'ANA?'
        s = self.query((cmd))
        f = float(s[-9:-2])
        return(f)

# John added this 02-18-04
    def setRefLevel(self,ref):
        #Sets the reference level
        cmd = 'REFL%.1f'%(ref)
        self.write(cmd)
        return

    def setYAxisScale(self,scale):
        #Sets the Y axis scale factor
        cmd = 'LSCL%.1f'%(scale)
        self.write(cmd)
        return

    def getSpanNm(self):
        #Returns span in nm
        cmd = 'SPAN?'
        return float(self.query(cmd))

    def setSpanNm(self,span):
        #Sets span in nm
        cmd = 'SPAN%.1f'%(span)
        self.write(cmd)
        return

    def setSpanTHz(self, fltSpanTHz):
        self.write( 'SPANF%0.2f' % fltSpanTHz )

    def setSpanGHz(self, fltSpanGHz):
        self.setSpanTHz( fltSpanGHz/1000.0 )

    def getSpanTHz(self):
        return float(  self.query('SPANF?').strip() )

    def getSpanGHz(self):
        return self.getSpanTHz()* 1000.0
        

    def setResolutionNm(self,Res_Nm):
        #Sets measuring resolution in nm
        rez = Res_Nm
        if rez < 0.01:
            rez = 0.01
        if rez > 2.0:
            rez = 2.0
        cmd = 'RESLN%.2f'%(rez)
        self.write(cmd)
        return

    def setResolutionGHz(self, nResGHz):
        'input is an integer because the resolution must be 2,4,10,20,40,100,200,400'
        self.write('RESLNF%d' % nResGHz)

    def getResolutionGHz(self):
        return float(  self.query( 'RESLNF?' ).strip() )
    

    def getResolutionNm(self):
        #Returns measure resolution in nm
        cmd = 'RESLN?'
        return float(self.query(cmd))

    def setCenterNm(self,nm):
        #Sets center wavelength in nm
        cmd = 'CTRWL%f'%(nm)
        self.write(cmd)
        return

    def getCenterNm(self):
        #Returns center wavelength in nm
        cmd = 'CTRWL?'
        return float(self.query(cmd))

    def setCenterTHz(self, fltCenterTHz):
        self.write( 'CTRF%0.4f' % fltCenterTHz)

    setCenter = setCenterTHz

    def getCenterTHz(self):
        return float( self.query('CTRF?').strip() )
    
    getCenter = getCenterTHz

    def setCenterGHz(self, fltCenterGHz):
        self.setCenterTHz(fltCenterGHz/1000.0)

    def getCenterGHz(self):
        return self.getCenterTHz() * 1000.0
    
    def setCenter(self,center):
        #ibclr(self.device)
        cmd = 'CTRF '+ str(center)
        self.write(cmd)

    def setSamplingPoints(self, points):
        #Sets the sampling points
        if (points > 0 and points < 11) or points > 20001: raise 'Invalid points'
        cmd = 'SMPL%d'%(points)
        self.write(cmd)
        return

    def getSamplingPoints(self):
        return int(  self.query('SMPL?').strip() )

    def measureOSNRbyMarker(self, wave=0):
        #Measures OSNR using markers. Center wavelength in nm. 0 if not setting center wavelength
        span = 2
        res = 0.2
        points = 200

        if wave:
            #self.setRefLevel(0)
            self.setSensitivity(3)
            self.setSpanNm(span)
            self.setYAxisScale(10)
            self.setResolutionNm(res)
            self.setSamplingPoints(points)
            self.setCenterNm(wave)

        self.setSweepStatus(3)           #single scan # Auto Reference level
        cnt = 0
        while self.getSweepStatus() <> 'Stopped':    #wait for sweep to finish
            time.sleep(.2)
            if (cnt >= 20): raise 'measureOSNRbyMarker: Timeout'
            cnt += 1
        self.setSweepStatus(3)           #single scan
        cnt = 0
        while self.getSweepStatus() <> 'Stopped':    #wait for sweep to finish
            time.sleep(.2)
            if (cnt >= 20): raise 'measureOSNRbyMarker: Timeout'
            cnt += 1
        self.write('SMSR1')         #query for peak position
        s = str(self.query('ANA?'))
        ctrf = float(s[:8])
        if dbg: print 'ctrf=%f'%(ctrf)

        lmrkr = ctrf - span/3.3     #set marker frequencies
        rmrkr = ctrf + span/3.3
        if dbg: print 'lmrkr=%.2f, rmrkr=%.2f'%(lmrkr,rmrkr)

        self.write('MKCL')          #clear marker
        cmd = 'WMKR %f'%(ctrf)      #set moving marker
        self.write(cmd)
        self.write('MKR1')
        s = str(self.query('MKR1?'))
        PeakDB = float(s[-9:-2])    #fixed marker level
        if dbg: print 'PeakDB=%f'%(PeakDB)

        cmd ='WMKR %f'%(lmrkr)
        self.write(cmd);
        self.write('MKR1')
        s = str(self.query('MKR1?'))
        LeftDB = float(s[-9:-2])    #fixed marker level
        if dbg: print 'LeftDB=%f'%(LeftDB)

        cmd ='WMKR %f'%(rmrkr)
        self.write(cmd);
        self.write('MKR1')
        s = str(self.query('MKR1?'))
        RightDB = float(s[-9:-2])   #fixed marker level
        if dbg: print 'RightDB=%f'%(RightDB)
        self.setSweepStatus(2)
        ##return PeakDB - RightDB #Modified by Anand on 4/21 to resolve differences between manual and automated stations
        MidDB = (RightDB + LeftDB) / 2.0
        if dbg: print 'MidDB=%f'%MidDB
        return PeakDB - MidDB      #return OSNR
# John added this 02-18-04

    def setSensitivity(self,sensitivity):
        #ibclr(self.device)
        #Sensitivity [0=SHI1,1=SHI2,2=SHI3,3=SNHD,4=SNAT,5=SMID]
        if sensitivity == 0 : senstr = 'SHI1'
        if sensitivity == 1 : senstr = 'SHI2'
        if sensitivity == 2 : senstr = 'SHI3'
        if sensitivity == 3 : senstr = 'SNHD'
        if sensitivity == 4 : senstr = 'SNAT'
        if sensitivity == 5 : senstr = 'SMID'
        cmd = senstr
        s = self.query(cmd, delay=0.2)
#        s = str(ibrd(self.device, 200))
        return (s)

    def getSensitivity(self):
        nSens = int(self.query('SENS?').strip())
        strSens
        if nSens==0:
            strSens = 'SHI1'
        elif nSens==1:
            strSens = 'SHI2'
        elif nSens==2:
            strSens = 'SHI3'
        elif nSens==3:
            strSens = 'SNHD'
        elif nSens==4:
            strSens = 'SNAT'
        elif nSens==5:
            strSens = 'SMID'
        return nSens, strSens
            

    def getSweepStatus(self):
        #print ("Device", self.device)
        #self.device = ibdev(self.board, self.pad, 0, T1s, 1, 0)
        #print ("Device", self.device)
        #ibclr(self.device)
        cmd = 'SWEEP?'
        #ibwrt(self.device, cmd, len(cmd))
        #s = int(ibrd(self.device, 200))
        s = int(self.query(cmd, delay = 0.2))
        if (s == 0) : return ('Stopped')
        if (s == 1) : return ('Single')
        if (S == 2) : return ('Repeat')
        else        : return ('Error')

    def setSweepStatus(self, mode = 1):
        '1 = Auto, 2 = RPT, 3 = SGL, 4 = Segment, 5 = Stop'
        #ibclr(self.device)
        if mode == 1:
            cmd = 'AUTO'
        elif mode == 2 :
            cmd = 'RPT'
        elif mode == 3 :
            cmd = 'SGL'
        elif mode == 4 :
            cmd = 'SMEAS'
        elif mode == 5 :
            cmd = 'STP'
        else:
            raise "Invalid Mode"
        self.write(cmd)
        #s = str(ibrd(self.device, 200))
 
##    def getSweepStatus(self):
##        return int( self.query('SWEEP?').strip() )

    def setup(self, SPANF=0.8, REFL=-10.0, RESLNF=4.0, SENS='MID', LSCL=10.0, MODIF=5.0):
        cmd = 'SPANF%3.3f'%SPANF
        self.write(cmd)
        cmd = 'REFL'+str(REFL)+',RESLNF'+str(RESLNF)+\
                  ',S'+SENS+',LSCL'+str(LSCL)+',MODIF'+str(MODIF)
        self.write(cmd)

    def LostFunctionName(self,SMSR_Mask=0.00):#Somehow this function name got deleted.9/4/2009
        cmd = 'ACTV0,SMSR1,SSMSK'+ str(SMSR_Mask)
        self.write(cmd)
        cmd = 'ANA?'
        ANS = self.query(cmd)
        if len(ANS) == 0:
            raise 'Empty String'
        indexbeg=0
        indexend=0
        #ANS="22,33,44,55,66,77,88"
        indexend=ANS.find(',',indexbeg)
        peak_freq = float(ANS[indexbeg:indexend])
        self.PeakFreq=peak_freq
        #print('PeakFreq',peak_freq)
        indexbeg=indexend+1
        indexend=ANS.find(',',indexbeg)
        peak_height = float(ANS[indexbeg:indexend])
        self.Peak_Ht=peak_height
        #print('Peak Ht',peak_height)
        indexbeg=indexend+1
        indexend=ANS.find(',',indexbeg)
        secpeak_freq = float(ANS[indexbeg:indexend])
        self.SecPeakFreq=secpeak_freq
        #print('Sec Peak Freq',secpeak_freq)
        indexbeg=indexend+1
        indexend=ANS.find(',',indexbeg)
        secpeak_height = float(ANS[indexbeg:indexend])
        self.SecPeakHt=secpeak_height
        #print('Sec Peak Ht',secpeak_height)
        indexbeg=indexend+1
        indexend=ANS.find(',',indexbeg)
        side_mode = float(ANS[indexbeg:indexend])
        self.SideMode=side_mode
        #print('SMSR', SMSR)
        indexbeg=indexend+1
        indexend=ANS.find(',',indexbeg)
        SMSR = float(ANS[indexbeg:indexend])
        self.SMSR=SMSR
        #print('SMSR', SMSR)
        return (SMSR)
    def setPeakToRefLevel(self):
        self.write('REF=P')
    def stop(self):
        self.write('STP')
    def sweepSingle(self, blnWaitForFinish = 0, fltTimeout = 60.0):
        self.write('SGL')
        if blnWaitForFinish:
            fltTimeStart = time.time()
            while time.time() - fltTimeStart < fltTimeout:
                nStatus = self.getSweepStatus()
                if nStatus ==0:
                    break
                else:
                    time.sleep(0.5)
            else:
                raise Exception('Timeout waiting for osa to finish sweep, time = %0.2f' % time.time() - fltTimeStart)
            
    def sweepRepeat(self):
        self.write('RPT')
    def sweepAuto(self):
        self.write('AUTO')

    def setActiveTrace(self, trace = 'A'):
        'trace can be either string "a", "b","c" case insensitive or int 1,2,3'
        nTrace = ['A', 'B', 'C'].index( self.__getTraceLetter(trace) )
        self.write('ACTV%d' % nTrace)
    def getActiveTrace(self):
        nTrace = int( self.query( 'ACTV?' ).strip() )
        return nTrace, self.__getTraceLetter(nTrace)
    
        
    def getTrace(self, trace = 'A'):
        'downloads freq, power arrays.  trace can be either string "a", "b","c" case insensitive or int 1,2,3'
        strTrace = self.__getTraceLetter(trace)
        self.write('LDAT' + strTrace)
        strResp = self.__readLongReply()
        lstPower = self.__getTraceList(strResp)
        time.sleep(1.0)
        self.write('WDAT' + strTrace)
        strResp = self.__readLongReply()
        lstWL = self.__getTraceList(strResp)
        return lstWL, lstPower
        
    def __readLongReply(self):
        strReply = self.read()
        while strReply[-2:] != '\r\n':
            strReply += self.read()
        return strReply
    def __getTraceList(self, strRawReply):
        # slice off the first number. that's the array length
        return map(float, strRawReply.strip().split(','))[1:]
        
    def __getTraceLetter(self, trace):    
        tupTraces = ('A','B','C')
        if type(trace) == types.StringType:
            trace = trace.upper()
            if trace not in tupTraces:
                raise Exception('TRACE must be either "a", "b", or "c" case insensitive or int 1,2,3.  you suppled %s' % str(trace))
            else:
                return trace
        else:
            try:
                trace = int(trace)
                trace = tupTraces[trace]
                return trace
            except:
                raise Exception('TRACE must be either "a", "b", or "c" case insensitive or int 1,2,3.  you suppled %s' % str(trace))


class HP3631A(Base):
    'This is a Triple output Powersupply'
    version = 1.0
    devicedict = {}
    counter = {}
    def __init__(self, board=0, pad=2,**GPIB):
        self.Volt = -1
        Base.__init__(self, board, pad)
        self.disconnected = 0
        self.Name = ''
        #<DS>
        self.__lstOutputs = ['P6V','P25V', 'N25V']
        #</DS>

    def __repr__(self):
        s = '\nDescription: Agilent Triple Output Power Supply\n'
        s += Base.__repr__(self)
        return(s)



    def connect(self):
        Base.connect(self)

    def beep(self):
        self.write('SYST:BEEP')
    def setText(self, strText = None):
        if strText:
            self.write('DISP:TEXT "%s"' % strText)
        else:
            self.write('DISP:TEXT:CLEAR')
    def clearText(self):
        self.setText()

    def getOutputList(self):
        return self.__lstOutputs[:]     # return a copy so that the client cannot mess it up
    
    def setVoltCurr(self, selOutput = 'P6V' , volts = 0.0, current = 0.1):
        '''Selects which output of the supply with selOutput.
        Sets the voltage output, and current limit'''
        cmd = 'APPL' + ' ' + selOutput.upper() + ',' + str(volts) + ',' + str(current)
        self.write(cmd)
        #ibwrt(self.device, cmd, len(cmd))
        return

    def getVolts(self, selOutput = 'P6V'):
        cmd = 'MEAS:VOLT? '+selOutput
        self.query(cmd)
        #ibwrt(self.device, cmd, len(cmd))
        self.Volt = float(self.query(cmd,delay=.50))
        return self.Volt

    def getCurr(self,selOutput = 'P6V'):
        '''Measure the output current of selected supply'''
        cmd = 'MEAS:CURR? '+selOutput
        #ibwrt(self.device, cmd, len(cmd))
        self.Curr = float(self.query(cmd,delay=.50))
        return self.Curr
    #<DS>
    def getPowerConsumption(self, strOutput = 'P6V'):
        return abs(self.getVolts(strOutput)*self.getCurr(strOutput))
    
    #</DS>    
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
            #return "Invalid Input"
        self.write(cmd)
        if state == "NONE":
            s = self.read()
            return (int(s))
        else: return state
    def setState(self, state = 'NONE'):
        return self.setOutputState(state)



class HP86120C(Base):
    def __init__(self, board=0, pad=21, type=0):
        Base.__init__(self, board, pad, type)

    def __repr__(self):
        s = 'Description: 86120C Agilent Multiwavelength Meter\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)

    def getFrequency(self):
        cmd = 'fetc:SCAL:POW:FREQ?'
        return float(self.query(cmd, delay = 0.2))/1E12
    
    #<DS>
    def getPower(self):
        strCmd = 'FETC:SCAL:POW?'
        return float(self.query(strCmd))
    #</DS>
    
    def GetDiagnostics(self, retHeader = 0):
        if retHeader:
            return ['Frequency_86120']
        row = []
        cmd = 'fetc:SCAL:POW:FREQ?'
        return [float(self.query(cmd))/1E12]
# updated 2002-08-26 by Paul Lin
# - changed name of class


class HP86122A(Base):
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)
        self.disconnected = 0
        self.Name = ''

    def __repr__(self):
        s = 'Description: HP86122 Multi-Wavelength Meter\n'
        s += Base.__repr__(self)
        return(s)


    def connect(self):
        Base.connect(self)
        print 'connected'
        self.setFreeze()


    def turnOffAverage(self):
        'Turns off averaging'
        #self.device = ibdev(self.board, self.pad, 0, T1s, 1, 0)

        cmd = ':CALCulate2:PWAVerage OFF'
        self.write(cmd)
       # s = str(ibrd(self.device, 200))
       # return (s)


    def setAverage(self, Average):
        '''Note: This will turn on Weighted averaging. It doesnt do
        anything with the 'Average' Variable. Its just there for
        compatability with Burleigh'''
        
        cmd = ':CALCulate2:PWAVerage ON'
        self.write(cmd)
        #s = str(ibrd(self.device, 200))
        #return (s)

    def setFreeze(self):
        '''set non continuous mode'''
        
        cmd = ':INITiate:CONTinuous OFF'
        self.write(cmd)
        #s = str(ibrd(self.device, 200))
        #return (s)
    def getFrequency(self,RES = None):
        '''returns frequency in Thz.
        Choose from one of the following Resolutions
        1) MINimum      = 0.001
        2) EXTended1    = 0.0001
        3) DEFault      = Current
        4) MAXimum      = 0.01'''

        cmd = ':MEAS:SCAL:POW:FREQ?'
        if RES:
            if type(RES) == types.StringType:
                cmd += str(RES)
            else:
                raise exceptions.TypeError, "Expecting Sting type. Use Module doc for more help"
        strResp = self.query(cmd)
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
        if RES:
            if type(RES) == types.StringType:
                cmd += str(RES)
            else:
                raise exceptions.TypeError, "Expecting Sting type. Use Module doc for more help"
        strResp = self.query(cmd)
        if (strResp.find('LO') != -1) :
            return (-1.0)
        return float(strResp)
        



class Agilent8163B(Base):
    #Agilent Lightwave Multimeter
    version = 1.1

    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)
        self.Name = ''
        self._conf = {}
        self._ActiveConf = None

    def __repr__(self):
        s = '\nDescription: Lightwave Multimeter \n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)
        #chassis = None, slot = None, head = None
    def SetActiveConf(self, Name = None, slot = None, head = None  ):
        #Set active configuration. Name=config name, slot=slot #, device=channel #
        if Name == None:
            Name = "%d:%d"%(slot,head)
        if not self._conf.has_key(Name):
            if slot == None or head == None:
                raise InstrumentException,'The Slot and device parameters cannot be empty'
            self._conf[Name] = [slot,head]
        self._ActiveConf = Name

    #<DS>
    def getName(self):
        return self._ActiveConf
    def getSlot(self):
        return self._conf[self._ActiveConf][0]
    def getHead(self):
        return self._conf[self._ActiveConf][1]
    #</DS>

    def getPower(self, queryDelay = 0.05):
        #Reads the power from active head
        cmd = 'READ%d:CHAN%d:POW?'%(self._conf[self._ActiveConf][0],self._conf[self._ActiveConf][1])
        return float(self.query(cmd, delay = queryDelay))


    def getDisplayedPower(self, queryDelay = 0.002):
        #getPower() will not work for the subordinate module, so we need to read the display with FETCH
        cmd = 'FETC%d:CHAN%d:POW?'%(self._conf[self._ActiveConf][0],self._conf[self._ActiveConf][1])
        reply = self.query(cmd, delay=queryDelay)
        try:
            ret = float(reply)
        except:
            ret = -80

        return ret

    
    
    def setWavelength(self, lambdaNM = 1556.5):
        #Sets the wavelength in nm. Default = 1556.5nm
        cmd = 'SENS%d:CHAN%d:POW:WAV %.2fnm'%(self._conf[self._ActiveConf][0],self._conf[self._ActiveConf][1],lambdaNM)
        self.write(cmd)
        return

    def getWavelength(self):
        #reads the wavelength in nm
        cmd = 'SENS%d:CHAN%d:POW:WAV?'%(self._conf[self._ActiveConf][0],self._conf[self._ActiveConf][1])
        return float(self.query(cmd)) * 1.00E+9

    def setFrequency(self, freqTHz = 194.0):
        #Convert freq in THz into nm and call setWavelength
        self.setWavelength(299792458.00/(freqTHz * 1.00E+3))
        return

    def getFrequency(self, slot = 1, channel = 1):
        #Call getWavelength and convert nm to THz
        return 299792458.00/(self.getWavelength() * 1.00E+3)

    def setPowerUnit(self, unit = 0):
        #Sets the unit of the power meter. 0 = dBm, 1 = Watt
        cmd = 'SENS%d:CHAN%d:POW:UNIT %d'%(self._conf[self._ActiveConf][0],self._conf[self._ActiveConf][1],unit)
        self.write(cmd)
        return
    def getPowerUnit(self):
        strCmd = 'SENS%d:CHAN%d:POW:UNIT?' % (self.getSlot(), self.getHead())
        return int( self.query(strCmd) )
    def setCalibrationConst(self,const=0):
        #cmd = 'SENS%d:corr %f'%(self._conf[self._ActiveConf][0],const)
        #cmd = 'SENS%d:corr %f'%(self._conf[self._ActiveConf][0],const)
        #print 'const =', const
        #print 'slot = %d, head = %d' % (self.getSlot(), self.getHead())
        cmd = 'SENS%d:CHAN%d:CORR %f%s' % (self.getSlot(),self.getHead(), const,'DB')
        #</DS>
        self.write(cmd)
    def getCalibrationConst(self):
        #<DS>
        #reply is in dB
        #cmd = 'SENS%d:corr?'%(self._conf[self._ActiveConf][0])
        cmd = 'SENS%d:CHAN%d:CORR?'%(self._conf[self._ActiveConf][0],self._conf[self._ActiveConf][1])
        #</DS>
        return float(self.query(cmd))

    #<DS>
    def triggerReadPower(self, fltQueryDelay = 0.05):
        #trigger must be done on the main channel, number 1.  It will also affect subordinate channel.
        #this is why the trigger is hard coded to be channel 1.
        self.write( ':INIT%d:CHAN1:TRIG:IMM' % self.getSlot())
        strCmd = 'FETC%d:CHAN%d:POW?'%(self.getSlot(),self.getHead())
        return float(self.query(strCmd, delay = fltQueryDelay))
        
    #</DS>    

    def setAvgTime(self,secs):
        cmd = 'SENS%d:CHAN%d:POW:ATIM %f'%(self._conf[self._ActiveConf][0],self._conf[self._ActiveConf][1],secs)
        self.write(cmd)

    def GetDiagnostics(self, retHeader = 0):
        if retHeader:
            self._powermeters = copy.deepcopy(self._conf)
            Header = []
            for i in self._powermeters:
                Header.append('%s_PM'%(i))
            return Header
        row = []
        for a in self._powermeters:
            if dbg: print a,'FETC%d:CHAN%d:POW?'%(self._conf[a][0],self._conf[a][1]),
            reply = self.query('FETC%d:CHAN%d:POW?'%(self._conf[a][0],self._conf[a][1]))
            if dbg: print reply
            if  reply.find('--') >= 0:
                row.append(DUMMY)
            else:
                row.append(float (reply ))
        if dbg: print row
        return row

class MAP(Base):
    '''This is a MAP SW OPTICAL SWITCH CASSETTE'''
    version = 1.0
    devicedict = {}
    counter = {}
    def __init__(self, board=0, pad=2,**GPIB):
        self.key = "%02d-%02d" %(board,pad)
        try :
            self.__class__.devicedict[self.key]
            self.__class__.counter[self.key] += 1
        except:
            self.__class__.devicedict.update({self.key:-1})
            self.__class__.counter.update({self.key:1})
        Base.__init__(self, board, pad)
        self.disconnected = 0
        self.Name = ''

    def __repr__(self):
        s = 'Description: HMAP SW OPTICAL SWITCH CASSETTE\n'
        s += Base.__repr__(self)
        return(s)

    def setRoute(self,chassis,slot,device,input,output):
        'set optical switch path'
        cmd = ':ROUT:CLOS '+"%d,%d,%d,%d,%d" %(chassis,slot,device,input,output)
        self.write(cmd)
        return

    def getRoute(self,chassis,slot,device,input):
        'get optical switch path'
        cmd = ':ROUT:CLOS? '+"%d,%d,%d,%d" %(chassis,slot,device,input)
        string = self.query(cmd)
        return int(string)

class AndoAQ8291(Base):
    '''Ando Mainframe with Switches AQ8101A'''
    version = 1.0
    devicedict = {}
    counter = {}
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)
        self.Name = ''

    def __repr__(self):
        s = 'Description: Ando SW OPTICAL SWITCH CASSETTE\n'
        s += Base.__repr__(self)
        return(s)

    def setRoute(self,slot,device,input,output):
        'set optical switch path'
        #cmd = ':ROUT:CLOS '+"%d,%d,%d,%d,%d" %(chassis,slot,device,input,output)
        cmd = 'C%02d,D%d,SA%dSB%d' %(slot,device,input,output)
        self.write(cmd)
        return

    def getRoute(self,chassis,slot,device,input):
        'get optical switch path'
        cmd = 'SASB?'
        resp = self.query(cmd)
        return resp




class HP8156A(Base):
    'Optical Attenuator'
    version = 1.0
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)

    def __repr__(self):
        s = 'Description: HP8156A Optical Attenuator\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)

    def setOutputState(self, state = 'NONE'):
        'This command enables the optical output when state = ON, and disables the optical output when state = OFF'
        if type(state) == types.IntType or type(state) == types.FloatType:
            state = ['ON','OFF'][int(state)]
            
        #<DS> cannot perform state.upper() if state == None
        if state:
            state = state.upper()
        #</DS>
        
        if state == "NONE":
            cmd = 'OUTP:STAT?'
        elif state == "ON":
            cmd = 'OUTP:STAT ON'
        elif state == "OFF":
            cmd = 'OUTP:STAT OFF'
        else:
            raise 'Invalid Input'
            #return "Invalid Input"
        self.write(cmd)
        if state == "NONE":
            s = str(self.read())
            return (int(s))
        else: return state

    def setAttenuationMode(self):
        'Sets the instrument to attenuation mode.'
        cmd = 'OUTP:APM:OFF'
        self.write(cmd)

    def setFrequency(self, freqTHz = 193.5):
        'Sets the optical frequency of the attenuator with the argument freqTHz in TeraHertz '
        nm = ((299792458.00)/(freqTHz * 1.00E+12))*1.00E+9
        cmd = 'INP:WAV'+ ' '+ str(nm) + 'nm'
        self.write(cmd)
        return

    def setAttenuation(self, attdB = 25.0):
        'Sets the optical attenuation value with the attdB argument in Decibels '
        cmd = 'INP:ATT %.3f'%attdB
        self.write(cmd)
        return

    #<DS>
    def setAttenuationOffset(self, fltOffset):
        strCmd = ':INP:OFFS %0.2f' % fltOffset
        self.write(strCmd)
    def getAttenuationOffset(self):
        return float( self.query(':INP:OFFS?'))
    #</DS>    
    
    def setWavelength(self,wavlen):
        strwavlen = str(wavlen)
        self.write(":INP:WAVE %.1lfnm"%(float(strwavlen)))

    def getAttenuation(self):
        return float(self.query(":INP:ATT?"))

    def GetDiagnostics(self, retHeader = 0):
        if retHeader:
            Header = []
            for i in self._Name:
                Header.extend(['%s_Attn'%(i),'%s_STATE'%(i)])
                break # there is only one attenuator
            return Header
        row = []
        for a in [0]:
            row.append(float ( self.query(  ":INP:ATT?"   ) ) )
            #row.append(float ( self.query(  ":OUTP:POW? %s"%(self._conf[a])   ) ) )
            row.append(float ( self.query('OUTP:STAT?') ) )
        return row
    def SetActiveConf(self, Name = None,chassis = 1, slot = None, head = None  ):
        self._Name = Name


class Agilent34970A(Base):
    'Data Aquisition/Switch Unit'
    version = 1.0
    def __init__(self, board=0, pad=2):
        self.Volt = -1
        Base.__init__(self, board, pad)

    def __repr__(self):
        s = '\nDescription: Agilent Data Aquistion Switch\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)

    def getVoltage(self, slot = 102):
        'Measure voltage on the channel number specified by the string channel, and int slot'
        cmd = 'MEAS:VOLT:DC?'+ ' ' + '(' + '@' + str(slot) + ')'
        self.Volts = float(self.query(cmd))
        return self.Volts

    def setCloseSwitch(self, chanList = '201'):
        '''Closes the specified switch postion in slot 2 or 3 '''
        slotLimit = 200
        chanList = str(chanList)
        #if slot < slotLimit:
         #   raise Exception,'Channel: %d does not have this function ' %slot
        cmd = 'ROUTE:CLOSE' + ' ' + '(@' + chanList.upper() + ')'
        self.write(cmd)
        return

    def setOpenSwitch(self, chanList = '201'):
        '''Closes the specified switch postion in slot 2 or 3 '''
        slotLimit = 200
        chanList = str(chanList)
        #if slot < slotLimit:
          #  raise Exception,'Channel: %d does not have this function ' %slot
        cmd = 'ROUTE:OPEN' + ' ' + '(@' + chanList.upper() + ')'
        self.write(cmd)
        return
    def setSwitchState(self, chanList = '201', blnState = 0):
        if blnState:
            self.setCloseSwitch(chanList)
        else:
            self.setOpenSwitch(chanList)
            
    def getSwitchState(self, nChannel):
        strCmd = 'ROUTE:CLOSE? (@' + str(nChannel) + ')'
        strResp = self.query(strCmd)
        # replies '0\n' for open, '1\n' for closed 
        strResp = strResp.strip()
        return int(strResp)
    
    def open(self, channel):
        if types.ListType != type(channel):
            channel = [channel]

        #ibclr(self.__class__.devicedict[self.key])
        cmd = ""
        for x in channel: cmd += str(x)+', '
        # strip the last two string chars
        #ROUT:CLOS (@  2,  3)
        cmd = cmd[:len(cmd)-2]
        cmd = 'ROUT:OPEN (@ '+ cmd + ')'
        if printcmd : print(cmd)
        self.write(cmd)

    def close(self,channel):
        if types.ListType != type(channel):
            channel = [channel]

        #ibclr(self.__class__.devicedict[self.key])
        cmd = ""
        for x in channel: cmd += str(x)+', '
        # strip the last two string chars
        #ROUT:CLOS (@  2,  3)
        cmd = cmd[:len(cmd)-2]
        cmd = 'ROUT:CLOS (@ '+ cmd + ')'
        if printcmd : print(cmd)
        self.write(cmd)

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
        if printcmd : print(cmd)
        self.write(cmd)

    #Added by Neeraja on Jul 19 2010
    #The default (DEF) transducer type is a J-Type thermocouple
    #MEASure:TEMPerature?TCouple,{B|E|J|K|N|R|S|T|DEF}[,1[,<resolution>|MIN|MAX|DEF}]] ,(@<scan_list>)
    #Purpose: Configure the specified channels for thermocouple measurements and
    #         immediately sweep through the scan list one time
    def getTemperature(self,channel):
        if types.ListType != type(channel):
            channel = [channel]
        #ibclr(self.__class__.devicedict[self.key])
        cmd = ""
        for x in channel: cmd += str(x)+', '
        # strip the last two string chars
        cmd = cmd[:len(cmd)-2]
        cmd = 'MEASure:TEMPerature? DEF,DEF,DEF, (@ '+ cmd + ')'
        if printcmd : print(cmd)
        self.write(cmd)     


class Agilent86060C(Base):
    'LightWave Switch'
    version = 1.0

    def __init__(self, board=0, pad=2):
        self.Volt = -1
        Base.__init__(self, board, pad)

    def __repr__(self):
        s = '\nDescription: Agilent Lightwave Switch\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)

    def setRouteChannel(self, inChannel = 'A1', outChannel = 'B1'):
        'Routes the input optical channel(inChannel) to the output optical channel (outChannel)'
        #<DS>
        if outChannel == 'OFF':
            return self.turnChannelOff()
        #</DS>
        
        cmd = 'ROUTE:LAYER1:CHANNEL'+ ' '+ inChannel.upper() + ',' + outChannel.upper()
        self.write(cmd)
        '''cmd = 'WAI*'
        ibwrt(self.device, cmd, len(cmd)) #sends a wait for channel to settle command
        cmd = 'SYSTEM CONFIG?' #polls to see if the channel has settled
        ibwrt(self.device, cmd, len(cmd))
        string = ibrd(self.device, 200)
        return string'''
        return

    def turnChannelOff(self):
        cmd = 'ROUTE:LAYER1:CHANNEL BOFF'
        self.write(cmd)
        return




class AssciateOven(Base):
    'Mux'
    version = 1.0
    devicedict = {}
    counter = {}
    def __init__(self, board=0, pad=2,**GPIB):
        Base.__init__(self, board, pad)
        self.Name = ''

    def __repr__(self):
        s = 'Description: AssciateOven\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)

    def getCaseTemp(self):
        cmd = 'R? 108,1'
        reply = self.query(cmd)
        if printcmd : print(cmd)
        return float(reply)/10.0

    def getOvenSetPoint(self):
        cmd = 'R? 300,1'
        reply = self.query(cmd)
        if printcmd : print(cmd)
        return float(reply)/10.0

    def getOvenTemp(self):
        cmd = "R? 100,1"
        reply = self.query(cmd)
        if printcmd : print(cmd)
        return float(reply)/10.0

    def setOvenTemp(self,temp):
        cmd = "W 300," + str(temp*10)
        if printcmd : print(cmd)
        reply = self.write(cmd)

    def stabilizeOvenTemp(self,setpoint,err = 0.2,timeout = 3600, sleep = 1):
        sttm = time.time()
        temperature = self.getCaseTemp()
        while abs(temperature - setpoint) > err and( time.time()- sttm) < timeout:
            temperature = self.getCaseTemp()
            if dbg >= 2: print temperature,
            time.sleep(sleep)
        if abs(temperature - setpoint) > 1:
            raise ApplicationDriverTimeout,"Oven Not Working..."
        return temperature

    def setHighRes(self):
        return
        self.write("W 606,1")
        self.write("W 616,1")
        self.write("W 626,1")
        pass

#added functions below  so that Associate Oven will work with NPI Test station code
##    def __init__(self, board=2, pad=15):
##        ##print board
##        ##print pad
##        ##print DYNVAR.Oven
##        Base.__init__(self, board, pad)
        

##    def __repr__(self):
##        s = 'Thermotron Environmental Oven\n'
##        s += Base.__repr__(self)
##        return(s)

##    def connect(self):
##        Base.connect(self)

    def RunManual(self):
##        strCmd = 'RUNM'
##        self.write(strCmd)
        pass
        
    def StopManual(self):
##        strCmd = 'STOP'
##        self.write(strCmd)
        pass
    
    def getSetPointn(self, Channel = 1):
##        strCmd = ('SETP' + str(Channel) +'?' )
##        SP=float(self.query(strCmd))
##        time.sleep(1)
##        strCmd = ('SETP' + str(Channel) +'?' )
##        ##print strCmd
##        #need to read twice since instrument returns junk the first time
##        return float(self.query(strCmd))
        cmd = 'R? 300,1'
        reply = self.query(cmd)
        if printcmd : print(cmd)
        return float(reply)/10.0

    def setSetPointn(self, Channel = 1, SP=25):
##        strCmd = ('SETP' + str(Channel) + ',' + str(SP) )
##        self.write(strCmd)
        #cmd = "W 300," + str(temp*10)
        cmd = "W 300," + str(SP*10)
        if printcmd : print(cmd)
        reply = self.write(cmd)

    def setSetPointnBySeq(self, Channel = 1,SequenceParms=['testname',25,100,'version']):
        ##This method determines the oven setpoin from the sequence name.  the name must follow the format Name_Temp_Volt__Versioninfo
##dvtber_25_100__v01
##        strCmd = ('SETP' + str(Channel) + ',' + SequenceParms[1])
##        self.write(strCmd)
        cmd = "W 300," + str(SequenceParms[1]*10)
        if printcmd : print(cmd)
        reply = self.write(cmd)
        
##    def getProcessVarn(self, Channel = 1):
##        strCmd = ('PVAR' + str(Channel) +'?' )
##        return float(self.query(strCmd))

    def getOvenStatus(self, MonitorChannel = 1, SPChannel=1,SP=25):
        dblSP=SP
        #dblPV=self.getProcessVarn(MonitorChannel)
        dblPV=self.getCaseTemp()
        intTime=0
        dblDeltaT=abs(dblSP-dblPV)
        while intTime<=300 and dblDeltaT>0.3:
            dblDeltaT=abs(dblSP-dblPV)
            time.sleep(1)
            intTime=intTime+1
            #dblPV=self.getProcessVarn(MonitorChannel)
            dblPV=self.getCaseTemp()
            print dblSP,dblPV
            ##self.__updateStatus( 'Oven SP ='+ dblSP + 'Oven T=' + dblPV)
            time.sleep(1)
            
        if dblDeltaT<=0.3:
            return 1
        else:
            return 0





class TDS8000(Base):
    'This is a Wavelength meter'
    version = 1.00
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)
        self.Name = ''

    def __repr__(self):
        s = 'TDS 8000  TEK Scope\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)

    def Clear(self):
        self.write(":ACQUIRE:DATA:CLEAR")
    def Measure(self):
        self.query(":MEASU:MEAS1:VAL?")


# this class was being redefined later in the file, not sure why.
class AgilentE4400B(Base):
    'This is a Signal Generator'
    version = 1.00
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)
        self.Name = ''

    def __repr__(self):
        s = 'Agilent Signal Generator\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)

    def SetFreq(self,wavl,crystaldiv = 16):
        self.write("FREQ:FIX %f MHz"%(float(wavl)/crystaldiv))

    def SetSonetFreq16(self,index):
        'SONET (9.9 G),10GBE (10.3 G),SONET_FEC (10.7 G),11.1 G)'
        index = int(index)
        combinations = [622.08,644.5313,669.3265,693.4830]
        print index,"Sonet Freq:",combinations,combinations[index]
        self.write("FREQ:FIX %f MHz"%(combinations[index]))

    def SetState(self,state=0):
        '''[OFF,ON]'''
        comb = ['OFF','ON']
        self.write(":OUTP:STAT "+comb[state])

    def SetModulationState(self,state = 0):
        '''[OFF,ON]'''
        comb = ['OFF','ON']
        self.write(":OUTP:MOD:STAT "+comb[state])

    def GetDiagnostics(self,retHeader=0):
        if retHeader:
            Header = ['Frequency','RF Output']
            return Header
        freq =(float(self.query(":FREQ:FIX?"))*1E-6)
        state = (float(self.query(":OUTP:STAT?")))
        return [freq,state]

    def setOutputState(self, state = 'NONE'):
        'This command enables the RF output when state = ON, and disables the RF output when state = OFF'
        state = state.upper()
        if state == "NONE":
            cmd = 'OUTP:STAT?'
        elif state == "ON":
            cmd = 'OUTP:STAT ON'
        elif state == "OFF":
            cmd = 'OUTP:STAT OFF'
        else:
            raise 'Invalid Input'
            #return "Invalid Input"
        self.write(cmd)
        if state == "NONE":
            s = str(self.read())
            return (int(s))
        else: return state
        
    def setPowerUnit(self, unit = 'DBM'):
        strCmd = ':UNIT:POW ' + unit
        self.write(strCmd)
        
    def setOutputPower(self, fltPower):
        strCmd = ':POW:LEV:IMM:AMPL %f' % fltPower
        self.write(strCmd)

class BERT_ED(Base):
    'This is a Bitalyzer'
    version = 1.00
    def __init__(self, board="10.243.60.17", pad=23):
        Base.__init__(self, board, pad,2)# type 2 --> TCP/IP
        self.Name = ''
        self.__blnHaveControl = 0

    def __repr__(self):
        s = 'Description: Bitalyzer\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)

    def SetManualMode(self):
        self.query("DET AUTORESYNC OFF 10000\n")
        self.query("DET DATATYPE PN31 FALSE\n")
        self.query("DET BER_WINDOWED OFF\n")

    def Resync(self,UntilBer=0,MaxRetry =5,wait = 1):
        #self.query("DET SYNC_RESET\n")
##        self.query("DET BER_RESET\n")
##        time.sleep(.5)
        self.query("DET SINGLE_RESYNC\n")
        time.sleep(1)
        self.query("DET BER_RESET\n")
        time.sleep(.5)
        if UntilBer:
            cntr = 0
            while cntr < MaxRetry:
                time.sleep(wait)
                BER = self.GetBer()
                if BER['BER'] != -1:
                    return BER
                self.query("DET SINGLE_RESYNC\n")
                time.sleep(1)
                self.query("DET BER_RESET\n")
                cntr += 1


    def DetectSync(self,DT="PN-31"):
        reply = self.query("DET SYNC?\n")
        reply = reply.strip().upper()
        return (reply.find(DT)!= -1)

    # <DS RequestNumber="10">
    # add a failure loop.  replysec[5] sometimes returns "UNAVAILABLE",
    # which raises an exception when converted to a float.
    def GetBer(self):
        reply = self.query("DET BER?\n", delay = 0.10)
        if verbose:print reply
        if reply.find('---') != -1:
            return {'Total Bits':-1,'Errors':-1,'BER':-1,'RESYNCS': -1}
        replysec = reply.split(' ')
        if replysec[5].find('UNAVAILABLE') != -1:
            #print 'BER unavailable.  device reply =', reply
            return {'Total Bits':-1,'Errors':-1,'BER':-1,'RESYNCS': -1}

        ret = {}
        ret['Total Bits'] = long(replysec[3].replace(',',''))
        ret['Errors'] = long(replysec[4].replace(',',''))
        ret['BER'] = float(replysec[5].replace(',',''))
        ret['RESYNCS'] = int(replysec[-2].replace(',',''))
        return ret
    def GetControl(self):
        self.query("REMOTE START\n")
        self.__blnHaveControl = 1
        
    def ReleaseControl(self):
        if self.__blnHaveControl:
            self.query("REMOTE STOP\n")
            self.__blnHaveControl = 0
            
    def GetDiagnostics(self, retHeader = 0):
        if retHeader:
            Header = ['ED_ClockFreq','ED_Sync']
            return Header
        freqstr = self.query("DET FREQ?\n")
        newstr = freqstr.split('FREQ')[1]
        newstr = newstr.strip()
        indx = 0
        for char in newstr:
            if(char.isalpha()):
                break
            else:
                indx +=1

        freq =float(newstr[:indx])
        sync = float(self.DetectSync())
        return [freq,sync]

class BERT_EDB(Base):
    'This is a Bitalyzer'
    version = 1.00
    def __init__(self, board="10.243.60.17", pad=23):
        Base.__init__(self, board, pad,2)# type 2 --> TCP/IP
        self.Name = ''
        self.__blnHaveControl = 0

    def __repr__(self):
        s = 'Description: Bitalyzer\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)

    def SetManualMode(self):
        self.query("DET AUTORESYNC OFF 10000\n")
        self.query("DET DATATYPE PN31 FALSE\n")
        self.query("DET BER_WINDOWED OFF\n")

    def Resync(self,UntilBer=0,MaxRetry =5,wait = 1):
        #self.query("DET SYNC_RESET\n")
##        self.query("DET BER_RESET\n")
##        time.sleep(.5)
        self.query("DET SINGLE_RESYNC\n")
        time.sleep(1)
        self.query("DET BER_RESET\n")
        time.sleep(.5)
        if UntilBer:
            cntr = 0
            while cntr < MaxRetry:
                time.sleep(wait)
                BER = self.GetBer()
                if BER['BER'] != -1:
                    return BER
                self.query("DET SINGLE_RESYNC\n")
                time.sleep(1)
                self.query("DET BER_RESET\n")
                cntr += 1


    def DetectSync(self,DT="PN-31"):
        reply = self.query("DET SYNC?\n")
        reply = reply.strip().upper()
        return (reply.find(DT)!= -1)

    # <DS RequestNumber="10">
    # add a failure loop.  replysec[5] sometimes returns "UNAVAILABLE",
    # which raises an exception when converted to a float.
    def GetBer(self):
        strReply = self.query("DET BER?\n", delay = 0.10)
        if verbose:print reply
        if strReply.find('---') != -1:
            return {'Total Bits':-1,'Errors':-1,'BER':-1,'RESYNCS': -1}
        lstReply = filter(len, strReply.split(' '))
        if 'UNAVAILABLE'in lstReply:
            #print 'BER unavailable.  device reply =', reply
            return {'Total Bits':-1,'Errors':-1,'BER':-1,'RESYNCS': -1}

        ret = {}
        ret['Total Bits'] = long(lstReply[3].replace(',',''))
        ret['Errors'] = long(lstReply[4].replace(',',''))
        ret['BER'] = float(lstReply[5].replace(',',''))
        ret['RESYNCS'] = int(lstReply[6].replace(',',''))
        return ret
    def GetControl(self):
        self.query("REMOTE START\n")
        self.__blnHaveControl = 1
        
    def ReleaseControl(self):
        if self.__blnHaveControl:
            self.query("REMOTE STOP\n")
            self.__blnHaveControl = 0
            
    def GetDiagnostics(self, retHeader = 0):
        if retHeader:
            Header = ['ED_ClockFreq','ED_Sync']
            return Header
        freqstr = self.query("DET FREQ?\n")
        newstr = freqstr.split('FREQ')[1]
        newstr = newstr.strip()
        indx = 0
        for char in newstr:
            if(char.isalpha()):
                break
            else:
                indx +=1

        freq =float(newstr[:indx])
        sync = float(self.DetectSync())
        return [freq,sync]

    
class BERT_PG(Base):
    'This is a Bitalyzer'
    version = 1.00
    def __init__(self, board="10.243.60.16", pad=23):
        Base.__init__(self, board, pad,2)# type 2 --> TCP/IP
        self.Name = ''
        self.__blnHaveControl = 0

    def __repr__(self):
        s = 'Description: Pattern Generator\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)

    def SetDatatype(self,Pattern = 4,InvertData = 1):
        '''["PN7","PN15","PN20","PN23","PN31","USER","TRIGGER"]'''
        patterns = ["PN7","PN15","PN20","PN23","PN31","USER","TRIGGER"]
        self.query("GEN DATATYPE %s %s\n"%(patterns[Pattern],["TRUE","FALSE"][InvertData]))

    def GetDiagnostics(self, retHeader = 0):
        if retHeader:
            Header = ['PG_ClockFreq']
            return Header
        reply = self.query("GEN FREQ?\n")
        spl = reply.split(' ')
        freq =(float(spl[3]))
        return [freq]


    def GetControl(self):
        self.query("REMOTE START\n")
        self.__blnHaveControl = 1

    def ReleaseControl(self):
        if self.__blnHaveControl:
            self.query("REMOTE STOP\n")
            self.__blnHaveControl = 0
            
class BurleighWA1100(Base):
    'This is a Wavelength meter'
    version = 1.00
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)

    def __repr__(self):
        s = 'Description: Burleigh 1100 Wave meter\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)


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

    def get_Frequency(self):
        cmd = ':FETC:FREQ?'
        ##cmd = ':FETC:SCAL:FREQ?'
        string = self.query(cmd)
        if (string.find('LO') != -1) :
            return (-1.0)
        s=float(string)
        s/=1000
        return (s)

    getFrequency = get_Frequency    

    def get_Power(self):
        cmd = ':FETC:POW?'
        return (float(self.query(cmd)))

    def reset_measurement(self):
        cmd=':CALC:RES'
        self.write(cmd)

class BurleighWA7100(Base):
    'This is a Wavelength meter'
    version = 1.00
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)

    def __repr__(self):
        s = 'Description: Burleigh 7100 Wave meter\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)


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

    def get_Frequency(self):
        cmd = ':FETC:SCAL:FREQ?'
        string = self.query(cmd)
        if (string.find('LO') != -1) :
            return (-1.0)
        s=float(string)
        s/=1000
        return (s)

    getFrequency = get_Frequency    

    def get_Power(self):
        cmd = ':FETC:POW?'
        return (float(self.query(cmd)))

    def reset_measurement(self):
        cmd=':CALC:RES'
        self.write(cmd)

class JDSUEDFA(Base):
    '''This is an Optical Amplifier.
    Author : john.chih@intel.com'''
    version = 1.00
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)
        self.Name = ''
        self._conf = {}
        self.ActiveConf = None

    def __repr__(self):
        s = 'JDSU Optical Amplifier\n'
        s += Base.__repr__(self)
        return (s)

    def SetActiveConf(self, Name = None, chassis = 1, slot = None, head = None):
        if Name == None:
            Name = "%d:%d:%d"%(chassis,slot,head)
        if not self._conf.has_key(Name):
            if chassis == None or slot == None or head == None:
                raise InstrumentException, 'The slot, chassis, head parameters cannot be empty'
            self._conf[Name] = "%d,%d,%d"%(chassis,slot,head)
        self._ActiveConf = Name

    def connect(self):
        Base.connect(self)

    def SetOutputCurrent(self,pow=50):
        #set output current in percent of max
        self.write(":SOUR:CURR:OUTP %s,%.1f"%(self._conf[self._ActiveConf],float(pow)))

    def GetOutputCurrent(self,pow=50):
        #query output current in percent of max
        return float(self.query(":SOUR:CURR:OUTP? %s"%(self._conf[self._ActiveConf])))

    def GetPower(self):
        #query output power
        #print ":FETC:POW:OUTP? %s"%(self._conf[self._ActiveConf])
        return float(self.query(":FETC:POW:OUTP? %s"%(self._conf[self._ActiveConf])))

    def setOutputState(self,state=0):
        #laser active, laser inactive
        self.write(":SOUR:STAT %s,%d"%(self._conf[self._ActiveConf],state))

    def GetOutputState(self):
        #query laser state
        return int(self.query(":SOUR:STAT? %s"%(self._conf[self._ActiveConf])))

    def GetDiagnostics(self, retHeader = 0):
        if retHeader:
            self._attenuators = copy.deepcopy(self._conf)
            Header = ['Set Current','STATE','Output Power'] * len(self._attenuators)
            return Header
        row = []
        for a in self._attenuators:
            row.append(float ( self.query(  ":SOUR:CURR:OUTP? %s"%(self._conf[a])   ) ) )
            row.append(float ( self.query(  ":SOUR:STAT? %s"%(self._conf[a])   ) ) )
            row.append(float ( self.query(  ":FETC:POW:OUTP? %s"%(self._conf[a])   ) ) )
        return row

class JDSUBBS(Base):
    '''This is a broadband source.
    Author : john.chih@intel.com'''
    version = 1.00
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)
        self.Name = ''
        self._conf = {}
        self.ActiveConf = None

    def __repr__(self):
        s = 'JDSU Broadband Source\n'
        s += Base.__repr__(self)
        return (s)

    def SetActiveConf(self, Name = None, chassis = 1, slot = None, head = None):
        if Name == None:
            Name = "%d:%d:%d"%(chassis,slot,head)
        if not self._conf.has_key(Name):
            if chassis == None or slot == None or head == None:
                raise InstrumentException, 'The slot, chassis, head parameters cannot be empty'
            self._conf[Name] = "%d,%d,%d"%(chassis,slot,head)
        self._ActiveConf = Name

    def connect(self):
        Base.connect(self)

    def setOutputState(self,state=0):
        #laser active, laser inactive
        self.write(":SOUR:STAT %s,%d"%(self._conf[self._ActiveConf],state))

    def GetOutputState(self):
        #query laser state
        return int(self.query(":SOUR:STAT? %s"%(self._conf[self._ActiveConf])))

    def GetDiagnostics(self, retHeader = 0):
        if retHeader:
            self._bbs = copy.deepcopy(self._conf)
            Header = ['STATE'] * len(self._bbs)
            return Header
        row = []
        for a in self._bbs:
            row.append(float ( self.query( ":SOUR:STAT? %s"%(self._conf[a]) ) ) )
        return row

class JDSUTB3TF(Base):
    '''This is a TB3 Tunable Grating Filter on MAP
    Author : john.chih@intel.com'''
    version = 1.00
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)
        self.Name = ''
        self._conf = {}
        self.ActiveConf = None

    def __repr__(self):
        s = 'JDSU TB3 Tunable Grating Filter\n'
        s += Base.__repr__(self)
        return (s)

    def SetActiveConf(self, Name = None, chassis = 1, slot = None, head = None):
        if Name == None:
            Name = "%d:%d:%d"%(chassis,slot,head)
        if not self._conf.has_key(Name):
            if chassis == None or slot == None or head == None:
                raise InstrumentException, 'The slot, chassis, head parameters cannot be empty'
            self._conf[Name] = "%d,%d,%d"%(chassis,slot,head)
        self._ActiveConf = Name

    def connect(self):
        Base.connect(self)

    def setWavelength(self,wavl):
        #set filter wavelength
        self.write(":FILT:WAV %s,%.3f"%(self._conf[self._ActiveConf],float(wavl)))

    def getWavelength(self):
        #query filter wavelength
        return float(self.query(":FILT:WAV? %s"%(self._conf[self._ActiveConf])))


    def GetDiagnostics(self, retHeader = 0):
        if retHeader:
            self._attenuators = copy.deepcopy(self._conf)
            Header = ['Wavelength'] * len(self._attenuators)
            return Header
        row = []
        for a in self._attenuators:
            row.append(float ( self.query(  ":FILT:WAV? %s"%(self._conf[a])   ) ) )
        return row

class JDSUAttn(Base):
    '''This is a Optical Attenuator.
    Author : anand.s.ramalingam@intel.com'''
    version = 1.00
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)
        self.Name = ''
        self._conf = {}
        self._ActiveConf = None

    def __repr__(self):
        s = 'JDSU Optical Attenuator\n'
        s += Base.__repr__(self)
        return(s)

    def SetActiveConf(self, Name = None,chassis = 1, slot = None, head = None  ):
        if Name == None:
            Name = "%d:%d:%d"%(chassis,slot,head)
        if not self._conf.has_key(Name):
            if chassis == None or slot == None or head == None:
                raise InstrumentException,'The Slot,chassis, head parameters cannot be empty'
            self._conf[Name] = "%d,%d,%d"%(chassis,slot,head)
        self._ActiveConf = Name


    def connect(self):
        Base.connect(self)

    def setWavelength(self,wavl):
        self.write(":OUTP:WAV %s,%d"%(self._conf[self._ActiveConf],int(wavl)))

    def getWavelength(self,wavl):
        return int(self.query(":OUTP:WAV? %s"%(self._conf[self._ActiveConf])))


    def setAttenuation(self,Attn):
        self.write(":OUTP:ATT %s,%f"%(self._conf[self._ActiveConf],float(Attn)))

    def getAttenuation(self):
        return float(self.query(":OUTP:ATT? %s"%(self._conf[self._ActiveConf])) )

    def getPower(self):
        return float(self.query(":OUTP:POW? %s"%(self._conf[self._ActiveConf])) )

    def setOutputState(self,state = 0):
        ''' [ Beam Block, Beam Enabled] '''
        self.write(":OUTP:BBL %s,%d"%(self._conf[self._ActiveConf],state))

    def getOutputState(self):
        return int(self.query(":OUTP:BBL %s?"%(self._conf[self._ActiveConf])))

    def GetDiagnostics(self, retHeader = 0):
        if retHeader:
            self._attenuators = copy.deepcopy(self._conf)
            Header = ['Wavelength','Attenuation','STATE','Power Mon1'] * len(self._attenuators)
            return Header
        row = []
        for a in self._attenuators:
            row.append(float ( self.query(  ":OUTP:WAV? %s"%(self._conf[a])   ) ) )
            row.append(float ( self.query(  ":OUTP:ATT? %s"%(self._conf[a])   ) ) )
            row.append(float ( self.query(  ":OUTP:BBL? %s"%(self._conf[a])   ) ) )
            row.append(float ( self.query(  ":OUTP:POW? %s"%(self._conf[a])   ) ) )
            #row.append(float ( self.query('READ:POW? 1,1,1')))
        return row

class JDSUPowM(Base):
    '''This is a Optical Attenuator.
    Author : anand.s.ramalingam@intel.com'''
    version = 1.00
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)
        self.Name = ''
        self._conf = {}
        self._ActiveConf = None

    def __repr__(self):
        s = 'JDSU Optical PowerMeter\n'
        s += Base.__repr__(self)
        return(s)

    def SetActiveConf(self, Name = None,chassis = 1, slot = None, head = None  ):
        if Name == None:
            Name = "%d:%d:%d"%(chassis,slot,head)
        if not self._conf.has_key(Name):
            if chassis == None or slot == None or head == None:
                raise InstrumentException,'The Slot,chassis, head parameters cannot be empty'
            self._conf[Name] = "%d,%d,%d"%(chassis,slot,head)
        self._ActiveConf = Name


    def connect(self):
        Base.connect(self)

    def setWavelength(self,wavl):
        self.write(":SENS:POW:WAV %s,%.3f"%(self._conf[self._ActiveConf],float(wavl)))

    def getWavelength(self):
        return float(self.query(":SENS:POW:WAV? %s"%(self._conf[self._ActiveConf])))

    def getPower(self):
        if dbg: print "READ:POW? %s"%(self._conf[self._ActiveConf])
        reply = self.query(":READ:POW? %s"%(self._conf[self._ActiveConf]))
        if dbg: print reply
        if reply.find('--') >=0 :
            return -80.0
        else:
            return float( reply)

    def getDisplayedPower(self):
        #Fetch power function to be compatible with Agilent power meter
        if dbg: print "FETC:POW? s"%(self._conf[self._ActiveConf])
        reply = self.query(":FETC:POW? %s"%(self._conf[self._ActiveConf]))
        if dbg: print reply
        if reply.find('--') >=0 :
            return -80.0
        else:
            return float( reply)

    def GetDiagnostics(self, retHeader = 0):
        if retHeader:
            self._attenuators = copy.deepcopy(self._conf)
            Header = []
            for i in self._attenuators:
                Header.append('%s_PM'%(i))
            return Header
        row = []
        for a in self._attenuators:
            if dbg: print a,'READ:POW? %s'%self._conf[a],
            reply = self.query('READ:POW? %s'%self._conf[a])
            if dbg: print reply
            if  reply.find('--') >= 0:
                row.append(-100000)
            else:
                row.append(float (reply ))
            #time.sleep(.01)
        if dbg: print row
        return row

class JDSUTB9TF(Base):
    '''This is a TB9 stand alone Tunable Filter
    Author : john.chih@intel.com'''
    version = 1.00
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)
        self.Name = ''

    def __repr__(self):
        s = 'JDSU TB9 Tunable Grating Filter\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)

    def setWavelength(self,wavl):
        #sets filter wavelength in nm
        self.write("WVL %.2f NM"%(float(wavl)))

    def getWavelength(self):
        #gets filter wavelength in nm
        return float(self.query("WVL?")) * 1E9

    def GetDiagnostics(self,retHeader=0):
        if retHeader:
            Header = ['Wavelength']
            return Header
        wavl = (float(self.query("WVL?")) *1E9)
        return [wavl]


class HP83732(Base):
    'This is a Signal Generator'
    version = 1.00
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)
        self.Name = ''

    def __repr__(self):
        s = 'HP High Freq Signal Generator\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)

    def setFreq(self,Freq):
        self.write("FREQ %f GHz"%(float(Freq)))

##    def SetSonetFreq16(self,index):
##        'SONET (9.9 G),10GBE (10.3 G),SONET_FEC (10.7 G),11.1 G, 11.317G)'
##        index = int(index)
##        combinations = [622.08,644.5313,669.3265,693.4830,707.375]
##        #print index,"Sonet Freq:",combinations,combinations[index]
##        self.write("FREQ:FIX %f MHz"%(combinations[index]))

    def setState(self,state=0):
        '''[OFF,ON]'''
        comb = ['OFF','ON']
        self.write(":OUTP:STAT "+comb[state])

##    def SetModulationState(self,state = 0):
##        '''[OFF,ON]'''
##        comb = ['OFF','ON']
##        self.write(":OUTP:MOD:STAT "+comb[state])

##    def GetDiagnostics(self,retHeader=0):
##        if retHeader:
##            Header = ['Frequency','RF Output']
##            return Header
##        freq =(float(self.query(":FREQ:FIX?"))*1E-6)
##        state = (float(self.query(":OUTP:STAT?")))
##        return [freq,state]

    def setOutputState(self, state = 'NONE'):
        'This command enables the RF output when state = ON, and disables the RF output when state = OFF'
        state = state.upper()
        if state == "NONE":
            cmd = 'OUTP:STAT?'
        elif state == "ON":
            cmd = 'OUTP:STAT ON'
        elif state == "OFF":
            cmd = 'OUTP:STAT OFF'
        else:
            raise 'Invalid Input'
            #return "Invalid Input"
        self.write(cmd)
        if state == "NONE":
            s = str(self.read())
            return (int(s))
        else: return state
        
    def setPowerUnit(self, unit = 'DBM'):
        strCmd = ':UNIT:POW ' + unit
        self.write(strCmd)
        
    def setOutputPower(self, fltPower):
        strCmd = ':POW:LEV %f DBM' % fltPower
        self.write(strCmd)


class TDS8000B(Base):
    'This a digital oscilloscope'
    version = 1.00
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)

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

    def __repr__(self):
        s = 'Tektronix Digital Sampling Oscilloscope\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)

    def lockFrontPanel(self):
        self.write('LOCK ALL')
    def unlockFrontPanel(self):
        self.write('UNLOCK ALL')

    def PrintScreen(self,filename):
        self.write('HARDCopy:filename "%s"' % filename)
        print 'HARDCopy:filename "%s"' % filename
        time.sleep(3)
        self.write('HARDCopy')
        time.sleep(.5)
        self.write('*WAI')

    def AcquireWaveForm(self, waveFormNumb, filename = ''):
        '''Optionally save screen under filename'''
        self.write('ACQuire:STATE OFF')
        time.sleep(.5)
        self.write('ACQuire:STOPAFTER:MODE CONDITION')
        time.sleep(.5)
        self.write('ACQuire:STOPAFTER:COUNT %d' % waveFormNumb)
        time.sleep(.5)
        self.write('ACQuire:STOPAfter:CONDition ACQWfms')
        if filename <> '':
            #self.write('ACQuire:SAVEFile:SAVEScreen '+ '"%s"' % filename )
            #self.write('ACQuire:STOPAfter:ACTion SAVEScreen')
            time.sleep(.5)
            self.write('ACQuire:STOPAfter:ACTion NONE')
        else:
            time.sleep(.5)
            self.write('ACQuire:STOPAfter:ACTion NONE')

        time.sleep(.5)
        self.write('ACQuire:DATA:CLEAR')
        # run acquisition
        self.write('ACQuire:STATE ON')
        time.sleep(1.0)
        self.WaitForOperationComplete()
        float(self.__GetResultString('MEASUrement:MEAS%d:VALue?' % self.__extinctionRatioList[0]))
        time.sleep(.5)
        if filename <> '':
            self.write('HARDCopy:filename "%s"' % filename)
            time.sleep(3)
            self.write('HARDCopy')
            time.sleep(.5)
            self.write('*WAI')

    def RecallSetup(self, filename):
        self.write('REC:SETU "%s"' % filename)

    # Setup scope to read following measurements
    # 1: Amplitude (NZR) -> ER (Extinction ratio [dB])
    # 2: Crossing (%)
    # 3: Pk-Pk Jitter
    # 4: RMS Jitter
    # 5: Quality Factor
    def SetupScopeMeasurement(self):
        '''Setup scope Measurements'''
        self.write('*CLS')
        self.write('AUTOSET:TYPE EYE')
        time.sleep(0.1)
        self.write('SELECT:CH%d ON' % (self.currentChannel))
        time.sleep(0.1)
        # // set the wfmdb source and enable and display the wfmdb
        self.write('WFMDB:WFMDB1:SOURCE CH%d,MAIN' % (self.currentChannel))
        time.sleep(0.1)
        self.write('WFMDB:WFMDB1:ENABLE ON')
        time.sleep(0.1)
        self.write('WFMDB:WFMDB1:DISPLAY ON')

        # Mask settings
        self.write('MASK:DISPLAY ON') # turn off mask
        time.sleep(0.1)
        self.write('MASK:AUTOSET:MODE MANUAL')
        time.sleep(0.1)
        #self.write('MASK:STANDARD OC192')
        self.write('MASK:STANDARD FEC10709')
        time.sleep(0.1)
        self.write('MASK:SOURCE CH%d' % (self.currentChannel))
        time.sleep(0.1)
        #self.write('MASK:AUTOSET:MODE AUTO')
        #self.write('MASK:WFMDB:STATE ON') # FIX: is it really what we want?
        #self.write('MASK:MARgin:PERCENT 10.0') # FIX: what is the percentage?
        #self.write('MASK:MARgin:STATE ON')

        #self.write('CH%d:EXTAtten:MODE DB' % (self.currentChannel))
        #self.write('CH%d:EXTAtten:VALue 0' % (self.currentChannel))
        time.sleep(0.1)
        self.write('HARDCopy:FORMat JPEG')
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
            self.write('MEASUrement:MEAS%d:TYPE %s' % (meas[0],meas[1]))
            time.sleep(0.1)
            self.write('MEASUrement:MEAS%d:SOURCE1:WFM CH%d' % (meas[0], self.currentChannel))
            time.sleep(0.1)
            self.write('MEASUrement:MEAS%d:SOURCE1:WFMDB:SIGType EYE' % (meas[0]))
            time.sleep(0.1)
            self.write('MEASUrement:MEAS%d:STATE ON' % (meas[0]))
            time.sleep(0.1)

        # Rise and fall measurements
        self.write('MEASUrement:MEAS%d:REFLevel:METHod RELative' % self.__RiseList[0])
        time.sleep(0.1)
        self.write('MEASUrement:MEAS%d:REFLevel:RELative:HIGH 80' % self.__RiseList[0])
        time.sleep(0.1)
        self.write('MEASUrement:MEAS%d:REFLevel:RELative:LOW 20' % self.__RiseList[0])
        time.sleep(0.1)

        self.write('MEASUrement:MEAS%d:REFLevel:METHod RELative' % self.__FallList[0])
        time.sleep(0.1)
        self.write('MEASUrement:MEAS%d:REFLevel:RELative:HIGH 80' % self.__FallList[0])
        time.sleep(0.1)
        self.write('MEASUrement:MEAS%d:REFLevel:RELative:LOW 20' % self.__FallList[0])
        time.sleep(0.1)

        # Recall setup and overwrite these files
        #self.RecallSetup('C:\\Config\Setup.stp')

    def __GetResultString(self, queryString):
        '''Extract result from query. Example: MEASU:MEAS1:VAL?
        v1.5.2.2 returns: 51.1\n
        v1.3.3.1 returns: MEASU:MEAS1:VAL? 51.1\n'''
        result = self.query(queryString)
        if result.find(' ')>=0:
            return result.split(' ')[1]
        else:
            return result

    def GetExtinctionRatio(self):
        return float(self.__GetResultString('MEASUrement:MEAS%d:VALue?' % self.__extinctionRatioList[0]))

    def GetCrossing(self):
        return float(self.__GetResultString('MEASUrement:MEAS%d:VALue?' % self.__CrossingList[0]))

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
            self.write('CH%d:FILTer:VALue OC192' % self.currentChannel)
        elif filterType == 2:
            self.write('CH%d:FILTer:VALue FEC10709' % self.currentChannel)
        else:
            self.write('CH%d:FILTer:VALue NONe' % self.currentChannel)

        if blnReadBack:
            nRead = self.GetFilter()
            if filterType != nRead:
                raise InstrumentException('Eye scope tried to set filter to %d but read back %d' % \
                                          (filterType, nRead))

    #<DS>
    def GetFilter(self):
        strCmd = 'CH%d:FILTer:VALue?' % self.currentChannel
        strResp = self.query(strCmd)
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
        self.write('COMPensate:DARKLev:CH%d' % (self.currentChannel))
        time.sleep(15)
        # FIX: wait until completed!
        self.write('*WAI')

    def ExecuteAutoset(self):
        self.write('ACQuire:STOPAFTER:MODE RUNSTOP')
        time.sleep(0.1)
        self.write('ACQuire:STATE ON')
        time.sleep(0.1)
        #self.write('ACQuire:STATE OFF')
        self.write('AUTOSet EXECute')
        time.sleep(0.1)
        self.WaitForOperationComplete()
        #self.write('ACQuire:STATE ON')
        #self.write('ACQuire:STATE OFF')

    def GetID(self):
        return self.query('*IDN?')

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
            self.write('MASK:STANDARD OC192')
        else:
            self.write('MASK:STANDARD FEC10709')
        self.WaitForOperationComplete()
        self.write('MASK:MARGIN:PERCENT %d' % int(marginPercent))


class OMNIBER(Base):
    'This is a Wavelength meter'
    version = 1.00
    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)
        self.Name = ''

    def __repr__(self):
        s = 'Description: Burleigh Wave meter\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)

    def command(self):
        self.write("dsfasdfasd")

    #
    # Function: getAlarmStatus
    #
    def getAlarmStatus(self):
        ret = self.query(':stat:isum:cond?')
        return int(ret)
    #
    # Function: getPower
    #
    def getPower(self):
        ret = self.query(":sense:data? 'OPOW'")
        return float(ret)
    #
    # Function: getBer
    #
    def getBer(self, mode = 'lastSecond'):

        wait = 1
        base_cmd = ':sens:data'

        if (mode == 'lastSecond'):
            cmd = "? 'erat:lsec:bit'"
        elif (mode == 'interval'):
            cmd = "? 'erat:bit'"
        else:
            cmd = "? 'erat:bit'"

        ret = self.query(base_cmd + cmd)
        time.sleep(1)

        return float(ret)
    #
    # Function: getJitterTransferData
    #
    def getJitterTransferData(self):

        base_cmd = ':fetc:arr:data:tel:tran:data?'

        dataArray = self.query(base_cmd)
        return dataArray
    #
    # Function: getJitterTransferData
    #
    def getJitterToleranceData(self):

        base_cmd = ':fetc:arr:data:tel:atol:data?'

        dataArray = self.query(base_cmd)
        return dataArray

    #
    # Function: getJitterGenData
    #
    def getJitterGenData(self, jitterValue = None):

        base_cmd = ':sens:data?'

        value = self.query(base_cmd + ' "' + jitterValue + '"')
        return float(value)
    #
    # Function: setJitterTransferRun
    #
    def setJitterTransferRun(self):

        base_cmd = ':sour:data:tel:'
        cmd = 'tran:mode'
        query = self.query(base_cmd + cmd + '?')[:-2]
        print '... Running %s ...' % query,

        wait = 5
        base_cmd = ':sour:data:tel:'
        cmd = 'tran'
        self.write(base_cmd + cmd + ' ' + 'on')
        time.sleep(wait)

        running = 1
        while (running):
            print '.',
            running = int(self.query(base_cmd + cmd + '?'))
            time.sleep(wait)
        print '.'

        base_cmd = ':sour:data:tel:'
        cmd = 'tran:mode'
        query = self.query(base_cmd + cmd + '?')
        print '... Ready for %s' % query
    #
    # Function: setJitterToleranceRun
    #
    def setJitterToleranceRun(self):

        wait = 5
        base_cmd = ':sour:data:tel:'
        cmd = 'tol'
        self.write(base_cmd + cmd + ' ' + 'on')
        time.sleep(wait)

        print '... Running jitter tolerance ...',

        running = 1
        while (running):
            print '.',
            running = int(self.query(base_cmd + cmd + '?'))
            time.sleep(wait)
        print '.'

    #
    # Function: unlockJitterTransfer
    #
    def unlockJitterTransfer(self):

        wait = 10

        base_cmd = ':sour:data:tel:'
        cmd = 'tran'

        self.write(base_cmd + cmd + ' ' + 'off')
        time.sleep(wait)
        print '... OmniBer jitter transfer stopped'

        base_cmd = ':sour:data:tel:'
        cmd = 'tran:lock'

        self.write(base_cmd + cmd + ' ' + 'off')
        time.sleep(wait)
        print '... OmniBer jitter transfer unlocked'

    #
    # Function: setRunStop
    #
    def setRunStop(self, mode = 'interval', runStop = 'stop'):

        base_cmd = ':sens:data:tel:'
        wait = 1
        cmd = 'test'
        if (runStop == 'run'):
            self.write(base_cmd + cmd + ' ' + 'on')
        elif (runStop == 'stop'):
            self.write(base_cmd + cmd + ' ' + 'off')
        else:
            self.write(base_cmd + cmd + ' ' + 'off')

        time.sleep(wait)
        if (runStop == 'run'):
            if (mode == 'interval'):
                running = 1
                while (running):
                    print '.',
                    running = int(self.query(base_cmd + cmd + '?'))
                    time.sleep(wait)
                print '.'

    #
    # Function: setLaser
    #
    def setLaser(self, switch = 'off', debug = 0):

        base_cmd = ':outp:tel:'
        wait_off = 1
        wait_on = 5
        cmd = 'las'
        if (switch == 'on'):
            self.write(base_cmd + cmd + ' ' + 'on')
            time.sleep(wait_on)
        else:
            self.write(base_cmd + cmd + ' ' + 'off')
            time.sleep(wait_off)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)
    #
    # Function: setCoupling
    #
    def setCoupling(self, mode = 'txrx', debug = 0):
        base_cmd = ':inst:'
        cmd = 'coup'
        if (mode == 'txrx'):
            self.write(base_cmd + cmd + ' ' + 'txrx')
        elif (mode == 'rxtx'):
            self.write(base_cmd + cmd + ' ' + 'rxtx')
        else:
            self.write(base_cmd + cmd + ' ' + 'off')
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)
    #
    # Function: setSonetTxRx
    #
    def setSonetTxRx(self, doOhDefault = 0, debug = 0):

        base_cmd = ':sour:data:tel:'
        wait = 1
        cmd = 'mode'
        self.write(base_cmd + cmd + ' ' + 'son')
        time.sleep(10)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'son:rate'
        self.write(base_cmd + cmd + ' ' + 'oc192')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'son:spe:type'
        self.write(base_cmd + cmd + ' ' + 'sts192c')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'son:sts3'
        self.write(base_cmd + cmd + ' ' + '1')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'patt:type'
        self.write(base_cmd + cmd + ' ' + 'prbs')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'patt:type:prbs'
        self.write(base_cmd + cmd + ' ' + 'prbs23')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'patt:polarity'
        self.write(base_cmd + cmd + ' ' + 'inv')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        if doOhDefault:
            cmd = 'son:over:def'
            self.write(base_cmd + cmd)
            time.sleep(wait)
            if debug: print '... query = default'
    #
    # Function: setOtnTxRx
    #
    def setOtnTxRx(self, doOhDefault = 0, debug = 0):

        base_cmd = ':sour:data:tel:'
        wait = 1
        cmd = 'mode'
        self.write(base_cmd + cmd + ' ' + 'otn')
        time.sleep(10)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'otn:rate'
        self.write(base_cmd + cmd + ' ' + 'otu2')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'otn:scr'
        self.write(base_cmd + cmd + ' ' + 'on')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'otn:fec'
        self.write(base_cmd + cmd + ' ' + 'off')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'otn:payl'
        self.write(base_cmd + cmd + ' ' + 'sdh')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'otn:mapp'
        self.write(base_cmd + cmd + ' ' + 'asyn')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'sdh:au:type'
        self.write(base_cmd + cmd + ' ' + 'au4_64c')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'patt:type'
        self.write(base_cmd + cmd + ' ' + 'prbs')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'patt:type:prbs'
        self.write(base_cmd + cmd + ' ' + 'prbs32')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'patt:polarity'
        self.write(base_cmd + cmd + ' ' + 'inv')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        if doOhDefault:
            cmd = 'otn:over:def'
            self.write(base_cmd + cmd)
            time.sleep(wait)
            if debug: print '... query = default'

            cmd = 'sdh:over:def'
            self.write(base_cmd + cmd)
            time.sleep(wait)
            if debug: print '... query = default'
    #
    # Function: setMeasureTime
    #
    def setMeasureTime(self, mode = 'single', debug = 0):

        base_cmd = ':sens:data:tel:test:'
        wait = 1

        cmd = 'type'
        if (mode == 'single'):
            self.write(base_cmd + cmd + ' ' + 'sing')
        elif (mode == 'manual'):
            self.write(base_cmd + cmd + ' ' + 'man')
        else:
            self.write(base_cmd + cmd + ' ' + 'man')

        time.sleep(wait)

        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        if (mode == 'single'):
            cmd = 'period'
            self.write(base_cmd + cmd + ' ' + '0,0,1,0')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)
    #
    # Function: setSonetJitter
    #
    def setSonetJitter(self, doTx = 1, doRx = 1,
                       tranPnts = 20, tranSet = 5, tranGate = 10,
                       tolPnts = 20, tolCnt = 300, tolSet = 1, tolGate = 3, debug = 0):

        # Tx settings ...

        if doTx:
            if debug: print '... Tx settings ...'
            base_cmd = ':sour:data:tel:jitt:'
            wait = 1

            cmd = 'type'
            self.write(base_cmd + cmd + ' ' + 'off')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)

        # Rx settings ...

        if doTx:
            if debug: print '... Rx settings ...'
            base_cmd = ':sens:data:tel:jitt:'
            wait = 5

            cmd = 'type'
            self.write(base_cmd + cmd + ' ' + 'jitt')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)

            cmd = 'rang'
            self.write(base_cmd + cmd + ' ' + 'ui0_8')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)

            cmd = 'pthr'
            self.write(base_cmd + cmd + ' ' + '0.025')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)

            cmd = 'nthr'
            self.write(base_cmd + cmd + ' ' + '0.025')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)

            cmd = 'filt:hpas'
            self.write(base_cmd + cmd + ' ' + 'on')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)

            cmd = 'filt:lpas'
            self.write(base_cmd + cmd + ' ' + 'on')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)

            cmd = 'dout'
            self.write(base_cmd + cmd + ' ' + 'bp_khz50')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)

        # Tolerance settings ...

        if debug: print '... Tolerance settings ...'
        base_cmd = ':sour:data:tel:tol:'
        wait = 1

        cmd = 'type'
        self.write(base_cmd + cmd + ' ' + 'jitt')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'mode'
        self.write(base_cmd + cmd + ' ' + 'auto')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'poin'
        self.write(base_cmd + cmd + ' ' + str(tolPnts))
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'mask'
        self.write(base_cmd + cmd + ' ' + 'gr253r')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'freq:star'
        self.write(base_cmd + cmd + ' ' + '100')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'freq:stop'
        self.write(base_cmd + cmd + ' ' + '80000000')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'err:mode'
        self.write(base_cmd + cmd + ' ' + 'berp')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'err:sour'
        self.write(base_cmd + cmd + ' ' + 'bit')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'err:coun'
        self.write(base_cmd + cmd + ' ' + str(tolCnt))
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'sett'
        self.write(base_cmd + cmd + ' ' + str(tolSet))
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'gate'
        self.write(base_cmd + cmd + ' ' + str(tolGate))
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        # Transfer settings ...

        if debug: print '... Transfer settings ...'
        base_cmd = ':sour:data:tel:tran:'
        wait = 1

        cmd = 'poin'
        self.write(base_cmd + cmd + ' ' + str(tranPnts))
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'mask:inp'
        self.write(base_cmd + cmd + ' ' + 'gr253r')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'freq:star'
        self.write(base_cmd + cmd + ' ' + '100')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'freq:stop'
        self.write(base_cmd + cmd + ' ' + '80000000')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'mask:pass'
        self.write(base_cmd + cmd + ' ' + 'gr253-core pass')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'mask:pass:offset'
        self.write(base_cmd + cmd + ' ' + '0')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'sett'
        self.write(base_cmd + cmd + ' ' + str(tranSet))
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'gate'
        self.write(base_cmd + cmd + ' ' + str(tranGate))
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'mode'
        self.write(base_cmd + cmd + ' ' + 'cal')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

    #
    # Function: setOtnJitter
    #
    def setOtnJitter(self, doTx = 1, doRx = 1,
                     tranPnts = 20, tranSet = 5, tranGate = 10,
                     tolPnts = 10, tolCnt = 100, tolSet = 1, tolGate = 10, debug = 0):

        # Tx settings ...

        if doTx:
            if debug: print '... Tx settings ...'
            base_cmd = ':sour:data:tel:jitt:'
            wait = 1

            cmd = 'type'
            self.write(base_cmd + cmd + ' ' + 'off')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)

        # Rx settings ...

        if doTx:
            if debug: print '... Rx settings ...'
            base_cmd = ':sens:data:tel:jitt:'
            wait = 5

            cmd = 'type'
            self.write(base_cmd + cmd + ' ' + 'jitt')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)

            cmd = 'rang'
            self.write(base_cmd + cmd + ' ' + 'ui0_8')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)

            cmd = 'pthr'
            self.write(base_cmd + cmd + ' ' + '0.025')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)

            cmd = 'nthr'
            self.write(base_cmd + cmd + ' ' + '0.025')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)

            cmd = 'filt:hpas'
            self.write(base_cmd + cmd + ' ' + 'on')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)

            cmd = 'filt:lpas'
            self.write(base_cmd + cmd + ' ' + 'on')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)

            cmd = 'dout'
            self.write(base_cmd + cmd + ' ' + 'bp_khz50')
            time.sleep(wait)
            query = self.query(base_cmd + cmd + '?')
            if debug: print '... query %s = %s' % (cmd, query)

        # Tolerance settings ...

        if debug: print '... Tolerance settings ...'
        base_cmd = ':sour:data:tel:tol:'
        wait = 1

        cmd = 'type'
        self.write(base_cmd + cmd + ' ' + 'jitt')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'mode'
        self.write(base_cmd + cmd + ' ' + 'auto')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'poin'
        self.write(base_cmd + cmd + ' ' + str(tolPnts))
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'mask'
        self.write(base_cmd + cmd + ' ' + 'g8251')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'freq:star'
        self.write(base_cmd + cmd + ' ' + '2000')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'freq:stop'
        self.write(base_cmd + cmd + ' ' + '80000000')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'err:mode'
        self.write(base_cmd + cmd + ' ' + 'berp')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'err:sour'
        self.write(base_cmd + cmd + ' ' + 'bit')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'err:coun'
        self.write(base_cmd + cmd + ' ' + str(tolCnt))
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'sett'
        self.write(base_cmd + cmd + ' ' + str(tolSet))
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'gate'
        self.write(base_cmd + cmd + ' ' + str(tolGate))
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        # Transfer settings ...

        if debug: print '... Transfer settings ...'
        base_cmd = ':sour:data:tel:tran:'
        wait = 1

        cmd = 'poin'
        self.write(base_cmd + cmd + ' ' + str(tranPnts))
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'mask:inp'
        self.write(base_cmd + cmd + ' ' + 'g8251')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'freq:star'
        self.write(base_cmd + cmd + ' ' + '2000')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'freq:stop'
        self.write(base_cmd + cmd + ' ' + '80000000')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'mask:pass'
        self.write(base_cmd + cmd + ' ' + 'g8251 odcr pass')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'mask:pass:offset'
        self.write(base_cmd + cmd + ' ' + '0')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'sett'
        self.write(base_cmd + cmd + ' ' + str(tranSet))
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'gate'
        self.write(base_cmd + cmd + ' ' + str(tranGate))
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)

        cmd = 'mode'
        self.write(base_cmd + cmd + ' ' + 'cal')
        time.sleep(wait)
        query = self.query(base_cmd + cmd + '?')
        if debug: print '... query %s = %s' % (cmd, query)


    def readback(self):
        return self.query("*idn?")[:-2]

class NONE:
    'This is a simulated class'
    version = 1.00
    def __repr__(self):
        s = 'Simulated Instrument: NONE\n'
        return(s)

    def __getattr__(self,attr):
        if attr in self.__dict__:
            return self.__dict__[attr]
        else:
            return self.__swallow
    def __swallow(self,*ignore,**Ignore):
        pass
    def GetDiagnostics(self,retHeader=0):
        if retHeader:
            Header = []
            return Header
        return []

    def __del__(self):
        pass


DIR = dir()


#<DS> # this portion is for child instruments only!
class ChildInstrument:
    def __init__(self, parentMF, location):
        #print 'entering ChildInstrument constructor'
        self._location = location
        #print 'type of parentMF arg = ', type(parentMF)
        if type(parentMF) == types.StringType:
            self._parentMF = findMyParent(parentMF)
        else:
            self._parentMF = parentMF
        if self._parentMF == None:
            raise InstrumentException('cannot find parent! parentMF = %s, location = %s' % \
                                      (parentMF, location) )
            
    
    def __del__(self):
        self.kill()

    def kill(self):
        self.disconnect()
        self._parentMF = None
    
    def getLocation(self):
        return self._location
           
    def disconnect(self):
        if self._parentMF:            
            return self._parentMF.disconnect()
        
    def connect(self):
        return self._parentMF.connect()
    def identity(self):
        return self._parentMF.identity()

    def reset(self):
        return self._parentMF.reset()
    def poll(self):
        return self._parentMF.poll()
    
    
    def write(self, strCommand):
        return self._parentMF.write(strCommand)

    def read(self, buffer = 100, delay = 0.005):
        return self._parentMF.read(strCommand, buffer, delay)

    
    def query(self, strQuery, buffer = 100, delay = 0.005):
        return self._parentMF.query(strQuery, buffer, delay)


########################################################################################
## child instruments
########################################################################################
class AndoChildVoa(ChildInstrument):
    '''
    This class implements the basic voa interface AND the basic pmc interface.
    Voa functions:
        setOutputState(state)  'ON' or 'OFF'
        setAttenuation(attenuation)
        setAttenuationOffset(offset) calibration constant for voa
    pmc functions:    
        getPower()    
        getDisplayedPower()
        SetActiveConf(name= None, slot, head)  useless for me, just swallow this function
    common functions:
        setWavelength(wl)
        getWavelength()
        setFrequency(freq)
        getFrequency()
    '''
    def __init__(self, parentMF, location):
        #print 'entering AndoChildVoa constructor'
        ChildInstrument.__init__(self, parentMF, location)
        self.__nSlot = int(self._location)
        self.__strName = 'JohnDoe'      # to support an agilent pmc function

    def __repr__(self):
        return 'AndoChildVoa at location: ' + str(self.getLocation())
    def connect(self):
        ChildInstrument.connect(self)
        self.setDisplayMode()
        
    #<attenuator functions>
    def setAttenuation(self, fltAttenuation = 25.0, fltSleepTime = 0.6):
        self.__selectMe()
        self.write( 'AAV%0.2f' % fltAttenuation )
        # TODO: get rid of this?
        time.sleep(fltSleepTime)
    def getAttenuation(self):
        self.__selectMe()
        return float(  self.query('AAV?')  )
    
    def setAttenuationOffset(self, fltOffset = 0.0):
        self.__selectMe()
        self.write('ACAL%0.3f' % fltOffset)
    def getAttenuationOffset(self):
        self.__selectMe()
        return float(  self.query('ACAL?')  )
    
    def setOutputState(self, state = 'NONE'):
        self.__selectMe()
        strCmd = 'ASHTR'

        if type(state) == types.IntType or type(state) == types.FloatType:
            state = ['ON','OFF'][int(state)]
            
        if state == 'NONE':
            # query the output state and return
            strCmd += '?'            
            return int( self.query(strCmd) )
        elif state.upper() == 'ON':
            # open shutter and return
            strCmd += '1'
        elif state.upper() == 'OFF':
            # close the shutter and return
            strCmd += '0'

        self.write(strCmd)
    #</attenuator functions>

    #<pmc functions>
    def getPower(self, queryDelay = 0.20):
        self.__selectMe()
        time.sleep(0.25)
        strResp = self.query('POD?', delay = queryDelay)
        #print 'AndoChildVoa.getPower() returned: ' + strResp
        return float( strResp )

    
    getDisplayedPower = getPower
    triggerReadPower = getPower

    def setCalibrationConst(self, fltCal):
        self.__selectMe()
        # reversing the sign of the calibration
        # because its "polarity" is different from
        # the Agilent powermeter calibration.
        self.write('PCAL%0.2f' % -fltCal)
    setPmcCalibration = setCalibrationConst 
    def getCalibrationConst(self):
        self.__selectMe()
        # reversing the sign of the calibration
        # because its "polarity" is different from
        # the Agilent powermeter calibration.
        return -float(  self.query('PCAL?')  )
    getPmcCalibration = getCalibrationConst
    
    def SetActiveConf(self, Name = None, slot = None, head = None  ):
        if Name:
            self.__strName = Name
    def getName(self):
        return self.__strName
    def getSlot(self):
        return int( self.getLocation() )
    def getHead(self):
        return 0
    def setPowerUnit(self, nUnit = 0):
        '0 is dBm, 1 is W'
        self.__selectMe()
        strCmd = 'PF'
        if nUnit:
            strCmd += 'A'
        else:
            strCmd += 'B'
        self.write(strCmd)
        
    def getPowerUnit(self):
        '0 is dBm, 1 is W'
        self.__selectMe()
        strResp = self.query('PF?')
        if strResp[-1]=='A':
            return 1
        elif strResp[-1] =='B':
            return 0
        else:
            raise InstrumentException('AndoChildVoa returned unrecognized response for power unit')
        
    #</pmc functions>        

    #<common functions>
    def setWavelength(self, fltWLnm):
        self.__selectMe()
        #print 'AndoChildVoa.setWavelength, wl = %0.4f' % fltWLnm
        strWL = str(int(round(fltWLnm)))
        #print 'wl converted to string:%s' % strWL
        self.write('AW' + strWL)      # attenuator wl
        self.write('PW' + strWL)      # powermeter wl
    def getWavelength(self):
        self.__selectMe()
        # stupid ANDO mainframe returns wl in meters, accepts wl in nm...
        return float( self.query('AW?') ) * 1e9
    
    def setFrequency(self, fltFreq_THz):
        fltWL = thztonm(fltFreq_THz)
        self.setWavelength( fltWL )
    def getFrequency(self):
        return nmtothz( self.getWavelength() )
    
    def setOutputPower(self, fltPower_dBm):
        self.__selectMe()
        self.write('APDB%0.2f' % fltPower_dBm)
    def setDisplayMode(self, nMode = 0):
        self.__selectMe()
        strCmd = 'AMOD'
        if nMode == 0:
            strCmd += 'B'
        else:
            strCmd += 'A'
        self.write(strCmd)
    #</common functions>        

    def __selectMe(self):
        self._parentMF.selectSlot( self.__nSlot )
    
class AndoChildSwitch(ChildInstrument):
    '''
    This class must implement the basic optical switch interface,
    setRouteChannel(inChannel, outChannel)
    turnChannelOff()
    
    ''' 
    def __init__(self, parentMF, location):
        ChildInstrument.__init__(self, parentMF, location)
        # expecting a location of the form slot.channel        
        lstLocation = map( int, str(location).split('.'))
        self.__nSlot = lstLocation[0]
        if len( lstLocation ) > 1:
            self.__nSubSlot = lstLocation[1]
        else:
            self.__nSubSlot = 0
        
        
    def setRouteChannel(self, inChannel, outChannel = None):
        self.__selectMe()
        # just verify that these are integers now
        if outChannel == None:
            # 2x2 switch
            self.write('S%s' % inChannel.upper())
        elif outChannel=='OFF':
            self.turnChannelOff(inChannel)
        else:
            nIn = int(inChannel)
            nOut = int(outChannel)
            self.write('SA%dSB%d' % (nIn, nOut) )
        
    
    def turnChannelOff(self, inChannel = 1):
        if self.getMinOutput():
            raise InstrumentException('Cannot turn this channel off:  there is no 0 output')
        self.setRouteChannel(inChannel, 0)
        

    def getMinOutput(self):
        self.__selectMe()
        return int( self.query('SBMIN?').strip('SBMIN') )
    
    def getMaxOutput(self):
        self.__selectMe()
        return int( self.query('SBMAX?').strip('SBMAX') )

    def getMinInput(self):
        self.__selectMe()
        return int( self.query('SAMIN?').strip('SAMIN') )

    def getMaxInput(self):
        self.__selectMe()
        return int( self.query('SAMAX?').strip('SAMAX') )

    def __selectMe(self):
        self._parentMF.selectSlot( self.__nSlot )
        if self.__nSubSlot:
            self._parentMF.selectSubSlot( self.__nSubSlot )
        
class AndoChildPmc(ChildInstrument):
    def __init__(self, parentMF, location):
        ChildInstrument.__init__(self, parentMF, location)
        # expecting a location of the form slot.channel        
        lstLocation = map( int, str(location).split('.'))
        self.__nSlot = lstLocation[0]
        if len( lstLocation ) > 1:
            self.__nSubSlot = lstLocation[1]
        else:
            self.__nSubSlot = 0
            
        # the keys are the ranges defined by the pmc,
        # the values are the character used to represent
        # the range in a text command.  for example,
        # to set to range -20 the command is 'PRH' where
        # the 'H' comes from the dictionary below
        self.__dicRange = {'AUTO':'A',
                           30.0:'C',
                           20.0:'D',
                           10.0:'E',
                           0.0:'F',
                           -10.0:'G',
                           -20.0:'H',
                           -30.0:'I',
                           -40.0:'J',
                           -50.0:'K',
                           -60.0:'L',
                           'HOLD':'Z'}

    def connect(self):
        ChildInstrument.connect(self)
        self.setRange()
    
    def getPower(self, queryDelay = 0.20):
        self.__selectMe()
        time.sleep(0.25)
        strResp = self.query('POD?', delay = queryDelay)
        #print 'AndoChildVoa.getPower() returned: ' + strResp
        return float( strResp )

    
    getDisplayedPower = getPower
    triggerReadPower = getPower

    def setCalibrationConst(self, fltCal):
        self.__selectMe()
        # reversing the sign of the calibration
        # because its "polarity" is different from
        # the Agilent powermeter calibration.
        self.write('PCAL%0.2f' % -fltCal)
    setPmcCalibration = setCalibrationConst 
    def getCalibrationConst(self):
        self.__selectMe()
        # reversing the sign of the calibration
        # because its "polarity" is different from
        # the Agilent powermeter calibration.
        return -float(  self.query('PCAL?')  )
    getPmcCalibration = getCalibrationConst
    
    def SetActiveConf(self, Name = None, slot = None, head = None  ):
        if Name:
            self.__strName = Name
    def getName(self):
        return self.__strName
    def getSlot(self):
        return self.__nSlot
    def getHead(self):
        return self.__nSubSlot
    def setPowerUnit(self, nUnit = 0):
        '0 is dBm, 1 is W'
        self.__selectMe()
        strCmd = 'PF'
        if nUnit:
            strCmd += 'A'
        else:
            strCmd += 'B'
        self.write(strCmd)
        
    def getPowerUnit(self):
        '0 is dBm, 1 is W'
        self.__selectMe()
        strResp = self.query('PF?')
        if strResp[-1]=='A':
            return 1
        elif strResp[-1] =='B':
            return 0
        else:
            raise InstrumentException('AndoChildVoa returned unrecognized response for power unit')
    def setWavelength(self, fltWLnm):
        self.__selectMe()
        #print 'AndoChildVoa.setWavelength, wl = %0.4f' % fltWLnm
        strWL = str(int(round(fltWLnm)))
        #print 'wl converted to string:%s' % strWL

        self.write('PW' + strWL)      # powermeter wl
    def getWavelength(self):
        self.__selectMe()
        # stupid ANDO mainframe returns wl in meters, accepts wl in nm...
        return float( self.query('PW?') ) * 1e9
    
    def setFrequency(self, fltFreq_THz):
        fltWL = thztonm(fltFreq_THz)
        self.setWavelength( fltWL )
    def getFrequency(self):
        return nmtothz( self.getWavelength() )

    def setRange(self, range=None):
        strCmd = 'PR'
        if range==None:
            # autorange
            strCmd += self.__dicRange['AUTO']
        else:
            #find the nearest range
            fltNearestRange = None
            for key in self.__dicRange.keys():
                if ( type(key) != types.StringType  ):
                    if (fltNearestRange == None ) or (abs( key- range ) < abs( fltNearestRange - range)):
                        fltNearestRange = key
            strCmd += self.__dicRange[fltNearestRange]

        self.__selectMe()
        self.write(strCmd)
    def getRange(self):
        strResp = self.query('PR?')
        #print 'AndoChildPmc.getRange() returned %s' % strResp
        return self.__dicRange.keys()[    self.__dicRange.values().index( strResp[-1])     ]   
        
    def __selectMe(self):
        self._parentMF.selectSlot( self.__nSlot )
        if self.__nSubSlot:
            self._parentMF.selectSubSlot( self.__nSubSlot )

class AgilentChildPmc(ChildInstrument):
    def __init__(self, parentMF, location):
        ChildInstrument.__init__(self, parentMF, location)
        lstLocation = map( int, str(location).split('.'))
        self.__nSlot = lstLocation[0]
        self.__nHead = lstLocation[1]
        # i have to use this tuple quite a bit to format command strings
        # so i will define it once here
        self.__tupCmd = (self.__nSlot, self.__nHead)
    def SetActiveConf(self, Name = None, slot = None, head = None):
        print 'Warning: AgilentChildPmc.SetActiveConf is obselete'
        pass
    def getName(self):
        return 'pmc_' + self._location
    def getSlot(self):
        return self.__nSlot
    def getHead(self):
        return self.__nHead
    def getPower(self, queryDelay = 0.05):
        if self.__nHead > 1:
            strCmd = ':INIT%d:CHAN1:TRIG:IMM' % self.__nSlot
            self.write(strCmd)
            strCmd = 'FETC%d:CHAN%d:POW?' % self.__tupCmd
        else:
            strCmd = 'READ%d:CHAN%d:POW?' % self.__tupCmd
        return float(self.query(strCmd, delay = queryDelay))
    triggerReadPower = getPower
    
    def getDisplayedPower(self, queryDelay = 0.002):
        strCmd = 'FETC%d:CHAN%d:POW?' % self.__tupCmd
        strResp = self.query(strCmd, delay = queryDelay)
        try:
            fltReturn = float(strResp)
        except:
            fltReturn = -80.0
        return fltReturn
    def setWavelength(self, fltWLnm):
        strCmd = 'SENS%d:CHAN%d:POW:WAV %.2fnm' % (self.__nSlot, self.__nHead, fltWLnm)
        self.write(strCmd)
    def getWavelength(self):
        strCmd = 'SENS%d:CHAN%d:POW:WAV?' % self.__tupCmd
        # convert response to nm.  The agilent will reply in meters
        return float(self.query(strCmd)) * 1.00E+9
    def setFrequency(self, fltFreq):
        self.setWavelength( thztonm(fltFreq) )
    def getFrequency(self):
        return nmtothz( self.getWavelength() )
    def setPowerUnit(self, nUnit = 0):
        'sets the power unit: 0 = dBm, 1 = Watts'
        strCmd = 'SENS%d:CHAN%d:POW:UNIT %d' % (self.__nSlot, self.__nHead, nUnit)
        self.write(strCmd)
    def getPowerUnit(self):
        strCmd = 'SENS%d:CHAN%d:POW:UNIT?' % self.__tupCmd
        return int( self.query(strCmd) )
    def setCalibrationConst(self, fltCal = 0.0):
        strCmd = 'SENS%d:CHAN%d:CORR %fDB' % (self.__nSlot, self.__nHead, fltCal)
        self.write(strCmd)
    def getCalibrationConst(self):
        strCmd = 'SENS%d:CHAN%d:CORR?' % self.__tupCmd
        return float( self.query(strCmd) )
    def setAvgTime(self, fltAvgSec):
        strCmd = 'SENS%d:CHAN%d:POW:ATIM %f' % (self.__nSlot, self.__nHead, fltAvgSec)
        self.write(strCmd)
    setAveragingTime = setAvgTime
    def getAvgTime(self):
        strCmd = 'SENS%d:CHAN%d:POW:ATIM?' % self.__tupCmd
        return float(  self.query( strCmd )  )
        


########################################################################################
## mainframes
########################################################################################
class MainframeBase(Base):
    def __init__(self, board=0, pad=2):
        #print 'entering MainframeBase constructor'
        Base.__init__(self, board, pad)
        self.__blnConnected = 0
    def connect(self):
        #print 'entering MainframeBase.connect()'
        if not self.__blnConnected:
            #print self.__repr__ + ' IS CONNECTING...'
            Base.connect(self)
            self.__blnConnected = 1
    def disconnect(self):
        #print 'entering MainframeBase.disconnect()'
        if self.__blnConnected:
            Base.disconnect(self)
            self.__blnConnected = 0
        
class AgilentMainframe(MainframeBase):
    def __init__(self, board=0, pad=20):
        MainframeBase.__init__(self, board, pad)

class AndoMainframe(MainframeBase):
    def __init__(self, board=0, pad=2):
        #print 'entering AndoMainframe constructor'
        MainframeBase.__init__(self, board, pad)
    def connect(self):
        MainframeBase.connect(self)
        time.sleep(1.0)
        self.__echoOff()
        
    def selectSlot(self, nSlot):
        self.write( 'C' + str(nSlot) )
        nSelected = self.getSelectedSlot()
        if nSelected != nSlot:
            raise InstrumentException('ANDO mainframe tried to select slot %d, read back %d' % \
                                      (nSlot, nSelected) )
    def getSelectedSlot(self):
        strResp = self.query('C?')
        #print 'AndoMainframe.getSelectedSlot() returned:' + strResp
        strResp = strResp.strip()
        strResp = strResp.strip('C')
        return int(strResp) 

    def selectSubSlot(self, nSubSlot):
        self.write('D' + str(nSubSlot) )
        nSelected = self.getSelectedSubSlot()
        if nSelected != nSubSlot:
            raise InstrumentException('ANDO mainframe tried to select subslot %d, read back %d' % \
                                      (nSubSlot, nSelected) )
        
    def getSelectedSubSlot(self):
        strResp = self.query('D?')
        return int( strResp[1:] )
    
    def query(self, strQuery, buffer = 100, delay = 0.005):
        strResp = MainframeBase.query(self, strQuery, buffer, delay)
        return strResp.strip('\r\n')
    
    def queryFloat(self, strCmd):
        strResp = self.query(strCmd)
        #strResp.replace('-'

    def __echoOff(self):
        self.write('HED1')
        
    
def defaultFindMyParent(parentDescriptor):
    strMsg = 'Error: You tried to instantiate a child instrument without passing the parent mainframe.' + \
             '  In order to do this, you must first provide this module with a function pointer that ' + \
             'will accept the argument you passed and return the parent instance.'
    print strMsg
    raise InstrumentException(strMsg)
findMyParent = defaultFindMyParent


def mwTodBm(fltPower_mW):
    return 10.0 * math.log10(fltPower_mW)
def dBmTomw(fltPower_dBm):
    return math.pow(10.0, fltPower_dBm/10.0)
mwtodbm = mwTodBm
dbmtomw = dBmTomw
def thztonm(fltTHz):
    return (LIGHT_SPEED/fltTHz) * 1e-3
def nmtothz(fltnm):
    return (LIGHT_SPEED/fltnm) * 1E-3

class Therm8800(Base):
    #Added by Tim Dense to support NPIMonarch activities
    
    def __init__(self, board=2, pad=15):
        ##print board
        ##print pad
        ##print DYNVAR.Oven
        Base.__init__(self, board, pad)
        

    def __repr__(self):
        s = 'Thermotron Environmental Oven\n'
        s += Base.__repr__(self)
        return(s)

    def connect(self):
        Base.connect(self)

    def RunManual(self):
        strCmd = 'RUNM'
        self.write(strCmd)
        
    def StopManual(self):
        strCmd = 'STOP'
        self.write(strCmd)
    
    def getSetPointn(self, Channel = 1):
        strCmd = ('SETP' + str(Channel) +'?' )
        SP=float(self.query(strCmd))
        time.sleep(1)
        strCmd = ('SETP' + str(Channel) +'?' )
        ##print strCmd
        #need to read twice since instrument returns junk the first time
        return float(self.query(strCmd))

    def setSetPointn(self, Channel = 1, SP=25):
        strCmd = ('SETP' + str(Channel) + ',' + str(SP) )
        self.write(strCmd)

    def setSetPointnBySeq(self, Channel = 1,SequenceParms=['testname',25,100,'version']):
        ##This method determines the oven setpoin from the sequence name.  the name must follow the format Name_Temp_Volt__Versioninfo
##dvtber_25_100__v01
        strCmd = ('SETP' + str(Channel) + ',' + SequenceParms[1])
        self.write(strCmd)        
        
    def getProcessVarn(self, Channel = 1):
        strCmd = ('PVAR' + str(Channel) +'?' )
        return float(self.query(strCmd))

    def getOvenStatus(self, MonitorChannel = 1, SPChannel=1,SP=25):
        dblSP=SP
        dblPV=self.getProcessVarn(MonitorChannel)
        intTime=0
        dblDeltaT=abs(dblSP-dblPV)
        while intTime<=300 and dblDeltaT>0.3:
            dblDeltaT=abs(dblSP-dblPV)
            time.sleep(1)
            intTime=intTime+1
            dblPV=self.getProcessVarn(MonitorChannel)
            print dblSP,dblPV
            ##self.__updateStatus( 'Oven SP ='+ dblSP + 'Oven T=' + dblPV)
            time.sleep(1)
            
        if dblDeltaT<=0.3:
            return 1
        else:
            return 0
        
class NewportTEC(Base):
    ' TEC controller'

    def __init__(self, board=0, pad=2):
        Base.__init__(self, board, pad)
        self.__lstModes = ['T', 'ITE', 'R']

    def __repr__(self):
        s = 'Description: NewPort TEC controller\n'
        s += Base.__repr__(self)
        return(s)


    def waitForTolerance(self, fltTimeout = 180.0):
        self.enable()
        fltTimeStart = time.time()
        while (time.time() - fltTimeStart) < fltTimeout:
            if self.pollOPC():
                break
            else:
                time.sleep(0.25)
        else:
            raise InstrumentException('Timeout (%0.2f s) waiting for Newport TEC to return OPC after enabling TEC' % fltTimeout)
    
    def getToleranceValue(self):
        return self.getTolerances()[0]
    def setToleranceValue(self, fltValue):
        strCmd = 'TEC:TOL %f, %f' % (fltValue, self.getToleranceTimeWindow())
        self.write(strCmd)

    def pollOPC(self):
        self.write('*OPC')
        nStatus = int( self.query('*ESR?').strip() )
        return nStatus & 1
    
    def getToleranceTimeWindow(self):
        return self.getTolerances()[1]
    def setToleranceTimeWindow(self, fltTimeWindow):
        strCmd = 'TEC:TOL %f, %f' % (self.getToleranceValue(), fltTimeWindow)
        self.write(strCmd)
        
    def getTolerances(self):
        strResp = self.query('TEC:TOL?').strip()
        return map( float, strResp.split(',') )
    def setTolerances(self, fltValue, fltTimeWindow):
        strCmd = 'TEC:TOL %f, %f' % (fltValue, fltTimeWindow)
        self.write(strCmd)
    
        
    def isEnabled(self):
        #print ("Device", self.device)
        #self.device = ibdev(self.board, self.pad, 0, T1s, 1, 0)
        #print ("Device", self.device)
        strResp = self.query('TEC:OUT?')
        
        s = float(strResp)
        if s == 0 : return 0
        else : return 1

    def getTemperature(self):
        strResp = self.query('TEC:T?')
        try:
            return float(strResp)
        except:
            print 'TEC temperature read=',strResp
            return -100000
        
    def getCurrent(self):
        strResp = self.query('TEC:ITE?')
        return float(strResp)
    
    def getVoltage(self):
        strResp = self.query('TEC:V?')
        return float(strResp)

    def getTargetTemperature(self):
        strResp = self.query('TEC:SET:T?')
        return float(strResp)

    def setTargetTemperature(self,temp):        
        strCmd= 'TEC:T '+ str(temp)
        self.write(strCmd)

    def setCurrentLimit(self, curLimit):
        strCmd = 'TEC:LIM:ITE '+ str(curLimit)
        self.write(strCmd)

    def setTemperatureHighLimit(self, tempLimit):
        strCmd = 'TEC:LIM:THI '+ str(tempLimit)
        self.write(strCmd)

    def setTemperatureLowLimit(self, tempLimit):
        strCmd = 'TEC:LIM:TLO '+ str(tempLimit)
        self.write(strCmd)        
        
        
    def enable(self):
        self.write('TEC:OUT 1')
    enableTEC = enable
    EnableTEC = enable
    def disable(self):
        self.write('TEC:OUT 0')
    disableTEC = disable
    DisableTEC = disable

    def setSensorType(self, nType = 4):
        '''
        Sets the sensor type.  default is 4, AD590
        AD590 is the type used by TTx line and ITLA line.
        0 = None
        1 = Thermistor at 100 uA drive
        2 = Thermistor at 10  uA drive
        3 = LM335
        4 = AD590
        5 = RTD
        '''        
        strCmd = 'TEC:SEN %d' % nType
        self.write(strCmd)
    def getSensorType(self):
        strCmd = 'TEC:SEN?'
        return int(self.query(strCmd))
    def getSensorDescription(self):
        nType = self.getSensorType()
        lstType = ['None',
                   'Thermistor at 100 uA drive',
                   'Thermistor at 10 uA drive',
                   'LM335', 'AD590', 'RTD']
        return lstType[nType]
    def setGain(self, nGain = 100, nSpeed = 1):
        lstSpeed = ['S', 'F']
        strCmd = 'TEC:GAIN %d%s' % (nGain, lstSpeed[nSpeed])
        self.write(strCmd)
    def setMode(self, nMode = 0):
        '''
        sets the tracking mode of the TEC
        0 = Constant T
        1 = constant ITE
        2 = constant R
        '''        
        strCmd = 'TEC:MODE:%s' % self.__lstModes[nMode]
        self.write(strCmd)
    
    def setConstantT(self):
        self.setMode()
    
        


    
                
 


