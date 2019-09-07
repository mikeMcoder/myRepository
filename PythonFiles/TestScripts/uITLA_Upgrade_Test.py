import time

#initial Time t0
t0 = time.time()
COM_NUM = 1
prevFirmwareString = r'c:\data\Sundial3094.ray'
latestFirmwareString = r'c:\data\Sundial3102.ray'

def upgradeRate(BAUDRATE):
    
    print
    print '########################## version 0.1 ###################################'
    print '               Baudrate: ', BAUDRATE
    print '##########################################################################'

    print
    print '********************************* Set Baudrate to 115200'
    it.baudrate(115200)
    print '********************************* Read Baudrate'
    print it.baudrate()
    print '********************************* Read Baudrate'
    print it.baudrate()
    print '********************************* Read Baudrate'
    print it.baudrate()
    
    print
    print '********************************* Read Release'
    print it.release()
    print '********************************* Read Release'
    print it.release()
    print '********************************* Read Release'
    print it.release()
    
    print
    print '********************************* Upgrade Previous Version @ 115200'
    it.upgrade('application',prevFirmwareString)
    
    #Print Elapsed Time
    print 
    print 'Elapsed Time Since Start of Regression Test (In Minutes): '
    print (time.time()-t0)/60.0   
    
    print
    print '********************************* Read Release'
    print it.release()
    print '********************************* Read Release'
    print it.release()
    print '********************************* Read Release'
    print it.release()

    print    
    it.baudrate(BAUDRATE)
    print '********************************* Read Baudrate'
    print it.baudrate()
    print '********************************* Read Baudrate'
    print it.baudrate()
    print '********************************* Read Baudrate'
    print it.baudrate()
   
    print
    print '********************************* Upgrade New Version @',BAUDRATE
    it.upgrade('application',latestFirmwareString)

    print
    print '********************************* Read Release'
    print it.release()
    print '********************************* Read Release'
    print it.release()
    print '********************************* Read Release'
    print it.release()

    #Print Elapsed Time
    print 
    print 'Elapsed Time Since Start of Regression Test (In Minutes): '
    print (time.time()-t0)/60.0    

    return(1)    


'''
#Read F2 .kv file
print it.disconnect()
print
print '********************************** t.connect()'
print t.connect(COM_NUM)
print '********************************** Save F2.kv'
t.save('f',r'c:\data\file_F2.kv')
print '********************************** Disconnect'
t.disconnect()
'''

print
print '********************************* it.connect()'
it.connect(COM_NUM)
print '********************************* Read Release'
print it.release()
print '********************************* Read Release'
print it.release()
print '********************************* Read Release'
print it.release()
#############################################################

upgradeRate(115200)
upgradeRate(57600)
upgradeRate(38400)
upgradeRate(19200)
upgradeRate(9600)

print
print '********************************* it.disconnect'
print it.disconnect()

'''
#Read F3 .kv file
print
print '********************************* t.connect()'
print
print t.connect(COM_NUM)
print
print '********************************* Save F3.kv'
t.save('f',r'c:\data\file_F3.kv')
print
print '********************************* Disconnect'
t.disconnect()
'''

#Print Elapsed Time
print 
print 'Elapsed Time Since Start of Regression Test (In Minutes): '
print (time.time()-t0)/60.0    
print 'Test completed!'
