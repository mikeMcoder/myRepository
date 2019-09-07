class genseq:
    def __init__(self):
        print 'genseq init'
        
    def maTH(self,paramL):
        [test_name,channelmode,channelmin,channelmax,channelfix,\
channelgap,channelcyc,channelseq,pwrmode,pwrmin,pwrmax,pwrfix,pwrgap,pwrcyc,\
pwrseq,samplingL,samplingP]=paramL
        channelseq = self.helperUI('channel',channelmode,channelfix,channelmin,channelmax,channelgap,channelseq)        
        pwrseq = self.helperUI('pwr',pwrmode,pwrfix,pwrmin,pwrmax,pwrgap,pwrseq)
        return([test_name,channelseq,channelcyc,pwrseq,pwrcyc,samplingL,samplingP])
    
    def helperUI(self,CorP,mode,fix,min,max,gap,seq):
        if mode == 0:
            seq=[fix]
            print '%sfix : %d'%(CorP,fix)
        elif mode == 1:
            seq = range(min,max,gap)    
            seq.extend(range(max,min,-gap))
            print '%sramp : %d to %d with gap %d'%(CorP,min,max,gap)
        elif mode == 2:
            seq = [min,max]
            print '%sjump : %d to %d'%(CorP,min,max)
        elif mode == 3:
            print '%sseq : %s'%(CorP,seq)
        else:
            raise 'input out of scope'
        return seq
