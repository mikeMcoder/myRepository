
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


REPEATX = 200
PORT = 7
BAUDRATE = 115200

class RestoreAndSave:
    def __init__(self):
        self.it = it
        self.t = t



    def test1(self):
        print ("==>TEST1")
        self.t.connect(PORT,BAUDRATE)
        lsr.logging(True)
        lsr.logfile('Test1Log.txt')
        
        for x in range(REPEATX):
            print ("Iteration:%d"%x)
            print("<==Restore the kv file")
            self.t.restore()#restore
            print("==>Save the kv file")
            self.t.save('f',str(it.serNo()[1][1].replace('\x00','') + '_' + str(x) + '_' +  '.kv'))
            time.sleep(3)
                
        print ("Test Complete!")
        self.t.disconnect()

    def test2(self):
        i = 999
        print ("==>TEST2")
        self.t.connect(PORT,BAUDRATE)
        self.t.restore()#restore
        self.t.save('f',str(it.serNo()[1][1].replace('\x00','') + '_' + str(i) + '_' +  '.kv'))# save to a location
        for x in range(REPEATX):
            print ("Iteration:%d"%x)
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
        time.sleep(1)


    def test3(self):

        print ("==>TEST3")
        self.t.connect(PORT,BAUDRATE)
        for x in range(REPEATX):
            print ("Iteration:%d"%x)
            print("<==Restore the kv file")
            t.restore()
            print("==>Save the kv file")
            t.save()
            time.sleep(3)#allow to initialize
           
        print ("Test Complete! Finished %dx restore and save"%x)
        self.t.disconnect()


    def test4(self):

        print ("==>TEST4")
        
        self.t.connect(PORT,BAUDRATE)
        for x in range(REPEATX):
            print ("Iteration:%d"%x)
            print("<==Restore the kv file")
            t.restore()

        print ("Test Complete! Finished %dx restore and save"%x)
        self.t.disconnect()



    def test5(self):
        print ("==>TEST5")
        
        self.t.connect(PORT,BAUDRATE)
        self.t.debugRS232(1)
        lsr.logging(True)
        lsr.logfile("TEST5Log.txt")
        for x in range(REPEATX):
            print ("Iteration:%d"%x)
            print("==>Save the kv file")
            t.save()
            time.sleep(3)#allow to initialize
        print ("Test Complete! Finished %dx restore and save"%x)
        self.t.disconnect()


    def test6(self):
        ''' Dictionaries that needed to be validated to be changing correctly and compare with kv_dict
         t.tuner().powerTuner().dictionary()
         t.system().dictionary()['system']['Actuator_state']
         t.system().dictionary()['ipc_defaults']['io_cap']
         t.domainStage().dictionary()['temperature_sensor_offset']
         t.modem().dictionary()['polarity']'''

