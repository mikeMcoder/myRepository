'''
NeoPhotonics CONFIDENTIAL
Copyright 2005-2015 NeoPhotonics Corporation All Rights Reserved.

The source code contained or described herein and all documents related to
the source code ("Material") are owned by NeoPhotonics Corporation or its
suppliers or licensors. Title to the Material remains with NeoPhotonics Corporation
or its suppliers and licensors. The Material may contain trade secrets and
proprietary and confidential information of NeoPhotonics Corporation and its
suppliers and licensors, and is protected by worldwide copyright and trade
secret laws and treat provisions. No part of the Material may be used, copied,
reproduced, modified, published, uploaded, posted, transmitted, distributed,
or disclosed in any way without NeoPhotonics's prior express written permission. 
No license under any patent, copyright, trade secret or other intellectual
property right is granted to or conferred upon you by disclosure or delivery
of the Materials, either expressly, by implication, inducement, estoppel or
otherwise. Any license under such intellectual property rights must be express
and approved by NeoPhotonics in writing.

Include any supplier copyright notices as supplier requires NeoPhotonics to use.

Include supplier trademarks or logos as supplier requires NeoPhotonics to use,
preceded by an asterisk. An asterisked footnote can be added as follows:
*Third Party trademarks are the property of their respective owners.

Unless otherwise agreed by NeoPhotonics in writing, you may not remove or alter this
notice or any other notice embedded in Materials by NeoPhotonics or NeoPhotonics's
suppliers or licensors in any way.
'''
import os
import sys
#if (os.name != 'posix'):
#    import win32ui
#if (sys.hexversion > 0x02060000):
#    import datetime
#    import collections
import serial
import struct
import time
#import types
import operator
import re
import copy
from enum import Enum
from json import encoder
import math
import numpy as np
import signal

if sys.hexversion > 0x02060000:
    import bz2

import Register
from Packet import HostBoundPacket
from Packet import ModuleBoundPacket

TOGGLE_MS_BAUD = 0          # 0=disable else baud: 9600
RX_TIMEOUT_DEFAULT = 0.05
RX_TIMEOUT_UPGRADE = 0.30
RX_TIMEOUT_UPGRADE_EAR = 0.06
REBOOT_TIME = 1.0             # FW reboot time in seconds

PZT_BIT = 0
SIB_TRACK_BIT = 1
POWER_ADJ_BIT = 2
REG_22V_BIT = 3
ADC_CLK_BIT = 4
IDAC_CLR_BIT = 5
    
LASERHWDICT = { 1:'Huawei uITLA',
            	2:'Single uITLA',
            	3:'Dual uITLA',
            	5:'Single nITLA',
            	7:'ACE uITLA',
            	9:'Gold Box' }

encoder.FLOAT_REPR = lambda o: '%g.0' % o if '.' not in '%g' % o and 'e' not in '%g' % o and not np.isnan(o) else '%.7g' % o


def version():
    versionfilename = 'notrack/ECLuITLA_gitid.txt'
    if os.path.isfile(versionfilename):
        f = open(versionfilename)
        verstr = f.readlines()[0].strip()
        f.close()
        return(verstr)
    else:
        return ' *** Unknown Version *** '

class StackMarker:
    __depth = 0
    def __init__(self, name):
        self._name = name
        print '=' * (self._depth * 4), 'Enter function =>', name
        self._depth += 1
    def __del__(self):
        print '=' * (self._depth * 4), 'Exit function =>', self._name
        self._depth -= 1

class DelayedKeyboardInterrupt(object):
    def __enter__(self):
        self.signal_received = False
        self.old_handler = signal.signal(signal.SIGINT, self.handler)

    def handler(self, sig, frame):
        sys.stderr.write('Delaying keyboard interrupt...') 
        sys.stderr.flush() 
        self.signal_received = (sig, frame)

    def __exit__(self, type, value, traceback):
        signal.signal(signal.SIGINT, self.old_handler)
        if self.signal_received:
            sys.stderr.write('...done\n') 
            sys.stderr.flush() 
            self.old_handler(*self.signal_received)

def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

class ITLA:
    '''
    DEBUG_NONE                  = 0
    DEBUG_MODULE_BOUND_REGISTER = 1 << 0
    DEBUG_HOST_BOUND_REGISTER   = 1 << 1
    DEBUG_REGISTER              = 3 << 0
    DEBUG_MODULE_BOUND_PACKET   = 1 << 2
    DEBUG_HOST_BOUND_PACKET     = 1 << 3
    DEBUG_PACKET                = 3 << 2
    DEBUG_FUNCTION              = 1 << 4
    DEBUG_PACKET_STRING         = 1 << 5
    '''

    class formatted:
        """ """

        def __init__(self):
            self._ignored = []
            self._width=35
            self._columns = 1

        def __repr__(self):
            returnval = []
            varstoreport = [a for a in dir(self) if not a.startswith('_') and not a in self._ignored]
            if len(varstoreport) == 0:
                return ''
            padding = len(max(varstoreport, key=len))
            for varname in varstoreport:
                if isinstance(getattr(self, varname), Enum):
                    strout = getattr(self, varname).name
                if isinstance(getattr(self, varname), float):
                    strout = encoder.FLOAT_REPR(getattr(self, varname))
                else:
                    strout = str(getattr(self, varname))
                returnval.append(' '.join([varname.rjust(padding), '=', strout]))
            retval2 = []
            if self._columns == 2:
                for v, w in zip(returnval[0:int(math.ceil(len(returnval) / 2.0))],
                                returnval[int(math.ceil(len(returnval) / 2.0)):] + ['']):
                    retval2.append(' '.join([v.ljust(self._width), w]))
            else:
                retval2 = returnval
                
            return('\n'.join(retval2))
            

        def __eq__(self, other):
            dict1 = dict((k, v.real) for (k, v) in self.__dict__.iteritems() if not k.startswith('_'))
            dict2 = dict((k, v.real) for (k, v) in other.__dict__.iteritems() if not k.startswith('_'))
            if dict1.keys() != dict1.keys():
                return False
            for (name, value) in dict1.iteritems():
                if not np.isclose(value.real, dict2[name], atol=0):
                    return False
            return True

        def __cmp__(self, other): 
            return self.__eq__(other)

    def __init__(self, t_object = None):
        #print 'Version:', version()
        self._register = None
        self._baud = 0
        self._port = 0
        self._timeout = RX_TIMEOUT_DEFAULT
        self._print_once = 1
        self._link = None
        self._packet = None
        self._module_packet = None
        self._debug_level = 0
        self._debug_rs232 = 0
        self._laserSelect = 0
        self._t_object = t_object
        self._OIFlogging = False
        self._droppedbytecount = 0
        self._retrying = False
        self._inTMode = False
        self._LaserType = None
        self._hwname = None
        self._boardid = ''
        self._dummyx99data = None # bit of a hack to try to get readx99() to return an object with the right attributes even when there is an OIF error

        if (os.name == 'posix'):
            #self._commslogfilename = os.path.expanduser("~/commslog_port" + str(self._port) + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3] + ".txt")
            self._commslogfilename = os.path.expanduser("~/commslog_port" + str(self._port) + "_" + 
                time.asctime().replace(" ", "_").replace(':','-') + ".txt")
            self._portprefix = '/dev/ttyS'
            self._gettime = time.time
        else:
            self._commslogfilename = "commslog_port" + str(self._port) + "_"
            self._commslogfilename +=  time.asctime().replace(" ", "_").replace(':','-')
            self._commslogfilename += ".txt"
            self._portprefix = 'com'
            self._gettime = time.clock
            
        if self._t_object is not None:
            if hasattr( self._t_object, 'it'):
                if self._t_object.it is not None:
                    self._t_object.it = self
                else:
                    print 't.it is none'

        self._logstarttime = self._gettime()


    def setupFromTMode(self,tMode = False):
        if tMode==True and self._t_object is not None:
            self._inTMode = True
            self._link = self._t_object._link
        else:
            self._inTMode = False
            self._link = None
            
