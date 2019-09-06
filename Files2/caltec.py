#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 14:16:14 2018

@author: mark
"""

import sys
import os
import time
import numpy as np
import pandas as pd

os.chdir('/home/mark/Sundial/Python')

sys.path.append(os.path.abspath('.'))


if sys.platform == 'cygwin':
    # for cygwin, use the packages installed from the windows installation of python
    sys.path.append('/cygdrive/c/Python27/Lib/site-packages/')


import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
t.save_it_obj(it)

t.connect('/dev/ttyUSB4',115200)

DACMIDPOINT=0x7FFF
REJECTIONTHRESHOLD = 0.2 # remove points with current more than this magnitude.  Timing bug? causes spikes...
DELTA_DAC = 1

R46=0.03


if not hasattr(it,'_gettime'):
    it._gettime = time.clock

it.setpassword()

#shut down heaters
t.discreteStage().mask().filter1(1)
t.discreteStage().mask().filter2(1)
t.discreteStage().mask().siBlock(1)
t.discreteStage().frame().filter1(0)
t.discreteStage().frame().filter2(0)
t.discreteStage().frame().siBlock(0)


datalist=[]


#for deltaT in [0.0, +30.0, -30.0]: # can't do this, as TEC ramp is limited
for deltaT in [0.0]:
    
    snapshot = it.readx99()    

    t.discreteStage().mask().tec(0)
    
    while 1:
        t.controlStage().sledTemperatureController().target(snapshot.caseT + deltaT)
        time.sleep(1)
        snapshot = it.readx99()
        print snapshot.caseT, snapshot.sled_temperature
        if snapshot.sledlocked:
            break
    
    t.discreteStage().mask().tec(1)
    t.discreteStage().frame().tec(DACMIDPOINT)     
        
    time.sleep(2)

    starttime = it._gettime()
    
    for iternum in range(50):

        if iternum % 10 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()

 
        for dacoffset in [ -DELTA_DAC + 1, +DELTA_DAC]:
        
            t.discreteStage().mask().tec(1)
            t.discreteStage().frame().tec(DACMIDPOINT + dacoffset)
            
            time.sleep(0.02)
            
            snapshot = it.readx99()
 #           samplesstage = t.sampleStage().frame()
            snapshot.time = it._gettime() - starttime
            snapshot.tecdac = DACMIDPOINT + dacoffset
            snapshot.dacoffset = dacoffset
            snapshot.deltaT = deltaT
            snapshot.iternum = iternum
 #           snapshot.__dict__.update({k: v for k, v in zip(samplesstage.labels(), samplesstage.elements())})
            datalist.append(snapshot.__dict__)
 
    
    t.discreteStage().frame().tec(DACMIDPOINT)
    t.discreteStage().mask().tec(0)

t.controlStage().sledTemperatureController().target(50.0)


dat = pd.DataFrame(datalist)
grouped = dat.groupby('dacoffset')

dat['sled_current'].loc[dat['sled_current'].abs() > REJECTIONTHRESHOLD ] = np.nan

dat.groupby('dacoffset').plot(x='time',y='sled_current',kind='scatter')

offsets = dat.groupby('dacoffset')['sled_current'].mean()

offset = offsets[1] - offsets[0]  # maybe should be just offsets[1], since offsets[0] ought to be zero...

print 'Offset', offset

t.kv.kvdict['DOMAIN_DICTIONARY']['vtec_N1_coeff'] *= 1.0 - offset * R46 / 3.3   # check if this is the right way around

#t.kv.kvdict['DOMAIN_DICTIONARY']['vtec_N2_coeff'] *= 1.0 + offset * R46 / 3.3   # might be this way around...


t.save()


