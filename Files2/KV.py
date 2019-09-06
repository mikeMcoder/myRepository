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


class KV():
    """
       Converts kv files to and from nested dictionaries
    """

    def __init__(self):
        self.nested_dict = lambda: defaultdict(self.nested_dict)
        self.kvdict = self.nested_dict()

    def kvdict_to_entries(self, d=None, oldkeys="", oldvals=None):
        if d is None:
            d = self.kvdict
        if oldvals is None:
            oldvals = []
        for key, value in d.iteritems():
            if len(oldkeys) > 0:
                fullkey = oldkeys + "']['" + key
            else:
                fullkey = "['" + key
            if isinstance(value, dict):
                self.kvdict_to_entries(value, fullkey, oldvals)
            else:
                if type(d[key]) is not type('hello'):
                    if math.isnan(d[key]):
                        valstr = "float('nan')"
                    else:
                        valstr = '%+g' % d[key]
                        if type(d[key]) is float and '.' not in valstr:
                            valstr += '.0'
                else:
                    valstr = "'" + d[key] + "'"
                oldvals.append(fullkey + "'] = " + valstr)
        return oldvals

    def getkvtext(self, kvdict=None):
        if kvdict is None:
            kvdict = self.kvdict
        return '\n'.join(self.kvdict_to_entries(kvdict))

    def savekvfile(self, filename, kvdict=None):
        with open(filename, 'w') as myfile:
            myfile.write(self.getkvtext(kvdict) + '\n')

    def _dataarraytostring(self, dataarray):
        if len(dataarray) > 0:
            return ''.join(map(chr,
                               OrderedDict(sorted(dataarray.items(), key=lambda e: int(e[0]))).values())).split('\x00', 1)[0]
        else:
            return None

    def getserialnum(self, kvdict=None):
        if kvdict is None:
            kvdict = self.kvdict
        return self._dataarraytostring(kvdict['SYSTEM_DICTIONARY']['serial_number'])

    def get_manufacturing_date(self, kvdict=None):
        if kvdict is None:
            kvdict = self.kvdict
        return self._dataarraytostring(kvdict['SYSTEM_DICTIONARY']['manufacturing_date'])

    def getkvdict(self):
        return self.kvdict

    def readkvfile(self, filename):
        with open(filename, 'r') as myfile:
            data = myfile.readlines()

        for entry in data:
            keys = entry.split('] ')[0].replace("'", "").replace('[', ' ')
            keys = re.sub(r'[^a-zA-Z0-9_ ]+', '', keys.strip()).split(' ')
            if len(keys) == 0:
                print 'Entry with no keys found', entry
                continue
            value = entry.split('=')[1].strip().strip("'")
            try:
                if '.' not in value:
                    value = int(value)
                else:
                    raise ValueError
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    # recognize special values for nan
                    if value.lower() == "float('nan')" or value.lower() == 'nan' or value.lower() == 'na':
                        value = float('nan')

            tmp = self.kvdict
            for key in keys[:-1]:
                tmp = tmp[key]
            tmp[keys[-1]] = value

        return self.kvdict


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