##    def __del__(self):
##        self.disconnect()

    def __repr__(self):
        msg  = 'Description : ITLA\n'
        msg += 'Port        : %i\n' % (self._port)
        msg += 'Baud        : %i\n' % (self._baud)
        msg += 'OIF Logging : %r\n' % (self._OIFlogging)
        msg += 'Log File    : %s' % (self._commslogfilename)

        return msg

    def hilite(self,string, status, bold):
        if (not 'TERM' in os.environ):
            return(string)
        attr = []
        if status:
            # green
            attr.append('32')
        else:
            # red
            attr.append('31')
        if bold:
            attr.append('1')
        return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)

    def getport(self):
        return(self._port)

    def getdroppedbytecount(self):
        return(self._droppedbytecount)

    def cleardroppedbytecount(self):
        print 'Clearing dropped byte count'
        self._droppedbytecount = 0
        return(self._droppedbytecount)

    def getlogfilename(self):
        return(self._commslogfilename)

    def logging(self,OIFlogging = None):
        if OIFlogging is None:
            print 'OIF Logging : %r' % (self._OIFlogging)
            print 'Log File    : %s' % (self._commslogfilename)
            return
        else:
            self._OIFlogging = OIFlogging
            if (self._OIFlogging):
                try:
                    oiflogfile=open(self._commslogfilename,"a")
                    self._logstarttime = self._gettime()
                    oiflogfile.write("# logging started " + time.asctime() + "\n")
                    oiflogfile.flush()
                except OSError:
                    print "Unable to open logfile", self._commslogfilename
                    self._OIFlogging = False
                    return

    def logfile(self,logfilename=None):
        if (logfilename is None):
            print 'OIF Logging : %r' % (self._OIFlogging)
            print 'Log File    : %s' % (self._commslogfilename)
            return self._commslogfilename
        loggingtimestring = time.asctime()
        if logfilename is None:
            if (os.name != 'posix'):
                self._commslogfilename = "commslog_port" + str(self._port) + "_" + time.asctime().replace(" ", "_").replace(':','-') + ".txt"
            else:
                self._commslogfilename = os.path.expanduser("~/commslog_port" + str(self._port) + "_" + 
                            time.asctime().replace(" ", "_").replace(':','-') + ".txt")

            logfilename = os.path.expanduser("~/commslog_" + loggingtimestring + ".txt")
        self._commslogfilename=logfilename
        print 'OIF Logging : %r' % (self._OIFlogging)
        print 'Log File    : %s' % (self._commslogfilename)
        return(self._commslogfilename)         
   
    def compresslog(self):
        if sys.hexversion > 0x02060000:
            bz2filename = self._commslogfilename.replace('.txt','.txt.bz2')
            if not os.path.isfile(self._commslogfilename):
                print "No comms log file to compress"
                return
            if os.path.isfile(bz2filename):
                print "zipped file exists, not overwriting" # todo: append
                return
            print 'Compressing',self._commslogfilename,'->',bz2filename
            outfile = bz2.BZ2File(bz2filename,'bw')
            outfile.write(open(self._commslogfilename,'r').read())
            outfile.close()
            os.remove(self._commslogfilename)  # danger: sanitize
        else:
            print 'Log compression not supported in this version of python'

    def _setx84bit(self, origval, bit, state):
        if (state):
            return self.register(Register.Register(address=0x84,data=origval | (1 << bit) ),write=True)
        else:
            return self.register(Register.Register(address=0x84,data=origval & ~ (1 << bit) ),write=True)

    def _x84bit(self, bit, state):
        x84_data = self.register(Register.Register(address=0x84,data=0x0000),write=False)
        if x84_data[0] != 'OK':
            print 'Error: Please set password!'
            return x84_data
        if state == None:
            if (x84_data[1].data() & (1<<bit)) != 0:
                return 'OK', 1
            return 'OK', 0
        return self._setx84bit(x84_data[1].data(), bit, state)
    
    def x84_pztState(self, state=None):
        return self._x84bit(PZT_BIT, state)
            
    def x84_siBTrackState(self, state=None):
        return self._x84bit(SIB_TRACK_BIT, state)
            
    def x84_pwrAdjState(self, state=None):
        return self._x84bit(POWER_ADJ_BIT, state)
            
    def x84_reg22State(self, state=None):
        return self._x84bit(REG_22V_BIT, state)
            
    def x84_adcClkState(self, state=None):
        return self._x84bit(ADC_CLK_BIT, state)
    
    def x84_GMI_State(self, state=None):
        return self._x84bit(IDAC_CLR_BIT, state)
            
    def readx99(self):
        if self._inTMode==True:
            print 'In t mode, readx99 not working'
            return
        with DelayedKeyboardInterrupt():
            self.writedatanoreply(Register.Register(address=0x99,data=0x1234),write=False)
            dataformatraw = self.read(1, maxRetry=3, incomplete=True)
            if len(dataformatraw) == 1:
                dataformat = ord(dataformatraw)
                databytes = ord(self.read(1,beginning=False,incomplete=True))
            else:
                print 'No reply'
                return(self._dummyx99data)
            if (databytes == 0x99):
                self.read(2)
                print "x99 Error: Password not set?"
                return(self._dummyx99data)
            
            if dataformat == 2:
                datastructure = [
                    ["L","stateflags"          ,"" ],
                    ["f","f1temp"              ,"degC" ],
                    ["f","f2temp"              ,"degC" ],
                    ["f","siblocktemp"         ,"degC" ],
                    ["f","N5Volts"             ,"V" ],
                    ["f","demodrealerr"        ,"" ],
                    ["f","tmpdebug"            ,"" ],
                    ["L","tmpdebugU32"         ,"" ],
                    ["f","df1"                 ,"degC" ],
                    ["f","df2"                 ,"degC" ],
                    ["f","filter1_power"       ,"" ],
                    ["f","filter2_power"       ,"" ],
                    ["f","sled_current"        ,"mA" ],
                    ["f","photodiode_current"  ,"uA" ],
                    ["f","sled_temperature"    ,"degC" ],
                    ["f","gain_medium_current" ,"mA" ]
                ] 
            elif dataformat == 3 or dataformat == 4: # v3 reports sled_current from control, v4 reports from domain
                datastructure = [
                    ["L","stateflags"          ,"" ],
                    ["f","f1temp"              ,"degC" ],
                    ["f","f2temp"              ,"degC" ],
                    ["f","siblocktemp"         ,"degC" ],
                    ["f","N5Volts"             ,"V" ],
                    ["f","demodrealerr"        ,"" ],
                    ["f","tmpdebug"            ,"" ],
                    ["L","tmpdebugU32"         ,"" ],
                    ["L","tmpdebugU32_2"       ,"" ],
                    ["f","df1"                 ,"degC" ],
                    ["f","df2"                 ,"degC" ],
                    ["f","filter1_power"       ,"W" ],
                    ["f","filter2_power"       ,"W" ],
                    ["f","sled_current"        ,"mA" ],
                    ["f","photodiode_current"  ,"uA" ],
                    ["f","sled_temperature"    ,"degC" ],
                    ["f","gain_medium_current" ,"mA" ]
                ]
            elif dataformat == 6: # v3 reports sled_current from control, v4 reports from domain
                datastructure = [
                    ["L","stateflags"          ,"" ],
                    ["f","f1temp"              ,"degC" ],
                    ["f","f2temp"              ,"degC" ],
                    ["f","siblocktemp"         ,"degC" ],
                    ["f","reg22V"              ,"V" ],
                    ["f","demodrealerr"        ,"" ],
                    ["f","tmpdebug"            ,"" ],
                    ["L","tmpdebugU32"         ,"" ],
                    ["L","tmpdebugU32_2"       ,"" ],
                    ["f","df1"                 ,"degC" ],
                    ["f","df2"                 ,"degC" ],
                    ["f","filter1_power"       ,"W" ],
                    ["f","filter2_power"       ,"W" ],
                    ["f","sled_current"        ,"mA" ],
                    ["f","photodiode_current"  ,"uA" ],
                    ["f","sled_temperature"    ,"degC" ],
                    ["f","gain_medium_current" ,"mA" ]
                ]  
            elif dataformat == 7: 
                datastructure = [
                    ["L","stateflags"          ,"" ],
                    ["f","f1temp"              ,"degC" ],
                    ["f","f2temp"              ,"degC" ],
                    ["f","siblocktemp"         ,"degC" ],
                    ["f","reg22V"              ,"V" ],
                    ["f","demodrealerr"        ,"" ],
                    ["f","tmpdebug"            ,"" ],
                    ["L","tmpdebugU32"         ,"" ],
                    ["L","tmpdebugU32_2"       ,"" ],
                    ["f","df1"                 ,"degC" ],
                    ["f","df2"                 ,"degC" ],
                    ["f","filter1_power"       ,"W" ],
                    ["f","filter2_power"       ,"W" ],
                    ["f","sled_current"        ,"mA" ],
                    ["f","photodiode_current"  ,"uA" ],
                    ["f","sled_temperature"    ,"degC" ],
                    ["f","gain_medium_current" ,"mA" ],
                    ["f","sled_current_set"    ,"" ],
                    ["f","caseT"               ,"degC" ],
                    ["f","Vcc"                 ,"V" ],
                ]
                if self._LaserType is not None:
                    if self._LaserType != 5:
                        datastructure[4][1] = 'N5Volts'
                        
            else:
                self.read(databytes,beginning=False)
                print "x99 Error: unrecognized data format"
                return(self._dummyx99data)
            
            if (databytes != len(datastructure)*4):
                self.read(databytes,beginning=False)
                print "x99 Error: incorrect data structure"
                return(self._dummyx99data)
                
            
            tunerstates = [
                [0,"TUNER_COLD_START"],
                [1,"TUNER_IDLE"],
                [2,"TUNER_DARK"],
                [3,"TUNER_TEMPERATURE"],
                [4,"TUNER_GAIN_MEDIUM"],
                [5,"TUNER_ADJUSTMENT"],
                [6,"TUNER_FIRST_LIGHT"],
                [7,"TUNER_CAVITY_LOCK"],
                [8,"TUNER_POWER_LEVEL"],
                [9,"TUNER_CAVITY_OFFSET_LOCK"],
                [10,"TUNER_STABILIZE"],
                [11,"TUNER_CHANNEL_LOCK"],
                [12,"TUNER_FINE_TUNE"],
                [13,"TUNER_MZM_STATE"]
            ]
      
            statebits = [
                [4,"tunerpending"],
                [5,"MRDY"],
                [6,"freqofflocked"],
                [7,"powerlocked"],
                [8,"f1locked"],
                [9,"f2locked"],
                [10,"siblocklocked"],
                [11,"sledlocked"],
                [12,"powertune"],
                [16,"healthSDF"],
                [17,"powermask"],
                [18,"systemmask"],
                [19,"tunermask"],
                [20,"flashfreeze"],
                [21,"bCavityLocked"],
                [22,"SMB"],
                [23,"NOPpending"],
                [24,"alarms"],
                [25,"alarmslatched"],
                [26,"hw_error"],
            ]	
        
            class x99:
                def __repr__(self):   
                    returnval=[]
                    padding = len(max([a for a in dir(self) if not a.startswith('_')] + map(operator.itemgetter(1),datastructure),key=len))
                    for vartype,varname,units in datastructure:
                        if varname not in ['stateflags','tmpdebug','tmpdebugU32','tmpdebugU32_2']:
                            returnval.append( ' '.join([varname.rjust(padding),'=',self._valtostr(getattr(self, varname)),units]) )
                    for statebit,varname in statebits:
                        returnval.append( ' '.join([varname.rjust(padding),'=',str(getattr(self,varname))]))
                    for varname in [a for a in dir(self) if not a.startswith('_') and 
                               not a in map(operator.itemgetter(1),datastructure) and 
                               not a in map(operator.itemgetter(1),statebits) and 
                               not a in ['stateflags','tmpdebug','tmpdebugU32','tmpdebugU32_2']]:
                        returnval.append( ' '.join([varname.rjust(padding),'=',self._valtostr(getattr(self, varname))]) )
                    #return(''.join(returnval))
                    retval2 = []
                    for v, w in zip(returnval[0:int(math.ceil(len(returnval) / 2.0))],
                                    returnval[int(math.ceil(len(returnval) / 2.0)):] + ['']):
                        retval2.append(' '.join([v.ljust(39), w]))
                    #returnval.append( 'tunerstate'.rjust(padding)+ ' = ' + self.tunerstate )
                    return('x99data format v'+str(dataformat)+':\n'+'\n'.join(retval2))
    
                def _valtostr(self,o):
                    if isinstance(o, float):
                        return '%g.0' % o if '.' not in '%g' % o and 'e' not in '%g' % o and not np.isnan(o) else '%g' % o
                    else:
                        return str(o)
    
            x99dat = x99()
            
            for vartype,varname,units in datastructure:
                rawdata=self.read(4,beginning=False,incomplete=(varname != datastructure[-1][1]))
                decodeddata = struct.unpack('>' + vartype,rawdata)[0]
                setattr(x99dat, varname, decodeddata)
    
            for statebit,varname in statebits:
                setattr(x99dat, varname, (x99dat.stateflags & (1 << statebit)) !=0 )  
    
            x99dat.tunerstate = tunerstates[ x99dat.stateflags & 0x0F ][1]
                    
            if (self._dummyx99data is None):
                self._dummyx99data = copy.deepcopy(x99dat)
                for varname in [a for a in dir(self._dummyx99data) if not a.startswith('__')]:
                    setattr(self._dummyx99data, varname, None)
    
            return(x99dat)

    def getdummyx99dat(self):
        return self._dummyx99data

    def setpassword(self,passwordlevel=3):
        passwords = [0x0000,0x0209,0xEE75,0xC3B2,0x632A,0xB5F1]
        for i in range(0,passwordlevel+1):
            level=self.register(Register.Register(address=0x99,data=passwords[i]),write=True)
        if (level[0] == 'OK'):
            print "Password level",level[1].data()
        else:
            print 'Unable to set password' 

    def manufacturingMode(self, enable = 1, readOnly=0):
        if self._LaserType != 5:
            return
        passwords = [0x4572,0x6963]
        if (readOnly == 1):
            if(self.register(Register.Register(address=0x63,data=0xDEAD),write=False)[1].data()!=1):
                print 'Manufacturing Mode Disabled.' 
            else:
                print 'Manufacturing Mode Enabled.' 
            return
            
        if (enable==1):
            for i in range(0,len(passwords)):
                level=self.register(Register.Register(address=0x63,data=passwords[i]),write=True)
            if (level[1].data() == 1):
                print "Manufacturing Mode Enabled."
            else:
                print 'Unable to set manufacturing mode.' 
        else:
            if(self.register(Register.Register(address=0x63,data=0xDEAD),write=True)[1].data()!=1):
                print 'Manufacturing Mode Disabled.' 
            else:
                print 'Unable to disable Manufacturing Mode.'

    def detect(self):
        self.write('\x00\x00\x00\x00')           # bit26=0
        st = self.read(4)
        if (len(st) == 4) and (ord(st[0]) & 0x40) == 0:
            if self.laser() == 0:
                self.laser(1)   # dual, make it laser 1
            print 'dual laser detected'
            return(2)
        else:                   # single or goldBox
            self.laser(0)       
            status, NA = self.dbgACR()
            if status == 'OK':
                print 'goldBox detected'
                return(1)
            else:
                print 'uitla detected'
        return(0)

    def _connect(self, port = 1, baud = 9600, RXtimeout = None, **kwargs):

        synccalmap = kwargs.get('synccalmap')
        retrievekvfile = kwargs.get('retrievekvfile')
        timeout = kwargs.get('timeout')
        
        if synccalmap is None:
            synccalmap=True
        if retrievekvfile is None:
            retrievekvfile=True
        if RXtimeout is None:
            if timeout is None:
                RXtimeout = RX_TIMEOUT_DEFAULT
            else:
                RXtimeout = timeout

        self.disconnect()
        self._baud = baud
        self._port = port
        self._timeout = RXtimeout
        if (self._OIFlogging):
            # with open(self._commslogfilename, "a") as oiflogfile:
            oiflogfile = open(self._commslogfilename, "a")
            oiflogfile.write("# connecting to port " + str(port) + " at " + time.strftime("%a %d %b %Y %H:%M:%S %Z") + "\n")
            oiflogfile.flush()
