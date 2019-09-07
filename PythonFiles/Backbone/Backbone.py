# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 12:48:53 2016

@author: mark
"""

# note: ipywidgets is not required, but seaborn throws a warning without it

import sys
import time
import struct
import os
import bz2
import zlib
#import serial
import numpy as np
#import operator
import pandas as pd
#import pprint
#import LSRIO
import inspect
import linecache
import warnings
#import TTM.Utility as Utility
#import base64
import math
import re
import json
from json import encoder
import copy
import collections
#import PyCRC.CRC16
#import progressbar
import datetime
import pickle
import textwrap
import enum

#import traceback

import distutils
from distutils import version

import ctypes

import KV

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

from enum import Enum

encoder.FLOAT_REPR = lambda o: '%g.0' % o if '.' not in '%g' % o and 'e' not in '%g' % o and not np.isnan(o) else '%.7g' % o

#PYTHON32BIT = sys.maxsize < 2**32

RX_TIMEOUT_DEFAULT  = 0.5 # flash writes are slow (~200ms)

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)



class Backbone(object):

    """Modulator control/debug interface"""

    _UNSUPPORTEDFUNCTIONSTRING = 'ERROR'  # dummy FW funcion name for unsupported set
    _LSR_WRITE_BIT  = 0x01
#    _LSR_ID_BIT     = 0x02 | 0x20
    _LSR_ID2_BIT    = 0x04
    _LSR_REMOTE_BIT = 0x08
    _LSR_OPTION_BIT = 0x10

     
    class Packet(ctypes.Union):
        """ """
    
        class _PackedPacket(ctypes.LittleEndianStructure):
            """ """
        
            class _HeaderPacket(ctypes.Union):
                """ """
                class _PacketBits1(ctypes.LittleEndianStructure):
                    """ """
                    _pack_ = 1
                    _fields_ = [
                        ("write", ctypes.c_uint8, 1),
                        ("protocol1", ctypes.c_uint8, 1),
                        ("protocol2", ctypes.c_uint8, 1),
                        ("remote", ctypes.c_uint8, 1),
                        ("option", ctypes.c_uint8, 1),
                        ("itla", ctypes.c_uint8, 1),
                        ("unused6", ctypes.c_uint8, 1),
                        ("unused7", ctypes.c_uint8, 1),
                        ("reg", ctypes.c_uint8, 8),
                        ("index", ctypes.c_uint8, 8),
                        ("index2", ctypes.c_uint8, 8),
                    ]
                

                class _PacketBits2(ctypes.LittleEndianStructure):
                    """ """
                    class _test2(ctypes.LittleEndianStructure):
                        """ """
                        _pack_ = 1
                        _fields_ = [
                                    ("numbytes", ctypes.c_uint8, 4), # uint8 for 64 bit
                                    ("offset", ctypes.c_uint16, 12),
                                ]
                    _pack_ = 1
                    if ctypes.sizeof(_test2) != 2: # workaround for python ctypes bug
                        _fields_ = [
                            ("write", ctypes.c_uint8, 1),
                            ("protocol1", ctypes.c_uint8, 1),
                            ("protocol2", ctypes.c_uint8, 1),
                            ("remote", ctypes.c_uint8, 1),
                            ("option", ctypes.c_uint8, 1),
                            ("itla", ctypes.c_uint8, 1),
                            ("unused6", ctypes.c_uint8, 1),
                            ("unused7", ctypes.c_uint8, 1),
                            ("reg", ctypes.c_uint8, 8),
                            ("numbytes", ctypes.c_uint16, 4), # uint16 for 32 bit
                            ("offset", ctypes.c_uint16, 12),
                        ]
                    else:
                        _fields_ = [
                            ("write", ctypes.c_uint8, 1),
                            ("protocol1", ctypes.c_uint8, 1),
                            ("protocol2", ctypes.c_uint8, 1),
                            ("remote", ctypes.c_uint8, 1),
                            ("option", ctypes.c_uint8, 1),
                            ("itla", ctypes.c_uint8, 1),
                            ("unused6", ctypes.c_uint8, 1),
                            ("unused7", ctypes.c_uint8, 1),
                            ("reg", ctypes.c_uint8, 8),
                            ("numbytes", ctypes.c_uint8, 4), # uint8 for 64 bit
                            ("offset", ctypes.c_uint16, 12),
                        ]
                
                class _PacketBits3(ctypes.LittleEndianStructure):
                    """ """
                    _pack_ = 1
                    _fields_ = [
                        ("write", ctypes.c_uint8, 1),
                        ("protocol1", ctypes.c_uint8, 1),
                        ("protocol2", ctypes.c_uint8, 1),
                        ("remote", ctypes.c_uint8, 1),
                        ("option", ctypes.c_uint8, 1),
                        ("itla", ctypes.c_uint8, 1),
                        ("unused6", ctypes.c_uint8, 1),
                        ("unused7", ctypes.c_uint8, 1),
                        ("reg", ctypes.c_uint8, 8),
                        ("index16", ctypes.c_uint16, 16),
                    ]   
                _pack_ = 1
                _fields_ = [("type1", _PacketBits1),
                            ("type2", _PacketBits2),
                            ("type3", _PacketBits3)]
    
        
            class _DataPacket(ctypes.Union):
                """ """
                _pack_ = 1
                _fields_ = [("uint32", ctypes.c_uint32),
                            ("uint16", ctypes.c_uint16),
                            ("uint8", ctypes.c_uint8),
                            ("int8", ctypes.c_int8),
                            ("int16", ctypes.c_int16),
                            ("float", ctypes.c_float),
                            ("uint8array", ctypes.c_uint8 * 4),]
    
            _pack_ = 1
            _fields_ = [("header", _HeaderPacket),
                        ("payload", _DataPacket)]
        

        _pack_ = 1
        _fields_ = [("packed", _PackedPacket),
                    ("rawdata", ctypes.c_uint8 * 8)]

#        def __init__(self):
#            self.packed.header.type1.protocol1 = True # ID as not MSA to module
#            self.packed.header.type1.itla = True # ID as ITLA
    
    
    class ModuleError(SystemExit):
        """ """
        pass
    
    
    class ModuleNoResponse(SystemExit):
        """ """
        pass
    
    
    class CALCONTAINER():
        """ """
        pass
    
    class CTRLCONTAINER():
        """ """
        pass
    
    class CALCLASS():
        """ """
        pass
    
    class CTRLCLASS():
        """ """
        pass

    class STATECONTAINER():
        """ """
        pass

    class EVENTCONTAINER():
        """ """
        pass

    class textlist(list):
        """ """
        def __repr__(self):
            return('\n'.join(self))

    class formatted:
        """ """

        def __init__(self):
            self._ignored = []
            self._width=35
            self._columns = 1

        def __repr__(self):
            containsself = False
            returnval = []
            varstoreport = [a for a in dir(self) if not a.startswith('_') and not a in self._ignored]
            if len(varstoreport) == 0:
                return ''
            varstoreport2 = [a.replace('__','.') for a in varstoreport]
            padding = len(max(varstoreport2, key=len))
            for varname in varstoreport:
                if getattr(self, varname).__class__.__name__ == self.__class__.__name__:
                    containsself = True
                if isinstance(getattr(self, varname), Enum):
                    strout = getattr(self, varname).name
                else:
                    strout = str(getattr(self, varname))
                if containsself:
                    returnval.append('\n\033[4m\033[1m' + varname + '\033[0m\n' + strout)
                else:
                    returnval.append(' '.join([varname.replace('__','.').rjust(padding), '=', strout]))
                    
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


    class _floatwithunits(float):
        def __new__(cls, value, *a, **k):
            if value is not None:
                return float.__new__(cls, value)
            else:
                return None

        def __init__(self, value, *args, **kwargs):
            self.units = kwargs.pop('units', None)
    
        def __str__(self):
            if self.units is not None:
                return '%s %s' % (encoder.FLOAT_REPR(self), self.units)
            else:
                return '%s' % encoder.FLOAT_REPR(self)

        def __repr__(self):
            if self.units is not None:
                return '%.7g %s' % (self, self.units)
            else:
                return '%.7g' % self

        def __eq__(self, other):
            if other is None:
                return self.real is None
            return np.isclose(self.real ,other.real, atol=0)

        def __cmp__(self, other):
            if other is None:
                return self.real is None
            if np.isclose(self.real ,other.real, atol=0):
                return 0
            else:
                return cmp(self.real,other.real)


    class _fixedptwithunits(float):  # since python is concerned with digits, not speed, this representation is base 10
        def __new__(cls, value, *a, **k):
            if value is not None:
                try:
                    return float.__new__(cls, value)
                except TypeError as e:
                    print 'Unable to set ' + cls.__name__ + ' to "' + str(value).replace('\n',',') + '"'
                    raise e
            else:
                return None
            
        def __init__(self, value, *args, **kwargs):
            self.units = kwargs.pop('units', None)
            self.pt = kwargs.pop('pt', None)
            if self.pt < 0.0:
                maxval = float(2**31 - 1) / float(10**-self.pt)
                minval = -maxval
                self._signtype = 'signed'
            else:
                maxval =  float(2**32 - 1) / float(10**self.pt)
                minval = 0.0
                self._signtype = 'unsigned'
            if not minval <= value <= maxval:
                raise ValueError( "Can't fit " + str(value) + " in an " + self._signtype + " fixed " + str(abs(self.pt)) + " point variable.  Must be between " + str(minval) + " and " + str(maxval) )

        def __setval__(self,value):
            self.real = value
            
        def __str__(self):
            if self.units is not None:
                return '%s %s' % (('{0:.%df}' % abs(self.pt)).format(self), self.units)
            else:
                return self._strwithoutunits()

        def __repr__(self):
            if self.units is not None:
                return '%s %s' % (('{0:.%df}' % abs(self.pt)).format(self), self.units)
            else:
                return self._strwithoutunits()

        def __eq__(self, other):
            if other is None:
                return self.real is None
            return np.isclose(self.real ,other.real, atol=0)

        def __cmp__(self, other): 
            if other is None:
                return self.real is None
            if np.isclose(self.real ,other.real, atol=0):
                return 0
            else:
                return cmp(self.real,other.real)
            
        def _strwithoutunits(self):
            return '%s' % ('{0:.%df}' % abs(self.pt)).format(self)
    
    class _intwithunits(np.int64):
        def __new__(cls, value, *a, **k):
            if value is not None:
                try:
                    return np.int64.__new__(cls, value)
                except TypeError as e:
                    print 'Unable to set ' + cls.__name__ + ' to "' + str(value).replace('\n',',') + '"'
                    raise e
            else:
                return None

        def __init__(self, value, *args, **kwargs):
            self.units = kwargs.pop('units', None)
    
        def __str__(self):
            if self.units is not None:
                return '%i %s' % (self, self.units)
            else:
                return self._strwithoutunits()

        def __repr__(self):
            if self.units is not None:
                return '%i %s' % (self, self.units)
            else:
                return self._strwithoutunits()

        def __eq__(self, other):
            return self.__cmp__(other) == 0

        def __cmp__(self, other):
            if other is None:
                return self.real is None
            if type(self) is str or type(other) is str:
                if type(other) is not type(self):
                    return False
                return self == other
            if np.isnan(self):
                return False
            if np.isnan(other):
                return False
            if np.isclose(self.real ,other.real, atol=0):
                return 0
            else:
                return cmp(self.real,other.real)

        def _strwithoutunits(self):
            return '%i' % self


    def __init__(self, *args, **kwargs):
        
        
        self._version = 'UNKNOWN VERSION'

        print self.get_control_Version()

        self._ttyhandle = kwargs.pop('_ttyhandle', None)

        self.kv = KV.KV()
        self.kv_defaults = KV.KV()
        self.kv_flash = KV.KV()
        self.rawcal = KV.KV()
        self._lastcalstate = None
        self._lastcalstate_defaults = None
        self._lastcalstate_flash = None
        self._connectime = None
        self._buildstring = None
        self._port = None
        self._baud = None
        self._print_once = False
        self._OIFlogging = False
        self._dummyx99data = None
        self.vlinecounter = 0
        self.lastomadata = None
        self.vlinenum = 0
        self._debug_rs232 = 0
        self.DEBUG_PRINT = False
        self._echocaller = False
        self._writetimestart = None
        self._writedonetime = None
        self._abortscriptonerror = True
        self._erroroccurred = False
        self._lastsentcmd = ''
        self._inunlock = False
        self._errors = ''
        if not hasattr(self,'_kvDictionaryname'):
            raise Exception('_kvDictionaryname must be defined')
            self._kvDictionaryname = 'to_be_defined'
        self._echodepth = 6
        #self.io = LSRIO.LSRIO(self)
        self._temperaturefilename = '/home/mark/currenttemperature.txt'  # todo: get/set functions for temperature and oma files
        self._omafilename = '/home/mark/current_oma_reading.txt'

            
        self._scalingtablefilename = 'AnalogScalingTable.csv'
        self._iocolumnstoadd = ['comment', 'Units', 'Description', 'uP',
                                 'Bit Depth', 'Range min', 'Range max', 'Int/SPI' ]
        self._functionstable = pd.DataFrame()
        self._caltable = pd.DataFrame()
        self._unsettablecalvars = ['calibVersion']
        self._cmdcounter = 0
        self._templastcmdtype = None

        if not hasattr(self,'_cachedir'):
            print '_cachedir should be defined'
            self._cachedir = os.getcwd() + os.sep + 'cache'

        if not hasattr(self,'_bridgedir'):
            print '_bridgedir should be defined'
            self._bridgedir = os.getcwd() + os.sep + 'nanobridge'

        self._keys = [None] * 20

        if not os.path.exists(self._cachedir):
            print 'Creating',self._cachedir
            os.makedirs(self._cachedir)

        if not os.path.exists(self._bridgedir):
            print 'Creating',self._bridgedir
            os.makedirs(self._bridgedir)

        pandasneeded = '0.22.0'
        if distutils.version.LooseVersion(pd.__version__) < distutils.version.LooseVersion(pandasneeded):
            print self.hilite('Pandas module is out of date.  You have version' + pd.__version__ + '  Please upgrade to ' + pandasneeded + ' or greater.', False, True)

#        serialneeded = '3.3'
#        if distutils.version.LooseVersion(serial.__version__) < distutils.version.LooseVersion(serialneeded):
#            print self.hilite('Serial module is out of date.  You have version' + serial.__version__ + '  Please upgrade to ' + serialneeded + ' or greater.', False, True)

        if os.name == 'posix':
            self._portprefix = '/dev/ttyS'
            self._gettime = time.time
        else:
            self._portprefix = 'com'
            self._gettime = time.clock

        self.logfile()

        print

        self._logstarttime = self._gettime()
        
        self._print_once = True

    def get_control_Version(self):
        """ """
        idfilename = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','notrack', 'ECLuITLA_gitid.txt')
        if os.path.isfile(idfilename):
            with open(idfilename, 'r') as f:
                self._version = f.readline().strip()
        return self.__class__.__name__ + ' (Version: ' + self._version + ')'

    def _generatecaltable(self, cppfilename=None, content=None,nanoDevice=False, progress=False):
        if cppfilename is not None:
            with open(cppfilename) as myfile:
                content = myfile.read()
        if nanoDevice == True:
            tables = [self._kvDictionaryname, 'calibrationDictionary', 'rawcaldict']
        else:        
            tables = [self._kvDictionaryname, 'calibrationDictionary', 'rawcaldict']
        parsedtables = []
                
        for tablename in tables:
            remote = 'Master' in tablename or 'rawcaldict' in tablename
            parsedtable = self._parsecaltable(content, structname=tablename, remote=remote, nanoDevice=nanoDevice, progress=progress)
            if parsedtable.shape[0] > 0:
                parsedtables.append(parsedtable)
            elif tablename == self._kvDictionaryname:
                self._kvDictionaryname = 'calibrationDictionary' # kludge for backwards compatibility
            print
            
        if len(parsedtables) == 0:
            print 'unable to find cal information'
            return pd.DataFrame()
            
        self._caltable = pd.concat(parsedtables)
                
        self._caltable = self._caltable[ ~self._caltable['variable'].isin(self._unsettablecalvars ) ]

        dups = self._caltable[ self._caltable.duplicated(['variable'])]
        
        if len(dups) > 0:
            print self.hilite("Warning: Duplicated calibration variable names : \n" + ' '.join(dups.variable), False, True)

        misaligned = self._caltable[ self._caltable.type.isin(['uint32_t','float','ufixed7pt','ufixed9pt','sfixed7pt','sfixed9pt']) & self._caltable.offset % 4 != 0 ]

        if len(misaligned) > 0:
            print self.hilite("Warning: Misaligned calibration variables : " + '\n'.join(misaligned.variable).replace('__','.'), False, True)
        

    def _addcalfunctions(self):
        """

        :param cppfilename: 

        """


        self._caltable.apply(self._addcalfunction, axis=1)

        self._caltable.apply(self._addcalfunction, args=('cal_defaults', ), axis=1)
        self._caltable.apply(self._addcalfunction, args=('cal_flash', ), axis=1)


        if self._cmdcounter > 0:
            print ': '+str(self._cmdcounter)+' entries'

    def getfunctionstable(self):
        """ """
        return self._functionstable.copy()

    def getcalstable(self):
        """ """
        return self._caltable.copy()


    def _fixedpttouint32(self, value, pt):
        if pt < 0.0:
            maxval = float(2**31 - 1) / float(10**-pt)
            minval = -maxval
            _signtype = 'signed'
        else:
            maxval =  float(2**32 - 1) / float(10**pt)
            minval = 0.0
            _signtype = 'unsigned'
        if not minval <= value <= maxval:
            raise ValueError( "Can't fit " + str(value) + " in an " + _signtype + " fixed " + str(abs(pt)) + " point variable.  Must be between " + str(minval) + " and " + str(maxval) )

        return int(round(value * 10**abs(pt)))
    
    def _fixedptfromuint32(self, value, pt):
        if pt < 0.0:
            if value > 2**31-1:
                return value / float(10**pt)
        return value / float(10**pt)

    def flashspace(self):
        try:
            flashvals = self.decodeuint32array(self.reg(0xC6))
        except self.ModuleError as e:
            if str(e).startswith('Command not recognized'):
                return None
        retval = self.formatted()
                
        retval.kvdictused = flashvals[0]
        retval.kvdicttotal = flashvals[1]
        retval.rawcalused = flashvals[2]
        retval.rawcaltotal = flashvals[3]
        retval.codeused = flashvals[4]
        retval.kvpctused = 100.0 * float(retval.kvdictused) / float(retval.kvdicttotal)
        retval.rawcalpctused = 100.0 * float(retval.rawcalused) / float(retval.rawcaltotal)
        return retval

    def _addcalfunction(self, functioninfo, container = 'cal' ):
        """

        :param functioninfo: 

        """

        if functioninfo.remote:  #TODO: make proper setting
            if container == 'cal':
                register = 0xC7
            else:
                return
        elif container == 'cal':
            register = 0xCA
        elif container == 'cal_flash':
            register = 0xC8
        elif container == 'cal_defaults':
            register = 0xC9
        else:
            raise ValueError( "Cal container " + container +" not recognized" )
            register = None

        if functioninfo['cal'] not in getattr(self,container).__dict__:
            setattr(getattr(self,container), functioninfo['cal'], self.CALCLASS())  # create table objects if needed
            if self._cmdcounter > 0:
                print ': '+str(self._cmdcounter)+' entries'
            print 'Creating ' + container + '.' + functioninfo['cal'],
            self._cmdcounter = 0
        
        function = None
        def getsetvalue(setval=None, markasinvalid=False, defaultstonone=False):
            """

            :param setval:  (Default value = None)

            """
            if getsetvalue.info.offset > 4096:
                print getsetvalue.info.variable + ": index > 4096 not yet supported"
                return None

            if markasinvalid is True: # mark value as invalid
#                print 'Setting ' + getsetvalue.info.variable + ' as invalid'
                self.validMapCmd(action=2, offset=getsetvalue.info.offset, size=getsetvalue.info.typelength)
                return None

            packet=self.Packet()
            packet.packed.header.type2.reg = register
            packet.packed.header.type2.offset = getsetvalue.info.offset
            packet.packed.header.type2.numbytes = getsetvalue.info.typelength
            packet.packed.header.type2.remote = getsetvalue.info.remote
                
            if setval is not None:
                packet.packed.header.type2.write = True
                if getsetvalue.info.type == 'float':
                    packet.packed.payload.float = setval
                elif getsetvalue.info.type == 'uint16_t':
                    packet.packed.payload.uint16 = setval
                elif getsetvalue.info.type == 'int16_t':
                    packet.packed.payload.int16 = setval
                elif getsetvalue.info.type == 'uint32_t':
                    packet.packed.payload.uint32 = setval
                elif getsetvalue.info.type == 'uint8_t':
                    packet.packed.payload.uint8 = setval
                elif getsetvalue.info.type == 'bool':
                    packet.packed.payload.uint8 = int(setval)
                elif getsetvalue.info.type == 'char':
                    packet.packed.payload.uint8 = setval
                elif getsetvalue.info.type == 'int8_t':
                    packet.packed.payload.int8 = setval
                elif getsetvalue.info.type == 'ufixed7pt':
                    packet.packed.payload.uint32 = self._fixedpttouint32(setval , 7)
                elif getsetvalue.info.type == 'ufixed9pt':
                    packet.packed.payload.uint32 = self._fixedpttouint32(setval , 9)
                elif getsetvalue.info.type == 'sfixed7pt':
                    packet.packed.payload.uint32 = self._fixedpttouint32(setval , -7)
                elif getsetvalue.info.type == 'sfixed9pt':
                    packet.packed.payload.uint32 = self._fixedpttouint32(setval , -9)
                elif getsetvalue.info.type == 'float16_t':
                    fp16buffer = np.array([setval]).astype(dtype='<f2').tobytes()
                    packet.packed.payload.uint8array[0] = ord(fp16buffer[0])
                    packet.packed.payload.uint8array[1] = ord(fp16buffer[1])
                else:
                    print 'Unknown type:' + getsetvalue.info.type
                    return None
                return self.sendpacket(packet).strip('\x00')
            else:
                if defaultstonone:
                    if container == 'cal':
                        isvalid = self.validMapCmd(action=3, offset=getsetvalue.info.offset, size=getsetvalue.info.typelength)
                    elif container == 'cal_flash':
                        isvalid = self.validMapCmd(action=4, offset=getsetvalue.info.offset, size=getsetvalue.info.typelength)
                    elif container == 'cal_defaults':
                        isvalid = True # all defaults are valid by definition
                    else:
                        print self.hilite("Cal container " + container +" not recognized",0,1)
                        isvalid = True
                    if not isvalid:
                        return None
                packet.packed.header.type2.write = False
                if getsetvalue.info.type == 'float':
                    return self._floatwithunits(self.decodefloatarray(self.sendpacket(packet))[0], units=getsetvalue.info.Units )
                elif getsetvalue.info.type == 'uint16_t':
                    return self._intwithunits(self.decodeuint16array(self.sendpacket(packet))[0], units=getsetvalue.info.Units )
                elif getsetvalue.info.type == 'int16_t':
                    return self._intwithunits(self.decodeint16array(self.sendpacket(packet))[0], units=getsetvalue.info.Units )
                elif getsetvalue.info.type == 'uint32_t':
                    return self._intwithunits(self.decodeuint32array(self.sendpacket(packet))[0], units=getsetvalue.info.Units )
                elif getsetvalue.info.type == 'uint8_t':
                    return self._intwithunits(self.decodeuint8array(self.sendpacket(packet))[0], units=getsetvalue.info.Units )
                elif getsetvalue.info.type == 'bool':
                    return self._intwithunits(self.decodeuint8array(self.sendpacket(packet))[0], units=getsetvalue.info.Units )
                elif getsetvalue.info.type == 'char':
                    return self._intwithunits(self.decodeuint8array(self.sendpacket(packet))[0], units=getsetvalue.info.Units )
                elif getsetvalue.info.type == 'int8_t':
                    return self._intwithunits(self.decodeuint8array(self.sendpacket(packet))[0], units=getsetvalue.info.Units )
                elif getsetvalue.info.type == 'ufixed7pt':
                    return self._fixedptwithunits(self._fixedptfromuint32(self.decodeuint32array(self.sendpacket(packet))[0], 7)  , units=getsetvalue.info.Units, pt=7 )
                elif getsetvalue.info.type == 'ufixed9pt':
                    return self._fixedptwithunits(self._fixedptfromuint32(self.decodeuint32array(self.sendpacket(packet))[0], 9)  , units=getsetvalue.info.Units, pt=9 )
                elif getsetvalue.info.type == 'sfixed7pt':
                    return self._fixedptwithunits(self._fixedptfromuint32(self.decodeuint32array(self.sendpacket(packet))[0], -7)  , units=getsetvalue.info.Units, pt=-7 )
                elif getsetvalue.info.type == 'sfixed9pt':
                    return self._fixedptwithunits(self._fixedptfromuint32(self.decodeuint32array(self.sendpacket(packet))[0], -9)  , units=getsetvalue.info.Units, pt=-9 )
                elif getsetvalue.info.type == 'float16_t':
                    return self._floatwithunits(np.frombuffer(bytearray(self.sendpacket(packet)), dtype='<f2')[0], units=getsetvalue.info.Units)
                else:
                    print 'Unknown type' + getsetvalue.info.type
                    return None
        getsetvalue.info = functioninfo.copy()
        if 'Units' not in getsetvalue.info.index:
            getsetvalue.info.Units = None
        getsetvalue.__doc__ = functioninfo['comment']
        getsetvalue.writable = True
        function = getsetvalue

        function.__name__ = functioninfo['variable']
        function.returntype = functioninfo.type
        function.container = container
        setattr(getattr(getattr(self,container), functioninfo['cal']), function.__name__, function)  # add get function
        
        if self._templastcmdtype == functioninfo['cal']:
            self._cmdcounter += 1
        else:
            self._cmdcounter = 1
            self._templastcmdtype = functioninfo['cal']
                   
    def _get_cal_map_ifneeded(self):
        if not hasattr(self,'cal'):
            print
            print 'Retrieving cal map from unit',
            self.setcalmapfromunit()

    def calstate(self, setval=None, cmdformat=False, progress=False, calcontainer=None, skipclosevalues=False, defaultstonone=False):
        """Read or write full calibration state from/to module

        :param setval: if present, calibration settings object to send to module (Default value = None)
        :param cmdformat: (Default value = False)
                           True: return list of executable python commands to
                           False: returns calibration settings object read from module set.
        :returns: calibration object (or command list if cmdformat is True)

        """

        self._get_cal_map_ifneeded()

        if calcontainer is None:
            calcontainer = self.cal

        if cmdformat:
            retval = self.textlist()
        else:
            retval = self.formatted()
            retval._width = 55
            retval._columns = 1
        i = 0
        if setval is None:
            for calname, cal in calcontainer.__dict__.iteritems():
                for name, val in sorted(cal.__dict__.iteritems()):
                    if 'dummy' in name:
                        continue
                    if callable(val):
                        i += 1
                        if progress and not i%50:
                            sys.stderr.write('.')
                        value = val(defaultstonone=defaultstonone)
                        if cmdformat:
                            retval.append('lsr.cal.' + calname + '.' + name + '(%g' %value.real + ')')
                        else:
                            setattr(retval, name, value )
        else:
            setval = copy.copy(setval)
            for calname, cal in calcontainer.__dict__.iteritems():
                for name, val in sorted(cal.__dict__.iteritems()):
                    if callable(val):
                        i += 1
                        name = self._manglename(name,setval.__dict__)
                        if name in setval.__dict__:
                            if 'dummy' in name:
                                continue
                            target = setval.__dict__[name]
                            if not i%50 and progress:
                                sys.stderr.write('.')
                                sys.stderr.flush()
                            if target is not None:
                                if cmdformat:
                                    retval.append('lsr.cal.' + calname + '.' + name + '(%g' %target + ')')
                                elif not (skipclosevalues and np.isclose(val() ,target, atol=0)):
                                    val(target)
                                    setattr(retval, name, setval.__dict__[name] )
                            else:
                                val(markasinvalid=True)
                                setattr(retval, name, setval.__dict__[name] )
                            delattr(setval, name)
            if len(setval.__dict__) > 3: # kludge fixme
                sys.stderr.flush()
                print "\nUnable to set:\n", setval

        if calcontainer == self.cal:
            self._lastcalstate = copy.deepcopy(retval)
        elif calcontainer == self.cal_defaults:
            self._lastcalstate_defaults = copy.deepcopy(retval)
        elif calcontainer == self.cal_flash:
            self._lastcalstate_flash = copy.deepcopy(retval)

        if progress:
            sys.stderr.flush()
            sys.stderr.write('\n')
        return retval


    def _flattennesteddict(self,d, parent_key='', sep='_', paddigits = 0):
        items = []
        for k, v in d.items():
            try:
                k = int(k)
                k = format(k,format( paddigits,'02' ))
                raise ValueError
            except ValueError:
                k = str(k)
            if k.startswith('_'):
                continue
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(self._flattennesteddict(v, new_key, sep=sep, paddigits=paddigits).items())
            else:
                items.append((new_key, v))
        return dict(items)


    def loadblankkv(self, calkvdict=None, kvdict=None):
        self._get_cal_map_ifneeded()
        if calkvdict is None:
            calkvdict = getattr(getattr(self,'cal'),self._kvDictionaryname)
        if kvdict is None:
            kvdict = self.kv.kvdict
        for keys,value in calkvdict.__dict__.items():
            keys = keys.split('__')
            tmp = kvdict
            for key in keys[:-1]:
                tmp = tmp[self.kv._coerce_to_numeric(key)]
            key=keys[-1]
            tmp[self.kv._coerce_to_numeric(key)] = None
        if kvdict is None and hasattr(self,'t'):
            self.t.tmode(mode=1,kvdict=self.kv.kvdict,nano=True)



    def load_kv_from_module(self, calcontainer=None, limitlist=[], defaultstonone=False, calbase=None):
        self._get_cal_map_ifneeded()
        
        if calcontainer is None:
            calcontainer = self.cal
            
        if calbase is None:
            calbase = self._kvDictionaryname
            
        calstate = self.calstate(progress=True, calcontainer=calcontainer, defaultstonone=defaultstonone)
        
        if calcontainer == self.cal:
            kvdict = self.kv.kvdict
        elif calcontainer == self.cal_defaults:
            kvdict = self.kv_defaults.kvdict
        elif calcontainer == self.cal_flash:
            kvdict = self.kv_flash.kvdict
        
        if calbase == 'rawcaldict':  # kludge for now
            kvdict = self.rawcal.kvdict
        
        caldict = calstate.__dict__
        
        for k in caldict.keys():
          if k.startswith('_'):
            caldict.pop(k)
          elif k not in getattr(getattr(self, 'cal'), calbase).__dict__.keys():
              caldict.pop(k)
          elif len(limitlist) > 0:
              if k not in limitlist:
                  caldict.pop(k)

#        calbase = 'calibrationDictionary' #self.cal.__dict__.keys()[0] # only supporting one base for now
        
        for fullkey, value in caldict.items():
            keys = fullkey.split('__')
            tmp = kvdict
            for key in keys[:-1]:
                tmp = tmp[self.kv._coerce_to_numeric(key)]
            key=keys[-1]
            tmp[self.kv._coerce_to_numeric(key)] = value
            if hasattr( getattr( getattr(self, 'cal'), calbase), fullkey):
                order = getattr( getattr( getattr( getattr( getattr(self, 'cal'), calbase), fullkey), 'info'), 'offset' )
            else:
                order = 99999
            tmp._order(self.kv._coerce_to_numeric(key), order)

        kvdict.remove_nones()
        
        if calcontainer == self.cal_defaults:
            kvdict = self.kv.kvdict_defaults = self.kv_defaults.kvdict.copy()
        elif calcontainer == self.cal_flash:
            kvdict = self.kv.kvdict_flash = self.kv_flash.kvdict.copy()

    def fixkvorder(self, kvobject, calbase = None):
        #calbase = self.cal.__dict__.keys()[0] # only supporting one base for now
        if calbase is None:
            calbase = self._kvDictionaryname
            
        if self._lastcalstate is None:
            self.calstate()
            
        caldict = dict((k, v) for k, v in self._lastcalstate.__dict__.items() if not str(k).startswith("_") ) 
        
        for fullkey, value in caldict.items():
            skip = False
            keys = fullkey.split('__')
            tmp = kvobject.kvdict
            for key in keys[:-1]:
                if tmp.get(key,None) is None:
                    skip = True
                    continue
                tmp = tmp[self.kv._coerce_to_numeric(key)]
            if skip:
                continue
            key=keys[-1]
            if hasattr( getattr( getattr(self, 'cal'), calbase), fullkey):
                order = getattr( getattr( getattr( getattr( getattr(self, 'cal'), calbase), fullkey), 'info'), 'offset' )
            else:
                order = 99999
            if hasattr(tmp, '_order'):
                tmp._order(self.kv._coerce_to_numeric(key), order)

#        for fullkey in self._flattennesteddict(kvobject, paddigits=2):
#            order = getattr( getattr( getattr( getattr( getattr(self, 'cal'), calbase), fullkey), 'info'), 'offset' )
            

    def loadonlynondefaultkv(self,blank=False):
        self.t.restore(loadall=True)
        caldiff = self.calcompare(self._lastcalstate, self._lastcalstate_defaults)
        changedvalues = [x[0] for x in caldiff['valuediff']] #TODO: deal with unchanged values in the middle of strings
        self.kv.clearkv()
        if blank:
            self.loadblankkv()
        self.load_kv_from_module( calcontainer=self.cal, limitlist = changedvalues)

    def save_kv_to_module(self, writetoflash = True, skipclosevalues=False, rawcal=False):
        self._get_cal_map_ifneeded()
        if rawcal is 2: # save both
            kvwriteresult = self.calstate(setval=self.getcalfromkv(self.rawcal.kvdict), progress=True, skipclosevalues=skipclosevalues)
            kvwriteresult2 = self.calstate(setval=self.getcalfromkv(), progress=True, skipclosevalues=skipclosevalues)
            kvwriteresult.__dict__.update(kvwriteresult2.__dict__)
        elif rawcal:
            kvwriteresult = self.calstate(setval=self.getcalfromkv(self.rawcal.kvdict), progress=True, skipclosevalues=skipclosevalues)
        else:
            kvwriteresult = self.calstate(setval=self.getcalfromkv(), progress=True, skipclosevalues=skipclosevalues)
        if writetoflash:
            if rawcal:
                kvburnresult = self.calBurn(burn=3)
            else:
                kvburnresult = self.calBurn(burn=1)
        else:
            kvburnresult = None
        return (kvwriteresult, kvburnresult)
    
    def load_kv_from_file(self,filename, calbase = None ):
        if calbase is None:
            calbase = self._kvDictionaryname
        if calbase == 'rawcaldict': # kludge
            self.rawcal.readkvfile(filename=filename)
            self.fixkvorder(self.rawcal,calbase)
        else:
            self.kv.readkvfile(filename=filename)
            self.fixkvorder(self.kv)

    def save_kv_to_file(self,filename,defaultstonone=None, rawcal=False):
        if defaultstonone:
            
            self._get_cal_map_ifneeded()

            sys.stderr.flush()
            sys.stderr.write('Retrieving kv defaults from nITLA')
            sys.stderr.flush()
            time.sleep(0.001)       # allow time for printing              
            self.load_kv_from_module(calcontainer=self.cal_defaults)
        
            self.comparekv(self.kv, self.kv_defaults,sametonone=True).savekvfile(filename=filename)
            
        else:
            if rawcal:                
                return self.rawcal.savekvfile(filename=filename)
            return self.kv.savekvfile(filename=filename)

    def getcalfromkv(self, kvdict = None):
        if kvdict is None:
            caldict = self._flattennesteddict(self.kv.kvdict, sep='__', paddigits = 2)
        else:
            caldict = self._flattennesteddict(kvdict, sep='__', paddigits = 2)
        #for calname, cal in self.cal.__dict__.iteritems():
        #    for name in sorted(caldict):
        #        newname = self._manglename(name,cal.__dict__)
        #        if newname is not name:
        #            caldict[newname] = caldict.pop(name)
        calvals = self.formatted()
        calvals.__dict__.update(caldict)
        return calvals
    

    def comparekv(self, d1, d2, **kwargs):
        comparisonkv = KV.KV()
        comparisonkv.readkvfile( data = self._comparekv( copy.deepcopy(d1), copy.deepcopy(d2),  **kwargs) )
        self.fixkvorder(comparisonkv)
        return comparisonkv

    def _comparekv(self, d1, d2, path="['", oldvals=None, sametonone=False ):
        if hasattr(d1, 'kvdict'):
            return self._comparekv(d1.kvdict, d2, path, oldvals, sametonone)
        
        if hasattr(d2, 'kvdict'):
            return self._comparekv(d1, d2.kvdict, path, oldvals, sametonone)

        if oldvals is None:
            oldvals = self.textlist()
        
        for key in d1.keys():
            if str(key).startswith('_'):
                continue
            
            if not d2.has_key(key):
                print path + "']:"
                print key + " as key not in d2\n"
            else:
                if isinstance(d1[key], dict) and not (d1[key]._isstring() or d2[key]._isstring()):
                    mypath = copy.copy(path)
                    if path == "['":
                        mypath = path + key
                    else:
                        mypath = mypath + "']['" + key
                    self._comparekv(d1[key],d2[key], mypath, oldvals, sametonone)
                else:
                    if type(key) is type('hello'):
                        keystr = "'" + key + "'"
                    else:
                        keystr = str(key)

                    if isinstance(d1[key], dict) and (d1[key]._isstring() or d2[key]._isstring()):
                        
                        for k,v in d1[key].items():
                            if v == 255:
                                d1[key][k] = 0

                        for k,v in d2[key].items():
                            if v == 255:
                                d2[key][k] = 0

                    if d1[key] == d2[key]:
                        if sametonone:
                            oldvals.append( path + "'][" + keystr + "] = None # " + self.kv.entrytostring( d2[key] ) )
                    else:
                        oldvals.append( path + "'][" + keystr +'] = ' + self.kv.entrytostring( d1[key] ) + ' # ' + self.kv.entrytostring( d2[key] ) )
                        
        return oldvals
                        
                        
    def _get_nestedcalmap_from_caltable(self):
        nestedcalmap = self.kv.nested_dict()
        for index, row in self._caltable.iterrows():
            keys = row['variable'].split('__')
            value = list(row[['offset','type','Units','comment']])
            tmp = nestedcalmap
            for key in keys[:-1]:
                tmp = tmp[key]
            key=keys[-1]
            tmp[key] = value
        return nestedcalmap
    
    def _set_caltable_from_nestedcalmap(self, nestedcalmap):
        flattened = self._flattennesteddict(nestedcalmap)
        
        self._caltable = pd.DataFrame( flattened.values(), columns=['offset','type','Units','comment'] )
        self._caltable['variable'] = flattened.keys()

    def _calval(self, value):
        if hasattr(value,'real'):
            return value.real
        else:
            return value

    def fwupgrade(self, filename):
        with open(filename,'rb') as fwfile:
            fwcontent = fwfile.read()
        fwcontent += '\xFF' * ( 16 - len(fwcontent) % 4 ) # make sure multiple of 4 bytes
        crc = PyCRC.CRC16.CRC16().calculate( fwcontent )
        
        packet = self.Packet()
        
        datachunks = [fwcontent[i:i+4] for i in range(0, len(fwcontent), 4)]
        
        
        if len(datachunks) > 65534:
            print 'FW image too big ('+ str(len(fwcontent)) + ' bytes)'
            return None

        print 'Sending',len(datachunks) ,'data chunks'
        
        bar = progressbar.ProgressBar(maxval=len(datachunks), 
                                      widgets=[progressbar.Bar('=', '[', ']'),' '
                                               , progressbar.Percentage(),
                                               ' (', progressbar.ETA(), ') '])

        bar.start()
        
        for index, chunk in enumerate(datachunks):

            packet.packed.header.type3.write = True
            packet.packed.header.type3.reg = 0xFC
            packet.packed.header.type3.index16 = index
            packet.packed.payload.uint8array[:] = [ord(c) for c in chunk]
            
            self.sendpacket(packet)
            bar.update(index)

            
        bar.finish()
        
        packet.packed.header.type3.write = True
        packet.packed.header.type3.reg = 0xFC
        packet.packed.header.type3.index16 = 0xFFFF
        packet.packed.payload.uint32 = 0
        packet.packed.payload.uint16 = crc

        return self.sendpacket(packet)
        
        

    def calcompare(self, cal1, cal2):
        """Compare calibration objects

        :param cal1: 
        :param cal2: 
        :returns: calibration differences list of lists:  
            item 1: list of settings in cal1 and not in cal2
            item 2: list of settings in cal2 and not in cal1
            item 3: settings present in both whose values do not match

        :rtype: calibration differences list of lists

        """
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find('(') + 1:-1].split(',')
        args = [s.encode('ascii') for s in args]
        
        dict1 = dict((k, self._calval(v)) for (k, v) in cal1.__dict__.iteritems() if not k.startswith('_'))
        dict2 = dict((k, self._calval(v)) for (k, v) in cal2.__dict__.iteritems() if not k.startswith('_'))

        diff1 = list(set(dict1.keys()) - set(dict2.keys()))
        diff2 = list(set(dict2.keys()) - set(dict1.keys()))

        valuediff = []
        
        for (name) in set(dict1).intersection(set(dict2)):
            if not np.isclose(dict1[name], dict2[name], atol=0) and not np.isnan(dict1[name]):
                valuediff.append( [ name, [ args[0], getattr(cal1,name)], [args[1], getattr(cal2,name) ] ])
        return { 'in_'+args[0]+'_but_not_'+args[1]: diff1, 'in_'+args[1]+'_but_not_'+args[0]: diff2, 'valuediff':valuediff }




    def __del__(self):
        self.disconnect()

    def __repr__(self):
        msg =  'Description : ' + self.get_control_Version() + '\n'
        if self._ttyhandle is not None:
            msg += 'Port        : ' + str(self._ttyhandle._port) + '\n'
            msg += 'Baud        : ' + str(self._ttyhandle.baudrate) + '\n'
        msg += 'Logging     : ' + str(self._OIFlogging) + '\n'
        msg += 'Log File    : ' + str(self._commslogfilename)

        return msg

    @staticmethod
    def hilite(string, status, bold):
        """

        :param string: 
        :param status: 
        :param bold: 

        """
        if not 'TERM' in os.environ:
            return string
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

    def logging(self, OIFlogging=None, append=False):
        """Turns logging on or off.  Clears the log file if 'append' is not True

        :param OIFlogging:  (Default value = None)

        """
        if OIFlogging is None:
            print 'OIF Logging : %r' % (self._OIFlogging)
            print 'Log File    : %s' % (self._commslogfilename)
            return
        else:
            self._OIFlogging = OIFlogging
            if self._OIFlogging:
                try:
                    if append:
                        oiflogfile = open(self._commslogfilename, "a")
                    else:
                        oiflogfile = open(self._commslogfilename, "w")
                    self._logstarttime = self._gettime()
                    oiflogfile.write(
                        "# logging started " + time.asctime() + "\n")
                    oiflogfile.flush()
                    oiflogfile.close()
                    oiflogfile = open(self._commslogfilename, "a")
                except OSError:
                    print "Unable to open logfile", self._commslogfilename
                    self._OIFlogging = False
                    return

    def logfile(self, logfilename=None):
        """Specifies filename for log file

        :param logfilename:  (Default value = None)

        """
        if logfilename is None:
            loggingtimestring = time.asctime().replace(" ", "_").replace(':', '-')
            logfilename = os.path.expanduser("~" + os.sep + "commslog_" + type(self).__name__ + "_"  + loggingtimestring + ".txt")
        
        self._commslogfilename = logfilename
        print 'Logging : %r' % (self._OIFlogging)
        print 'Log File    : %s' % (self._commslogfilename)
        return self._commslogfilename

    def compresslog(self):
        """ """
        if sys.hexversion > 0x02060000:
            bz2filename = self._commslogfilename.replace('.txt', '.txt.bz2')
            if not os.path.isfile(self._commslogfilename):
                print "No comms log file to compress"
                return
            if os.path.isfile(bz2filename):
                print "zipped file exists, not overwriting"  # todo: append
                return
            print 'Compressing', self._commslogfilename, '->', bz2filename
            outfile = bz2.BZ2File(bz2filename, 'bw')
            outfile.write(open(self._commslogfilename, 'r').read())
            outfile.close()
            os.remove(self._commslogfilename)  # danger: sanitize
        else:
            print 'Log compression not supported in this version of python'

    def logentry(self, string=None):
        """Adds an entry to the log file

        :param string:  (Default value = None)

        """
        if (self._OIFlogging):
            oiflogfile = open(self._commslogfilename, "a")
            oiflogfile.write("# " + "%04.6fs: " % (self._gettime() - self._logstarttime) + string + "\n")
            oiflogfile.flush()
        else:
#            if self._print_once:
#                self._print_once = 0
#                print self.hilite("Warning: Not logging OIF transactions. Use\n it.logfile(<filename>) to set log filename and\n it.logging(True) to enable logging", False, True)
            print 'Unable to write log entry', string
        return

    def datalogentry(self, string=None):
        """

        :param string:  (Default value = None)

        """
        if (self._OIFlogging):
            oiflogfile = open(self._commslogfilename, "a")
            oiflogfile.write(
                "# " + "%04.6fs: " %
                (float(string.split(' ')[0]) - self._logstarttime) + 'Datalog ' + string.split(' ', 1)[-1] + "\n")
            oiflogfile.flush()
        else:
#            if self._print_once:
#                self._print_once = 0
#                print self.hilite("Warning: Not logging OIF transactions. Use\n it.logfile(<filename>) to set log filename and\n it.logging(True) to enable logging", False, True)
            print 'Unable to write log entry', string
        return

    def hostbaudrate(self, baudrate = None):
        if self._ttyhandle is not None:
            if baudrate is not None:
                self._ttyhandle.baudrate = baudrate
                time.sleep(0.05)
            return self._ttyhandle.baudrate
        return None
        
    def buildstring(self, remote=0):
        """Returns Firmware build string

        :param remote:  (Default value = False)

        """
        self._buildstring = self.reg(0xB0, remote=remote, write=1).split('\x00')[0]
        return self._buildstring
    

    def _getcachefilename(self,headernum,crc=None):
        if crc is None:
            crc = self._getheaderCRC(headernum)
            if crc is None:
                return None
        
        filename = type(self).__name__ + '_' + "".join(c if c.isalnum() or c in ('.','_') else '_' for c in '%02d_'%headernum + '%08X' % crc[1] +'_'+crc[0] ).rstrip()
        return filename

    def _getheaderfromunit(self,headernum, progress=False, usecache=True, crc=None):
        """Returns calibration header file from unit
        """
        
        cachefilename =  self._getcachefilename(headernum=headernum,crc=crc)
        
        if cachefilename is None:
            return None
        
        cachefilename = self._cachedir + os.sep + cachefilename

        data=''

        if usecache and os.path.isfile(cachefilename):
            if progress:
                print 'Cache entry found (' + cachefilename + ")"
            with open(cachefilename,"rb") as myfile:
                data = myfile.read()
        else:
            ndx = 0
            newdata = data = self.reg(regnum=0xCC, index=ndx, index2=headernum, write=1)
            while len(newdata) > 0:
                ndx += 1
                newdata = self.reg(regnum=0xCC, index=ndx, index2=headernum, write=1)
                data += newdata
                if progress and not ndx%5:
                    sys.stdout.write('.')
                    sys.stdout.flush()
            if len(data) > 0:
                if usecache:
                    with open(cachefilename,"wb") as myfile:
                        myfile.write(data)

        if len(data) > 0:
            decodeddata = zlib.decompress(data, 16+zlib.MAX_WBITS)
            self._keys[headernum] = data[-4:] 
        else:
            decodeddata = None
        return decodeddata

    def _getheaderCRC(self,headernum):
        """Returns header CRC
        """
        try:
            data = self.decodeuint32array(self.reg(regnum=0xCD, index2=headernum))
            if len(data) > 0:
                date = datetime.datetime.fromtimestamp(data[0]).strftime('%Y-%m-%d %H:%M:%S')
                return [date , data[1]]
            else:
                return None
        except self.ModuleError:
            return None
 
    def _unlockheader(self, headernum):
        
        if self._keys[headernum] is not None:
            
            packet = self.Packet()
            packet.packed.header.type1.index2 = headernum
            packet.packed.header.type1.reg = 0xCD
            packet.packed.header.type1.write = True
            
            packet.packed.payload.uint32 = self.decodeuint32array(self._keys[headernum])[0]
            
            self._inunlock = True
            return self.sendpacket(packet)
        
        else:
            print "No key available"

    
    def setcalmapfromunit(self, calheader=None, progress=True, usecache=True):
        
        self._caltable = pd.DataFrame()
        self._keys = [None] * 20


        bridgefilename = self._bridgedir + os.sep + self._getcachefilename(headernum=0)
        bridgeincache = os.path.isfile(bridgefilename)

        if usecache and bridgeincache:
            if progress:
                print 'Bridge entry found (' + bridgefilename + ")"
            with bz2.BZ2File(bridgefilename, 'r') as handle:
#            with open(bridgefilename ,'rb') as handle:
                loadeddat = pickle.load(handle)
            self._keys = loadeddat[0]
            self._caltable = loadeddat[1]
                
        if calheader is None and not bridgeincache:
            calheader = self._getheaderfromunit(headernum=0, progress=progress)
            if type(self).__name__ == 'LSRcontrol':
                self._generatecaltable(content=calheader, nanoDevice=True, progress=True)
            else:
                self._generatecaltable(content=calheader, nanoDevice=False, progress=True)
            tosave = [ self._keys, self._caltable ]
            with bz2.BZ2File(bridgefilename, 'w') as handle:
#            with open(bridgefilename ,'wb') as handle:
                pickle.dump(tosave, handle)

        if self._caltable.shape[0] > 0:
            self._cmdcounter = 0
            self.cal = self.CALCONTAINER()
            self.cal_defaults = self.CALCONTAINER()
            self.cal_flash = self.CALCONTAINER()
            self._addcalfunctions()  # add to self.ctrl
            #self._unlockheader(0)
        else:
            print 'No data: Unable to set cal from unit'

                
    def _substbitshifts(self, string):
        if type(string) is type('hello') and '<<' in string:
            split = string.split('<<')
            return int(split[0]) << int(split[1])
        else:
            return string
            
            
    def setstatemachinemapfromunit(self):
        fsmheader = self._getheaderfromunit(headernum=3)
        if fsmheader is None:
            print self.hilite("No data: Unable to set state machine map from unit", False, True)
            return
        else:
            anystatepattern='dfkujnsgku'

            eventtypes = re.findall('enum (.*?)_EVENT',fsmheader)
            statetypes = re.findall('enum (.*?)_STATE',fsmheader)
            tasks = re.findall(' (.*?)_taskstate',fsmheader)
            
            if len(tasks) == 0:
                self.task = enum.Enum('task',{'DUMMY':0})  # workaround forr old version of enum module that doesn't support empty enum
            else:
                self.task = enum.Enum('task',{ tasks[i].upper():i for i in range(0, len(tasks) ) })
            
            if eventtypes != statetypes:
                print self.hilite("mismatch between event types ("+str(eventtypes)+") and state types ("+str(statetypes)+")", False, True)

            #transitiontables = re.findall('transition_t TRANS\[\]=(.*?)};',fsmheader,flags=re.MULTILINE | re.DOTALL)
            inittables = re.findall('stateInitTableEntry INIT\[\]=(.*?)};',fsmheader,flags=re.MULTILINE | re.DOTALL)

            #print 'Creating FSMs:',
            
            self.state = self.STATECONTAINER()
            self.event = self.EVENTCONTAINER()

            for fsm in statetypes:
                #print fsm,
                states = re.findall('enum '+fsm+'_STATE.*?{(.*?)};',fsmheader,flags=re.MULTILINE | re.DOTALL)[0]
                events = re.findall('enum '+fsm+'_EVENT.*?{(.*?)};',fsmheader,flags=re.MULTILINE | re.DOTALL)[0]
                                
                fsm=fsm.upper()
                
                #if fsm=='TEC':
                #    fsm='UMODTEC' # support historical umod tec task name
                
                #transitiontable = [x for x in transitiontables if fsm+'_' in x][0]
                inittable = [x for x in inittables if fsm+'_' in x]
                if len(inittable) > 0:
                    inittable = inittable[0]
                else:
                    inittable = None
                                
                # todo: deduplicate code
                    
                texttoread=StringIO(events.replace('=','@').replace(',','@').replace('//','@'))
                
                dfevents = pd.read_csv(texttoread, sep="@", names =['event','number','comment'])
                    
                dfevents.number = dfevents.number.apply(self._substbitshifts)
                dfevents.number = dfevents.number.apply(lambda x:pd.eval(x,engine='numexpr'))
                dfevents = dfevents[~dfevents.event.str.contains('_SAME_STATE')]
            
                dfevents['event'] = dfevents['event'].map(lambda x: x.strip()[len(fsm)+1:])
                dfevents['comment'] = dfevents['comment'].map(lambda x: '' if isinstance(x, float) else "\\n".join(textwrap.wrap(x,30)))
            
                if len(dfevents.number.unique()) != len(dfevents.number):
                    print self.hilite(' '+fsm+' event enums are duplicated!', False, True)
                
                dfevents = dfevents[~dfevents.event.str.contains(anystatepattern)]
                dfevents = dfevents[ dfevents.event.str.len() > 0 ]
                    
                setattr(self.event,fsm, Enum(fsm, pd.Series(dfevents.number.values, index=dfevents.event).to_dict()))

                texttoread=StringIO(states.replace('=','@').replace(',','@').replace('//','@'))
                
                dfstates = pd.read_csv(texttoread, sep="@", names =['state','number','comment'])

                dfstates.number = dfstates.number.apply(self._substbitshifts)
                dfstates.number = dfstates.number.apply(lambda x:pd.eval(x,engine='numexpr'))
                    
                dfstates = dfstates[~dfstates.state.str.contains('_SAME_STATE')]
            
                dfstates['state'] = dfstates['state'].map(lambda x: x.strip()[len(fsm)+1:])
                dfstates['comment'] = dfstates['comment'].map(lambda x: '' if isinstance(x, float) else "\\n".join(textwrap.wrap(x,30)))
            
                if len(dfstates.number.unique()) != len(dfstates.number):
                    print self.hilite(' '+fsm+' state enums are duplicated!', False, True)
               
                dfstates = dfstates[~dfstates.state.str.contains(anystatepattern)]
                dfstates = dfstates[ dfstates.state.str.len() > 0 ]

                setattr(self.state,fsm, Enum(fsm, pd.Series(dfstates.number.values, index=dfstates.state).to_dict()))

            sys.stdout.write('\n')
            sys.stdout.flush()


    def dumpstack(self):
        """ """
        stack = inspect.stack()
        print
        for stackndx in range(self._echodepth, 2, -1):
            if stackndx >= len(stack):
                break
            callerframerecord = stack[stackndx]
            frame = callerframerecord[0]
            info = inspect.getframeinfo(frame)
            if os.path.basename(info.filename) != os.path.basename(__file__).strip("c"):  # info.filename != "LSRIO.py"
                if os.path.isfile(info.filename):
                    print self.hilite(str(info.filename) + ' ' + str(info.lineno).ljust(5) + linecache.getline(info.filename, info.lineno).rstrip().lstrip(), True, False)

    def sendcommand(self, cmd, retries=3, timeout=None):
        """

        :param cmd: 
        :param retries:  (Default value = 3)

        """
        
        if self._ttyhandle is None:
            raise IOError('Not connected')

        if len(cmd) > 0:
            cmd = bytearray(cmd)
            cmd[0] |= self._cmd_id_setbits
            cmd[0] &= ~self._cmd_id_clearbits

            if not self._inunlock:
                self._lastsentcmd = copy.deepcopy(cmd)


        #pb self._ttyhandle = self.it._getSerialHandle()
        for tries in range(0, retries):
            try:
                # print "Writing:" + " ".join("{:02X}".format(ord(c)) for c in cmd)
                # time.sleep(0.02) # prevent unit crashing
                sys.stdout.flush()
                if self._echocaller:  # help debugging by printing caller
                    self.dumpstack()
                if self._OIFlogging:
                    oiflogfile = open(self._commslogfilename, "a")
                    oiflogfile.write("%04.6fs " % (self._gettime() - self._logstarttime))
                    oiflogfile.write('Tx: ')
                    if self._debug_rs232:
                        print 'Tx:',
                    for ch in cmd:
                        oiflogfile.write('%02X ' % ch)
                        if self._debug_rs232:
                            print ('%02X' % ch),
                    oiflogfile.flush()
                elif self._debug_rs232:
                    print 'Tx:',
                    for ch in cmd:
                        print ('%02X' % ch),
                if len(cmd) > 0:
                    self._ttyhandle.flushInput()   # in ver 3.0
                    self._writetimestart = self._gettime()
                    self._ttyhandle.write(cmd)
                    if "outWaiting" in dir(self._ttyhandle):
                        while self._ttyhandle.outWaiting():
                            time.sleep(0.001)
                    else:
                        self._ttyhandle.flush()
                self._writedonetime = self._gettime()
                reply = None
                try:
                    reply = self.getreply(timeout=timeout)
                except self.ModuleError as e:
                    if (not self._inunlock) and str(e).startswith('Cal locked'): # cal is locked.  Try to unlock and retry command
                        sys.stderr.write('\nCal settings are locked---trying to unlock...\n')
                        sys.stderr.flush()
                        self._inunlock = True
                        self._unlockheader(0)
                        reply = self.sendcommand(self._lastsentcmd)
                    else:
                        raise
#                    if (self._inunlock != 2) and str(e) == 'Incorrect Key':
#                        sys.stderr.write('Incorrect Key---trying to acquire key...\n')
#                        sys.stderr.flush()
#                        self.setcalmapfromunit()
#                        self._inunlock = 2
#                        reply = self.sendcommand(self._lastsentcmd)
                self._inunlock = False
                if reply is not None:
                    return reply 
            except self.ModuleNoResponse:
                retrystr = "Retry " + str(tries + 1) + '...'
                print retrystr
                self.logentry(retrystr)
                continue
            break

    def getreply(self,timeout=None):
        """ """
        if timeout is not None:
            if hasattr(self._ttyhandle,'timeout'):
                oldtimeout = self._ttyhandle.timeout
                self._ttyhandle.timeout = timeout
            else:
                print self.hilite('Unable to override timeout.  Please check serial module version', False, True )
        flags = self._ttyhandle.read(size=1)
        databytes = self._ttyhandle.read(size=2)
        if self._OIFlogging:
            oiflogfile = open(self._commslogfilename, "a")
            oiflogfile.write('Rx: ')
            if self._debug_rs232:
                print 'Rx:',
            for ch in flags:
                oiflogfile.write('%02X ' % ord(ch))
                if self._debug_rs232:
                    print ('%02X' % ord(ch)),
            for ch in databytes:
                oiflogfile.write('%02X ' % ord(ch))
                if self._debug_rs232:
                    print ('%02X' % ord(ch)),
            oiflogfile.flush()
        elif self._debug_rs232:
            print 'Rx:',
            for ch in flags:
                print ('%02X' % ord(ch)),
            for ch in databytes:
                print ('%02X' % ord(ch)),
        if len(databytes) == 0:
            errorstr = "No response from module after waiting " + str((self._gettime() - self._writedonetime) * 1000.0) + "ms"
            print self.hilite(errorstr, False, True)
            if self._OIFlogging:
                self.logentry("No Response from module")
            self.dumpstack()
            #print "Raising exception because module is not responding"
            if self._erroroccurred:
                if self._abortscriptonerror:
                    self._erroroccurred = False
                    tmperrors = self._errors
                    self._errors = ''
                    self.dumpstack()
                    raise self.ModuleError(tmperrors)
            raise self.ModuleNoResponse(errorstr)
            if timeout is not None:
                self._ttyhandle.timeout = oldtimeout
            return ''
            # self._ttyhandle.close()
            # raise ValueError('Device Timeout')
        iserror = ord(flags) & 0x01
        iswarning = ord(flags) & 0x02
        databytes = struct.unpack('<H', databytes)[0]
        # print 'Returned bytes:', databytes
        rawdata = self._ttyhandle.read(size=databytes)
        writetimems = (self._gettime() - self._writedonetime) * 1000.0
        # print " ".join("{:02X}".format(ord(c)) for c in rawdata)
        if self._OIFlogging:
            oiflogfile = open(self._commslogfilename, "a")
            for ch in rawdata:
                oiflogfile.write('%02X ' % ord(ch))
                if self._debug_rs232:
                    print ('%02X' % ord(ch)),
            oiflogfile.write('%2.3fms\n' % writetimems)
            oiflogfile.flush()
        if self._debug_rs232:
            for ch in rawdata:
                print ('%02X' % ord(ch)),
            print ' '       # CR
        if iserror:
            # print "Error:", rawdata
            if len(self._errors) > 0:
                self._errors += " ; "
            self._errors += rawdata
            self._erroroccurred = True
            if self._OIFlogging:
                oiflogfile = open(self._commslogfilename, "a")
                oiflogfile.write( "# Error: " + rawdata + "\n")
                oiflogfile.flush()
            if timeout is not None:
                self._ttyhandle.timeout = oldtimeout
            return self.sendcommand(cmd='')
        elif iswarning:
            sys.stdout.flush()
            warnings.warn(rawdata)
            sys.stdout.flush()
            if self._OIFlogging:
                oiflogfile = open(self._commslogfilename, "a")
                oiflogfile.write( "# Warning: " + rawdata + "\n")
                oiflogfile.flush()
            if timeout is not None:
                self._ttyhandle.timeout = oldtimeout
            return self.sendcommand(cmd='')
        else:
            if self._erroroccurred:
                if self._abortscriptonerror:
                    self._erroroccurred = False
                    tmperrors = self._errors
                    self._errors = ''
                    self.dumpstack()
                    # print "Raising exception because module reports error"
                    raise self.ModuleError(tmperrors)
            if timeout is not None:
                self._ttyhandle.timeout = oldtimeout
            return rawdata

    def printlog(self, lines=20):
        """Prints the last n lines of the log (default 20)

        :param lines:  (Default value = 20)

        """
        try:
            f = open(self._commslogfilename, "r")
        except:
            if (not self._OIFlogging):
                print "Unable to open logfile (and logging is not enabled)"
            else:
                print "Unable to open logfile:", self._commslogfilename,  sys.exc_info()[0]
            return
        if sys.hexversion > 0x02060000:  # temporary fix (disable) for this failing in python 2.2
            f.seek(0, 2)
            endbyte = f.tell()
            lines_to_go = lines
            blocknum = -1
            blocks = []
            while lines_to_go > 0 and endbyte > 0:
                if (endbyte - 1024 > 0):
                    f.seek(blocknum * 1024, 2)
                    blocks.append(f.read(1024))
                else:
                    f.seek(0, 0)
                    blocks.append(f.read(endbyte))
                lines_found = blocks[-1].count('\n')
                lines_to_go -= lines_found
                endbyte -= 1024
                blocknum -= 1
            all_read_text = ''.join(reversed(blocks))
            print "Log file: " + self._commslogfilename
            print "Showing last", lines, "lines:"
            print '\n'.join(all_read_text.splitlines()[-lines:])
        else:
            print 'Log print not supported in this version of python'

    @staticmethod
    def decodefloatarray(rawdata):
        """

        :param rawdata: 

        """
        floatlist = []
        for rawfloat in [rawdata[i:i + 4] for i in range(0, len(rawdata), 4)]:
            if len(rawfloat) is not 4:
                floatlist.append(np.nan)
            else:
                floatlist.append(struct.unpack('<f', rawfloat)[0])
        return floatlist


#    @staticmethod
    def decodeufixed7array(self,rawdata):
        """

        :param rawdata: 

        """
        datlist = []
        for rawfloat in [rawdata[i:i + 4] for i in range(0, len(rawdata), 4)]:
            datlist.append( self._fixedptfromuint32(struct.unpack('<L', rawdata)[0], pt=7) )
        return datlist
    
    @staticmethod
    def decodedoublearray(rawdata):
        """

        :param rawdata: 

        """
        floatlist = []
        for rawfloat in [rawdata[i:i + 8] for i in range(0, len(rawdata), 8)]:
            floatlist.append(struct.unpack('<d', rawfloat)[0])
        return floatlist
    
    @staticmethod
    def decodeuint64array(rawdata):
        """

        :param rawdata: 

        """
        intlist = []
        for rawint in [rawdata[i:i + 8] for i in range(0, len(rawdata), 8)]:
            intlist.append(struct.unpack('<Q', rawint)[0])
        return intlist

    @staticmethod
    def decodeuint32array(rawdata):
        """

        :param rawdata: 

        """
        intlist = []
        for rawint in [rawdata[i:i + 4] for i in range(0, len(rawdata), 4)]:
            intlist.append(struct.unpack('<L', rawint)[0])
        return intlist

    @staticmethod
    def decodeuSfpxparray(rawdata):
        """

        :param rawdata: 

        """
        intlist = []
        for rawint in [rawdata[i:i + 4] for i in range(0, len(rawdata), 4)]:
            intlist.append(struct.unpack('<l', rawint)[0] / float(1 << 10))
        return intlist

    @staticmethod
    def decodeuint16array(rawdata):
        """

        :param rawdata: 

        """
        intlist = []
        for rawint in [rawdata[i:i + 2] for i in range(0, len(rawdata), 2)]:
            intlist.append(struct.unpack('<H', rawint)[0])
        return intlist

    @staticmethod
    def decodeint16array(rawdata):
        """

        :param rawdata: 

        """
        intlist = []
        for rawint in [rawdata[i:i + 2] for i in range(0, len(rawdata), 2)]:
            intlist.append(struct.unpack('<h', rawint)[0])
        return intlist

    @staticmethod
    def decodeuint8array(rawdata):
        """

        :param rawdata: 

        """
        intlist = []
        for rawint in [rawdata[i] for i in range(0, len(rawdata), 1)]:
            intlist.append(ord(rawint))
        return intlist

    @staticmethod
    def decodeuint(rawdata):
        """

        :param rawdata: 

        """
        # print ord(rawdata[0])
        return [ord(rawdata[0])]

    def debugcaller(self, setting=None):
        """

        :param setting:  (Default value = None)

        """
        'Get/Set caller (stack) debug'
        if setting is not None:
            self._echocaller = setting
        return self._echocaller

    def debugRS232(self, level=None):
        """

        :param level:  (Default value = None)

        """
        'Get/Set debug level'
        if level is not None:
            self._debug_rs232 = level
        return self._debug_rs232

    def sendpacket(self, packet, timeout=None):
        """

        :param packet: 

        """
        return self.sendcommand(str(bytearray(packet.rawdata)), timeout=timeout)

    def reg(self, regnum, val1=0, val2=0, val3=0, val4=0, index=0, index2=0, write=0, option=0, remote=0):
        """

        :param regnum:  Register number
        :param val1-4:  chars to write
        :param index:   subcommand1
        :param index2:  subcommand2
        :param write:   1=write, 0=read
        :param option:  1=option
        :param remote:  1=remote cmd

        """
        flags = 0
        if(write):
            flags |= self._LSR_WRITE_BIT
        if(remote):
            flags |= self._LSR_REMOTE_BIT
        if(option):
            flags |= self._LSR_OPTION_BIT
            
        #if regnum == 0xCB:  # this has suddenly started failing for some reason on cal stations...
        #    timeout = 0.5
        #else:
        timeout = None
        return self.sendcommand(chr(flags) + chr(regnum) + chr(index) + chr(index2) +
                                chr(val1) + chr(val2) + chr(val3) + chr(val4), timeout=timeout )

    def reg_uint16(self, regnum, val1=0, val2=0, index=0, index2=0, write=0, option=0, remote=0):
        """

        :param regnum:  Register number
        :param val1-2:  uints to write
        :param index:   subcommand1
        :param index2:  subcommand2
        :param write:   1=write, 0=read
        :param option:  1=option
        :param remote:  1=remote cmd

        """
        flags = 0
        if(write):
            flags |= self._LSR_WRITE_BIT
        if(remote):
            flags |= self._LSR_REMOTE_BIT
        if(option):
            flags |= self._LSR_OPTION_BIT
        if write:
            return self.sendcommand(chr(flags) + chr(regnum) + chr(index) + chr(index2) +
                                struct.pack('<H', val1) + struct.pack('<H', val2))
        else:
            return self.decodeuint16array(self.sendcommand(chr(flags) + chr(regnum) + chr(index) + chr(index2) +
                                struct.pack('<H', val1) + struct.pack('<H', val2)))

    def reg_int16(self, regnum, val1=0, val2=0, index=0, index2=0, write=0, option=0, remote=0):
        """

        :param regnum:  Register number
        :param val1-2:  ints to write
        :param index:   subcommand1
        :param index2:  subcommand2
        :param write:   1=write, 0=read
        :param option:  1=option
        :param remote:  1=remote cmd

        """
        flags = 0
        if(write):
            flags |= self._LSR_WRITE_BIT
        if(remote):
            flags |= self._LSR_REMOTE_BIT
        if(option):
            flags |= self._LSR_OPTION_BIT
        if write:
            return self.sendcommand(chr(flags) + chr(regnum) + chr(index) + chr(index2) +
                                struct.pack('<h', val1) + struct.pack('<h', val2))
        else:
            return self.decodeint16array(self.sendcommand(chr(flags) + chr(regnum) + chr(index) + chr(index2) +
                                struct.pack('<h', val1) + struct.pack('<h', val2)))
        
    def reg_uint32(self, regnum, val=0, index=0, index2=0, write=1, option=0, remote=0):
        """

        :param regnum:  Register number
        :param val:     uint32 to write
        :param index:   subcommand1
        :param index2:  subcommand2
        :param write:   1=write, 0=read
        :param option:  1=option
        :param remote:  1=remote cmd

        """
        flags = 0
        if(write):
            flags |= self._LSR_WRITE_BIT
        if(remote):
            flags |= self._LSR_REMOTE_BIT
        if(option):
            flags |= self._LSR_OPTION_BIT
        if(write):
            return self.sendcommand(chr(flags) + chr(regnum) + chr(index) + chr(index2) +
                                struct.pack('<I', val) )
        else:
            return self.decodeuint32array(self.sendcommand(chr(flags) + chr(regnum) + chr(index) + chr(index2) +
                                struct.pack('<I', val) ))

    def reg_float(self, regnum, val=0, index=0, index2=0, write=0, option=0, remote=0, units=None):
        """

        :param regnum:  Register number
        :param val:     float to write
        :param index:   subcommand1
        :param index2:  subcommand2
        :param write:   1=write, 0=read
        :param option:  1=option
        :param remote:  1=remote cmd
        :param units:   string to append

        """
        flags = 0
        if(write):
            flags |= self._LSR_WRITE_BIT
        if(remote):
            flags |= self._LSR_REMOTE_BIT
        if(option):
            flags |= self._LSR_OPTION_BIT
        if(write):
            return self.sendcommand(chr(flags) + chr(regnum) + chr(index) + chr(index2) +
                                struct.pack('<f', val) )
        else:
            return self._floatwithunits( self.decodefloatarray(self.sendcommand(chr(flags) +
                                     chr(regnum) + chr(index) + chr(index2) + chr(0x00) * 4 ))[0], units=units )

    def calBurn(self, burn=0):
        if(burn == 1):
            result = self.reg(0xCB, index=1, write=1)   # Burn calibraion/Dictionary entries to FLASH.
        elif(burn == 2):
            result = self.reg(0xCB, index=3, write=1)   # Burn cal valid bitmap to FLASH.
        elif(burn == 3):
            result = self.reg(0xCB, index=14, write=1)  # Burn Raw Calibration to FLASH.
        else:
            result = self.reg(0xCB)
        return [ 'Cal Version: 0x' + ''.join(r'{0:02x}'.format(ord(c)) for c in result[:1]),
                 'CRC value: 0x' + ''.join(r'{0:02x}'.format(ord(c)) for c in result[2:])]
            
    def calErase(self, command = 0):
        if(command == 1):
            result = self.reg(0xCB, index=2, write=1)   # Erase calibraion/Dictionary FLASH.
        if(command == 2):
            result = self.reg(0xCB, index=4, write=1)   # Erase cal valid bitmap FLASH.
        if(command == 3):
            result = self.reg(0xCB, index=13, write=1)  # Erase Raw Calibration FLASH.
        else:
            result = self.reg(0xCB)
        return [ 'Cal Version: 0x' + ''.join(r'{0:02x}'.format(ord(c)) for c in result[:1]),
                 'CRC value: 0x' + ''.join(r'{0:02x}'.format(ord(c)) for c in result[2:])]
            
    def calRefresh(self, command = 0):
        if(command == 1):
            result = self.reg(0xCB, index=15, write=1)  # Pull Cal from FLASH or defaults (like startup).
        if(command == 2):
            result = self.reg(0xCB, index=16, write=1)  # Pull Raw Cal from FLASH (if valid).
        else:
            result = self.reg(0xCB)
        return [ 'Cal Version: 0x' + ''.join(r'{0:02x}'.format(ord(c)) for c in result[:1]),
                 'CRC value: 0x' + ''.join(r'{0:02x}'.format(ord(c)) for c in result[2:])]
            
    def validMapCmd(self, action=0, offset=0, size=1):
        if(action == 1):    # Validate bytes in calibration bitmap
            result = self.reg_uint16(0xCB, index=5, write=1, val1=offset, val2=size)
        elif(action == 2):  # Invalidate bytes in calibration bitmap
            result = self.reg_uint16(0xCB, index=6, write=1, val1=offset, val2=size)
        elif(action == 3):  # Request valid/invalid state of bytes in calibration bitmap (RAM COPY)
            result = self.reg_uint16(0xCB, index=7, write=0, val1=offset, val2=size)
        elif(action == 4):  # Request valid/invalid state of bytes in calibration bitmap (FLASH COPY)
            result = self.reg_uint16(0xCB, index=8, write=0, val1=offset, val2=size)
        elif(action == 5):  # Invalidate all bytes in calibration/calibration -bitmap (RAM COPY)
            result = self.reg_uint16(0xCB, index=12, write=1)
        else:
            result = self.reg(0xCB)

        # -Now handle reply-            
        if(action == 3 or action == 4):    # Request if cal bytes are valid or not.
            return result[0] != 0 #['Offset: ' + str(offset) + ' Bytes:' + str(size) + ' Valid:' + str(result)]
        else:
            return [ 'Cal Version: 0x' + ''.join(r'{0:02x}'.format(ord(c)) for c in result[:1]),
                 'CRC value: 0x' + ''.join(r'{0:02x}'.format(ord(c)) for c in result[2:])]

    def calVersion(self):
        returndat = self.reg_uint16(0xCB, index = 17, write=0)
        retval = self.formatted()
        retval.flash_vrsn = returndat[1]
        retval.fw_vrsn = returndat[0]
        retval.ram_vrsn = returndat[2]
        return retval         
        #return [ 'FW Cal Version: ' + str(result[0]) + ' FLASH Cal Version: ' + str(result[1]) ]            
                    
    def validMapDwnldCmd(self, action=1):
        if(action == 1):    # Pull 1st 255 bytes of the calibration valid bitmap.
            result = self.reg_uint16(regnum=0xCB, index=10, write=0)
        elif(action == 2):    # Pull remaining bytes of the calibration valid bitmap.
            result = self.reg_uint16(regnum=0xCB, index=11, write=0)
        return result

    def rdRtos(self, remote=0, command=0, task=0, charval1=0, charval2=0,
               charval3=0, charval4=0):
        """

        :param remote:  (Default value = 0)
        :param command:  (Default value = 0)
        :param task:  (Default value = 0)
        :param charval1:  (Default value = 0)
        :param charval2:  (Default value = 0)
        :param charval3:  (Default value = 0)
        :param charval4:  (Default value = 0)

        """
        regnum = 0xCF
        if remote:
            flags = 0x0B
        else:
            flags = 0x03
        if command == 0:
            return self.sendcommand(chr(flags) + chr(regnum) + chr(command) +
                                chr(task) + chr(charval1) +
                                chr(charval2) + chr(charval3) +
                                chr(charval4))
        else:
            return pd.read_csv(StringIO(self.sendcommand(chr(flags) + chr(regnum) + chr(command) +
                                chr(task) + chr(charval1) +
                                chr(charval2) + chr(charval3) +
                                chr(charval4)).decode('utf-8')),sep='\t',skiprows=2)

    def isrStats(self, remote= 0, start = 0):
        """

        :param remote:  (Default value = 0)
        :param start:  (Default value = 0)

        """
        if remote:
            flags = 0x0B
        else:
            flags = 0x03
        pos = 0
        returndat = self.sendcommand(chr(flags) + chr(0xDB) + chr(4) + 
             chr(start) + chr(0) + chr(0) + chr(0) + chr(0) )
        ipcDefStructure = [
            "ISR Collection Active(1=true): ",
            "Log Index: ",
            " 1: ",
            " 2: ",
            " 3: ",
            " 4: ",
            " 5: ",
            " 6: ",
            " 7: ",
            " 8: ",
            " 9: ",                     # Yeah -it's a hack.
            " 10: ",
            ]
        for varname in ipcDefStructure:
            rawdata=returndat[pos:pos+4]
            decodeddata = hex(struct.unpack('<' + "L",rawdata)[0])
            pos=pos+4
            print str(varname),decodeddata
            

####################################################################################
# Pull serial debug stats.
#	Action==1: Show stats. (clear on read)
#	Action==2: Clear stats.
####################################################################################
    def uartDbg(self, action=1):
        if(action == 1):    # Pull 1st 255 bytes of the calibration valid bitmap.
            returndat = self.reg_uint32(regnum=0xD0, index=0, write=0)
            ipcDefStructure = [
                "Bad Isr Count: ",
                "Bad Isr Index: ",
                "  ISR Status 1: ",
                " UART Status 1: ",
                "    ISR Enab 1: ",
                " RX at Error 1: ",
                "    Ctrl Reg 1: ",
                "  ISR Status 2: ",
                " UART Status 2: ",
                "    ISR Enab 2: ",
                " RX at Error 2: ",
                "    Ctrl Reg 2: ",
                "  ISR Status 3: ",
                " UART Status 3: ",
                "    ISR Enab 3: ",
                " RX at Error 3: ",
                "    Ctrl Reg 3: ",
                " RX at Error 4: ",
                "  ISR Status 4: ",
                " UART Status 4: ",
                "    ISR Enab 4: ",
                "    Ctrl Reg 4: ",
                " RX buffer Count: ",
                "  Rx Buff 1: ",
                "  Rx Buff 2: ",
                "  Rx Buff 3: ",
                "  Rx Buff 4: ",
                "  Rx Buff 5: ",
                "  Rx Buff 6: ",
                "  Rx Buff 7: ",
                "  Rx Buff 8: ",
                "  Rx Buff 9: ",
                "  Rx Buff 10: ",
                "  Rx Buff 11: ",
                "  Rx Buff 12: ",
                "  Rx Buff 13: ",
                "  Rx Buff 14: ",
                "  Rx Buff 15: ",
                "  Rx Buff 16: ",
                "Processed Msg Count: ",
                "Com Inter-Byte Timeout Count: ",
                ]
            print "Bad ISR bit-map: 0x01=Frame Error, 0x02=Parity Error, 0x08=Overrun Error."
            pos = 0
            for varname in ipcDefStructure:
                decodeddata=returndat[pos]
                pos=pos+1
                print str(varname),hex(decodeddata)
        elif (action == 2):  
            self.reg_uint32(regnum=0xD0, index=0, write=0)

    def newevent(self, task, event, nowait=False):
        """

        :param task: 
        :param event: 

        """
        if not isinstance(task, self.task):
            raise Exception('Must specify a task')
            return
                
        packet = self.Packet()
        packet.packed.header.type1.write = True
        packet.packed.header.type1.reg = 0x39
        packet.packed.header.type1.index = task.value
        packet.packed.payload.uint32 = event.value

        retval = self.sendpacket(packet)
    
        if not nowait:
            time.sleep(0.05) # kludge to make sure event has enough time to be acted on
        return retval

    def writefloat(self, reg, floatval, index = 0, index2 = 0):
        packet = self.Packet()
        packet.packed.header.type1.write = True
        packet.packed.header.type1.reg = reg
        packet.packed.header.type1.index = index
        packet.packed.header.type1.index2 = index2
        packet.packed.payload.float = floatval

        return self.sendpacket(packet)
        
    def writeufixed7pt(self, reg, fixed7ptvalasfloat, index = 0, index2 = 0):
        packet = self.Packet()
        packet.packed.header.type1.write = True
        packet.packed.header.type1.reg = reg
        packet.packed.header.type1.index = index
        packet.packed.header.type1.index2 = index2
        packet.packed.payload.uint32 = self._fixedpttouint32(fixed7ptvalasfloat, pt=7) 

        return self.sendpacket(packet)

    def getstates(self): # fixme: task names should come from FW
        """ """
        returndat = self.reg(0x40)
        retval = self.formatted()
        for state in self.task:
            try:
                dataval = getattr(self.state, state.name)(ord(returndat[state.value]))
            except (ValueError):
                dataval = 'INVALID (state '+ str(ord(returndat[state.value])) + ' not mapped)'
            except (AttributeError):
                dataval = 'INVALID (missing state mapper)'
            setattr(retval, self.task(state.value).name, dataval)
        return retval

    def gettaskstatus(self, task):
        """

        :param task: 

        """
        if not isinstance(task, self.task):
            raise Exception('Must specify a task')
            return
                
        packet = self.Packet()
        packet.packed.header.type1.write = True
        packet.packed.header.type1.reg = 0x41
        packet.packed.header.type1.index = task.value

        return self.decodeuint8array(self.sendpacket(packet))
    

    def waitforstate(self, task, state, timeout=5.0, log99=False):
        """

        :param task: 
        :param state: 
        :param timeout:  (Default value = 5.0)
        :param log99:  (Default value = True)

        """
        starttime = time.time()
        i=0
        while (1):
            i = i + 1
            if not i % 100:
                sys.stdout.write('.')
                sys.stdout.flush()
            if log99:
                self.readx99()
            if self.checkinstate(task, state):
                return True
            if time.time() - starttime > timeout:
                return False

    def checkinstate(self, task, state):
        """

        :param task: 
        :param state: 

        """
        states = self.getstates()
        return getattr(states, task.name) == state

    def getcpuusage(self):
        """Reports CPU usage (%)"""
        return ord(self.reg(0x11, write=1))


    def savedata(self, filename, myobject, compact=False):
        """

        :param filename: 
        :param myobject: 

        """
        # strip the units, and send the real value
        varstosave = [a for a in dir(myobject) if not a.startswith('_') ]
        for varname in varstosave:
            if hasattr(myobject,'real' ):
                setattr( myobject, varname, getattr( myobject, varname).real )
        
        if hasattr( myobject,'__dict__'):
            ordered_data = collections.OrderedDict(sorted(myobject.__dict__.items()))        
            ordered_data = collections.OrderedDict((k, v) for (k, v) in ordered_data.iteritems() if not k.startswith('_'))
        else:
            ordered_data = myobject
            
        with open(filename,"w") as myfile:
            if compact:
                json.dump(ordered_data, myfile, separators=(',', ':') )  
            else:
                json.dump(ordered_data, myfile, indent=4)  



    def loaddata(self, filename):
        """

        :param filename: 

        """
        retval = self.formatted()
        with open(filename,"r") as myfile:
            myobject = json.load(myfile)
        retval.__dict__.update(myobject)
        return retval
    
    def _reg_DA(self, offset, index, value=None, valuetype='float'):

        decodefunction = getattr(self, 'decode' + valuetype + 'array')
                    
        if value is None:
            packet=self.Packet()
            packet.packed.header.type1.reg = 0xDA
            packet.packed.header.type1.index = index
            packet.packed.header.type1.index2 = offset
            packet.packed.header.type1.write = False

            return decodefunction(self.sendpacket(packet))[0]
        else:
            packet=self.Packet()
            packet.packed.header.type1.reg = 0xDA
            packet.packed.header.type1.index = index
            packet.packed.header.type1.index2 = offset
            packet.packed.header.type1.write = True
            
            if valuetype is 'ufixed7':
                packet.packed.payload.uint32 = self._fixedpttouint32(value, pt=7)
            elif valuetype is 'ufixed9':
                packet.packed.payload.uint32 = self._fixedpttouint32(value, pt=9)
            elif valuetype is 'fixed7':
                packet.packed.payload.uint32 = self._fixedpttouint32(value, pt=-7)
            elif valuetype is 'fixed9':
                packet.packed.payload.uint32 = self._fixedpttouint32(value, pt=-9)
            else:
                setattr(packet.packed.payload, valuetype, value)

            return self.sendpacket(packet)
        
    # these must be implemented in the derived class
    def connect(self):
        raise NotImplementedError
        
    def disconnect(self):
        raise NotImplementedError