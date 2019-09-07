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
import re

class Member:

    def __init__(self):

        self.__name = 'Undefined name'
        self.__type = 'Undefined type'
        self.__number = 1
        self.__offset = 0
        self.__size = 0

    def __str__(self):

        s =  'Name  : %s\n' % (self.__name)
        s += 'Type  : %s\n' % (self.__type)
        s += 'Number: %d\n' % (self.__number)
        s += 'Offset: 0x%X\n' % (self.__offset)
        s += 'Size  : %d' % (self.__size)

        return(s)

    def name(self, n = None):

        if (n == None): return(self.__name)

        self.__name = n

    def number(self, n = None):

        if (n == None): return(self.__number)

        self.__number = n

    def offset(self, offset = None):

        if (offset == None): return(self.__offset)

        self.__offset = offset

    def size(self, size = None):

        if (size == None): return(self.__size)

        self.__size = size

    def type(self, t = None):

        if (t == None): return(self.__type)

        self.__type = t

class Structure:

    def __init__(self):

        self.__name = ''
        self.__size = 0
        self.__members = []

    def __iter__(self): return(iter(self.__members))

    def __repr__(self):

        MEMBER_FORMAT = 'Name: %-*s Type: %-*s Number: %04d Offset: 0x%04X Size: %04d\n'
        
        s =  'Name: %s\n' % (self.__name,)
        s += 'Size: %d\n\n' % (self.__size,)
        s += 'Members:\n\n'

        name_width = 0
        type_width = 0
        
        for m in self.__members:

            if (len(m.name()) > name_width): name_width = len(m.name())
            if (len(m.type()) > type_width): type_width = len(m.type())

        for m in self.__members:

            s += MEMBER_FORMAT % (name_width,
                                  m.name(),
                                  type_width,
                                  m.type(),
                                  m.number(),
                                  m.offset(),
                                  m.size())
        return(s[:-1])

    def member(self, name):

        '''
Test for membership.
        '''

        for m in self.__members:

            if (m.name() == name): return(m)

        return(None)

    def name(self, n = None):

        if (n == None): return(self.__name)

        self.__name = n

    def addMember(self, member): self.__members.append(member)

    def size(self, s = None):

        if (s == None): return(self.__size)

        self.__size = s

class Collection:

    def __init__(self):

        self.__collection = []

    def __iter__(self): return(iter(self.__collection))

    def addStructure(self, m):

        self.__collection.append(m)

    def structure(self, name):

        '''
Test for membership. Return the reference or None.
        '''

        for m in self.__collection:

            if (m.name() == name): return(m)

        return(None)

class KeilCollection(Collection):

    def __init__(self, header_files, list_file):

        Collection.__init__(self)

        for header_file in header_files: self.__readHeaderFile(header_file)

        self.__readListFile(list_file)
    #
    # Read a file such as "Dictionary.H"
    #
    def __readHeaderFile(self, filename):

        file = open(filename)

        text = file.read()

        file.close()

        #26 January 2010, Christian Gingras
        #the line "type, name =  tuple(subitem.split())" below
        #is creating an exception
        #
        #This function is called as part of the source code processing
        #which is performed after each compilation of the 8051 Keil compiler
        #The Python script "PostBuild.py"
        #is called by the GUI "uVision 2"
        #after finishing to compile and link all the files in the project
        #
        #The problem is caused by some recent edition of the file "Dictionary.h"
        #
        #Found the problem : I replaced the C++ comment style "//"
        #by the older style "/*", to check if Python would parse the file differently
        #It appears that when parsing the C source code inside a structure,
        #only the C++ style of comment is recognized
        #I replaced the comment back to "//" and the Python parser pass without creating any exception
        #
        #print('structure.py is reading:<%s>' %(filename))

        struct_expression = re.compile(r"""
                      typedef\s+struct\s+
                      (?P<tag>\S*?)         # Group the tag.
                      \s*                   # Any whitespace.
                      \{(?P<contents>.*?)\} # Group the contents.
                      \s+(?P<name>\S*?)\s*; # Group the name.
                      """, re.DOTALL | re.VERBOSE)

        comment_expression = re.compile(r'//.*?(\n|$)')

        for item in struct_expression.finditer(text):

            #print('---> structure.py loop #1A:<%s>' %(item))
            # Remove comments.
            contents_text = comment_expression.sub('\n',
                                                   item.group('contents'))

            #print('---> structure.py loop #1B:<%s>' %(contents_text))

            structure = Structure()
            structure.name(item.group('name'))

            #print('---> structure.py loop #1C:<%s>' %(item))

            # Use slicing to omit the last item from the split results.
            for subitem in contents_text.split(';')[:-1]:

                #print('---> structure.py loop #2A:<%s>' %(subitem))

                # Remove 'const' string.
                subitem = subitem.replace('const', '')

                #print('---> structure.py loop #2B:<%s>' %(subitem))

                type, name =  tuple(subitem.split())

                # If an array may need to do more extraction.
                if (name.find('[') != -1):

                    # Looks like an array.
                    name = name.replace('[', ' ')
                    name = name.replace(']', '')
                    name = name.strip()

                    name, count_string = name.split()

                    if (count_string.isdigit() == True):

                        number = int(count_string)

                    else:

                        # The count string is likely a symbolic constant.
                        # Resolve later.
                        number = count_string

                else:

                    # Not an array.
                    number = 1

                # The offset is not yet known.
                member = Member()
                member.name(name)
                member.type(type)
                member.number(number)
                structure.addMember(member)

            self.addStructure(structure)

    #
    # Read a file such as "Dictionary.LST"
    #
    def __readListFile(self, filename):

        '''
Update the list of structures with size and offset information found in the
given listing file.
        '''

        file = open(filename)

        DUMMY = Structure()
        DUMMY.name('Dummy')

        structure = None

        for line in file:

            if (line.find('* TAG *') != -1):

                structure = DUMMY
                continue

            if (line.find('TYPEDEF') != -1):

                pieces = line.replace('.', ' ').split()

                name = pieces[0]
                size = int(pieces[5])

                structure = self.structure(name)

                # A match wasn't found. Set the current structure to a dummy
                # in case members of the found structure match.

                if (structure == None): structure = DUMMY

                structure.size(size)

            if (line.find('MEMBER') != -1):

                pieces =  line.replace('.', ' ').split()

                name = pieces[0]
                offset = int(pieces[4].replace('H', ''), 16)
                size = int(pieces[5])

                member = structure.member(name)

                if (member != None):

                    member.offset(offset)
                    member.size(size)

        file.close()

