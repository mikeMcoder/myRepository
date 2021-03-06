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

import exceptions
import os
import sys
import re
import shelve
import types
import time

import Memory
import Structure
import System

if (os.name != 'posix'):
    pathdelimiter = '\\'
else:
    pathdelimiter = '/'


BASE_RAM_ADDRESS = 0xD70
RAM_SIZE    = 656

BASE_FLASH_ADDRESS = 0x400
FLASH_SIZE = 1536
FLASH_PAGE_SIZE = 512
# address 0400
FLASH_START_PAGE = 2  

DEBUG_DICT = False
def DebugOut(s):
    if DEBUG_DICT:
        print s

class Dictionary(Memory.Object):

    '''
Dictionary class.
    '''

    def __exportString__(self, root = ''):
        DebugOut('Dictionary.__exportString__(%s)' % (root))
        
        s = ''

        keys = self.__dictionary.keys()
        keys.sort()

        for key in keys:

            value = self.__dictionary[key]


            if (type(key) == types.StringType):
                
                # If the key is a string then the quotes must be added.
                current = "['%s']" % (key)

            else:

                current = "[%s]" % (key)

            if (isinstance(value, Dictionary) == True):

                s += value.__exportString__(root + current)

            else:

                if (isinstance(value, Memory.Character) == True):

                    s += "%s%s = '%s'\n" % (root, current, str(value))

                else:
                    
                    s += '%s%s = %s\n' % (root, current, str(value))

        return(s)

    def __init__(self):
        DebugOut('Dictionary.__init__')
        
        Memory.Object.__init__(self)

        self.__dictionary = {}
        self.__format_width = 0

    def __getitem__(self, index):
        DebugOut('Dictionary.__getitem__(%s)' % (index))
        
        item = self.__dictionary[index]

        if (isinstance(item, Dictionary) == True):

            return(item)
        
        else:
            
            return(item.value())

    def __repr__(self):
        DebugOut('Dictionary.__repr__()')

        DICTIONARY_STRING = '<DICTIONARY>'
        DICTIONARY_STRING_LENGTH = len(DICTIONARY_STRING)

        s = 'Description: ' + self.description() + '\n\n'

        keys = self.__dictionary.keys()

        keys.sort()

        for name in keys:

            value = self.__dictionary[name]

            s += '%-*s: ' % (self.__format_width, name)

            if (isinstance(value, Dictionary) == True):

                #s += DICTIONARY_STRING + '\n'
                s += '<%s>\n' % (value.description())
                
            else:

                s += str(value) + '\n'

        return(s[:-1])

    def __setitem__(self, index, value):
        DebugOut('Dictionary.__setitem__(%s, %s)' % (index, value))

        item = self.__dictionary[index]

        if (isinstance(item, Dictionary) == True):

            raise 'Values that are themselves dictionaries cannot be assigned.'
        
        else:
            
            item.value(value)

    def address(self, a = None):
        DebugOut('Dictionary.address(%s)' % (a))

        current_address = Memory.Object.address(self)

        if (a == None): return(current_address)

        shift = a - current_address

        for i in self.__dictionary.values(): 
            i.address(i.address() + shift)

        Memory.Object.address(self, a)

    def addEntry(self, key, value):
        DebugOut('Dictionary.addEntry(%s, value)' % (key))

        self.__dictionary[key] = value

        format_width = len(str(key))

        if (format_width > self.__format_width):

            self.__format_width = format_width

    def keys(self):
        DebugOut('Dictionary.keys()')
        return(self.__dictionary.keys())

    def memory(self, m = None):
        DebugOut('Dictionary.memory()')
        '''
Set or retrieve the memory object.
        '''

        if (m == None): 
            return(Memory.Object.memory(self))

        # Recursively set the memory object for each memory.
        for item in self.__dictionary.values(): 
            item.memory(m)
        
        Memory.Object.memory(self, m)

    def restore(self, source):
        DebugOut('Dictionary.restore(source)')
        
        '''
Returns a list of lines that could not be resolved. Source is either the
filename as a string or a file object from which the data will be read.
        '''

        f = None

        if (type(source) == types.StringType):

            f = open(source)

        else:

            f = source

        error_lines = []

        for line in f:

            try: exec('self' + line)

            except:
                print 'Ignored', line
                error_lines.append(line)

        if (type(source) == types.StringType): f.close()
        if error_lines == []:
            print 'KV file read, no errors'

        return(error_lines)

    def save(self, target):
        DebugOut('Dictionary.save(target)')

        '''
Save this dictionary to file. Target can be either the filename as a string
or a file object. If the target is specified as a string the contents of the
file will be overwritten.
        '''

        if (type(target) == types.StringType):

            target = open(target, 'w')
            target.write(self.__exportString__())
            target.close()
            return

        target.write(self.__exportString__())

