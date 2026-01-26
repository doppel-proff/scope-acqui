import pyvisa
import time

# Windows: Use NI-VISA backend
rm = pyvisa.ResourceManager()
instruments = rm.list_resources()
print(f"Found instruments: {instruments}")

if instruments :
    scope = rm.open_resource(instruments[0])
    scope.timeout = 5000 # time out de 5s
    #scope.encoding = 'latin_1'
    scope.read_termination = '\n'
    scope.write_termination = None
    scope.write('*cls') # clear ESR
    device_info = scope.query("*IDN?")
    print("Oscilloscope : ", {device_info})

    # Reset
    scope.write('*rst') 
    t1 = time.perf_counter()
    r = scope.query('*opc?') # sync
    t2 = time.perf_counter()
    print('reset time: {}'.format(t2 - t1))

    # Auto set
    scope.write('autoset EXECUTE') 
    t3 = time.perf_counter()
    r = scope.query('*opc?') # sync
    t4 = time.perf_counter()
    print('autoset time: {} s'.format(t4 - t3))

    # io setting

    scope.close()
rm.close()

print("ok")