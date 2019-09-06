from gpib import *
import time
import socket as sok
import serial as ser
import win32event as w
import win32api
import array
import types
import select
import sys
import os
from TExException import *
from TExException import _warn
#d = dir();d.sort();print d

def debug(*arg,**karg):
    'prints out TExdebug information to Win32 Debug Stream'
    if __debug__:
        tempstr = ""
        for a in arg:
            tempstr += "%s "%(a)
        win32api.OutputDebugString(tempstr)
        for k in karg:
            win32api.OutputDebugString("%s : %s"%(k,karg[k]))
try:
    dbg = int(os.environ['INSTR_DBG'])
    print 'Debug',dbg
except:
    dbg = 0
try:
    printcmd = int(os.environ['INSTR_PrintCmd'])
except:
    printcmd = 0



if warn: import traceback,warnings

try:
    ver = GetVersion()[0]
    vern = ver.split('.')
    Version = float(vern[0]) + float(vern[1])/100.0
except:
    Version = 1.0

if Version < 2.0:
    debug(BaseDLLVersion = Version)
    raise Exception,"Incorrect GPIB DLL Version. GPIB V 2.x.x.x required"


class InstrumentException(CommunicationError):pass
class GPIBException(InstrumentException):pass

class GPIBTimeout(TimeOutError,GPIBException):pass
class TCP_IPTimeout(TimeOutError):pass
class SerialTimeout(TimeOutError):pass