#        else:
#            if self._print_once:
#                self._print_once = 0
#                print self.hilite("Warning: Not logging OIF transactions. Use\n it.logfile(<filename>) to set log filename and\n it.logging(True) to enable logging",False,True)
        
        try:
            if os.name == 'posix':
                self._port = "/dev/ttyS" + str(port)
#                self._port = "/dev/ttyUSB" + str(port)
            else:
                self._port = "com" + str(port)
            self._link = serial.Serial(self._port, baud, timeout = RXtimeout)
        except:
            raise 'Port unavailable'
            
    def setportprefix(self, portprefix = None):  # usually 'com', '/dev/ttyS', or '/dev/ttyUSB'
        if portprefix is None:
            return(self._portprefix)
        else:
            self._portprefix = portprefix

    def connect(self, port = 1, baud = 9600, timeout = RX_TIMEOUT_DEFAULT, **kwargs):

        synccalmap = kwargs.get('synccalmap')
        retrievekvfile = kwargs.get('retrievekvfile')
        
        if synccalmap is None:
            synccalmap=True
        if retrievekvfile is None:
            retrievekvfile=True
        
        global t        
        if '..' not in sys.path:
            sys.path.append("..")
        import LSR.LSRcontrol

        if sys.modules['__main__'].__dict__.get('t',None) is None: 

            lsr = LSR.LSRcontrol.LSRcontrol(it=self)

            sys.modules['__main__'].__dict__['lsr']   = lsr
            sys.modules['__main__'].__dict__['t']    = lsr.t
        else:
            lsr = LSR.LSRcontrol.LSRcontrol(it = self, t = sys.modules['__main__'].__dict__['t'] )
            sys.modules['__main__'].__dict__['lsr']   = lsr
            
        retval = lsr.connect(port=port, baud=baud, timeout=timeout, synccalmap=synccalmap)
        self._link = lsr._ttyhandle
        lsr.t.save_handle(lsr._ttyhandle)
        if lsr.it.getLaserType() != 5:
            lsr.t.tmode(mode=0)
        return retval

        
    def sync(self):
        'sync with port'
        self.reset()
        
    def flushBuffer(self):
        try:
            #read a large number of bytes without keeping the result
            self.read(0xFFFF)
        except:
            pass
        return

    def _getSerialHandle(self):
        return self._link
    
    def save_handle(self, t_param):
        if self._t_object is not None:
            self._t_object._link = t_param
        self._link = t_param

    def save_t_obj(self, t_param):
        self._t_object = t_param

    def debugRS232(self, level = None):
        'Get/Set debug level'
        if level != None:
            self._debug_rs232 = level
        return self._debug_rs232
    
    def laser(self, level = None):
        'Get/Set debug level'
        if level != None:
            self._laserSelect = level
        return self._laserSelect
    
    def toModulePacket(self):
        'Return last packet sent to module'
        return self._module_packet
    
    def writedatanoreply(self, register = None, write = 0):
        packet = ModuleBoundPacket()
        if write:
            packet.mode('WRITE')
        if self.laser() == 2:
            packet.laser('LASER1')      # laser 2 set bit 26
        else:
            packet.laser('LASER0')      # 0 or 1 clear bit 26
        packet.register(register.address())
        packet.data(register.data())
        packet.checksum(packet.computedChecksum())
        self.write(packet.buffer())

    def register(self, register = None, write = 0):
        'Get last register sent or set register, return (status_string, register)'
        status = 'OK'
        if register != None:
            packet = ModuleBoundPacket()
            if write:
                packet.mode('WRITE')
            if self.laser() == 2:
                packet.laser('LASER1')      # laser 2 set bit 26
            else:
                packet.laser('LASER0')      # 0 or 1 clear bit 26
            packet.register(register.address())
            packet.data(register.data())
            Max_RXretry = 1
            if (register.address() == Register.DLCONFIG):
                Max_RXretry = RX_TIMEOUT_UPGRADE / self._timeout
            if (register.address() == Register.EAR):
                Max_RXretry = RX_TIMEOUT_UPGRADE_EAR / self._timeout

            p = self.packet(packet, RXretries = Max_RXretry)
            if p == None:      # check for a complete response
                status = 'No response'
                return (status, self._register)

            address = ord(p.buffer()[1])
            data = struct.unpack('>H', p.buffer()[2:])[0]
            self._register = Register.Register(address, data)

            #if self._debug_level & ITLA.DEBUG_HOST_BOUND_REGISTER:
            #    print '%s Mode = %s, To Host Register %s' % ('-' * 24, packet.mode(), '-' * 24)
            #    print self._register

            if p.communicationError() == 'TRUE':
                status = 'Communication error'
            elif p.computedChecksum() != p.checksum():
                status = 'Checksum error (expected 0x%X, received 0x%X)' % (p.computedChecksum(), p.checksum())
            elif register.address() != address:
                status = 'Register address mismatched'
            #elif (self.laser() == 2) and not(ord(p.buffer()[1]) & 64):
            #    status = 'Bit26 not set'        #pb used for dual
            else:
                status = p.status()
                
        return (status, self._register)

    def write(self, buffer):
        # needs a way to flush to eleminates leftover of previous commands
        #self.flushBuffer()
        self._link.flushInput()
        if (self._OIFlogging):
            oiflogfile = open(self._commslogfilename, "a")
            oiflogfile.write("%04.6fs " % (self._gettime() - self._logstarttime))
            oiflogfile.write('Tx: ')
            for c in buffer:
                oiflogfile.write( '%02X ' % ord(c) )
            oiflogfile.flush()
        if self._debug_rs232 !=0:
            print 'Tx:',
            for c in buffer:
                print '%02X' % ord(c), 
        self._lastwritetime = self._gettime()
        return self._link.write(buffer)
        
    def read(self, byte_count = 1, maxRetry = 1, beginning=True, incomplete=False): # call with maxRetry=0 to do a dummy read (for log file completeness)
        if byte_count == 0xFFFF:
            return self._link.read(byte_count)         # flushBuffer()
            
        retries = 0
        string = ''
        writetimems = (self._gettime() - self._lastwritetime) * 1000 # dummy value
        while(retries < maxRetry):
            string += self._link.read(byte_count)
            writetimems = (self._gettime() - self._lastwritetime) * 1000
            if (len(string) >= byte_count):
                if self._debug_rs232 !=0:
                    print ' Rx:',
                    for c in string:
                        print '%02X' % ord(c), 
                    if retries:
                        print 'RD reties:', retries, 'max:',maxRetry 
                    else:
                        print ""    # CR/LF
                if (self._OIFlogging):
                    oiflogfile = open(self._commslogfilename, "a")
                    if beginning:
                        oiflogfile.write('Rx: ')
                    for c in string:
                        oiflogfile.write( '%02X ' % ord(c) )
                    if not incomplete:
                        oiflogfile.write('%2.3fms\n' % writetimems)
                    oiflogfile.flush()
                return string
            retries += 1
        if (self._OIFlogging):
            oiflogfile = open(self._commslogfilename, "a")
            if beginning:
                oiflogfile.write('Rx: ')
                oiflogfile.write( 'NA ' * (byte_count - len(string)) )
            if not incomplete:
                oiflogfile.write('%2.3fms\n' % writetimems)
            oiflogfile.flush()
        if maxRetry > 0:
            print 'Expected %d bytes, got %d' % (byte_count, len(string))
            self._droppedbytecount += byte_count - len(string)
        return string
    
    def printlog( self, lines = 20 ):
        try:
            f = open(self._commslogfilename, "r")
        except:
            if (not self._OIFlogging):
                print "Unable to open logfile (and logging is not enabled)"
            else:
                print "Unable to open logfile:", sys.exc_info()[0]
            return
        if sys.hexversion > 0x02060000: # temporary fix (disable) for this failing in python 2.2
            f.seek(0, 2)
            endbyte = f.tell()
            lines_to_go = lines
            blocknum = -1
            blocks = []
            while lines_to_go > 0 and endbyte > 0:
                if (endbyte - 1024 > 0):
                    f.seek(blocknum*1024, 2)
                    blocks.append(f.read(1024))
                else:
                    f.seek(0,0)
                    blocks.append(f.read(endbyte))
                lines_found = blocks[-1].count('\n')
                lines_to_go -= lines_found
                endbyte -= 1024
                blocknum -= 1
            all_read_text = ''.join(reversed(blocks))
            print "Log file: " + self._commslogfilename
            print "Showing last",lines,"lines:"
            print '\n'.join(all_read_text.splitlines()[-lines:])
        else:
            print 'Log print not supported in this version of python'


    def moduleSelect(self):
        'Toggle the module select line'
        self._link.setRTS(0)
        self._link.setRTS(1)
    
    def reset(self):
        'Resynchronize the transmit and receive buffer'
        print 'Flushing RS232 Buffers'
        self._link.flushInput()
        for i in range(5):
            self._lastwritetime = self._gettime()
            try:
                if (self._OIFlogging): # dummy blank 4-byte write
                    oiflogfile = open(self._commslogfilename, "a")
                    oiflogfile.write("%04.6fs " % (self._gettime() - self._logstarttime))
                    oiflogfile.write('Tx: ')
                    oiflogfile.write( 'NA ' * 4)
                    oiflogfile.flush()
                    time.sleep(0.001)
                self.read(0xFFFF)
                break
            except:
                time.sleep(0.001)
                pass
        
    def packet(self, packet = None, computeChecksum = 1, RXretries = 1, MS_baud = TOGGLE_MS_BAUD):
        'Send packet or return last packet received'
        if packet != None:
            if self.laser() == 2:	
                packet.laser('LASER1')      # laser 2 set bit 26
            else:
                packet.laser('LASER0')      # 0 or 1 clear bit 26

            if computeChecksum:
                packet.checksum(packet.computedChecksum())

            self._module_packet = packet
            
            if self._retrying:  # prevent retry recursion
                return None
            self._retrying = True
            # Retry if no answer
            for retry in range(3):
                if retry:
                    print 'retry',
                self.write(packet.buffer())
                self._packet = HostBoundPacket()
                string = self.read(4, maxRetry = RXretries)
                if len(string) >= 4: 
                    self._packet.buffer(string)
                    self._retrying = False
                    return self._packet
                if MS_baud :
                    print 'Toggling MS line'
                    oldbaud = self._baud
                    mstogglebaud = MS_baud
                    MS_baud = 0             # toggle once
                    self.logentry("Toggling MS line")
                    self.moduleSelect() 
                    if (mstogglebaud != oldbaud):
                        self._port.baudrate = oldbaud   # reset the baud
            self._retrying = False                
            return None

    ###############################################################
    # Complete commands which may combine multiple ITLA registers
    ###############################################################
    def nop(self):
        'Return tuple (status_string, register)'
        return self.register(Register.Register(Register.NOP))

    def nopStats(self):
        'Return tuple (status_string, register)'
        return self.register(Register.Register(Register.NOP_STATS))

    def dbgACR(self, offset=0, amplitud=0):
        'Return tuple (status_string, register)'
        value = ((amplitud & 0xF) << 12) | (offset & 0x0FFF)
        return self.register(Register.Register(Register.DBG_ACR, value))
        
    def dbgTemps(self, sel=0):
        'Return tuple (status_string, register)'
        return self.register(Register.Register(Register.DBG_TEMPS, sel))
        
    def isLocked(self, timeout = 25.0):
        'Query NOP until pending is cleared, timeout in seconds. Return (boolean, lock_time_in_seconds)'
        start = self._gettime()
        while True:
            #print 'checking', self._gettime() - start
            status, nop = self.nop()
            if nop.fieldPending().value() == 0:
                return True, self._gettime() - start
            if (self._gettime() - start) >= timeout:
                return False, timeout

    def aeaString(self, address):
        'Return tuple (byte_count, string)'
        register = Register.Register(address)
        status, response = self.register(register)
        if status != 'AEA':
            return status, (0, 'Error')
        
        if response.name() != register.name():
            return 'Register name mismatched (expected %s, received %s)' % (register.name(), response.name()), (0, 'Error')
        
        byteCount = response.data()

        status, response = self.register(Register.Register(Register.AEA_EA))
        if status != 'OK':
            return status, (1, 'Error')

        if response.data() == 0:
            return 'Invalid extended address', (0, 'Error')

        status, response = self.register(Register.Register(Register.AEA_EAC))
        if status != 'OK':
            return status, (2, 'Error')

        if response.fieldIncr().value() != 2 or response.fieldRai().value() != 1:
            return 'Extended address not configured', (0, 'Error')

        s = Register.Register(Register.AEA_EAR)
        message = ''
        odd = byteCount % 2
        for i in range(byteCount / 2):
            status, response = self.register(s)
            if status != 'OK':
                return status, (3, 'Error')
            word = response.data()
            message += struct.pack('BB', (word & 0xFF00) >> 8, word & 0xFF)
            
        if odd:
            status, response = self.register(s)
            if status != 'OK':
                return status, (4, 'Error')
            message += struct.pack('B', (response.data()>>8) & 0xFF)

        return status, (byteCount, message)
    
    def monitor(self, addr = 0x80A8):   # Monitor version 1.2.x or 2.1.x
        if addr == 0:
            addr = 0xB152               # Monitor version 1.1.0
        #Get Monitor 2 data bytes, 
        'Return tuple (status_string, register)'
        status, response = self.register(Register.Register(Register.MONITOR, addr))
        if status == 'OK':
            word = response.data()
            message = struct.pack('BB', (word & 0xFF00) >> 8, word & 0xFF)
            status, response = self.register(Register.Register(Register.MONITOR, addr+2))
            word = response.data()
            message += struct.pack('BB', (word & 0xFF00) >> 8, word & 0xFF)
        else:
            message = '\x00\x00\x00\x00'
        return status, (4, message)

    def i2c(self, addr=0):   # OC% I2C data
        'Return tuple (status_string, register)'
        status, response = self.register(Register.Register(Register.MONITOR, addr))
        if status == 'OK':
            word = response.data()
            word = ((word & 0xFF00) >> 8) | ((word & 0xFF) << 8)   #-> Big endian
            if addr==1:
                print 'VCC = %5.3f' % ((word * 2.4/0xFFFF)*4)
            else:
                print '0x%04X' % word
            return status, word
        return status, -1

    def devTyp(self):
        'Return tuple (status, (byte_count, string))'
        return self.aeaString(Register.DEVTYP)

    def mfgr(self):
        'Return tuple (status, (byte_count, string))'
        return self.aeaString(Register.MFGR)

    def model(self):
        'Return tuple (status, (byte_count, string))'
        return self.aeaString(Register.MODEL)
    
    def logentry(self,string=None):
        if (self._OIFlogging):
            oiflogfile = open(self._commslogfilename, "a")
            oiflogfile.write("# " + "%04.6fs: " % (self._gettime() - self._logstarttime) + string.encode('string-escape') + "\n")
            oiflogfile.flush()
        else:
#            if self._print_once:
#                self._print_once = 0
#                print self.hilite("Warning: Not logging OIF transactions. Use\n it.logfile(<filename>) to set log filename and\n it.logging(True) to enable logging",False,True)
            print 'Unable to write log entry', string
        return
        
    
    def serNo(self):
        'Return tuple (status, (byte_count, string))'
        serialnum = self.aeaString(Register.SERNO)
        if (self._OIFlogging):
            self.logentry("unit serial number: " + str(serialnum[1][1]) )
#        else:
#            if self._print_once:
#                self._print_once = 0
#                print self.hilite("Warning: Not logging OIF transactions. Use\n it.logfile(<filename>) to set log filename and\n it.logging(True) to enable logging",False,True)
        return serialnum
    
    def buildstring(self):
        buildstring = self.aeaString(0xB0)[1][1].split('\x00',1)[0]
        if (self._OIFlogging):
            self.logentry("FW build string: " + str(buildstring) )
#        else:
#            if self._print_once:
#                self._print_once = 0
#                print self.hilite("Warning: Not logging OIF transactions. Use\n it.logfile(<filename>) to set log filename and\n it.logging(True) to enable logging",False,True)
        return buildstring
    
#define HUAWEI_UITLA	1		
#define SINGLE_UITLA	2
#define DUAL_UITLA	    3
#define SINGLE_NANO	    5
#define ACE_UITLA	    7
#define GOLD_BOX	    9
    def laserDetect(self):
        UNKNOWN = 0
        self._LaserType = UNKNOWN;
        debug = None
        currLaser = self.laser(debug)      #1, 2 = dual, 0 = single
        
        if currLaser == 0:      # single laser
            try:
                buildStr = self.buildstring()

                if 'Build' not in buildStr:
                    error = 'Laser1 Not Connected!'
                    print error
                    return (UNKNOWN, error)   # error

                print buildStr
                
                productsearch = re.search('Product #([0-9]+) (.+?) ; (.+?) ;', buildStr + ';')
                                          
                if productsearch:
                    self._LaserType = int(productsearch.group(1))
                    self._legacyFWname = productsearch.group(2)
                    self._boardid = productsearch.group(3)
                    if self._boardid.count(' ') > 1:
                        self._boardid = ''
                    self._hwname = LASERHWDICT.get(self._LaserType, None) + ' ' + self._boardid
                else:
                    error = 'Missing Product number'
                    print error
                    return (UNKNOWN, error)   # error

                if self._hwname is None:
                    error = 'Illegal Product #'
                    print error
                    return (UNKNOWN, error)   # error

            except serial.SerialException as e:
                error = 'Not Connected! ' + e
                print error
                return (UNKNOWN, error)   # error

        print 'Connected to',self._hwname

                
        if currLaser >= 1:      # dual laser
            self.laser(1)
            time.sleep(0.1)
            try:
                buildStr = self.buildstring()
                if 'Build' not in buildStr:
                    return (UNKNOWN, 'Laser1 Not Connected!')   # error
            except:
                return (UNKNOWN, 'Laser1 Not Connected!')   # error

            self.laser(2)
            time.sleep(0.1)
            try:
                buildStr1 = self.buildstring()
            except:
                return (UNKNOWN, 'Laser2 Not Connected!')   # error
                
            self.laser(currLaser)
            if (buildStr == buildStr1):
                if "#3 " in buildStr:
                    print "Dual",
                else:
                    return (UNKNOWN, 'Dual bad versions')   # error
            else:
                return (UNKNOWN, 'Different versions')   # error

        if self._LaserType >= 0:
            return (self._LaserType, self._legacyFWname)   

        return (UNKNOWN, 'Bad version')                 # error
        
    def getLaserType(self):
        return self._LaserType

    def mfgDate(self):
        'Return tuple (status, (byte_count, string))'
        return self.aeaString(Register.MFGDATE)

    def release(self):
        'Return tuple (status, (byte_count, string))'
        return self.aeaString(Register.RELEASE)

    def relBack(self):
        'Return tuple (status, (byte_count, string))'
        return self.aeaString(Register.RELBACK)

    def aeaEac(self):
        'Return tuple (status, register)'
        command = Register.Register(Register.AEA_EAC)
        return self.register(command)
    
    def aeaEa(self):
        'Return tuple (status, register)'
        command = Register.Register(Register.AEA_EA)
        return self.register(command)
    
    def aeaEar(self, write = False):
        'Return tuple (status, register)'
        command = Register.Register(Register.AEA_EAR)
        return self.register(command, write)

    def genCfg(self, sdc = None):
        'Set/Get General Module Configuration, return tuple (status_string, register)'
        command = Register.Register(Register.GENCFG)

        if sdc != None:
            command.fieldSdc(sdc)
            
        return self.register(command, sdc != None)
    
    def ioCap(self, baudrate = None, module_select_no_reset = True):
        'Set/Get (integer) baud rate, return tuple (status_string, register)'
        command = Register.Register(Register.IOCAP)
        
        if baudrate != None:
            try:
                command.fieldCurrentBaudRate(str(baudrate))
            except:
                return 'Baud rate %i not supported' % (baudrate), None
            
            command.fieldRms(module_select_no_reset)
        return self.register(command, baudrate != None)
        
    def baudrate(self, baudrate = None):
        'Set/Get (integer) baud rate and reconnect with new baud rate, return tuple (status_string, baud_rate)'
        if self._link is None:
            raise Exception("Cannot change baud rate when not connected")
            return            
        curr_laser = self.laser()
        if baudrate != None:
            status, response = self.ioCap(baudrate, 1)
            if status == 'OK':            
                time.sleep(0.030)       #allow timeout to clean buffers and baud change
                rate = response.fieldCurrentBaudRate().cipher()
                if rate != str(baudrate):
                    print 'Unable to retrieve Lasers baud rate', str(baudrate)
            else:
                print 'Unable to configure Laser baudrate'
            self._link.baudrate = baudrate
            time.sleep(0.05)

        # Read to confirm baud rate is properly configured
        status, response = self.ioCap()
        if status != 'OK':
            return (status, 0)
        rate = response.fieldCurrentBaudRate().cipher()
        if baudrate != None and rate != str(baudrate):
            return 'Unable to configure baud rate ' + str(baudrate), 0

        return ('OK', rate)

    def eac(self):
        'Return tuple (status, register)'
        command = Register.Register(Register.EAC)
        return self.register(command)
    
    def ea(self):
        'Return tuple (status, register)'
        command = Register.Register(Register.EA)
        return self.register(command)
    
    def ear(self, value = None):
        'Return tuple (status, register)'
        command = Register.Register(Register.EAR, value)
        return self.register(command, value != None)

    def earfloatread(self):
        return (struct.unpack('>f',struct.pack('>H',(self.aeaEar()[1].data())) + struct.pack('>H',self.aeaEar()[1].data()))[0])

    def ear16bitread(self):
        return (struct.unpack('>H', struct.pack('>H',self.aeaEar()[1].data()))[0])

    def readAEAfloatarray(self,register = None, write = 0):
       regreq=self.register(register,write)
       if regreq[0] !='AEA':
           print 'Float array read failed'
           return
       numbytes=regreq[1].data()
       returndat=[]
       for i in range(0,numbytes,4):
           returndat.append(struct.unpack('>f',
                                          struct.pack('>H',self.aeaEar()[1].data()) + 
                                          struct.pack('>H',self.aeaEar()[1].data()) )[0])
       return returndat                              

    def earfloatwrite(self, value):
        floatbytes = map(ord,struct.pack('>f',value))
        self.register(Register.Register(address=Register.AEA_EAR,data=0x100 * floatbytes[0] + floatbytes[1]),write=True)
        self.register(Register.Register(address=Register.AEA_EAR,data=0x100 * floatbytes[2] + floatbytes[3]),write=True)
        return

    def writeAEAfloatarray(self,register = None, floatlist=[], write = True):
       regreq=self.register(register,write)
       if regreq[0] !='AEA':
           print 'Float array write failed'
           return
       numbytes=regreq[1].data()
       if numbytes / 4 != len(floatlist):
           print 'Expecting ', numbytes / 4, ' floats, but ', len(floatlist), ' given'
           return
       for i in range(0,numbytes,4):
           self.earfloatwrite(floatlist.pop(0))
       return

    def readAlarmTriggerLog(self):
        return self._readDebugStuff(index=1)

    def readHiH20(self):
        return self._readDebugStuff(index=6)
        
    def _readDebugStuff(self, index = 1):
       if(self._LaserType == 5):        # Namp
           dbgAlarmTriggerStruct = [    
                ["f","debug_df1"],
                ["f","debug_df2"],
                ["f","debug_sled"],
                ["f","debug_filter1"],
                ["f","debug_filter2"],
                ["f","debug_gain_medium_current"],
                ["f","debug_pd_current"],
                ["f","debug_power_target"],
                ["f","debug_power"],
                ["f","debug_SiBlock"],
                ["f","debug_averageDemod_delta"],
                ["H","debug_tuner_status"],
                ["H","debug_statusF"],
                ["H","debug_statusW"],
                ["H","debug_statusVSF"],
                ["H","debug_alrm_iterations"],
                ["f","debug_V33"],
                ["f","debug_V22"],
                ["H","debug_statusVSFLatches"],
                ["H","debug_statusVSFActive"]
                ]
           dbgAlrmHiH20Strct = [                        # NANO
                ["f","domain_PD_Delta_HiH20"],
                ["f","domain_Average_Demod_HiH20"],
                ["f","domain_Average_Demod_LowH20"],
                ["f","debug_V33_HiH20"],
                ["f","debug_V33_LowH20"],
                ["f","debug_Tec_Current_LowH20"],
                ["f","debug_Tec_Current_HiH20"],
                ["f","debug_Tec_Voltage_LowH20"],
                ["f","debug_Tec_Voltage_HiH20"],
                ["f","debug_V22_HiH20"],
                ["f","debug_V22_LowH20"],
                ["f","debug_siBlock_current_HiH20"],
                ["f","debug_siBlock_current_LowH20"],
                ["f","debug_Filter1_Temp_HiH20"],
                ["f","debug_Filter1_Temp_LowH20"],
                ["f","debug_Filter2_Temp_HiH20"],
                ["f","debug_Filter2_Temp_LowH20"],
                ["f","debug_df1_HiH20"],
                ["f","debug_df1_LowH20"],
                ["f","debug_df2_HiH20"],
                ["f","debug_df2_LowH20"],
                ["f","debug_df_delta_HiH20"],
                ["f","debug_df_delta_LowH20"],
                ]
       else:                            # uITLA
           dbgAlarmTriggerStruct = [    
                ["f","debug_df1"],
                ["f","debug_df2"],
                ["f","debug_sled"],
                ["f","debug_filter1"],
                ["f","debug_filter2"],
                ["f","debug_gain_medium_current"],
                ["f","debug_pd_current"],
                ["f","debug_power_target"],
                ["f","debug_power"],
                ["f","debug_SiBlock"],
                ["f","debug_averageDemod_delta"],
                ["H","debug_tuner_status"],
                ["H","debug_statusF"],
                ["H","debug_statusW"],
                ["H","debug_statusVSF"],
                ["H","debug_alrm_iterations"],
                ["f","debug_V52"],
                ]
           dbgAlrmHiH20Strct = [
                ["f","domain_PD_Delta_HiH20"],
                ["f","domain_Average_Demod_HiH20"],
                ["f","domain_Average_Demod_LowH20"],
                ["f","domain_Average_Filter2_HiH20"],
                ["f","domain_Average_Filter2_LowH20"],
                ]
           
       if(index == 1):
           decodeStruct = dbgAlarmTriggerStruct
       elif(index == 6):
           decodeStruct = dbgAlrmHiH20Strct
       else:
           print "Unsuported 0x85 index."
           return

       regreq=self.register(Register.Register(address=0x85,data=index),write=False)
       if regreq[0] !='AEA':
           print 'Read Alarm Trigger Log Failed'
           return

        # Put in size check numbytes vs struct bytes required.
