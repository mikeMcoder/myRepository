'''
NeoPhotonics CONFIDENTIAL
Copyright 2003, 2004 NeoPhotonics Corporation All Rights Reserved.

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

    $Source: /data/development/cvs/Sundial2/Python/TTX/Logger.py,v $
    $Revision: 1.2 $
    $Date: 2007/11/26 19:32:16 $
    $Name: Sundial2_01_02_01_01 $
    
'''
'''

#example of command to print the content of every frames
>>> for a in range(l.frameCount()):
... 	for b in l.content(a):
... 		print 'f[',a,']:',b

Example of the end of frame 20 and beginning of frame 21:

f[ 20 ]: ['sample_frame']['sample9'] = +0
f[ 20 ]: ['sample_frame']['siblock_rtd'] = +0
f[ 20 ]: ['sample_frame']['sled_thermistor'] = +25304
f[ 20 ]: ['status_fatal'] = +0
f[ 20 ]: ['status_warning'] = +0
f[ 21 ]: ['Index_log'] = +0
f[ 21 ]: ['Line_Number'] = +7
f[ 21 ]: ['control_frame']['filter1_power'] = +2.0886660
f[ 21 ]: ['control_frame']['filter2_power'] = +2.0886593



A quick primer on the new data logger:

There are two classes that you can instantiate:

>>> import TTX.Logger as L
>>> d = L.DiskLogger()
>>> m = L.MemoryLogger()

The only difference between the two is that a DiskLogger has an associated filename:

>>> d.filename('test.txt')
>>> d
Description: DiskLogger.
Priority   : NORMAL
Port       : COM1
Filename   : 'test.txt'
Frame Size : 250
Frame Count: 0
>>> m
Description: MemoryLogger.
Priority   : NORMAL
Port       : COM1
Frame Size : 250
Frame Count: 0

The port number is no longer specified as a string:

>>> d.portNumber(6)
>>> d
Description: DiskLogger.
Priority   : NORMAL
Port       : COM6
Filename   : 'test.txt'
Frame Size : 250
Frame Count: 0

You'll also notice that you can set the thread priority to one of three values:

>>> d.priority('HIGHEST')
>>> d.priority('TIME_CRITICAL')
>>> d
Description: DiskLogger.
Priority   : TIME_CRITICAL
Port       : COM6
Filename   : 'test.txt'
Frame Size : 250
Frame Count: 0

As before you start a session by setting the frame count:

>>> d.frameCount(100)
>>> d
Description: DiskLogger.
Priority   : TIME_CRITICAL
Port       : COM6
Filename   : 'test.txt'
Frame Size : 250
Frame Count: 100
>>> d.frame(99)
Description: LoggerFrame

control_frame        : <ControlFrame>
discrete_frame       : <DiscreteFrame>
domain_frame         : <DomainFrame>
dual_controller_frame: <DualControllerFrameSet>
index                : +123
sample_frame         : <SampleFrame>
tuner_frame          : <TunerFrame>

Also as before you can preempt an existing session by setting the frame count to another value:

>>> d.frameCount(100 * 60 * 10) # Ten minute session.
>>> d
Description: DiskLogger.
Priority   : TIME_CRITICAL
Port       : COM6
Filename   : 'test.txt'
Frame Size : 250
Frame Count: 60000
>>> d.frameCount(100)
>>>
>>>
>>> d
Description: DiskLogger.
Priority   : TIME_CRITICAL
Port       : COM6
Filename   : 'test.txt'
Frame Size : 250
Frame Count: 100

This release also allows the ability to iterate over the frames contained by a logger:

>>> d.frameCount(10)
>>> d
Description: DiskLogger.
Priority   : TIME_CRITICAL
Port       : COM6
Filename   : 'test.txt'
Frame Size : 250
Frame Count: 10
>>> for frame in d: frame['index']
...
201
202
203
204
205
206
207
208
209
210

To view an existing file simply switch to that filename. The updated frame count reflects the size of the file. Suppose we start a new python session and open the file created in the previous example:

>>> import TTX.Logger as L
>>> d = L.DiskLogger()
>>> d.filename('test.txt')
>>> d
Description: DiskLogger.
Priority   : NORMAL
Port       : COM1
Filename   : 'test.txt'
Frame Size : 250
Frame Count: 10

Caveats!!!

If you attach to an existing file and issue a frame count. The new session will overwrite that data. It will not warn you.

The data contained in the file is pure binary and is only frame data. A header is not written to indicate the version of TTX python code that created the file. You must use compatible software to read the file. However, the frame format doesn't change frequently so differing versions of python code are still capable of reading files written by another release of the software.
'''


