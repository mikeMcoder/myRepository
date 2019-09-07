'''
NeoPhotonics CONFIDENTIAL
Copyright 2003-2015 NeoPhotonics Corporation All Rights Reserved.

The source code contained or described herein and all documents related to
the source code ("Material") are owned by NeoPhotonics Corporation or its
suppliers or licensors. Title to the Material remains with NeoPhotonics Corporation
or its suppliers and licensors. The Material may contain trade secrets and
proprietary and confidential information of NeoPhotonics Corporation and its
suppliers and licensors, and is protected by worldwide copyright and trade
secret laws and treaty provisions. No part of the Material may be used, copied,
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

    $Source: /data/development/cvs/Lux/Python/TTM/System.py,v $
    $Revision: 1.43 $
    $Date: 2009/11/19 17:31:55 $
    $Name: HEAD $

'''
import os
import sys
import time
import PyTTXTalk


import Utility

if (os.name != 'posix'):
    pathdelimiter = '\\'
else:
    pathdelimiter = '/'

from Utility import *

MODULE_INDEX = 0
METHOD_INDICES = {
                  'version'             : 0,
                  'readRamBytes'        : 1,
                  'readFlashBytes'      : 2,
                  'writeRamBytes'       : 3,
                  'writeFlashBytes'     : 4,
                  'eraseFlashPage'      : 5,
                  'reset'               : 6,
                  'baudrate'            : 7,
                  'actuatoron'          : 8,
                  'actuatoroff'         : 9,
                  'it_command'          : 12
                  }

PROPERTIES = {'WRITE_CHUNK_SIZE': 16,
              'READ_CHUNK_SIZE': 16}

MAX_CDR_REG = 185

__CURRENT_PATH = os.path.split(os.path.abspath(__file__))[0]

DEBUG_SYSTEM = 0
def DebugOut(s):
    if DEBUG_SYSTEM:
        print s

