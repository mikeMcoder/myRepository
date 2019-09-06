'''
NeoPhotonics CONFIDENTIAL
Copyright 2008 NeoPhotonics Corporation All Rights Reserved.

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
import Frame
import Mask
from Utility import *

MODULE_INDEX = 3

METHOD_INDICES = {'frameElementF32':0,
                  'maskElement'    :1,
                  'isLocked'       :2,
                  'target'         :3,
                  'error'          :4,
                  'variance'       :5,
                  'mode'           :6,
                  'integratorValue':7,
                  'targetOffset'   :8,
                  'slot'           :9}
                  ###'siBlockError'   :10}

ELEMENT_DATA = (('FILTER1_POWER',           'W'),
                ('FILTER2_POWER',           'W'),
                ('SI_BLOCK_TEMPERATURE',    'C'),
                ('GAIN_MEDIUM_CURRENT',     'mA'),
                ('SLED_CURRENT',            'A'),
                ('SBSS_GAIN',               'ABU'),
                )

ELEMENT_PROPERTIES = []

for index in range(len(ELEMENT_DATA)):

    data = ELEMENT_DATA[index]
    
    ELEMENT_PROPERTIES.append({'index':index,
                               'label':data[0],
                               'units':data[1],
                               'type' :'F32'})

CONTROLLER_IDS = {'SLED'                :(0,'Sled controller'),
                  'FILTER1'             :(1,'Filter 1 controller'),
                  'FILTER2'             :(2,'Filter 2 controller'),
                  'SIBLOCK_TEMPERATURE' :(3,'SiBlock temperature controller'),
                  'SIBLOCK_CAVITY'      :(4,'SiBlock cavity contoller'),
                  'SLED_CAVITY'         :(5,'Sled Cavity contoller')}

SLOT_IDS = {'SLED'   :0,
            'FILTER1':1,
            'FILTER2':2,
            'SIBLOCK':3}

PROPERTIES = {'ELEMENT_PROPERTIES':ELEMENT_PROPERTIES,
              'CONTROLLER_IDS'    :CONTROLLER_IDS,
              'SLOT_IDS'          :SLOT_IDS}
        
class ControlStage:

    def __init__(self, dictionary_manager):
        
        self.__module_index = MODULE_INDEX
        
        self.__method_indices = METHOD_INDICES

        self.__frame = ControlFrame()
        self.__mask = ControlMask()

        self.__controller_ids = PROPERTIES['CONTROLLER_IDS']
        self.__slot_ids = PROPERTIES['SLOT_IDS']
            
        self.__sled_temperature_controller =\
            DualController(self.__module_index,
                           self.__method_indices,
                           self.__controller_ids['SLED'],
                           dictionary_manager.dictionary(\
                           'SLED_TEMPERATURE_CONTROLLER_DICTIONARY'))

        self.__filter1_temperature_controller =\
            DualController(self.__module_index,
                             self.__method_indices,
                             self.__controller_ids['FILTER1'],
                             dictionary_manager.dictionary(\
                             'FILTER1_TEMPERATURE_CONTROLLER_DICTIONARY'))

        self.__filter2_temperature_controller =\
            DualController(self.__module_index,
                             self.__method_indices,
                             self.__controller_ids['FILTER2'],
                             dictionary_manager.dictionary(\
                             'FILTER2_TEMPERATURE_CONTROLLER_DICTIONARY'))

        self.__siblock_temperature_controller =\
            DualController(self.__module_index,
                           self.__method_indices,
                           self.__controller_ids['SIBLOCK_TEMPERATURE'],
                           dictionary_manager.dictionary(\
                           'SI_BLOCK_TEMPERATURE_CONTROLLER_DICTIONARY'))

        self.__siblock_cavity_controller =\
            DualController(self.__module_index,
                           self.__method_indices,
                           self.__controller_ids['SIBLOCK_CAVITY'],
                           dictionary_manager.dictionary(\
                           'SI_BLOCK_CONTROLLER_DICTIONARY'))

        self.__sled_cavity_controller =\
            DualController(self.__module_index,
                           self.__method_indices,
                           self.__controller_ids['SLED_CAVITY'],
                           dictionary_manager.dictionary(\
                           'SI_BLOCK_CONTROLLER_DICTIONARY'))

    def frame(self):
        
        'Returns ControlFrame.'
        return(self.__frame)

    def mask(self):
        
        'Returns ControlMask.'
        return(self.__mask)

    def sledTemperatureController(self):
        
        'Returns a DualController controller'
        return(self.__sled_temperature_controller)

    def sledCavityController(self):
        
        'Returns a DualController controller'
        return(self.__sled_cavity_controller)
    
    def filter1TemperatureController(self):
        
        'Returns an AnalogController controller'
        return(self.__filter1_temperature_controller)
        
    def filter2TemperatureController(self):
        
        'Returns an AnalogController controller'
        return(self.__filter2_temperature_controller)

    def siBlockTemperatureController(self):
        
        'Returns a SiBlock temperature controller'
        return(self.__siblock_temperature_controller)

    def siBlockCavityController(self):
        
        'Returns a SiBlock temperature controller'
        return(self.__siblock_cavity_controller)

    def siBlockSlot(self, controller = None):
        
        'Sets/gets controller for siblock control.'
        newOperation(self.__module_index, self.__method_indices['slot'])
        PyTTXTalk.pushU8(self.__slot_ids['SIBLOCK'])

        id = self.__controllerIDLookup__(controller)        

        if (id != None):
            PyTTXTalk.pushU8(id);

        sendPacket(1);

        if (id == None):
            return(self.__controllerLookup__(PyTTXTalk.popU8()))            

    def sledSlot(self, controller = None):
        
        'Sets/gets controller for siblock control.'
        newOperation(self.__module_index, self.__method_indices['slot'])
        PyTTXTalk.pushU8(self.__slot_ids['SLED'])

        id = self.__controllerIDLookup__(controller)        

        if (id != None):
            PyTTXTalk.pushU8(id);

        sendPacket(1);

        if (id == None):
            return(self.__controllerLookup__(PyTTXTalk.popU8()))            

    def __controllerIDLookup__(self, controller):
        
        ' Returns controller ID based on controller. '
        data = {self.sledTemperatureController().id() : self.__controller_ids['SLED'][0],
                self.filter1TemperatureController().id() : self.__controller_ids['FILTER1'][0],
                self.filter2TemperatureController().id() : self.__controller_ids['FILTER2'][0],
                self.siBlockTemperatureController().id() : self.__controller_ids['SIBLOCK_TEMPERATURE'][0],
                self.siBlockCavityController().id() : self.__controller_ids['SIBLOCK_CAVITY'][0],
                self.sledCavityController().id() : self.__controller_ids['SLED_CAVITY'][0]}

        if (controller):
            if (data.has_key(controller.id())):
                return(data[controller.id()])
            
        return(None)

    def __controllerLookup__(self, id):
        
        ' Returns controller ID based on controller. '
        data = {self.__controller_ids['SLED'][0] : self.__sled_temperature_controller,
                self.__controller_ids['FILTER1'][0] : self.__filter1_temperature_controller,
                self.__controller_ids['FILTER2'][0] : self.__filter2_temperature_controller,
                self.__controller_ids['SIBLOCK_TEMPERATURE'][0] : self.__siblock_temperature_controller,
                self.__controller_ids['SIBLOCK_CAVITY'][0] : self.__siblock_cavity_controller,
                self.__controller_ids['SLED_CAVITY'][0] : self.__sled_cavity_controller}

        if (data.has_key(id)): return(data[id])

        return(None)    

    def labels(self):
        data = []

        label = []
        for i in self.__sled_temperature_controller.labels():
            label.append('SledTemperatureController.' + i)
        data.extend(label)

        label = []
        for i in self.__sled_cavity_controller.labels():
            label.append('SledCavityController.' + i)
        data.extend(label)

        label = []
        for i in self.__filter1_temperature_controller.labels():
            label.append('Filter1TemperatureController.' + i)
        data.extend(label)

        label = []
        for i in self.__filter2_temperature_controller.labels():
            label.append('Filter2TemperatureController.' + i)
        data.extend(label)

        label = []
        for i in self.__siblock_temperature_controller.labels():
            label.append('SiblockTemperatureController.' + i)
        data.extend(label)
        
        label = []
        for i in self.__siblock_cavity_controller.labels():
            label.append('SiblockCavityController.' + i)
        data.extend(label)  

        return data
   
    def elements(self):
        data = []
        data.extend(self.__sled_temperature_controller.elements())
        data.extend(self.__sled_cavity_controller.elements())
        data.extend(self.__filter1_temperature_controller.elements())
        data.extend(self.__filter2_temperature_controller.elements())
        data.extend(self.__siblock_temperature_controller.elements())
        data.extend(self.__siblock_cavity_controller.elements())

        return data

class ControlFrame(Frame.Frame):

    def __init__(self):

        Frame.Frame.__init__(self,
                             'Controller frame.',
                             PROPERTIES['ELEMENT_PROPERTIES'],
                             MODULE_INDEX,
                             METHOD_INDICES)

class ControlMask(Mask.Mask):

    def __init__(self):

        Mask.Mask.__init__(self,
                           'Controller mask.',
                           PROPERTIES['ELEMENT_PROPERTIES'],
                           MODULE_INDEX,
                           METHOD_INDICES)

class Controller:
    def __init__(self,
             module_index,
             method_indices,
             controller_id,
             dictionary):
    
        self.__module_index = module_index
        self.__method_indices = method_indices
        self.__controller_id = controller_id
        self.__dictionary = dictionary

    def __repr__(self): return(str(self.id()))

    def id(self): return(self.__controller_id)
        
    def dictionary(self): return(self.__dictionary)

    def isLocked(self):
        
        newOperation(self.__module_index, self.__method_indices['isLocked'])
        PyTTXTalk.pushU8(self.__controller_id[0])
        sendPacket(1)

        return(PyTTXTalk.popU8())

    def target(self, value = None):
        
        newOperation(self.__module_index, self.__method_indices['target'])

        if (value != None): PyTTXTalk.pushF32(value);

        PyTTXTalk.pushU8(self.__controller_id[0])

        sendPacket(1);

        if (value == None): return(PyTTXTalk.popF32())
    
    def __cmp__(self, obj):
        return(cmp(self.__controller_id[0], obj.__controller_id[0]))

    def labels(self):
        return ('IsLocked', 'Target')
    
    def elements(self):
        data = [self.isLocked(),
                self.target(),
               ]
        return data

    def __methodIndices__(self):
        return self.__method_indices

    def __moduleIndex__(self):
        return self.__module_index

    def __controllerID__(self):
        return self.__controller_id
        
#class AnalogController(Controller):
#
#    def __init__(self,
#                 module_index,
#                 method_indices,
#                 controller_id,
#                 dictionary):
#
#        Controller.__init__(self,
#                 module_index,
#                 method_indices,
#                 controller_id,
#                 dictionary)
#
#
#    def targetOffset(self, value = None):
#
#        newOperation(self.__moduleIndex__(), self.__methodIndices__()['targetOffset'])
#
#        if (value != None): PyTTXTalk.pushF32(value);
#
#        PyTTXTalk.pushU8(self.id()[0])
#
#        sendPacket(1);
#
#        if (value == None): return(PyTTXTalk.popF32())
#
#    def labels(self):
#        l = list(Controller.labels(self))
#        l += ['targetOffset']
#        return (tuple(l))
#
#    def elements(self):
#        data = Controller.elements(self).append(self.targetOffset())
#        return data
        
class DualController(Controller):

    MODES = {0:'TRACK', 1:'SEEK'}
    
    def __init__(self,
                 module_index,
                 method_indices,
                 controller_id,
                 dictionary):
        
        Controller.__init__(self,
                 module_index,
                 method_indices,
                 controller_id,
                 dictionary)

    def seekDictionary(self): return(self.dictionary()['seek'])

    def trackDictionary(self): return(self.dictionary()['track'])

    def error(self):

        newOperation(self.__moduleIndex__(), self.__methodIndices__()['error'])
        PyTTXTalk.pushU8(self.__controllerID__()[0])
        sendPacket(1)
        return(PyTTXTalk.popF32())

    def mode(self):
        
        newOperation(self.__moduleIndex__(), self.__methodIndices__()['mode'])
        PyTTXTalk.pushU8(self.__controllerID__()[0])
        sendPacket(1)
        return(DualController.MODES[PyTTXTalk.popU8()])

    def variance(self):
        
        newOperation(self.__moduleIndex__(), self.__methodIndices__()['variance'])
        PyTTXTalk.pushU8(self.__controllerID__()[0])
        sendPacket(1)
        return(PyTTXTalk.popF32())

    def integratorValue(self):
        
        newOperation(self.__moduleIndex__(),
                     self.__methodIndices__()['integratorValue'])
        PyTTXTalk.pushU8(self.__controllerID__()[0])
        sendPacket(1)
        return(PyTTXTalk.popF32())

    def labels(self):
        l = list(Controller.labels(self))
        l += ['Error', 'IntegratorValue', 'Mode', 'Variance']
        return (tuple(l))
    
    def elements(self):
        data = Controller.elements(self)
        data += [self.error(),
                self.integratorValue(),
                self.mode(),
                self.variance()]
        return data
        
class SiBlockController(Controller):

    MODES = {0:'TEMPERATURE', 1:'CAVITY_LOCK'}
    
    def __init__(self,
                 module_index,
                 method_indices,
                 controller_id,
                 dictionary):
        
        Controller.__init__(self,
                 module_index,
                 method_indices,
                 controller_id,
                 dictionary)

    '''def error(self):

        newOperation(self.__moduleIndex__(), self.__methodIndices__()['siBlockError'])
        sendPacket(1)
        return(PyTTXTalk.popF32())

    def mode(self, value = None):

        newOperation(self.__moduleIndex__(), self.__methodIndices__()['slot'])
        
        if (value == None):        
            sendPacket(1)
            return(SiBlockController.MODES[PyTTXTalk.popU8()])

        PyTTXTalk.pushU8(value);
        sendPacket(1);

    def labels(self):
        l = list(Controller.labels(self))
        l += ['Error', 'IntegratorValue', 'Mode', 'Variance']
        return (tuple(l))
    
    def elements(self):
        data = Controller.elements(self)
        data += [self.error(),
                self.integratorValue(),
                self.mode(),
                self.variance()]
        return data
'''
