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

    $Source: /data/development/cvs/Lux/Python/TTM/Utility.py,v $
    $Revision: 1.2 $
    $Date: 2009/03/13 22:40:50 $
    $Name: HEAD $
    
'''
import ConfigParser
import exceptions
import sys
import time
import types

import PyTTXTalk

ACRONYMNS = ['ADC', 'DAC', 'DC', 'MUX', 'PCB', 'RTD', 'TEC']

ERROR_CODES = {+000: 'Connected.',
               -100: 'General error.',
               -101: 'Timeout.',
               -102: 'Unable to load library.',
               -103: 'Incompatible library.',
               -104: 'Unable to open.',
               -105: 'Unable to close.',
               -106: 'Invalid handle.',
               -107: 'I2C unavailable.',
               -108: 'I2C not enabled.',
               -109: 'I2C read error.',
               -110: 'I2C write error.',
               -111: 'Incompatible device. Check firmware version.',
               -200: 'Write failure.',
               -201: 'Write starve.',
               -202: 'Write timeout.',
               -203: 'Write not ready.',
               -204: 'Write exception.',
               -205: 'Write stale handle.',
               -300: 'Read failure.',
               -301: 'Read timeout.',
               -302: 'Read final timeout.',
               -303: 'Read starve.',
               -304: 'Read disconnect.',
               -305: 'Read stale handle.',
               -400: 'Unable to find device.',
               -401: 'Already connected.'}

__debug = False

def buildFunctionName(constant_name):

    pieces = constant_name.split('_')

    function_name = pieces.pop(0).lower()

    for piece in pieces:

        try:

            ACRONYMNS.index(piece)

            function_name += piece.upper()

        except exceptions.ValueError:
        
            function_name += piece.title()

    return(function_name)

def newOperation(module, operation):

    PyTTXTalk.newOperation(module, operation)


def debug(flag = None):
    global __debug
    
    if flag == None:
        return __debug
    else:
        if flag:
            __debug = True
        else:
            __debug = False

def sendPacket(timeout):

    error_code = PyTTXTalk.send(timeout)

    if (error_code != 0):

        raise exceptions.Exception('%d: %s' % (error_code,
                                               ERROR_CODES[error_code]))

    if (PyTTXTalk.getError() != 0):
        
        raise exceptions.Exception((PyTTXTalk.getError(),
                                    PyTTXTalk.popU8()))

def help(object): print(object.doc)

def query(question, default_answer, autoresponse = False):

    sys.stdout.write('%s (%s):' % (question, default_answer))

    if (autoresponse == True):

        sys.stdout.write(default_answer + '\n')
        return(default_answer)

    answer = sys.stdin.readline()[:-1]

    if (answer == ''): return(default_answer)

    return(answer)

def parseEnum(file_name, type_name):
    '''Parse the C enum entries and return a dictionary of {number : name}
    Expect C code format as follows:
    typedef enum
    {
        A,
        B = 3,
        C
    }
    MyEnum;

    returns {0 : 'A', 3 : 'B', 4 : 'C'}
    '''
    f = file(file_name, 'r')
    text = f.readlines()
    f.close()

    def_found = False
    open_found = False
    close_found = False
    type_found = False
    enum = {}
    line_number = 1
    for line in text:
        line_number += 1
        line = line.strip()
        if len(line) == 0:
            continue
        elif line.find('//') == 0:
            # comment
            continue
        elif line.find('typedef enum') == 0:
            def_found = True
            enum = {}
            index = 0
            continue
        elif line.find('{') == 0:
            open_found = True
            type_found = False
            continue
        elif line.find('}') == 0:
            close_found = True
            def_found = False
            if line.find(type_name) > 0:
                type_found = True
                break
            continue
        elif line.find(type_name) == 0:
            type_found = True
            break

        if def_found and open_found:
            if line.find('=') != -1:
                name, value = line.split('=')
                name = name.strip()
                if value.find('0x') != 0:
                    radix = 16
                else:
                    radix = 10
                index = int(value.split(',')[0], radix)
            else:
                name = line.split(',')[0].strip()
            enum[index] = name
            index += 1
            
    if not type_found:
        enum = {}

    return enum

def saveConfiguration(file_name, section, dictionary):
    'Saves a dictionary into a configuration file'
    cp = ConfigParser.ConfigParser()
    cp.read(file_name)
    f = file(file_name, 'w')
    if not cp.has_section(section):
        cp.add_section(section)
    for key in dictionary:
        cp.set(section, str(key), dictionary[key])
    cp.write(f)
    f.close()

def restoreConfiguration(file_name, section):
    'Returns a dictionary'
    cp = ConfigParser.ConfigParser()
    cp.read(file_name)
    dictionary = {}
    if cp.has_section(section):
        for key in cp.options(section):
            dictionary[key] = cp.get(section, key)
        
    return dictionary

class DictionaryFlattener:
    def __init__(self):
        pass
        
    def header(self, d, header, parent = ''):
        ' Make header into a one dimensional list, only need to do this once '
        keys = d.keys()
        keys.sort()
        
        if keys.count('index') == 1:
            keys.remove('index')
            keys.insert(0, 'index')
            
        for i in keys:
            object = d[i]
            if type(object) == types.InstanceType:
                # Flatten further
                self.header(object, header, parent + i + '.')
            else:
                header.append(parent + i)
                
    #parameter "data" passed by reference already contain one float, the time stamp
    #the function "data" explore the dictionary tree
    #and insert any "leaf" found
    def data(self, dictParam, data, parent = ''):
        ' Make data into a one dimensional list, allow multiple invokations '
        keys = dictParam.keys()
        keys.sort()
        
        if keys.count('index') == 1:
            keys.remove('index')
            keys.insert(0, 'index')
        if keys.count('time') == 1:
            keys.remove('time')
            
        for i in keys:
            #print 'flat key:',i
            object = dictParam[i]
            if type(object) == types.InstanceType:
                # Flatten further
                #print '$$$ Recursive call START to explore the tree branch:', parent + i
                self.data(object, data, parent + i + '.')
                #print '$$$ Recursive call END to explore the tree branch:', parent + i
            else:
                data.append(object)

def main(): pass
        
if __name__ == '__main__': main()