class DictionaryManager:

    SHELF_FILENAME = 'Dictionary.shelf'
    ROOT_DICTIONARY_KEY = 'root_dictionary'

    def __init__(self, kvdict=None):
        DebugOut('DictionaryManager.__init__')
        self.kvdict = kvdict
        self.__root_dictionary = self.kvdict
        pass

    def shelf(self, shelf_path):
        DebugOut('DictionaryManager.shelf(%s)' % (shelf_path))
        # Determine the path of this module and use it to read the shelf.
        self.__shelf_path = shelf_path + pathdelimiter + self.SHELF_FILENAME

        DebugOut('self.__shelf_path = %s' % (self.__shelf_path))
        # Create default dictionary.
        self.__root_dictionary = Dictionary()

        if (os.path.exists(self.__shelf_path) == False):
            return False
 
        if self.kvdict is not None:
            self.__root_dictionary = self.kvdict
        else:
            self.__root_dictionary = \
                shelve.open(self.__shelf_path,
                            'r')[DictionaryManager.ROOT_DICTIONARY_KEY]
        
        '''self.__memory = Memory.Memory(BASE_RAM_ADDRESS,
                                      '\x00' * RAM_SIZE)'''

        self.__memory = Memory.Memory(BASE_FLASH_ADDRESS,
                                      '\x00' * FLASH_SIZE)

        self.__root_dictionary.memory(self.__memory)
        return True

    def keys(self):
        DebugOut('DictionaryManager.keys()')
        'Return all keys in the root dictionary'
        return self.__root_dictionary.keys()

    def rootDictionary(self):
        DebugOut('DictionaryManager.rootDictionary()')
        'Return the root dictionary'
        return self.__root_dictionary

    def dictionary(self, name):
        DebugOut('DictionaryManager.dictionary(%s)' % (name))
        '''
The name refers to the firmware variable name of dictionary of interest.
        '''

        return(self.__root_dictionary[name])

    def restore(self, source = None):
        DebugOut('DictionaryManager.restore(source)')
        
        '''
Restore dictionaries to values from eeprom/ram or file. File is either a file object
or a file path name.
        '''    
        if (source == None):
            
            '''ram_data = System.Ram().read(BASE_RAM_ADDRESS, RAM_SIZE)
        
            self.__memory.write(BASE_RAM_ADDRESS, ram_data)'''
            #time.sleep(1)
            flash_data = System.Flash().read(BASE_FLASH_ADDRESS, FLASH_SIZE)
            #time.sleep(1)
            self.__memory.write(BASE_FLASH_ADDRESS, flash_data)            
            #time.sleep(1)
            return

        return(self.__root_dictionary.restore(source))

    def save(self, target = None):
        DebugOut('DictionaryManager.save(target)')
        '''
Save to eeprom/ram or to a file. The target can be None (Save to flash), a file
path as a string, or a file object.
        '''

        if (target == None):            
            '''System.Ram().write(BASE_RAM_ADDRESS,
                        self.__memory.read(BASE_RAM_ADDRESS, RAM_SIZE))'''
            flash = System.Flash()
            flash.erasePage(FLASH_START_PAGE)
            flash.erasePage(FLASH_START_PAGE + 1)
            flash.erasePage(FLASH_START_PAGE + 2)
            flash.write(BASE_FLASH_ADDRESS, self.__memory.read(BASE_FLASH_ADDRESS, FLASH_SIZE))
            return

        self.__root_dictionary.save(target)

