0# This module configures and controls the unused SPI pins on the Aardvark dongle as GPIO

import sys
from aardvark_py import *
from array import *
import time

# GPIO bit mask and pin definition:
GPIO_SCL = 0x01 # pin1, 
GPIO_SDA = 0x02 # pin3, 
GPIO_MISO = 0x04 # pin5
GPIO_SCK = 0x08 # pin7
GPIO_MOSI = 0x10 # pin8
GPIO_SS = 0x20 # pin9



class gpio:
    def __init__(self,port=0,handle=None,aardvark_id=None):
        if handle != None:
            print 'Shared handle has been passed to GPIO connection...'
            self.aard_handle = handle
        elif aardvark_id != None:
            print 'User supplied unique id, looking for port...'
            (intReturn, devices, unique_ids) = aa_find_devices_ext(32,32)
            if intReturn < 1:
                print 'No aardvark devices connected'
            else:
                for i in unique_ids:
                    n = 0
                    if i == self.aard_id:
                        self.aard_port = devices[n]
                        print 'Found unique id %d at port %d' % (i, devices[n])
                    n += 1
                self.open()
        else:
            self.aard_port = port
            self.open()

        # IO dictionary, 0 is input, 1 is output
        self.dicIOConfig = {'scl' : 1,
                            'sda' : 1,
                            'miso' : 1,
                            'sck' : 1,
                            'mosi' : 1,
                            'ss' : 1}

        self.dicOutPinState = {'scl' : 0,
                            'sda' : 0,
                            'miso' : 0,
                            'sck' : 0,
                            'mosi' : 0,
                            'ss' : 0}

        self.configure()

    def open(self):
        self.aard_handle = aa_open(self.aard_port)
            
    def close(self):
        aa_close(self.aard_handle)

    def configure(self):
        direction_mask = (self.dicIOConfig['scl']*GPIO_SCL | \
                          self.dicIOConfig['sda']*GPIO_SDA | \
                          self.dicIOConfig['miso']*GPIO_MISO | \
                          self.dicIOConfig['sck']*GPIO_SCK | \
                          self.dicIOConfig['mosi']*GPIO_MOSI | \
                          self.dicIOConfig['ss']*GPIO_SS)

        aa_configure(self.aard_handle,AA_CONFIG_GPIO_ONLY)
        aa_gpio_direction(self.aard_handle,direction_mask)
        

    def setInOut(self,intPin,strDirection):
        if strDirection.upper() == 'IN':
            intDirection = 0
        else:
            intDirection = 1
        if intPin == 1:
            self.dicIOConfig['scl'] = intDirection
        elif intPin == 3:
            self.dicIOConfig['sda'] = intDirection
        elif intPin == 5:
            self.dicIOConfig['miso'] = intDirection
        elif intPin == 7:
            self.dicIOConfig['sck'] = intDirection
        elif intPin == 8:
            self.dicIOConfig['mosi'] = intDirection
        elif intPin == 9:
            self.dicIOConfig['ss'] = intDirection
        else:
            raise gpioError('Invalid GPIO pin designation.')
        self.configure()

    def setOutputState(self,intPin,intState):
        if intPin == 1:
            self.dicOutPinState['scl'] = intState
        elif intPin == 3:
            self.dicOutPinState['sda'] = intState
        elif intPin == 5:
            self.dicOutPinState['miso'] = intState
        elif intPin == 7:
            self.dicOutPinState['sck'] = intState
        elif intPin == 8:
            self.dicOutPinState['mosi'] = intState
        elif intPin == 9:
            self.dicOutPinState['ss'] = intState
        else:
            raise gpioError('Invalid GPIO pin designation.')
    
        
        output_mask = (self.dicOutPinState['scl']*GPIO_SCL | \
                       self.dicOutPinState['sda']*GPIO_SDA | \
                       self.dicOutPinState['miso']*GPIO_MISO | \
                       self.dicOutPinState['sck']*GPIO_SCK | \
                       self.dicOutPinState['mosi']*GPIO_MOSI | \
                       self.dicOutPinState['ss']*GPIO_SS)
        
        aa_gpio_set(self.aard_handle,output_mask)

    def readOutputState(self,intPin):
 
        
        pinRead = aa_gpio_get(self.aard_handle)
        print pinRead

    def InitPin(self):
        self.setInOut(1,'OUT')#LDIS_N
        self.setInOut(3,'OUT')#LDIS1_N
        self.setInOut(5,'OUT')#RST_N
        self.setInOut(7,'OUT')#MODSEL_N
        self.setInOut(8,'OUT')#MODSEL1_N
        self.setInOut(9,'IN') #SRQT
        self.configure()
        self.setOutputState(1,1)
        self.setOutputState(3,1)
        self.setOutputState(5,1)
        self.setOutputState(7,1)
        self.setOutputState(8,1)
        self.setOutputState(9,0)
        
    def LDIS_N_Enable(self):
        pinNO = 1
        return self.setOutputState(pinNO,1)
    
    def LDIS_N_Disable(self):
        pinNO = 1
        return self.setOutputState(pinNO,0)
    
    def LDIS1_N_Enable(self):
        pinNO = 3
        return self.setOutputState(pinNO,1)
    
    def LDIS1_N_Disable(self):
        pinNO = 3
        return self.setOutputState(pinNO,0)
    
    def reset(self,delay=0.0):
        self.setOutputState(5,0)
        time.sleep(delay)
        self.setOutputState(5,1)
        
    def reset_toggleOn(self):
        self.setOutputState(5,0)

    def reset_toggleOff(self):
        self.setOutputState(5,1)        
        
    def MODSEL_N_Enable(self):
        pinNO = 7
        return self.setOutputState(pinNO,1)
    
    def MODSEL_N_Disable(self):
        pinNO = 7
        return self.setOutputState(pinNO,0)

    def MODSEL1_N_Enable(self):
        pinNO = 8
        return self.setOutputState(pinNO,1)
    
    def MODSEL1_N_Disable(self):
        pinNO = 8
        return self.setOutputState(pinNO,0)
    
    def readSRQT(self):
        pinNO = 9
        return self.readOutputState(pinNO)


    def setLaser(self):
        self.setInOut(1,'OUT')
        self.configure()
        self.setOutputState(1,1)
        time.sleep(3)
        self.setOutputState(1,0)

    def setPin(self,pinNO):
        self.setInOut(pinNO,'OUT')
        self.configure()
        self.setOutputState(pinNO,1)
        time.sleep(3)
        self.setOutputState(pinNO,0)
        


     
        
        
        
        
        
# todo: create get inputState function 
        


class gpioError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)