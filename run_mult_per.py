#Author MU
#Wavefrom aqcuisition from tektro oscilloscope
#from documentation : https://www.pyvisa.org/docs/tektronix-instruments

import os
import test_connexion as tc
import tek_aqui as ta
import time
#from utils import graph_utils as gu
from utils import files_utils as fu

# === VAR ===
On_channels=[1,2,3,4]
Acq_time_range=25e-6
Acq_Y_range=1
Acq_sample_rate= None
Trig_channel=1
Trig_level=0
Acq_channel=[2,3,4]
Acq_timeout=10

Run_time = 3600*24 

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
Data_Repo = "data"
Data_name = "rec.parquet"

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

            Lx,My = ta.wavefrom_acqui_multich(scope,Acq_channel,Acq_timeout)

            Data_name_t = (str(time.time() - t))+"_"+Data_name
            fu.save_mult_pqt(Lx,My,Path,Data_Repo,Data_name_t)
    

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
        print(f"Ni_err : {Ni_err}")
        time.sleep(10)