class System:

    # Version type.
    FIRMWARE = 0
    BOARD = 1

    def __init__(self):
        DebugOut('System.__init__')
        
        self.__module = MODULE_INDEX
        self.__operation = METHOD_INDICES
        self.__dictionary = None
        self.__picassoTmode = False

    def dictionary(self, d = None):
        DebugOut('System.dictionary')

        if (d == None): return(self.__dictionary)

        self.__dictionary = d

    def __repr__(self):
        DebugOut('System.__repr__')
        
        string = ''

        return(string)

    def version_system(self):
        Utility.newOperation(self.__module, self.__operation['version'])
        PyTTXTalk.pushU32(0x00)
        Utility.sendPacket(1)
        v = Version()
        v.name(PyTTXTalk.popString())
        v.major(PyTTXTalk.popU8())
        v.minor(PyTTXTalk.popU8())
        v.patch(PyTTXTalk.popU8())
        v.build(PyTTXTalk.popU8())
        return(v)

    # 27 July 2009 : reboot the 8051 CPU
    def reset(self):
        global LaserType
        if LaserType == 3:
            print 'Resetting NANO...'
        else:
            print 'Resetting laser...'
        sys.stdout.flush() 
        newOperation(self.__module, self.__operation['reset'])
        sendPacket(1);               
        if LaserType == 3:
            time.sleep(5)               # wait for NANO to come up
        else:
            time.sleep(0.6)             # wait for laser to come up
        # flush buffer
        PyTTXTalk.read_bin(1000)        # allow time for uitla to clean up     


    def baudrate(self,baud_rate):
        DebugOut('System.baudrate %s' % (baud_rate))
        
        time.sleep(0.02)
        newOperation(self.__module,
                             self.__operation['baudrate'])
        PyTTXTalk.pushU32(baud_rate)
        sendPacket(1);       
        print 'setting baudrate done'
        
    def actuatoron(self):
        DebugOut('System.actuatoron')
        
        newOperation(self.__module,
                    self.__operation['actuatoron'])
        sendPacket(1)

    def actuatoroff(self):
        DebugOut('System.actuatoroff')
        
        newOperation(self.__module, self.__operation['actuatoroff'])
        sendPacket(1)  

    def send_code_switch_PicassoTalk(self):
        debug = None
        if PyTTXTalk.laser(debug) > 0:      #1, 2 = dual, 0 = single
            if PyTTXTalk.debugRS232(debug):
                print 'WR=> 0x67232323 switch laser1 to Engr mode'
            time.sleep(0.03)                #allow time for uitla to clean up     
            PyTTXTalk.write_bin('\x67\x23\x23\x23')   # for dual laser1
            PyTTXTalk.read_bin(1000)        #allow time for uitla to clean up     
        if PyTTXTalk.debugRS232(debug):
            if PyTTXTalk.laser(debug) > 0:
                print 'WR=> 0x01232323 switch laser2 to Engr mode'
            else:
                print 'WR=> 0x01232323 switch single laser to Engr mode'
        PyTTXTalk.write_bin('\x01\x23\x23\x23') 
        PyTTXTalk.read_bin(1000)        #allow time for uitla to clean up     
        self.__picassoTmode = True

    def send_code_abort_PicassoTalk(self):
        PyTTXTalk.write_bin('\x20\x27\x27\x27')  # x27 = '(single quote) aborts picasso
        PyTTXTalk.read_bin(1000)     # allow time to clean buffers
        self.__picassoTmode = False

    def picassoMode(self, mode=None):
        if mode is not None:
            self.__picassoTmode = mode
        return self.__picassoTmode
    
    def detectMode(self):
        global LaserType
        UNKNOWN = 0
        SINGLE = 1
        DUAL = 2
        NANO = 3
        LaserType = UNKNOWN;
        debug = None
        currLaser = PyTTXTalk.laser(debug)      #1, 2 = dual, 0 = single
        
        self.send_code_switch_PicassoTalk()
        if currLaser == 0:      # single laser
            try:
                firmware_version = self.version_system()
                if (firmware_version.name() == 'Sundial4S'):
                    LaserType = NANO
                else:
                    if (firmware_version.name() == 'Sundial3D'):
                        print 'Switching to dual laser(1)'
                        PyTTXTalk.laser(1)      #1, 2 = dual, 0 = single
                        currLaser = 1
                    else:
                        LaserType = SINGLE
            except:
                firmware_version = 'Not Connected!'
        if currLaser >= 1:      # dual laser
            PyTTXTalk.laser(1)
            try:
                firmware_version = self.version_system()
                if (firmware_version.name() != 'Sundial3D'):
                    print 'Switching to single laser(0)'
                    PyTTXTalk.laser(0)      #1, 2 = dual, 0 = single
                    currLaser = 0
            except:
                return (UNKNOWN, 'Not Connected!')   # error

            PyTTXTalk.laser(2)
            try:
                firmware_version1 = self.version_system()
            except:
                return (UNKNOWN, firmware_version)   # error
                
            PyTTXTalk.laser(currLaser)
            if (firmware_version == firmware_version1):
                LaserType = DUAL;
            else:
                return (LaserType, 'Different versions')   # error
        return (LaserType, firmware_version)   
        
    def getLaserType(self):
        global LaserType
        return LaserType
    
    def it_command(self, cmd=0x30210000):
        Utility.newOperation(self.__module, self.__operation['it_command'])
        PyTTXTalk.pushU32(cmd)
        sendPacket(1);
        reply = 0
        for i in range(4):
            data = PyTTXTalk.popU8()
            reply |= data << (i*8)
        #print 'cmd: %08X  reply: %08X' % (cmd,reply)
        return(reply)
                
