import os
import sys
import time
sys.path.append(os.path.abspath('.'))




# Author: Michael Mercado
# August 09,2018

HUAWEI = 0
GENERIC = 1
BASIC = 0
GPIO_TEST = 0
FW_UPGRADE = 0





if (GPIO_TEST==1):
    
    import HardResetTestRelease as HRTR
    import LdisTestRelease as LDTR


elif (HUAWEI == 1) or (GENERIC == 1) or (BASIC== 1) or (FW_UPGRADE == 1):
        
    import SequentialFrequencyTestSuite as SFTS
    import RandomFrequencyTestSuite as RFTS
    import SequentialPowerTestSuite as SPTS
    import RandomPowerTestSuite as RPTS
    import SequentialFtfTestSuite as SFTFTS
    import RandomFtfTestSuite as RFTFTS
    import ReadOnlyRegisterTestSuite as RORTS
    import EchoResetTestRelease as ERTR
    import MainResetTestRelease as MRTR
    import SoftResetTestRelease as SRTR
    import PowerCycleTestRelease as PCTR
    import HwSoftResetTestRelease as HWSRTR
    import SanityCheckTestSuite as SCTS
    import OifTestSuite as OTS
    import FlashWriteStressTestSuite as FWSTS
    import FirmwareUpgradeTestSuite as FUTS
    
    


if __name__ == '__main__':
    
    if FW_UPGRADE:
        
        print "\n"
        print "\n"
        print "\n"
        print "####################################################"
        print "#############FIRMWARE UPGRADE TEST##################"
        print "####################################################"
        print "\n"
        print "\n"
        print "\n"

        try:
            FUTS.runTest() #run the case1 of sequential frequency test
        except:
            raise
        
        
        
    
    if BASIC:
        
        print "\n"
        print "\n"
        print "\n"
        print "#################################################"
        print "#############BASIC TEST SUITES##################"
        print "#################################################"
        print "\n"
        print "\n"
        print "\n"
        


        
        
        try:

            OTS.runCase1()    
            SCTS.SanityCheck().channelTest()
            SCTS.SanityCheck().pwrTest()
            SCTS.SanityCheck().nopTest()
            SCTS.SanityCheck().laserDisabletest(g)
            SCTS.SanityCheck().moduleSelecttest(g)
            SCTS.SanityCheck().hardResettest(g)
            SCTS.SanityCheck().mainResettest()
            SCTS.SanityCheck().softResettest()
            SCTS.SanityCheck().adtTest()
            SCTS.SanityCheck().genConfigtest()
            SCTS.SanityCheck().resenaTest()
            SCTS.SanityCheck().fPowthTest()
            SCTS.SanityCheck().wPowThTest()
            SCTS.SanityCheck().freqandThermalthresholdTest()
            SCTS.SanityCheck().srqTest()
            SCTS.SanityCheck().fatalTTest()
            SCTS.SanityCheck().almTTest()
            SCTS.SanityCheck().gridTest()
            RORTS.runCase1()
        except:
            raise
        


        
        
        

    if HUAWEI:
        print "\n"
        print "\n"
        print "\n"
        print "#################################################"
        print "#############HUAWEI TEST SUITES##################"
        print "#################################################"
        print "\n"
        print "\n"
        print "\n"
        
        
 
        
##        try:
##            SFTS.runCase1() #run the case1 of sequential frequency test
##        except:
##            raise
##        
##        try:
##            RFTS.runCase1() #run the case1 of random frequency test
##        except:
##            raise
##            
##        try:
##            SPTS.runCase1() #run the case1 of random frequency test
##        except:
##            raise
          
        try:
            RPTS.runCase1() #run the case1 of random frequency test
        except:
            raise


        try:
            SFTFTS.runCase1() #run the case1 of random frequency test
        except:
            raise 

        try:
            RFTFTS.runCase1() #run the case1 of random frequency test
        except:
            raise      

        try:
            ertr = ERTR.EchoResetTest()
            ertr.runTest()#run ECHO Reset Test
        except:
            raise      
            
        try:
            mrtr = MRTR.MainResetTest()
            mrtr.runTest()#run ECHO Reset Test
        except:
            raise
            
            
        try:
            hwsrtr = HWSRTR.HwSoftResetTest()
            hwsrtr.runTest()#run ECHO Reset Test
        except:
            raise

        try:
            pctr = PCTR.PowerCycleTest()
            pctr.runTest()#run ECHO Reset Test
        except:
            raise

        try:
            fwsts = FWSTS.main()
        except:
            raise


    if GPIO_TEST:

        print "\n"
        print "\n"
        print "\n"
        print "#################################################"
        print "#############GPIO TEST SUITES##################"
        print "#################################################"
        print "\n"
        print "\n"
        print "\n"
                
        try:
           
            hrtr = HRTR.HardResetTest()
            hrtr.runTest()#run ECHO Reset Test
        except:
            raise 
        
        try:
            ldtr = LDTR.LaserDisableTest()
            ldtr.runTest()#run ECHO Reset Test
        except:
            raise    
            
                             
            


#################################################################################################################################
#################################################################################################################################

    if GENERIC:
        print "\n"
        print "\n"
        print "\n"
        print "###################################################"
        print "############# GENERIC TEST SUITES##################"
        print "###################################################"
        print "\n"
        print "\n"
        print "\n"
        

        

##        try:
##            SFTS.runCase1() #run the case1 of sequential frequency test
##        except:
##            raise
##        
##        try:
##            RFTS.runCase1() #run the case1 of random frequency test
##        except:
##            raise 
##            
##        try:
##            SPTS.runCase1() #run the case1 of sequential power test
##        except:
##            raise
##
##        try:
##            RPTS.runCase1() #run the case1 of random power test
##        except:
##            raise

        try:
            SFTFTS.runCase1() #run the case1 of sequential ftf test
        except:
            raise             
            
        try:
            RFTFTS.runCase1() #run the case1 of random ftf test
        except:
            raise


        try:
            mrtr = MRTR.MainResetTest()
            mrtr.runTest()#run Main Reset Test
        except:
            raise                        
            
        try:
            srtr = SRTR.SoftResetTest()
            srtr.runTest()#run Soft Reset Test
        except:
            raise
            
            
        try:
            pctr = PCTR.PowerCycleTest()
            pctr.runTest()#run ECHO Reset Test
        except:
            raise      

       
        

    if not HUAWEI and not GENERIC:
        print "No Selection Made..."


















    
    