#       numbytes=regreq[1].data()
        
       retval = self.formatted()
       
       for dbgStructEntry in decodeStruct: 
           if(dbgStructEntry[0] == 'f'):
               setattr(retval, dbgStructEntry[1], self.earfloatread())
#               print dbgStructEntry[1], ': ', str(self.earfloatread())
           elif(dbgStructEntry[0] == 'H'):                               
               setattr(retval,dbgStructEntry[1], self.ear16bitread())
#               print dbgStructEntry[1], ': ', str(self.ear16bitread())
              
       return retval

    def lstResp(self):
        'Return tuple (status, register)'
        command = Register.Register(Register.LSTRESP)
        return self.register(command)

    def dlConfig(self, init_write = None, abrt = None, done = None, init_read = None, init_check = None, init_run = None, runv = None, type = None):
        'Return tuple (status, register)'
        command = Register.Register(Register.DLCONFIG)
        command.fieldInitWrite(init_write)
        command.fieldAbrt(abrt)
        command.fieldDone(done)
        command.fieldInitRead(init_read)
        command.fieldInitCheck(init_check)
        command.fieldInitRun(init_run)
        command.fieldRunv(runv)
        command.fieldType(type)

        write = init_write != None or \
                abrt != None or \
                done != None or \
                init_read != None or \
                init_check != None or\
                init_run != None or \
                runv != None or \
                type != None

        return self.register(command, write)

    def dlStatus(self):
        return self.register(Register.Register(Register.DLSTATUS))
    
    def statusF(self, xel = 0, cel = 0, mrl = 0, crl = 0, fvsfl = 0, ffreql = 0, ftherml = 0, fpwrl = 0):
        'Get/Set status fatal, return (status_string, register)'
        command = Register.Register(Register.STATUSF)
        command.fieldXel(xel)
        command.fieldCel(cel)
        command.fieldMrl(mrl)
        command.fieldCrl(crl)
        command.fieldFvsfl(fvsfl)
        command.fieldFfreql(ffreql)
        command.fieldFtherml(ftherml)
        command.fieldFpwrl(fpwrl)
        write = xel or cel or mrl or crl or fvsfl or ffreql or ftherml or fpwrl

        return self.register(command, write)
    
    def statusW(self, xel = 0, cel = 0, mrl = 0, crl = 0, wvsfl = 0, wfreql = 0, wtherml = 0, wpwrl = 0):
        'Get/Set status fatal, return (status_string, register)'
        command = Register.Register(Register.STATUSW)
        command.fieldXel(xel)
        command.fieldCel(cel)
        command.fieldMrl(mrl)
        command.fieldCrl(crl)
        command.fieldWvsfl(wvsfl)
        command.fieldWfreql(wfreql)
        command.fieldWtherml(wtherml)
        command.fieldWpwrl(wpwrl)
        write = xel or cel or mrl or crl or wvsfl or wfreql or wtherml or wpwrl

        return self.register(command, write)

    def fPowTh(self, dB100 = None):
        'Set/Get fatal power threshold in dB*100, return (status_string, threshold)'
        command = Register.Register(Register.FPOWTH, dB100)
        status, response = self.register(command, dB100 != None)
        if status == 'OK':
            return status, response.data()
        return status, 0
    
    def wPowTh(self, dB100 = None):
        'Set/Get warning power threshold in dB*100, return (status_string, threshold)'
        command = Register.Register(Register.WPOWTH, dB100)
        status, response = self.register(command, dB100 != None)
        if status == 'OK':
            return status, response.data()
        return status, 0

    def fFreqTh(self):
        'Get fatal frequency threshold in GHz*10, return (status_string, threshold)'
        command = Register.Register(Register.FFREQTH)
        status, response = self.register(command)
        if status == 'OK':
            return status, response.data()
        return status, 0
    
    def wFreqTh(self):
        'Get warning frequency threshold in GHz*10, return (status_string, threshold)'
        command = Register.Register(Register.WFREQTH)
        status, response = self.register(command)
        if status == 'OK':
            return status, response.data()
        return status, 0
    
    def fThermTh(self):
        'Get fatal thermal threshold in degC*100, return (status_string, threshold)'
        command = Register.Register(Register.FTHERMTH)
        status, response = self.register(command)
        if status == 'OK':
            return status, response.data()
        return status, 0
    
    def wThermTh(self):
        'Get warning thermal threshold in degC*100, return (status_string, threshold)'
        command = Register.Register(Register.WTHERMTH)
        status, response = self.register(command)
        if status == 'OK':
            return status, response.data()
        return status, 0

    def srqT(self, dis = None, wvsfl = None, wfreql = None, wtherml = None, wpwrl = None, xel = None, cel = None, mrl = None, crl = None, fvsfl = None, ffreql = None, ftherml = None, fpwrl = None):
        'Set/Get SRQ triggers, return (status_string, register)'
        command = Register.Register(Register.SRQT)
        write = dis     != None or \
                wvsfl   != None or \
                wfreql  != None or \
                wtherml != None or \
                wpwrl   != None or \
                xel     != None or \
                mrl     != None or \
                crl     != None or \
                fvsfl   != None or \
                ffreql  != None or \
                ftherml != None or \
                fpwrl   != None

        if write:
            status, response = self.register(command)
            if status != 'OK':
                return status, response
            command = Register.Register(Register.SRQT, response.data())

        command.fieldDis(dis)
        command.fieldWvsfl(wvsfl)
        command.fieldWfreql(wfreql)
        command.fieldWtherml(wtherml)
        command.fieldWpwrl(wpwrl)
        command.fieldXel(xel)
        command.fieldCel(cel)
        command.fieldMrl(mrl)
        command.fieldCrl(crl)
        command.fieldFvsfl(fvsfl)
        command.fieldFfreql(ffreql)
        command.fieldFtherml(ftherml)
        command.fieldFpwrl(fpwrl)

        return self.register(command, write)

    def fatalT(self, wvsfl = None, wfreql = None, wtherml = None, wpwrl = None, mrl = None, fvsfl = None, ffreql = None, ftherml = None, fpwrl = None):
        'Set/Get fatal triggers, return (status_string, register)'
        command = Register.Register(Register.FATALT)
        write = wvsfl   != None or \
                wfreql  != None or \
                wtherml != None or \
                wpwrl   != None or \
                mrl     != None or \
                fvsfl   != None or \
                ffreql  != None or \
                ftherml != None or \
                fpwrl   != None

        if write:
            status, response = self.register(command)
            if status != 'OK':
                return status, response
            command = Register.Register(Register.FATALT, response.data())

        command.fieldWvsfl(wvsfl)
        command.fieldWfreql(wfreql)
        command.fieldWtherml(wtherml)
        command.fieldWpwrl(wpwrl)
        command.fieldMrl(mrl)
        command.fieldFvsfl(fvsfl)
        command.fieldFfreql(ffreql)
        command.fieldFtherml(ftherml)
        command.fieldFpwrl(fpwrl)

        return self.register(command, write)

    def almT(self, wvsf = None, wfreq = None, wtherm = None, wpwr = None, fvsf = None, ffreq = None, ftherm = None, fpwr = None):
        'Set/Get alarm triggers, return (status_string, register)'
        command = Register.Register(Register.ALMT)
        write = wvsf != None or\
                wfreq != None or \
                wtherm != None or \
                wpwr != None or \
                fvsf != None or \
                ffreq != None or \
                ftherm != None or \
                fpwr != None

        if write:
            status, response = self.register(command)
            if status != 'OK':
                return status, response
            command = Register.Register(Register.ALMT, response.data())

        command.fieldWvsf(wvsf)
        command.fieldWfreq(wfreq)
        command.fieldWtherm(wtherm)
        command.fieldWpwr(wpwr)
        command.fieldFvsf(fvsf)
        command.fieldFfreq(ffreq)
        command.fieldFtherm(ftherm)
        command.fieldFpwr(fpwr)

        return self.register(command, write)

    def channel(self, channel = None):
        'Set/Get channel, return (status_string, channel_number)'
        command = Register.Register(Register.CHANNEL, channel)
        if channel == None:
            status, response = self.register(command)
            if status != 'OK':
                return (status, -1)
            return status, int(response.data())
        status, response = self.register(command, True)
        
        if response.name() != 'CHANNEL':
            return 'Inconsistent register name (expected CHANNEL, received %s)' % (response.name()), -1
        return status, response.data()

    def gmislope(self, slope = None):
        'Set/Get gmi slope, return (status_string, slope_value)'
        command = Register.Register(Register.GMISLOPE, slope)
        if slope == None:
            status, response = self.register(command)
            if status != 'OK':
                return (status, -1)
            return status, int(response.data())
        
        status, response = self.register(command, True)
        
        if response.name() != 'GMISLOPE':
            return 'Inconsistent register name (expected GMISLOPE, received %s)' % (response.name()), -1

        return status, response.data()

    def pwr(self, power = None):
        'Get/Set power set point, return (status_string, powerdBm*100)'
        command = Register.Register(Register.PWR, power)
        status, response = self.register(command, power != None)
        power = response.data()
        if power > 0x7FFF:
            power -= 0x10000
        
        return (status, power)

    def resena(self, sena = None, sr = None, mr = None):
        'Get/Set reset/enable, return (status_string, register)'
        command = Register.Register(Register.RESENA)
        write = sena != None or sr != None or mr != None

        command.fieldSena(sena)
        command.fieldSr(sr)
        command.fieldMr(mr)

        return self.register(command, write)

    def mcb(self, ado = None, sdf = None, adt = None):
        'Get/Set module configuration behavior, return (status_string, register)'
        command = Register.Register(Register.MCB)   

        write = ado != None or sdf != None or adt != None
        if write:
            status, response = self.register(command)
            command = Register.Register(Register.MCB, response.data())
        command.fieldAdo(ado)
        command.fieldSdf(sdf)
        command.fieldAdt(adt)

        return self.register(command, write)
    
    def _frequency(self, frequency1, frequency2):
        'Get laser\'s frequency in THz, return (status_string, fThz)'
        command = Register.Register(frequency1)
        status, response = self.register(command)
        if status != 'OK':
            return status, -1.0
        frequency = response.data()

        command = Register.Register(frequency2)
        status, response = self.register(command)
        if status != 'OK':
            return status, -1.0
        frequency += response.data() / 10000.0

        return 'OK', frequency
    
    def grid(self, frequency = None):
        'Get/Set grid spacing in GHz*10, return (status_string, fGHz*10)'
        command = Register.Register(Register.GRID, frequency)
        status, response = self.register(command, frequency != None)
        frequency = response.data()
        if frequency > 0x7FFF:
            frequency -= 0x10000
        return status, frequency

    def fcf(self, frequency = None):
        'Get/Set first channel frequency in THz, return (status, fTHz)'
        if frequency != None:
            THz = int(frequency)
            GHz10 = (frequency - THz + 0.00005) * 10000.0
            status, lfl = self.lfl()
            self.fcf1(lfl + 1)

            status, response = self.fcf2(GHz10)
            if status != 'OK':
                return status, 0

            status, response = self.fcf1(THz)
            if status != 'OK':
                return status, 0
        
        return self._frequency(Register.FCF1, Register.FCF2)
    
    def fcf1(self, fTHz = None):
        'Get/Set first channel frequency THz, return (status_string, fTHz)'
        if fTHz != None:
            fTHz = int(fTHz)
        command = Register.Register(Register.FCF1, fTHz)
        status, response = self.register(command, fTHz != None)
        return status, response.data()
        
    def fcf2(self, fGHz10 = None):
        'Get/Set first channel frequency THz, return (status_string, fGHz*10)'
        if fGHz10 != None:
            fGHz10 = int(fGHz10)
        command = Register.Register(Register.FCF2, fGHz10)
        status, response = self.register(command, fGHz10 != None)
        return status, response.data()
        
    def lf(self):
        'Get channel\'s frequency in THz, return (status_string, fThz)'
        return self._frequency(Register.LF1, Register.LF2)

    def oop(self):
        'Get optical output power, return (status_string, powerdBm*100)'
        command = Register.Register(Register.OOP)
        status, response = self.register(command)
        return status, struct.unpack('h', struct.pack('H', response.data()))[0]

    def ctemp(self):
        'Get current temperature, return (status_string, degreeC*100)'
        command = Register.Register(Register.CTEMP)
        status, response = self.register(command)
        return status, struct.unpack('h', struct.pack('H', response.data()))[0]

    def ftfr(self):
        'Get Fine Tune frequency Range, return (status_string, MHz)'
        command = Register.Register(Register.FTFR)
        status, response = self.register(command)
        return status, struct.unpack('h', struct.pack('H', response.data()))[0]

    def opsl(self):
        'Get minimum power setting, return (status_string, powerdBm*100)'
        command = Register.Register(Register.OPSL)
        status, response = self.register(command)
        return status, struct.unpack('h', struct.pack('H', response.data()))[0]
        
    def opsh(self):
        'Get maximum power setting, return (status_string, powerdBm*100)'
        command = Register.Register(Register.OPSH)
        status, response = self.register(command)
        return status, struct.unpack('h', struct.pack('H', response.data()))[0]
        
    def lfl(self):
        'Get laser\'s first frequency in THz, return (status_string, fThz)'
        return self._frequency(Register.LFL1, Register.LFL2)
    
    def lfh(self):
        'Get laser\'s last frequency in THz, return (status_string, fTHz)'
        return self._frequency(Register.LFH1, Register.LFH2)

    def lgrid(self):
        'Get laser\'s minimum supported grid spacing in GHz*10, return (status_string, fGHz*10)'
        command = Register.Register(Register.LGRID)
        status, response = self.register(command)
        return status, response.data()

    def aeaList(self, address):
        'Return tuple (status, (byte_count, list))'
        register = Register.Register(address)
        status, response = self.register(register)
        results = []
        if status != 'AEA':
            return status, (0, results)
        
        byteCount = response.data()

        status, response = self.register(Register.Register(Register.AEA_EA))
        if status != 'OK':
            return status, (0, results)

        if response.data() == 0:
            return 'Invalid extended address', (0, results)

        status, response = self.register(Register.Register(Register.AEA_EAC))
        if status != 'OK':
            return status, (0, results)

        if response.fieldIncr().value() != 2 or response.fieldRai().value() != 1:
            return 'Extended address not configured', (0, results)

        if byteCount % 2 != 0:
            return 'Invalid byte count', (byteCount, results)

        command = Register.Register(Register.AEA_EAR)

        for i in range(byteCount / 2):
            status, response = self.register(command)
            if status != 'OK':
                return status, (0, [])
            results.append(response.data())

        return status, (byteCount, results)
        
    def currents(self):
        'Return tuple (status, (byte_count, list))'
        return self.aeaList(Register.CURRENTS)
    
    def temps(self):
        'Return tuple (status, (byte_count, list))'
        temps = self.aeaList(Register.TEMPS)  # signed shorts
        if temps[0] == 'OK':
            if temps[1][1][0] > 32767:
                temps[1][1][0] -= 65536
            if temps[1][1][1] > 32767:
                temps[1][1][1] -= 65536
        return temps
    
    def ditherE(self, wf = None, de = None):
        'Get/Set dither, return (status_string, register)'
        command = Register.Register(Register.DITHERE)
        command.fieldWf(wf)
        command.fieldDe(de)
        return self.register(command, wf != None or de != None)

    def ditherR(self, rate = None):
        'Get/Set dither rate in KHz, return (status_string, rateKHz)'
        command = Register.Register(Register.DITHERR, rate)
        status, response = self.register(command, rate != None)

        return status, response.data()

    def ditherF(self, width = None):
        'Get/Set dither width in GHz * 10, return (status_string, width100MHz)'
        command = Register.Register(Register.DITHERF, width)
        status, response = self.register(command, width != None)

        return status, response.data()

    def ditherA(self, gain = None):
        'Get/Set dither gain in percent, return (status_string, gain)'
        command = Register.Register(Register.DITHERA, gain)
        status, response = self.register(command, gain != None)

        return status, response.data()

    def fAgeTh(self, threshold = None):
        'Get/Set fatal laser age threshold in percentage, return (status_string, threshold)'
        command = Register.Register(Register.FAGETH, threshold)
        status, response = self.register(command, threshold != None)

        return status, response.data()
    
    def wAgeTh(self, threshold = None):
        'Get/Set warning laser age threshold in percentage, return (status_string, threshold)'
        command = Register.Register(Register.WAGETH, threshold)
        status, response = self.register(command, threshold != None)

        return status, response.data()
    
    def age(self):
        'Get laser\'s age in percentage, return (status_string, age)'
        command = Register.Register(Register.AGE)
        status, response = self.register(command)
        return status, response.data()

    def ftf(self, MHz = None):
        'Get/Set the fine tune frequency in +/-MHz, return (status_string, MHz)'
        command = Register.Register(Register.FTF, MHz)
        status, response = self.register(command, MHz != None)

        frequency = response.data()
        if frequency > 0x7FFF:
            frequency -= 0x10000

        return status, frequency

    def health(self):
        'Get the health status (status_string, 16bit status report)'
        return self.register(Register.Register(Register.HEALTH))

    def _upgradeFirmware(self, filename, version):
        # Open file 
        file = open(filename, 'rb')
        text = file.read()
        file.close()
        
