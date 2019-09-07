import sys
import os
import time

import os
import sys
sys.path.append(os.path.abspath('.'))

import TTM.TTM
t = TTM.TTM.TTM()
import ITLA.ITLA
it = ITLA.ITLA.ITLA(t)
import TTM.Logger as l
t.save_it_obj(it)
print 'Instantiated a TTX interface as t, ITLA as it.'


port = 3
target = 195.7
pollLimit = 60.0
t = 0





t.tuner().currentTuner().mask().tuner(0)
t.tuner().currentTuner().frequency(target)
start = time.time()
dur = time.time()-start
print 'FREQ','F1','F2','GMI','SIBLOCK','DEMODR'
while dur < pollLimit:
    print t.tuner().currentTuner().frequency(),o.filter1Temperature(),o.filter2Temperature,o.gainMediumCurrent(),o.siBlockTemperature(),o.demodulationReal()
    dur = time.time()-start

t.tuner().currentTuner().currentTarget(0)
for i in range(20):
    print o.filter1Temperature(),o.filter2Temperature,o.gainMediumCurrent(),o.siBlockTemperature(),o.demodulationReal()

    
