'''
NeoPhotonics CONFIDENTIAL
Copyright 2008 NeoPhotonics Corporation All Rights Reserved.

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
'''

DEBUG_VAR = 0
def DebugOut(s):
    if DEBUG_VAR:
        print s

class Variable:
    def __init__(self):
        DebugOut('Variable.__init__')
        
        self.__dictionary = {}
        self.__types = {'char'              : 1,
                        'signed char'       : 1,
                        'unsigned char'     : 1,
                        'int'               : 2,
                        'signed int'        : 2,
                        'unsigned int'      : 2,
                        'enum'              : 2,
                        'short'             : 2,
                        'signed short'      : 2,
                        'unsigned short'    : 2,
                        'long'              : 4,
                        'signed long'       : 4,
                        'unsigned long'     : 4,
                        'float'             : 4,
                        'double'            : 8,
                        'Character'         : 1,
                        'S8'                : 1,
                        'S16'               : 2,
                        'S32'               : 4,
                        'U8'                : 1,
                        'U16'               : 2,
                        'U32'               : 4,
                        'F32'               : 4,
                        'F64'               : 8,
                        'String'            : 32,
                        'Boolean'           : 1,
                        'Error'             : 1,
                        'Range'             : 8,                 
                        }

    def dictionary(self, filename = None):
        DebugOut('Variable.dictionary(%s)' % (filename))
        
        if filename == None:
            return self.__dictionary
        
        main_file = file(filename, 'r')
        lines = main_file.read()
        for line in lines.split('\n'):
            line = line.strip()
            fields = line.split()
            if len(fields) != 5:
                continue
            key, token, kind, vartype,  name = fields
            if '?' in token:
                continue
            if token == 'MODULE':
                module = name
                DebugOut( 'Found module ' + str(module))
##                try:
##                    module_file = file('%s.c' % module, 'r')
##                except:
##                    module_file = None
##                    continue
                self.__dictionary[module] = {}
                continue
            if '?' in name:
                continue

            if kind == 'XDATA':
                DebugOut( '.map ==>' + str(line))
                address = '0x' + key[4:-1]
                DebugOut( '%s.%s %s' % (module, name, address))
                self.__dictionary[module][name] = address
                #self.variableType(module_file, module, name)
        main_file.close()

    def variableType(self, file_object, module, name):
        DebugOut('Variable.variableType(file_object, module,%s)' % (name))
        
        return
        file_object.seek(0)
        lines = file_object.read().split('\n')
        print 'variable [%s]' % name
        for line in lines:
            if line.find(name) != -1:
                print 'find %d %s' % (line.find(name), line)
                
                type = line.strip().split(name)[0].strip()
                print type
                type = type.split()
                print type
                if len(type) != 1:
                    type = type[-1].split('(')[-1].strip()
                else:
                    type = type[0]
                print type
                if type in self.__types:
                    print '.c ==>', line
                    #print type, name.split(';')[0]
                    self.__dictionary[module][name] = type
                    return

                