import copy
import os

if (os.name != 'posix'):
    pathdelimiter = '\\'
else:
    pathdelimiter = '/'


import time
import shelve
if (os.name != 'posix'):
    import win32api
    import win32con
    import win32process
import PyTTXTalk
#from Utility import *
import Utility
import System
#from Dictionary import *
import Dictionary

import Memory
#import PyLogger
import Structure
import string

SHELF_FILENAME = 'Logger.shelf'

MODULE_INDEX = 11
METHOD_INDICES = {  'mask'          : 0,
                    'kick'          : 1
                  }

#Datalogger priority:
#
#t.sampleStage().frame()
#[0],RTD1            : +0014036482 Counts
#[1]RTD2            : +0013901825 Counts
#[2],SLED_THERMISTOR : +33836 Counts
#[3],SIBLOCK_RTD     : +65532 Counts
#[4],PHOTODIODE      : +37632 Counts
#
#t.domainStage().frame()
#[5],FILTER1_TEMPERATURE           :  +72.7437 C
#[6],FILTER2_TEMPERATURE           :  +79.3131 C
#[7],SLED_TEMPERATURE              :  +39.9979 C
#[8],SI_BLOCK_TEMPERATURE          :  +55.4274 C
#[9],PHOTODIODE_CURRENT            : +2132.6777 uA
#[10],DEMODULATION_REAL             :   +0.0067 ABU
#[11],DEMODULATION_IMAGINARY        :   +0.0031 ABU
#[12],GAIN_MEDIUM_CURRENT           : +134.8215 mA
#
#t.discreteStage().frame()
#[13],TEC        : +33018 Counts
#[14],FILTER1    : +40012 Counts
#[15],FILTER2    : +42631 Counts
#[16],SI_BLOCK   : +33315 Counts
#[17],GAIN_MEDIUM: +21838 Counts
#
#t.controlStage().frame()
#[18],FILTER1_POWER       :   +0.0302 W
#[19],FILTER2_POWER       :   +0.0343 W
#[20],SLED_CURRENT        :   +0.0175 A

