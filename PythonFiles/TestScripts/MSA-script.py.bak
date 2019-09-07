import time
import struct
import inspect

cmdDebug = 1
calculateSum = 1
fail = 0

def ln():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def sleep(cnt):
    print('Wait %d sec ' % cnt)
    for i in range(cnt):    
        print('.'),
        sys.stdout.flush() 
        time.sleep(1)
    print('done')

def addChecksum(cmd):
    if calculateSum == 0:
        return cmd
    bytes = struct.unpack('BBBB', cmd)
    bip8 = (bytes[0] & 0x0F) ^ bytes[1] ^ bytes[2] ^ bytes[3]    
    b =  ((((bip8 & 0xF0) >> 4) ^ (bip8 & 0x0F))<<4) | (bytes[0] & 0x0F)
    cmd = struct.pack('BBBB', b, bytes[1], bytes[2], bytes[3])
    return cmd

def send(line, cmd, reply=None):
    global fail
    cmd = addChecksum(cmd)
    it.write(cmd)
    answer = it.read(4, 1)     #no retries
    if len(answer) != 4:
        fail = 1
        print 'error: No Response'
        if(cmdDebug == 1): return 1      # do not abort script
        sys.exit()
    if (reply != None):
        reply = addChecksum(reply)
        if (answer != reply):
            print line, ' Expected: \\x%02X\\x%02X\\x%02X\\x%02X  Got: \\x%02X\\x%02X\\x%02X\\x%02X' % ( \
                  ord(reply[0]), ord(reply[1]), ord(reply[2]), ord(reply[3]), \
                  ord(answer[0]), ord(answer[1]), ord(answer[2]), ord(answer[3]))
            fail = 1
            if(cmdDebug == 1): return 1      # do not abort script
            sys.exit()
    else:
        print '** COMPARE SKIPPED!'
    return 0    # OK no errors
    
#COM_PORT = input("Enter COM PORT #")
if len(sys.argv) < 2:
    COM_PORT = 1        # default, no argument
else:
    COM_PORT = sys.argv[1] 
print '\n\n\nCOM PORT = ', COM_PORT 
if len(sys.argv) < 3:
    it.debugRS232(0)
else:
    it.debugRS232(sys.argv[2])
it.connect(COM_PORT,9600)

#first cmd was sent by connect = x27272727 -> error 2 RNW
print '0x00 NOP test'
send(ln(), '\x00\x66\x00\x00', '\x55\x66\x00\x00')    #cmd has an error
send(ln(), '\x00\x00\x00\x00', '\x04\x00\x00\x11')    #last cmd had an error
send(ln(), '\x08\x00\x00\x00', '\x04\x00\x00\x11')    #resend last reply
send(ln(), '\x00\x00\x00\x00', '\x04\x00\x00\x10')    #normal response OK
calculateSum = 0;
send(ln(), '\x10\x00\x00\x00', '\xCC\x00\x00\x00')    #checksum error
calculateSum = 1;
send(ln(), '\x00\x00\x00\x00', '\x04\x00\x00\x10')    #normal response OK

print '0x01 DevType test'
send(ln(), '\x00\x01\x00\x00', '\x06\x01\x00\x08')                        
send(ln(), '\x00\x0B\x00\x00', '\x04\x0B\x43\x57')    #CW
send(ln(), '\x00\x0B\x00\x00', '\xF4\x0B\x20\x75')    # u
send(ln(), '\x00\x0B\x00\x00', '\x34\x0B\x49\x54')    #IT
send(ln(), '\x00\x0B\x00\x00', '\x24\x0B\x4C\x41')    #LA
send(ln(), '\x00\x0B\x00\x00', '\xE5\x0B\x00\x00')    #error max size 

print '0x02 Manufacturer test'
send(ln(), '\x00\x02\x00\x00', '\x06\x02\x00\x06')
send(ln(), '\x00\x0B\x00\x00', '\x04\x0B\x45\x6D')    #Em
send(ln(), '\x00\x0B\x00\x00', '\x04\x0B\x63\x6F')    #co
send(ln(), '\x00\x0B\x00\x00', '\x04\x0B\x72\x65')    #re
send(ln(), '\x00\x0B\x00\x00', '\x05\x0B\x00\x00')    #error max size
send(ln(), '\x00\x00\x00\x00', '\x04\x00\x00\x16')    #status has an error ERE
send(ln(), '\x00\x00\x00\x00', '\x04\x00\x00\x10')

