'''
NeoPhotonics CONFIDENTIAL
Copyright 2010 NeoPhotonics Corporation All Rights Reserved.

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

#import PyTTXTalk3
import time
#import iPort
import struct
import sys
import os
if (os.name != 'posix'):
    import win32ui
import Memory
#import Logger

#print 'starting code in file PyTTXTalk2.py'
#print '+++++ -> Python interpreter is reading <PyTTXTalk2.py>'

__laserSelect = 0
__debugRS232 = 0
__debugCOMM = False
#attribute name starting with "__" and not ending with "__" are made semi-private with class/module name appended
__debug2 = False
#__debug2 = True
__debug_write = False
#__debug_write = True
__debug_no_print_cur_operation = 0
__count_print_statements = 0
#__use_rs232_instead_of_i2c = False
#__use_iPort = False
__obj_com_port = None
#__obj_iport = None
#-----
__selected_rs232_com_port = 0
__selected_rs232_baud = 9600
#-----
__last_selected_module = 0
__last_selected_method = 0
__num_items_send = 0
#-----
__str_data_python_send_to_firmware = ''
__last_str_received = ''
__last_ptr_read_recv = 0
__ptr_read_end_to_beginning = 0
#-----
__str_last_line = ''
#-----
__Log_Line_Number = 0
__Total_frames_received = 0    
__Total_star_lines_received = 0    
__Log_Expected_Line_Number = 0
__LogCurrentFrame = ''
__LogTotalFramesSaved = 0    
__LogTotalBytesCapture = 0
__LogExpectedFrameSize = 0
__LogFrames = []
__LogTimestamp = []
__Logfilehandle = None    
    # @@@@@ Global_function_definition @@@@@
def newOperation(module, operation):
    #attribute name inside a class starting with "__" and not ending with "__" are made semi-private with class name prepended by the Python interpreter
    global __last_selected_module
    global __last_selected_method
    global __num_items_send
    global __debug_no_print_cur_operation
    global __str_data_python_send_to_firmware
    #global __debug2

    __str_data_python_send_to_firmware  = ''
    __last_selected_module              = module
    __last_selected_method              = operation
    __num_items_send                    = 0
    if __last_selected_module == 0:
        if __last_selected_method == 2:
            __debug_no_print_cur_operation = 1
            return
    __debug_no_print_cur_operation = 0
    #if __debug2 == True:
    #    print 'new operation for RS232,module:', module, ',operation:', operation

# @@@@@ Global_function_definition @@@@@
def send(timeout):
#   global __use_iPort
#   global __obj_iport
    global __last_selected_module
    global __last_selected_method
    #global __num_items_send
    global __str_data_python_send_to_firmware
    global __last_str_received
    global __last_ptr_read_recv
    global __ptr_read_end_to_beginning
    global __debug2
    global __Total_frames_received
    global __Total_star_lines_received
    global __laserSelect


    __last_ptr_read_recv        = 0
    __ptr_read_end_to_beginning = 0
    __last_str_received         = ''
    if(__laserSelect== 2):
        laserBit = 128
    else:
        laserBit = 0
    
    #generate PicassoTalk header
    str_to_send = '~' + \
            str_bin8_to_hex(len(__str_data_python_send_to_firmware)) + \
            str_bin8_to_hex(__last_selected_module + laserBit) + \
            str_bin8_to_hex(__last_selected_method)

    #Append the data to the PicassoTalk message
    for ival_8 in __str_data_python_send_to_firmware:
        str_to_send = str_to_send + str_bin8_to_hex(ord(ival_8))
    #
    #do not append '\n', this is done inside 'write' of the current 'PyTTXTalk.py' module
    #


    if __debugCOMM == True:
        print 'send:', str_to_send
    
    write_txt(str_to_send)
    time.sleep(0.01 * timeout)
    if __debug2 == True:
        print '#sending packet:', str_to_send
    __Total_frames_received = 0
    __Total_star_lines_received = 0
    __LogCurrentFrame = ''
    picasso_talk_get_answer_rs232(str_to_send)
    
    #if(__Total_frames_received != 0):

    #    print 'lines starting by <*>', __Total_star_lines_received
    #    print 'lines starting by <&> (frames)', __Total_frames_received
    #    print 'average lines per frame:', (float(__Total_star_lines_received) / float(__Total_frames_received))
    return 0

# @@@@@ Global_function_definition @@@@@
def picasso_talk_increment_num_items():
    global __num_items_send

    __num_items_send = __num_items_send + 1

def debugRS232(debug):
    global __debugRS232
    if debug != None:
        __debugRS232 = debug
    return __debugRS232

#XREF:def send(timeout):
# @@@@@ Global_function_definition @@@@@
def picasso_talk_get_answer_rs232(string_repeat):
    global __str_last_line
    global __last_str_received
    global __debugRS232

    if __debugRS232:
        print 'WR-> ', string_repeat
    num_seconds_total           = 0.2       # never gets reached unless disconnected
    num_seconds_rs232_quiet     = 0.5      #  interbyte timeout
    __str_last_line             = ''
    start_time                  = time.time()
    got_bytes                   = 0         # used in interbyte timeout
    byte_count                  = 1
    while((start_time + num_seconds_total) > time.time()):
        string = __obj_com_port.read(byte_count)
        strSize = len(string)
        if (strSize > 0):
            got_bytes = 1
            idle_time = time.time()
            rs232_accumulate_byte_separate_strings(string)
            if string[strSize-1] == chr(0x0A):      # reply terminator
                break
        else:
            if(got_bytes):          # got 1st bytes
                if(idle_time + num_seconds_rs232_quiet) < time.time():
                    print 'Receive partial data from RS-232...'
                    break
    if __debugRS232:
        print '  <- ',
        for i in range(len(__last_str_received)):
            print str_bin8_to_hex(ord(__last_str_received[i])),
        print ''

    if __debugCOMM == True:
        print 'picasso_talk_get_answer_rs232:', string
        
# @@@@@ Global_function_definition @@@@@
def DataSize():
    global __ptr_read_end_to_beginning

    return __ptr_read_end_to_beginning

# @@@@@ Global_function_definition @@@@@
def pushS8(ival_8):
    global __str_data_python_send_to_firmware
    #global __debug_no_print_cur_operation
    global __debug2

    #adjust the "item counter", this is one of the 5 bytes in the PicassoTalk header
    picasso_talk_increment_num_items()
    __str_data_python_send_to_firmware = __str_data_python_send_to_firmware + chr(ival_8)
    #if __debug2 == True:
    #    print 'pushS8 for RS232:%02X' % (ival_8)

# @@@@@ Global_function_definition @@@@@
def pushU8(ival_8):
    global __str_data_python_send_to_firmware
    global __debug_no_print_cur_operation
    global __debug2

    #adjust the "item counter", this is one of the 5 bytes in the PicassoTalk header
    picasso_talk_increment_num_items()
    __str_data_python_send_to_firmware = __str_data_python_send_to_firmware + chr(ival_8)
    #if __debug2 == True:
    #    if __debug_no_print_cur_operation == 0:
    #        print 'pushU8 for RS232:%02X' % (ival_8)

# @@@@@ Global_function_definition @@@@@
def pushRS232_no_print(ival_8):
    global __str_data_python_send_to_firmware

    __str_data_python_send_to_firmware = __str_data_python_send_to_firmware + chr(ival_8)

# @@@@@ Global_function_definition @@@@@
def pushS16(ival_16):
    #global __debug_no_print_cur_operation

    #adjust the "item counter", this is one of the 5 bytes in the PicassoTalk header
    picasso_talk_increment_num_items()
    pushRS232_no_print((ival_16 >> 8) & 255)
    pushRS232_no_print( ival_16       & 255)
    #if __debug_no_print_cur_operation == 0:
    #    print 'pushS16 for RS232:%04X' % (ival_16)

# @@@@@ Global_function_definition @@@@@
def pushU16(ival_16):
    #global __debug_no_print_cur_operation

    #adjust the "item counter", this is one of the 5 bytes in the PicassoTalk header
    picasso_talk_increment_num_items()
    pushRS232_no_print((ival_16 >> 8) & 255)
    pushRS232_no_print( ival_16       & 255)
    #if __debug_no_print_cur_operation == 0:
    #    print 'pushU16 for RS232:%04X' % (ival_16)

# @@@@@ Global_function_definition @@@@@
def pushS32(ival_32):
    #adjust the "item counter", this is one of the 5 bytes in the PicassoTalk header
    picasso_talk_increment_num_items()
    pushRS232_no_print((ival_32 >> 24) & 255)
    pushRS232_no_print((ival_32 >> 16) & 255)
    pushRS232_no_print((ival_32 >>  8) & 255)
    pushRS232_no_print( ival_32        & 255)
    #if __debug_no_print_cur_operation == 0:
    #    print 'pushS32 for RS232:%08X' % (ival_32)

# @@@@@ Global_function_definition @@@@@
def pushU32(ival_32):
    #adjust the "item counter", this is one of the 5 bytes in the PicassoTalk header
    picasso_talk_increment_num_items()
    pushRS232_no_print((ival_32 >> 24) & 255)
    pushRS232_no_print((ival_32 >> 16) & 255)
    pushRS232_no_print((ival_32 >>  8) & 255)
    pushRS232_no_print( ival_32        & 255)
    #if __debug_no_print_cur_operation == 0:
    #    print 'pushU32 for RS232:%08X' % (ival_32)

# @@@@@ Global_function_definition @@@@@
def pushF32(fval_32):
    #adjust the "item counter", this is one of the 5 bytes in the PicassoTalk header
    picasso_talk_increment_num_items()
    for ch_float in struct.pack('>f', fval_32):
        pushRS232_no_print(ord(ch_float))
    #if __debug_no_print_cur_operation == 0:
    #    print 'pushF32 for RS232:', fval_32

# @@@@@ Global_function_definition @@@@@
def pushString(str_param):
    global __debug2
    #global __debug_no_print_cur_operation

    #adjust the "item counter", this is one of the 5 bytes in the PicassoTalk header
    picasso_talk_increment_num_items()
    for ival_8 in str_param:
        pushRS232_no_print( ord(ival_8) & 255)
    #if __debug2 == True:
    #    print 'pushF32 for RS232:', fval_32

# @@@@@ Global_function_definition @@@@@
def popS8():
    global __last_str_received
    global __last_ptr_read_recv
    global __ptr_read_end_to_beginning
    global __debug2

    if __ptr_read_end_to_beginning > 0:
        ival_8_answer = ord(__last_str_received[__ptr_read_end_to_beginning])
        __ptr_read_end_to_beginning = __ptr_read_end_to_beginning - 1
        if ival_8_answer < 128:
            #if __debug2 == True:
            #    print 'popS8 for RS232,answer is:+ %02X' % (ival_8_answer)
            return ival_8_answer
        else:
            #if __debug2 == True:
            #    print 'popS8 for RS232,answer is:- %02X' % (ival_8_answer - 256)
            return ival_8_answer - 256
    else:
        #print 'popS8 for RS232,no more data, return 0x00 for now... should raise exception'
        print 'popS8, no data'
        raise PyTTXTalkException('No answer, expected 8 bit value')

# @@@@@ Global_function_definition @@@@@
def popU8():
    global __last_str_received
    global __last_ptr_read_recv
    global __ptr_read_end_to_beginning
    global __debug_no_print_cur_operation
    global __debug2

    if __ptr_read_end_to_beginning > 0:
        ival_8_answer = ord(__last_str_received[__ptr_read_end_to_beginning])
        __ptr_read_end_to_beginning = __ptr_read_end_to_beginning - 1
        #if __debug2 == True:
        #    if __debug_no_print_cur_operation == 0:
        #        print 'popU8 for RS232,answer is:%02X' % (ival_8_answer)
        return ival_8_answer
    else:
        #print 'popS8 for RS232,no more data, return 0x00 for now... should raise exception'
        #TypeError: exceptions must be strings, classes, or instances, not NoneType
        raise PyTTXTalkException('byte(s) missing from laser answer, caused either by an incorrect protocol implementation in Python/firmware or the answer comes too late, such as reading CDR using Juno PCB with incorrect CDR hardware')
        #raise serialutil.SerialException, "could not open port <%s>, error desc.: %s" % (self.portstr, msg)
        #raise LUXI2CException('Error establishing communication with TTM I2C. Low level exception message: %s' % str(ex))
        #raise ('Error establishing communication with TTM I2C. Low level exception message: %s' % str(ex))
        #   strMsg = 'Maximum number of iterations (%d) is exceeded.  failure' % nMaxIterations
        #   raise Exception( strMsg )

        return 0
    #if __last_ptr_read_recv + 5 < len(__last_str_received):
    #    ival_8_answer = ord(__last_str_received[__last_ptr_read_recv + 5])
    #    if __debug2 == True:
    #        if __debug_no_print_cur_operation == 0:
    #            print 'popU8 for RS232,answer is:%02X' % (ival_8_answer)
    #    __last_ptr_read_recv = __last_ptr_read_recv + 1
    #    return ival_8_answer
    #else:
    #    #print 'popU8 for RS232,no more data, return 0x00 for now... should raise exception'
    #    raise
    #    return 0

# @@@@@ Global_function_definition @@@@@
def popS16():
    global __last_str_received
    global __ptr_read_end_to_beginning
    global __last_ptr_read_recv
    global __debug2

    if __ptr_read_end_to_beginning > 1:
        #print 'popS16 for RS232,ptr_read:%d, size:%d' % (__ptr_read_end_to_beginning, len(__last_str_received))
        ival_8_a = ord(__last_str_received[__ptr_read_end_to_beginning - 1])
        ival_8_b = ord(__last_str_received[__ptr_read_end_to_beginning - 0])
        __ptr_read_end_to_beginning = __ptr_read_end_to_beginning - 2
        ival_16_answer = (ival_8_a * 256) + ival_8_b
        if ival_16_answer < 32768:
            #if __debug2 == True:
            #    print 'popS16 for RS232,answer is:+ %04X' % (ival_16_answer)
            return ival_16_answer
        else:
            #if __debug2 == True:
            #    print 'popS16 for RS232,answer is:- %04X' % (ival_16_answer - 65536)
            return ival_16_answer - 65536
    else:
        #print 'popS16 for RS232,ptr_read:%d, size:%d' % (__ptr_read_end_to_beginning, len(__last_str_received))
        #print 'popU16 for RS232,no more data,returning constant for now... should raise exception'
        print 'popS16, no data'
        raise PyTTXTalkException('No answer, expected 16 bit value')

# @@@@@ Global_function_definition @@@@@
def popU16():
    global __last_str_received
    global __ptr_read_end_to_beginning
    global __last_ptr_read_recv
    global __debug2

    if __ptr_read_end_to_beginning > 1:
        ival_8_a = ord(__last_str_received[__ptr_read_end_to_beginning - 1])
        ival_8_b = ord(__last_str_received[__ptr_read_end_to_beginning - 0])
        __ptr_read_end_to_beginning = __ptr_read_end_to_beginning - 2
        ival_16_answer = (ival_8_a * 256) + ival_8_b
        #if __debug2 == True:
        #    print 'popU16 for RS232,answer is:%04X' % (ival_16_answer)
        return ival_16_answer
    else:
        #print 'popU16 for RS232,no more data,returning constant for now... should raise exception'
        print 'popU16, no data'
        raise PyTTXTalkException('No answer, expected 16 bit value')

# @@@@@ Global_function_definition @@@@@
def popS32():
    global __ptr_read_end_to_beginning
    global __last_ptr_read_recv
    global __last_str_received

    if __ptr_read_end_to_beginning > 3:
        ival_8_a = ord(__last_str_received[__ptr_read_end_to_beginning - 3])
        ival_8_b = ord(__last_str_received[__ptr_read_end_to_beginning - 2])
        ival_8_c = ord(__last_str_received[__ptr_read_end_to_beginning - 1])
        ival_8_d = ord(__last_str_received[__ptr_read_end_to_beginning - 0])
        __ptr_read_end_to_beginning = __ptr_read_end_to_beginning - 4
        ival_32_answer = (ival_8_a * 256 * 256 * 256) + (ival_8_b * 256 * 256) + (ival_8_c * 256) + ival_8_d
        if ival_8_a >= 128:
            ival_32_answer = 0 - ival_32_answer
        #if __debug2 == True:
        #    print 'popS32 for RS232,answer is:%08X' % (ival_32_answer)
        return ival_32_answer
    else:
        #print 'popS32 for RS232 not implemented yet,returning constant for now'
        raise PyTTXTalkException('No answer, expected 32 bit value (4 bytes)')

# @@@@@ Global_function_definition @@@@@
def popU32():
    global __ptr_read_end_to_beginning
    global __last_str_received
    i =0
    while i < 50:
        if __ptr_read_end_to_beginning > 3:
            ival_8_a = ord(__last_str_received[__ptr_read_end_to_beginning - 3])
            ival_8_b = ord(__last_str_received[__ptr_read_end_to_beginning - 2])
            ival_8_c = ord(__last_str_received[__ptr_read_end_to_beginning - 1])
            ival_8_d = ord(__last_str_received[__ptr_read_end_to_beginning - 0])
            __ptr_read_end_to_beginning = __ptr_read_end_to_beginning - 4
            ival_32_answer = (ival_8_a * 256 * 256 * 256) + (ival_8_b * 256 * 256) + (ival_8_c * 256) + ival_8_d
            if __debug2 == True:
                print 'popU32 for RS232,answer is:%08X' % (ival_32_answer)
                #return ival_32_answer
            break;
        else:
        #print 'popS32 for RS232 not implemented yet,returning constant for now'
           i = i + 1
           if i >= 50:
              raise PyTTXTalkException('No answer, expected 32 bit value (4 bytes)')

    return ival_32_answer    

# @@@@@ Global_function_definition @@@@@
def popF32():
    global __last_str_received
    global __ptr_read_end_to_beginning
    global __last_ptr_read_recv
    global __debug2
    i =0
    while i < 20:
        try:
            if __ptr_read_end_to_beginning > 3:                  
                char_a = __last_str_received[__ptr_read_end_to_beginning - 3]
                char_b = __last_str_received[__ptr_read_end_to_beginning - 2]
                char_c = __last_str_received[__ptr_read_end_to_beginning - 1]
                char_d = __last_str_received[__ptr_read_end_to_beginning - 0]
                __ptr_read_end_to_beginning = __ptr_read_end_to_beginning - 4
                fval_32_answer = struct.unpack('>f', char_a + char_b + char_c + char_d)[0]
                if __debug2 == True:
                    print 'popF32 for RS232,answer is:%f,recv:%02X,%02X,%02X,%02X' % (fval_32_answer, ord(char_a), ord(char_b), ord(char_c), ord(char_d))
                return fval_32_answer
            else:
                print 'popF32, no data, resend...'
                send(1)
                i = i + 1
        except:
            i= i + 1
            print "Trying again"     
    raise PyTTXTalkException('No answer, expected 32 bit value (4 bytes)')


# @@@@@ Global_function_definition @@@@@
def popString():
    global __last_str_received
    global __ptr_read_end_to_beginning
    global __last_ptr_read_recv
    global __debug2

    #size answer for popString:15
    #ch[0]:0E       ;PicassoTalk Header 1/5 : total size
    #ch[1]:00       ;PicassoTalk Header 2/5 : Module : 0x00 = System
    #ch[2]:00       ;PicassoTalk Header 3/5 : Method : 0x00, read firmware version
    #ch[3]:00       ;PicassoTalk Header 4/5 : Error code (not used)
    #ch[4]:05       ;PicassoTalk Header 5/5 : total number of items
    #ch[5]:0A       ;Build
    #ch[6]:00       ;Patch
    #ch[7]:00       ;Minor : 0
    #ch[8]:01       ;Major : 1
    #ch[9]:4C       ;'L'
    #ch[10]:75      ;'u'
    #ch[11]:78      ;'x'
    #ch[12]:00      ;end of string
    #ch[13]:04      ;size of string
    #ch[14]:00      ;extra byte...
    str_answer = ''
    #if __debug2 == True:
    #    print '********** [start]size answer for popString:%d,index_end:%d' % (len(__last_str_received), __ptr_read_end_to_beginning)
    #    cnt = 0
    #    for ch in __last_str_received:
    #        if(ch >= 0x20) and (ch <= 0x7E):
    #            print 'start_pop_buffer[%d]:%02X,<%c>' % (cnt, ord(ch), ch)
    #        else:
    #            print 'start_pop_buffer[%d]:%02X' % (cnt, ord(ch))
    #        cnt = cnt + 1
    if __ptr_read_end_to_beginning < 1:
        return str_answer
    #while __last_ptr_read_recv+5 < len(__last_str_received):
    #    char_a = __last_str_received[__last_ptr_read_recv + 5]
    #    __last_ptr_read_recv = __last_ptr_read_recv + 1
    #    if __debug2 == True:
    #        print 'strchar[%d+5]:%02X' % (__last_ptr_read_recv, ord(char_a))
    #    if ord(char_a) == 0:
    #        break
    #    str_answer = str_answer + char_a
    num_char_string = ord(__last_str_received[__ptr_read_end_to_beginning])
    #if __debug2 == True:
    #    print 'size String:%d' % (num_char_string)
    __ptr_read_end_to_beginning = __ptr_read_end_to_beginning - num_char_string
    str_read_ptr = __ptr_read_end_to_beginning
    while num_char_string != 0:
        num_char_string = num_char_string - 1
        char_a = __last_str_received[str_read_ptr]
        str_read_ptr = str_read_ptr + 1
        #if __debug2 == True:
        #    print 'read_popstring[%d]:%02X' % (str_read_ptr, ord(char_a))
        if ord(char_a) == 0:
            break
        str_answer = str_answer + char_a
    #if __debug2 == True:
    #    print 'popString answer:', str_answer
    #    print '********** [end]size answer for popString:%d,index_end:%d' % (len(__last_str_received), __ptr_read_end_to_beginning)
    __ptr_read_end_to_beginning = __ptr_read_end_to_beginning - 1
    return str_answer

# @@@@@ Global_function_definition @@@@@
def getError():
    #print 'get error using RS232'
    return 0

# @@@@@ Global_function_definition @@@@@
def debug_rs232(flag = None):
    global __debug2

    if flag == None:
        return __debug2
    else:
        if flag:
            __debug2 = True
        else:
            __debug2 = False

# @@@@@ Global_function_definition @@@@@
def laser(flag = None):
    global __laserSelect

    if flag == None:
        return __laserSelect
    else:
        __laserSelect = flag

# @@@@@ Global_function_definition @@@@@
def save_handle(com_port_handle = None):
    global __obj_com_port
    __obj_com_port = com_port_handle

def set_rs232_com_port(com_port_number = None, rs232_baud = None, com_port_handle = None):
    global __selected_rs232_com_port
    global __selected_rs232_baud
    global __obj_com_port
#    global __obj_iport

    if com_port_number == None:
        return __selected_rs232_com_port
    else:
        __selected_rs232_com_port   = com_port_number
        __selected_rs232_baud       = rs232_baud
        __obj_com_port              = com_port_handle
 #       __obj_iport                 = iport_object
        print 'setting RS232 COM Port number to:%s and baud rate to:%d' % (str(com_port_number), rs232_baud)

#the iPort uses RS232 to communicate to a USB/I2C adapter
#the current design of the Python scripts is as follow:

# 1 - use Aardvark USB/I2C if starting with "t.connect(0)
# 2 - use "RS232" development board protocol if starting with "t.connect(1-255)
# 3 - use iPort/RS232 protocol if the file "config.ini" is found
#     in the folder where the Python have been started (where the link 'AngelicalPython.lnk' is located)
#     and the RS232 com port/baud rate match an actual iPort device

#It is probable that we will use a special paramter in "t.connect()" to select iPort

# @@@@@ Global_function_definition @@@@@
def ival_8_conv_hex(char_hex_1, char_hex_2):
    table_hex_char = { 
        '0':0,  '1':1,  '2':2,  '3':3,  '4':4,  
        '5':5,  '6':6,  '7':7,  '8':8,  '9':9,
        'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15,
        'a':10, 'b':11, 'c':12, 'd':13, 'e':14, 'f':15
    }
    if table_hex_char.has_key(char_hex_1) == 0:
        return -1
    if table_hex_char.has_key(char_hex_2) == 0:
        return -1
    ival_d7_d4 = table_hex_char[char_hex_1]
    ival_d3_d0 = table_hex_char[char_hex_2]
    return (ival_d7_d4 * 16) + ival_d3_d0

#sending string: ~010005

# answer  ~12,03,01,00,05,CD,answer_to_python<~010005>
# answer  ~13,03,01,00,05,CD,answer_to_python<~010005>
# answer  ~14,03,01,00,05,CD,answer_to_python<~010005>

#first character in answer is "~"
#then, each pair of hexadecimal number is appended to the answer until finding a non hexadecimal character

# @@@@@ Global_function_definition @@@@@
#
#The caller make sure only one complete line is present in parameter
#The parameter is a PicassoTalk hexadecimal ASCII frame
#for example, the following string:
#       "~030123\n"
#would be converted to a binary array as follow
#binary_array[0] = 0x03     : total size in byte, including header
#binary_array[1] = 0x01     : Module : select the "C or PY" file such as 0 for "System", 1 for "Sample"
#binary_array[2] = 0x23     : Method : select a functiopn inside a given module
#
#
#The present function perform the conversion to binary
#The end result is similar to the original I2C PicassoTalk frame as seen in ITLA lasers
#
def analyze_picasso_talk_rs232_answer(str_line):
    global __last_str_received
    global __debug2
    global __ptr_read_end_to_beginning

    if __debug2 == True:
        print '### answer ', str_line
    __last_str_received = ''
    __ptr_read_end_to_beginning = 0
    size_str_line = len(str_line)
    if size_str_line < 3:
        #
        #The PicassoTalk protocol require 3 byte for the header
        #Discard a line too short
        return
    if (str_line[0] != '~') and  (str_line[0] != '+'):
        if (str_line[0] == '&') or  (str_line[0] == '*'):
            Parse_Logger_Line(str_line)
            if __debug2 == True:
                #TODO:parsing the content of logger generated lines
                print 'Logger line detected'
            return
        else:
            #the first character does not conform to the RS232 PicassoTalk protocol
            #Possible reasons are: 
            #       - incorrect baud rate
            #       - flow control
            #                   - RS232 receive buffer overflow because sender is too fast
            #                   - System own transmit buffer overflow because of inacurate sampling of internal buffer space
            #       - protocol extension from sender not recognized by receiver
            if __debug2 == True:
                ascii_code = ord(str_line[0])
                if(ascii_code >= 0x20) and (ascii_code <= 0x7E):
                    print 'Error, first characeter found:%02X,<%c>' % (ascii_code, chr(ascii_code))
                else:
                    print 'Error, first characeter found:%02X' % (ascii_code)
            return
    #here, we are parsing a reply to a query ; the logger lines are parsed in a diffenrent part of the code
    if __debug2 == True:
        ascii_code = ord(str_line[0])
        #if(ascii_code >= 0x20) and (ascii_code <= 0x7E):
        #    print 'first characeter:%02X,<%c>' % (ascii_code, chr(ascii_code))
        #else:
        #    print 'first characeter:%02X' % (ascii_code)
    rd_ptr = 1
    num_char_bin = 0
    while rd_ptr+1 < size_str_line:
        hex_val = ival_8_conv_hex(str_line[rd_ptr+0], str_line[rd_ptr+1])
        if hex_val < 0:
            __ptr_read_end_to_beginning = len(__last_str_received) - 1
            return
        __last_str_received = __last_str_received + chr(hex_val)
        if __debug2 == True:
            pass
            #if(num_char_bin < 3):
            #    #Print the first 3 bytes as 'header'
            #    if(hex_val >= 0x20) and (hex_val <= 0x7E):
            #        print 'hex_val[header]:%02X,<%c>' % (hex_val, chr(hex_val))
            #    else:
            #        print 'hex_val[header]:%02X' % (hex_val)
            #else:
            #    #Print the following bytes as optional data with index starting at "0"
            #    if(hex_val >= 0x20) and (hex_val <= 0x7E):
            #        print 'hex_val[0x%02X]:%02X,<%c>' % (num_char_bin-3, hex_val, chr(hex_val))
            #    else:
            #        print 'hex_val[0x%02X]:%02X' % (num_char_bin-3, hex_val)
        num_char_bin = num_char_bin + 1
        rd_ptr = rd_ptr + 2
    __ptr_read_end_to_beginning = len(__last_str_received) - 1

# @@@@@ Global_function_definition @@@@@
#
#The parameter is a snapshot of the RS232 receive buffer
#It may contain parial line or many lines
#The main goal is to recombine the lines for processing by next layer
def rs232_accumulate_byte_separate_strings(string_param = ''):
    global __str_last_line
    global __debug2

    #print 'string to accumulate:', string_param
    num_char_recv = 0
    for ch_param in string_param:
        ival_8 = ord(ch_param)
        if ival_8 == 17:
            continue
        if ival_8 == 19:
            continue
        if ival_8 == 0x99:
            #ignore the character 0x99, code used for switching from MSA to ASCII-PicassoTalk
            continue        
        if ( (ival_8 == 10) or (ival_8 == 13)):
            if len(__str_last_line) > 0:
                if __debug2 == True:
                    print 'string received:',__str_last_line
                analyze_picasso_talk_rs232_answer(__str_last_line)
            __str_last_line = ''
        else:
            __str_last_line = __str_last_line + ch_param
            if __debug2 == True:
                #print '%02X,' % (ival_8),
                if ival_8 == 0:
                    print 'char received[%02d] is 0x00, end of string' % (num_char_recv)
                else:
                    pass
            num_char_recv = num_char_recv + 1
    #print 'end of loop, previous string received:', __str_last_line
            
# @@@@@ Global_function_definition @@@@@
def str_bin8_to_hex(picasso_param1):
    return '%02X' % (picasso_param1)

# @@@@@ Global_function_definition @@@@@

#
# @@@@@ Global_function_definition @@@@@
#XREF:<print_kv_file> in <System.py>
    #example of command which call "print_kv_file":
    #       - "t.system().print_kv_file()"
#XREF:<wr> in class <TTM> in file <TTM.py>
#example of command line:
#       - t.wr("['MODEL_DICTIONARY']['default_si_block_temperature'] = +77.890000")
def print_rs232_lines(flag_print_line_in_interactive_window = None):
    global __str_last_line

    num_seconds_rs232_quiet     = (1.00 + 0.5)
    start_time                  = time.time()
    #save_start_time            = start_time
    byte_count                  = 500
    __str_last_line             = ''
    list_str_from_RS232         = []
    while((start_time + num_seconds_rs232_quiet) > time.time()):
        string                  = __obj_com_port.read(byte_count)
        if (len(string) > 0):
            #rs232_accumulate_2_byte_separate_strings(string)
            parse_rs232_bloc_of_bytes_separate_strings(string, list_str_from_RS232, flag_print_line_in_interactive_window)
            #if received some characters from RS232,
            #then reset the timer
            #keep extending the timeout
            #until the RS232 port become silent
            start_time          = time.time()

    if len(__str_last_line) > 0:
        #analyze_picasso_talk_rs232_answer(__str_last_line)
        if(flag_print_line_in_interactive_window == None):
            #here, called by "wr" : we want to print every line on Python window
            #Otherwise, when called thru "print_kv_file", we just accumulate the string in a "list" (array of string)
            print __str_last_line

        else:
            list_str_from_RS232.append(__str_last_line)

    __str_last_line             = ''
    if(flag_print_line_in_interactive_window == None):
        #print '-->>Juno Read dictionary (internal KV File) total time (seconds):', time.time() - save_start_time
        return 'Finished_rs232_lines'
    else:
        return (list_str_from_RS232)

# @@@@@ Global_function_definition @@@@@
#XREF: function <get_kv_file_string_from_Juno> in class <System>
def read_lines_till_rs232_quiet():
    total_lines_received    = 0
    line_cnt_progress       = 0
    progress_cnt_new_line   = 0
    num_seconds_rs232_quiet = 1.00
    max_time_seconds_stop   = 20.0
    start_time              = time.time()
    save_start_time         = start_time
    byte_count              = 500
    str_answer_all_lines    = ''
    #mem_ival_answer_cbInQueCom = 0
    #print 'calling <read_lines_till_rs232_quiet>,time:', start_time
    while((start_time + num_seconds_rs232_quiet) > time.time()):
        #ival_answer_cbInQueCom  = PyTTXTalk2.rs232_get_cbInQueCom()
        #ival_answer_cbInQueCom  = rs232_get_cbInQueCom()
        #if not (mem_ival_answer_cbInQueCom == ival_answer_cbInQueCom):
        #    mem_ival_answer_cbInQueCom = ival_answer_cbInQueCom
        #    print 'RS232_in_queue:', ival_answer_cbInQueCom
        string              = __obj_com_port.read(byte_count)
        if (len(string) > 0):
            for ch_param in string:
                ival_8 = ord(ch_param)
                #eliminate the pesky XON and XOFF character
                #which could be inserted at random position in the received string
                #if we don't receive any answer for some time,
                #we may want to manually send a "XON" character to unfreeze the communication
                #XOFF : 17,0x11, ctrl-Q, DC1
                #XON  : 19,0x13, ctrl-S, DC3
                if ival_8 == 17:
                    continue
                if ival_8 == 19:
                    continue
                if ( (ival_8 == 10) or (ival_8 == 13) ):
                    total_lines_received    = total_lines_received + 1
                    line_cnt_progress       = line_cnt_progress + 1
                    if line_cnt_progress > 9:
                        line_cnt_progress   = 0
                        progress_cnt_new_line = progress_cnt_new_line + 1
                        if progress_cnt_new_line < 10:
                            print 'line[%d],' % (total_lines_received),
                        else:
                            progress_cnt_new_line = 0
                            print 'line[%d]' % (total_lines_received)
                    str_answer_all_lines    = str_answer_all_lines + '\n'
                else:
                    str_answer_all_lines    = str_answer_all_lines + ch_param

            #if received some characters from RS232,
            #then reset the timer
            #keep extending the timeout
            #until the RS232 port become silent
            start_time      = time.time()

        if((save_start_time + max_time_seconds_stop) < time.time()):
            #Juno or other device
            #connected to the RS232 serial port
            #is still sending string
            #when encountering this timeout
            break

    print 'line[%d].' % (total_lines_received)
    print '-->>Juno Read dictionary (internal KV File) total lines:', total_lines_received
    print '-->>Juno Read dictionary (internal KV File) total time (seconds):', time.time() - save_start_time
    return str_answer_all_lines

# @@@@@ Global_function_definition @@@@@
#def rs232_accumulate_2_byte_separate_strings(string_param = ''):
def parse_rs232_bloc_of_bytes_separate_strings(string_param, list_str_from_RS232, flag_print_line_in_interactive_window = None):
    global __str_last_line

    for ch_param in string_param:
        ival_8 = ord(ch_param)
        #eliminate the pesky XON and XOFF character
        #which could be inserted at random position in the received string
        #if we don't receive any answer for some time, we may want to manually send a "XON" character to unfreeze the communication
        #XOFF : 17,0x11, ctrl-Q, DC1
        #XON  : 19,0x13, ctrl-S, DC3
        if ival_8 == 17:
            continue
        if ival_8 == 19:
            continue
        if ( (ival_8 == 10)  or (ival_8 == 13) ):
            if len(__str_last_line) > 0:
                list_str_from_RS232.append(__str_last_line)
                if(flag_print_line_in_interactive_window == None):
                    #here, called by "wr" : we want to print every line on Python window
                    #Otherwise, when called thru "print_kv_file", we just accumulate the string in a "list" (array of string)
                    print __str_last_line
            #now that the line is saved, and possibly printed, erase it to get ready to accumulate the characters from the next line
            __str_last_line = ''
        else:
            #__str_last_line = __str_last_line + ch_param
            __str_last_line = __str_last_line + chr(ival_8)

# @@@@@ Global_function_definition @@@@@
def rs232_send_string_as_is(string_param = ''):
    global __obj_com_port

    #__obj_com_port.write_txt(string_param)
    #__obj_com_port.write(string_param)
    write_txt(string_param)

#PyTTXTalk.disconnect()
def disconnect():
    print 'Disconnecting RS232... Serial port actually released in the class TTM'
    
def write_txt(string_param):
    global __debug2
    global __count_print_statements

    __obj_com_port.flushInput()
    if __debug_write == True:
        #print 'write_txt:', string_param
        index = 0
        for char_in_str in string_param:
            #print 'write_txt[%02d]:%02X,<%c>' % (index, ord(char_in_str), ord(char_in_str))
            index = index + 1
            __count_print_statements = __count_print_statements + 1
            if(__count_print_statements &   0x07) == 1:
                #print 'pumping messages txt',__count_print_statements
                win32ui.PumpWaitingMessages(0, -1)
    __obj_com_port.write(string_param + '\r\n')
    #__obj_com_port.write(string_param + '\r\n\r\n\r\n')
    if "outWaiting" in dir(__obj_com_port):
        while __obj_com_port.outWaiting():
            time.sleep(0.001)
    else:
        __obj_com_port.flush()
    # added 1/18/17 transmits bytes

def write_bin(string_param):
    global __debug2
    global __count_print_statements
    
    if __debug_write == True:
        print 'write_bin', string_param
        index = 0
        for char_in_str in string_param:
            #print 'write_bin[%02d]:%02X,<%c>' % (index, ord(char_in_str), ord(char_in_str))
            index = index + 1
            __count_print_statements = __count_print_statements + 1
            if(__count_print_statements & 0x07) == 1:
                #print 'pumping messages bin', __count_print_statements
                win32ui.PumpWaitingMessages(0, -1)
    __obj_com_port.write(string_param)
    if "outWaiting" in dir(__obj_com_port):
        while __obj_com_port.outWaiting():
            time.sleep(0.001)
    else:
        __obj_com_port.flush()

def read_bin(count):
    global __debugRS232
    num_seconds_rs232_quiet     = 0.050     
    start_time                  = time.time()
    string                      = ''
    RxChars                     = ''
    while((start_time + num_seconds_rs232_quiet) > time.time()):
        RxChars = __obj_com_port.read(count)
        if(len(RxChars)):
            start_time = time.time()
            string  = string + RxChars  #pb
            if (len(string) >= count):
                break;

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#called when the test "if (str_line[0] == '&') or  (str_line[0] == '*'):"  succeed
#example of lines generated to describe a frame
#&0046000002
#*011E0000019C68C079605A7FF4A7000000007FFF0A
#*02D40AD468730000C61BDA31C61BDAA0424C5B2000
#*0300000041AF893F410928E6421CB6480000000000
#*04000000C61BDAF2C61BDAD6424C82C40000000041
#*05BAB22E0000000000000000000000004005A64C40
#*0605ADC84270000000000000000000000000000000
#*07000000000000070000
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$ Description of the Ascii logger protocol $$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#The protocol allow to send a relatively large array of binary data
#using many lines of text comprised of 7 bit ASCII characters
#There is 4 distinct fields s in each line
#       1 - first character is "&" (first) or "*" (next)
#       2 - second/third character is a line number specified as 8 bit hexadecimal value
#       3 - from 1 to "n" pair of hexadecimal character representing the original binary data found in the frame
#       4 - a line terminator : 0x0D (Carriage Return), 0x0A (Line feed) or the pair 0x0D,0x0A together, represented as "\r\n" in C language
#The line number allow to detect missing or repeated lines or other corruption in the transmission of a logger frame
#The first line of a frane starts with ampersand "&" and have a line number of "00"
#The following lines of the frame start by star "*" and have a line number ranging from "01" to "FF" nad exaactly "n" pair of hexadecimal values
#The last line of the frame may have from 1 to n pair of hexadecimal value depending on the size of the original binary frame
#The first line may include information about the frame itself such as a frame counter or time stamp, size/checksum for entire frame, etc
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def Parse_Logger_Line(str_line):
    global __debug2
    global __Total_frames_received
    global __Total_star_lines_received
    global __Log_Line_Number
    global __Log_Expected_Line_Number
    global __LogCurrentFrame
    
    rd_ptr = 1
    log_line_number = ival_8_conv_hex(str_line[rd_ptr+0], str_line[rd_ptr+1])
    rd_ptr = rd_ptr + 2
    if(str_line[0] == '&'):
        __Total_frames_received = __Total_frames_received + 1
        __Log_Expected_Line_Number = 0
        if(len(__LogCurrentFrame) > 0):
            Parse_Logger_frame_completed(__LogCurrentFrame)
        __LogCurrentFrame = ''
    if(str_line[0] == '*'):
        __Total_star_lines_received = __Total_star_lines_received + 1
        __Log_Expected_Line_Number = __Log_Expected_Line_Number + 1
    if(__Total_frames_received == 0):
        #synchronisation process : ignore the first lines that start with "*"
        #We start filling our very first frame buffer
        #only when encountering a line that starts with "&"
        #In other words, if the Python command to start logging is sent
        #while the firmware was already sending the log information,
        #then wait untill the firmware finish the current frame before effectively capturing any data
        return
    #if(log_line_number != __Log_Expected_Line_Number):
    #    print 'read_line:',log_line_number,',expected:',__Log_Expected_Line_Number
    size_str_line = len(str_line)
    #start a loop to analyze a pair of character from the received string
    #The starting index is 3 ; we skip the first character which identify the type of line
    #and we skip the first 2 hex characters, an 8 bit bytem which is not a frame data value but the line number
    while rd_ptr+1 < size_str_line:
        hex_val = ival_8_conv_hex(str_line[rd_ptr+0], str_line[rd_ptr+1])
        if hex_val < 0:
            if __debug2 == True:
                print 'invalid hex value at string index %d, line size:%d' % (rd_ptr, size_str_line)
            return
        #append the byte to the logger frame buffer
        #this buffer keep accumulating bytes when parsing each lines starting with "*"
        #the buffer is erased when parsing a line starting with "&", a new logger frame is being detected
        __LogCurrentFrame = __LogCurrentFrame + chr(hex_val)
        rd_ptr = rd_ptr + 2
        
def Parse_Logger_finish():
    global __Logfilehandle 
    if(__Logfilehandle !=None):
        __Logfilehandle.close()
        
def Parse_Logger_frame_completed(log_frame):
    global __LogTotalBytesCapture
    global __LogFrames
    global __LogTimestamp
    global __LogExpectedFrameSize
    global __LogTotalFramesSaved
    global __Logfilehandle
    num_bytes_current_frame = len(log_frame)
    if(__LogExpectedFrameSize != 0):
        if(num_bytes_current_frame != __LogExpectedFrameSize):
            #TODO: increment an error counter for statistical report
            return
    #else:
        #ignore frame size implicitly means print it, useful when testing a different firmware version
        #print 'Current Frame Size:', num_bytes_current_frame
    #
    #frame size is correct or is ignored
    #append the latest received frame to the array
    
    __LogTotalBytesCapture = __LogTotalBytesCapture + num_bytes_current_frame
    if (__Logfilehandle == None):
        __LogFrames.append(__LogCurrentFrame)
        __LogTimestamp.append(time.time())
    else:
        #We write a compacted binary file
        #A separate command is used to read back that file and convert to a CSV text document
        #It is assumed that writing in binary is orders of magnitude faster
        #compared to the generation of decimal numbers, and other markers
        #convert "double" to 8 bytes string
        time_stamp_as_string = struct.pack('>f', time.time())
        padding = chr(0xAB) + chr(0xAB) + chr(0xAB) + chr(0xAB) + chr(0xAB) + chr(0xAB) + chr(0xAB) + chr(0xAB) + chr(0xAB) + chr(0xAB) + chr(0xAB) + chr(0xAB) + chr(0xAB)
        __Logfilehandle.write(time_stamp_as_string + __LogCurrentFrame + padding)
    __LogTotalFramesSaved = __LogTotalFramesSaved + 1
    
#Programmer test of formatting in class    
def print_time_stamp():
    time_stamp = float(time.time())
    time_f32 = Memory.F32()
    time_f32.value(time_stamp)
    print 'Time stamp as read from time.py:', time_stamp
    print 'Time stamp as saved in CSV:', time_f32
    
#def time_unix_to_excel(time_param = None):
#    time_stamp = time.time()
#    seconds_per_days = 24 * 60 * 60
#    days_from_epoch = int(time_stamp / seconds_per_days)
#    fraction_seconds = time_stamp - (days_from_epoch * seconds_per_days)
#    print 'Excel date/time:', (days_from_epoch + 25569 + (fraction_seconds / seconds_per_days))
#    print 'time_stamp', time_stamp
#    print 'days_from_epoch:', days_from_epoch
#    print 'seconds since epoch:', (days_from_epoch * seconds_per_days)
#    print 'fraction_seconds:', fraction_seconds
#    print 'fraction_days:', (fraction_seconds / seconds_per_days)
    
def Log_Capture(SecondsWait, expected_frame_size = 0, filename = None, kick_logger = None):
    global __LogTotalBytesCapture
    global __LogFrames
    global __LogTimestamp
    global __LogExpectedFrameSize
    global __LogTotalFramesSaved
    global __Logfilehandle
    global __Total_frames_received
    
    if(filename != None):
        __Logfilehandle = open(filename,'w')
    else:
        __Logfilehandle = None
    __LogExpectedFrameSize = expected_frame_size
    str_to_send = ''
    #total_loops = 0
    #__Total_frames_received = 0
    #__Total_star_lines_received = 0
    #__LogCurrentFrame = ''
    __LogTotalFramesSaved = 0
    __LogTotalBytesCapture = 0
    last_frames_received = 0
    __LogFrames = []
    __LogTimestamp = []
    start_time                  = time.time()
    kick_time                   = start_time
    update_screen_time          = start_time
    while((start_time + SecondsWait) > time.time()):
        #total_loops = total_loops + 1
        #print 'Loop to capture logger frames:', total_loops
        time_time = time.time()
        picasso_talk_get_answer_rs232(str_to_send)
        if((kick_time + 2.0) > time_time):
            kick_time = time_time
            kick_logger(5)
            if((update_screen_time + 15.0) > time_time):
                update_screen_time = time_time
                if(last_frames_received != __LogTotalFramesSaved):
                    last_frames_received = __LogTotalFramesSaved
                    print 'Frames received:', __LogTotalFramesSaved
                win32ui.PumpWaitingMessages(0, -1)
        #if(__Total_frames_received != 0):
        #    print 'lines starting by <*>', __Total_star_lines_received
        #    print 'lines starting by <&> (frames)', __Total_frames_received
        #    print 'average lines per frame:', (float(__Total_star_lines_received) / float(__Total_frames_received))
    Parse_Logger_finish()        
    if(__LogTotalBytesCapture == 0):
        print 'No data from logger, make sure to enable logging with <t.logger.mask(1)> or <l.mask(1)> if <l = t.logger()>'
        if(filename != None):
            return (__LogTotalBytesCapture, __LogTotalFramesSaved)
        else:
            return (__LogFrames, __LogTimestamp)
    else:
        if(filename != None):
            print 'Logger total frames:',__LogTotalFramesSaved,', total size:', __LogTotalBytesCapture
            return (__LogTotalBytesCapture, __LogTotalFramesSaved)
        else:
            print 'Logger total frames:',__LogTotalFramesSaved,', total size:', __LogTotalBytesCapture
            return (__LogFrames, __LogTimestamp)
    
class PyTTXTalkException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)