#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 10:05:55 2019

***Do Not Share this file with customers***

This contains the code to generate bridge files from the unit.  

Instead, if customers need to calibrate units, supply customer with firmware binary, python without this file, 
and bridge file matching the firmware binary version.

@author: mark
"""

import os
import sys

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

import re
import distutils
import copy
import math
    
import pandas as pd


class DoNotShare(object):
    
    print "Including 'DoNotShare.py' (do not share this file with customer)"


    def structureIndexList(self, dfm, typesandlengths):
        structListName=[]
        structlistLength = []
        structlistIndex = []        # PLEASE re-write this!
#        structList = []
        for index,row in dfm.iterrows():
            if row['type'] == 'typedef':
                start = index
            if row['type'] not in typesandlengths.keys() and row['type']!='typedef':
                if row['type'] not in structListName:
#                if row['type'] not in structList:
#                    structList.append([row['type'],index-start-1,index])
                    structListName.append(row['type'])
                    structlistLength.append(index-start-1)
                    structlistIndex.append(index)
        return zip(structListName,structlistIndex,structlistLength)

    def _flattendicts(self, df, typelengths, varsep='__', base_struct_name=None, progress=False):
        """
        
        creates ordered list of cal entries from nested structs

        :param df: raw data frame from parsed cal text
        :param typelengths:  dict of known types and their lengths
        :param varsep:  text used to separate variable names (Default value = '__')
        :param base_struct_name:  name of the base struct (Default value = 'calibrationDictionary')

        """        
        if base_struct_name is None:
            base_struct_name = self._kvDictionaryname
            
        structIndxList = self.structureIndexList(df,typelengths)  # Get list of structure names, indexes and lengths.

        knowntypes = set(typelengths.keys())

        df['ndx'] = df.index.map('{:04d}'.format) # kludge to keep the order
        df['knowntype'] = df['type'].isin(knowntypes)

        self._listoftables=dict()
        for i in range(len(structIndxList)):    
            entry = structIndxList[i]
            self._listoftables[entry[0]] = df[entry[1]-entry[2]:entry[1]]
                
        listoftables = self._listoftables.copy()
        
        
        for key, value in listoftables.iteritems():
            listoftables[key] = listoftables[key].reset_index(drop=True)
            listoftables[key]['name'] = key
        
        keys = listoftables.keys()
        
        donekeys=set([])
        
        tablesremaining = len(keys) - len(donekeys)
        
        i = 0
        
        while tablesremaining:
            for key1 in keys:
                if listoftables[key1]['knowntype'].all():
                    donekeys.add(key1)
                else:
                    for key2 in keys:
                        if key1 == key2:
                            continue
                        if (listoftables[key1]['type'] == key2).any():
                            #print key1 + ' replacing ' + key2
                            listoftables[key1] = listoftables[key1].set_index('type').join( listoftables[key2].set_index('name'), how='outer', rsuffix='_key2',sort=False  )
                            listoftables[key1].loc[listoftables[key1]['type'].isnull(),'type'] = listoftables[key1].index[listoftables[key1]['type'].isnull()]
                            listoftables[key1].loc[listoftables[key1]['ndx_key2'].isnull() ,'ndx_key2'] = '0000'
                            listoftables[key1]['ndx'] = listoftables[key1]['ndx'].astype(str) + listoftables[key1]['ndx_key2']
                            listoftables[key1].loc[~listoftables[key1]['variable_key2'].isnull() ,'variable'] += varsep + listoftables[key1][~listoftables[key1]['variable_key2'].isnull()]['variable_key2'] 
#                            listoftables[key1].loc[~listoftables[key1]['comment_key2'].isnull() ,'comment'] += ' ; ' + listoftables[key1][~listoftables[key1]['comment_key2'].isnull()]['comment_key2'] 
                            listoftables[key1].loc[~listoftables[key1]['Units_key2'].isnull() ,'Units'] += ' ' + listoftables[key1][~listoftables[key1]['Units_key2'].isnull()]['Units_key2']
#                            print list(listoftables[key1].filter(regex = '_key2'))
                            listoftables[key1].drop(list(listoftables[key1].filter(regex = '_key2')), axis = 1, inplace = True)
                            listoftables[key1]['knowntype'] = listoftables[key1]['type'].isin(knowntypes)
                            
                            i += 1

                            if progress and not i%5:
                                sys.stdout.write('.')
                                sys.stdout.flush()

            lasttablesremaining = tablesremaining
            tablesremaining = len(keys) - len(donekeys)
            if tablesremaining == lasttablesremaining:
                raise Exception('Cal decoder is stuck.  Circular reference?')
                return None

        if base_struct_name in listoftables:
    
            flattened = listoftables[base_struct_name].sort_values(['ndx']).reset_index(drop=True)
            flattened.comment=flattened.comment.str.strip(' ')
            flattened.Units=flattened.Units.str.strip(' ')
            
            flattened['cal'] = base_struct_name

        else:
            flattened = pd.DataFrame()

        return flattened

    def _parsecaltable(self, content, structname=r'CalibDataRecABC', remote=False, nanoDevice=True, progress=False):
        """

        :param content: 
        :param structname:  (Default value = r'CalibDataRecABC')
        :param remote:  (Default value = False)

        """

        #structname=r'CalibDataRecMaster'
        #calcppfilename = '..' + os.sep + 'firmware' + os.sep + 'CFP2ACOFW' + os.sep + 'src' + os.sep + 'CalibrationData.hpp'
        #with open(calcppfilename) as myfile:
        #    content = myfile.read()
        
        
        dummychar = '`' # char we guarantee not to be used in struct
#        if nanoDevice == False:
#            beginstring = r'typedef struct PACKED '
#            text = re.search( beginstring + r'(.*?)'+ structname + ';', content, re.DOTALL).group()
#        else:
        beginstring = r'#define __DICTIONARY_H__'
        try:
            toss,text = content.split(beginstring)
        except ValueError:
            text = content
    
        # extract the table
        #content = self._comment_remover(content)
        text = text.replace(beginstring, "", 1)
        text = text.replace('__attribute__((packed))','')
        text2 = re.search( beginstring + r'.*\s\n.*?' + structname + ';', text, re.DOTALL) # fixme: kludge to get second stuct
        if text2 is not None:
            text=text2.group()
        textlines = text.split('\n')
        text2 = [line for line in textlines if not line.lstrip().startswith('//')]      # Remove lines with just comment.
        textlines = text2
        textlines = [ line.split('//')[0] + (line.split('//')+ [''])[1].replace(' ',dummychar).replace(';', ' ') for line in textlines ]
        text = '\n'.join(textlines)
        text = re.sub(r'{|}', ' ', text).replace(';', '')
        text=re.sub(' +',' ', text)
        textlines = text.split('\n')
        textlines = [line.strip().replace('\n', '')
                     for line in textlines if 
                     line.strip() is not '']
#        if nanoDevice == False:
#            textlines=textlines[1:-1] # strip first and last
#        textlines = [line.replace('&' + classname + '::', '')
#                     for line in textlines if re.match('.*?' + classname + '::.*?', line)]

        # read into a dataframe
        texttoread = StringIO('\n'.join(textlines))
        df = pd.read_csv(texttoread, sep=" ", header=None, dtype=str, names=['type','variable','Units','comment'] )
                        
        df.comment=df.comment.str.strip(dummychar)
        df.Units=df.Units.str.strip(dummychar)

        df.comment=df.comment.str.replace(dummychar,' ')
        df.Units=df.Units.str.replace(dummychar,' ')

        df.comment=df.comment.str.strip(' ')
        df.Units=df.Units.str.strip(' ')


        typelengths = {'uint8_t': 1,
                       'int8_t': 1,
                       'uint16_t': 2,
                       'int16_t': 2,
                       'uint32_t': 4,
                       'int32_t': 4,
                       'float': 4,
                       'uint64_t': 8,
                       'int64_t': 8,
                       'char': 1,      
                       'bool': 1,
                       'ufixed7pt': 4,
                       'ufixed9pt': 4,
                       'sfixed7pt': 4,
                       'sfixed9pt': 4,
                       'float16_t': 2,
                       }
        self._tempdf = df

#        if nanoDevice == True:
        # Remove a couple lines from the header file.
        df = df[ ~ df.type.str.contains('#define')]
        df = df[ ~ df.type.str.contains('#endif')]
        df = df[ ~ df.type.str.startswith("`")]
    
        df = df[ ~ df.type.str.contains('extern')]

        df1 = self._flattendicts(df, typelengths, base_struct_name = structname, progress=progress)
        df1['ndx'] = df1.index

#            df2 = self._flattendicts(df, typelengths, base_struct_name = 'rawcaldict', progress=progress)
#            df2['ndx'] = df2.index
#            df = pd.concat([df1,df2]).reset_index()
        df = df1

#        print structname, df.shape[0] 
#        print len(content),content

            
#        else:
#            df['cal'] = structname
#            df['ndx'] = df.index


        if df.shape[0] == 0:
            return df
            
        else:
            df['cal'] = structname
            df['ndx'] = df.index

        if df.shape[0] == 0:
            return df

        df = df[ ~ df.variable.isnull() ] # remove empty lines
        df.loc[:, 'typelength'] = df['type'].map(typelengths)
        
        df.loc[:, 'variable'] = df['variable'].astype(str)

        df.loc[:, 'variable'] = df['variable'].str.replace('DICTIONARY_F','DICTIONARY')

        if distutils.version.LooseVersion(pd.__version__) < distutils.version.LooseVersion('0.18.0'):
            dim1 = df.variable.str.extract('(.*)\s*\[(.*)\]')#, expand = True)
            dim2 = dim1[0].astype(str).str.extract('(.*)\s*\[(.*)\]')#, expand = True)
        else:
            dim1 = df.variable.str.extract('(.*)\s*\[(.*)\]',expand=False)#, expand = True)
            dim2 = dim1[0].astype(str).str.extract('(.*)\s*\[(.*)\]',expand=False)#, expand = True)
            
        dim1.columns = ['variable', 'dim2']
        dim2.columns = ['variable', 'dim1']
        dim2['dim2'] = dim1['dim2']

        dim2.loc[dim2['variable'].isnull(),'variable'] = dim1['variable']
        dim2.loc[dim2['variable'].isnull(),'variable'] = df['variable']
        
        df.loc[:,'dim1'] = dim2['dim1']
        df.loc[:,'dim2'] = dim2['dim2']
        df.loc[:,'variable'] = dim2['variable']

        df.loc[:,'ndx'] = df.index
        
        df.loc[df['dim1'].isnull(),'dim1'] = 1
        df.loc[df['dim2'].isnull(),'dim2'] = 1

        df.loc[:,'dim1'] = df['dim1'].astype(int)
        df.loc[:,'dim2'] = df['dim2'].astype(int)
        
        # todo: add array support

        df.loc[:,'cal'] = structname

        
        df.loc[:,'arraylist'] = map(lambda dim1, dim2: [ '__'+str(x).rjust(len(str(dim1)),'0')+'__'+str(y).rjust(len(str(dim2)),'0') for x in range(dim1) for y in range(dim2)], df['dim1'], df['dim2'])

        df = pd.DataFrame(
            [(key + (item,)) 
             for key, val in df.set_index([ item for item in df.columns if item is not 'arraylist' ])['arraylist'].iteritems()
             for item in map(list, val) or [[]]], columns = df.columns )

        df.loc[:,'arraylist'] = map(lambda arraylist: ''.join(arraylist), df['arraylist'])
    
        df.loc[(df.dim1 == 1) & (df.dim2 == 1),'arraylist']= ''
        
        df.loc[(df.dim1 == 1) & (df.dim2 != 1),'arraylist'] = df.loc[(df.dim1 == 1) & (df.dim2 != 1),'arraylist'].apply( (lambda x: x[3:]) )
        
        df.loc[:,'variable'] = df['variable'] + df['arraylist']
            
        # df['totalbytes'] = df['dim1'] * df['dim2'] * df['typelength']  # if not using arrays
        df['totalbytes'] = df['typelength']
#        df['offset'] = np.cumsum(np.insert(df['totalbytes'][:-1].values,0,0))
        df['offset'] = df.groupby('cal')['totalbytes'].transform(pd.Series.cumsum)
        
#        df['offset'] = df['offset'].shift(1, fill_value=0)
        df.loc[:,'offset'] = df['offset'].shift(1)  # pandas < 0.24.0 shift does not support fill_value
        df['offset'].iat[0] = 0
        
        self._tempdf = df
        
        df.loc[:,'totalbytes'] = df['totalbytes'].astype(int)
        df.loc[:,'offset'] = df['offset'].astype(int)
        
        df['remote'] = remote
        
        df = df[ df.variable.str.contains("dummy") == False] # remove the dummy variables
                
        return df
    
    
    def _manglename(self,name,targetdict): # fixme: kludge to deal with inconsistent zero padding
        if name not in targetdict: # kludge to deal with inconsistent zero padding
            if re.sub( r'__(\d)', r'__0\1',copy.copy(name)) in targetdict:
                return re.sub( r'__(\d)', r'__0\1',copy.copy(name))
            matches = re.finditer('__\d', name)
            nummatches = 0
            for match in matches:
                nummatches += 1
            for i in range(0,nummatches):
                if re.sub( r'__(\d)', r'__0\1',copy.copy(name),i):
                    return re.sub( r'__(\d)', r'__0\1',copy.copy(name),i)
        return name
    
        
    def setctrlfunctionsfromunit(self):
        ctrlheader = self._getheaderfromunit(headernum=1)
        scalingheader = self._getheaderfromunit(headernum=2)
        if ctrlheader is not None:
            self.ctrl = self.CTRLCONTAINER()
            self._addcmdfunctions(cmdcontent=ctrlheader,scalingcontent=scalingheader)  # add to self.ctrl
            self._unlockheader(1)
            self._unlockheader(2)
        else:
            print self.hilite("No data: Unable to set ctrl from unit", False, True)
            
    def _addcmdfunctions(self, cppfilename=None, cmdcontent=None, scalingcontent=None):
        """

        :param cppfilename: 

        """
        
        if cppfilename is not None:    
            with open(cppfilename) as myfile:
                cmdcontent = myfile.read()

        tables = self._findcmdtables(cmdcontent)
        parsedtables = []
        for tablename in tables:
            parsedtable = self._parsecmdtable(cmdcontent, tablename)
            parsedtables.append(parsedtable)

        # merge the tables
        self._functionstable = pd.concat(parsedtables, sort=True)
        self._functionstable = self._functionstable.fillna('')
        self._functionstable[['enum', 'index']] = self._functionstable[['enum', 'index']].astype('int')

        # sanity check
        getandsets = self._functionstable[self._functionstable['set'] != '']
        # getsonly = functionstable[ functionstable['set'] == '' ]
        mismatches = getandsets[getandsets['set'] != getandsets['set']]
        if mismatches.shape[0] > 0:
            print self.hilite("Warning: Function names for Gets and Sets do not match", False, True)
            print mismatches

        scalingtable = None

        if scalingcontent is not None:
            scalingtable = pd.read_csv(StringIO(scalingcontent))
        else:
            if os.path.isfile(self._scalingtablefilename):
                scalingtable = pd.read_csv(self._scalingtablefilename)

        if scalingtable is not None:
            scalingtable['matchcol'] = scalingtable['get'].str.replace(r'-', '_').str.replace(r'_', '_')
            self._functionstable['matchcol'] = self._functionstable['get'].str.replace(r'-', '_')
            scalingtable.drop(['get'],axis=1, inplace=True)
            self._functionstable = pd.merge(self._functionstable, scalingtable, how='outer', on = 'matchcol')
            #scalingtable.drop(['matchcol'],axis=1, inplace=True)
            self._functionstable.fillna('', inplace=True)
            
        self._cmdcounter = 0

        self._functionstable.apply(self._addgetsetfunction, axis=1)

        if self._cmdcounter > 0:
            print ': '+str(self._cmdcounter)+' functions'
        
        unmatched = self._functionstable[self._functionstable['Signals'] == '']
        unmatched = unmatched['table'] + '.' + unmatched['get']
        if unmatched.shape[0] > 0:
            print
            print "Warning: " + self._scalingtablefilename + " contains no match for these ctrl functions:"
            print
            print ', '.join(unmatched)

    def _findcmdtables(self, content):
        return re.findall(r'able_t (.*)\[\]', content)
    
    
    def _parsecmdtable(self, content, tablename):
        """

        :param content: 
        :param tablename: 

        """

        # extract the table
        text = re.search(tablename + r'\[\].*?\s+};', content, re.DOTALL).group()
        text = self._comment_remover(text)
        text = re.sub(r'{|}', ' ', text).replace(' ', '')
        classname = re.search(r'&.*?::', text).group().replace(':', '').replace('&', '')
        textlines = text.split('\n')
        textlines = [line.replace('&' + classname + '::', '')
                     for line in textlines if re.match('.*?' + classname + '::.*?', line)]

        # read into a dataframe
        texttoread = StringIO('\n'.join(textlines))
        df = pd.read_csv(texttoread, sep=",", header=None, dtype=str)

        # retrieve the enum
        text = re.search(r'MZ_CMD.*?\s+};', content, re.DOTALL).group()
        text = re.search(r'{.*?\s+};', text, re.DOTALL).group()
        text = self._comment_remover(text)
        text = re.sub(r'{|}|\n|;', ' ', text).replace(' ', '').strip(',')
        textlines = text.split(',')

        # todo: remove hardcoding---the enum name structure (MZ_ at start and _bit
        # at end) is hardcoded here, so that it can match the enum to the class
        enumname = [line for line in textlines if re.search(
                    r'MZ.*_.*?',
                    line,
                    re.DOTALL).group()[3:-1] + '_Table' == tablename][0]
        enumnum = [i for i, x in enumerate(textlines) if x == enumname][0]

        # add column names
        colnames = []
        for col in df.columns[:-1]:
            prefix = re.search(r'.*?_', df[col][0]).group()
            colnames.append(prefix.strip('_'))
            df[col] = df[col].str.replace(prefix, '')

        colnames.append('comment')
        df.rename(columns=dict(zip(df.columns, colnames)), inplace=True)

        df = df.fillna('').replace(self._UNSUPPORTEDFUNCTIONSTRING, '')

        df['table'] = tablename[:-6]  # strip the '_Table'
        df['class'] = classname
        df['enum'] = enumnum
        # df['enumname'] = enumname
        df['index'] = df.index

        df['type'] = float

        if 'GPIO' in classname:  # hard code in python for now
            df['type'] = bool
        else:
            df['type'] = float

        return df

    def _comment_remover(self, text):
        def replacer(match):
            """

            :param match: 

            """
            s = match.group(0)
            if s.startswith('/'):
                return " "  # note: a space and not an empty string
            else:
                return s
        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )
        return re.sub(pattern, replacer, text)
    

    def _addgetsetfunction(self, functioninfo):
        if functioninfo['index'] == '':
            return
        if math.isnan(functioninfo['index']):
            return
        if functioninfo['table'] not in self.ctrl.__dict__:
            setattr(self.ctrl, functioninfo['table'], self.CTRLCLASS())  # create table objects if needed
            if self._cmdcounter > 0:
                print ': '+str(self._cmdcounter)+' functions'
            print 'Creating ' + 'mz.ctrl.'+functioninfo['table'],
            self._cmdcounter = 0
        function = None
        if functioninfo['set'] == functioninfo['get']:  # set function exists
            def getsetvalue(setval=None,rawOpt=False):
                """

                :param setval:  (Default value = None)
                :param rawOpt:  (Default value = False)

                """
                if type(rawOpt) is not bool:
                    raise Exception('rawOpt must be boolean')
                    return None
                if setval is not None:
                    if type(setval) is not getsetvalue.info.type:
                        if not ( getsetvalue.info.type is bool and ( setval == 1 or setval == 0 )):
                            raise Exception('setval must be '+ str(getsetvalue.info.type) + '(' + str(type(setval)) + 'given)' )
                            return None
                    if getsetvalue.info.type == float:
                        if rawOpt:
                            return self.writeOfloat(reg=0xF1, index=getsetvalue.info.enum, floatval=setval, index2=getsetvalue.info.ndx).strip('\x00')
                        return self.writefloat(reg=0xF1, index=getsetvalue.info.enum, floatval=setval, index2=getsetvalue.info.ndx).strip('\x00')
                    elif getsetvalue.info.type == bool:
                        return self.reg(reg=0xF1, index=getsetvalue.info.enum, val=setval, index2=getsetvalue.info.ndx,write=True).strip('\x00')
                    else:
                        print 'Unknown type' + getsetvalue.info.type
                        return None
                else:
                    if getsetvalue.info.type == float:
                        if rawOpt:
                            return self._floatwithunits(self.decodefloatarray(self.reg(regnum=0xF1, option=True,index=getsetvalue.info.enum, index2=getsetvalue.info.ndx))[0], units=getsetvalue.info.RawUnits )
                        return self._floatwithunits(self.decodefloatarray(self.reg(regnum=0xF1, index=getsetvalue.info.enum, index2=getsetvalue.info.ndx))[0], units=getsetvalue.info.Units )
                    elif getsetvalue.info.type == bool:
                        return ord(self.reg(regnum=0xF1, index=getsetvalue.info.enum, index2=getsetvalue.info.ndx))
                    else:
                        print 'Unknown type' + getsetvalue.info.type
                        return None
            getsetvalue.info = functioninfo.copy()
            getsetvalue.info.enum = int(getsetvalue.info.enum)
            getsetvalue.info.ndx = int(getsetvalue.info['index'])
            if 'Units' not in getsetvalue.info.index:
                getsetvalue.info.Units = None
            getsetvalue.__doc__ = "Get/set function for " + functioninfo['class'] + "::" + functioninfo['get']
            for col in self._iocolumnstoadd:
                if col in functioninfo.index:
                    if functioninfo[col] != '':
                        getsetvalue.__doc__ =  getsetvalue.__doc__ + '\n' + col + ' : ' + str(functioninfo[col])
            getsetvalue.writable = True
            function = getsetvalue
        else:
            def getvalue(rawOpt=False):
                """

                :param rawOpt:  (Default value = False)

                """
                if type(rawOpt) is not bool:
                    raise Exception('rawOpt must be boolean')
                    return None
                if getvalue.info.type == float:
                    if rawOpt:
                        return self._floatwithunits(self.decodefloatarray(self.reg(regnum=0xF1, index=getvalue.info.enum, index2=getvalue.info.ndx,option=True))[0], units=getvalue.info.RawUnits )
                    return self._floatwithunits(self.decodefloatarray(self.reg(regnum=0xF1, index=getvalue.info.enum, index2=getvalue.info.ndx))[0], units=getvalue.info.Units  )                
                elif getvalue.info.type == bool:
                    return ord(self.reg(regnum=0xF1, index=getvalue.info.enum, index2=getvalue.info.ndx))
                else:
                    print 'Unknown type' + getvalue.info.type
                    return None
            getvalue.info = functioninfo.copy()
            getvalue.info.enum = int(getvalue.info.enum)
            getvalue.info.ndx = int(getvalue.info['index'])
            if 'Units' not in getvalue.info.index:
                getvalue.info.Units = None

            getvalue.__doc__ = "Get function for " + functioninfo['class'] + "::" + functioninfo['get'] + '\n' + \
                               functioninfo['comment']
            getvalue.writable = False
            function = getvalue
        function.__name__ = functioninfo['get']
        function.returntype = functioninfo.type
        function.enum = functioninfo.enum
        function.index = functioninfo.index
        setattr(getattr(self.ctrl, functioninfo['table']), function.__name__, function)  # add get function
        self._cmdcounter += 1
