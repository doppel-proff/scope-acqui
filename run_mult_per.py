#Author MU
#Wavefrom aqcuisition from tektro oscilloscope
#from documentation : https://www.pyvisa.org/docs/tektronix-instruments

import os
import test_connexion as tc
import tek_aqui as ta
import time
import pandas as pd 
from datetime import datetime

from utils import files_utils as fu
from utils import list_utils as lu

# === VAR ===
On_channels=[1,2,3,4]
Acq_time_range=25e-5
Acq_Y_range=10
Acq_sample_rate= None
Trig_channel=1
Trig_level=0
Acq_channel=[2,3,4]
Acq_timeout=10

Run_time = 3600*24*7 

start_time = time.time()

# = GRAPH =
Path = os.getcwd()
Graph_Repo = "graph_oscillo"
Fig_name = ["Acqui_oscillo"]
Y_axe = ["Tension"]
X_axe = ["temps"]
Y_min = None
Y_max = None
X_min = None
X_max = None

# = DATA =
Data_Repo = "data_TR26_0011_run2"
Data_name = "TR26_0011_run2.parquet"

# = Error =
cols = ["time", "err_message"]
rows = []
error_log_repo = os.path.join(Path, Data_Repo+"error_log")
os.makedirs(error_log_repo,exist_ok=True)
errr_log_file_path = os.path.join(error_log_repo, "error_log.csv")
# === VAR ===

# === FUNC ===
def run(Run_time):
    t = time.time()
    rm = tc.open_rm()
    while time.time() - t < Run_time :
        try :
            scope = tc.scope_init(rm)

            ta.encod(scope)

            ta.acqui_conf(scope,On_channels,Acq_time_range,Acq_Y_range,Acq_sample_rate)

            ta.trig_conf(scope,Trig_channel,Trig_level)

            Lx, My, L_Ts = ta.wavefrom_acqui_multich(scope,Acq_channel,start_time,Acq_timeout)

            Time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            Data_name_t = f"{Data_name}_{Time_stamp}.parquet"
            fu.save_mult_pqt(Lx,My,L_Ts,Path,Data_Repo,Data_name_t)
    

        finally :
            print("... ... ...")
            time.sleep(20)

    tc.close(scope,rm)

    print("Done.")
    print(f"data saved to {Path}/{Data_Repo}")

    return(True)

# === RUN ===
Ni_err = 0
while True :
    try:
        run(Run_time)
        Ni_err = 0
    except Exception as e :
        Ni_err += 1
        rows.append([datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), e])
        df_error = pd.DataFrame(data=rows, columns=cols)
        df_error.to_csv(errr_log_file_path)
        print(f"Ni_err : {Ni_err}")
        time.sleep(10)