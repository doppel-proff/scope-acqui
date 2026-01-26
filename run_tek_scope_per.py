#Author MU
#Wavefrom aqcuisition from tektro oscilloscope
#from documentation : https://www.pyvisa.org/docs/tektronix-instruments

import os
import test_connexion as tc
import time
import tek_aqui as ta
from utils import graph_utils as gu
from utils import files_utils as fu

# === VAR ===
On_channels=[1]
Acq_time_range=1e-1
Acq_Y_range=1
Acq_sample_rate= None
Trig_channel=1
Trig_level=0
Acq_channel=1
Acq_timeout=10

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
Data_name = "rec.csv"

# === VAR ===

# === RUN ===
t = time.time()
while time.time() - t < 60 :
    rm = tc.open_rm()
    try :
        scope = tc.scope_init(rm)

        ta.encod(scope)

        ta.acqui_conf(scope,On_channels,Acq_time_range,Acq_Y_range,Acq_sample_rate)

        ta.trig_conf(scope,Trig_channel,Trig_level)

        Lx,Ly = ta.wavefrom_acqui(scope,Acq_channel,Acq_timeout)
    
        Data_name_t = str(time.time() - t)+"_"+Data_name
        fu.save_tuple_csv(Lx,Ly,Path,Data_Repo,Data_name_t)

    finally :
        tc.close(scope,rm)

    time.sleep(1)
    t=t+1
    print("... ... ...")

print("Done.")
print(f"data saved to {Path}/{Data_Repo}")
