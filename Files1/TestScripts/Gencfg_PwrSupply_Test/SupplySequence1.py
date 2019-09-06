
def P3_3ONF(delay):


    #import sys 
    #sys.path.append(r'C:\Documents and Settings\rcanwa-lltltest\Desktop\ITLA2TestCode2')
    #sys.path.append(r'C:\Documents and Settings\rcanwa-lltltest\Desktop\LUX\pCode')
    import InstrumentDrivers_DS as inst
    import time as tt
    
   
    P3_3ON = inst.HP3631A(0,1)
    P5_2ON = inst.HP3631A(0,10)
    P3_3ON.connect()
    P5_2ON.connect()
    tt.sleep(5)

    P3_3ON.setOutputState('ON')
    tt.sleep(delay)
    P5_2ON.setOutputState('ON')
    
    
    
    P3_3ON.disconnect()
    P5_2ON.disconnect()

def P5_2V_ONF(delay):


    #import sys 
    #sys.path.append(r'C:\Documents and Settings\rcanwa-lltltest\Desktop\ITLA2TestCode2')
    #sys.path.append(r'C:\Documents and Settings\rcanwa-lltltest\Desktop\LUX\pCode')
    import InstrumentDrivers_DS as inst
    import time as tt
    
   
    P3_3ON = inst.HP3631A(0,1)
    P5_2ON = inst.HP3631A(0,10)
    P3_3ON.connect()
    P5_2ON.connect()

    P5_2ON.setOutputState('ON')    
    tt.sleep(delay)
    P3_3ON.setOutputState('ON')
        
    P3_3ON.disconnect()
    P5_2ON.disconnect()

def POFF():


    #import sys 
    #sys.path.append(r'C:\Documents and Settings\rcanwa-lltltest\Desktop\ITLA2TestCode2')
    #sys.path.append(r'C:\Documents and Settings\rcanwa-lltltest\Desktop\LUX\pCode')
    import InstrumentDrivers_DS as inst
    import time as tt
    
   
    P3_3ON = inst.HP3631A(0,1)
    P5_2ON = inst.HP3631A(0,10)
    P3_3ON.connect()
    P5_2ON.connect()

    P5_2ON.setOutputState('OFF')    
    P3_3ON.setOutputState('OFF')
        
    P3_3ON.disconnect()
    P5_2ON.disconnect()   