#        if text[8] != self._LaserType:
#            print '*** Warning: possible product mismatch ***'
#            if not query_yes_no('Do you want to ontinue with FW upgrade?', default='no'):
#                return
            
        
        if version.lower().startswith('interrupt'):
            type = 3
        elif version.lower().startswith('maintain'):
            type = 1
        else:
            return 'Invalid version'
        
        self.detect()
        start = self._gettime()		# time the download
        curr_laser = self.laser()
        if curr_laser == 0:			# single uITLA
            # Abort any current operation.
            status, NA = self.dlConfig(abrt = 1) 	
            if (status != 'OK'): return('Abrt ' + status) 

            status, NA = self.dlConfig(init_write = 1, type = type)	
            if (status != 'OK'): return('Init_Write ' + status) 

            # Pad to even number of bytes: Two bytes per packet. The firmware can
            # deal with the extra byte without an error.
            if (len(text) & 0x01): text += '\xFF' 

            print 'Loading Code'
            #time.sleep(1)		#pb change to 0.2 sec
            #self._link.flushInput()
            # self.flushBuffer()

            EAR = Register.Register(Register.EAR)
            packet = ModuleBoundPacket()
            packet.register(Register.EAR)
            packet.mode(1)

            for i in range(4):
                try:
                    self.nop()
                    break
                except:
                    time.sleep(0.2)
                    pass        
            else:
                return 'Unable to upgrade: Monitor not responding'

            cnt = 0
            dotCnt = 0
            cnt16K = 0
            oldDebug = self._debug_rs232;
            for i in range(0, len(text), 2):
                packet.data(struct.unpack('>H', text[i : i + 2])[0])
                packet.checksum(packet.computedChecksum())
                self.write(packet.buffer())
                response = self.read(4, maxRetry = RX_TIMEOUT_UPGRADE_EAR / self._timeout)
                if len(response) != 4:
                    self._debug_rs232 = oldDebug
                    return('Aborting upgrade')
                if ord(response[1]) & 0x3 != 0:           
                    self._debug_rs232 = oldDebug
                    return ('Write failed', i, map(hex, map(ord, response)))
                
                if(self._debug_rs232 == 1):
                    self._debug_rs232 = 0
                #print a dot to let the operator know that we are working...
                cnt = cnt+1
                if (cnt >= 512):    
                    cnt = 0
                    dotCnt = dotCnt+1
                    if (dotCnt >= 32):
                        dotCnt = 0
                        cnt16K += 2
                        print '%dK' % (cnt16K * 16)
                    else:
                        print '.',
                    sys.stdout.flush() 
                    time.sleep(0.001)               

            # Read the response packets left-over on the UART buffer
            #pb self.flushBuffer()
            self._link.flushInput()
            self._debug_rs232 = oldDebug

            # DLCONFIG:DONE
            status, NA = self.dlConfig(done = 1)
            if (status != 'OK'):
                return('Done ' + status)
            # DLCONFIG:INIT_CHECK
            status, register = self.dlConfig(init_check = 1)

            if (status == 'CP'):
                # Pending loop.
                # Extract pending flag.
                pending_flag = register.data() >> 8
                cnt = 10
                while (cnt):
                    cnt -= 1
                    NA, register = self.nop()
                    if ((register.fieldPending().value() & pending_flag) == 0):
                        break
                    time.sleep(0.1)
                if(cnt == 0):
                    return('Status CP stuck ' + status)
            elif (status != 'OK'):
                return('Init_Check ' + status)

            status, dlStatus = self.dlStatus()
            if dlStatus.fieldValid().value() != 1:
                return 'dlStatus invalid'

            # TODO: Remove hardcoded type.
            status, NA = self.dlConfig(init_run = 1, runv = type)
            if (status != 'OK'):
                return('Init_run failed:' + status)

            # Allow firmware to boot
            time.sleep(REBOOT_TIME)
            print 'Seconds elapsed', self._gettime() - start
            return('Download Complete!')

        # Dual uITLA firmware upgrade, upgrades both laser at once
        self.laser(1)
        # Abort any current operation.
        status, NA = self.dlConfig(abrt = 1) 
        if (status != 'OK'): return('Laser1: Abrt ' + status) 
        status, NA = self.dlConfig(init_write = 1, type = type)
        if (status != 'OK'): return('Laser1: Init_Write ' + status) 
        self.laser(2)
        # DLCONFIG: ABORT0-1
        # Abort any current operation.
        status, NA = self.dlConfig(abrt = 1) 
        if (status != 'OK'): return('Laser2: Abrt ' + status) 
        status, NA = self.dlConfig(init_write = 1, type = type)
        if (status != 'OK'): return('Laser2: Init_Write ' + status) 

        # Pad to even number of bytes: Two bytes per packet. The firmware can
        # deal with the extra byte without an error.
        if (len(text) & 0x01): text += '\xFF' 

        print 'Monitor mode'
        self._link.flushInput()

        EAR = Register.Register(Register.EAR)
        packet = ModuleBoundPacket()
        packet.register(Register.EAR)
        packet.mode('WRITE')
        if self.laser() == 2:	
            packet.laser('LASER1')      # laser 2 set bit 26
        else:
            packet.laser('LASER0')      # 0 or 1 clear bit 26

        for i in range(4):
            try:
                self.nop()
                break
            except:
                time.sleep(0.2)
                pass        
        else:
            return 'Unable to upgrade: Monitor not responding'

        # DLCONFIG: WRITE0-1
        cnt = 0
        dotCnt = 0
        cnt16K = 0
        oldDebug = self._debug_rs232;
        for i in range(0, len(text), 2):
            packet.data(struct.unpack('>H', text[i : i + 2])[0])
            packet.laser('LASER0')
            packet.checksum(packet.computedChecksum())
            self.write(packet.buffer())
            response = self.read(4, maxRetry = RX_TIMEOUT_UPGRADE_EAR / self._timeout)
            if len(response) != 4:
                self._debug_rs232 = oldDebug
                return('Aborting upgrade: Laser2')
            if ord(response[1]) & 0x3 != 0:           
                self._debug_rs232 = oldDebug
                return ('Write failed: Laser2', i, map(hex, map(ord, response)))
            packet.laser('LASER1')
            packet.checksum(packet.computedChecksum())
            self.write(packet.buffer())
            response = self.read(4, maxRetry = RX_TIMEOUT_UPGRADE_EAR / self._timeout)
            if len(response) != 4:
                self._debug_rs232 = oldDebug
                return('Aborting upgrade: Laser1')
            if ord(response[1]) & 0x3 != 0:           
                self._debug_rs232 = oldDebug
                return ('Write failed: Laser1', i, map(hex, map(ord, response)))
            
            if(self._debug_rs232):
                self._debug_rs232 = 0
            #print a dot to let the operator know that we are working...
            cnt = cnt+1
            if (cnt >= 512):    
                cnt = 0
                dotCnt = dotCnt+1
                if (dotCnt >= 32):
                    dotCnt = 0
                    cnt16K += 2
                    print '%dK' % (cnt16K * 16)
                else:
                    print '.',
                sys.stdout.flush() 
                time.sleep(0.001)               

        # Read the response packets left-over on the UART buffer
        #pb self.flushBuffer()
        self._link.flushInput()
        self._debug_rs232 = oldDebug

        self.laser(2)
        # DLCONFIG: DONE0
        status, NA = self.dlConfig(done = 1)
        if (status != 'OK'):
            return('Laser2: Done ' + status)
        # DLCONFIG: INIT_CHECK0
        status, register = self.dlConfig(init_check = 1)

        if (status == 'CP'):
            # Pending loop.
            # Extract pending flag.
            pending_flag = register.data() >> 8
            cnt = 10
            while (cnt):
                cnt -= 1
                NA, register = self.nop()
                if ((register.fieldPending().value() & pending_flag) == 0):
                    break
                time.sleep(0.1)
            if(cnt == 0):
                return('Laser2: Status CP stuck ' + status)
        elif (status != 'OK'):
            return('Laser2: Init_Check ' + status)

        status, dlStatus = self.dlStatus()
        if dlStatus.fieldValid().value() != 1:
            return 'Laser2: dlStatus invalid'

        self.laser(1)
        # DLCONFIG: DONE1
        status, NA = self.dlConfig(done = 1)
        if (status != 'OK'):
            return('Laser1: Done ' + status)

        # DLCONFIG:INIT_CHECK1
        status, register = self.dlConfig(init_check = 1)

        if (status == 'CP'):
            # Pending loop.
            # Extract pending flag.
            pending_flag = register.data() >> 8
            cnt = 10
            while (cnt):
                cnt -= 1
                NA, register = self.nop()
                if ((register.fieldPending().value() & pending_flag) == 0):
                    break
                time.sleep(0.1)
            if(cnt == 0):
                return('Laser1: Status CP stuck ' + status)
        elif (status != 'OK'):
            return('Laser1: Init_Check ' + status)

        status, dlStatus = self.dlStatus()
        if dlStatus.fieldValid().value() != 1:
            return 'Laser1: dlStatus invalid'

        # DLCONFIG: INIT_RUN0-1
        self.laser(2)
        status, NA = self.dlConfig(init_run = 1, runv = type)
        if (status != 'OK'):
            return('Laser2: Init_run ' + status)
        time.sleep(REBOOT_TIME)     # Allow laser 2 to boot --> drive laser 1
        self.laser(1)
        status, NA = self.dlConfig(init_run = 1, runv = type)
        if (status != 'OK'):
            return('Laser1: Init_run ' + status)

        # Allow firmware to boot
        time.sleep(REBOOT_TIME)
        self.laser(curr_laser)
        print 'Seconds elapsed', self._gettime() - start
        return('Download Complete!')

    def upgrade(self, target, filename, version = 'Interrupting'):
        if ('APPLICATION'.startswith(target.upper())):
            return(self._upgradeFirmware(filename, version))
        else:
            raise 'Target type unknown.' 

    def upload(self, filename):
        start = self._gettime()
        
        # Open file and download.
        file = open(filename, 'rb')
        text = file.read()
        file.close()

        # Pad to even number of bytes: Two bytes per packet. The firmware can
        # deal with the extra byte without an error.
        if (len(text) & 0x01): text += '\x00' 

        EAR = Register.Register(Register.EAR)
        packet = ModuleBoundPacket()
        packet.register(Register.EAR)
        packet.mode(1)

        for i in range(0, len(text), 2):

            packet.data(struct.unpack('>H', text[i : i + 2])[0])
            packet.checksum(packet.computedChecksum())

            attempts = 8
            while attempts > 0:
                #print 'packet', map(hex, map(ord, packet.buffer()))
                # Send buffer to module
                self.write(packet.buffer())

                # Read the response back
                response = self.read(4)
                # Move on to next buffer is the status field is OK
                if ord(response[1]) & 0x3 == 0:
                    break
                else:
                    attempts -= 1

            if attempts == 0:
                return 'Write failed', ord(response[1])

        return 'OK', self._gettime() - start

    def dbgReset(self):
        'Return tuple (status_string, register)'
        return self.register(Register.Register(Register.DBG_RESET))

    # Nano Only.
    def statusVSF(self):
        command = Register.Register(Register.VSF)
        return self.register(command, 0)

    # Nano Only.
    def statusVSFL(self, clearFlags = 0x0000):
        command = Register.Register(Register.VSFL, clearFlags)
        write = clearFlags != 0
        return self.register(command, write)

    # Nano Only.
    def statusHwFailure(self):
        command = Register.Register(Register.HW_FAIL)
        return self.register(command, 0)

