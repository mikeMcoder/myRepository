'''
NeoPhotonics CONFIDENTIAL
Copyright 2003-2015 NeoPhotonics Corporation All Rights Reserved.

The source code contained or described herein and all documents related to
the source code ("Material") are owned by NeoPhotonics Corporation or its
suppliers or licensors. Title to the Material remains with NeoPhotonics Corporation
or its suppliers and licensors. The Material may contain trade secrets and
proprietary and confidential information of NeoPhotonics Corporation and its
suppliers and licensors, and is protected by worldwide copyright and trade
secret laws and treaty provisions. No part of the Material may be used, copied,
reproduced, modified, published, uploaded, posted, transmitted, distributed,
or disclosed in any way without NeoPhotonics's prior express written permission.
No license under any patent, copyright, trade secret or other intellectual
property right is granted to or conferred upon you by disclosure or delivery
of the Materials, either expressly, by implication, inducement, estoppel or
otherwise. Any license under such intellectual property rights must be express
and approved by NeoPhotonics in writing.

Include any supplier copyright notices as supplier requires NeoPhotonics to use.

Include supplier trademarks or logos as supplier requires NeoPhotonics to use,
preceded by an asterisk. An asterisked footnote can be added as follows:
*Third Party trademarks are the property of their respective owners.

Unless otherwise agreed by NeoPhotonics in writing, you may not remove or alter this
notice or any other notice embedded in Materials by NeoPhotonics or NeoPhotonics's
suppliers or licensors in any way.
'''
import exceptions
import os
import sys
import time
import types
import serial
import AmbientCompensator
import Control
import Dictionary
import Domain
import Discrete
import FilterDither
import PyTTXTalk
import Sample
import System
import Utility
import Tuner
import SideModeBalancer
import MODEM
import Logger
import Health
import os
if (os.name != 'posix'):
    import win32ui

RX_TIMEOUT_DEFAULT = 0.05

class TTM:

    def __init__(self, it_object = None):
        self._firmware_version = None
        self._need_restore = 1
        sys.path.append('..\\')
        if (os.name == 'posix'):
            self._portprefix = '/dev/ttyS'
        else:
            self._portprefix = 'com'
        if it_object is None:
            import ITLA.ITLA
            self.it = ITLA.ITLA.ITLA(self)
        else:
            self.it = it_object
        self.type = 0
        self.laserType = 0
        self._link = None

    def __repr__(self):
        try:
            s =  'Description        : TTM interface object.\n\n'
            s += 'Firmware Version   : %s\n' % (self.firmwareVersion(),)
            s += 'Electronics Version: %s' % (self.electronicsVersion(),)
            return(s)
        except TypeError:
            return 't object'

    def latestSupportedFirmwareVersion(self):
        return System.version()
               
    #def __open_rs232_port(self, rs232_port = 1, rs232_baud = 115200):
    def _open_rs232_port(self, rs232_port = 1, rs232_baud = 9600):
        self._port = rs232_port
        self._baud = rs232_baud
        try:
            #
            #for transmission of KV file from Python to Juno,
            #we need the serial port to wait more when the transmit buffer is becoming full
            #