class Logger:

    def __getitem__(self, index):

        frame = self.frame(index)

        if (frame == None): 
            raise StopIteration

        return(frame)

    def __init__(self):
        self.__module_index = MODULE_INDEX
        self.__method_indices = METHOD_INDICES        
        self.__bridge_file = None
        self.__frames = None
        self.__priority = 'NORMAL'
        self.logger = self #was "PyLogger.py" in ITLA, now point to same "Logger.py"
        self.__frameCount = 0
        self.__frameSize = 0
        self.__flag_first_column = 0
        self.__flat = Utility.DictionaryFlattener()

    #example of command line to query the entire content of a logger frame:
    #       print l.frame(7).__exportString__()
    #the logger tree is expanded in the same way as seen in the "KV" files
    #each branch is a string enclosed in a pair "[...]" and the leaf value appear at the end
    #for example:
    #['Index_log'] = +0
    #['Line_Number'] = +7
    #['control_frame']['filter1_power'] = +2.0887957
    #['control_frame']['filter2_power'] = +2.0891962
    #etc
    def frame(self, index):
        
        #the frame is generated by "SPI...DLL" in ITLA
        #for "micro-ITLA", the frame are generated by "PyTTXTalk"
        #when calling "Capture" or a variant of that function
        #f = self.logger.frame(index)
        #f = None
        f = self.__frames[index]

        if (f == None): 
            return(None)
        #the object "self.__dictionary"
        #is a template of the class generated when reading the file 'logger.shelf'
        #the object "d" contain a new instance of the class "Dictionary"
        #the call to "memory" trigger the following
        #       return(Memory.Object.memory(self))
        #which is located in "Dictionary.py"
        #Finally, the function "write" is located in "Memory.py"
        #It will copy the frame "f" at offset 0x0000
        frame = copy.deepcopy(self.__dictionary)
        frame._Dictionary__dictionary['time'] = self.__timestamps[index]
        frame.memory().write(0, f)
        return(frame)
        
    #print the actual  content of a frame using the "KV" file format
    def content(self, index):
        f = self.frame(index)
        if (f == None): 
            return(None)
        print f.__exportString__()
        #return (f.__exportString__().splitlines())
            
    #the initial test version uses "mask" as "logger enable"
    def mask(self, Mask = None):

        Utility.newOperation(self.__module_index, self.__method_indices['mask'])

        if (Mask != None): 
            PyTTXTalk.pushU8(Mask)

        Utility.sendPacket(1)

        if (Mask == None): 
            return(PyTTXTalk.popU8())
            
    #kick the logger to encourage it to keep sending more data
    #This is a "logical flow control" which self regulate the stream of data
    #based on the USB-RS232 adapter 
    #and/or 
    #Windows interrnal thread scheduler
    #both of which able to create intermitent response time
    #the parameter is the number of frames 
    #It is a count of frames sent by the firmware
    #If that counter reaches zero, the logger stop the stream of data
    #if we kick the logger before this count expire,
    #we get a continuous flow which uses the highest bandwidth available
    #otherwise, the log data will have some pause between some group of frames
    #These delays can be precisely computed with the timestamp attached to each frame
    #a value of 1 allow to control the timing of each frame
    #a value too large may take a long time, defeating the kick algorithm
    #the latest kick value overwrite the previous one
    def kick_logger(self, max_frames = 10):
        #print 'Logger kick:', max_frames
        Utility.newOperation(self.__module_index, self.__method_indices['kick'])

        if (max_frames != None): 
            PyTTXTalk.pushU8(max_frames)

        Utility.sendPacket(1)

        if (max_frames == None): 
            return(PyTTXTalk.popU8())                    
            
    def capture(self, filename, SecondsWait = 10):
        #
        #the result is zero or more frame
        #for example, if the file "logger.c" defined 133 bytes for a frame,
        #and suppose we receive 10 frames during the time specified,
        #then we get an array of 10 * 133 = 1330 bytes total
        #it other words, it is only the "raw data" without information about their name and address
        #self.__frames = PyTTXTalk.Log_Capture(SecondsWait, self.frameSize())
        #self.__timestamps = []
        #(self.__frames, self.__timestamps) = PyTTXTalk.Log_Capture(SecondsWait, self.frameSize(), filename, self.kick_logger)
        (capture_total_bytes, capture_total_frames) = PyTTXTalk.Log_Capture(SecondsWait, self.frameSize(), filename, self.kick_logger)
        print 'Binary file size generated:', capture_total_bytes, ', Frames:', capture_total_frames
        #float_time = 0.5
        #for index in range(len(self.__frames)):
        #    self.__timestamps.append(float_time)
        #    float_time = float_time + 2.25
        return (self.frameCount(capture_total_frames))

    #called by "T.connect()" with the path of the brifge for the current firmware (path name depends on firmware version)
    #the initial test version uses "mask" as "logger enable"
    def mem_capture(self, SecondsWait = 10):
        #
        #the result is zero or more frame
        #for example, if the file "logger.c" defined 133 bytes for a frame,
        #and suppose we receive 10 frames during the time specified,
        #then we get an array of 10 * 133 = 1330 bytes total
        #it other words, it is only the "raw data" without information about their name and address
        #self.__frames = PyTTXTalk.Log_Capture(SecondsWait, self.frameSize())
        #self.__timestamps = []
        (self.__frames, self.__timestamps) = PyTTXTalk.Log_Capture(SecondsWait, self.frameSize())
        #float_time = 0.5
        #for index in range(len(self.__frames)):
        #    self.__timestamps.append(float_time)
        #    float_time = float_time + 2.25
        return (self.frameCount(len(self.__frames)))

    #called by "T.connect()" with the path of the brifge for the current firmware (path name depends on firmware version)
    def bridgeFile(self, bridge_file = None):
        'Bridge file for data structure format of logger'

        if bridge_file == None:
            return self.__bridge_file
        try:
            self.__bridge_file = bridge_file + pathdelimiter + 'logger.shelf'
            shelf = shelve.open(self.__bridge_file, 'r')
            self.logger.frameSize(shelf['FRAME_SIZE'])
            #
            #the object "self.__dictionary" is an instance of the class "Dictionary" located in "Dictionary.py"
            #with the entire tree structure made when parsing the file "Logger.c" from the Keil 8051 source code
            self.__dictionary = shelf['FRAME_DICTIONARY'] 
            shelf.close()
            #
            #create an instance of the class <DictionaryFlattener> located in "./TTM/Utility.py"
            flat = Utility.DictionaryFlattener()
            #
            #for ITLA, the first column is always the "time stamp"
            #as first test, we give an empty string to not reserve a first column
            self.__header = ['time stamp']
            #self.__header = ['']
            #self.__header = []
            flat.header(self.__dictionary, self.__header)            
        except:
            #raise 'Bridge file %s not found' % (bridge_file)
            #raise 'Bridge file not found,', bridge_file
            print '-' * 40
            import traceback
            traceback.print_exc()
            print '-' * 40
            raise 'Bridge file not found,', self.__bridge_file
        
    def frameCount(self, c = None):

        if (c == None): 
            return(self.__frameCount)

        self.__priority = 'NORMAL'
        self.__frameCount = c

    def frameSize(self,size=None):
        if (size ==None):
            #return(self.logger.frameSize())
            return(self.__frameSize)
        self.__frameSize = size

    def frameData(self, index):
        'Return a single frame data in a one dimensional list'
        if self.__frames == None:
            return None
        #frame = self.__frames[index]
        frame = self.frame(index)
        #
        #list of float values with very first item set to the timestamp
        #the other values are inserted by the function "data" in the class "DictionaryFlattener" located in "./TTM/Utility.py"
        data = [self.__timestamps[index]]
        self.__flat.data(frame, data)
        return data
        
    def str_here(self, str_param):
        if (self.__flag_first_column == 0):
            self.__flag_first_column = 1
            #print 'str_first_column:', str_param
            return time.ctime(str_param)
        #else:
        #    print 'str_next_column:', str_param
        return str(str_param)
        
    def save(self, filename):
        
        'Save frames to a file in CSV format'
        if not filename.upper().endswith('.CSV'):
            filename += '.csv'
        f = file(filename, 'w')
        f.write('%s\n' % string.join(self.header(), ','))
        self.__flag_first_column = 0
        for i in range(self.frameCount()):
            #f.write('%s\n' % string.join(map(str, self.frameData(i)), ','))
            f.write('%s\n' % string.join(map(self.str_here, self.frameData(i)), ','))
            self.__flag_first_column = 0
        f.close()
        
   
    #The project "micro-ITLA" doesn't uses a separate port number for the logging operation
    #As brief recapitulation, for ITLA lasers,
    #           - the "t" commands are picassoTalk over I2C,
    #           - the "it" commands are MSA over RS232,
    #           - the "l" commands (are ogger over SPI
    #All these protocoles and hardware interfaces 
    #are replaced by a single hardware interface : 
    #       - RS232 restricting by design to ASCII mode only
    #               We are still using 8 bit shift register for data in and out, however the bit D7 is always 0
    #               Futhermore, the non printable ASCII range 0x00-0x1F is avoided, except the line terminators
    #               The characters to really worry are XON and XOFF
    #               The goal is to allow using USB-RS232 adapters 
    #               which often use the XON/XOFF protocol even if specifically requested to not do
    #               The result is that the characters XON and/or XOFF
    #               may appear at random position, like spurious noise
    #The protocol is identified by the first character on each line
    #
    #def portNumber(self, n = None):

    #    if (n == None): return(self.logger.portNumber())

    #    self.logger.portNumber(n)

    def priority(self, p = None):

        if (p == None): return(self.__priority)

        table = {'NORMAL' : win32con.NORMAL_PRIORITY_CLASS,
                 'HIGH'   : win32con.HIGH_PRIORITY_CLASS}
                 
        win32process.SetPriorityClass(win32api.GetCurrentProcess(),
                                      table[p])

        self.__priority = p
        
    def dictionary(self):
        return self.__dictionary
        
    def frames(self):
        return self.__frames
        
    def header(self):
        return self.__header