'''    
    def debug(self, index = 0, address = None):
        'Retrieve two bytes of RAM content at address. 
        Use an index of zero for bytes 0 and 1 and
        an index of one for bytes 2 and 3. 
        Return the status string and the two bytes as string 
        in the same order read from RAM.
        '
        command = Register.Register(Register.DEBUG, address)
        command.fieldWordIndex(index)
        status, response = self.register(command)
        return status, struct.pack('>H', response.data())

    def debugU8(self, address):
        # Return RAM content of U8 at address.
        NA, bytes01  = self.debug(0, address)
        return struct.unpack('B', bytes01[:1])[0]

    def debugS8(self, address):
        # Return RAM content of S8 at address.
        NA, bytes01  = self.debug(0, address)
        return chr(struct.unpack('b', bytes01[:1])[0])

    def debugU16(self, address):
        # Return RAM content of U16 at address.
        NA, bytes01  = self.debug(0, address)
        return struct.unpack('>H', bytes01)[0]

    def debugS16(self, address):
        # Return RAM content of S16 at address.
        NA, bytes01  = self.debug(0, address)
        return struct.unpack('>h', bytes01)[0]
            
    def debugFloat(self, address):
        # Return RAM content of float at address.
        NA, bytes01  = self.debug(0, address)
        NA, bytes23 = self.debug(1, address)
        return struct.unpack('>f', bytes01 + bytes23)[0]

    def debugU32(self, address):
        # Return RAM content of unsigned 32 at address.
        NA, bytes01  = self.debug(0, address)
        NA, bytes23 = self.debug(1, address)
        return struct.unpack('>L', bytes01 + bytes23)[0]

    def debugS32(self, address):
        # Return RAM content of signed 32 at address.
        NA, bytes01  = self.debug(0, address)
        NA, bytes23 = self.debug(1, address)
        return struct.unpack('>l', bytes01 + bytes23)[0]
        
    def channel(i, channel):
        print 'Tuning to channel', channel
        i.statusF()
        i.statusW()
        i.statusF(1,1,1,1, 1,1,1,1)
        i.statusW(1,1,1,1, 1,1,1,1)
        timeout = 30.0
        start = self._gettime()
        i.resena(sena=1)
        status, response = i.channel(channel)
        if status != 'OK':
            print status, response
            return
        duration = 0.0
        while True:
            i.statusF()
            i.statusW()
            i.debugLevel(i.DEBUG_NONE)
            status, nop = i.nop()
            i.debugLevel(i.DEBUG_HOST_BOUND_REGISTER)
            #print nop
            if status != 'OK':
                print status, channel
                return
            if nop.fieldPending().value() == 0:
                duration = float(self._gettime() - start)
                break
            elif (self._gettime() - start) > timeout:
                print 'Tuning timeout', channel
                return

        status, channel = i.channel()
        if status != 'OK':
            print (status, -1)
            return
                    
        print status, 'Channel %i tuned in %f seconds' % (channel, duration)


def unitTest():
    # Unit test this module and illustrate sample usage 
    i = ITLA()
    #i.debugLevel(ITLA.DEBUG_PACKET)
    print i.connect(2)

    i.debugLevel(ITLA.DEBUG_REGISTER)
    #i.debugLevel(ITLA.DEBUG_NONE)
    print 'Testing Individual Registers with all support baud rates'
    for baudrate in [9600, 19200, 38400, 57600, 115200]:
        i.baudrate(baudrate)
        i.baudrate()

    print 'Testing Channel Tune'
    timeout = 30.0
    for c in range(1, 100):
        channel(i, c)

    # Graceful exit!    
    i.disconnect()
    
def statusTest():
    i = ITLA()
    try:
        i.connect(2)
        #i.debugLevel(ITLA.DEBUG_REGISTER)
        i.debugLevel(ITLA.DEBUG_HOST_BOUND_REGISTER)
        i.almT()
        i.srqT()
        i.fatalT()
        i.almT(1,1,1,1)
        i.srqT(0,0,0,0,0,0,0,0,0,1,1,1,1)
        i.fatalT(0,0,0,0,0,1,1,1,1)
        
        i.wPowTh(176)
        i.fPowTh(10000)
        i.wPowTh()
        i.fPowTh()

        i.mcb(sdf = 0, adt = 1)
        channel(i, 1)
        print 'Should see power and frequency warnings - with ADT set'

        i.mcb(adt = 0)
        channel(i, 2)
        print 'Should not see warnings - with ADT clear'

        i.wPowTh(10)
        i.wPowTh()
        channel(i, 3)
        print 'Should see power warning - with lower power warning threshold'

        i.resena(sena=0)
        i.fPowTh(20)
        i.fPowTh()
        channel(i, 4)
        print 'Should see power fatal - with lower power fatal threshold'

        i.channel()
        print 'Should not see shutdown - with SDF clear'

        i.mcb(sdf = 1)
        time.sleep(3)
        i.channel()
        print 'Should see shutdown - with SDF set'

        i.fatalT(fpwrl = 0)
        channel(i, 5)
        time.sleep(3)
        i.channel()
        print 'Should not see shutdown - with fatalT.FPWRL = 0'

    finally:
        # Graceful exit!    
        i.disconnect()
    
# print 'from <ITLA.py>, the value of <__name__> is:', __name__

if __name__ == '__main__':
    unitTest()
    statusTest()
'''
