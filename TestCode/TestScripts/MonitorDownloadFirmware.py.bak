import os
import sys
import time
sys.path.append(os.path.abspath('.'))

import TTM.TTM
import ITLA.ITLA
import TTM.Logger as l
import filecmp
import win32ui

MIN_FLASH_TIME = 30.0
FLASH_EXE_NAME = 'flashutilcl.exe'
DEFAULT_RETRY_COUNT = 2

RS232_COMPORT = 1

MyBaudRate = 115200
#MyBaudRate = 115200

if (__name__ == '__main__'):
    t = TTM.TTM.TTM()
    it = ITLA.ITLA.ITLA(t)
    t.save_it_obj(it)
    print 'Instantiated a TTX interface as t, ITLA as it.'

    #Connect to it using baud rate 9600
    it.connect(RS232_COMPORT)
    print 'it.connect(RS232_COMPORT)'

    print 'sleeping for 1 seconds'
    time.sleep(1) #Wait 1 seconds before 

    it.debugRS232(1)
    print 'it.debugRS232(1)'

    for i in range(4):
        try:
            it.nop()
            break
        except:
            pass

    
    time.sleep(1) #Wait 1 seconds before
    it.baudrate()
        
    print 'set baud rate to', MyBaudRate
    it.baudrate(MyBaudRate)

    time.sleep(1) #Wait 1 seconds before 
    it.baudrate()

    time.sleep(2) #Wait 1 seconds before 
    print 'upgrading firmware via monitor...'
    it.upgrade('application', r'..\FlashUtil\hex\Sundial3.ray')

    print 'sleeping for 5 seconds'
    time.sleep(5) #Wait 5 seconds before 

    it.release()

    time.sleep(1) #Wait 1 seconds before 
    it.nop()

    time.sleep(1) #Wait 1 seconds before 
    it.baudrate(9600)

    time.sleep(1) #Wait 1 seconds before 
    it.baudrate(9600)

    time.sleep(1) #Wait 1 seconds before 
    it.baudrate()

    it.disconnect()

    print 'sleeping for 5 seconds'
    time.sleep(5) #Wait 5 seconds before     

    #T2 Interface Tests...
    t.connect(RS232_COMPORT)

    #Restore kv File
    strTargetKVfilename = r'..\FlashUtil\hex\UITLA-6-139.kv'
    #upload kv file
    #Restore given kv file to RAM
    t.restore('f', strTargetKVfilename)

    t.save()

    t.disconnect()

    #Reboot/Power Cycle    
    win32ui.MessageBox("Power Cycle Unit to reboot...  Press OK when done.", "uITLA Firmware Test")    

    t.connect(RS232_COMPORT)

    #Save to a Results.kv file
    strResultsFileName = r'..\FlashUtil\hex\Results.kv'
    if (os.path.exists(strResultsFileName)):
        os.remove(strResultsFileName)
    
    t.save('f', strResultsFileName)

    #Compare kv file and make sure there are no difference
    if filecmp.cmp(strTargetKVfilename, strResultsFileName):
        print 'PASS Dictionary Integrity Test:'
    else:
        print 'FAIL Dictionary Integrity Test:'


        
