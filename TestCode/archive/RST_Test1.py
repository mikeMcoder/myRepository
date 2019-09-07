#print 'hello?'
import time
COM = 4


t.disconnect()
it.connect(COM)
print it.release()
print it.release()
print it.release()
print it.release()
print it.release()
print it.release()

it.resena(mr=1)
time.sleep(1)
it.resena(sena=1)

it.disconnect()
t.connect(COM)
time.sleep(20)

for i in range(20):
    print t.domainStage().frame().sledTemperature(),t.discreteStage().frame().tec(),t.domainStage().frame().gainMediumCurrent(),t.discreteStage().frame().gainMedium(),t.discreteStage().frame().filter1(),t.discreteStage().frame().filter2(),t.domainStage().frame().siBlockTemperature(),t.discreteStage().frame().siBlock()

t.reset()

for i in range(200):
    print t.domainStage().frame().sledTemperature(),t.discreteStage().frame().tec(),t.domainStage().frame().gainMediumCurrent(),t.discreteStage().frame().gainMedium(),t.discreteStage().frame().filter1(),t.discreteStage().frame().filter2(),t.domainStage().frame().siBlockTemperature(),t.discreteStage().frame().siBlock()