class DiskLogger(Logger):

    def __init__(self):
    
        Logger.__init__(self)
        
        #reference to "PyLogger" 
        #Python line "#import PyLogger"
        #to open the file "PyLogger.DLL"
        #
        #not used for micro ITLA
        #self.logger = PyLogger.DiskLogger()


    def __repr__(self):

        s =  'Description: DiskLogger.\n'
        s += 'Priority   : %s\n'    % self.priority()
        s += 'Port       : COM%d\n' % self.portNumber()
        s += 'Bridge File: %s\n'    % self.bridgeFile()
        s += 'Filename   : \'%s\'\n' % self.filename()
        s += 'Frame Size : %d\n'    % self.frameSize()
        s += 'Frame Count: %d'      % self.frameCount()
        
        return(s)

    #def filename(self, n = None):

    #    if (n == None): return(self.logger.filename())

    #    self.logger.filename(n)

class MemoryLogger(Logger):

    def __init__(self):

        Logger.__init__(self)

        #reference to "PyLogger" 
        #Python line "#import PyLogger"
        #to open the file "PyLogger.DLL"
        #
        #not used for micro ITLA
        #self.logger = PyLogger.MemoryLogger()


    def __repr__(self):

        s =  'Description: MemoryLogger.\n'
        s += 'Priority   : %s\n' % self.priority()
        #s += 'Port       : COM%d\n' % self.portNumber()
        s += 'Bridge File: %s\n' % self.bridgeFile()
        s += 'Frame Size : %d\n' % self.frameSize()
        s += 'Frame Count: %d' % self.frameCount()

        return(s)