class Base(object):
    __Type = 0; # 0: GPIB, 1: RS232 , 2 : TCPIP
    __sDevicedict = {}
    __sCounter = {}
    __sMutex = {} # inorder to be thread safe, you gotta have Mutex lock on device handles while writing and reading
    __sConnectCntr = {}
    def __init__(self, board, pad,type = 0):
        self.pid = self.__class__.__name__
        self.board = board
        self.pad = pad
        self.Device = None
        self.disconnected = 1
        self.connectcount = 0
        self.__Type = type
        self.__Name = ''
        if self.__Type == 0:
            self.key = "%02d-%02d" %(board,pad)
        elif self.__Type == 1:
            self.key = "%03d-%d" %(board,pad)
            self.__strCommandTerm = '\r\n'
            self.__strReplyTerm = '\r\n'
            
        elif self.__Type == 2:
            board.strip()
            parsed = board.split('.')
            board = "%03d.%03d.%03d.%03d"%(int(parsed[0]),int(parsed[1]),int(parsed[2]),int(parsed[3]))
            board = self.board
            self.key = "%s-%d" %(board,pad)
        try :
            self.__class__.__sDevicedict[self.key]
            self.__class__.__sCounter[self.key] += 1
        except:
            self.__class__.__sDevicedict.update({self.key:None})
            self.__class__.__sCounter.update({self.key:1})
            self.__class__.__sConnectCntr.update({self.key:0})
            if dbg: print 'Debug',dbg
            if dbg: print "Creating Mutex :",self.key
            self.__class__.__sMutex.update({self.key:w.CreateMutex(None,0,self.key)})
            debug(CreateMutex=self.key)
            if not self.__class__.__sMutex[self.key]:
                raise WindowsError,"Synchronziation object creation failed. CreateMutex : %s Failed"%self.key


        if dbg: print "__sDevicedict :",self.__class__.__sDevicedict
        if dbg: print "__sCounter :",self.__class__.__sCounter
        if dbg: print "key :",self.key
        
    def getCommandTermChar(self):
        return self.__strCommandTerm
    def getReplyTermChar(self):
        return self.__strReplyTerm
    def setCommandTermChar(self, strChar):
        self.__strCommandTerm = strChar
    
    def setReplyTermChar(self, strChar):
        self.__strReplyTerm = strChar
    def setTermChar(self, strTerm):
        self.__strReplyTerm = strTerm
        self.__strCommandTerm = strTerm
    
    def __del__(self):#disconnect the instrument if it goes outof scope even if no explicit command is given
        'disconnect the instrument if it goes outof scope even if no explicit command is given'
        if self.__class__.__sDevicedict[self.key] != None:
            if not self.disconnected:
                _warn("Instrument instance of %s Not disconnected explicitly"%self.pid)
                time.sleep(5)
                self.disconnect()
                if dbg: print "disconnected..."
        self.__class__.__sCounter[self.key] -= 1
        if not self.__class__.__sCounter[self.key]:
            print "Destroying Mutex :",self.key
            debug(DestroyMutex=self.key)
            win32api.CloseHandle(self.__class__.__sMutex[self.key])
            del self.__class__.__sDevicedict[self.key]

    def __AcquireMutex__(self):
        result = w.WaitForSingleObject(self.__class__.__sMutex[self.key],10000)
        if result == w.WAIT_ABANDONED or result == w.WAIT_TIMEOUT:
            raise WindowsError,"Lock on GPIB instrument not possible : %s for %s Instance of:%s"%(['WAIT_ABANDONED','WAIT_TIMEOUT'][[w.WAIT_ABANDONED,w.WAIT_TIMEOUT].index(result)],self.key,self.pid)
        if dbg: print ("Lock Acquired for " + self.key)

    def __ReleaseMutex__(self):
        w.ReleaseMutex(self.__class__.__sMutex[self.key])
        if dbg: print ("Lock Released for " + self.key)

    def __repr__(self):
        if self.__Type == 0:
            s = 'Board: %d\n'%(self.board)
            s += 'GPIB Address: %d'%(self.pad)
        elif self.__Type == 1:
            s = 'Com %d\nBaud %d'%(self.board,self.pad)
        elif self.__Type == 2:
            s = 'IP : %s \nPort : %s\n'%(self.board,self.pad)
        return(s)

    def disconnect(self):
        # Take the device offline.
        if dbg: print "inside disconnect"
        if self.disconnected:
            debug("Disconnecting instrument that has been already disconnected: Instance of :" + self.pid)
            _warn("Disconnecting instrument that has been already disconnected: Instance of :" + self.pid)
            if dbg: print "Already Disconnected"
            return
        self.disconnected = 1
        self.connectcount -= 1
        if dbg: print "Type :",self.__Type,self.__class__.__sCounter[self.key],self.__class__.__sConnectCntr[self.key]
        self.__class__.__sConnectCntr[self.key] -= 1
        if not self.__class__.__sConnectCntr[self.key] == 1:
            if self.__Type == 0:
                self.__closeHW()
                self.device = self.Device = None#legacy support
                self.__class__.__sDevicedict[self.key] = None
               # del self.__class__.__sMutex[self.key]
                if dbg: print self.key, " disconnected"
            elif self.__Type == 1:
                self.__closeHW()
                self.device = self.Device = None
                self.__class__.__sDevicedict[self.key] = None
            elif self.__Type == 2:
                self.__class__.__sDevicedict[self.key].close()
                self.__class__.__sDevicedict[self.key] = None
                self.device = self.Device = None#legacy support
##            self.disconnected = 1
        else:
            if self.Device:
                pass#self.__class__.__sCounter[self.key] -=1
            else:
                debug("disconnect attempted without connection")

            self.device = self.Device = None#legacy support
            if dbg: print self.key, " count :",self.__class__.__sCounter[self.key]

    def SetTimeout(self,ibTMO):
