import os
import sys
sys.path.append(os.path.abspath('.'))

import TTM.TTM
import ITLA.ITLA
import TTM.Logger as l
import filecmp
import win32ui


if (__name__ == '__main__'):
    t = TTM.TTM.TTM()
    it = ITLA.ITLA.ITLA(t)
    t.save_it_obj(it)
    print 'Instantiated a TTX interface as t, ITLA as it.'

    #T2 Interface Tests...
    t.connect(4)

    #1.  kv file integrity check...
    #1a.  Save to kv file Save1st.kv
    strSave1stFileName = r'c:\pub\Save1st.kv'
    if (os.path.exists(strSave1stFileName)):
        os.remove(strSave1stFileName)
    
    t.save('f', strSave1stFileName)
    
    #1b.  Restore Save1st.kv to RAM
    t.restore('f', strSave1stFileName)

    t.save()

    #Reboot/Power Cycle    
    win32ui.MessageBox("Power Cycle Unit to reboot...  Press OK when done.", "uITLA Firmware Test")    

    #1c.  Save to kv file Save2nd.kv
    strSave2ndFileName = r'c:\pub\Save2nd.kv'
    if (os.path.exists(strSave2ndFileName)):
        os.remove(strSave2ndFileName)
    
    t.save('f', strSave2ndFileName)

    #1d.  Compare all these files to make sure they match...
    if filecmp.cmp(strSave1stFileName, strSave2ndFileName):
        print 'PASS Dictionary Integrity Test:'
    else:
        print 'FAIL Dictionary Integrity Test:'

    strTargetKVfilename = r'C:\Pub\UITLA-6-139.kv'
    #2.  upload kv file
    #2a.  Restore given kv file to RAM
    t.restore('f', strTargetKVfilename)

    t.save()

    #Reboot/Power Cycle    
    win32ui.MessageBox("Power Cycle Unit to reboot...  Press OK when done.", "uITLA Firmware Test")    

    #2b.  Save to a Results.kv file
    strResultsFileName = r'c:\pub\Results.kv'
    if (os.path.exists(strResultsFileName)):
        os.remove(strResultsFileName)
    
    t.save('f', strResultsFileName)

    #2c.  Compare kv file and make sure there are no difference
    if filecmp.cmp(strTargetKVfilename, strResultsFileName):
        print 'PASS 2nd Dictionary Integrity Test:'
    else:
        print 'FAIL 2nd Dictionary Integrity Test:'

    #BASIC Tests
    #1.  Upload latest kv file in given good unit (Done from last step...)
    #2.  Read that F1, F2, SiTemps are in good range
    #3.  Use Current Tuner to tune to a frequency @ a particular GMI
    #3a.  Output DomainStage frame
    #3b.  Output ControlStage frame
    #3c.  Output DiscreteStage frame
    
    
    #4.  Use Power Tuner to tune to a frequency @ a particular power...


    #Monitor firmware/Firmware upgrade tests

    

    #MSA commands...


    t.disconnect()