print '0x03 Model test'
send(ln(), '\x00\x03\x00\x00', '\x46\x03\x00\x10')
send(ln(), '\x00\x0B\x00\x00', '\xF4\x0B\x54\x54')    #TT
send(ln(), '\x00\x0B\x00\x00', '\x04\x0B\x58\x31')    #X1
send(ln(), '\x00\x0B\x00\x00', '\xF4\x0B\x39\x39')    #99
send(ln(), '\x00\x0B\x00\x00', '\xD4\x0B\x35\x37')    #57
send(ln(), '\x00\x0B\x00\x00', '\x34\x0B\x35\x39')    #59
send(ln(), '\x00\x0B\x00\x00', '\xF4\x0B\x30\x30')    #00
send(ln(), '\x00\x0B\x00\x00', '\x94\x0B\x4E\x48')    #NH
send(ln(), '\x00\x0B\x00\x00', '\xC4\x0B\x30\x00')    #0
                                
print '0x04 Serial No test'
send(ln(), '\x00\x04\x00\x00', '\xD6\x04\x00\x0F')
send(ln(), '\x00\x0B\x00\x00', '\xE4\x0B\x47\x31')    #G1
send(ln(), '\x00\x0B\x00\x00', '\x84\x0B\x41\x31')    #A1
send(ln(), '\x00\x0B\x00\x00', '\x34\x0B\x2D\x30')    #-0
send(ln(), '\x00\x0B\x00\x00', '\xF4\x0B\x30\x30')    #00
send(ln(), '\x00\x0B\x00\x00', '\x34\x0B\x2D\x30')    #-0
send(ln(), '\x00\x0B\x00\x00', '\xF4\x0B\x30\x30')    #00
send(ln(), '\x00\x0B\x00\x00', '\xE4\x0B\x30\x31')    #01
send(ln(), '\x00\x0B\x00\x00', '\xF4\x0B\x00\x00')    #
                          
print '0x05 MFG Date test'
send(ln(), '\x00\x05\x00\x00', '\xF6\x05\x00\x0C')
send(ln(), '\x00\x0B\x00\x00', '\xE4\x0B\x30\x31')    #01
send(ln(), '\x00\x0B\x00\x00', '\x94\x0B\x2D\x4D')    #-M
send(ln(), '\x00\x0B\x00\x00', '\x64\x0B\x41\x59')    #AY
send(ln(), '\x00\x0B\x00\x00', '\x14\x0B\x2D\x32')    #-2
send(ln(), '\x00\x0B\x00\x00', '\xE4\x0B\x30\x31')    #01
send(ln(), '\x00\x0B\x00\x00', '\xF4\x0B\x33\x00')    #3
                          
print '0x06 Release test'
send(ln(), '\x00\x06\x00\x00', '\x86\x06\x00\x2A')
send(ln(), '\x00\x0B\x00\x00', '\x94\x0B\x50\x56')    #PV
send(ln(), '\x00\x0B\x00\x00', '\xC4\x0B\x20\x32')    # 2
send(ln(), '\x00\x0B\x00\x00', '\x04\x0B\x2E\x30')    #.0
send(ln(), '\x00\x0B\x00\x00', '\x04\x0B\x2E\x30')    #.0
send(ln(), '\x00\x0B\x00\x00', '\xA4\x0B\x3A\x48')    #:H
send(ln(), '\x00\x0B\x00\x00', '\xF4\x0B\x57\x20')    #W 
send(ln(), '\x00\x0B\x00\x00', '\x24\x0B\x32\x2E')    #2. 
send(ln(), '\x00\x0B\x00\x00', '\x04\x0B\x30\x2E')    #0. 
send(ln(), '\x00\x0B\x00\x00', '\x54\x0B\x30\x3A')    #0: 
send(ln(), '\x00\x0B\x00\x00', '\xF4\x0B\x46\x57')    #FW
send(ln(), '\x00\x0B\x00\x00', '\xD4\x0B\x20\x33')    # 3 
send(ln(), '\x00\x0B\x00\x00', '\x04\x0B\x2E\x30')    #.0 
send(ln(), '\x00\x0B\x00\x00', '\x64\x0B\x2E\x36')    #.6
send(ln(), '\x00\x0B\x00\x00', '\x34\x0B\x3A\x41')    #:A 
send(ln(), '\x00\x0B\x00\x00', '\xB4\x0B\x53\x20')    #S  
send(ln(), '\x00\x0B\x00\x00', '\xA4\x0B\x43\x31')    #C1 
send(ln(), '\x00\x0B\x00\x00', '\xD4\x0B\x3A\x4F')    #:O 
send(ln(), '\x00\x0B\x00\x00', '\xC4\x0B\x54\x20')    #T  
send(ln(), '\x00\x0B\x00\x00', '\xC4\x0B\x31\x2E')    #1.  
send(ln(), '\x00\x0B\x00\x00', '\xC4\x0B\x30\x2E')    #0.  
send(ln(), '\x00\x0B\x00\x00', '\xC4\x0B\x30\x00')    #0  
                                
