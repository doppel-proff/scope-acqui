import pyvisa

rm = pyvisa.ResourceManager()
instruments = rm.list_resources()
print(f"Found instruments: {instruments}")

if instruments:

    scope = rm.open_resource(instruments[0])
print(scope)