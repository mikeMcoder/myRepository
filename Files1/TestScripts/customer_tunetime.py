import time

newTime = 0
freqHi  = 96
freqLo  = 1
pend    = 0
alm     = 0
numFreq = freqHi - freqLo
COM_PORT = 1
t1 = 0
t2 = 0
statusF = 0


def tuneChannel(chan):
    time.sleep(1)
    it.channel(chan)
    startTuneTime = time.time()
    time.sleep(1)
    #warn = it.statusW()
    #wPow = warn[1].fieldWpwr()
    #wFreq = warn[1].fieldWfreq()
    nop = it.nop()
    pend = int(nop[1].fieldPending().value())
    statusF=it.statusF()
    alm = int(statusF[1].fieldAlm().value())
    #print pend
    while(pend == 1):
        #warn = it.statusW()
        #wPow = warn[1].fieldWpwr()
        #wFreq = warn[1].fieldWfreq()        
        nop = it.nop()
        pend = int(nop[1].fieldPending().value())
        statusF=it.statusF()
        alm = int(statusF[1].fieldAlm().value())
        #print pend
        #print pend, alm
        #print it.nop()
    
    t1 = time.time()- startTuneTime

    statusF=it.statusF()
    alm = int(statusF[1].fieldAlm().value())
    while(alm == 1):
        statusF=it.statusF()
        alm = int(statusF[1].fieldAlm().value())
        
    t2 = time.time()-startTuneTime
        
    print chan, t1, t2
    return(1)

##################################################
## Start Code
##################################################
print 'Custumer Tune Time Test  -- Version 2.0 --'
it.connect(COM_PORT)
print it.release()
print it.release()
#print numFreq
it.resena(sena=1)
time.sleep(1)
#print it.channel()

for i in range(numFreq):
    if(i%2 == 0):
        tuneChannel(freqHi)
        freqHi = freqHi - 1
    else:   
        tuneChannel(freqLo)
        freqLo = freqLo + 1
        
it.resena(sena=0)
it.disconnect()        
    