print '0x07 Release Back test'
send(ln(), '\x00\x07\x00\x00', '\x96\x07\x00\x2A')
send(ln(), '\x00\x0B\x00\x00', '\x94\x0B\x50\x56')    #PV
send(ln(), '\x00\x0B\x00\x00', '\xF4\x0B\x20\x31')    # 1
send(ln(), '\x00\x0B\x00\x00', '\x04\x0B\x2E\x30')    #.0
send(ln(), '\x00\x0B\x00\x00', '\x04\x0B\x2E\x30')    #.0
send(ln(), '\x00\x0B\x00\x00', '\xA4\x0B\x3A\x48')    #:H
send(ln(), '\x00\x0B\x00\x00', '\xF4\x0B\x57\x20')    #W 
send(ln(), '\x00\x0B\x00\x00', '\x24\x0B\x32\x2E')    #2. 
send(ln(), '\x00\x0B\x00\x00', '\x04\x0B\x30\x2E')    #0. 
send(ln(), '\x00\x0B\x00\x00', '\x54\x0B\x30\x3A')    #0: 
send(ln(), '\x00\x0B\x00\x00', '\xF4\x0B\x46\x57')    #FW
send(ln(), '\x00\x0B\x00\x00', '\xD4\x0B\x20\x33')    # 3 
send(ln(), '\x00\x0B\x00\x00', '\x04\x0B\x2E\x30')    #.0 
send(ln(), '\x00\x0B\x00\x00', '\x04\x0B\x2E\x30')    #.0
send(ln(), '\x00\x0B\x00\x00', '\x34\x0B\x3A\x41')    #:A 
send(ln(), '\x00\x0B\x00\x00', '\xB4\x0B\x53\x20')    #S  
send(ln(), '\x00\x0B\x00\x00', '\xA4\x0B\x43\x31')    #C1 
send(ln(), '\x00\x0B\x00\x00', '\xD4\x0B\x3A\x4F')    #:O 
send(ln(), '\x00\x0B\x00\x00', '\xC4\x0B\x54\x20')    #T  
send(ln(), '\x00\x0B\x00\x00', '\xC4\x0B\x31\x2E')    #1.  
send(ln(), '\x00\x0B\x00\x00', '\xC4\x0B\x30\x2E')    #0.  
send(ln(), '\x00\x0B\x00\x00', '\xC4\x0B\x30\x00')    #0  
                        
print '0x08 Gen CFG test'
send(ln(), '\x00\x08\x00\x00', '\xC4\x08\x00\x00')

print '0x0D IO_CAP test'
send(ln(), '\x00\x0D\x00\x00', '\xC4\x0D\x00\x05')
 
print '0x14 DL CONFIG test'
send(ln(), '\x00\x14\x00\x00', '\x04\x14\x01\x00')

print '0x15 DL STATUS test'
send(ln(), '\x00\x15\x00\x00', '\x04\x15\x00\x00')

print '0x0 MODULE STATUStest'
send(ln(), '\x00\x20\x00\x00', '\xC4\x20\xE2\x42')
send(ln(), '\x00\x21\x00\x00', '\xD4\x21\xE7\x47')
                        
print '0x22-3 Power Thresh test'
send(ln(), '\x00\x22\x00\x00', '\x04\x22\x03\xE8')    
send(ln(), '\x00\x23\x00\x00', '\x04\x23\x00\xB0')   
print '0x24-5 Freq Thresh test'
send(ln(), '\x00\x24\x00\x00', '\x04\x24\x00\x64')    
send(ln(), '\x00\x25\x00\x00', '\x04\x25\x00\x19')   
print '0x26-7 Thermal Thresh test'
send(ln(), '\x00\x26\x00\x00', '\x74\x26\x1B\x58')    
send(ln(), '\x00\x27\x00\x00', '\x44\x27\x0F\xA0')   
print '0x28 SRQ Trigger test'
send(ln(), '\x00\x28\x00\x00', '\x04\x28\x10\x3F')      #pb it should be 0x1FBF   
print '0x29 Fatal Trigger test'
send(ln(), '\x00\x29\x00\x00', '\x04\x29\x00\x0F')   
print '0x2A SRQ Trigger test'
send(ln(), '\x00\x2A\x00\x00', '\x04\x2A\x0D\x0D')   

