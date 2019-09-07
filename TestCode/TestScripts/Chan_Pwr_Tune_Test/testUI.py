import time

class testUI:
    def __init__(self):
        print 'testUI init'

    def startUI(self):
        test_name = 'default'
        
        try:test_name = input('test_name(put "" around):')
        except:pass
        print'testname:',test_name
        
        #channel
        channelmode = 0
        channelmin = 1
        channelmax = 92
        channelfix = channelmin
        channelgap = 1
        channelcyc = 1
        channelseq = []
        
        try:channelmode = input('channelmode(fix:0, ramp:1, jump:2, seq:3):')
        except:pass
        print'channelmode:',channelmode

        try:channelmin  = input('channelmin:')
        except:pass
        print'channelmin:',channelmin

        try:channelmax  = input('channelmax:')
        except:pass
        print'channelmax:',channelmax
        
        try:channelfix  = input('channelfix(%d-%d):'%(channelmin,channelmax))
        except:pass
        print'channelfix:',channelfix
        
        try:channelgap  = input('channelgap(s):')
        except:pass
        print'channelgap:',channelgap

        try:channelcyc  = input('channelcyc:')
        except:pass
        print'channelcyc:',channelcyc

        try:channelseq  = input('channelseq([,]):')
        except:pass
        print'channelseq:',channelseq

        #pwr
        pwrmode = 0
        (dummy16, pwrmin) = it.opsl()
        pwrmin = int(pwrmin)
        (dummy15, pwrmax) = it.opsh()
        pwrmax = int(pwrmax)
        pwrfix = pwrmax
        pwrgap = 1
        pwrcyc = 1
        pwrseq = []
        
        try:pwrmode = input('pwr(fix:0, ramp:1, jump:2, seq:3):')
        except:pass
        print'pwrmode:',pwrmode

        try:pwrmin  = input('pwrmin:')
        except:pass
        print'pwrmin:',pwrmin

        try:pwrmax  = input('pwrmax:')
        except:pass
        print'pwrmax:',pwrmax
        
        try:pwrfix  = input('pwrfix(%d-%d /100*db):'%(pwrmin,pwrmax))
        except:pass
        print'pwrfix:',pwrfix
        
        try:pwrgap  = input('pwrgap(s):')
        except:pass
        print'pwrgap:',pwrgap

        try:pwrcyc  = input('pwrcyc:')
        except:pass
        print'pwrcyc:',pwrcyc

        try:pwrseq  = input('pwrseq([,]):')
        except:pass
        print'pwrseq:',pwrseq

        samplingL = 600
        samplingP = 1

        try:samplingL = input('samplingL(s):')
        except:pass
        print'samplingL:',samplingL

        try:samplingP= input('samplingP(s):')
        except:pass
        print'samplingP:',samplingP

        return ([test_name,channelmode,channelmin,channelmax,channelfix,\
channelgap,channelcyc,channelseq,pwrmode,pwrmin,pwrmax,pwrfix,pwrgap,pwrcyc,\
pwrseq,samplingL,samplingP]) 

