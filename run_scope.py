import os
import pyvisa
import time
import numpy as np
import polars as pl

import config as cf

Path = os.getcwd()
Data_repo = cf.Data_repo
os.makedirs(Data_repo, exist_ok=True)
Data_file = cf.Data_file

Run_Dur = cf.Run_Dur

On_channels = cf.On_channels
Trig_chanel = cf.Trig_channel
Rec_channels = cf.Rec_channels
Rec_channels_sca = cf.Rec_channels_sca

time_start = time.time()

def open_rm():
    return pyvisa.ResourceManager()

def scope_init(rm):
    return rm.list_resources()

def meta_data_dict (meta_data : str) -> dict :
    parts = meta_data.split(";")
    return {
            "BYT_NR": int(parts[0]),
            "BIT_NR": int(parts[1]),
            "ENCDG": parts[2],
            "BN_FMT": parts[3],
            "BYT_OR": parts[4],
            "WFID": parts[5],
            "NR_PT": int(parts[6]),
            "PT_FMT": parts[7],
            "XUNIT": parts[8],
            "XINCR": float(parts[9]),
            "XZERO": float(parts[10]),
            "PT_OFF": int(parts[11]),
            "YUNIT": parts[12],
            "YMULT": float(parts[13]),
            "YOFF": float(parts[14]),
            "YZERO": float(parts[15]),
            }

Chans = [1,2,3,4]

