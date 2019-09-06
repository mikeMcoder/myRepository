
import os
import sys
import time
sys.path.append(os.path.abspath('.'))

if sys.platform == 'cygwin':
    # for cygwin, use the packages installed from the windows installation of python
    sys.path.append('/cygdrive/c/Python27/Lib/site-packages/')

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
t.save_it_obj(it)

print 'Instantiated a TTX interface as t, ITLA as it.'

REPEAT = 10
REPEAT_RESTORE = 100
REPEATX = 100
PORT = 1
BAUDRATE = 115200

class RestoreAndSave:
    def __init__(self):
        self.it = it
        self.t = t

    def test1(self):
        self.t.connect(PORT,BAUDRATE)
        for i in range(REPEAT):#run restore and save 100x
            for x in range(REPEAT_RESTORE):
                print("<==Restore the kv file")
                self.t.restore()#restore
            print("==>Save the kv file")
            self.t.save('f',str(it.serNo()[1][1].replace('\x00','') + '_' + str(i) + '_' +  '.kv'))
        print ("Test Complete!")
        self.t.disconnect()

    def test2(self):
        i = 999
        self.t.connect(PORT,BAUDRATE)
        self.t.restore()#restore
        self.t.save('f',str(it.serNo()[1][1].replace('\x00','') + '_' + str(i) + '_' +  '.kv'))# save to a location
        for x in range(REPEATX):
            print("<==Restore the kv file")
            t.restore('f',str(it.serNo()[1][1].replace('\x00','') + '_' + str(i) + '_' +  '.kv'))
            print("==>Save the kv file")
            t.save()
            time.sleep(3)#allow to initialize
            print("<==Restore the kv file")
            self.t.restore()
            print("==>Save the kv file")
            self.t.save('f',str(it.serNo()[1][1].replace('\x00','') + '_' + str(x) + '_' + 'FromUnit' + '.kv'))# save to a location
            time.sleep(3)
        print ("Test Complete! Finished %dx restore and save"%x)
        self.t.disconnect()

class TestActuator:
    """test the actuator on/off feature"""
    def __init__(self):
        self.repeat = 1
        self.t = t
    def testActuatorOnAndOff(self):
        for i in range(self.repeat):
            try:
                self.t.connect(PORT,BAUDRATE)
                time.sleep(1)
                print "\n"
                print "==>TURN ACTUATOR ON"
                print "\n"
                self.t.actuatoron()
                time.sleep(1)
                print self.t.domainStage().frame()
                time.sleep(1)
                print "\n"
                print "==>TURN ACTUATOR OFF"
                print "\n"
                self.t.actuatoroff()
                time.sleep(1)
                print self.t.domainStage().frame()
                self.t.disconnect()
            except (Exception):
                raise "Command Not Working"

class TestBaudrate:
    """Switch baudrates"""
    def __init__(self):
        self.t = t
        self.a = None
        self.b = None

    def testBaudrates(self):
        try:
            self.t.connect(PORT,BAUDRATE)
            time.sleep(1)
            a, b = self.t.baudrate()
            print "Current Budrate is:%d"%b
            self.t.baudrate(9600)
            a, b = self.t.baudrate()
            print "Current Budrate is:%d"%b
            self.t.baudrate(19200)
            a, b = self.t.baudrate()
            print "Current Budrate is:%d"%b
            self.t.baudrate(38400)
            a, b = self.t.baudrate()
            print "Current Budrate is:%d"%b
            self.t.baudrate(57600)
            a, b = self.t.baudrate()
            print "Current Budrate is:%d"%b
            self.t.baudrate(115200)
            self.t.disconnect()
            print "Test Done"
        except(Exception):
            raise "Not Correct Badurate"


class TestControlstage:
    """Test Functionality of Controlstage parameters"""
    def __init__(self):
        self.t = t

    def testControlstage(self):
        try:
            self.t.connect(PORT,BAUDRATE)
            time.sleep(1)
            print ("==>>t.controlStage().frame()")
            self.t.controlStage().frame()
            print ("==>>t.controlStage().frame().elements()")
            self.t.controlStage().frame().elements()
        
            
            
                
        
    
    
        
                      
        
        
        


if __name__=='__main__':
    r = RestoreAndSave()
    Actuator = TestActuator()
    #r.test1()
    #r.test2()
    #Actuator.testActuatorOnAndOff()
    Baudrate = TestBaudrate()
    Baudrate.testBaudrates()
    


                    