class DictionaryBuilder:

    if (os.name != 'posix'):
        HEADER_FILES = ('Dictionary.h', 'Type.h')
        LIST_FILE = 'Output\\Dictionary.lst'
    else:
        HEADER_FILES = ('Dictionary.h', 'Type.h')
        LIST_FILE = 'Output\Dictionary.lst'

    def __init__(self, firmware_path, name, base_address = BASE_FLASH_ADDRESS):
        DebugOut('DictionaryBuilder.__init__(%s, %s, %s)' % (firmware_path, name, base_address))

        if (name == 'Sundial4S'):           # NANO
            return
        file = open('Dictionary.h')
        text = file.read()
        file.close()

        '''original code for RAM dictioanry access'''
        '''extern_expression = re.compile(r"""
                      extern                # Look for 'extern'.
                      \s+                   # One or more whitespace.
                      (?P<type>\S+?)        # Group the type.
                      \s+                   # One or more whitespace.
                      xdata                 # Look for 'xdata'.
                      \s+                   # One or more whitespace.
                      (?P<name>\S+?)        # Group the name.
                      \s*                   # Zero or more whitespace.
                      ;                     # Find the semicolon.
                                        """, re.DOTALL | re.VERBOSE)'''

        extern_expression = re.compile(r"""
                      extern                # Look for 'extern'.
                      \s+                   # One or more whitespace.
                      (?P<type>\S+?)        # Group the type.
                      \s+                   # One or more whitespace.
                      code                  # Look for 'code'.
                      \s+                   # One or more whitespace.
                      (?P<name>\S+?)        # Group the name.
                      \s*                   # Zero or more whitespace.
                      ;                     # Find the semicolon.
                                        """, re.DOTALL | re.VERBOSE)

        # Build a dictionary that relates variable names to types.
        name_type_table = {}

        for item in extern_expression.finditer(text):

            name_type_table[item.group('name')] = item.group('type')

            # Build a dictionary that relates variable names to addresses.
            name_address_table = {}
    
        MP1_FILE = '..' + os.sep + '..' + os.sep + '..' + os.sep + 'Firmware' + os.sep + 'src' + os.sep + 'uITLA' + os.sep + 'Output' + os.sep + 'Sundial3D.map'
        file = open(MP1_FILE)

        file_iterator = iter(file)

        # Iterate until you find the beginning of the dictionary module
        # definitions.
        for line in file_iterator:

            pieces = line.split()
        
            if (len(pieces) != 5): continue

            if ((pieces[1] == 'MODULE') and (pieces[4] == 'DICTIONARY')): break

        # Iterate until your reach the end of the dictionary module
        # definitions.
        for line in file_iterator:

            pieces = line.split()

            # Skip lines that do not have the correct format.
            if (len(pieces) != 5): continue

            if ((pieces[1] == 'MODULE') and (pieces[4] == 'DICTIONARY')): continue

            # Stop iterating if we find the end of the dictionary module.
            if pieces[1] != 'PUBLIC':
               break

            # Extract the variable name and address information.
            name = pieces[4]
            address = int(pieces[0].replace('H', ''), 16) - 0x01000000

            name_address_table[name] = address

            DebugOut('DictionaryBuilder.__init__: name = %s, address = %s' % (name, address))
    
        file.close()

        # Build the dictionaries.
        header_files = []

        for filename in self.HEADER_FILES:

            header_files.append(firmware_path + pathdelimiter + filename)

        list_file = firmware_path + pathdelimiter + self.LIST_FILE
        
        collection = Structure.KeilCollection(header_files, list_file)

        self.__root_dictionary = Dictionary()
        self.__root_dictionary.description('Root Dictionary')

        for name in name_type_table:

            d = self.__buildDictionary(name_type_table[name], collection)
            d.address(name_address_table[name])
            self.__root_dictionary.addEntry(name, d)

        '''memory = Memory.Memory(BASE_RAM_ADDRESS, '\x00' * RAM_SIZE)'''
        memory = Memory.Memory(BASE_FLASH_ADDRESS, '\x00' * FLASH_SIZE)
        self.__root_dictionary.memory(memory)

    def __repr__(self):
        DebugOut('DictionaryBuilder.__repr__')
        return(repr(self.__root_dictionary))
    
    def __buildDictionary(self, name, collection):
        DebugOut('DictionaryBuilder.__buildDictionary(%s, collection)' % (name))
        
        structure = collection.structure(name)
    
        if (structure == None): return(None)
    
        dictionary = Dictionary()
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
        DebugOut('DictionaryBuilder.__buildArrayDictionary(member)')

        '''
Build a dictionary that represents an array. The address will be the default
of zero and can be set appropriately by the client.
        '''
    
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

    def dictionary(self, name):
        DebugOut('DictionaryBuilder.dictionary(%s)' % (name))
        return(self.__root_dictionary[name])

    def save(self, shelf_name):
        DebugOut('DictionaryBuilder.save(%s)' % (shelf_name))
        s = shelve.open(shelf_name)
        s[DictionaryManager.ROOT_DICTIONARY_KEY] = self.__root_dictionary
        s.close()
