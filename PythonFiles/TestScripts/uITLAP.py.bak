#   this program determines the polarity of a TTx       Joe Lo 5/2004
#  add program to calibrate phaase of the waveform     Joe Lo..3/30/2005
#  for uITLA  Joe   1/2012

import math
import sys
import time
import types
import Scientific.Functions.LeastSquares as sfl
import TTM.TTM

lsfit = sfl.leastSquaresFit

t = None
cs = None
#clc = None
stc = None
ds = None
f1tc = None
f2tc = None

def setTTX(ttx):

    global t, cs, stc, scc, ds, f1c, f2c
    t=ttx
    cs=t.controlStage()
    #clc=cs.cavityLengthController()
    stc=cs.sledTemperatureController()
    scc=cs.sledCavityController()
    ds=t.domainStage().frame()
    f1tc=t.controlStage().filter1TemperatureController()
    f2tc=t.controlStage().filter2TemperatureController()


def run(SA=1, Tstart=60., Tstop=50.0, Tstep=0.2, TF1=69.0, TF2=75.0, dTF1F2=0.5, gmi=150.0, VA=1, TableFile = "c:\\scanner\\polarity.txt"):
    RImag_threshold=0.5
    datafile = open(TableFile, 'w')
    datafile.write('sled_T\t sled_T\t demod_R\t Filter1_T\t Filter2_T\t gmi\t demod_I\n')
    t.restore()
    t.modem().dictionary()['polarity']=1
    t.save()
    time.sleep(10)
    t.tuner().currentTuner().mask().tuner(0)
    t.tuner().currentTuner().frequency(0)
    t.sideModeBalancer().iteration(0)
    #cs.sledSlot(stc)
    #stc.target(Tstart)
    t.controlStage().mask().sledCurrent(0)
    t.controlStage().mask().siBlockTemperature(0)
    t.controlStage().filter1TemperatureController().target(TF1)
    t.controlStage().filter2TemperatureController().target(TF2)
    cs.mask().filter1Power(0)
    cs.mask().filter2Power(0)
    cs.mask().gainMediumCurrent(0)
    cs.frame().gainMediumCurrent(gmi)
    time.sleep(3)

    F1minusF2=0.0
    trynum=1

    while (trynum<=2):
        if (trynum>1):
            print 'SHIFT FILTER TEMPS'
            F1minusF2=dTF1F2
        print '---------------'
        print 'F1minusF2=',F1minusF2
        t.controlStage().filter1TemperatureController().target(TF1+F1minusF2/2.0)
        t.controlStage().filter2TemperatureController().target(TF2-F1minusF2/2.0)
        #stc.target(Tstart)
        t.controlStage().siBlockCavityController().target(Tstart)
        print 'start SiBlock.TEMPERATURE=', t.domainStage().frame().siBlockTemperature()
        time.sleep(2)
        t.sideModeBalancer().iteration(1000)
        while (t.sideModeBalancer().iteration() > 0):
            time.sleep(1)

        time.sleep(1)
        demod_array = []
        temp_array = []
        phase_array = []
        la_fdemodR=t.domainStage().frame().demodulationReal()
        la_fdemodI=t.domainStage().frame().demodulationImaginary()
        TSledCurrent = Tstart
        while (TSledCurrent >= Tstop):
            #stc.target(TSledCurrent)
            t.controlStage().siBlockCavityController().target(TSledCurrent)
            time.sleep(0.4)
            fgmi=t.domainStage().frame().gainMediumCurrent()
            ff1=t.domainStage().frame().filter1Temperature()
            ff2=t.domainStage().frame().filter2Temperature()
            fsiBt=t.domainStage().frame().siBlockTemperature()
            fdemodR=t.domainStage().frame().demodulationReal()
            fdemodI=t.domainStage().frame().demodulationImaginary()

            print( '%4.3f\t%4.3f\t%4.3f\t%4.3f\t%4.3f\t%4.3f\t%4.3f' %(TSledCurrent, fsiBt, fdemodR, ff1, ff2, fgmi, fdemodI) )
            datafile.write( '%4.3f\t%4.3f\t%4.3f\t%4.3f\t%4.3f\t%4.3f\t%4.3f\n' %(TSledCurrent, fsiBt, fdemodR, ff1, ff2, fgmi, fdemodI) )
            temp_array.append(TSledCurrent)
            demod_array.append(fdemodR)
            deltaR=fdemodR-la_fdemodR
            deltaI=fdemodI-la_fdemodI
            magRI=math.sqrt(deltaR**2+deltaI**2)
            if (magRI < RImag_threshold):
                phase_array.append( ([fdemodR],fdemodI) )
            la_fdemodR=fdemodR
            la_fdemodI=fdemodI
            TSledCurrent=TSledCurrent - Tstep
            
        direction_array = []
        i = 0
        
        last_index = len(demod_array) - 1
        print 'last_index=',last_index
        
        print 'direction_array:'
        while i < last_index:
            # set to 1 if positive. set to -1 if negative
            direction_array.append(2*((demod_array[i]-demod_array[i+1])>=0)-1)
            print direction_array[-1]
            i=i+1

        vl=len(direction_array)
        direction_sum=0
        for i in range(vl):
            direction_sum=direction_sum+direction_array[i]

        print 'direction_sum=',direction_sum
        datafile.write('direction_sum = %d\t' %(direction_sum))
        
        polarity=(2*(direction_sum>=0)-1)
        print 'polarity=',polarity
        datafile.write('polarity = %d\t' %(polarity))

        if abs(direction_sum)>10:
            trynum=999
            print 'POLARITY FOUND'
            datafile.write('POLARITY FOUND')
        else:
            trynum+=1
            print 'POLARITY INVALID'
            datafile.write('POLARITY INVALID')
        print 'trynum=',trynum