#f = lsr.kv.kvdict['SYSTEM_DICTIONARY']['Actuator_state']
#a = lsr.kv.kvdict['IPC_DICTIONARY']['io_cap']
#t = lsr.kv.kvdict['DOMAIN_DICTIONARY']['temperature_sensor_offset']
#x = lsr.kv.kvdict['MODEM_DICTIONARY']['polarity']
        passCnt = 0
        print ("==>TEST6")
        self.t.connect(PORT,BAUDRATE)
        
        print("<==Restore the kv file")
        self.t.restore()                                                                 #restore the original kv file
        #self.t.save('f','original.kv')                                                   #save the file to a directory
        
        for i in range(REPEATX):
                
            try:
                self.actuatorState = lsr.kv.kvdict['SYSTEM_DICTIONARY']['Actuator_state']        #retrieve lsr kv_dict of actuator state
                print("The actuator state bit in the lsr dictionary is %d"%self.actuatorState)   #print value

                if self.actuatorState != 1 and self.actuatorState != -1:                         #check the actuator state if it is a valid value
                    raise ("Please check the unit, there is an issue with kv file")
                else:
                    pass


                self.ioCap = lsr.kv.kvdict['IPC_DICTIONARY']['io_cap']                           #iocap              
                print("The IOCAP value in the lsr dictionary is %d"%self.ioCap)                  #print value

                  
                
                #self.tempsensorOffset = lsr.kv.kvdict['DOMAIN_DICTIONARY']['temperature_sensor_offset'] #temp sensor offset-->commented because it does not exist in new kv file paramter
                #print("The Temperature offset value in the lsr dictionary is %d"%self.tempsensorOffset) #print value

                self.Tcase_adjustment_gain = lsr.kv.kvdict['DOMAIN_DICTIONARY']['Tcase_adjustment_gain'] #tcase adjustment gain--new addition to the test
                print("The Tcase_adjustment_gain value in the lsr dictionary is %d"%self.Tcase_adjustment_gain) #print value


                
                self.polarity = lsr.kv.kvdict['MODEM_DICTIONARY']['polarity']                           #retrieve kv_dict of polarity
                print("The Polarity bit in the lsr dictionary is %d"%self.polarity)                     #print value


                if self.polarity  != 1 and self.polarity  != -1:                                        #check the polarity if it is a valid value
                    raise ("Please check the unit, there is a polarity issue with kv file")
                else:
                    pass

               
            except:
                raise
            print ('\n')
            print ("==>Change the values of the parameters and check and compare")
            print ('\n')

            
    ##########################################################################################################################################################################
    ##########################################################################################################################################################################

            try:

                self.actuatorState = lsr.kv.kvdict['SYSTEM_DICTIONARY']['Actuator_state'] = 0                        #change lsr kv_dict of actuator state to -1
                self.ioCap = lsr.kv.kvdict['IPC_DICTIONARY']['io_cap'] = 70                                          #change the iocap value to 70             
                self.tempsensorOffset = lsr.kv.kvdict['DOMAIN_DICTIONARY']['temperature_sensor_offset'] = 60         #cahnge temp sensor offsetto 60
                self.Tcase_adjustment_gain= lsr.kv.kvdict['DOMAIN_DICTIONARY']['Tcase_adjustment_gain'] = 0.6
                self.polarity = lsr.kv.kvdict['MODEM_DICTIONARY']['polarity'] = 1                                    #retrieve kv_dict of polarity to 1
     

                self.t.save() #save it and check
                self.t.restore()#restore from unit
                
                self.actuatorState = lsr.kv.kvdict['SYSTEM_DICTIONARY']['Actuator_state']                               #get value
                print("The actuator state bit in the lsr dictionary is:  %d"%self.actuatorState)                        #print value
                
                self.ioCap = lsr.kv.kvdict['IPC_DICTIONARY']['io_cap']                                                  #get value
                print("The IOCAP value in the lsr dictionary after changing is: %d"% self.ioCap)                        #print value
                
                #self.tempsensorOffset = lsr.kv.kvdict['DOMAIN_DICTIONARY']['temperature_sensor_offset']                 #get value
                #print("The Temperature offset value in the lsr dictionary after changing is: %d"%self.tempsensorOffset) #print value
                
                self.Tcase_adjustment_gain = lsr.kv.kvdict['DOMAIN_DICTIONARY']['Tcase_adjustment_gain']
                print("The Tcase_adjustment_gain value in the lsr dictionary after changing is %d"%self.Tcase_adjustment_gain)
                
                self.polarity = lsr.kv.kvdict['MODEM_DICTIONARY']['polarity']                                           #get value
                print("The Polarity bit in the lsr dictionary after changing is: %d"%self.polarity)                     #print value

                print("\n") 
                print("==>Compare with t dictionaries")
                print("\n")
                self.actuatorStateSystem = self.t.system().dictionary()['system']['Actuator_state']                     #get value
                print("The actuator state bit in the t dictionary after changing is:  %d"%self.actuatorState)                        #print value
                
                self.ioCapSystem = t.system().dictionary()['ipc_defaults']['io_cap']                                          #get value
                print("The IOCAP value in the t dictionary after changing is: %d"% self.ioCap)                        #print value
                
                #self.tempsensorOffsetDomain = t.domainStage().dictionary()['temperature_sensor_offset']                       #get value
                #print("The Temperature offset value in the t dictionary after changing is: %d"%self.tempsensorOffset) #print value

                self.Tcase_adjustment_gainDomain = t.domainStage().dictionary()['Tcase_adjustment_gain']
                print("Tcase_adjustment_gainDomain value in the t dictionary after changing is: %d")%self.Tcase_adjustment_gainDomain


                self.polarityModem = t.modem().dictionary()['polarity']                                                      #get value
                print("The Polarity bit in the t dictionary after changing is: %d"%self.polarity)                     #print value
                
                
                if self.actuatorState != self.actuatorStateSystem:
                    print "Actuate State Failed"

                if self.ioCap != self.ioCapSystem:
                    print "Iocap Failed"

                if self.Tcase_adjustment_gain != self.Tcase_adjustment_gainDomain:
                    print "Tcase_adjustment_gain Failed"

                if self.polarity != self.polarityModem:
                    print "Polarity Failed"

                else:
                    print("All parameters passed")
                    
                    passCnt +=1
                    print ("Pass Count:", passCnt)

                t.restore('f','B31905A0Q.kv')
                t.save()

              
            except Exception as e:
                e.message
                raise


        print ("Pass Count:", passCnt)
        self.t.disconnect()
        print("Test Done")



    def test7(self):
        print ("==>TEST7")
        
        self.t.connect(PORT,BAUDRATE)
        self.t.restore()
        self.t.save('f','test77.kv') # get the original kv
        
        for x in range(REPEATX):
            print ("Iteration:%d"%x)
            print ("==> Hit Reset")
            self.t.reset()
            print("==>Restore the kv file from a location")
            time.sleep(3)
            self.t.connect(PORT,BAUDRATE)
            self.t.restore('f','test77.kv')
            self.t.save()
            time.sleep(3)#allow to initialize
        print ("Test Complete! Finished %dx restore and save"%x)
        self.t.disconnect()

    def test8(self):
        """calburn write and erase"""
        print("==>TEST8")
        self.t.connect(PORT,BAUDRATE)
        lsr.logging(True)
        lsr.logfile("TEST8Logs.txt") 
        for x in range(REPEATX):
            #print lsr.calBurn(burn=3) #write
            #print "==> Iteration:%d"%x," Burn"
            print lsr.calBurn(erase=3) #erase
            print "==> Iteration:%d"%x," Erase"

        print ("Test Complete! ")
        self.t.disconnect()


    def test9(self):
        """actuator on/ off calburn burn = 1"""
        REPEATXX = 100
        print("==>TEST9")
        self.t.connect(PORT,BAUDRATE)
        lsr.logging(True)
        lsr.logfile("TEST9Logs.txt") 
        for x in range(REPEATXX):
            print ("==>Iteration:",x)
            print "==>Actuator off"
            lsr.logentry("==>Actuator off")
            self.t.actuatoroff()
            time.sleep(0)
            print "==>Calburn(burn=1)"
            lsr.logentry("==>Calburn(burn=1)")
            lsr.calBurn(burn=1)
            print "==>Actuator on"
            lsr.logentry("==>Actuator on")
            self.t.actuatoron()
            time.sleep(3)

        print ("Test Complete! ")
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


##class TestControlstage:
##    """Test Functionality of Controlstage parameters"""
##    def __init__(self):
##        self.t = t
##
##    def testControlstage(self):
##        try:
##            self.t.connect(PORT,BAUDRATE)
##            time.sleep(1)
##            print ("==>>t.controlStage().frame()")
##            self.t.controlStage().frame()
##            print ("==>>t.controlStage().frame().elements()")
##            self.t.controlStage().frame().elements()
##        
            
            
                
        
    
    
        
                      
        
        
        


if __name__=='__main__':
    r = RestoreAndSave()
    Actuator = TestActuator()
    # r.test9()
    #r.test1()
    #r.test2()
    #r.test3()
    #r.test4()
    #r.test5()
    r.test6()
    r.test7()
    r.test9()

    #Actuator.testActuatorOnAndOff()
    #Baudrate = TestBaudrate()
    #Baudrate.testBaudrates()
    


                    