class Version:

    FORMAT_STRING = 0
    FORMAT_INTEGER = 1

    def __cmp__(self, candidate):
        DebugOut('Version.__cmp__ %s' % (candidate))
        return(cmp(str(self), str(candidate)))

    def __init__(self):
        DebugOut('Version.__init__')
        self.__name = ''
        self.__major = 0
        self.__minor = 0
        self.__patch = 0
        self.__build = 0

    def __repr__(self):
        DebugOut('Version.__repr__')
        return(str(self))

    def __str__(self):
        s = '%s.%02d.%02d.%02d.%02d' % (self.name(),
                                      self.major(),
                                      self.minor(),
                                      self.patch(),
                                      self.build())
        
        DebugOut('Version.__str__ = %s' % (s))
        return(s.strip())

    def buildFormat(self):
        'Return true if new number format'
        number = self.major() + self.minor() / 100.0 + self.patch() / 10000.0
        # if number >= 1.0701:
          #   return Version.FORMAT_INTEGER
        # else:
          #  return Version.FORMAT_STRING

        DebugOut('Version.buildFormat = %s' % (number))
        
        return Version.FORMAT_INTEGER
    def name(self, n = None):
        DebugOut('Version.name = %s' % (n))
        if (n == None): return(self.__name)

        self.__name = n
        #if n != '':
        #    print 'assign name:', n

    def major(self, n = None):
        DebugOut('Version.major = %s' % (n))
        if (n == None): return(self.__major)

        self.__major = n

    def minor(self, n = None):
        DebugOut('Version.minor = %s' % (n))
        if (n == None): return(self.__minor)

        self.__minor = n

    def patch(self, n = None):
        DebugOut('Version.patch = %s' % (n))
        if (n == None): return(self.__patch)

        self.__patch = n

    def build(self, n = None):
        DebugOut('Version.build = %s' % (n))
        if (n == None): return(self.__build)

        self.__build = n

def version():
    v = Version()

    v.name('Sundial3D')
    v.major(4)
    v.minor(0)
    v.patch(3)
    v.build(0)

    DebugOut('version = %s' % (str(v)))

    return str(v)

def bridgePath(version):

    if sys.version_info[:2] == (2,2):
        bridgesubpath = 'Bridge'
    else:
        bridgesubpath = 'Bridge' + ''.join(map(str,sys.version_info[:2]))

    path = os.path.split(os.path.abspath(__CURRENT_PATH))[0] + pathdelimiter + bridgesubpath + pathdelimiter 
 
   # Bridge files are shared between SUNDIAL3D.04.00.xx.xx
    #ver = str(version)
    #v = ver.split('.',4)
    #path += v[0] + '.' + v[1] + '.' + v[2]
    path += str(version).replace(' ', '.')

    if (os.path.exists(path) == False):
        # Try another place, perhaps code compiled with py2exe

        path1 = os.path.split(os.path.abspath(sys.path[0]))[0] + pathdelimiter + bridgesubpath + pathdelimiter 

        path1 += str(version).replace(' ', '.')
        #print path1
        if (os.path.exists(path1)):
               path = path1 # Path exists

    DebugOut('bridgePath: version = %s ; path = %s' % (version, path))
    return path

class Configuration:

    def __init__(self):
        DebugOut('Configuration.__init__')
        self.__NAME = pathdelimiter + 'TTX.ini'

    def save(self, firmware_path, bridge_path):
        DebugOut('Configuration.save(%s, %s) ' % (firmware_path, bridge_path))
        pass

        config_name = 'TunerStatus'
        configuration = Utility.parseEnum('../Common/C_Tuner.h', config_name)
        Utility.saveConfiguration(bridge_path + self.__NAME, config_name, configuration)

        config_name = 'PowerState'
        configuration = Utility.parseEnum('../Common/C_Power.h', config_name)
        Utility.saveConfiguration(bridge_path + self.__NAME, config_name, configuration)

    def restore(self, firmware_version, config_name):
        DebugOut('Configuration.restore(%s, %s) ' % (firmware_version, config_name))

        path = bridgePath(firmware_version) + self.__NAME
        return Utility.restoreConfiguration(path, config_name)

