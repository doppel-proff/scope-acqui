#Author MU
#Objectitive connecting to a MSO44B oscilloscope
#from documentation : https://www.pyvisa.org/docs/tektronix-instruments

import pyvisa

#returns 
def scope_init():
    rm = pyvisa.ResourceManager()
    instruments = rm.list_resources()
    print(f"Found intruments: {instruments}")
    if instruments :
        scope = rm.open_resource(instruments[0])

        scope.timeout = 1e4 #10s timeout
        scope.write('*RST') #reset
        scope.write('*CLS') #clear status

        return(scope)
    else : 
        print("No instruments found")

def close(scope):
    rm = pyvisa.ResourceManager()
    scope.close()
    rm.close()
    print("closed : " + str(scope))

scope=scope_init()
print(type(scope))
print("Connected to " + str(scope))
close(scope)