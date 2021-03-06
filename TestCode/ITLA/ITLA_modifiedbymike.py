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

if sys.hexversion > 0x02060000:
    import bz2

import Register
from Packet import HostBoundPacket
from Packet import ModuleBoundPacket

def version():
    return '3.0.1.0'

class StackMarker:
    __depth = 0
    def __init__(self, name):
        self.__name = name
        print '=' * (self.__depth * 4), 'Enter function =>', name
        self.__depth += 1
    def __del__(self):
        print '=' * (self.__depth * 4), 'Exit function =>', self.__name
        self.__depth -= 1

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
    def __init__(self, t_object = None):
        self.__register = None
        self.__baud = 0
        self.__port = 0
        self.__link = None
        self.__packet = None
        self.__module_packet = None
        self.__debug_level = 0
        self.__debug_rs232 = 0
        self.__laserSelect = 0
        self.__t_object = t_object
        self.__OIFlogging = False
        self.__logstarttime = time.time()
        self.__droppedbytecount = 0
        self.__retrying = False
        self.__inTMode = False
        self.__dummyx99data = None # bit of a hack to try to get readx99() to return an object with the right attributes even when there is an OIF error
        if (os.name == 'posix'):
            #self.__commslogfilename = os.path.expanduser("~/commslog_port" + str(self.__port) + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3] + ".txt")
            self.__commslogfilename = os.path.expanduser("~/commslog_port" + str(self.__port) + "_" + 
                time.asctime().replace(" ", "_").replace(':','-') + ".txt")
            self.__portprefix = '/dev/ttyS'
        else:
            self.__commslogfilename = "commslog_port" + str(self.__port) + "_"
            self.__commslogfilename +=  time.asctime().replace(" ", "_").replace(':','-')
            self.__commslogfilename += ".txt"
            self.__portprefix = 'com'

    def setupFromTMode(self,tMode = False):
        self.__inTMode = tMode
        if tMode==True:
            self.__link = self.__t_object
        else:
            self.__link = None
    def __del__(self):
        self.disconnect()

    def __repr__(self):
        msg  = 'Description : ITLA\n'
        msg += 'Port        : %i\n' % (self.__port)
        msg += 'Baud        : %i\n' % (self.__baud)
        msg += 'OIF Logging : %r\n' % (self.__OIFlogging)
        msg += 'Log File    : %s' % (self.__commslogfilename)

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
        return(self.__port)

    def getdroppedbytecount(self):
        return(self.__droppedbytecount)

    def cleardroppedbytecount(self):
        print 'Clearing dropped byte count'
        self.__droppedbytecount = 0
        return(self.__droppedbytecount)

    def getlogfilename(self):
        return(self.__commslogfilename)

    def logging(self,OIFlogging = None):
        if OIFlogging is None:
            print 'OIF Logging : %r' % (self.__OIFlogging)
            print 'Log File    : %s' % (self.__commslogfilename)
            return
        else:
            self.__OIFlogging = OIFlogging
            if (self.__OIFlogging):
                try:
                    oiflogfile=open(self.__commslogfilename,"a")
                    self.__logstarttime = time.time()
                    oiflogfile.write("# logging started " + time.asctime() + "\n")
                    oiflogfile.flush()
                except OSError:
                    print "Unable to open logfile", self.__commslogfilename
                    self.__OIFlogging = False
                    return

    def logfile(self,logfilename=None):
        if (logfilename is None):
            print 'OIF Logging : %r' % (self.__OIFlogging)
            print 'Log File    : %s' % (self.__commslogfilename)
            return self.__commslogfilename
        loggingtimestring = time.asctime()
        if logfilename is None:
            if (os.name != 'posix'):
                self.__commslogfilename = "commslog_port" + str(self.__port) + "_" + time.asctime().replace(" ", "_").replace(':','-') + ".txt"
            else:
                self.__commslogfilename = os.path.expanduser("~/commslog_port" + str(self.__port) + "_" + 
                            time.asctime().replace(" ", "_").replace(':','-') + ".txt")

            logfilename = os.path.expanduser("~/commslog_" + loggingtimestring + ".txt")
        self.__commslogfilename=logfilename
        print 'OIF Logging : %r' % (self.__OIFlogging)
        print 'Log File    : %s' % (self.__commslogfilename)
        return(self.__commslogfilename)         
   
    def compresslog(self):
        if sys.hexversion > 0x02060000:
            bz2filename = self.__commslogfilename.replace('.txt','.txt.bz2')
            if not os.path.isfile(self.__commslogfilename):
                print "No comms log file to compress"
                return
            if os.path.isfile(bz2filename):
                print "zipped file exists, not overwriting" # todo: append
                return
            print 'Compressing',self.__commslogfilename,'->',bz2filename
            outfile = bz2.BZ2File(bz2filename,'bw')
            outfile.write(open(self.__commslogfilename,'r').read())
            outfile.close()
            os.remove(self.__commslogfilename)  # danger: sanitize
        else:
            print 'Log compression not supported in this version of python'
            
    def readx99(self):
        if self.__inTMode==True:
            print 'In t mode, readx99 not working'
            return
        self.writedatanoreply(Register.Register(address=0x99,data=0x1234),write=False)
        dataformat = ord(self.read(1,incomplete=True))
        databytes = ord(self.read(1,beginning=False,incomplete=True))
        if (databytes == 0x99):
            self.read(2)
            print "x99 Error: Password not set?"
            return(self.__dummyx99data)
        
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
                ["f","sled_current"        ,"A" ],
                ["f","photodiode_current"  ,"uA" ],
                ["f","sled_temperature"    ,"degC" ],
                ["f","gain_medium_current" ,"mA" ]
            ] 
        elif dataformat == 3:
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
                ["f","filter1_power"       ,"mW" ],
                ["f","filter2_power"       ,"mW" ],
                ["f","sled_current"        ,"A" ],
                ["f","photodiode_current"  ,"uA" ],
                ["f","sled_temperature"    ,"degC" ],
                ["f","gain_medium_current" ,"mA" ]
            ] 
        else:
            self.read(databytes,beginning=False)
            print "x99 Error: unrecognized data format"
            return(self.__dummyx99data)
        
        if (databytes != len(datastructure)*4):
            self.read(databytes,beginning=False)
            print "x99 Error: incorrect data structure"
            return(self.__dummyx99data)
            
        
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
            [5,"cavitylocked"],
            [6,"freqofflocked"],
            [7,"powerlocked"],
            [8,"f1locked"],
            [9,"f2locked"],
            [10,"siblocklocked"],
            [11,"sledlocked"],
            [12,"powertune"],
            [13,"freqtune"]
		]	
        
        class x99:
            def __repr__(self):   
                returnval=['x99data format v'+str(dataformat)+':\n']
                padding = len(max([a for a in dir(self) if not a.startswith('__')] + map(operator.itemgetter(1),datastructure),key=len))
                for vartype,varname,units in datastructure:
                    if varname not in ['stateflags','tmpdebug','tmpdebugU32','tmpdebugU32_2']:
                        returnval.append( ' '.join([varname.rjust(padding),'=',str(getattr(self,varname)),units,'\n']) )
                for statebit,varname in statebits:
                    returnval.append( ' '.join([varname.rjust(padding),'=',str(getattr(self,varname)),'\n']))
                for varname in [a for a in dir(self) if not a.startswith('__') and 
                           not a in map(operator.itemgetter(1),datastructure) and 
                           not a in map(operator.itemgetter(1),statebits) and 
                           not a in ['stateflags','tmpdebug','tmpdebugU32','tmpdebugU32_2']]:
                    returnval.append( ' '.join([varname.rjust(padding),'=',str(getattr(self,varname)),'\n']) )
                #returnval.append( 'tunerstate'.rjust(padding)+ ' = ' + self.tunerstate )
                return(''.join(returnval))

        x99dat = x99()
        
        for vartype,varname,units in datastructure:
            rawdata=self.read(4,beginning=False,incomplete=(varname != datastructure[-1][1]))
            decodeddata = struct.unpack('>' + vartype,rawdata)[0]
            setattr(x99dat, varname, decodeddata)

        for statebit,varname in statebits:
            setattr(x99dat, varname, (x99dat.stateflags & (1 << statebit)) !=0 )  

        x99dat.tunerstate = tunerstates[ x99dat.stateflags & 0x0F ][1]
                
        if (self.__dummyx99data is None):
            self.__dummyx99data = x99dat
            for varname in [a for a in dir(self.__dummyx99data) if not a.startswith('__')]:
                setattr(self.__dummyx99data, varname, None)

        return(x99dat)

    def getdummyx99dat(self):
        return self.__dummyx99data

    def setpassword(self,passwordlevel=3):
        passwords = [0x0000,0x0209,0xEE75,0xC3B2,0x632A,0xB5F1]
        for i in range(0,passwordlevel+1):
            level=self.register(Register.Register(address=0x99,data=passwords[i]),write=True)
        if (level[0] == 'OK'):
            print "Password level",level[1].data()
        else:
            print 'Unable to set password' 

    def __connect(self, port, baud):
        self.disconnect()
        self.__baud = baud
        self.__port = port
        if (self.__OIFlogging):
            # with open(self.__commslogfilename, "a") as oiflogfile:
            oiflogfile = open(self.__commslogfilename, "a")
            oiflogfile.write("# connecting to port " + str(port) + " at " + time.strftime("%a %d %b %Y %H:%M:%S %Z") + "\n")
            oiflogfile.flush()
        else:
            print self.hilite("Warning: Not logging OIF transactions. Use\n it.logfile(<filename>) to set log filename and\n it.logging(True) to enable logging",False,True)
        
        # timeout is 200ms for firmware upgrade
        self.__link = serial.Serial(self.__portprefix + str(port), baud, timeout = 0.06)
            
    def setportprefix(self, portprefix = None):  # usually 'com', '/dev/ttyS', or '/dev/ttyUSB'
        if portprefix is None:
            return(self.__portprefix)
        else:
            self.__portprefix = portprefix


    def connect(self, port = 1, baud = None):
        if self.__inTMode:
            return
        '''Connect to a port, return tuple (baud_rate, status_string)
        When baud is not give, it will try to auto detect.'''
        self.disconnect()
        #if self.__debug_level & self.DEBUG_FUNCTION:
        #    stack = StackMarker('connect')
   
        if baud == None:
            #baud = 115200
            baud = 9600
        if baud != None:
            self.__baud = baud
            self.__connect(port, baud)
            #
            #in case micro ITLA is using picassoTalk,
            #we send the command to switch back to MSA
            #However, if the laser is already in MSA, then the command should not impact the laser
            #self.sync()
            print 'MSA mode'
            self.write('\x20\x27\x27\x27')  # x27 = '(single quote) aborts picasso
            self.read(4)
            time.sleep(0.03)    # cleans MSA buffer -> timeout
            self.sync()
            #
            return (baud, 'Connected - serial port opened')
        else:
            bauds = [9600, 19200, 38400, 57600, 115200]
            command = Register.Register(Register.IOCAP)
            for i in bauds:
                tries = 2
                while tries > 0:
                    try:
                        self.__connect(port, i)
                    except:
                        return (0, 'Port unavailable')
                    try:

                        #print 'BAUD=============>', i
                        status, response = self.nop()
                        #print status
                        if status == 'OK':
                            self.__baud = i
                            return (i, 'Connected')
                    except:
                        self.reset()
                    tries -= 1
            self.__baud = 0
            return (0, 'Unit not responding')
        
    def sync(self):
        'sync with port'
        self.reset()
        
    def disconnect(self):
        if self.__inTMode:
            return
        'Disconnect from port'
        self.__baud = 0
        if self.__link != None:
            print 'Releasing the serial port'
            self.__link.close()
            self.__link = None
            if (self.__OIFlogging):
                oiflogfile = open(self.__commslogfilename, "a")
                oiflogfile.write("# disconnecting from port " + str(self.__port) + " at " + time.asctime().replace(" ", "_").replace(':','-') + "\n")
                oiflogfile.flush()


    def flushBuffer(self):
        try:
            #read a large number of bytes without keeping the result
            self.read(0xFFFF)
        except:
            pass
    '''
    def debugLevel(self, level = None):
        'Get/Set debug level'
        if level != None:
            self.__debug_level = level
        return self.__debug_level
    '''    
    def debugRS232(self, level = None):
        'Get/Set debug level'
        if level != None:
            self.__debug_rs232 = level
        return self.__debug_rs232
    
    def laser(self, level = None):
        'Get/Set debug level'
        if level != None:
            self.__laserSelect = level
        return self.__laserSelect
    
    def toModulePacket(self):
        'Return last packet sent to module'
        return self.__module_packet
    
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
        #if self.__debug_level & self.DEBUG_FUNCTION:
        #    stack = StackMarker('register')
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

            #if self.__debug_level & ITLA.DEBUG_MODULE_BOUND_REGISTER:
            #    print '%s Mode = %s, To Module Register %s' % ('-' * 23, packet.mode(), '-' * 23)
            #    print register

            p = self.packet(packet)
            if p == None:      # check for a complete response
                status = 'No response'
                return (status, self.__register)

            address = ord(p.buffer()[1])
            data = struct.unpack('>H', p.buffer()[2:])[0]
            self.__register = Register.Register(address, data)

            #if self.__debug_level & ITLA.DEBUG_HOST_BOUND_REGISTER:
            #    print '%s Mode = %s, To Host Register %s' % ('-' * 24, packet.mode(), '-' * 24)
            #    print self.__register

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
                
        return (status, self.__register)

    def write(self, buffer):
        # needs a way to flush to eleminates leftover of previous commands
        #self.flushBuffer()
        self.__link.flushInput()
        if (self.__OIFlogging):
            oiflogfile = open(self.__commslogfilename, "a")
            oiflogfile.write("%04.4fs " % (time.time() - self.__logstarttime))
            oiflogfile.write('Tx: ')
            for c in buffer:
                oiflogfile.write( '%02X ' % ord(c) )
            oiflogfile.flush()
        if self.__debug_rs232 !=0:
            print 'Tx: '
            for c in buffer:
                print '%02X ' % ord(c) 
        self.__lastwritetime = time.time()
        return self.__link.write(buffer)
        
    def read(self, byte_count = 1, maxRetry = 8, beginning=True, incomplete=False): # call with maxRetry=0 to do a dummy read (for log file completeness)
        string = ''
        retries = 0
        writetimems = (time.time() - self.__lastwritetime) * 1000 # dummy value
        while(retries < maxRetry):
            string += self.__link.read(byte_count)
            writetimems = (time.time() - self.__lastwritetime) * 1000
            if (len(string) >= byte_count):
                if self.__debug_rs232 !=0:
                    print 'Rx: '
                    for c in string:
                        print '%02X ' % ord(c) 
                    if retries:
                        print 'retries %d' % (retries)
                if (self.__OIFlogging):
                    oiflogfile = open(self.__commslogfilename, "a")
                    if beginning:
                        oiflogfile.write('Rx: ')
                    for c in string:
                        oiflogfile.write( '%02X ' % ord(c) )
                    if not incomplete:
                        oiflogfile.write('%2.1fms\n' % writetimems)
                    oiflogfile.flush()
                return string
            retries += 1
            time.sleep(0.1)
        if (self.__OIFlogging):
            oiflogfile = open(self.__commslogfilename, "a")
            if beginning:
                oiflogfile.write('Rx: ')
                oiflogfile.write( 'NA ' * (byte_count - len(string)) )
            if not incomplete:
                oiflogfile.write('%2.1fms\n' % writetimems)
            oiflogfile.flush()
        if maxRetry > 0:
            print 'Expected %d bytes, got %d' % (byte_count, len(string))
            self.__droppedbytecount += byte_count - len(string)
        return string
    
    def printlog( self, lines = 20 ):
        try:
            f = open(self.__commslogfilename, "r")
        except:
            if (not self.__OIFlogging):
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
            print "Log file: " + self.__commslogfilename
            print "Showing last",lines,"lines:"
            print '\n'.join(all_read_text.splitlines()[-lines:])
        else:
            print 'Log print not supported in this version of python'


    def moduleSelect(self):
        'Toggle the module select line'
        self.__link.setRTS(0)
        self.__link.setRTS(1)
    
    def reset(self):
        'Resynchronize the transmit and receive buffer'
        print 'Flushing RS232 Buffers'
        self.__link.flushInput()
        for i in range(5):
            self.__lastwritetime = time.time()
            try:
                if (self.__OIFlogging): # dummy blank 4-byte write
                    oiflogfile = open(self.__commslogfilename, "a")
                    oiflogfile.write("%04.4fs " % (time.time() - self.__logstarttime))
                    oiflogfile.write('Tx: ')
                    oiflogfile.write( 'NA ' * 4)
                    oiflogfile.flush()
                    time.sleep(0.001)
                self.read(4)
                break
            except:
                time.sleep(0.001)
                pass
            #self.write('0')
        
    def packet(self, packet = None, computeChecksum = 1):
        'Send packet or return last packet received'
        if packet != None:
            if self.laser() == 2:	
                packet.laser('LASER1')      # laser 2 set bit 26
            else:
                packet.laser('LASER0')      # 0 or 1 clear bit 26

            if computeChecksum:
                packet.checksum(packet.computedChecksum())

            self.__module_packet = packet
            
            #if self.__debug_level & ITLA.DEBUG_MODULE_BOUND_PACKET:
            #    print '%s To Module Packet %s' % ('-' * 31, '-' * 31)
            #    print repr(packet)
            #if self.__debug_level & ITLA.DEBUG_PACKET_STRING:
            #    print str(packet)

            if not self.__retrying:  # prevent retry recursion
                self.__retrying = True
                # Retry if no answer
                for mstoggleretry in range(2):
                    for retry in range(3):
                        if retry:
                            print 'retry',
                        self.write(packet.buffer())
                        self.__packet = HostBoundPacket()
                        string = self.read(4)
                        if len(string) >= 4: 
                            self.__packet.buffer(string)
                            #if self.__debug_level & ITLA.DEBUG_HOST_BOUND_PACKET:
                            #    print '%s To Host Packet %s' % ('-' * 32, '-' * 32)
                            #    print repr(self.__packet)
                            #if self.__debug_level & ITLA.DEBUG_PACKET_STRING:
                            #    print str(self.__packet)
                            self.__retrying = False
                            return self.__packet
                    print 'Toggling MS line'
                    oldbaud = self.__baud
                    mstogglebaud = 9600 # todo: allow user to set
                    self.logentry("Toggling MS line")
                    self.moduleSelect() 
                    if (mstogglebaud != oldbaud):
                        self.__connect(self.__port,mstogglebaud)
                        self.baudrate(oldbaud) # reset the baud
                self.__retrying = False
                
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

    def dbgTemps(self, sel=0):
        'Return tuple (status_string, register)'
        return self.register(Register.Register(Register.DBG_TEMPS, sel))
        
    def isLocked(self, timeout = 25.0):
        'Query NOP until pending is cleared, timeout in seconds. Return (boolean, lock_time_in_seconds)'
        start = time.time()
        while True:
            #print 'checking', time.time() - start
            status, nop = self.nop()
            if nop.fieldPending().value() == 0:
                return True, time.time() - start
            if (time.time() - start) >= timeout:
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
            message += struct.pack('B', response.data() & 0xFF)

        return status, (byteCount, message)
    
    def monitor(self, addr = 0x8068):
        #Get Monitor 2 data bytes, 
        'Return tuple (status_string, register)'
        return self.register(Register.Register(Register.MONITOR, addr))

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
        if (self.__OIFlogging):
            oiflogfile = open(self.__commslogfilename, "a")
            oiflogfile.write("# " + "%04.4fs: " % (time.time() - self.__logstarttime) + string + "\n")
            oiflogfile.flush()
        else:
            print self.hilite("Warning: Not logging OIF transactions. Use\n it.logfile(<filename>) to set log filename and\n it.logging(True) to enable logging",False,True)
            print 'Unable to write log entry', string
        return
        
    
    def serNo(self):
        'Return tuple (status, (byte_count, string))'
        serialnum = self.aeaString(Register.SERNO)
        if (self.__OIFlogging):
            oiflogfile = open(self.__commslogfilename, "a")
            oiflogfile.write("# unit serial number: " + str(serialnum[1][1]) + "\n")
            oiflogfile.flush()
        else:
            print self.hilite("Warning: Not logging OIF transactions. Use\n it.logfile(<filename>) to set log filename and\n it.logging(True) to enable logging",False,True)
        return serialnum
    
    def buildstring(self):
        buildstring = self.aeaString(0xB0)[1][1].split('\x00',1)[0]
        if (self.__OIFlogging):
            oiflogfile = open(self.__commslogfilename, "a")
            oiflogfile.write("# FW build string: " + str(buildstring) + "\n")
            oiflogfile.flush()
        else:
            print self.hilite("Warning: Not logging OIF transactions. Use\n it.logfile(<filename>) to set log filename and\n it.logging(True) to enable logging",False,True)
        return buildstring
    
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
        curr_laser = self.laser()
        if baudrate != None:
            status, response = self.ioCap(baudrate, 1)
            if status == 'OK':            
                rate = response.fieldCurrentBaudRate().cipher()
                if rate != str(baudrate):
                    print 'Unable to retrieve Lasers baud rate', str(baudrate)
            else:
                print 'Unable to configure Laser2 baudrate'

            # Disconnect and connect with new baudrate
            self.disconnect()
            self.__connect(self.__port, baudrate)

        if curr_laser > 0:   
            self.laser(1)
            time.sleep(0.030)    #allow timeout to clean buffers
            status1, response1 = self.ioCap()      # Read baud rate is properly configured
            self.laser(2)
            time.sleep(0.030)    #allow timeout to clean buffers
            status, response = self.ioCap()      # Read baud rate is properly configured
            self.laser(curr_laser)      #restore original setting

            if status == 'OK':
                rate = response.fieldCurrentBaudRate().cipher()
                print 'Laser2 baud rate: ', rate
            if status1 == 'OK':
                rate1 = response1.fieldCurrentBaudRate().cipher()
                print 'Laser1 baud rate: ', rate1

            if status != 'OK':
                return (status, 0)
            if status1 != 'OK':
                return (status1, 0)
            if baudrate != None and ((rate != str(baudrate)) or (rate1 != str(baudrate))):
                return 'Unable to configure baud rate ' + str(baudrate), 0
            
        else:           # single uITLA
            # Read to confirm baud rate is properly configured
            time.sleep(0.030)    #allow timeout to clean buffers
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
    
    def __frequency(self, frequency1, frequency2):
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
        
        return self.__frequency(Register.FCF1, Register.FCF2)
    
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
        return self.__frequency(Register.LF1, Register.LF2)

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
        return self.__frequency(Register.LFL1, Register.LFL2)
    
    def lfh(self):
        'Get laser\'s last frequency in THz, return (status_string, fTHz)'
        return self.__frequency(Register.LFH1, Register.LFH2)

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

    def __upgradeFirmware(self, filename, version):
        # Open file 
        file = open(filename, 'rb')
        text = file.read()
        file.close()
        if version.lower().startswith('interrupt'):
            type = 3
        elif version.lower().startswith('maintain'):
            type = 1
        else:
            return 'Invalid version'
        
        start = time.time()		# time the download
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

            print 'Booting Monitor'
            time.sleep(1)		#pb change to 0.2 sec
            self.__link.flushInput()
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
            oldDebug = self.__debug_rs232;
            for i in range(0, len(text), 2):
                packet.data(struct.unpack('>H', text[i : i + 2])[0])
                packet.checksum(packet.computedChecksum())
                self.write(packet.buffer())
                response = self.read(4)
                if len(response) != 4:
                    return('Aborting upgrade')
                if ord(response[1]) & 0x3 != 0:           
                    return ('Write failed', i, map(hex, map(ord, response)))
                
                if(self.__debug_rs232):
                    self.__debug_rs232 = 0
                #print a dot to let the operator know that we are working...
                cnt = cnt+1
                if (cnt >= 512):    
                    cnt = 0
                    dotCnt = dotCnt+1
                    if (dotCnt >= 32):
                        dotCnt = 0
                        cnt16K += 2
                        if cnt16K == 6:
                            self.__debug_rs232 = 1
                        print '%dK' % (cnt16K * 16)
                    else:
                        print '.',
                    sys.stdout.flush() 
                    time.sleep(0.001)               

            # Read the response packets left-over on the UART buffer
            #pb self.flushBuffer()
            self.__link.flushInput()
            self.__debug_rs232 = oldDebug

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
            time.sleep(0.5)
            print 'Seconds elapsed', time.time() - start
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
        self.__link.flushInput()

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
        oldDebug = self.__debug_rs232;
        for i in range(0, len(text), 2):
            packet.data(struct.unpack('>H', text[i : i + 2])[0])
            packet.laser('LASER0')
            packet.checksum(packet.computedChecksum())
            self.write(packet.buffer())
            response = self.read(4)
            if len(response) != 4:
                self.__debug_rs232 = oldDebug
                return('Aborting upgrade: Laser2')
            if ord(response[1]) & 0x3 != 0:           
                self.__debug_rs232 = oldDebug
                return ('Write failed: Laser2', i, map(hex, map(ord, response)))
            packet.laser('LASER1')
            packet.checksum(packet.computedChecksum())
            self.write(packet.buffer())
            response = self.read(4)
            if len(response) != 4:
                self.__debug_rs232 = oldDebug
                return('Aborting upgrade: Laser1')
            if ord(response[1]) & 0x3 != 0:           
                self.__debug_rs232 = oldDebug
                return ('Write failed: Laser1', i, map(hex, map(ord, response)))
            
            if(self.__debug_rs232):
                self.__debug_rs232 = 0
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
        self.__link.flushInput()
        self.__debug_rs232 = oldDebug

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
        time.sleep(0.2)     # Allow laser 2 to boot --> drive laser 1
        self.laser(1)
        status, NA = self.dlConfig(init_run = 1, runv = type)
        if (status != 'OK'):
            return('Laser1: Init_run ' + status)

        # Allow firmware to boot
        time.sleep(0.2)
        self.laser(curr_laser)
        print 'Seconds elapsed', time.time() - start
        return('Download Complete!')

    def upgrade(self, target, filename, version = 'Interrupting'):
        if ('APPLICATION'.startswith(target.upper())):
            return(self.__upgradeFirmware(filename, version))
        else:
            raise 'Target type unknown.' 

    def upload(self, filename):
        start = time.time()
        
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

        return 'OK', time.time() - start


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
        start = time.time()
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
                duration = float(time.time() - start)
                break
            elif (time.time() - start) > timeout:
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