class Ram:

    def __init__(self):
        DebugOut('Ram.__init__')
        self.__module_index = MODULE_INDEX
        self.__method_indices = METHOD_INDICES

    def write(self, address, bytes):
        DebugOut('Ram.write(%s, %s)' % (address, bytes))
        CHUNK_SIZE = PROPERTIES['WRITE_HUNK_SIZE']

        while (len(bytes) != 0):

            # Grab up to 'chunk size' worth of bytes.
            chunk = bytes[:CHUNK_SIZE]
            bytes = bytes[CHUNK_SIZE:]

            newOperation(self.__module_index,
                         self.__method_indices['writeRamBytes'])


            # Reverse the string to place on the packet stack.
            chunk = list(chunk)
            chunk.reverse()
            chunk = ''.join(chunk)

            for byte in chunk: PyTTXTalk.pushU8(ord(byte))

            PyTTXTalk.pushU32(address)
            sendPacket(1);

            address += len(chunk)

    def read(self, address, count):
        DebugOut('Ram.read(%s, %s)' % (address, count))

        CHUNK_SIZE = PROPERTIES['READ_CHUNK_SIZE']

        data = []

        while (count > 0):

            subcount = CHUNK_SIZE

            if (count < subcount): subcount = count

            newOperation(self.__module_index,
                         self.__method_indices['readRamBytes'])
            PyTTXTalk.pushU8(subcount)
            PyTTXTalk.pushU32(address)
            sendPacket(1);

            address += subcount
            count -= subcount

            subdata = []

            while (subcount > 0):

                subdata.append(chr(PyTTXTalk.popU8()))
                subcount -= 1

            subdata.reverse()

            data.extend(subdata)

        return(''.join(data))

