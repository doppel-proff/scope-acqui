#Author MU
#Wavefrom aqcuisition from tektro oscilloscope
#from documentation : https://www.pyvisa.org/docs/tektronix-instruments

import pyvisa
import time
import numpy as np
import test_connexion as tc

#Sets encoding to scope --ok.
def encod(scope):
    scope.write('DAT:ENC RIB')
    scope.write('DAT:WID 2')
    #scope.write('DAT:ENC ASC')
    scope.write('VERB OFF')
    print("Set encoding to : " + str(scope))

#Sets acquisition parameters --ok.
def acqui_conf(scope,channels,time_range,Y_range,sample_rate):
    for i in range (1 ,5):
        if i in channels :
            scope.write(f'SEL:CH{i} ON')
            print(f'CH{i} ON') # -- ok
            scope.write(f'CH{i}:SCA {Y_range}')
        else :
            scope.write(f'SEL:CH{i} OFF')
            print(f'CH{i} OFF') #-- ok
    scope.write(f'HOR:SCA {time_range}')
    print(f"set record length to {time_range} s / div")
    if sample_rate:
        scope.write(f'HOR:SAM {sample_rate}')
        print(f"set sample rate to {sample_rate} Hz")
    scope.write('ACQ:MODE SAM')
    print("set to sample mod")
    scope.write('ACQ:STPOA SEQ')
    print("set to single") # -- ok

#Sets up trigger --ok.
def trig_conf(scope, channel, level):
    scope.write('TRIG:MAI:TYP EDGE')
    scope.write(f'TRIG:MAI:EDGE:SOU CH{channel}')
    scope.write(f'TRIG:MAI:LEV {level}')
    scope.write(f'TRIG:MAI:EDGE:SLO RISE')
    print("set trigger")

def wavefrom_acqui(scope, channel, timeout):
    scope.write(f'DAT:SOU CH{channel}')
    #scope.write('ACQ:STOPA SEQ')
    scope.write('ACQ:STATE RUN')
    scope.query("*OPC?")
    #scope.write('TRIG:FORC')
    time.sleep(0.3)
    scope.write('ACQ:STOPA SEQ')

    #trigger timeout  --ok.
    st_time=time.time()
    while time.time() - st_time < timeout:
        state = scope.query('ACQ:STATE?').strip()
        #print(f"state :{state}")
        if state == '0':  # Acquisition stopped
            print("triggered")
            break
        time.sleep(0.1)
    else:
        #tc.close(scope)
        raise TimeoutError("Acquisition timeout")
    preamble=scope.query('WFMP?').split(',') #signal meta data
    #print(preamble)
    #print(len(preamble))
    y_scale = 156.25e-6
    y_offset = 0
    y_position = 0

    x_scale = 40e-9
    x_offset = 22.4e-9
    scope.write('DAT:STAR 1')
    scope.write(('DAT:STOP 250000'))
    raw_data = scope.query_binary_values('CURV?', datatype='h', is_big_endian=True )
    #raw_data = scope.query_ascii_values('CURV?') # -- Ok.
    Ly = ((np.array(raw_data) - y_offset) * y_scale) + y_position
    Nb_pt = len(raw_data)
    print(f"Nb_pt : {Nb_pt}")
    Lx = np.arange(Nb_pt) * x_scale + x_offset
    return(Lx,Ly)

#Channel is an array containing measuerd channels.
def wavefrom_acqui_multich(scope, channels, timeout):
    #scope.write('ACQ:STOPA SEQ')
    scope.write('ACQ:STATE RUN')
    scope.query("*OPC?")
    #scope.write('TRIG:FORC')
    time.sleep(0.3)
    scope.write('ACQ:STOPA SEQ')

    #trigger timeout  --ok.
    st_time=time.time()
    while time.time() - st_time < timeout:
        state = scope.query('ACQ:STATE?').strip()
        #print(f"state :{state}")
        if state == '0':  # Acquisition stopped
            print("triggered")
            break
        time.sleep(0.1)
    else:
        #tc.close(scope)
        raise TimeoutError("Acquisition timeout")
    My=[]
    for i in channels :
        scope.write(f'DAT:SOU CH{i}')
        preamble=scope.query('WFMP?').split(',') #signal meta data
        print(preamble)
        #print(len(preamble))
        y_scale = 156.25e-6
        y_offset = 0
        y_position = 0

        x_scale = 160e-9
        x_offset = 6.4e-9
        scope.write('DAT:STAR 1')
        scope.write(('DAT:STOP 2500'))
        raw_data = scope.query_binary_values('CURV?', datatype='h', is_big_endian=True )
        #raw_data = scope.query_ascii_values('CURV?') # -- Ok.
        Ly = ((np.array(raw_data) - y_offset) * y_scale) + y_position
        My.append(Ly)
    Nb_pt = len(raw_data)
    print(f"Nb_pt : {Nb_pt}")
    Lx = np.arange(Nb_pt) * x_scale + x_offset
    return(Lx,My)