#define TNONE    0   /* Infinite timeout (disabled)        */
#define T10us    1   /* Timeout of 10 us (ideal)           */
#define T30us    2   /* Timeout of 30 us (ideal)           */
#define T100us   3   /* Timeout of 100 us (ideal)          */
#define T300us   4   /* Timeout of 300 us (ideal)          */
#define T1ms     5   /* Timeout of 1 ms (ideal)            */
#define T3ms     6   /* Timeout of 3 ms (ideal)            */
#define T10ms    7   /* Timeout of 10 ms (ideal)           */
#define T30ms    8   /* Timeout of 30 ms (ideal)           */
#define T100ms   9   /* Timeout of 100 ms (ideal)          */
#define T300ms  10   /* Timeout of 300 ms (ideal)          */
#define T1s     11   /* Timeout of 1 s (ideal)             */
#define T3s     12   /* Timeout of 3 s (ideal)             */
#define T10s    13   /* Timeout of 10 s (ideal)            */
#define T30s    14   /* Timeout of 30 s (ideal)            */
#define T100s   15   /* Timeout of 100 s (ideal)           */
#define T300s   16   /* Timeout of 300 s (ideal)           */
#define T1000s  17   /* Timeout of 1000 s (ideal)          */

        self.__AcquireMutex__()
        try:
            ibconfig(self.Device,IbcTMO,ibTMO)
        finally:
            self.__ReleaseMutex__()

    def connect(self):
        'initializes the hardware. Instrument Name is created here'
        if dbg: print "inside connect"
        self.__AcquireMutex__()
        try:
            self.connectcount +=1
            if self.Device:
                debug("connecting to the same instrument using the same instance too many times.... Count : %s InstanceOf: %s"%(self.connectcount,self.pid))
                _warn("connecting to the same instrument using the same instance too many times.... Count : %s InstanceOf: %s"%(self.connectcount,self.pid))
                return None
            if (self.__class__.__sDevicedict[self.key] != None):
                self.Device = self.__class__.__sDevicedict[self.key]
                self.device = None#self.Device #legacy support <dropping all legacy support)
                self.disconnected = 0
                self.__class__.__sConnectCntr[self.key] += 1
                if dbg: print "Instrument already connected",self.Device
                return None

            self.__class__.__sDevicedict[self.key] = self.__initHW()
            self.Device = self.__class__.__sDevicedict[self.key]
            self.device = None#self.Device #legacy support <dropping all legacy support)
            self.__class__.__sConnectCntr[self.key] = 1 #this will have to be the first connect
            self.disconnected = 0

        finally:
            self.__ReleaseMutex__()
            if dbg: print "inst connected (new)"
            #return self.Device

    def identity(self):
        self.__AcquireMutex__()
        try:
            if self.__Type == 0:
                ibclr(self.Device)
                cmd = '*IDN?'
                ibwrt(self.Device, cmd, len(cmd))
                # Remove the newline.
                s = ibrd(self.Device, 255)[:-2]
                self.__Name = s
            elif self.__Type == 1:
                s = None
                _warn("supported only for gpib")
            elif self.__Type == 2:
                s = None
                _warn("supported only for gpib")
            return s
        finally:
            self.__ReleaseMutex__()


    def reset(self):
        self.__AcquireMutex__()
        if self.__Type == 0:
            ibclr(self.Device)
            cmd = '*RST'
            ibwrt(self.Device, cmd, len(cmd))
            self.__ReleaseMutex__()
            s = None
        elif self.__Type == 1:
            self.Device.write('*RST\n')
            s = None
            self.__ReleaseMutex__()
            #_warn("supported only for gpib")
        elif self.__Type == 2:
            s = None
            self.__ReleaseMutex__()
            _warn("supported only for gpib")
        return s

    def poll(self):
        self.__AcquireMutex__()
        try:
            if self.__Type == 0:
                count = 0
                while (not (ibrsp(self.Device) & (1 << 4))):
                    time.sleep(0.1)
                    if (count > 50):
                        raise GPIBTimeout,"Instrument Busy"
                    count += 1
            elif self.__Type == 1:
                s = None
                _warn("supported only for gpib")
            elif self.__Type == 2:
                s = None
                _warn("supported only for gpib")
        finally:
            self.__ReleaseMutex__()
    def write(self,Str):
        self.__AcquireMutex__()
        try:
            if self.__Type == 0:
                if printcmd:print Str
                if type(Str) == types.ListType:
                    L = len(Str)
                    Str = array.array('B',Str).tostring()
                    if dbg:print Str
                else:
                    L = len(Str)
                try:
                    ibwrt(self.Device,Str,L)
                except Exception,e:
                    try:
                        ibwrt(self.Device,Str,L)
                    except Exception,e:
                        raise GPIBException(e)
            elif self.__Type == 1:
                #_warn("Not yet Implemented")
