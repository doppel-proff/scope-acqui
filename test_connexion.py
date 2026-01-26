#Author MU
#Objectitive connecting to a MSO44B oscilloscope
#from documentation : https://www.pyvisa.org/docs/tektronix-instruments

import pyvisa

def open_rm():
    return pyvisa.ResourceManager()

def scope_init(rm):
    instruments = rm.list_resources()
    print(f"Found intruments: {instruments}")
    if instruments :
        scope = rm.open_resource(instruments[0])

        scope.timeout = 2e4 #10s timeout
        scope.write('*RST') #reset
        scope.write('*CLS') #clear status
        #scope.timeout = 2e4
        #scope.write('*RST')
        #scope.query('*OPC?')
        #scope.write('*CLS')

        return(scope)
    else : 
        print("No instruments found")

def close(scope,rm):
    try:
        if scope is not None:
            scope.clear()
            scope.close()
    finally:
        if rm is not None:
            rm.close()
    print("closed : " + str(scope))

rm = open_rm()
try :
    scope = scope_init(rm)
finally :
    close(scope,rm)