# start phase adjustment
    print 'phase calculation'
    datafile.write('\nphase calculation\n')
#        print phase_array
    parameterGuess = (0.1, 0.05)
    (bestFit1, residual1) = lsfit(Rotateeq, parameterGuess, phase_array)
    print bestFit1, residual1
    ##datafile.write('bestFit1[0] = %f\t' %(bestFit1[0]))
    ##datafile.write('bestFit1[1] = %f\t' %(bestFit1[1]))
    ##datafile.write('residual = %f\n' %(residual1))
    adangle=math.atan(bestFit1[0])*180./math.pi
    print 'angle adjust=', adangle
    ##datafile.write('angle adjust = %f\n' %(adangle))
    t.restore()
    wf=t.modem().waveform()
    wangle=wf[0]
    print 'waveform angle=', wangle
    datafile.write('waveform angle = %f\n' %(wangle))
    newangle=wangle-adangle
    print 'new angle=', newangle
    ##datafile.write('new angle = %f\n' %(newangle))
    ##t.modem().waveform(newangle, wf[1])

# read demod offset at gmi=15 mA
    cs.frame().gainMediumCurrent(15)
    time.sleep(1)
    fgmi=t.domainStage().frame().gainMediumCurrent()
    fdemodR=t.domainStage().frame().demodulationReal()
    fdemodI=t.domainStage().frame().demodulationImaginary()
    datafile.write('reading demod offset at under threshold current\n')
    datafile.write('gmi, demod_Real, demod_Img\n')
    datafile.write('%4.3f\t%4.3f\t%4.3f\n\n' %(fgmi, fdemodR, fdemodI))

    datafile.flush()
    if ((trynum==999) and (SA==1)):
        t.modem().dictionary()['polarity']=polarity
        ##t.modem().waveform(newangle, wf[1])
        print 'Saving polarity and not new angle to flash...'
        t.save()
        time.sleep(10)
# start phase verification
    if ((VA==1) and (SA==1)):
        t.tuner().currentTuner().mask().tuner(0)
        t.tuner().currentTuner().frequency(0)
        t.sideModeBalancer().iteration(0)
        #cs.sledSlot(stc)
        #stc.target(Tstart)
        t.controlStage().mask().sledCurrent(0)
        t.controlStage().mask().siBlockTemperature(0)
        t.controlStage().filter1TemperatureController().target(TF1+F1minusF2/2.0)
        t.controlStage().filter2TemperatureController().target(TF2-F1minusF2/2.0)
        cs.mask().filter1Power(0)
        cs.mask().filter2Power(0)
        cs.mask().gainMediumCurrent(0)
        cs.frame().gainMediumCurrent(gmi)
        time.sleep(5)
        t.sideModeBalancer().iteration(1000)
        while (t.sideModeBalancer().iteration() > 0):
            time.sleep(1)
#        ve_phase_array = []
        TSledCurrent = Tstart
        time.sleep(1.0)
        print 'phase verification start...'
        datafile.write('\nphase verification start\n')
        while (TSledCurrent >= (Tstart-4.5)):
            t.controlStage().siBlockCavityController().target(TSledCurrent)
            time.sleep(0.4)
            fgmi=t.domainStage().frame().gainMediumCurrent()
            ff1=t.domainStage().frame().filter1Temperature()
            ff2=t.domainStage().frame().filter2Temperature()
            fsiBt=t.domainStage().frame().siBlockTemperature()
            fdemodR=t.domainStage().frame().demodulationReal()
            fdemodI=t.domainStage().frame().demodulationImaginary()

            print( '%4.3f\t%4.3f\t%4.3f\t%4.3f\t%4.3f\t%4.3f\t%4.3f' %(TSledCurrent, fsiBt, fdemodR, ff1, ff2, fgmi, fdemodI) )
            datafile.write( '%4.3f\t%4.3f\t%4.3f\t%4.3f\t%4.3f\t%4.3f\t%4.3f\n' %(TSledCurrent, fsiBt, fdemodR, ff1, ff2, fgmi, fdemodI) )
#            ve_phase_array.append([fdemodR,fdemodI])
            TSledCurrent=TSledCurrent - Tstep
    datafile.close()

def Rotateeq(a,d):
    return (a[0]*d[0]+a[1])