#            if (os.name != 'posix'):
#                self._link = serial.Serial(rs232_port - 1, rs232_baud, timeout = RX_TIMEOUT_DEFAULT)
#            else:
            self._link = serial.Serial(self._portprefix + str(rs232_port), rs232_baud, timeout = RX_TIMEOUT_DEFAULT)
        except:
            print '# Error in open RS232, COM Port #', rs232_port, 'could not be opened. Verify if another application may have opened this serial port.'
            print '-'*40
            import traceback
            traceback.print_exc()
            print '-'*40
            #Utility.ERROR_CODES[code]
            return -399
        PyTTXTalk.set_rs232_com_port(rs232_port, rs232_baud, self._link)
        
        return 0

    def save_handle(self, it_param):
        PyTTXTalk.save_handle(it_param)
        self._system = System.System()

    # for uitla only
    def save_it_obj(self, it_param):
        self.it = it_param

    def tmode(self, kvdict=None, mode=1, nano=None):
        if(mode != 1):
            self._system.send_code_abort_PicassoTalk()
            return 
        ###
        (self.laserType, firmware_version) = self._system.detectMode()      # leaves in picasso tmode
        if (self.laserType == 0):
            print ('Laser not detected')
            return
        self._firmware_version = firmware_version
        if nano is None:
            if self.it.getLaserType() == 5:  # FIXME: why is this None?
                Nano = True
            else:
                Nano = False
        else:
            Nano = nano
        if Nano and (kvdict == None):       # NANO
            print 'Error: Nano detected, kvdict parameter is needed!'
            return

        dm = Dictionary.DictionaryManager(kvdict)
        self._dictionary_manager = dm      

        if Nano == False:       # not NANO
            if not dm.shelf(System.bridgePath(firmware_version)):
                print "Unable to find bridge files in " + System.bridgePath(firmware_version)
                print ('Firmware version [%s] not supported.' % (firmware_version))
                return
            self.it.setupFromTMode(True)
        
        self._root_dictionary = dm.rootDictionary()
        d = Dictionary.Dictionary()

        if Nano == False:       # not NANO
            # Give it a valid memory object
            d.memory(dm.dictionary('SYSTEM_DICTIONARY').memory())
            d.addEntry('system', dm.dictionary('SYSTEM_DICTIONARY'))

            # Some firmware version may not have this dictionary
            try:
                d.addEntry('ipc_defaults', dm.dictionary('IPC_DICTIONARY'))
            except:
                pass
        else:
            self.type = 2;
        self._system.dictionary(d)
        self._sample_stage = Sample.SampleStage(nano = nano)
        self._domain_stage = Domain.DomainStage(self.type)
        self._domain_stage.dictionary(dm.dictionary('DOMAIN_DICTIONARY'))
        self._control_stage = Control.ControlStage(dm)
        self._tuner = Tuner.TunerManager(self, dm, Nano)
        self._discrete_stage = Discrete.DiscreteStage()
        self._discrete_stage.dictionary(dm.dictionary('DISCRETE_DICTIONARY'))
        self._side_mode_balancer = SideModeBalancer.SideModeBalancer()
        self._side_mode_balancer.dictionary(dm.dictionary('SIDE_MODE_BALANCER_DICTIONARY'))
        self._ambient_compensator = AmbientCompensator.AmbientCompensator()
        self._ambient_compensator.dictionary(dm.dictionary('AMBIENT_COMPENSATOR_DICTIONARY'))
        self._modem = MODEM.MODEM()
        self._modem.dictionary(dm.dictionary('MODEM_DICTIONARY'))
        self._health = Health.Health()
        self._health.dictionary(dm.dictionary('HEALTH_DICTIONARY'))
        self.shortcut_definition()
        #pb self._dictionary_manager.restore()
        self._need_restore = 1
        self._system.picassoMode(True)
        return 
        
    def debugRS232(self, debug = None):
        return PyTTXTalk.debugRS232(debug)

    def laser(self, debug = None):
        return PyTTXTalk.laser(debug)

    def getlaserType(self):
        return self.laserType

    def connect(self, port_param = 1, rs232_baud_param = 9600, **kwargs):
        # should not get here.  User tried to connect before lsr was created

        if '..' not in sys.path:
            sys.path.append("..")
        import LSR.LSRcontrol

        if sys.modules['__main__'].__dict__.get('it',None) is None: 
            lsr = LSR.LSRcontrol.LSRcontrol(it=sys.modules['__main__'].__dict__.get('it',None), t=self)
            sys.modules['__main__'].__dict__['lsr']   = lsr
        else:
            lsr = LSR.LSRcontrol.LSRcontrol(t=self)
            sys.modules['__main__'].__dict__['lsr']   = lsr
            sys.modules['__main__'].__dict__['it']   = lsr.it
            self.it = lsr.it
        
        retval = lsr.connect(port=port_param, baud=rs232_baud_param,**kwargs)
        lsr.it.save_handle(lsr._ttyhandle)
        self.save_handle(lsr._ttyhandle)
        if lsr.it.getLaserType() != 5:
            self.tmode()
        return retval   
       
    def _connect(self, port_param = 1, rs232_baud_param = 9600, skip = False, **kwargs):
        code = 0
        if(skip == False):
            self.disconnect()
            self.it.disconnect()   # disconnect it serial port
            if rs232_baud_param == 0:
                baud, success = self.it.connect(port_param, 0)
                print baud, success
                if success != 'Connected':
                    return (baud, success)
                rs232_baud_param = baud
                self.it.disconnect()   # disconnect it serial port
            code = self._open_rs232_port(port_param, rs232_baud_param)
            if (code != 0):
                return(code, Utility.ERROR_CODES[code])
            # Sucessfully connected.
        self._system = System.System()
        #self._logger = Logger.Logger()     #pb may be commented out
        ###

        (result_detect_mode, firmware_version) = self._system.detectMode()
        if (result_detect_mode == 0):
            code = -501
            return (code, 'Laser not detected')
        ###
        self._firmware_version = firmware_version
        #self._logger.bridgeFile(System.bridgePath(firmware_version))   #pb may be commented out

        dm = Dictionary.DictionaryManager()
        self._dictionary_manager = dm      

        if not dm.shelf(System.bridgePath(firmware_version)):
            print "Unable to find bridge files in " + System.bridgePath(firmware_version)
            code = -500
            return (code, 'Firmware version [%s] not supported.' % (firmware_version))

        self.it.setupFromTMode(True)
        
        self._root_dictionary = dm.rootDictionary()
        d = Dictionary.Dictionary()

        # Give it a valid memory object
        d.memory(dm.dictionary('SYSTEM_DICTIONARY').memory())
        d.addEntry('system', dm.dictionary('SYSTEM_DICTIONARY'))

        # Some firmware version may not have this dictionary
        try:
            d.addEntry('ipc_defaults', dm.dictionary('IPC_DICTIONARY'))
        except:
            pass
        
        if self.it.getLaserType() == 5:  # FIXME: why is this None?
            self.type = 2
        else:
            self.type = 0
        self._system.dictionary(d)
        self._sample_stage = Sample.SampleStage()
        self._domain_stage = Domain.DomainStage(self.type)
        self._domain_stage.dictionary(dm.dictionary('DOMAIN_DICTIONARY'))
        self._control_stage = Control.ControlStage(dm)
        self._tuner = Tuner.TunerManager(self, dm)
        self._discrete_stage = Discrete.DiscreteStage()
        self._discrete_stage.dictionary(dm.dictionary('DISCRETE_DICTIONARY'))
        self._side_mode_balancer = SideModeBalancer.SideModeBalancer()
        self._side_mode_balancer.dictionary(dm.dictionary('SIDE_MODE_BALANCER_DICTIONARY'))
        self._ambient_compensator = AmbientCompensator.AmbientCompensator()
        self._ambient_compensator.dictionary(dm.dictionary('AMBIENT_COMPENSATOR_DICTIONARY'))
        self._modem = MODEM.MODEM()
        self._modem.dictionary(dm.dictionary('MODEM_DICTIONARY'))
        self._health = Health.Health()
        self._health.dictionary(dm.dictionary('HEALTH_DICTIONARY'))
        self.shortcut_definition()
        #pb self._dictionary_manager.restore()
        self._need_restore = 1
        return (code, '%s %s' % (Utility.ERROR_CODES[code], firmware_version))

    def dictionary(self): return(self._system.dictionary())

    def electronicsVersion(self):
        try:
            return self.it._hwname
        except:
            return('UNKNOWN')

    def firmwareVersion(self):
        return self._firmware_version

    def help(self, object): print(object.__doc__)

    def sampleStage(self): return(self._sample_stage)

    def domainStage(self): return(self._domain_stage)

    def controlStage(self): return(self._control_stage)

    def discreteStage(self): return(self._discrete_stage)

    def health(self): return (self._health)
    def tuner(self): return(self._tuner)

    def sideModeBalancer(self): return(self._side_mode_balancer)

    def ambientCompensator(self): return(self._ambient_compensator)

    def system(self): return(self._system)
    
    def logger(self): return(self._logger)
    
    def modem(self): return(self._modem)
    
    def dictionaryManager(self): return(self._dictionary_manager)
    
    def _restore(self, source = 'TTM', bin = None, autoresponse = False):

        if ('TTM'.startswith(source.upper())):

            if (bin != None):
                raise 'Error: Bin must be specified as None.'

            print 'Retrieving kv file from uITLA',
            sys.stdout.flush() 
            time.sleep(0.001)       # allow time for printing              
            self._dictionary_manager.restore()
            self._need_restore = 0
            return

        if ('FILE'.startswith(source.upper())):

            if (type(bin) != types.StringType):

                raise 'Error: Bin must be specified as a string.'

            if (os.path.exists(bin) == False):

                raise 'Error: File does not exist.'

            self._need_restore = 0
            return(self._dictionary_manager.restore(bin))

    def _save(self, destination = 'TTM', bin = None, autoresponse = False, \
             verify = False, verify_retry = 0):
        if self._need_restore == 1:
            print '\'Unable to Save!, need to restore first'
            return
        self.actuatoroff()
        if ('TTM'.startswith(destination.upper())):

            if (bin != None):
                raise 'Error: Bin must be specified as None when saving to the TTM'
            print 'Saving kv file to uITLA',
            sys.stdout.flush() 
            time.sleep(0.001)       # allow time for printing              
            self._dictionary_manager.save()
            self._system.reset()
            self.actuatoron()       # manufacturing kas the actuator off in kv file
            return

        if ('FILE'.startswith(destination.upper())):

            if (type(bin) != types.StringType):

                raise 'Error: Bin must be specified as a string.'

            # If file exists, ask if user wants to over write.
            ANSWER_LIST = ['y', 'yes', 'n', 'no']
            answer = ''

            if (os.path.isfile(bin)):

                while(answer.lower() not in ANSWER_LIST):

                    try:

                        answer = Utility.query('This file exists. Overwrite?',
                                               'Y',
                                               autoresponse)

                    except KeyboardInterrupt:

                        answer = 'n'

                if (answer[0].lower() == 'n'):

                    sys.stdout.write('Save task cancelled.\n')
                    return
            self.actuatoron()
            return(self._dictionary_manager.save(bin))

        raise 'Error: \'%s\' is not a valid source.' % (destination)
        
    def shortcut_definition(self):
        'shortcut used by optical engineers'

        try:
            sys.modules['__main__'].__dict__['c']   = self.controlStage().frame()
            sys.modules['__main__'].__dict__['d']   = self.discreteStage().frame()
            sys.modules['__main__'].__dict__['o']   = self.domainStage().frame()
            sys.modules['__main__'].__dict__['s']   = self.sampleStage().frame()
            #sys.modules['__main__'].__dict__['gc']  = self.controlStage().frame().gainMediumCurrent
            #sys.modules['__main__'].__dict__['sb']  = self.controlStage().siBlockController().target
            #sys.modules['__main__'].__dict__['p1']  = self.controlStage().frame().mzmPhase1
            #sys.modules['__main__'].__dict__['p2']  = self.controlStage().frame().mzmPhase2
            #sys.modules['__main__'].__dict__['f1']  = self.controlStage().filter1TemperatureController().target
            #sys.modules['__main__'].__dict__['f2']  = self.controlStage().filter2TemperatureController().target
            #sys.modules['__main__'].__dict__['sl']  = self.controlStage().sledTemperatureController().target
            #sys.modules['__main__'].__dict__['m1']  = self.controlStage().frame().mzmBias1
            #sys.modules['__main__'].__dict__['m2']  = self.controlStage().frame().mzmBias2
            #sys.modules['__main__'].__dict__['amp'] = self.controlStage().frame().mzmDriverAmplitude
            #sys.modules['__main__'].__dict__['xp']  = self.controlStage().frame().mzmDriverCrossPoint
            #sys.modules['__main__'].__dict__['t2']  = self.controlStage().Tec2TemperatureController().target
            #sys.modules['__main__'].__dict__['lg']  = self.runlogger()
            #sys.modules['__main__'].__dict__['l']  = self._logger
            #print 'shortcut defined : c, d, o, s, gc, sb, p1, p2, f1, f2, sl, m1, m2, amp, xp, t2'
            print 'shortcut defined : c, d, o, s (control, discrete, domain, sample)'
        except:
            import traceback
            print '-'*40
            traceback.print_exc()
            print '-'*40

    def off(self):
        self._tuner.powerTuner().coldStart()

    def reset(self):
        self._system.reset()
               
    def switch_picasso(self): 
        self._system.send_code_switch_PicassoTalk()
        
    def switch_MSA(self): 
        self._system.send_code_abort_PicassoTalk()
                
    def actuatoron(self):
        self._system.actuatoron()    

    def actuatoroff(self):
        self._system.actuatoroff()

    def it_command(self, cmd = 0x30210000):     # cmd = it.statusW()
        self._system.it_command(cmd)
  
    def write(self, cmd):
        cmdNum=0
        for c in cmd:
            cmdNum = (cmdNum<<8) | ord(c)
        self.x = self._system.it_command(cmdNum)

    def read(self, cmd):
        ret=''
        c =self.x
        for i in range (4):
            v = c & 0xff
            ret = chr(v)+ret
            c = c / 256
        return ret

    def flushInput(self):
        pass

    def close(self):
        pass