def run ():
    rm = open_rm()
    try :
        instr = scope_init(rm)
        print(instr)
        scope = rm.open_resource(str(instr[0]))
        print (scope)
        scope.write("*IDN?")
        print(scope.read())

        scope.write("DAT:ENC RIB")
        assert scope.query("DAT:ENC?").strip() == "RIBINARY"
        print(f"set encodind to : {scope.query("DAT:ENC?")}")

        scope.write("DAT:WID 2")
        assert scope.query("DAT:WID?").strip() == "2"
        print(f"bytes : {scope.query("DAT:ENC?")}")

        for chan in Chans :
            if chan in On_channels :
                scope.write(f"SEL:CH{chan} ON")
                assert scope.query(f"SEL:CH{chan}?").strip() == "1"
                print(f"channel {chan} : {scope.query(f"SEL:CH{chan}?")}")
            else :
                scope.write(f"SEL:CH{chan} OFF")
                assert scope.query(f"SEL:CH{chan}?").strip() == "0"
                print(f"channel {chan} : {scope.query(f"SEL:CH{chan}?")}")

        for i in range(len(Rec_channels)):
            scope.write(f"CH{Rec_channels[i]}:SCA {Rec_channels_sca[i]}")
            assert np.abs((float(scope.query(f"CH{Rec_channels[i]}:SCA?").strip()) - Rec_channels_sca[i] ))<= 1e-6 
            print(f"channel {Rec_channels[i]} scaling : {scope.query(f"CH{Rec_channels[i]}:SCA?")}")

        scope.write("ACQ:MODE SAM")
        assert scope.query("ACQ:MODE?").strip() == "SAMPLE"
        print(f"acquisition mode : {scope.query("ACQ:MODE?")}")

        scope.write("TRIG:A:TYP EDGE")
        assert scope.query("TRIG:A:TYP?").strip() == "EDGE"
        print(f"trigger type : {scope.query("TRIG:A:TYP?")}")

        scope.write("TRIG:A:EDGE:SOU CH1")
        assert scope.query("TRIG:A:EDGE:SOU?").strip() == "CH1"
        print(f"trigger on chan : {scope.query("TRIG:A:EDGE:SOU?")}")

        scope.write("TRIG:A:LEV 0")
        #assert np.abs (float(scope.query("TRIG:A:LEV?").strip())) < 1e-3
        print(f"trigger level : {scope.query("TRIG:A:LEV?")[0]}")

        scope.write("TRIG:A:EDGE:SLO RISE")
        assert scope.query("TRIG:A:EDGE:SLO?").strip() == "RISE"
        print(f"trigger edge : {scope.query("TRIG:A:EDGE:SLO?")}")

        scope.write("ACQ:STATE STOP")
        assert scope.query("ACQ:STATE?").strip() == "0" 
        print(f"acquisition state : {scope.query("ACQ:STATE?")}")

        scope.write("DAT:SOU CH2")
        assert scope.query("DAT:SOU?").strip() == "CH2"
        print(f"data source : {scope.query("DAT:SOU?")}")

        scope.write("HOR:MAIN:SCA 5E-3")
        scope.write("HOR:RECO MAX")
        record_len = int(scope.query("HOR:RECO?").strip())
        sample_rate = float(scope.query("HOR:MAI:SAMPLERATE?").strip())
        print(f"sampling rate : {sample_rate}")

        scope.write("ACQ:STOPA SEQ")
        assert scope.query("ACQ:STOPA?").strip() == "SEQUENCE"
        print(f"aqcuisition type : {scope.query("ACQ:STOPA?")}")

        counter = 0
        while (time.time() - time_start) < Run_Dur :
            scope.write("ACQ:STATE RUN")
            assert scope.query("ACQ:STATE?").strip() == "1"
            print(f"acquisition state : {scope.query("ACQ:STATE?")}")

            while scope.query("ACQ:STATE?").strip() != "0" :
                time.sleep(1e-3)

            acq_state = scope.query("ACQ:STATE?")
            print(f"acquisition state : {acq_state}")

            scope.write("DAT:STAR 1")
            scope.write(f"DAT:STOP {record_len}")
            assert scope.query("DAT:STAR?").strip() == "1"
            assert int(scope.query("DAT:STOP?")) == record_len
            print(f"data start : {scope.query("DAT:STAR?")}")
            print(f"data stop : {scope.query("DAT:STOP?")}")

            data_dict = {}
            for chan in Rec_channels :
                scope.write(f"DAT:SOU CH{chan}")
                assert scope.query("DAT:SOU?").strip() == f"CH{chan}"
                print(f"data source : {scope.query("DAT:SOU?")}")

                meta_data = scope.query("WFMP?")
                #print(f"acquisition metadata = {meta_data}")
                meta_dict = meta_data_dict(meta_data)

                ymult = meta_dict["YMULT"]
                yoff = meta_dict["YOFF"]
                yzero = meta_dict["YZERO"]

                data = np.array(scope.query_binary_values(
                    "CURV?",
                    datatype = "h",
                    is_big_endian = True
                ))

                data_dict[f"LyCH{chan}"] = (data - yoff) * ymult + yzero

            xincr = meta_dict["XINCR"]
            xzero = meta_dict["XZERO"]
            Lx = xzero + np.arange(len(data)) * xincr
            
            formatted_time = time.strftime("%Y-%m-%d %H-%M-%S",time.localtime())

            df = pl.DataFrame({
                "LT": formatted_time,
                "Lx":Lx,
                **data_dict
            })

            df = df.with_columns(pl.col("LT").str.strptime(pl.Datetime, "%Y-%m-%d %H-%M-%S"))

            print(df.tail(3))

            data_file_name = f"{Data_file}_{counter}_{formatted_time}"+".parquet"
            data_file_path = os.path.join(Data_repo,data_file_name)
            df.write_parquet(data_file_path)
            print(f"measurements saved @ : {data_file_path}")


            counter += 1
            time.sleep(20)
        print("\n --- Run ended --- \n")
    finally:
        if scope is not None :
            scope.clear()
            scope.close()
        if rm is not None:
            rm.close()

N_err = 0
err_row = []
err_cols = ["nb err", "date and time", "error message"]
if __name__ == "__main__":
    while True :
        try : 
            run()
        except Exception as err :
            N_err  += 1
            print(f"Nb error : {N_err}")
            err_row.append([str(N_err), str(time.strftime("%Y-%m-%d %H-%M-%S",time.localtime())), str(err)])
            df_error = pl.DataFrame(err_row, schema=err_cols)
            err_log_repo = os.path.join(Path, "error_log")
            os.makedirs(err_log_repo, exist_ok=True) 
            error_log_file = os.path.join(err_log_repo,f"error_log.csv")
            df_error.write_csv(error_log_file)
            time.sleep(5)