print '0x30 Channel test'
send(ln(), '\x00\x30\x00\x00', '\x65\x30\x00\x00')      # 1?, error not cfg
#send(ln(), '\x01\x30\x00\x59', '\x04\x30\x00\x59')     #max ch:0x59 = 89d
#send(ln(), '\x00\x30\x00\x00', '\x04\x30\x00\x59')
#send(ln(), '\x00\x00\x00\x00', '\x04\x00\x00\x10')     #pending ?
#send(ln(), '\x01\x30\x00\x01', '\x04\x30\x00\x01')
#send(ln(), '\x00\x30\x00\x00', '\x04\x30\x00\x01')     #back to default
#send(ln(), '\x00\x00\x00\x00', '\x04\x00\x00\x10')
send(ln(), '\x01\x30\x00\x00', '\x05\x30\x00\x00')      #error, pass min/max
#send(ln(), '\x01\x30\x00\x5A', '\x05\x30\x00\x5A')

print '0x31 OPTICAL PWR test'
send(ln(), '\x00\x31\x00\x00', '\x74\x31\x05\x15')

print '0x32 RESET ENABLE test'
send(ln(), '\x00\x32\x00\x00', '\xD4\x32\x00\x08')      #pb SENA=1, should be 0

print '0x33 CFG BEHAVIOR test'
send(ln(), '\x00\x33\x00\x00', '\x64\x33\x00\x02')

print '0x34 GRID SPACING test'
send(ln(), '\x00\x33\x00\x00', '\x64\x33\x00\x02')

print '0x35-6 FIRST CH FREQ test'
send(ln(), '\x00\x35\x00\x00', '\x64\x35\x00\xBF')
send(ln(), '\x00\x36\x00\x00', '\x94\x36\x0B\xB8')
                        
print '0x40-1 LASER FREQ test'
send(ln(), '\x00\x40\x00\x00') #, '\xF4\x40\x00\xC3')
send(ln(), '\x00\x41\x00\x00') #, '\x54\x41\x1D\x4C')
                          
print '0x42 OPTICAL OUTPUT PWR test'
send(ln(), '\x00\x42\x00\x00') #, '\x14\x42\x03\xBB')

print '0x43 CURR TEMP test'
send(ln(), '\x00\x43\x00\x00')    #, '\x14\x43\xE6\x0A')

print '0x4F FINE TUNE FREQ RANGE test'
send(ln(), '\x00\x4F\x00\x00', '\xE5\x4F\x00\x00')

print '0x50-1 OPTICAL PWR MIN-MAX test'
send(ln(), '\x00\x50\x00\x00', '\x34\x50\x02\xBB')
send(ln(), '\x00\x51\x00\x00', '\x74\x51\x05\x46')
                          
print '0x52-5 LASER FIRST LAST FREQ test'
send(ln(), '\x00\x52\x00\x00', '\x74\x52\x00\xBF')
send(ln(), '\x00\x53\x00\x00', '\xA4\x53\x0B\xB8')
send(ln(), '\x00\x54\x00\x00', '\xD4\x54\x00\xC4')
send(ln(), '\x00\x55\x00\x00', '\xE4\x55\x01\xF4')
                        
print '0x56 LASER MIN GRID SPACING test'
send(ln(), '\x00\x56\x00\x00', '\x64\x56\x00\x01')

print '0x57 MODULE CURRENTS test'
send(ln(), '\x00\x57\x00\x00', '\x06\x57\x00\x04')

print '0x58 MODULE TEMP TEST'
send(ln(), '\x00\x58\x00\x00', '\xF6\x58\x00\x04')

print '0x59-C DIGITAL DITHER test'
send(ln(), '\x00\x59\x00\x00', '\xA4\x59\x00\x02')
send(ln(), '\x00\x5A\x00\x00', '\xB4\x5A\x00\x00')
send(ln(), '\x00\x5B\x00\x00', '\xA4\x5B\x00\x00')
send(ln(), '\x00\x5C\x00\x00', '\xD4\x5C\x00\x00')
                        
print '0x5D-E WARNING LIMIT test'
send(ln(), '\x00\x5D\x00\x00', '\xD5\x5D\x00\x00')
send(ln(), '\x00\x5E\x00\x00', '\xE5\x5E\x00\x00')
                        
print '0x5F-60 AGE THRESH test'
send(ln(), '\x00\x5F\x00\x00', '\xC4\x5F\x00\x64')
send(ln(), '\x00\x60\x00\x00', '\xD4\x60\x00\x5A')
                        
print '0x61 LASER AGE test'
send(ln(), '\x00\x61\x00\x00', '\x34\x61\x00\x00')

print '0x62 FINE TUNE FREQ test'
send(ln(), '\x00\x62\x00\x00', '\x04\x62\x00\x00')

#send(ln(), '\x00\x00\x00\x00')    #just get a response and ignore

it.disconnect()
if fail == 1:
    print '*** MSA CMDS FAILED! ***'
else:
    print 'MSA CMDS PASSED!'
