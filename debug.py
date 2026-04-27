import pyvisa
import time

def open_rm():
    return pyvisa.ResourceManager()

def scope_init(rm):
    return rm.list_resources()
    

def open_scope(instr):
    return rm.open_resource(instr[0])

def set_and_check(cmd,quer,excpected):
    scope.write(cmd)
    val = scope.query(quer)
    print(f"{cmd} set to {val}")
    assert val.strip == excpected

if __name__ == "__main__":
    rm = open_rm()
    try :
        instr = scope_init(rm)
        print(instr)
        scope = rm.open_resource(str(instr[0]))
        print (scope)
        scope.write("*IDN?")
        print(scope.read())

        scope.write("DAT:ENC RIB")
        encoding = scope.query("DAT:ENC?")
        print(f"set encodind to : {encoding}")

        scope.write("DAT:WID 2")
        data_width = scope.query("DAT:WID?")
        print(f"bytes : {data_width}")

        scope.write("SEL:CH1 ON")
        state_chan_1 = scope.query("SEL:CH1?")
        print(f"channel 1 : {state_chan_1}")

        scope.write("SEL:CH2 ON")
        state_chan_2 = scope.query("SEL:CH2?")
        print(f"channel 2 : {state_chan_2}")

        scope.write("SEL:CH3 OFF")
        state_chan_3 = scope.query("SEL:CH3?")
        print(f"channel 3 : {state_chan_3}")

        scope.write("SEL:CH4 OFF")
        state_chan_4 = scope.query("SEL:CH4?")
        print(f"channel 4 : {state_chan_4}")

        scope.write("ACQ:MODE SAM")
        acq_mode = scope.query("ACQ:MODE?")
        print(f"acquisition mode : {acq_mode}")

        scope.write("TRIG:A:TYP EDGE")
        trig_type = scope.query("TRIG:A:TYP?")
        print(f"trigger type : {trig_type}")

        scope.write("TRIG:A:EDGE:SOU CH1")
        trig_chan = scope.query("TRIG:A:EDGE:SOU?")
        print(f"trigger on chan : {trig_chan}")

        scope.write("TRIG:A:LEV 0")
        trig_lvl = scope.query("TRIG:A:LEV?")
        print(f"trigger level : {trig_lvl[0]}")

        scope.write("TRIG:A:EDGE:SLO RISE")
        trig_edge = scope.query("TRIG:A:EDGE:SLO?")
        print(f"trigger edge : {trig_edge}")

        scope.write("ACQ:STATE STOP")
        acq_state = scope.query("ACQ:STATE?")
        print(f"acquisition state : {acq_state}")

        scope.write("DAT:SOU CH2")
        data_source = scope.query("DAT:SOU?")
        print(f"data source : {data_source}")

        scope.write("ACQ:STOPA SEQ")
        stop_squence = scope.query("ACQ:STOPA?")
        print(f"aqcuisition type : {stop_squence}")

        scope.write("ACQ:STATE RUN")
        acq_state = scope.query("ACQ:STATE?")
        print(f"acquisition state : {acq_state}")

        while scope.query("ACQ:STATE?").strip() != "0" :
            time.sleep(1e-3)

        acq_state = scope.query("ACQ:STATE?")
        print(f"acquisition state : {acq_state}")

        meta_data = scope.query("WFMP?")
        print(f"acquisition metadata = {meta_data}")

        scope.write("DAT:STAR 1")
        scope.write("DAT:STOP 25000")
        data_start = scope.query("DAT:STAR?")
        data_stop = scope.query("DAT:STOP?")
        print(f"data start : {data_start}")
        print(f"data stop : {data_stop}")

        data = scope.query_binary_values(
            "CURV?",
            datatype = "h",
            is_big_endian = True
        )

        print(data[:10])

    finally:
        if scope is not None :
            scope.clear()
            scope.close()
        if rm is not None:
            rm.close()