class Flash:

    def __init__(self):
        DebugOut('Flash.__init__')
        
        self.__module_index = MODULE_INDEX
        self.__method_indices = METHOD_INDICES

    def erasePage(self, page_number):
        DebugOut('Flash.erasePage(%s)' % (page_number))
        
        newOperation(self.__module_index, self.__method_indices['eraseFlashPage'])
        PyTTXTalk.pushU16(page_number);
        retry = 0
        fail = 1
        while retry < 3:
            retry += 1
            sendPacket(10);      #pb sleep 100ms after sending
            try:
                chk = PyTTXTalk.popU8()
                add = PyTTXTalk.popU8()
                if (add == 0) or (add == 0x80):
                    fail = 0
                    break       # break out
                else:
                    print retry, 'retry got', add, chk
            except:
                print retry, 'retry Rx', PyTTXTalk.DataSize(), 'Bytes'
        if fail:
            raise 'Flash.erase Failed 3 times'

    def write(self, address, bytes):
        DebugOut('Flash.write(%s, %s)' % (address, bytes))

        CHUNK_SIZE = PROPERTIES['WRITE_CHUNK_SIZE']

        adr_cnt = 15;
        while (len(bytes) != 0):

            # Grab up to 'chunk size' worth of bytes.
            chunk = bytes[:CHUNK_SIZE]
            bytes = bytes[CHUNK_SIZE:]

            newOperation(self.__module_index,
                         self.__method_indices['writeFlashBytes'])


            # Reverse the string to place on the packet stack.
            chunk = list(chunk)
            chunk.reverse()
            chunk = ''.join(chunk)

            for byte in chunk: PyTTXTalk.pushU8(ord(byte))
            PyTTXTalk.pushU32(address)
            retry = 0
            fail = 1
            while retry < 3:  #pb3
                retry += 1
                sendPacket(6);      #pb sleep 60 ms after sending
                try:
                    chk = PyTTXTalk.popU8()
                    add = PyTTXTalk.popU8()
                    if (add == 0) or (add == 0x80):
                        fail = 0
                        break       # break out
                    else:
                        print retry, 'retry got', add, chk
                except:
                    print retry, 'retry Rx', PyTTXTalk.DataSize(), 'Bytes'
            if fail:
                raise 'Flash.write Failed 3 times'

            address += len(chunk)
            adr_cnt += 1
            if(adr_cnt >= 16):
                adr_cnt = 0
                print '.',
                sys.stdout.flush() 
                time.sleep(0.001)               

    def read(self, address, count, multiple_query = 1):
        #print('Flash.read(%s, %s, %s)' % (address, count, multiple_query))

        CHUNK_SIZE = PROPERTIES['READ_CHUNK_SIZE']
        query_1_Answer = 0
        query_2_answer = 0
        total_loop = 0
        data = []
        packetCnt = 0

        while (count > 0):
            packetCnt += 1
            if packetCnt > 16:
                packetCnt = 0
                print '.',
                sys.stdout.flush() 
                time.sleep(0.001)       # allow time for printing              
            subcount = CHUNK_SIZE
            if (count < subcount): 
                subcount = count
            total_loop = total_loop + 1
            #print '[',total_loop,'] Address:0x',hex(address)
            newOperation(self.__module_index,
                         self.__method_indices['readFlashBytes'])
            PyTTXTalk.pushU8(subcount)
            PyTTXTalk.pushU32(address)
            sendPacket(1);
            if(multiple_query == 2):
                newOperation(self.__module_index,
                         self.__method_indices['readFlashBytes'])
                PyTTXTalk.pushU8(subcount)
                PyTTXTalk.pushU32(address + CHUNK_SIZE)
                sendPacket(1);
            chksum = 0
            subdata = []
            if(PyTTXTalk.DataSize() > 3):
                try:
                    checksum_recv = PyTTXTalk.popU8()
                    num_data_bytes = subcount
                    while (num_data_bytes > 0):
                        v8 = PyTTXTalk.popU8()
                        subdata.append(chr(v8))
                        chksum = chksum+v8
                        num_data_bytes -= 1
                    #no exception after "subcount" loops, we can stop the retry loop
                    adrl = PyTTXTalk.popU8()
                    adrh = PyTTXTalk.popU8()
                    adr16 = adrh * 256 + adrl
                    if(checksum_recv != (chksum & 0xFF)):
                        print 'Error,Checksum recv:0x', hex(checksum_recv)
                        print 'Error,Checksum computed:0x', hex(chksum & 0xFF)
                    else:
                        if(multiple_query == 1):
                            if(adr16 != address):
                                print 'Address received:0x', hex(adr16), ',command:0x', hex(address)
                            else:
                                #print 'good address and checksum'
                                address += subcount
                                count -= subcount
                                #continue
                        else:
                            if(adr16 == address):
                                query_1_Answer = 1
                            else:
                                if(adr16 == address + CHUNK_SIZE):
                                    query_2_Answer = 1
                                else:
                                    print 'Address received:0x', hex(adr16), ',command:0x', hex(save_address), 'and 0x', hex(address + CHUNK_SIZE)
                            if(query_1_Answer == 1) and (query_2_Answer == 1):
                                address += subcount
                                count -= subcount
                                address += subcount
                                count -= subcount
                                #continue
                            time.sleep(0.05)
                except:
                    print '*** Exception generated while reading flash memory'
                    import traceback
                    traceback.print_exc()
                    #exception generated because line too short probably
                    #sleep long enough to finish receive a string at 115200 baud
                    #10 ms would cover 100 bytes string
                    time.sleep(0.01)
            else:
                time.sleep(0.01)
                if(multiple_query == 1):
                    print 'No response in Flash.read'
                    #assuming an empty line can be ignored, we use "break" to avoid repeating the query
                    break
            subdata.reverse()
            data.extend(subdata)
        return(''.join(data))
