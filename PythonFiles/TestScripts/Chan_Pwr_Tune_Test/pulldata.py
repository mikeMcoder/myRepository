import InstrumentDrivers_DS as inst
import time

class pulldata:

    def __init__(self):
        print 'pulldata init'

    def record(self,paramL):

        try:
            WA_1100_address = input('BurleighWA1100 GPIB address(def:4)')
        except:
            WA_1100_address = 4
        print 'WA_1100_address :',WA_1100_address
        WA_1100 = inst.BurleighWA1100(0,WA_1100_address)
        WA_1100.connect()
        
        try:
            POW_8163A_address = input('Agilent8163A GPIB address(def:20)')
        except:
            POW_8163A_address = 20
        print 'POW_8163A_address :',POW_8163A_address
        POW_8163A = inst.Agilent8163B(0,POW_8163A_address)
        POW_8163A.connect()
        try:
            POW_8163A_config = input('Agilent8163A SetActiveConf(def:"1,1")')
        except:
            POW_8163A_config = "1,1"
        exec("POW_8163A.SetActiveConf('POW',%s)"%(POW_8163A_config))
        print 'meters initialized'
        
        [test_name,channelseq,channelcyc,pwrseq,pwrcyc,samplingL,samplingP]=paramL
        test_file = open("%s.csv"%(test_name),"w")
        test_file.write("serNo,release,datetime,timelapse,lf,meterf,\
channel,PWR,OOP,meterpwr,sledT,pcbT,teccurrent,\
diodcurrent,SRQ,ALM,FATAL,DIS,WVSF,WFREQ,\
WTHERM,WPWR,XEL,CEL,MRL,CRL,WVSFL,WFREQL,\
WTHERML,WPWRL,FVSF,FFREQ,FTHERM,FPWR,FVSFL,\
FFREQL,FTHERML,FPWRL\n")
        test_file.close()

        expectduration = float(channelcyc*pwrcyc*len(channelseq)*len(pwrseq))*samplingL
        print 'channelseq : %s\nchannelcyc : %d\npwrseq : %s\npwrcyc : %d\nsamplingL(s) : %d\nsamplingP(s) : %d'%(channelseq,channelcyc,pwrseq,pwrcyc,samplingL,samplingP)

        globleST = time.time()
        for i in range(channelcyc):
            for curchannel in channelseq:
                for j in range(pwrcyc):
                    for curpwr in pwrseq:
                        localST = time.time()
                        localTL= 0.0
                        it.channel(curchannel)
                        it.pwr(curpwr)
                        #clear alarm & fatal in each channel/pwr change
                        #self.clearalarm()
                        
                        while(localTL<(samplingL-samplingP)):
                            samplingST = time.time()
                            outstring = ""
                            if 1:
                            #try:
                                outstring += self.itpull(globleST,POW_8163A,WA_1100)
                                try:
                                    test_file = open("%s.csv"%(test_name),"a+")
                                    test_file.write(outstring+"\n")
                                    test_file.close()
                                    print 'output : %s'%(outstring)
                                    
                                except IOError:
                                    raise 'Error : file is opened in another program'
                            else:
                            #except:
                                test_file = open("%s.csv"%(test_name),"a+")
                                test_file.write("Error")
                                test_file.close()
                                print ' Error : itpull'

                            curtime     = time.time()                
                            samplingTL  = curtime-samplingST
                            localTL     = curtime-localST
                            globleTL    = curtime-globleST
                            countdown   = (expectduration - globleTL)/3600
                            restP = max(samplingP-samplingTL,0)
                            print 'samplingTL : %s \nlocalTL : %s \nglobleTL : %s \ncountdown in hrs: %s \nsleep: %s \n'%(samplingTL,localTL,globleTL,countdown, restP)
                            sys.stdout.flush()
                            time.sleep(restP)
                            sys.stdout.flush()
        print 'finished\n'


    def itpull (self,time0,pwrmeter,freqmeter):
        dummy0 = it.serNo()
        c0 = str(dummy0[1][1:])
        c0 = c0.strip("('")
        c0 = c0.strip("',)")
        c1 = time.asctime()
        c2 = str((time.time()-time0)/3600)
        (dummy1,c3) = it.lf()
        c3 = str(c3)
        (dummy4,c4) = it.channel()
        c4 = str(c4)
        dummy5 = it.statusW()
        c5 = str(int(dummy5[1].fieldSrq().value()))
        c6 = str(int(dummy5[1].fieldAlm().value()))
        c7 = str(int(dummy5[1].fieldFatal().value()))
        c8 = str(int(dummy5[1].fieldDis().value()))
        c9 = str(int(dummy5[1].fieldWvsf().value()))
        c10 = str(int(dummy5[1].fieldWfreq().value()))
        c11 = str(int(dummy5[1].fieldWtherm().value()))
        c12 = str(int(dummy5[1].fieldWpwr().value()))
        c13 = str(int(dummy5[1].fieldXel().value()))
        c14 = str(int(dummy5[1].fieldCel().value()))
        c15 = str(int(dummy5[1].fieldMrl().value()))
        c16 = str(int(dummy5[1].fieldCrl().value()))

        it.statusW(xel=1)
        it.statusW(cel=1)       
        it.statusW(mrl=1)
        it.statusW(crl=1)  
        
        c17 = str(int(dummy5[1].fieldWvsf().value()))
        c18 = str(int(dummy5[1].fieldWfreql().value()))
        c19 = str(int(dummy5[1].fieldWtherml().value()))
        c20 = str(int(dummy5[1].fieldWpwrl().value()))

        it.statusW(wvsfl=1)
        it.statusW(wfreql=1)       
        it.statusW(wtherml=1)
        it.statusW(wpwrl=1)  

        dummy6 = it.statusF()
        c21 = str(int(dummy6[1].fieldFvsf().value()))
        c22 = str(int(dummy6[1].fieldFfreq().value()))
        c23 = str(int(dummy6[1].fieldFtherm().value()))
        c24 = str(int(dummy6[1].fieldFpwr().value()))
        c25 = str(int(dummy6[1].fieldFvsf().value()))
        c26 = str(int(dummy6[1].fieldFfreql().value()))
        c27 = str(int(dummy6[1].fieldFtherml().value()))
        c28 = str(int(dummy6[1].fieldFpwrl().value()))

        it.statusF(fvsfl=1)
        it.statusF(ffreql=1)       
        it.statusF(ftherml=1)
        it.statusF(fpwrl=1)  
        
        (dummy7,(dummy8, [c29, c30]))=it.temps()
        c29 = str(int(c29))
        c30 = str(int(c30))
        (dummy9,(dummy10,[c31,c32]))= it.currents()
        c31 = str(int(c31))
        c32 = str(int(c32))
        dummy12 = it.release()
        c33 = str(dummy12[1][1:])
        c33 = c33.strip("('")
        c33 = c33.strip("',)")
        (dummy13, c34) = it.pwr()
        c34 = str(int(c34))
        (dummy14, c35) = it.oop()
        c35 = str(c35)
        c36 = str(pwrmeter.getDisplayedPower())
        c37 = str(freqmeter.get_Frequency())
        return c0+","+c33+","+c1+","+c2+","+c3+","+c37+","+c4 + "," + c34+","+c35+ ","+c36+"," + c29 + ","\
               + c30 + "," + c31 + "," + c32+","+ c5 + ","\
               + c6 + "," + c7 + "," + c8 + "," + c9 + ","\
               + c10 + "," + c11 + "," + c12 + "," + c13 + ","\
               + c14 + "," + c15 + "," + c16 + "," + c17 + ","\
               + c18 + "," + c19 + "," + c20 + "," + c21 + ","\
               + c22 + "," + c23 + "," + c24 + "," + c25 + ","\
               + c26 + "," + c27 + "," + c28
    def clearalarm(self):
        STalarm = time.time()
        TLalarm = 0.0
        while TLalarm < 60:
            TLalarm = time.time()-STalarm
            time.sleep(3)
            print '.',
            sys.stdout.flush()
            dummy11 = it.statusW()
            try:
                flagalarm = int(dummy11[1].fieldAlm().value())
            except:
                raise'cannot receive it.statusW()'
            if not flagalarm:
                print 'alarm cleared'
                break
        if (not(TLalarm < 60)) & flagalarm:
            raise 'alarm no cleared'
        STfatal = time.time()
        TLfatal = 0.0
        while TLfatal < 60:
            TLfatal = time.time()-STfatal
            time.sleep(3)
            print '.',
            sys.stdout.flush()
            dummy11 = it.statusF()
            try:
                flagfatal = int(dummy11[1].fieldFatal().value())
            except:
                raise'cannot receive it.statusF()'
            if not flagfatal:
                print 'fatal cleared'
                break
        if (not(TLfatal < 60)) & flagfatal:
            raise 'fatal no cleared'