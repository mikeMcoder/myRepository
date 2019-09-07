import os
import sys
sys.path.append(os.path.abspath('.'))

import TTM.TTM
import ITLA.ITLA
import TTM.Logger as l
import filecmp
import win32ui

MIN_FLASH_TIME = 30.0
FLASH_EXE_NAME = 'flashutilcl.exe'
DEFAULT_RETRY_COUNT = 2

if (__name__ == '__main__'):
    t = TTM.TTM.TTM()
    it = ITLA.ITLA.ITLA(t)
    t.save_it_obj(it)
    print 'Instantiated a TTX interface as t, ITLA as it.'

    #Connect to the msa
    it.connect(4)

    #Download the application ray files via 
    it.upgrade('application', r'C:\data\Sundial3.ray')

    it.release()

    #Reboot/Power Cycle    
    win32ui.MessageBox("Power Cycle Unit to reboot...  Press OK when done.", "uITLA Firmware Test") 

    #Restore kv File
    strTargetKVfilename = r'C:\Pub\UITLA-6-139.kv'
    #upload kv file
    #Restore given kv file to RAM
    

    #Connect via TTx interface...
    t.connect(4)
    
    t.restore('f', strTargetKVfilename)

    t.save()

    #Reboot/Power Cycle    
    win32ui.MessageBox("Power Cycle Unit to reboot...  Press OK when done.", "uITLA Firmware Test")    

    #Save to a Results.kv file
    strResultsFileName = r'c:\pub\Results.kv'
    if (os.path.exists(strResultsFileName)):
        os.remove(strResultsFileName)
    
    t.save('f', strResultsFileName)

    #Compare kv file and make sure there are no difference
    if filecmp.cmp(strTargetKVfilename, strResultsFileName):
        print 'PASS Dictionary Integrity Test:'
    else:
        print 'FAIL Dictionary Integrity Test:'


        
