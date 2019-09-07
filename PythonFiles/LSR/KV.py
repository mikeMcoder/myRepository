# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 10:43:39 2018

@author: mark
"""

#import os
import re
import math
#import pandas as pd
from collections import defaultdict, OrderedDict
import copy

_stringdicts = [ 'rel_back_ot',
                'device_type',
                'release_hw',
                'unique_board_ID',
                'fw_at_calburn',
                'board_id',
                'goldBox_ID',
                'serial_number',
                'rel_back_hw',
                'manufacturer',
                'manufacturing_date',
                'release_ot',
                'release_as',
                'cavity_id',
                'model',
                'rel_back_as' ]

_notstringdicts = [ 'q_table',
                    'modulation_table',
                    's_table' ]

class KVDICT(defaultdict):  # dictionary which remaps legacy keys
    
    def __init__(self, *args, **kwargs):
        super(KVDICT, self).__init__(*args, **kwargs)
        self.__dict__ = self
        self._legacymapping = {}
    

    
        self._isstr = False
        self._notstr = False
        self._comments = {}
        self._orders = {}
        
    def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
        if isinstance(key, basestring):
            for k, v in self._legacymapping.iteritems():
                if key == k:
                    key = v
        if isinstance(value, str):
            value = KVDICT(None,self._string_to_dict(value))

        
        if key in self and "pt" in dir(self[key]):
            return defaultdict.__setitem__(self, key, type(self[key])(value, units=self[key].units, pt=self[key].pt) )

        if key in self and "withunits" in str(type(self[key])):
            return defaultdict.__setitem__(self, key, type(self[key])(value, units=self[key].units) )


        if value is None and key in self:
            if "_isstring" in dir(self[key]):
                self[key].invalidate()
                return # what to return here?

        if "_isstring" in dir(value):
            value._isstr = key in _stringdicts
            value._notstr = key in _notstringdicts

        if self._isstring() and isinstance(value, dict) and key not in ['_comments','_orders']:
            raise TypeError("Can't add kv entry as subset of string " + str(key) + ' ' + str(value))

        return defaultdict.__setitem__(self, key, value)
    
    def __getitem__(self, key):
        if isinstance(key, basestring):
            for k, v in self._legacymapping.iteritems():
                if key == k:
                    key = v         
        return defaultdict.__getitem__(self, key)
    
    def comment(self, key, value=None):
        if value is None:
            return self._comments.get(key,None)
        else:
            self._comments[key] = value
    
    def _order(self, key, value=None):
        if value is None:
            return self._orders.get(key,None)
        else:
            self._orders[key] = value
    
    def __repr__(self):
        if len(self._comments) == 1:
            commentstr = ' # ' + str( self._comments.values()[0] )
        elif len(self._comments) > 1:
            commentstr = ' # ' + str( self._comments )
        else:
            commentstr = ''
            
        if self._isstring():
            strdict = dict((k, v) for k, v in self.items() if not str(k).startswith("_") and v is not None)
            try:
                return  ''.join(map(chr,
                                   OrderedDict(sorted(strdict.items(), key=lambda e: int(e[0]))).values())).split('\x00', 1)[0] + commentstr
            except:
                # screwed up string.  This should never happen.  Represent as dict so __repr__ isn't broken
                self._isstr = False
        
        return KV.getkvtext(self)
    
    def _isstring(self):

        if self._isstr:
            return True

        if self._notstr:
            return False
        
        # not in either list... try to guess

        keys = self.keys()
        if all(isinstance(x, int) for x in keys):
            if min(keys) != 0: # not begin at zero
                return False 
            if len(sorted(set(range(keys[0], keys[-1] + 1)).difference(keys))) > 0: # missing keys
                return False
        else:
            return False # keys not integers
        return all(isinstance(x, int) for x in self.values()) and \
               all(int(x) < 128 for x in self.values()) and \
               all(int(x) >= 0 for x in self.values()) # all keys and values are integers < 128, treat as string
            
    def _string_to_dict(self,string):
        string = string.strip('\x00') + '\x00'        # NULL terminator
        return dict([(ndx,ord(c)) for ndx,c in enumerate(string)])
        
    def invalidate(self, d=None):
        if d is None:
            d = self
        for key, value in d.iteritems():
            if str(key).startswith('_'):
                continue
            if isinstance(value, dict):
                if not value:
                    continue # skip empty dictionary
            if isinstance(value, dict):
                if "_isstring" in dir(value):
                    self.invalidate(value)
                else:
                    print "Error: Entry is not a KVDICT:", key,value
            else:
                d[key] = None
        return

    def clearcomments(self, d=None):
        if d is None:
            d = self
        for key, value in d.iteritems():
            if str(key) is '_comments':
                d[key]={}
            if str(key).startswith('_'):
                continue
            elif isinstance(value, dict):
                if "_isstring" in dir(value):
                    self.clearcomments(value)
                else:
                    print "Error: Entry is not a KVDICT:", key,value
        return

class Printable(str):
    def __repr__(self):
        return self
    
class KV():
    """
       Converts kv files to and from nested dictionaries
    """
    
    _comment = None

    def __init__(self):
        self.nested_dict = lambda: KVDICT(self.nested_dict)
        self.clearkv()

    def __repr__(self):
        return self.getkvtext(self.kvdict)


    def __setattr__(self, name, value):
        if name == "kvdict" and value is None:
            self.__dict__[name].invalidate()
        else:
            self.__dict__[name] = value

    @staticmethod
    def entrytostring(value):
        if type(value) is not type('hello'):
            if "_isstring" in dir(value):
                if value._isstring():
                    return "'" + str(value) + "'"
            if isinstance(value, dict):
                return str(value.values())
            if value is None:
                valstr = 'None'
            elif math.isnan(value):
                valstr = "float('nan')"
            else:
                if 'fixedpt' in str(type(value)):
                    valstr = value.__repr__()
                else:
                    valstr = '%+.7g' % value
                    if 'float' in str(type(value)) and '.' not in valstr:
                        if 'e' not in valstr:
                            valstr += '.0'
                        else:
                            valstr = re.sub(r'(e)', r'.0\1', valstr)
        else:
            valstr = "'" + value + "'"
            
        return valstr

    @staticmethod
    def kvdict_to_entries( *args, **kwargs):
        retval = KV._kvdict_to_entries(*args, **kwargs)
        return [x[6:] for x in sorted(retval, key=lambda x:x[:5]) ]

    @staticmethod
    def _kvdict_to_entries(d, oldkeys="", oldvals=None):
            
        commentstr = ''
        order =  '%05d ' % 99999
        
        if oldvals is None:
            if d.get('_comments',None) is not None:
                oldvals = [ '00000 # ' + x for x in d._comments]
            else:
                oldvals = []

        for key, value in d.iteritems():
            if str(key).startswith('_'):
                continue
            if isinstance(value, dict):
                if not value:
                    continue # skip empty dictionary
                
            if type(key) is type('hello'):
                keystr = "'" + key + "'"
            else:
                keystr = str(key)
            if len(oldkeys) > 0:
                fullkey = oldkeys + "][" + keystr
            else:
                fullkey = "[" + keystr

            if d._comments.get(key,None) is not None:
                commentstr = ' # ' + d.comment(key)

            if isinstance(value, dict):
                if "_isstring" in dir(value):
                    if value._isstring():
                        if value._orders.get(0,None) is not None:
                            order = '%05d ' % value._order(0)
                        oldvals.append(order + fullkey + "] = " + KV.entrytostring( value ) + commentstr )
                    else:
                        KV._kvdict_to_entries(value, fullkey, oldvals)
                else:
                    print "Error: Entry is not a KVDICT:", keystr,value
            elif isinstance(value, list):
                print 'Lists not handled', key, value
            else:
                if d._orders.get(key,None) is not None:
                    order = '%05d ' % d._order(key)
                oldvals.append(order + fullkey + "] = " + KV.entrytostring( value ) + commentstr )
                    
        return oldvals

    def clearkv(self):
        self.kvdict = self.nested_dict()
        self.kvdict._legacymapping = { 'system':'SYSTEM_DICTIONARY',
                                       'ipc_defaults':'IPC_DICTIONARY',
                                       'model':'MODEL_DICTIONARY',
                                       'ambient_compensator':'AMBIENT_COMPENSATOR_DICTIONARY'}
        self._comments = []
    

    @staticmethod
    def getkvtext(kvdict, searchstring=None):
        entries = KV.kvdict_to_entries(kvdict)
        if searchstring is not None:
            entries = [entry for entry in entries if searchstring.upper() in entry.upper()]
        return '\n'.join(entries)

    def grep(self, searchstring, kvdict=None):
        if kvdict is None:
            kvdict = self.kvdict
        return Printable(self.getkvtext(kvdict=kvdict, searchstring=searchstring ) )

    def savekvfile(self, filename, kvdict=None):
        if kvdict is None:
            kvdict = self.kvdict
        with open(filename, 'w') as myfile:
            myfile.write(self.getkvtext(kvdict) + '\n')

    def _dataarraytostring(self, dataarray):
        if len(dataarray) > 0:
            return ''.join(map(chr,
                               OrderedDict(sorted(dataarray.items(), key=lambda e: int(e[0]))).values())).split('\x00', 1)[0]
        else:
            return None

    def getkvdict(self):
        return self.kvdict

    def _coerce_to_numeric(self, valuestr):
        if type(valuestr) is type('hello'):
            try:
                if '.' not in valuestr:
                    value = int(valuestr)
                else:
                    raise ValueError
            except ValueError:
                try:
                    value = float(valuestr)
                except ValueError:
                    # recognize special values for nan
                    if valuestr.lower() == "float('nan')" or valuestr.lower() == 'nan' or valuestr.lower() == 'na':
                        value = float('nan')
                    elif valuestr == 'None':
                        value = None
                    else:
                        value = valuestr
        else:
            value = valuestr
        return value
    
    def _to_dict_entry(self,string):
        return  self._coerce_to_numeric(string)
    
    def readkvfile(self, filename=None, data=None):
        
        if data is None and filename is not None:
            with open(filename, 'r') as myfile:
                data = myfile.readlines()
        

        for entry in data:
            split = entry.split('#')
            entry = split[0]
            if len(split) > 1:
                comment = split[1].strip()
            else:
                comment = None
            if len(entry) == 0:
                if comment is not None and comment not in self._comments:
                    self._comments.append(comment)
                continue
            keys = entry.split('] ')[0].replace("'", "").replace('[', ' ')
            keys = re.sub(r'[^a-zA-Z0-9_ ]+', '', keys.strip()).split(' ')
            if len(keys) == 0:
                print 'Entry with no keys found', entry
                continue
            value = entry.split('=')[1].strip().strip("'")
            value = self._to_dict_entry(value)
            tmp = self.kvdict
            for key in keys[:-1]:
                tmp = tmp[self._coerce_to_numeric(key)]
            try:
                tmp[self._coerce_to_numeric(keys[-1])] = value
            except ValueError as e:
                print 'Skipping '+ entry,
                print 'ValueError: ' + str(e)

            if comment is not None:
                tmp.comment(self._coerce_to_numeric(keys[-1]), comment)

    def clearcomments(self):
        self._comments=[]
        self.kvdict.clearcomments()



#
#if __name__ == "__main__":
#    alldata = pd.DataFrame()
#
#    os.chdir('/home/mark/')
#
#    directory = os.getcwd()
#
#
#    for filename in os.listdir(directory):
#        if filename.endswith(".kv") or filename.endswith(".KV"):
#            print filename
#            fullfilename = os.path.join(directory, filename)
#            kv = KV()
#            kv.readkvfile(fullfilename)
#     #       serialnum = re.search('_(CRT.+?)_', filename).group(1)
#
#     #       lock_enh_dict = { 'serialnum': serialnum }
#     #       lock_enh_dict.update( kv.getkvdict()['LOCKING_ENHANCEMENT_DICTIONARY'] )
#
#     #       alldata = alldata.append ( pd.DataFrame( lock_enh_dict, index=[0]),ignore_index=True )
#
#            print kv.getkvtext()
#            print filename, kv.getserialnum(), kv.get_manufacturing_date()
#        else:
#            continue
#
#    alldata.to_csv( '/home/mark/data/summary.csv' )
#
