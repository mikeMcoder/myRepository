import time
import struct

def sleep(cnt):
    print('Wait %d sec ' % cnt)
    for i in range(cnt):    
        print('.'),
        sys.stdout.flush() 
        time.sleep(1)
    print('done')
  
#COM_PORT = input("Enter COM PORT #")
if len(sys.argv) < 2:
    COM_PORT = 1        # default, no argument
else:
    COM_PORT = sys.argv[1] 
print '\n\n\nCOM PORT = ', COM_PORT

if len(sys.argv) < 3:
    it.debugRS232(0)
else:
    it.debugRS232(sys.argv[2])

it.connect(COM_PORT,9600)

# Code to validate MSA commands on ITLA (reference MSA v1.2)

print 'NOP'
print it.nop()[1].data()
it.resena(sena=1)
print it.nop()[1].data()
it.resena(sena=0)
print it.nop()
print 'DevType'
print it.devTyp()
print 'Manufacturer'
print it.mfgr()
print 'Model'
print it.model()
print 'Serial Number'
print it.serNo()
print 'Manufacturing Date'
print it.mfgDate()
print 'Release'
print it.release()
print 'Release backwards compatibility'
print it.relBack()
print 'GenCfg()'
print it.genCfg()[1].data()
print it.channel()
print it.pwr()
it.channel(15)
it.pwr(835)
#it.genCfg(sdc=1)
print it.channel()
print it.pwr()
print it.genCfg()[1].data()
it.channel(1)
it.pwr(1600)
#it.genCfg(sdc=1)
print 'Baud rate test'
print it.ioCap()[1].data()
it.baudrate(19200)
print it.ioCap()[1].data()
it.baudrate(38400)
print it.ioCap()[1].data()
it.baudrate(57600)
print it.ioCap()[1].data()
it.baudrate(115200)
print it.ioCap()[1].data()

print 'MS switch test'
it.baudrate(9600)
print it.ioCap()[1].data()
it.ioCap(module_select_no_reset=0)
print it.ioCap()[1].data()
it.baudrate(19200)
print it.ioCap()[1].data()
test=input("press MS switch and enter a 1")
print it.ioCap()[1].data()
it.ioCap(module_select_no_reset=1)
print it.ioCap()[1].data()
test=input("press MS switch and enter a 1")
print it.ioCap()[1].data()
it.baudrate(57600)
#it.genCfg(sdc=1)
it.baudrate(115200)
print it.ioCap()[1].data()
test=input("press MS switch and enter a 1")
print it.ioCap()[1].data()
it.baudrate(9600)

#it.genCfg(sdc=1)
print 'extended addressing        MORE?'
print it.aeaEac()[1].data()
print it.eac()[1].data()
print 'last response'
print it.lstResp()[1].data()
print 'DLconfig                 NEED TO TEST'
print it.dlStatus()[1].data()
print 'statusF,statusW'
print it.statusF()[1].data()
print it.statusW()[1].data()
it.resena(sena=1)
print it.statusF()[1].data()
print it.statusW()[1].data()
sleep(30)
print it.statusF()[1].data()
print it.statusW()[1].data()
it.statusF(ftherml=1,fpwrl=1,ffreql=1)
print it.statusF()[1].data()
it.statusW(wvsfl=1,wpwrl=1,wfreql=1)
print it.statusW()[1].data()
print 'power thresholds'
print it.fPowTh()
print it.wPowTh()
it.fPowTh(900)
it.wPowTh(300)
print it.fPowTh()
print it.wPowTh()
print 'frequency thresholds'
print it.fFreqTh()
print it.wFreqTh()
#it.fFreqTh(60)
#it.wFreqTh(30)
print it.fFreqTh()
print it.wFreqTh()
print 'thermal thresholds'
print it.fThermTh()
print it.wThermTh()
#it.fThermTh(9000)
#it.wThermTh(3000)
print it.fThermTh()
print it.wThermTh()
print 'SRQ triggers              more work'
print 'fatal triggers     needs work'
print it.fatalT()[1].data()
print 'ALM triggers needs works'
print 'channel register'
print it.channel()
it.channel(4)
print it.lf()
it.channel(60)
print it.lf()
it.channel(96)
print it.lf()
print 'power setpoint'
pow=700
while pow<1600:
    it.pwr(pow)
    print pow,it.pwr()
    pow=pow+1
print 'reset enable'
it.resena(sena=1)
print it.resena()[1].data()
it.resena(sena=0)
print it.resena()[1].data()
it.resena(sena=1)
print it.resena()[1].data()
#it.resena(sr=1)
print it.resena()[1].data()
#it.resena(mr=1)
print it.resena()[1].data()
print 'MCB     needs work'
print 'gridspacing'
print it.grid()
it.grid(1)
it.channel(50)
print it.channel()
it.channel(51)
print it.channel()
it.grid(500)
print it.grid()
print 'fcf'
print it.fcf1()
it.fcf1(193)
print it.fcf1()
print it.fcf2()
it.fcf2(8500)
print it.fcf2()
print 'oop'
it.resena(sena=1)
sleep(20)
print it.pwr()
print it.oop()
it.pwr(1500)
sleep(5)
print it.oop()
it.pwr(1000)
sleep(5)
it.oop()
print 'Ctemp'
print it.ctemp()
print 'FTFR         needs implementation in sunshell'
#print it.ftfr()
print 'OPSL, OPSH'
print it.opsl()
print it.opsh()
print 'lfl, lfh'
print it.lfl()
print it.lfh()
print 'lgrid'
print it.lgrid()
print 'currents'
it.resena(sena=1)
sleep(30)
print it.currents()
print 'temperatures'
print it.temps()
# dithers
# tbtf warnings
print 'age threshold'
print 'laser age'
print it.age()
# FTF
it.disconnect()
print 'TEST DONE!'