class DictionaryBuilder:

    SOURCE_FILES = ('Control.h',
                    'Discrete.h',
                    'Domain.h',
                    'Logger.c',
                    'Sample.h')
    
    LIST_FILE = 'Logger.lst'

    def __init__(self, firmware_path):

        # Build the dictionaries.
        source_files = []

        for filename in self.SOURCE_FILES:

            source_files.append(firmware_path + pathdelimiter + filename)

        list_file = firmware_path + pathdelimiter + self.LIST_FILE
        
        collection = Structure.KeilCollection(source_files, list_file)

        self.__frame_size = collection.structure('LoggerFrame').size()

        d = self.__buildDictionary('LoggerFrame', collection)

        memory = Memory.Memory(0, '\x00' * 256)
        d.memory(memory)

        self.__dictionary = d

    def __repr__(self):

        return(repr(self.__dictionary))
    
    def __buildDictionary(self, name, collection):

        structure = collection.structure(name)
    
        if (structure == None): 
            return(None)
    
        dictionary = Dictionary.Dictionary()
        dictionary.description(structure.name())

        for member in structure:

            object = None

            if (member.number() > 1):

                # Member contains multiple elements therefore convert the
                # array to a dictionary.
                object = self.__buildArrayDictionary(member)
            
            elif (collection.structure(member.type()) != None):

                # Member is itself a user defined structure and is to be
                # converted in to a dictionary.
                object = self.__buildDictionary(member.type(), collection)

            else:

                exec('object = Memory.%s()' % (member.type()))

            object.address(member.offset())
        
            dictionary.addEntry(member.name(), object)

        dictionary.size(structure.size())

        return(dictionary)

    def __buildArrayDictionary(self, member):

        '''
Build a dictionary that represents an array.
The address will be the default of zero 
and can be set appropriately by the client.
        '''
        #the variable "dictionary" is an instance of the class "Dictionary" which is located in "Dictionary.py"
        dictionary = Dictionary()
        dictionary.description('%s Array' % (member.type()))
        dictionary.address(0)

        object_size = 0
    
        for i in range(member.number()):

            exec('object = Memory.%s()' % (member.type()))

            object_size = object.size()
            object.address(i * object_size)
            
            dictionary.addEntry(i, object)

        dictionary.size(object_size * member.number())

        return(dictionary)

    def dictionary(self): 
        return(self.__dictionary)

    def save(self, bridge_path):

        bridge_path += pathdelimiter + SHELF_FILENAME
        s = shelve.open(bridge_path)
        s['FRAME_DICTIONARY'] = self.__dictionary
        s['FRAME_SIZE'] = self.__frame_size
        s.close()
        print 'Logger frame size in bytes:', self.__frame_size