##                if Str[-1] != '\n':
##                    Str += '\n'
                if not Str.endswith(self.__strCommandTerm):
                    Str += self.__strCommandTerm
                self.__debugPrint(Str)
                self.Device.write(Str)
            elif self.__Type == 2:
                r, w, e = select.select([],[self.Device],[], None)
                if not w:
                    raise InstrumentException,'Socket not writable.'
                else:
                    self.Device.send(Str)
        finally:
            self.__ReleaseMutex__()

    def read(self,buffer=1000,timeout = 2):
        self.__AcquireMutex__()
        try:
            if self.__Type == 0:
                try:
                    return ibrd(self.Device,buffer)
                except TimeOutException, e:
                    raise GPIBTimeout(e)
                except Exception,e:
                    raise GPIBException(e)
            elif self.__Type == 1:
                #raise Usage,"Not yet Implemented"
                #<old>
##                strResp = self.Device.readline()
##                strResp = strResp.strip('\n')
##                nPos = strResp.find( '<END>' )
##                if nPos == -1:
##                    return strResp
##                else:
##                    return strResp[:nPos]
                #</old>

                #<new>
                strResp = ''
                blnFinished = 0
                while 1:
                    strChar = self.Device.read()
                    if strChar == '':
                        break
                    strResp += strChar 
                    if len(strResp) > 1:
                        if strResp.endswith(self.__strReplyTerm):
                            self.__debugPrint(strResp)
                            strResp = strResp[:- len(self.__strReplyTerm)]
                            break
                
                return strResp
                #</new>                
            elif self.__Type == 2:
                r, w, e = select.select([self.Device], [], [], 2)
                if dbg: print r
                if not r:
                    raise InstrumentException,"Could not receive data from socket"
                else:
                    return self.Device.recv(buffer)
        finally:
            self.__ReleaseMutex__()


    def query(self,Str,buffer=1000,delay=.005):
        self.__AcquireMutex__()
        try:
            try:
                self.write(Str)
                time.sleep(delay)
                return self.read(buffer)#[:-2] #gpib always returns a /r/n
            except Exception,e:
                raise e##Automatically generated code Do not modifiy
        finally:
            self.__ReleaseMutex__()

    def __initHW(self):
        self.__AcquireMutex__()
        try:
            if self.__Type == 0:
                self.Device = ibdev(self.board, self.pad, 0, T1s, 1, 0)
            elif self.__Type == 1:
                #raise Usage,"Not yet Implemented"
                self.Device = ser.Serial(self.board-1, self.pad, timeout=3.0) # comm port, baud rate
                # should have already 'connected' in constructor
                self.Device.flushInput()
                self.Device.flushOutput()
                return self.Device                
            elif self.__Type == 2:
                self.Device = sok.socket(sok.AF_INET,sok.SOCK_STREAM)
                self.Device.connect((self.board,self.pad))
            return self.Device
        finally:
            self.__ReleaseMutex__()

    def __closeHW(self):
        if dbg: print "inside close HW"
        self.__AcquireMutex__()
        try:
            if self.__Type == 0:
                if self.Device:
                    self.Device = ibonl(self.__class__.__sDevicedict[self.key], 0)
                    print "Cleared HW Handle :%s"%self.key
                try:
                    self.__class__.devicedict[self.key] = -1 #backwards compatiblity
                except:
                    pass
            elif self.__Type == 1:
                #raise Usage,"Not yet Implemented"
                self.Device.close()                
            elif self.__Type == 2:
                self.Device.close()
            self.Device = None
            self.__class__.__sDevicedict[self.key] = None
            #self.__class__.__sCounter[self.key] -=1
            return self.Device
        finally:
            self.__ReleaseMutex__()
            
    def __debugPrint(self, strDebug):
        return
        strDebug = strDebug.replace('\r', 'CR')
        strDebug = strDebug.replace('\n', 'LF')
        print strDebug
        